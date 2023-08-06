"""
Collection of classes and functions geared towards facilitating computations involving both numeric and symbolic values.

This module offers various functions for performing a series of checks and operations on numerical and unit-based data.
For instance, the module contains functions to verify if a value or unit is dimensionless, to determine if a numeric
value has an offset, or to check if two values or units are compatible.
A set of utility functions provides detailed inspection capabilities on numerical data, allowing to ascertain whether a
value is zero, non-zero, or not a number (NaN), among others.
Moreover, the module includes functions to confirm the data structure type of the provided data, identifying whether
it's a scalar, an array, or a vector.
"""

from enum import Enum
from numbers import Number
from typing import Literal, Optional, Union, get_args

import casadi
import numpy as np

from optool.uom import UNITS, Quantity, Unit

NUMERIC_TYPES = Union[Number, np.ndarray, Quantity]  # type:ignore
"""Numbers with or without units of measurement"""

SYMBOLIC_TYPES = Union[casadi.SX]
"""Symbols used by the supported modeling languages"""


class VectorRepresentation(Enum):
    """Description of vector layouts."""
    COLUMN = 0
    """Convenient shortcut to describe column vectors, where the entries are stacked vertically"""
    ROW = 1
    """Convenient shortcut to describe row vectors, where the entries are stacked horizontally"""


def has_offset(value_or_unit: Union[NUMERIC_TYPES, Unit]) -> bool:
    """
    Checks whether a given numeric value or unit has an offset in its measurement, such as Celsius.

    :param value_or_unit: Numeric value or unit to check.
    :return: {py:data}`True` if the given value or unit has an offset in its measurement, {py:data}`False` otherwise.
    """
    if isinstance(value_or_unit, Unit):
        return has_offset(Quantity(1.0, value_or_unit))
    # noinspection PyProtectedMember
    return isinstance(value_or_unit, Quantity) and not value_or_unit._is_multiplicative


def _get_unit(quantity_or_unit: Union[Quantity, Unit, str]) -> Unit:
    if isinstance(quantity_or_unit, Unit):
        return quantity_or_unit
    if isinstance(quantity_or_unit, str):
        return UNITS.parse_units(quantity_or_unit)
    if isinstance(quantity_or_unit, Quantity):
        return quantity_or_unit.units
    raise ValueError(
        f"The input argument must either be a quantity or a unit, but is {quantity_or_unit.__class__.__name__}")


def is_dimensionless(value_or_unit: Union[NUMERIC_TYPES, Unit, str]) -> bool:
    """
    Checks if a given value or unit is dimensionless.

    :param value_or_unit: The value or unit to check.
    :return: {py:data}`True` if the given value or unit is dimensionless, {py:data}`False` otherwise.
    """
    if isinstance(value_or_unit, (Quantity, Unit, str)):
        return _get_unit(value_or_unit).dimensionless
    return True


def is_compatible(value_or_unit: Union[NUMERIC_TYPES, Unit, str], unit: Optional[Union[Unit, str]]) -> bool:
    """
    Checks if a given value or unit is compatible with a specific unit.

    :param value_or_unit: The value or unit to check.
    :param unit: The specific unit to check compatibility against.
    :return: {py:data}`True` if the given value or unit is compatible with the specific unit, {py:data}`False`
        otherwise.
    """
    if unit is None:
        return is_dimensionless(value_or_unit)
    if isinstance(unit, str):
        unit = UNITS.parse_units(unit)
    both_are_dimensionless = is_dimensionless(value_or_unit) and is_dimensionless(unit)
    units_are_compatible = isinstance(value_or_unit,
                                      (Quantity, Unit, str)) and _get_unit(value_or_unit).is_compatible_with(unit)
    return both_are_dimensionless or units_are_compatible


def is_non_nan(value: NUMERIC_TYPES):
    """
    Checks if a given numeric value is not NaN.

    :param value: The numeric value to check.
    :return: {py:data}`True` if the given numeric value is not NaN, {py:data}`False` otherwise.
    """
    return ~np.isnan(value)  # type: ignore


def is_zero(value: NUMERIC_TYPES):
    """
    Checks if a given numeric value is zero.

    :param value: The numeric value to check.
    :return: {py:data}`True` if the given numeric value is zero, {py:data}`False` otherwise.
    """
    return value == 0


def is_nonzero(value: NUMERIC_TYPES):
    """
    Checks if a given numeric value is not zero.

    :param value: The numeric value to check.
    :return: {py:data}`True` if the given numeric value is not zero, {py:data}`False` otherwise.
    """
    return value != 0


def is_numeric(value) -> bool:
    """
    Checks if a given value is numeric.

    :param value: The value to check.
    :return: {py:data}`True` if the given value is numeric, {py:data}`False` otherwise.
    """
    return isinstance(value, get_args(NUMERIC_TYPES))


