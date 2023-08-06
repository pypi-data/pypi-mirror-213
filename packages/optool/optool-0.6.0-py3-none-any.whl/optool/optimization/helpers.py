"""
Utilities that assist the formulation and analysis of optimization problems.

This module provides ancillary features for the optimization process.
It houses tools for organizing debug information, handling solver responses, and managing Ipopt options.
"""

from datetime import timedelta
from typing import TYPE_CHECKING, Any, Dict

import humanize
import pandas as pd
from pydantic import Field, StrictBool, StrictFloat, StrictStr

from optool.core import BaseModel
from optool.fields.containers import ConstrainedMutatingList
from optool.fields.misc import NonEmptyStr
from optool.fields.quantities import QuantityLike
from optool.util import ValueRange

if TYPE_CHECKING:
    ValueRangeList = list
else:

    class ValueRangeList(ConstrainedMutatingList[ValueRange]):
        pass


class DebugInfo(BaseModel):
    """Container for debug information related to the solving of an optimization problem."""

    problem_name: NonEmptyStr = Field(allow_mutation=False)
    """The name of the optimization problem."""

    normed_variable_values: ValueRangeList = []
    normed_constraints_lagrange_multipliers: ValueRangeList = []

    def print_details(self) -> None:
        for val in self.get_details():
            print(val)

    def get_details(self) -> list[str]:
        prefix = "|   "
        separator = f"{prefix}{'-' * 60}"
        details = [
            f"Debug information for the optimization problem entitled '{self.problem_name}'",
            f"{prefix}Normed values of the decision variables (as seen by the solver):", separator
        ]

        self._append_normed_values(details, prefix, self.normed_variable_values)
        details.extend((
            separator,
            f"{prefix}Normed values of the lagrange multipliers of the constraints (as seen by the solver):",
        ))
        self._append_normed_values(details, prefix, self.normed_constraints_lagrange_multipliers)
        details.append(separator)
        return details

    @staticmethod
    def _append_normed_values(details: list[str], prefix: str, normed_values: list[ValueRange]) -> None:
        attributes_to_show = ["min", "avg", "max", "max_abs"]
        df = pd.DataFrame(index=attributes_to_show)
        for val in normed_values:
            df[f"{val.name}:  "] = [getattr(val, attr) for attr in attributes_to_show]
        table_rows = df.transpose().to_string().split("\n")
        details.extend(f"{prefix}{row}" for row in table_rows)


class UnsuccessfulOptimization(Exception):
    """Unsuccessful attempt to solve the optimization problem."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class SolverResponse(BaseModel, frozen=True):
    """The response returned by the solver."""

    problem_name: StrictStr
    """The name of the optimization problem."""

    function_value: QuantityLike[Any, StrictFloat]
    """The final value of the objective."""

    success: StrictBool
    """Indication if the optimization problem was solved successfully."""

    solver_status: Dict[str, Any]
    """Details on the status of the numerical solver."""

    debug_info: DebugInfo
    """Details of the solution found that can be used to fix potential problems or analyze the performance."""

    def get_return_status(self) -> str:
        """Gets the return status of the solver."""
        return self.solver_status["return_status"]

    def get_number_of_iterations(self) -> int:
        """Gets the number of iterations used by the solver."""
        return int(self.solver_status["iter_count"])

    def get_solver_time(self) -> timedelta:
        """
        Gets the time it took the solver to find the solution.

        :return: The "wall time", i.e. actual physical time it took to solve the problem.

        :::{seealso}
        [Wikipedia: Elapsed real time](wiki:Elapsed_real_time)
        :::
        """

        # See https://groups.google.com/g/casadi-users/c/dMSGV8KII30?pli=1 for an explanation of both
        # 't_wall_total' and 't_proc_total' and the difference between them.
        return timedelta(seconds=self.solver_status["t_wall_total"])

    def guarantee_success(self) -> None:
        """
        Checks if the optimization was successful.

        :raises UnsuccessfulOptimization: If the optimization was not successful
        """
        if not self.success:
            raise UnsuccessfulOptimization(f"The problem entitled '{self.problem_name}' was not solved successfully, "
                                           f"but returned with '{self.get_return_status()}'.")

    def get_message(self) -> str:
        """
        Returns a message summarizing the results of the optimization.

        :return: A string message summarizing the results of the optimization
        """
        success_msg = "" if self.success else "NOT "
        duration_str = humanize.naturaldelta(self.get_solver_time(), minimum_unit="microseconds")
        return f"The optimization problem {self.problem_name!r} was {success_msg}solved successfully " \
               f"after {self.get_number_of_iterations()} iterations and {duration_str} " \
               f"with return status {self.get_return_status()!r}."


class IpoptOption(BaseModel, frozen=True):
    """
    The options available in Ipopt.

    :::{seealso}
    [Ipopt documentation](https://coin-or.github.io/Ipopt/OPTIONS.html#OPT_print_options_documentation)
    :::
    """

    category: NonEmptyStr
    """The category of the option."""

    name: NonEmptyStr
    """The name of the option."""

    values: NonEmptyStr
    """The possible values to set."""

    description: NonEmptyStr
    """The description of the option."""

    def pretty_print(self) -> None:
        """Prints a formatted message describing the option."""
        print(f"{self.name}: ({self.category})\t{self.values}:\n{self.description}")
