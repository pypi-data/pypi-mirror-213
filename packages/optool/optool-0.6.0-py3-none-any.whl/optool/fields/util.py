"""
Utility functions facilitating the implementation of the Pydantic-compatible fields in the other modules of this
package.

This module contains various utility functions designed to augment and simplify coding tasks related to the
Pydantic-compatible fields implemented in the other modules of this package.
"""

from __future__ import annotations

import re
from typing import Any, Callable, Dict, Iterable, Optional, Tuple, Type, TypeVar, Union

import numpy as np
import pydantic
from pydantic.fields import ModelField
from pydantic.validators import find_validators

from optool.core import BaseModel
from optool.uom import PhysicalDimension

TypeDefinition = Union[Type, Tuple[Type, ...]]
"""Type alias used to annotate function parameters and return types."""

ValidationFunc = Callable[[Any], Any]
"""Type alias used to annotate callable function accepting a single parameter and returning a value of any type."""

T = TypeVar("T")
"""Type variable that can represent any type, used for creating generic function parameters and return types."""


class WrongTypeError(ValueError):
    """
    Raised when the type of the value specified does not meet the expectations.

    :param expected: The expected type.
    :param value: The value that causes the error due to its type
    """

    def __init__(self, *, expected: TypeDefinition, value: Any) -> None:
        super().__init__(f"expected {expected}, but got {value}")


class WrongSubTypeError(ValueError):
    """
    Raised when the subtype of a value does not meet the expectations.

    :param expected_type: The expected main type.
    :param expected_subtype: The expected subtype.
    :param actual_subtype: The actual subtype of the value.
    :param value: The value that causes the error due to its subtype.
    """

    def __init__(self, *, expected_type: TypeDefinition, expected_subtype: TypeDefinition,
                 actual_subtype: TypeDefinition, value: Any) -> None:
        super().__init__(f"expected subtype {expected_subtype} of {expected_type}, "
                         f"but got subtype {actual_subtype} of {type(value)}")


class ArbitrarySubTypeError(ValueError):
    """
    Raised when the subtype of a {py:class}`ModelField` is not handled by any specific validators.

    :param name: The name of the field.
    :param field: The model field with the problematic subtype.
    """

    def __init__(self, *, name: str, field: ModelField) -> None:
        sub_type = None if field.sub_fields is None else field.sub_fields[0].type_
        super().__init__(f"the sub-field of {name!r} has the type {field.type_} (with subtype {sub_type}), "
                         f"but {field.type_} does not offer any specific validators that would be able to handle "
                         f"subtypes")


class _ConfigWithArbitraryTypesNotAllowed(BaseModel.Config):
    arbitrary_types_allowed = False


def has_specific_type_validator(type_: Type[Any]) -> bool:
    """
    Determines if the type specified has one or more validators specific validators.

    A specific validator is a validator that is not just the `arbitrary_type_validator` used when
    {py:attr}`pydantic.Config.arbitrary_types_allowed` is set to {py:data}`True`.

    :param type_: The type to analyze.
    :returns: {py:data}`True` if the type specified has a validator that is different from the
        `arbitrary_type_validator`, {py:data}`False` otherwise.
    """

    try:
        next(find_validators(type_, _ConfigWithArbitraryTypesNotAllowed))
        return True
    except Exception as e:
        if re.match("no validator found for <.*?>, see `arbitrary_types_allowed` in Config", str(e)):
            return False
        raise e


def check_validation_is_passed_on_to_sub_types(name: str, field: ModelField) -> None:
    """
    Checks if the validation is passed on to subtypes of the provided field.

    :param name: The name of the field.
    :param field: The model field to check.
    :raises optool.fields.util.ArbitrarySubTypeError: If validation is not passed on to subtypes
    """
    if field.sub_fields is None:
        return
    if not has_specific_type_validator(field.type_):
        raise ArbitrarySubTypeError(name=name, field=field)
    for sub_field in field.sub_fields:
        check_validation_is_passed_on_to_sub_types(field.name, sub_field)


def check_sub_fields_level(field: ModelField) -> None:
    """
    Checks if a {py:class}`pydantic.ModelField` has generic types more than one level deep.

    :param field: The model field to check.
    :raises ValueError: If generic types more than one level deep are found.
    """
    if field.sub_fields is None:
        return
    if field.sub_fields[0].sub_fields:
        raise ValueError(f"Generic types more than one level deep are currently not supported. "
                         f"Got {field.sub_fields[0].type_} and {field.sub_fields[0].sub_fields[0].type_}.")


def get_type_validator(expected_type: Type[T]) -> Callable[[Any], T]:
    """
    Creates a validation function that checks if the input argument is of the expected type.

    :param expected_type: The type the resulting validator will enforce.
    :returns: A new function that can be used to validate if an input value is an instance of the type specified.
    """

    def validate_type(value: Any) -> T:
        if isinstance(value, expected_type):
            return value
        raise WrongTypeError(expected=expected_type, value=value)

    return validate_type