def is_symbolic(value) -> bool:
    """
    Checks if a given value is symbolic.

    :param value: The value to check.
    :return: {py:data}`True` if the given value is symbolic, {py:data}`False` otherwise.
    """
    return isinstance(value, SYMBOLIC_TYPES) or (  # type: ignore
        isinstance(value, Quantity) and is_symbolic(value.magnitude))  # type: ignore


def is_scalar(value: Union[NUMERIC_TYPES, SYMBOLIC_TYPES]) -> bool:
    """
    Checks if a given value is scalar.

    :param value: The value to check.
    :return: {py:data}`True` if the given value is scalar, {py:data}`False` otherwise.
    """
    return num_elements(value) == 1


def is_array(value: NUMERIC_TYPES) -> bool:
    """
    Checks if a given numeric value is an array.

    :param value: The numeric value to check.
    :return: {py:data}`True` if the given numeric value is an array, {py:data}`False` otherwise.
    """
    if isinstance(value, Number):
        return True
    if isinstance(value, np.ndarray):
        return np.ndim(value) == 1
    if isinstance(value, Quantity):
        return is_array(value.magnitude)
    raise TypeError(f"Unsupported type {type(value)}")


def is_vector(value: Union[NUMERIC_TYPES, SYMBOLIC_TYPES],
              representation: Optional[VectorRepresentation] = None) -> bool:
    """Checks if a given value is a (column or row) vector.

    :param value: The value to check
    :param representation: The representation of the vector
    :returns: {py:data}`True` if the value has two dimensions and is either a row or a column vector, depending on the
        requested axis, or {py:data}`False` otherwise.

    :::{seealso}
    {py:func}`is_column`, {py:func}`is_row`, {py:class}`VectorRepresentation`
    :::
    """
    if not representation:
        return is_column(value) or is_row(value)
    return is_column(value) if representation is VectorRepresentation.COLUMN else is_row(value)


def is_column(value: Union[NUMERIC_TYPES, SYMBOLIC_TYPES]) -> bool:
    """
    Checks if a given numeric or symbolic value is a column (i.e., has a vertical vector representation).

    :param value: The numeric or symbolic value to check.
    :return: {py:data}`True` if the given value is a column, {py:data}`False` otherwise.
    """
    if isinstance(value, Number):
        return True
    if isinstance(value, np.ndarray):
        return is_scalar(value) or (value.ndim > 1 and value.shape[1] == 1)
    if isinstance(value, casadi.SX):
        return value.is_column()
    if isinstance(value, Quantity):
        return is_column(value.magnitude)
    raise TypeError(f"Unsupported type {type(value)}")


def is_row(value: Union[NUMERIC_TYPES, SYMBOLIC_TYPES]) -> bool:
    """
    Checks if a given numeric or symbolic value is a row (i.e., has a horizontal vector representation).

    :param value: The numeric or symbolic value to check.
    :return: {py:data}`True` if the given value is a row, {py:data}`False` otherwise.
    """
    if isinstance(value, Number):
        return True
    if isinstance(value, np.ndarray):
        return is_scalar(value) or (value.ndim > 1 and value.shape[0] == 1)
    if isinstance(value, casadi.SX):
        return value.is_row()
    if isinstance(value, Quantity):
        return is_row(value.magnitude)
    raise TypeError(f"Unsupported type {type(value)}")


def num_elements(value: Union[NUMERIC_TYPES, SYMBOLIC_TYPES]) -> int:
    """
    Determines the number of elements in a given numeric or symbolic value.

    :param value: The numeric or symbolic value to count elements in.
    :return: The number of elements in the given value.
    """
    if isinstance(value, Quantity):
        return num_elements(value.magnitude)
    if is_numeric(value):
        return np.size(value)  # type: ignore
    if isinstance(value, casadi.SX):
        return value.numel()
    raise TypeError(f"Unsupported type {type(value)}")


def is_monotonic(value: NUMERIC_TYPES,
                 direction: Literal['ascending', 'descending'] = 'ascending',
                 strict: bool = False) -> bool:
    """
    Checks if a given numeric value is monotonic in a specific direction.

    :param value: The numeric value to check.
    :param direction: The direction in which to check monotonicity.
    :param strict: A boolean indicating whether to enforce strict monotonicity.
                   If {py:data}`True`, the function checks for strictly increasing or decreasing values.
                   Otherwise, the function allows for equal successive values.
    :return: {py:data}`True` if the given value is monotonic in the specified direction, {py:data}`False` otherwise.
    """
    if num_elements(value) < 2:
        raise ValueError(f"Requires at least 2 elements, but got only {num_elements(value)}.")
    if not all(is_non_nan(value)):
        raise ValueError(f"The array contains {np.sum(~is_non_nan(value))} NaN value(s).")

    difference = np.diff(value)  # type: ignore
    if direction == 'ascending':
        if strict:
            return bool(np.all(difference > 0))
        return bool(np.all(difference >= 0))
    if direction == 'descending':
        if strict:
            return bool(np.all(difference < 0))
        return bool(np.all(difference <= 0))
    raise ValueError(f"Direction must be ascending or descending, but is {direction!r}.")
