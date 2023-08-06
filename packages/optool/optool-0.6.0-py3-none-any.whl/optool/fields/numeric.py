"""
Pydantic-compatible field types for [Numpy](https://pypi.org/project/numpy/) arrays.

This module provides a suite of Pydantic-compatible field types tailored for validation and control of Numpy array
objects.
Utilizing these custom fields in Pydantic models enables stricter control over Numpy data structure, aiding in enforcing
desired data shapes, dimensions, and immutability constraints.
"""

from __future__ import annotations

import itertools
import numbers
from typing import TYPE_CHECKING, Any, ClassVar, Generic, Iterable, Literal, Optional, Tuple, Type, TypeVar, Union

import numpy as np
import pydantic
from pydantic.fields import ModelField

from optool.fields.util import (WrongTypeError, check_only_one_specified, check_sub_fields_level, get_subtype_validator,
                                get_type_validator, update_object_schema)

T = TypeVar("T", bound=np.generic)
"""Type variable with an upper bound of {py:class}`numpy.generic`."""

TypesParseableToNdArrays = Union[np.ndarray[Any, np.dtype[T]], numbers.Number, Iterable]
"""
Type alias for a union of types that can be parsed into objects of type {py:class}`numpy.ndarray`.

:type: typing.Union[numpy.ndarray[typing.Any, numpy.dtype[numpy.generic]], numbers.Number, typing.Iterable]

The union includes the following types:

- N-dimensional arrays.
- Any type of number, including integers, floating points, complex numbers, etc.
- Any object capable of returning its members one at a time, including lists, tuples, strings, dictionaries, sets, etc.
"""


# Due to the generic class, Pydantic has to be tricked out such that the automatic creation of schemas is working.
class ConstrainedNdArray(pydantic.BaseModel, Generic[T]):
    """Pydantic-compatible field type for {py:class}`numpy.ndarray` objects, which allows to specify the data-type.

    The approach is inspired by https://github.com/cheind/pydantic-numpy.

    :::{seealso}
    [Pydantic documentation: Custom Data Types](https://docs.pydantic.dev/usage/types/#custom-data-types) and
    {py:class}`pydantic.types.ConstrainedInt` or similar of {py:mod}`pydantic`.
    :::
    """

    strict: ClassVar[bool] = True
    strict_datatype: ClassVar[bool] = True
    dimensions: ClassVar[Optional[int]] = None
    shape: ClassVar[Optional[Tuple[Optional[int], ...]]] = None
    writeable: ClassVar[Literal['keep', 'make_true', 'make_false', 'check_true', 'check_false']] = 'keep'

    @classmethod
    def __get_validators__(cls):
        if cls.strict:
            yield get_type_validator(np.ndarray)
        if cls.strict_datatype:
            yield get_subtype_validator(np.ndarray, lambda x: x.dtype)

        if not cls.strict:
            yield cls.validate_ndarray
        yield cls.validate_dimensions
        yield cls.validate_shape
        yield cls.validate_writeable

    @classmethod
    def __modify_schema__(cls, field_schema: dict[str, Any], field: Optional[ModelField]):
        update_object_schema(field_schema,
                             dimensions=cls.dimensions,
                             shape=cls.shape,
                             writeable=cls.writeable,
                             datatype=field.sub_fields[0].type_.__name__ if field and field.sub_fields else None)

    @classmethod
    def validate_ndarray(cls, val: Any, field: ModelField) -> np.ndarray:
        if not isinstance(val, Iterable):
            val = [val]  # otherwise, np.asarray returns something weird

        if field.sub_fields is not None:
            check_sub_fields_level(field)
            expected_subtype = field.sub_fields[0].type_
            array = np.asarray(val, dtype=expected_subtype)
        else:
            try:
                array = np.asarray(val)
            except Exception as e:
                raise WrongTypeError(expected=(np.ndarray, numbers.Number, Iterable), value=val) from e

        if cls.writeable == 'make_true':
            array.setflags(write=True)
        elif cls.writeable == 'make_false':
            array.setflags(write=False)
        return array

    @classmethod
    def validate_dimensions(cls, val: np.ndarray) -> np.ndarray:
        if cls.dimensions is None or cls.dimensions == val.ndim:
            return val
        raise DimensionsError(expected=cls.dimensions, value=val)

    @classmethod
    def validate_shape(cls, val: np.ndarray) -> np.ndarray:
        if cls.shape is None:
            return val
        if all(cls._compare_dim(*dims) for dims in itertools.zip_longest(cls.shape, val.shape)):
            return val
        raise ShapeError(expected=cls.shape, value=val)

    @classmethod
    def validate_writeable(cls, val: np.ndarray) -> np.ndarray:
        if cls.writeable == 'check_true' and val.flags.writeable is False:
            raise ArrayWriteableError(expected=True, value=val)
        if cls.writeable == 'check_false' and val.flags.writeable is True:
            raise ArrayWriteableError(expected=False, value=val)
        return val

    @classmethod
    def _compare_dim(cls, expected: Optional[int], actual: Optional[int]) -> bool:
        return actual == expected or expected is None


