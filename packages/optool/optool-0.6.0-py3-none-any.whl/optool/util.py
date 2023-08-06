"""
General utility classes used within this package.

This module contains utility classes designed to augment and simplify coding tasks.
"""

from __future__ import annotations

from enum import Enum

import numpy as np

from optool.core import BaseModel
from optool.fields.misc import NonEmptyStr


class StrEnum(str, Enum):
    """
    Python {py:class}`~enum.Enum` that inherits from {py:class}`str` to complement {py:class}`~enum.IntEnum` in the
    standard library.

    It can be used to create string enums, where the enum members are instances of {py:class}`str`.

    The implementation ensures that a lower case string of the {py:class}`enum.Enum` member is produced as its value.
    """

    def _generate_next_value_(self, *_):
        return self.lower()


class ValueRange(BaseModel, frozen=True):
    """Ranges of the normed values of the optimization variables."""

    name: NonEmptyStr
    """The name of the decision variable."""

    min: float
    """The smallest value."""
    avg: float
    """The average (arithmetic mean) value."""
    max: float
    """The greatest value."""
    max_abs: float
    """The greatest absolute value."""

    @classmethod
    def of(cls, name: str, val: np.ndarray) -> ValueRange:
        """
        Creates a value range by analyzing the numeric array specified.

        :param name: The name of the decision variable.
        :param val: The normed values as array.
        :returns: The value range of the array specified.
        """
        return cls(name=name, min=np.min(val), avg=float(np.mean(val)), max=np.max(val), max_abs=np.max(np.abs(val)))
