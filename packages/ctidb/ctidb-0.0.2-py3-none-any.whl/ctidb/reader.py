"""
ctidb.reader

This module contains the pure Python database reader and related classes.

"""
import os

try:
    import mmap
except ImportError:
    # pylint: disable=invalid-name
    mmap = None  # type: ignore

import ipaddress
import struct
from typing import AnyStr, Any, Optional, Tuple, Union, List, Dict, cast

Primitive = Union[AnyStr, bool, float, int]
Record = Union[Primitive, "RecordList", "RecordDict"]

MODE_AUTO = 0
MODE_MEMORY = 8

class CCtiReader:
    """
    Instances of this class provide a reader for the cti DB format. IP
    addresses can be looked up using the ``get`` method.
    """

    _DATA_SECTION_SEPARATOR_SIZE = 16
    _METADATA_START_MARKER = b"\x44\x48\x43AISpera.com"

    _buffer: mmap.mmap

    def __init__(
        self, database: str,
        mode: int = MODE_AUTO
    ) -> None:
        """Reader for the cti DB file format

        Arguments:
        database -- A path to a valid cti DB file such as a GeoIP2 database file.
        mode -- mode to open the database with. Valid mode are:
            * MODE_MEMORY - load database into memory.
            * MODE_AUTO - tries MODE_MMAP and then MODE_FILE. Default.
        """

        if not os.path.exists(database):
            raise InvalidDatabaseError(
                f"Error finding database file ({database}).")

        if mode == MODE_AUTO and mmap:
            with open(database, "rb") as db_file:  # type: ignore
                self._buffer = mmap.mmap(db_file.fileno(), 0, access=mmap.ACCESS_READ)
                self._buffer_size = self._buffer.size()
        elif mode == MODE_MEMORY:
            with open(database, "rb") as db_file:  # type: ignore
                self._buffer = db_file.read()
                self._buffer_size = len(self._buffer)
        else:
            raise ValueError(
                f"Unsupported open mode ({mode}). Only MODE_AUTO, "
                "MODE_MEMORY are supported by the pure Python Reader")

        filename = database
        metadata_start = self._buffer.rfind(
            self._METADATA_START_MARKER, max(0, self._buffer_size - 128 * 1024)
        )
        if metadata_start == -1:
            self.close()
            raise InvalidDatabaseError(
                f"Error opening database file ({filename}). "
                "Is this a valid cti DB file?")

        metadata_start += len(self._METADATA_START_MARKER)
        metadata_decoder = Decoder(self._buffer, metadata_start)
        (metadata, _) = metadata_decoder.decode(metadata_start)
        if not isinstance(metadata, dict):
            raise InvalidDatabaseError(
                f"Error reading metadata in database file ({filename})."
            )

        self._metadata = Metadata(**metadata)  # pylint: disable=bad-option-value
        self._decoder = Decoder(
            self._buffer,
            self._metadata.search_tree_size + self._DATA_SECTION_SEPARATOR_SIZE,
        )
        self.closed = False

    def metadata(self) -> "Metadata":
        """Return the metadata associated with the cti DB file"""
        return self._metadata

    def get(self, ip_address: str) -> Optional[Record]:
        """Return the record for the ip_address in the cti DB

        Arguments:
        ip_address -- an IP address in the standard string notation
        """
        if not isinstance(ip_address, str):
            raise TypeError("argument 1 must be a string")

        try:
            address = ipaddress.ip_address(ip_address)
            packed_address = bytearray(address.packed)
        except AttributeError as ex:
            raise TypeError("argument 1 must be a string or ipaddress object") from ex
        if address.version == 6:
            raise ValueError(
                f"Error looking up {ip_address}. You attempted to look up "
                "an IPv6 address in an IPv4-only database.")

        (pointer, prefix_len) = self._find_address_in_tree(packed_address)
        if not pointer:
            return None

        return self._resolve_data_pointer(pointer)

    def _find_address_in_tree(self, packed: bytearray) -> Tuple[int, int]:
        bit_count = len(packed) * 8
        node = 0
        node_count = self._metadata.node_count

        i = 0
        while i < bit_count and node < node_count:
            bit = 1 & (packed[i >> 3] >> 7 - (i % 8))
            node = self._read_node(node, bit)
            i = i + 1

        if node == node_count:
            # Record is empty
            return 0, i
        if node > node_count:
            return node, i

        raise InvalidDatabaseError("Invalid node in search tree")

    def _read_node(self, node_number: int, index: int) -> int:
        base_offset = node_number * self._metadata.node_byte_size

        record_size = self._metadata.record_size
        if record_size == 24:
            offset = base_offset + index * 3
            node_bytes = b"\x00" + self._buffer[offset : offset + 3]
        elif record_size == 28:
            offset = base_offset + 3 * index
            node_bytes = bytearray(self._buffer[offset : offset + 4])
            if index:
                node_bytes[0] = 0x0F & node_bytes[0]
            else:
                middle = (0xF0 & node_bytes.pop()) >> 4
                node_bytes.insert(0, middle)
        elif record_size == 32:
            offset = base_offset + index * 4
            node_bytes = self._buffer[offset : offset + 4]
        else:
            raise InvalidDatabaseError(f"Unknown record size: {record_size}")
        return struct.unpack(b"!I", node_bytes)[0]

    def _resolve_data_pointer(self, pointer: int) -> Record:
        resolved = pointer - self._metadata.node_count + self._metadata.search_tree_size

        if resolved >= self._buffer_size:
            raise InvalidDatabaseError("The cti DB file's search tree is corrupt")

        (data, _) = self._decoder.decode(resolved)
        return data

    def close(self) -> None:
        """Closes the cti DB file and returns the resources to the system"""
        try:
            self._buffer.close()  # type: ignore
        except AttributeError:
            pass
        self.closed = True

    def __exit__(self, *args) -> None:
        self.close()

    def __enter__(self) -> "Reader":
        if self.closed:
            raise ValueError("Attempt to reopen a closed cti DB")
        return self

