"""
Miscellaneous Pydantic-compatible field types for custom validations.

This module contains a collection of Pydantic-compatible field types, designed for enforcing specific validation rules
on strings and numbers, including non-empty strings, number bounds within the [0, 1] interval, finiteness checks, etc.
"""

from typing import TYPE_CHECKING

from pydantic import ConstrainedFloat, ConstrainedStr


class NonEmptyStr(ConstrainedStr):
    """Pydantic-compatible field type for non-empty strings, with leading and trailing spaces removed."""
    strict = True
    strip_whitespace = True
    min_length = 1


class FractionFloat(ConstrainedFloat):
    """
    Pydantic-compatible field type for numbers, enforcing them to be greater than or equal to zero and smaller than
    or equal to one.
    """
    strict = False
    ge = 0.0
    le = 1.0
    allow_inf_nan = False


class PositiveFiniteFloat(ConstrainedFloat):
    """
    Pydantic-compatible field type for numbers, enforcing them to be finite (i.e., not NaN or infinite) and greater
    than zero.
    """
    strict = False
    gt = 0
    allow_inf_nan = False


class NonNegativeFiniteFloat(ConstrainedFloat):
    """
    Pydantic-compatible field type for numbers, enforcing them to be finite (i.e., not NaN or infinite) and greater
    than or equal to zero.
    """
    strict = False
    ge = 0
    allow_inf_nan = False


class NegativeFiniteFloat(ConstrainedFloat):
    """
    Pydantic-compatible field type for numbers, enforcing them to be finite (i.e., not NaN or infinite) and smaller
    than zero.
    """
    strict = False
    lt = 0
    allow_inf_nan = False


class NonPositiveFiniteFloat(ConstrainedFloat):
    """
    Pydantic-compatible field type for numbers, enforcing them to be finite (i.e., not NaN or infinite) and smaller
    than or equal to zero.
    """
    strict = False
    le = 0
    allow_inf_nan = False


if TYPE_CHECKING:
    from typing_extensions import TypeAlias

    NonEmptyStr: TypeAlias = str  # type: ignore[no-redef] # noqa: F811
    FractionFloat: TypeAlias = float  # type: ignore[no-redef] # noqa: F811
    PositiveFiniteFloat: TypeAlias = float  # type: ignore[no-redef] # noqa: F811
    NonNegativeFiniteFloat: TypeAlias = float  # type: ignore[no-redef] # noqa: F811
    NegativeFiniteFloat: TypeAlias = float  # type: ignore[no-redef] # noqa: F811
    NonPositiveFiniteFloat: TypeAlias = float  # type: ignore[no-redef] # noqa: F811
