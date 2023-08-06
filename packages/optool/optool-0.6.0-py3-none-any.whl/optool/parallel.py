"""
Utilities to execute code in parallel across multiple processes.
"""

import os
from multiprocessing import Pool, current_process
from typing import Any, Callable, Iterable

from pydantic import DirectoryPath, StrictInt

from optool.core import BaseModel
from optool.logging import LOGGER, LogFilter, LogLevels, setup_logger, timeit


def _get_system_cpu_counts() -> int:
    if count := os.cpu_count():
        return count
    raise ValueError("Cannot determine number of CPUs of this system.")


class ParallelExecutor(BaseModel):
    """
    Utility class to execute a function in parallel across multiple processes.

    ::::{admonition} Example
    :class: example dropdown

    ```python
    import os
    import tempfile
    from pathlib import Path

    from optool import LOGGER
    from optool.parallel import ParallelExecutor

    # Define a simple function that we want to execute in parallel
    def calculate(n):
        LOGGER.debug("Performing calculation with {}.", n)
        return n * n


    if __name__ == '__main__':
        temporary_directory = tempfile.TemporaryDirectory(suffix=None, prefix="test_parallel_")
        log_path = Path(temporary_directory.name)

        # Define the inputs for the function
        inputs = list(range(10))

        # Create an instance of ParallelExecutor
        LOGGER.info("Executing function {!r} with arguments {} in parallel.", calculate.__name__, inputs)
        executor = ParallelExecutor(function=calculate,
                                    log_sink=log_path,
                                    log_level='INFO',
                                    processes=4)

        # Execute the function in parallel
        results = executor.run(inputs)
        LOGGER.info("Done. Solver output is written to {}. Results are {}.", log_path, results)

        log_files = os.listdir(log_path)
        LOGGER.info("Content of output directory is: {}", log_files)
    ```
    """

    function: Callable
    """The function to execute."""

    log_sink: DirectoryPath
    """The directory path where to store the logs."""

    log_level: LogLevels = 'TRACE'
    """The level of logging, default to 'TRACE'."""

    processes: StrictInt = _get_system_cpu_counts()
    """The number of processes to spawn, defaults to the system CPU count."""

    @timeit(log_level='INFO')
    def run(self, *args: Any) -> Any:
        """
        Executes the function across multiple processes.

        :param args: Arguments to be passed to the function.
        :return: A list of results from each process.
        """
        if len(args) == 1 and isinstance(args, Iterable):
            args = args[0]
        processes = min([self.processes, len(args)])
        LOGGER.info("Executing function {} on {} processes in parallel.", self.function.__name__, processes)
        # TODO: Figure out if this is actually necessary, and if so, how to extract the logger and add it again
        # LOGGER.remove()  # Default "sys.stderr" sink cannot be pickled
        with Pool(processes=processes) as pool:
            out = pool.map(self.run_subprocess, args)
        return out

    def run_subprocess(self, arg: Any) -> Any:
        """
        Sets up the logger for a subprocess, runs the function on a single argument, and then tears down the logger.

        :param arg: The argument to be passed to the function.
        :return: The result of the function execution.
        """
        self.setup_subprocess_logger()
        out = timeit(self.function, log_level='INFO')(arg)
        self.tear_down_subprocess_logger()
        return out

    def setup_subprocess_logger(self) -> None:
        """
        Sets up the logger for a subprocess.
        """
        process = current_process()
        log_file_name = str(self.log_sink.absolute() / f"log_{process.name}.log")
        setup_logger(sink=log_file_name, filter=LogFilter(), level=self.log_level)

    @staticmethod
    def tear_down_subprocess_logger() -> None:
        """
        Tears down the logger for a subprocess.

        This makes sure the queue (consumed by a thread started internally) is left in a stable state.
        """
        LOGGER.complete()
