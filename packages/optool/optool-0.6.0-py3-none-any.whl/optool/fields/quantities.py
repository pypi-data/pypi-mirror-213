"""
Pydantic-compatible field types for unit and quantity objects of [Pint](https://pypi.org/project/Pint/).

This module introduces Pydantic-compatible field types designed to handle and validate objects related to units of
measurements.
Through the use of these custom fields, it is possible to impose desired dimensionality requirements on units and
quantities within Pydantic models, which strengthens the data integrity throughout the codebase.
"""

from __future__ import annotations

from numbers import Number
from typing import TYPE_CHECKING, Any, ClassVar, Generic, Optional, TypeVar

import pydantic
from pydantic import ValidationError
from pydantic.fields import ModelField

from optool.fields.util import (WrongTypeError, check_validation_is_passed_on_to_sub_types, get_dimension,
                                get_subfield_schema, get_subtype_validator, get_type_validator, update_object_schema)
from optool.uom import UNITS, PhysicalDimension, Quantity, Unit

D = TypeVar("D", bound=PhysicalDimension)
"""Type variable with an upper bound of {py:class}`~optool.uom.PhysicalDimension`."""


# Due to the generic class, Pydantic has to be tricked out such that the automatic creation of schemas is working.
class ConstrainedUnit(pydantic.BaseModel, Generic[D]):
    """
    Pydantic-compatible field type for {py:class}`~optool.uom.Unit` objects, which allows to specify the desired
    dimensionality.

    :::{seealso}
    [Pydantic documentation: Custom Data Types](https://docs.pydantic.dev/usage/types/#custom-data-types) and
    {py:class}`pydantic.types.ConstrainedInt` or similar of {py:mod}`pydantic`
    :::
    """
    strict: ClassVar[bool] = True

    @classmethod
    def __get_validators__(cls):
        yield get_type_validator(Unit) if cls.strict else cls.validate_unit
        yield cls.validate_dimensionality

    @classmethod
    def __modify_schema__(cls, field_schema, field: Optional[ModelField]):
        dimension = get_dimension(field, 0)
        update_object_schema(field_schema, dimensionality=dimension.dimensionality if dimension else None)

    @classmethod
    def validate_unit(cls, value: Any, field: ModelField) -> Unit:
        if isinstance(value, Unit):
            return value

        if isinstance(value, str):
            try:
                return UNITS.parse_units(value)
            except Exception as e:
                raise UnitParseError(unit=value) from e

        raise WrongTypeError(expected=(Unit, str), value=value)

    @classmethod
    def validate_dimensionality(cls, val: Unit, field: ModelField) -> Unit:
        dimension = get_dimension(field, 0)
        if dimension is None or val.dimensionality == UNITS.get_dimensionality(dimension.dimensionality):
            return val
        raise DimensionalityError(expected=dimension.dimensionality, value=val)


T = TypeVar("T")  # Allow storing everything as magnitude in Quantity
"""
Type variable to specify the type of the magnitude of a {py:attr}`~optool.uom.Quantity`.
"""


# Due to the generic class, Pydantic has to be tricked out such that the automatic creation of schemas is working.
class ConstrainedQuantity(pydantic.BaseModel, Generic[D, T]):
    """
    Pydantic-compatible field type for {py:class}`~optool.uom.Quantity` objects, which allows to specify the desired
    dimensionality.

    :::{seealso}
    Class {py:class}`pydantic.types.ConstrainedInt` or similar of {py:mod}`pydantic`.
    :::
    """

    strict: ClassVar[bool] = True
    strict_magnitude: ClassVar[bool] = True

    @classmethod
    def __get_validators__(cls):
        if cls.strict:
            yield get_type_validator(Quantity)
        if cls.strict_magnitude:
            yield get_subtype_validator(Quantity, lambda x: type(x.m))

        if not cls.strict:
            yield cls.validate_quantity
        yield cls.validate_dimensionality
        yield cls.validate_magnitude

    @classmethod
    def __modify_schema__(cls, field_schema, field: Optional[ModelField]):
        dimension = get_dimension(field, 0)
        update_object_schema(field_schema,
                             dimensionality=dimension.dimensionality if dimension else None,
                             datatype=get_subfield_schema(field, 1))

    @classmethod
    def validate_quantity(cls, val: Any, field: ModelField) -> Quantity:
        try:
            return Quantity(val)
        except Exception as e:
            raise WrongTypeError(expected=(Quantity, str, Number), value=val) from e

    @classmethod
    def validate_dimensionality(cls, val: Quantity, field: ModelField) -> Quantity:
        dimension = get_dimension(field, 0)
        if dimension is None or val.dimensionality == UNITS.get_dimensionality(dimension.dimensionality):
            return val
        raise DimensionalityError(expected=dimension.dimensionality, value=val)

    @classmethod
    def validate_magnitude(cls, val: Quantity, field: ModelField) -> Quantity:
        if not field.sub_fields:
            return val

        magnitude_field = field.sub_fields[1]
        check_validation_is_passed_on_to_sub_types(field.name, magnitude_field)
        valid_value, error = magnitude_field.validate(val.m, {}, loc='magnitude')
        if error:
            raise ValidationError([error], cls)

        return Quantity(valid_value, val.u)


