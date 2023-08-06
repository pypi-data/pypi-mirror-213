"""
Representation of decision variables for Nonlinear Programs (NLP)s.

This module offers utilities for defining and manipulating decision variables in an NLP formulation.
With functions to handle the initialization, updates, and querying of variable sets, this module streamlines the
creation and management of decision variables, providing a flexible and intuitive interface for designing numerical
optimization problems.
"""

import math
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union, final

import casadi
import numpy as np
from pydantic import StrictBool, root_validator, validator

from optool.core import BaseModel
from optool.fields.misc import NonEmptyStr
from optool.fields.numeric import ImmutableArray
from optool.fields.quantities import QuantityLike, UnitLike
from optool.fields.util import validate
from optool.logging import LOGGER
from optool.math import SYMBOLIC_TYPES, has_offset, num_elements
from optool.uom import UNITS, Quantity, Unit


class OptimizationVariable(BaseModel, ABC):
    """Abstract representation of a decision variable for the formulation of a nonlinear program (NLP)."""

    _frozen_nominal_values: StrictBool = False
    """Indicator flag to ensure that nominal values cannot be changed anymore. Shouldn't be set manually."""

    name: NonEmptyStr
    """The name of the decision variable."""

    unit: Optional[UnitLike] = None
    """The physical unit of the decision variable."""

    initial_guess: QuantityLike[Any, ImmutableArray]
    """The initial values to provide to the solver."""

    lower_bounds: QuantityLike[Any, ImmutableArray]
    """The minimum values allowed for the decision variable."""

    upper_bounds: QuantityLike[Any, ImmutableArray]
    """The maximum values allowed for the decision variable."""

    nominal_values: QuantityLike[Any, ImmutableArray]
    """The nominal values for scaling the variables."""

    solution: Optional[QuantityLike[Any, ImmutableArray]] = None
    """The solution obtained after solving the NLP."""

    lagrange_multipliers: Optional[QuantityLike[Any, ImmutableArray]] = None
    """The lagrange multipliers obtained after solving the NLP."""

    @final
    @validator('unit', allow_reuse=True)
    def _is_offset_free(cls, value):
        return validate(value, lambda x: not has_offset(x), 'The unit should be offset-free, but {value} is not.')

    @final
    @validator('initial_guess', 'lower_bounds', 'upper_bounds', 'nominal_values', allow_reuse=True)
    def _inflate_scalar_if_necessary(cls, value: Quantity, values: Dict):
        if np.size(value.magnitude) == 1:
            array_lengths, numerical_values, unique_lengths = cls._get_array_lengths(values)

            if np.size(unique_lengths) == 1 and unique_lengths > 1:
                return Quantity(np.full(unique_lengths, value.magnitude), value.units)

        return value

    @final
    @validator('initial_guess', 'nominal_values', allow_reuse=True)
    def _is_finite(cls, value):
        return validate(value, lambda x: np.all(np.isfinite(x)), 'All array elements must be finite, but have {value}.')

    @final
    @validator('lower_bounds', 'upper_bounds', allow_reuse=True)
    def _is_not_nan(cls, value):
        return validate(value, lambda x: np.all(~np.isnan(x)), 'At least one array elements is NaN, see {value}.')

    @final
    @validator('nominal_values', allow_reuse=True)
    def _is_not_zero(cls, value):
        return validate(value, lambda x: np.all(x != 0), 'At least one array elements is zero, see {value}.')

    @final
    @validator('nominal_values', allow_reuse=True)
    def _is_not_frozen(cls, value, values: Dict):
        flag_field_name = '_frozen_nominal_values'
        frozen = values.get(flag_field_name, cls.__private_attributes__[flag_field_name].default)
        return validate(value, not frozen, 'Cannot change nominal value after retrieving the regular variable.')

    @final
    @root_validator(allow_reuse=True)
    def _is_consistent(cls, values: Dict) -> Dict:
        array_lengths, numerical_values, unique_lengths = cls._get_array_lengths(values)

        if np.size(unique_lengths) != 1:
            raise ValueError(f"Not all arrays have the same number of elements, see {array_lengths}")

        unit = values['unit'] or UNITS.dimensionless
        array_units: Dict[str, Unit] = {key: values[key].units for key in numerical_values}

        if any(not unit.is_compatible_with(other) for other in list(array_units.values())):
            raise ValueError(f"Not all numerical values have compatible units, see {array_units}")

        return values

    @staticmethod
    def _get_array_lengths(values: Dict):
        numerical_values = [key for (key, value) in values.items() if isinstance(value, Quantity)]
        array_lengths: Dict[str, int] = {key: num_elements(values[key].magnitude) for key in numerical_values}
        unique_lengths = np.unique(list(array_lengths.values()))
        return array_lengths, numerical_values, unique_lengths

    @property
    @abstractmethod
    def normed(self) -> SYMBOLIC_TYPES:
        r"""
        The normed symbols, i.e., the actual decision variables not multiplied by the nominal value.

        The normed symbols are the actual variable seen by the optimizer. These values should ideally be in the range of
        $\pm 1$ to enhance numerical stability. However, formulating an optimization problem can become inconvenient if
        the user always has to keep track of the normalization value. Hence, {py:attr}`OptimizationVariable.regular`
        offers the _actual_ variable value that includes both the nominal value and the physical unit specified.
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def regular(self) -> Quantity:
        """
        The regular symbols, i.e., the decision variables multiplied by the nominal value.

        The regular symbols typically are used to formulate any constraints of the optimization problem. They include
        both the nominal value and the physical unit specified.
        """
        raise NotImplementedError()

    @abstractmethod
    def length(self) -> int:
        """
        The number of elements (i.e., the vector length) of this optimization variable.

        :return: An integer representing the number of elements of this optimization variable.
        """
        raise NotImplementedError()

    def _freeze_nominal_values(self):
        if not self._frozen_nominal_values:
            LOGGER.debug("Freezing nominal values of variable named {}.", self.name)
            self._frozen_nominal_values = True

    @staticmethod
    def casadi(name: str, n: int, unit: Optional[UnitLike] = None):
        """
        Creates a [CasADi](https://web.casadi.org) variable.

        :param name: Name of the new variable.
        :param n: Number of elements of the new variable.
        :param unit: Physical unit of the new variable.
        :return: The variable created.
        """
        return CasadiVariable(name, n, unit)


class CasadiVariable(OptimizationVariable):
    """Representation of a decision variable using the modeling language [CasADi](https://web.casadi.org)."""

    _symbols: casadi.SX

    def __init__(self, name: str, n: int, unit: Optional[UnitLike] = None):
        super().__init__(name=name,
                         unit=unit,
                         initial_guess=Quantity(np.zeros((n,)), unit),
                         lower_bounds=Quantity(np.full((n,), -math.inf), unit),
                         upper_bounds=Quantity(np.full((n,), math.inf), unit),
                         nominal_values=Quantity(np.ones((n,)), unit))
        self._symbols = casadi.SX.sym(self.name, n, 1)

    @final
    @root_validator
    def _is_consistent_with_symbol_size(cls, values: Dict) -> Dict:
        numerical_values = [key for (key, value) in values.items() if isinstance(value, Quantity)]
        array_lengths: Dict[str, int] = {key: np.size(values[key].magnitude) for key in numerical_values}

        if '_symbols' not in values:  # cannot validate yet (class is still being initialized)
            return values

        symbol_size = values['_symbols'].numel()
        if any(symbol_size != size for size in array_lengths.values()):
            raise ValueError(f"Not all numerical values have the same number of elements than the number of symbols "
                             f"({symbol_size}), see {array_lengths}")

        return values

    @property
    def normed(self) -> casadi.SX:
        return self._symbols

    @property
    def regular(self) -> Union[casadi.SX, Quantity]:
        self._freeze_nominal_values()
        return self._symbols * self.nominal_values

    def length(self) -> int:
        return self._symbols.numel()
