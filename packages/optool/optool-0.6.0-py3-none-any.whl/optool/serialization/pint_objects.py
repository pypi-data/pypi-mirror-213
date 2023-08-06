"""
Serialization of [Pint](https://pypi.org/project/Pint/) objects.

This module offers custom serialization of {py:class}`~optool.uom.Quantity`, {py:class}`~optool.uom.Unit`, and
{py:class}`~pint_pandas.PintArray` objects.
"""

from __future__ import annotations

from typing import Any, Dict

from pint.util import to_units_container
from pint_pandas import PintArray

from optool.serialization import AllowedSerializedDictKeys, Serializer
from optool.uom import UNITS, Quantity, Unit


class PintQuantitySerializer(Serializer[Quantity]):
    """Serializer for {py:class}`optool.uom.Quantity` objects."""

    def serialize(self, obj: Quantity) -> Dict[AllowedSerializedDictKeys, Any]:
        return {'mag': obj.m, 'unit': obj.u}

    def deserialize(self, raw: Dict[AllowedSerializedDictKeys, Any]) -> Quantity:
        return Quantity(raw['mag'], raw['unit'])


class PintUnitSerializer(Serializer[Unit]):
    """Serializer for {py:class}`optool.uom.Unit` objects."""

    def serialize(self, obj: Unit) -> Dict[AllowedSerializedDictKeys, Any]:
        return dict(to_units_container(obj))  # type: ignore

    def deserialize(self, raw: Dict[AllowedSerializedDictKeys, Any]) -> Unit:
        return UNITS.Unit(UNITS.UnitsContainer(raw))


class PintArraySerializer(Serializer[PintArray]):
    """Serializer for {py:class}`pint_pandas.PintArray` objects."""

    def serialize(self, obj: PintArray) -> Dict[AllowedSerializedDictKeys, Any]:
        return {'mag': obj.quantity.m, 'unit': obj.quantity.u}

    def deserialize(self, raw: Dict[AllowedSerializedDictKeys, Any]) -> PintArray:
        return PintArray(raw['mag'], raw['unit'])
