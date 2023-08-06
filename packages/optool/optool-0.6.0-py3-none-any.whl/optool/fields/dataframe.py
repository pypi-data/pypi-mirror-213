"""
Pydantic-compatible field types for [Pandas](https://pypi.org/project/pandas/) DataFrame objects.

This module contains classes that provide Pydantic-compatible field types specifically tailored for Pandas DataFrame
objects.
These custom fields allow developers to enforce specific index types.
"""

from typing import TYPE_CHECKING, Any, Optional, Type

import pandas as pd
from pandas import DatetimeIndex, Index, TimedeltaIndex
from pydantic.fields import ModelField

from optool.fields.util import get_type_validator, update_object_schema


class ConstrainedDataFrame:
    """
    Pydantic-compatible field type for {py:class}`pandas.DataFrame` objects, which allows to specify the index type.

    :::{seealso}
    [Pydantic documentation: Custom Data Types](https://docs.pydantic.dev/usage/types/#custom-data-types) and
    {py:class}`pydantic.types.ConstrainedInt` or similar of {py:mod}`pydantic`
    :::
    """

    strict: bool = True
    index_type: Type[Index] = pd.RangeIndex

    @classmethod
    def __get_validators__(cls):
        yield get_type_validator(pd.DataFrame) if cls.strict else cls.validate_dataframe
        yield cls.validate_index_type

    @classmethod
    def __modify_schema__(cls, field_schema, field: Optional[ModelField]):
        update_object_schema(field_schema, index_type=cls.index_type.__name__)

    @classmethod
    def validate_dataframe(cls, val: Any, field: ModelField) -> pd.DataFrame:
        if isinstance(val, pd.DataFrame):
            return val
        if field.sub_fields:
            raise TypeError(f"A constrained DataFrame cannot by typed, but have sub-fields {field.sub_fields}")

        return pd.DataFrame(val)

    @classmethod
    def validate_index_type(cls, val: pd.DataFrame, field: ModelField) -> pd.DataFrame:
        if cls.index_type is None or isinstance(val.index, cls.index_type):
            return val
        raise IndexTypeError(expected=cls.index_type, value=val)


class DataFrameLike(ConstrainedDataFrame):
    """
    Pydantic-compatible field type for {py:class}`~pandas.DataFrame` objects.

    Assigned values not already of type {py:class}`~pandas.DataFrame` are parsed using the regular constructor
    {py:class}`DataFrame(val) <pandas.DataFrame>`.
    """
    strict = False


class DatetimeDataFrame(ConstrainedDataFrame):
    """
    Pydantic-compatible field type for {py:class}`~pandas.DataFrame` objects, the index of which must be of type
    {py:class}`~pandas.DatetimeIndex`.

    Assigned values not already of type {py:class}`~pandas.DataFrame` are parsed using the regular constructor
    {py:class}`DataFrame(val) <pandas.DataFrame>`.
    """
    strict = False
    index_type = DatetimeIndex


class TimedeltaDataFrame(ConstrainedDataFrame):
    """
    Pydantic-compatible field type for {py:class}`~pandas.DataFrame` objects, the index of which must be of type
    {py:class}`~pandas.TimedeltaIndex`.

    Assigned values not already of type {py:class}`~pandas.DataFrame` are parsed using the regular constructor
    {py:class}`DataFrame(val) <pandas.DataFrame>`.
    """
    strict = False
    index_type = TimedeltaIndex


if TYPE_CHECKING:
    from typing_extensions import TypeAlias

    DataFrameLike: TypeAlias = pd.DataFrame  # type: ignore[no-redef] # noqa: F811
    DatetimeDataFrame: TypeAlias = pd.DataFrame  # type: ignore[no-redef] # noqa: F811
    TimedeltaDataFrame: TypeAlias = pd.DataFrame  # type: ignore[no-redef] # noqa: F811


class IndexTypeError(ValueError):
    """
    Raised when the type of index of a {py:class}`pandas.DataFrame` does not meet the expectations.

    :param expected: The expected type of the index.
    :param value: The DataFrame that causes the error due to its index type.
    """

    def __init__(self, *, expected: Type[Index], value: pd.DataFrame) -> None:
        super().__init__(f"expected index type {expected}, but got a DataFrame with index type {type(value.index)}")
