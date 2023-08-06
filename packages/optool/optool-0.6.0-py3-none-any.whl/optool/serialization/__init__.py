"""
Serialization of a variety of well-known Python data types.

The package features a collection of modules, each dedicated to the data types of a specific third-party package.
Accordingly, each module implements dedicated serializer classes that handle the respective serialization and
deserialization processes.
"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from collections import OrderedDict
from typing import Any, Callable, Dict, ForwardRef, Generic, Type, TypeVar, Union, get_args

from optool.logging import LOGGER

T = TypeVar("T")
"""Generic type variable used for defining the type of the objects a particular {py:class}`Serializer` can handle."""

AllowedSerializedDictKeys = Union[str, int, float, bool, None]
"""Type alias describing all types that are allowed as as keys of a dictionary that represents a serialized object."""


class Serializer(ABC, Generic[T]):
    """
    An abstract base class that defines a serializer for objects of a specific type.

    The serializer provides methods to convert objects of the specified type to a dictionary of primitive types and
    vice versa, thereby enabling the serialization and deserialization of objects for storage or transmission.

    The actual serialization and deserialization logic is to be implemented in subclasses. The type of the objects the
    corresponding serializers can handle are specified via generic type annotations.

    ::::{admonition} Example
    :class: example
    To serialize objects of type {py:class}`zoneinfo.ZoneInfo`, the following implementation could be used.

    ```python
    from zoneinfo import ZoneInfo

    class ZoneInfoSerializer(Serializer[ZoneInfo]):

        def serialize(self, obj: ZoneInfo) -> Dict[AllowedSerializedDictKeys, Any]:
           return {'key': obj.key}

        def deserialize(self, raw: Dict[AllowedSerializedDictKeys, Any]) -> ZoneInfo:
            return ZoneInfo(raw['key'])
    ```

    To enable serialization of all {py:class}`zoneinfo.ZoneInfo` within fields or sub-fields of any
    {py:class}`pydantic.BaseModel`, the class is added to the {py:class}`SerializationAssistant` via
    ```python
    SerializationAssistant.register(ZoneInfoSerializer())
    ```
    the output of which is set {py:attr}`pydantic.BaseConfig.json_encoders`.
    ::::

    :::{seealso}
    {py:class}`SerializationAssistant` and implementation of {py:attr}`optool.BaseModel.Config.json_encoders`.
    :::
    """

    _type_T: Type

    def __init_subclass__(cls) -> None:
        # Get the generic type. Approach taken from https://stackoverflow.com/a/71720366
        # noinspection PyUnresolvedReferences
        cls._type_T = get_args(cls.__orig_bases__[0])[0]  # type: ignore

    @classmethod
    def get_type(cls) -> Type:
        """
        Gets the type of the objects this serializer is supposed to handle.

        :return: The type of the objects to serialize and deserialize.
        """
        return cls._type_T

    @classmethod
    def get_type_name(cls) -> str:
        """
        Gets the name of the type of the objects this serializer is supposed to handle.

        :return: {py:meth}`get_type` converted to a string.
        """
        return str(cls.get_type())

    @abstractmethod
    def serialize(self, obj: T) -> Dict[AllowedSerializedDictKeys, Any]:
        """
        Serializes an object to a dictionary of primitive types.

        :param obj: The object to serialize.
        :return: Dictionary describing the serialized object, potentially containing values the need further
            serialization.
        """
        raise NotImplementedError()

    @abstractmethod
    def deserialize(self, raw: Dict[AllowedSerializedDictKeys, Any]) -> T:
        """
        Deserializes a dictionary of primitive types to an object.

        :param raw: The raw descriptive content of the object from which the latter is to be created.
        :return: The deserialized object.
        """
        raise NotImplementedError()


class SerializationAssistant:
    """Utility class holding all serializers registered."""

    _serializers: Dict[str, Serializer] = {}

    @classmethod
    def register(cls, *serializers: Serializer) -> Dict[Union[Type[Any], str, ForwardRef], Callable]:
        """
        Registers the serializers specified.

        :param serializers: The serializers to register
        :returns: Dictionary mapping types to the corresponding JSON encoders.
        """
        for serializer in serializers:
            obj_type = serializer.get_type()
            obj_type_name = serializer.get_type_name()
            LOGGER.debug("Registering serializer for {}.", obj_type)
            if obj_type_name in cls._serializers:
                raise ValueError(f"There is already an entry in the registry for {obj_type_name}.")
            cls._serializers[obj_type_name] = serializer

        return {serializer.get_type(): cls._create_json_encoder(serializer) for serializer in serializers}

    @staticmethod
    def _create_json_encoder(serializer: Serializer[T]) -> Callable[[T], Dict[AllowedSerializedDictKeys, Any]]:

        def _encode_obj(obj: T) -> Dict[AllowedSerializedDictKeys, Any]:
            return OrderedDict({'obj_type': serializer.get_type_name()}, **serializer.serialize(obj))

        return _encode_obj

    @classmethod
    def json_loader(cls, raw: Union[str, bytes]) -> Any:
        """
        Loads a JSON object from a string or bytes and parses it into a Python object.

        This method uses the custom object pair hook function defined in this class to parse the
        JSON object, providing flexibility in how the JSON object is converted to a Python object.

        :param raw: The JSON object to be loaded, represented as a string or bytes.
        :return: The Python object resulting from parsing the JSON object.
        """
        return json.loads(raw, object_pairs_hook=cls._parse_raw)

    @classmethod
    def _parse_raw(cls, tuples: list[tuple[Any, Any]]) -> Any:
        dct = OrderedDict(tuples)

        if 'obj_type' not in dct:
            return dct

        obj_type = dct.pop('obj_type')
        if obj_type not in cls._serializers:
            raise ValueError(f"The registry has no entry for {obj_type}. Have only {cls._serializers.keys()}.")
        return cls._serializers[obj_type].deserialize(dct)