class UnitLike(ConstrainedUnit[D], Unit):
    """
    Pydantic-compatible field type for {py:class}`~optool.uom.Unit` objects.

    Assigned values not already of type {py:class}`~optool.uom.Unit` are parsed using `UNITS.parse_units(...)`. The
    subtype specified using type hinting (e.g., `UnitLike[Length]`) is used to check if the unit has the correct
    dimensionality.

    ::::{admonition} Example
    :class: example dropdown

    ```python
    from optool import BaseModel
    from optool.fields.quantities import UnitLike
    from optool.uom import Mass

    class ExampleModel(BaseModel):
        mass_unit: UnitLike[Mass]

    mdl = BaseModel(mass_unit="kg")
    ```
    """
    strict = False


class StrictUnit(ConstrainedUnit[D], Unit):
    """
    Pydantic-compatible field type for {py:class}`~optool.uom.Unit` objects.

    Assigned values must be of type {py:class}`~optool.uom.Unit`. The subtype specified using type hinting (e.g.,
    `UnitLike[Length]`) is used to check if the unit has the correct dimensionality.
    """
    strict = True


class QuantityLike(ConstrainedQuantity[D, T], Quantity):
    """
    Pydantic-compatible field type for {py:class}`~optool.uom.Quantity` objects.

    Assigned values not already of type {py:class}`~optool.uom.Quantity` are parsed using the regular constructor
    {py:class}`Quantity(val) <optool.uom.Quantity>`.

    The two subtypes specified using type hinting (e.g., `QuantityLike[Length, PositiveInt]`) are used to check if the
    unit has the expected dimensionality and the magnitude matches the expected specification. For the latter, the
    validation and parsing is forwarded to the specific type, e.g., in the example above, the value is validated using
    the implementation provided by {py:class}`pydantic.PositiveInt`.

    ::::{admonition} Example
    :class: example dropdown

    ```python
    from optool import BaseModel
    from optool.fields.quantities import QuantityLike
    from optool.fields.misc import PositiveFiniteFloat
    from optool.uom import Mass

    class ExampleModel(BaseModel):
        mass: QuantityLike[Mass, PositiveFiniteFloat]

    mdl = BaseModel(mass="5 kg")
    ```
    """
    strict = False
    strict_magnitude = False


class StrictQuantity(ConstrainedQuantity[D, T], Quantity):
    """
    Pydantic-compatible field type for {py:class}`~optool.uom.Quantity` objects.

    Assigned values must be of type {py:class}`~optool.uom.Quantity`.

    The two subtypes specified using type hinting (e.g., `QuantityLike[Length, PositiveInt]`) are used to check if the
    unit has the expected dimensionality and the magnitude matches the expected specification. For the latter, the
    validation and parsing is forwarded to the specific type, e.g., in the example above, the value is validated using
    the implementation provided by {py:class}`pydantic.PositiveInt`.
    """
    strict = True
    strict_magnitude = False


if TYPE_CHECKING:
    from typing_extensions import TypeAlias

    UnitLike: TypeAlias = Unit  # type: ignore[no-redef] # noqa: F811
    StrictUnit: TypeAlias = Unit  # type: ignore[no-redef] # noqa: F811
    QuantityLike: TypeAlias = Quantity  # type: ignore[no-redef] # noqa: F811
    StrictQuantity: TypeAlias = Quantity  # type: ignore[no-redef] # noqa: F811


class DimensionalityError(ValueError):
    """
    Raised when an incorrect dimensionality is encountered.

    :param expected: The expected dimensionality
    :param value: The value that causes the error due to its incorrect dimensionality.
    """

    def __init__(self, *, expected: Optional[str], value: Quantity) -> None:
        super().__init__(f"expected the dimensionality {expected}, "
                         f"but got a value with dimensionality {value.dimensionality}")


class UnsupportedMagnitudeConversion(ValueError):
    """
    Raised when a value cannot be automatically converted to the expected magnitude.

    :param value: The value that causes the error due to unsupported automatic conversion.
    """

    def __init__(self, *, value: Any) -> None:
        super().__init__(f"the value of {type(value)} cannot be converted automatically")


class UnitParseError(ValueError):
    """
    Raised when a unit string cannot be parsed.

    :param unit: The unit string that causes the error due to parsing issues.
    """

    def __init__(self, *, unit: str) -> None:
        super().__init__(f"cannot parse the unit {unit}")
