# pylint:disable=C0111
import os
from typing import IO, AnyStr, Union, cast

from .reader import CCtiReader, MODE_AUTO, MODE_MEMORY

try:
    # pylint: disable=import-self
    from . import extension as _extension
except ImportError:
    _extension = None  # type: ignore[assignment]


__all__ = [
    "CCtiReader",
	"MODE_AUTO",
	"MODE_MEMORY"
]

__version__ = "0.0.2"
__author__ = "AISpera"
__license__ = "Apache License, Version 2.0"