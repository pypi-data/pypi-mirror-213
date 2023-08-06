"""
ctidb.reader

This module contains the pure Python database reader and related classes.

"""
import os
import time
import hashlib

try:
    import mmap
except ImportError:
    # pylint: disable=invalid-name
    mmap = None  # type: ignore

import ipaddress
import struct
from typing import AnyStr, Any, Optional, Tuple, Union, List, Dict, cast

from .custom import Record, InvalidDatabaseError
from .decoder import Decoder

MODE_AUTO = 0
MODE_MEMORY = 8


# =======================================================================================
# CCtiReader
# =======================================================================================
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

        build_epoch = metadata.get('build_epoch') if isinstance(metadata.get('build_epoch'), int) else 0
        build_epoch_limit = metadata.get('build_epoch_limit') if isinstance(metadata.get('build_epoch_limit'), int) else 0
        if 0 != build_epoch_limit:
            if 0 == build_epoch + build_epoch_limit or time.time() > build_epoch + build_epoch_limit:
                raise InvalidDatabaseError(
                    f"Error reading metadata in database file ({filename})."
                )

            tmp_buffer_md5 = hashlib.md5(self._buffer[:metadata_start]).hexdigest()
            if metadata.get('license')[:32] != tmp_buffer_md5.encode('utf8'):
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


# =======================================================================================
# Metadata
# =======================================================================================
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
        self.build_epoch_limit = kwargs["build_epoch_limit"] if 'build_epoch_limit' in kwargs else None
        self.description = kwargs["description"]
        self.alias = kwargs["alias"] if 'alias' in kwargs else None
        self.license = kwargs["license"] if 'license' in kwargs else None

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