class Decoder:  # pylint: disable=too-few-public-methods
    """Decoder for the data section of the MaxMind DB"""

    def __init__(
        self,
        database_buffer: mmap.mmap,
        pointer_base: int = 0,
        pointer_test: bool = False,
    ) -> None:
        """Created a Decoder for a MaxMind DB

        Arguments:
        database_buffer -- an mmap'd MaxMind DB file.
        pointer_base -- the base number to use when decoding a pointer
        pointer_test -- used for internal unit testing of pointer code
        """
        self._pointer_test = pointer_test
        self._buffer = database_buffer
        self._pointer_base = pointer_base

    def _decode_array(self, size: int, offset: int) -> Tuple[List[Record], int]:
        array = []
        for _ in range(size):
            (value, offset) = self.decode(offset)
            array.append(value)
        return array, offset

    def _decode_boolean(  # pylint: disable=no-self-use
        self, size: int, offset: int
    ) -> Tuple[bool, int]:
        return size != 0, offset

    def _decode_bytes(self, size: int, offset: int) -> Tuple[bytes, int]:
        new_offset = offset + size
        return self._buffer[offset:new_offset], new_offset

    def _decode_double(self, size: int, offset: int) -> Tuple[float, int]:
        self._verify_size(size, 8)
        new_offset = offset + size
        packed_bytes = self._buffer[offset:new_offset]
        (value,) = struct.unpack(b"!d", packed_bytes)
        return value, new_offset

    def _decode_float(self, size: int, offset: int) -> Tuple[float, int]:
        self._verify_size(size, 4)
        new_offset = offset + size
        packed_bytes = self._buffer[offset:new_offset]
        (value,) = struct.unpack(b"!f", packed_bytes)
        return value, new_offset

    def _decode_int32(self, size: int, offset: int) -> Tuple[int, int]:
        if size == 0:
            return 0, offset
        new_offset = offset + size
        packed_bytes = self._buffer[offset:new_offset]

        if size != 4:
            packed_bytes = packed_bytes.rjust(4, b"\x00")
        (value,) = struct.unpack(b"!i", packed_bytes)
        return value, new_offset

    def _decode_map(self, size: int, offset: int) -> Tuple[Dict[str, Record], int]:
        container: Dict[str, Record] = {}
        for _ in range(size):
            (key, offset) = self.decode(offset)
            (value, offset) = self.decode(offset)
            container[cast(str, key)] = value
        return container, offset

    def _decode_pointer(self, size: int, offset: int) -> Tuple[Record, int]:
        pointer_size = (size >> 3) + 1

        buf = self._buffer[offset : offset + pointer_size]
        new_offset = offset + pointer_size

        if pointer_size == 1:
            buf = bytes([size & 0x7]) + buf
            pointer = struct.unpack(b"!H", buf)[0] + self._pointer_base
        elif pointer_size == 2:
            buf = b"\x00" + bytes([size & 0x7]) + buf
            pointer = struct.unpack(b"!I", buf)[0] + 2048 + self._pointer_base
        elif pointer_size == 3:
            buf = bytes([size & 0x7]) + buf
            pointer = struct.unpack(b"!I", buf)[0] + 526336 + self._pointer_base
        else:
            pointer = struct.unpack(b"!I", buf)[0] + self._pointer_base

        if self._pointer_test:
            return pointer, new_offset
        (value, _) = self.decode(pointer)
        return value, new_offset

    def _decode_uint(self, size: int, offset: int) -> Tuple[int, int]:
        new_offset = offset + size
        uint_bytes = self._buffer[offset:new_offset]
        return int.from_bytes(uint_bytes, "big"), new_offset

    def _decode_utf8_string(self, size: int, offset: int) -> Tuple[str, int]:
        new_offset = offset + size
        return self._buffer[offset:new_offset].decode("utf-8"), new_offset

    _type_decoder = {
        1: _decode_pointer,
        2: _decode_utf8_string,
        3: _decode_double,
        4: _decode_bytes,
        5: _decode_uint,  # uint16
        6: _decode_uint,  # uint32
        7: _decode_map,
        8: _decode_int32,
        9: _decode_uint,  # uint64
        10: _decode_uint,  # uint128
        11: _decode_array,
        14: _decode_boolean,
        15: _decode_float,
    }

    def decode(self, offset: int) -> Tuple[Record, int]:
        """Decode a section of the data section starting at offset

        Arguments:
        offset -- the location of the data structure to decode
        """
        new_offset = offset + 1
        ctrl_byte = self._buffer[offset]
        type_num = ctrl_byte >> 5
        # Extended type
        if not type_num:
            (type_num, new_offset) = self._read_extended(new_offset)

        try:
            decoder = self._type_decoder[type_num]
        except KeyError as ex:
            raise InvalidDatabaseError(
                f"Unexpected type number ({type_num}) encountered"
            ) from ex

        (size, new_offset) = self._size_from_ctrl_byte(ctrl_byte, new_offset, type_num)
        return decoder(self, size, new_offset)

    def _read_extended(self, offset: int) -> Tuple[int, int]:
        next_byte = self._buffer[offset]
        type_num = next_byte + 7
        if type_num < 7:
            raise InvalidDatabaseError(
                "Something went horribly wrong in the decoder. An "
                f"extended type resolved to a type number < 8 ({type_num})"
            )
        return type_num, offset + 1

    @staticmethod
    def _verify_size(expected: int, actual: int) -> None:
        if expected != actual:
            raise InvalidDatabaseError(
                "The MaxMind DB file's data section contains bad data "
                "(unknown data type or corrupt data)"
            )

    def _size_from_ctrl_byte(
        self, ctrl_byte: int, offset: int, type_num: int
    ) -> Tuple[int, int]:
        size = ctrl_byte & 0x1F
        if type_num == 1 or size < 29:
            return size, offset

        if size == 29:
            size = 29 + self._buffer[offset]
            return size, offset + 1

        # Using unpack rather than int_from_bytes as it is faster
        # here and below.
        if size == 30:
            new_offset = offset + 2
            size_bytes = self._buffer[offset:new_offset]
            size = 285 + struct.unpack(b"!H", size_bytes)[0]
            return size, new_offset

        new_offset = offset + 3
        size_bytes = self._buffer[offset:new_offset]
        size = struct.unpack(b"!I", b"\x00" + size_bytes)[0] + 65821
        return size, new_offset

