"""
Pydantic-compatible field types for objects that are used to create symbolic expressions.

This module focuses on providing data validation for symbolic expressions implemented via the
[CasADi](https://web.casadi.org) library.
CasADi is a symbolic framework for automatic differentiation and optimal control, which is used extensively for
nonlinear optimization and algorithmic differentiation.
With the Pydantic-compatible fields of this module, it can be ensured that any CasADi symbolic expressions used in a
Pydantic model adheres to specific dimensional requirements, thereby reducing the risk of shape-related errors in the
symbolic computations.
"""

from __future__ import annotations

import itertools
from typing import TYPE_CHECKING, Optional, Tuple

import casadi
from pydantic.fields import ModelField

from optool.fields.util import get_type_validator, update_object_schema


class ConstrainedCasadiSymbol:
    """
    Pydantic-compatible field type for {py:class}`casadi.SX` objects.

    :::{seealso}
    [Pydantic documentation: Custom Data Types](https://docs.pydantic.dev/usage/types/#custom-data-types) and
    {py:class}`pydantic.types.ConstrainedInt` or similar of {py:mod}`pydantic`.
    :::
    """

    shape: Optional[Tuple[Optional[int], ...]] = None

    @classmethod
    def __get_validators__(cls):
        yield get_type_validator(casadi.SX)
        yield cls.validate_shape

    @classmethod
    def __modify_schema__(cls, field_schema, field: Optional[ModelField]):
        update_object_schema(field_schema, shape=cls.shape)

    @classmethod
    def validate_shape(cls, val: casadi.SX, field: ModelField) -> casadi.SX:
        if cls.shape is None or all(cls._compare_dim(*dims) for dims in itertools.zip_longest(cls.shape, val.size())):
            return val
        raise ShapeError(expected=cls.shape, value=val)

    @classmethod
    def _compare_dim(cls, expected: Optional[int], actual: Optional[int]) -> bool:
        return actual == expected or expected is None


class CasadiScalar(ConstrainedCasadiSymbol):
    """Pydantic-compatible field type for two-dimensional {py:class}`casadi.SX` objects representing scalars."""
    shape = (1, 1)


class CasadiRow(ConstrainedCasadiSymbol):
    """Pydantic-compatible field type for two-dimensional {py:class}`casadi.SX` objects representing row vectors."""
    shape = (1, None)


class CasadiColumn(ConstrainedCasadiSymbol):
    """Pydantic-compatible field type for two-dimensional {py:class}`casadi.SX` objects representing column vectors."""
    shape = (None, 1)


class CasadiMatrix(ConstrainedCasadiSymbol):
    """Pydantic-compatible field type for two-dimensional {py:class}`casadi.SX` objects representing matrices."""
    shape = (None, None)


if TYPE_CHECKING:
    from typing_extensions import TypeAlias

    CasadiScalar: TypeAlias = casadi.SX  # type: ignore[no-redef] # noqa: F811
    CasadiRow: TypeAlias = casadi.SX  # type: ignore[no-redef] # noqa: F811
    CasadiColumn: TypeAlias = casadi.SX  # type: ignore[no-redef] # noqa: F811
    CasadiMatrix: TypeAlias = casadi.SX  # type: ignore[no-redef] # noqa: F811


class ShapeError(ValueError):
    """
    Raised when the shape of a CasADi SX variable does not meet the expectations.

    :param expected: The expected shape of the array, {py:data}`None` indicating arbitrary length of the corresponding
        dimension.
    :param value: The CasADi SX variable that causes the error due to its shape.
    """

    def __init__(self, *, expected: Tuple[Optional[int], ...], value: casadi.SX) -> None:
        super().__init__(f"expected the shape {expected}, "
                         f"but got a value with shape ('called size' in CasADi) {value.size()}")