def get_subtype_validator(object_type: Type[T], subtype_provider: Callable[[T],
                                                                           Type]) -> Callable[[Any, ModelField], T]:
    """
    Creates a validation function that checks if the subtype of the input argument is of the expected type.

    :param object_type: The type the resulting validator will enforce.
    :param subtype_provider: Callable to get the subtype of the provided value.
    :returns: A new function that can be used to validate if an input value is an instance of the type specified.
    """

    def validate_subtype(value: Any, field: ModelField) -> T:
        if field.sub_fields:
            expected_subtype = field.sub_fields[0].type_
            actual_subtype = subtype_provider(value)
            if expected_subtype != actual_subtype:
                if isinstance(actual_subtype, np.dtype):
                    actual_subtype = actual_subtype.type
                raise WrongSubTypeError(expected_type=object_type,
                                        expected_subtype=expected_subtype,
                                        actual_subtype=actual_subtype,
                                        value=value)
            check_sub_fields_level(field)

        return value

    return validate_subtype


def check_only_one_specified(first: Any, second: Any, message: str) -> None:
    """
    Checks if either the first or the second argument is {py:data}`None`.

    :param first: The first object to check.
    :param second: The second object to check.
    :param message: The error message to raise if both are specified.
    :raises ValueError: If both 'first' and 'second' are specified, i.e. not {py:data}`None`.
    """
    first_present = first if isinstance(first, bool) else first is not None
    second_present = second if isinstance(second, bool) else second is not None
    if first_present and second_present:
        raise ValueError(message)


def get_subfield_schema(field: Optional[ModelField], subfield_index: int) -> Optional[Dict[str, Any]]:
    """
    Creates a schema of the sub-field of the model field specified.

    :param field: The model field.
    :param subfield_index: The index of the sub-field of interest.
    :returns: The schema representing the sub-field of the model field if it is present, {py:data}`None` otherwise.
    """
    if field is None or field.sub_fields is None:
        return None
    subfield_schema = pydantic.schema_of(field.sub_fields[subfield_index].type_)
    subfield_schema.pop('title', None)
    return subfield_schema


def get_dimension(field: Optional[ModelField], subfield_index: int) -> Optional[PhysicalDimension]:
    """
    Gets the physical dimension associated to the model field specified.

    :param field: The model field.
    :param subfield_index: The index of the sub-field of interest.
    :returns: The physical dimension associated to the model field if it is present, {py:data}`None` otherwise.
    """
    if field is None or field.sub_fields is None:
        return None
    dimension = field.sub_fields[subfield_index].type_
    if dimension == Any:
        return None
    if issubclass(dimension, PhysicalDimension):
        return dimension

    raise TypeError(f"Unsupported {dimension}, should be a {PhysicalDimension.__name__!r} or 'typing.Any'.")


def update_object_schema(field_schema: Dict[str, Any], **properties) -> None:
    """Updates the field schema with object properties, ignoring {py:data}`None` values.

    Updates the dictionary with a key `type` set to `object` and a key `property`, the value of which is a dictionary
    containing all properties specified that are not {py:data}`None`.

    :param field_schema: The field schema to update.
    :param properties: The properties
    """
    field_schema |= {"type": "object", "properties": {k: v for (k, v) in properties.items() if v is not None}}


def validate(value: T,
             validators: Union[bool, ValidationFunc, Iterable[ValidationFunc]],
             msg_template: Optional[str] = None) -> T:
    """
    Validates a given value based on the validator function(s) specified.

    :param value: The value to validate.
    :param validators: The validator function(s).
    :param msg_template: The message to show in case the validation fails, may contain ``{value}`` to refer to the
        value.
    :returns: The given value in case the validation is successful.
    """
    msg_template = msg_template or "Validation failed for {value}"
    error = ValueError(msg_template.format(value=value))
    if isinstance(validators, bool):
        if validators:
            return value
        raise error

    for validator in validators if isinstance(validators, Iterable) else [validators]:
        try:
            satisfied = validator(value)
        except Exception as e:
            raise error from e

        if not satisfied:
            raise error

    return value


def validate_each(value: Iterable,
                  validators: Union[bool, ValidationFunc, Iterable[ValidationFunc]],
                  msg_template: Optional[str] = None) -> None:
    """
    Validates each element in an iterable according to the provided validators.

    :param value: The iterable whose elements need to be validated.
    :param validators: A single or a collection of validation functions to apply on each element.
    :param msg_template: An optional error message template used if validation fails.
    """
    for (i, element) in enumerate(value):
        validate(element, validators, f'While validating element {i}: {msg_template}')