def conndarray(
        *,
        strict: bool = False,
        dimensions: Optional[int] = None,
        shape: Optional[Tuple[int, ...]] = None,
        writeable: Literal['keep', 'make_true', 'make_false', 'check_true',
                           'check_false'] = 'keep') -> Type[np.ndarray]:
    """Creates a Pydantic-compatible field type for {py:class}`numpy.ndarray` objects, which allows specifying
    constraints on the accepted values.

    :param strict: If {py:data}`True` only values of type {py:class}`numpy.ndarray` are accepted. (Default:
            {py:data}`False`)
    :param dimensions: The expected dimensions as in {py:attr}`~numpy.ndarray.ndim`.
    :param shape: The shape expected. One shape dimension can be {py:data}`None` indicating that this dimension is
        arbitrary.
    :param writeable: Specification on how to deal with the `writeable` flag of the {py:class}`numpy.ndarray` object.
    :returns: A new Pydantic-compatible field type.

    :::{seealso}
    {py:func}`pydantic.conint` or similar of {py:mod}`pydantic`.
    :::
    """
    check_only_one_specified(dimensions, shape, "Cannot specify both dimensions and shape.")
    namespace = dict(strict=strict, dimensions=dimensions, shape=shape, writeable=writeable)
    return type('ConstrainedNdArrayValue', (ConstrainedNdArray,), namespace)  # type: ignore


class NdArrayLike(ConstrainedNdArray[T]):
    """
    Pydantic-compatible field type for {py:class}`numpy.ndarray` objects.

    Assigned values not already of type {py:class}`~numpy.ndarray` are parsed using {py:func}`numpy.asarray`. The
    subtype specified using type hinting (e.g., ``NdArrayLike[np.int_]``) is also not enforced, but rather used to set
    the data-type of the numeric values. Accepted types to be parsed are {py:data}`TypesParseableToNdArrays`.
    """
    strict = False
    strict_datatype = False


class Array(ConstrainedNdArray[T]):
    """
    Pydantic-compatible field type for one-dimensional {py:class}`numpy.ndarray` objects.

    Assigned values not already of type {py:class}`~numpy.ndarray` are parsed using {py:func}`numpy.asarray`. The
    subtype specified using type hinting (e.g., ``Array[np.int_]``) is also not enforced, but rather used to set the
    data-type of the numeric values. Accepted types to be parsed are {py:data}`TypesParseableToNdArrays`.
    """
    strict = False
    strict_datatype = False
    dimensions = 1


class ImmutableArray(ConstrainedNdArray[T]):
    """
    Pydantic-compatible field type for one-dimensional immutable {py:class}`numpy.ndarray` objects.

    Assigned values not already of type {py:class}`~numpy.ndarray` are parsed using {py:func}`numpy.asarray`. The
    subtype specified using type hinting (e.g., ``ImmutableArray[np.int_]``) is also not enforced, but rather used to
    set the data-type of the numeric values. Accepted types to be parsed are {py:data}`TypesParseableToNdArrays`.

    Immutability is established by setting the flag ``writeable`` to {py:data}`False`.
    """
    strict = False
    strict_datatype = False
    dimensions = 1
    writeable = 'make_false'


