from typing import AnyStr, Union, List, Dict

Primitive = Union[AnyStr, bool, float, int]
Record = Union[Primitive, "RecordList", "RecordDict"]

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