class Metadata:
    """Metadata for the cti DB reader

    .. attribute:: binary_format_major_version
      The major version number of the binary format used when creating the
      database.
      :type: int

    .. attribute:: binary_format_minor_version
      The minor version number of the binary format used when creating the
      database.
      :type: int

    .. attribute:: build_epoch
      The Unix epoch for the build time of the database.
      :type: int

    .. attribute:: database_type
      A string identifying the database type
      :type: str

    .. attribute:: description
      A map from locales to text descriptions of the database.
      :type: dict(str, str)

    .. attribute:: languages
      A list of locale codes supported by the databse.
      :type: list(str)

    .. attribute:: node_count
      The number of nodes in the database.
      :type: int

    .. attribute:: record_size
      The bit size of a record in the search tree.
      :type: int
    """

    def __init__(self, **kwargs) -> None:
        """Creates new Metadata object. kwargs are key/value pairs from spec"""
        # Although I could just update __dict__, that is less obvious and it
        # doesn't work well with static analysis tools and some IDEs
        self.node_count = kwargs["node_count"]
        self.record_size = kwargs["record_size"]
        self.database_type = kwargs["database_type"]
        self.languages = kwargs["languages"]
        self.binary_format_major_version = kwargs["binary_format_major_version"]
        self.binary_format_minor_version = kwargs["binary_format_minor_version"]
        self.build_epoch = kwargs["build_epoch"]
        self.description = kwargs["description"]
        # self.alias = kwargs["alias"]
        # self.license = kwargs["license"]

    @property
    def node_byte_size(self) -> int:
        """The size of a node in bytes

        :type: int
        """
        return self.record_size // 4

    @property
    def search_tree_size(self) -> int:
        """The size of the search tree

        :type: int
        """
        return self.node_count * self.node_byte_size

    def __repr__(self):
        args = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{self.__module__}.{self.__class__.__name__}({args})"

class InvalidDatabaseError(RuntimeError):
    """This error is thrown when unexpected data is found in the database."""

class RecordList(List[Record]):  # pylint: disable=too-few-public-methods
    """
    RecordList is a type for lists in a database record.
    """

class RecordDict(Dict[str, Record]):  # pylint: disable=too-few-public-methods
    """
    RecordDict is a type for dicts in a database record.
    """