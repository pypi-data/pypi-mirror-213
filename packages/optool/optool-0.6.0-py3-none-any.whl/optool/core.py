"""
Core data model based on a customized base model of [Pydantic](https://docs.pydantic.dev/latest/).

This module contains the base model for all data model classes of this project.
Compared to the original Pydantic base model, the behavior is adapted to meet the purpose of the project at hand.
"""

from __future__ import annotations

from typing import Any, no_type_check

import numpy as np
import pydantic

from optool.logging import LOGGER
from optool.serialization import SerializationAssistant
from optool.serialization.datetime_objects import DatetimeSerializer, ZoneInfoSerializer
from optool.serialization.numpy_objects import NumpyNdArraySerializer
from optool.serialization.pandas_objects import (PandasDataFrameSerializer, PandasDatetimeIndexSerializer,
                                                 PandasRangeIndexSerializer, PandasSeriesSerializer)
from optool.serialization.pint_objects import PintArraySerializer, PintQuantitySerializer, PintUnitSerializer


def _recursive_dict_eq(dict1, dict2):
    """
    Recursively compare two dictionaries, handling arrays.

    :param dict1: The first dictionary.
    :param dict2: The second dictionary.
    """
    if set(dict1.keys()) != set(dict2.keys()):
        return False

    for key in dict1.keys():
        val1, val2 = dict1[key], dict2[key]
        if isinstance(val1, dict) and isinstance(val2, dict):
            if not _recursive_dict_eq(val1, val2):
                return False
        elif not np.all(val1 == val2):
            return False

    return True


class BaseModel(pydantic.BaseModel):
    """
    Main base model used in this project.

    All data models inheriting from this base model have the following default behavior:

    - Model fields can be of arbitrary user types.
    - The creation of new fields at runtime is forbidden.
    - The validation on field assignment is enabled, not only on creation.
    - All attributes starting with an underscore are private.
    - Default values are also validated.
    - Do not copy models on validation, simply keep them untouched.
    - Allows to get the private field values as items of the `values` dictionary during validation.
    - Customized JSON loader that can deserialize specified objects.
    - Customized JSON encoder that can serialize specified objects.

    Furthermore, comparing models for equality invokes a recursive comparison of the two dictionaries, which allows to
    handle array-like elements.

    :::{seealso}
    https://pydantic-docs.helpmanual.io/usage/model_config/#change-behaviour-globally.
    :::
    """

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.__doc__ = ''  # Null out the representation docstring of every subclass

    # noinspection PyUnboundLocalVariable
    @no_type_check
    def __setattr__(self, name, value):
        offer_private_attrs: bool = getattr(self.__config__, 'offer_private_attrs_during_validation', False)

        if offer_private_attrs:
            private_values = {name: getattr(self, name) for name in self.__private_attributes__ if hasattr(self, name)}
            LOGGER.trace("Adding private attributes {} to the dictionary of {} with ID {} for validation.",
                         list(private_values.keys()), self.__class__.__name__, id(self))
            if any(key in self.__dict__ for key in private_values):
                raise NotImplementedError(f"Some of the private values {private_values.keys()} are already present as "
                                          f"keys in the dictionary, see {self.__dict__.keys()}.")
            keys_before = list(self.__dict__.keys()).copy()
            self.__dict__.update(private_values)

        try:
            # Call overridden method
            super().__setattr__(name, value)
        finally:
            # Always remove the private attributes
            if offer_private_attrs:
                LOGGER.trace("Removing private attributes {} from the dictionary of {} with ID {} again.",
                             list(private_values.keys()), self.__class__.__name__, id(self))

                for key in private_values:
                    self.__dict__.pop(key)

                keys_after = list(self.__dict__.keys()).copy()
                if keys_before != keys_after:
                    raise NotImplementedError(f"The keys before are not equal to the ones after manipulation, "
                                              f"i.e., {keys_before=} vs. {keys_after=}.")

    def __eq__(self, other: Any) -> bool:
        try:
            return super().__eq__(other)
        except Exception as e:
            if str(e) != "The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()":
                raise e

        if isinstance(other, BaseModel):
            other = other.dict()
        return _recursive_dict_eq(self.dict(), other)

    class Config(pydantic.BaseConfig):
        arbitrary_types_allowed = True
        """Allow arbitrary user types for fields."""

        extra = pydantic.Extra.forbid
        """Forbids creation of new fields at runtime."""
        # see https://pydantic-docs.helpmanual.io/usage/model_config/#options.

        validate_assignment = True
        """Enable validation on field assignment, not only on creation."""

        underscore_attrs_are_private = True
        """All attributes starting with an underscore are private."""

        validate_all = True
        """Validate also default values."""

        copy_on_model_validation = 'none'
        """Do not copy models on validation, simply keep them untouched."""

        offer_private_attrs_during_validation = True
        """Allows to get the private field values as items of the 'values' dictionary during validation."""

        json_loads = SerializationAssistant.json_loader
        """Customized JSON loader that can deserialize specified objects."""

        json_encoders = SerializationAssistant.register(
            NumpyNdArraySerializer(),
            PintQuantitySerializer(),
            PintUnitSerializer(),
            PintArraySerializer(),
            PandasDataFrameSerializer(),
            PandasSeriesSerializer(),
            PandasRangeIndexSerializer(),
            PandasDatetimeIndexSerializer(),
            ZoneInfoSerializer(),
            DatetimeSerializer(),
        )
        """Customized JSON encoder that can serialize specified objects."""