class StrictNdArray(ConstrainedNdArray[T]):
    """
    Pydantic-compatible field type for {py:class}`numpy.ndarray` objects.

    Assigned values must be of type {py:class}`~numpy.ndarray`. Furthermore, the subtype specified using type hinting
    (e.g., ``StrictNdArray[np.int_]``) must also match the data-type of the numeric values.
    """
    strict = True
    strict_datatype = True


class Row(ConstrainedNdArray[T]):
    """
    Pydantic-compatible field type for two-dimensional {py:class}`numpy.ndarray` objects representing row vectors.

    Assigned values must be of type {py:class}`~numpy.ndarray`. However, the subtype specified using type hinting (e.g.,
    ``Row[np.int_]``) is also not enforced, but rather used to set the data-type of the numeric values.
    """
    strict = True
    strict_datatype = False
    shape = (1, None)


class Column(ConstrainedNdArray[T]):
    """
    Pydantic-compatible field type for two-dimensional {py:class}`numpy.ndarray` objects representing column vectors.

    Assigned values must be of type {py:class}`~numpy.ndarray`. However, the subtype specified using type hinting (e.g.,
    ``Column[np.int_]``) is also not enforced, but rather used to set the data-type of the numeric values.
    """
    strict = True
    strict_datatype = False
    shape = (None, 1)


class Matrix(ConstrainedNdArray[T]):
    """
    Pydantic-compatible field type for two-dimensional {py:class}`numpy.ndarray` objects representing matrices.

    Assigned values must be of type {py:class}`~numpy.ndarray`. However, the subtype specified using type hinting (e.g.,
    ``Matrix[np.int_]``) is also not enforced, but rather used to set the data-type of the numeric values.
    """
    strict = True
    strict_datatype = False
    dimensions = 2


if TYPE_CHECKING:
    from typing_extensions import TypeAlias

    NdArrayLike: TypeAlias = np.ndarray[Any, np.dtype[T]]  # type: ignore[no-redef] # noqa: F811
    Array: TypeAlias = np.ndarray[Any, np.dtype[T]]  # type: ignore[no-redef] # noqa: F811
    ImmutableArray: TypeAlias = np.ndarray[Any, np.dtype[T]]  # type: ignore[no-redef] # noqa: F811
    StrictNdArray: TypeAlias = np.ndarray[Any, np.dtype[T]]  # type: ignore[no-redef] # noqa: F811
    Row: TypeAlias = np.ndarray[Any, np.dtype[T]]  # type: ignore[no-redef] # noqa: F811
    Column: TypeAlias = np.ndarray[Any, np.dtype[T]]  # type: ignore[no-redef] # noqa: F811
    Matrix: TypeAlias = np.ndarray[Any, np.dtype[T]]  # type: ignore[no-redef] # noqa: F811


class ShapeError(ValueError):
    """
    Raised when the shape of a numpy array does not meet the expectations.

    :param expected: The expected shape of the array, {py:data}`None` indicating arbitrary length of the corresponding
        dimension.
    :param value: The array that causes the error due to its shape.
    """

    def __init__(self, *, expected: Tuple[Optional[int], ...], value: np.ndarray) -> None:
        super().__init__(f"expected the shape {expected}, but got a value with shape {value.shape}")


class DimensionsError(ValueError):
    """
    Raised when the number of dimensions of a {py:class}`numpy.ndarray` does not meet the expectations.

    :param expected: The expected number of dimensions.
    :param value: The array that causes the error due to its number of dimensions.
    """

    def __init__(self, *, expected: int, value: np.ndarray) -> None:
        super().__init__(f"expected {expected} dimension(s), but got a value with {np.ndim(value)} dimension(s)")


class ArrayWriteableError(ValueError):
    """
    Raised when the writeable flag of a {py:class}`numpy.ndarray` does not meet the expectations.

    :param expected: The expected state of the writeable flag.
    :param value: The array that causes the error due to its writeable flag state.
    """

    def __init__(self, *, expected: bool, value: np.ndarray) -> None:
        super().__init__(f"expected writeable is {expected}, "
                         f"but got a value with writeable flag set to {value.flags.writeable}")
