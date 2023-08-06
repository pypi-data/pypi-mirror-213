"""
Utilities for streamlining logging for Python applications.

This module provides comprehensive logging capabilities, contributing to effective debugging and information tracking.
It furnishes classes that filter log messages based on different criteria, ensuring only relevant information is logged.
The module includes functions to set up the logger, measure and log the execution time of functions, further enhanced by
a decorator for function execution timing.
It also incorporates data elements defining available logging levels, message formats, logger settings, and an alias to
a logger instance. Overall, this module enables developers to implement robust logging mechanisms in their Python
applications.

::::{admonition} Example
:class: example dropdown

Setting up a logger works as for example in the following.
```python
import sys
from optool.logging import LogFilter, MessageFilter, setup_logger

log_filter = LogFilter(process="MainProcess")
log_filter.add(
    MessageFilter(module="optool.math", level="INFO"),
    MessageFilter(module="optool.uom", level="INFO"),
)
setup_logger(sink=sys.stdout, filter=log_filter, level='DEBUG')
```

It can then be used everywhere in the code as follows:
```python
from optool.logging import LOGGER

LOGGER.info("The value {!r} is logged on level info.", 13.0)
```
::::

"""

import time
from fnmatch import fnmatch
from functools import wraps
from typing import Any, Callable, Dict, List, Literal, Optional, Protocol, TextIO, Union

from loguru import logger
from pydantic import StrictStr, validate_arguments

LogLevels = Literal['TRACE', 'DEBUG', 'INFO', 'SUCCESS', 'WARNING', 'ERROR', 'CRITICAL']
"""
A Literal type representing available levels of logging.

The levels are, in increasing order of severity: `TRACE`, `DEBUG`, `INFO`, `SUCCESS`, `WARNING`, `ERROR`, `CRITICAL`.
"""


class MessageFilter:
    """
    A class that filters log messages based on specific criteria.

    The criteria available include the module name, function name, process name, and log level.

    :param module: Name of the module to filter on.
    :param function: Name of the function to filter on.
    :param process: Name of the process to filter on.
    :param level: The minimum log level of messages to accept.
    """

    __slots__ = 'module', 'function', 'process', 'level'

    @validate_arguments
    def __init__(self,
                 module: Optional[str] = None,
                 function: Optional[str] = None,
                 process: Optional[str] = None,
                 level: LogLevels = 'CRITICAL') -> None:

        self.module = None if module == "" else module
        self.function = None if function == "" else function
        self.process = None if process == "" else process
        self.level = logger.level(level)

    def is_accepted(self, record: Dict[str, Any]) -> bool:
        """
        Determines whether a given log record is accepted by this filter.

        :param record: The log record to evaluate.
        :return: {py:data}`True` if the record is accepted, {py:data}`False` otherwise.
        """

        if self.module is not None and self.module != record["name"]:
            return True
        if self.function is not None and self.function != record["function"]:
            return True
        if self.process is not None and self.process != record["process"].process__name:
            return True

        return record["level"].no >= self.level.no


class LogFilter:
    """
    A class that filters log messages based on a global minimum level, the process name, and a list of message filters.

    :param minimum_level: The minimum log level of messages to accept.
    :param process: The name of the process to filter on.
    """

    __slots__ = 'level', 'process', '_filters'

    @validate_arguments
    def __init__(self, *, minimum_level: LogLevels = 'TRACE', process: StrictStr = "*") -> None:
        self.level = logger.level(minimum_level)
        self.process = process
        self._filters: List[MessageFilter] = []

    def __call__(self, record) -> bool:
        """
        Determines whether a given log record is accepted by this filter.

        :param record: The log record to evaluate.
        :return: {py:data}`True` if the record is accepted, {py:data}`False` otherwise.
        """
        if (record["level"].no < self.level.no) or not fnmatch(record["process"].name, self.process):
            return False

        # noinspection PyShadowingBuiltins
        return all(filter.is_accepted(record) for filter in self._filters)

    # noinspection PyShadowingBuiltins
    def add(self, *filters: MessageFilter) -> None:
        """
        Adds one or more message filters to this log filter.

        :param filters: One or more {py:class}`MessageFilter` objects to add.
        """
        for filter in filters:
            if isinstance(filter, MessageFilter):
                self._filters.append(filter)


FORMAT = r"{time:YYYY-MM-DD HH:mm:ss.SSS} | {process.name} | <level>{level: <8}</level> | " \
         r"<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>{exception}"
"""
A string defining the formatting for log messages.

The log message format includes:
- Time of the log message.
- Name of the process that produced the log message.
- Level of the log message.
- Name of the module, function and line number where the log message originated.
- The actual log message.
- Any exception information (if applicable).
"""

logger_settings = dict(
    # rotation="10 MB",
    serialize=False,
    format=FORMAT,
    diagnose=True,
    backtrace=True,
    enqueue=True,
)
"""
A dictionary of settings for the logger.

These settings include:
- `serialize`: Specify if log messages are serialized to a structured format. (Default: {py:data}`False`)
- `format`: The format string to use for log messages. (Default: {py:data}`FORMAT`)
- `diagnose`: Specify if diagnostics information is added to the log messages. (Default: {py:data}`True`)
- `backtrace`: Specify if a stack trace is added to the log messages when an exception occurs. (Default:
  {py:data}`True`)
- `enqueue`: Specify if log messages are added to a queue to be processed asynchronously. (Default: {py:data}`True`)
"""


class Writable(Protocol):

    def write(self, message) -> None:
        pass


# noinspection PyShadowingBuiltins
def setup_logger(sink: Union[TextIO, Writable, str], filter: Optional[Callable[[Any], bool]], level: LogLevels) -> None:
    """
    Sets up the logger with a given sink, filter, and level.

    :param sink: Where the log messages should be sent. This can be either a {py:class}`~io.TextIOWrapper` object (e.g.
        {py:data}`sys.stdout`) or a string specifying a filename.
    :param filter: The filter to use for the log messages.
    :param level: The minimum log level to record.
    :raises ValueError: If sink is not a {py:class}`~io.TextIOWrapper` object or a string.
    """

    logger.remove()
    if isinstance(sink, str):
        logger.add(sink, mode="w", filter=filter, level=level, **logger_settings)  # type: ignore
    else:
        logger.add(sink, filter=filter, level=level, **logger_settings)  # type: ignore


LOGGER = logger
"""
Alias to an instance of the
[Loguru logger](https://loguru.readthedocs.io/en/stable/api/logger.html#module-loguru._logger).
"""


def time_function(func: Callable, log_level: LogLevels, *args, **kwargs):
    """
    Times the execution of a function and logs the result.

    :param func: The function to time.
    :param log_level: The level at which to log the result.
    :param args: Positional arguments to pass to the function.
    :param kwargs: Keyword arguments to pass to the function.
    :return: The result of the function.

    :::{seealso}
    https://loguru.readthedocs.io/en/stable/resources/recipes.html#logging-entry-and-exit-of-functions-with-a-decorator
    :::
    """
    start = time.time()
    result = func(*args, **kwargs)
    end = time.time()
    LOGGER.log(log_level, "Function {!r} executed in {:f} s.", func.__name__, end - start)
    return result


def timeit(func: Optional[Callable] = None, /, *, log_level: LogLevels = "DEBUG"):
    """
    A decorator to time the execution of a function and log the result.

    :param func: The function to be timed. If {py:data}`None`, returns a decorator to be used.
    :param log_level: The level at which to log the result.
    :return: If `func` is not {py:data}`None`, returns the result of the function. Otherwise, returns a decorator.

    ::::{admonition} Examples
    :class: example dropdown

    Annotate any function to log the time it takes to execute it as follows:

    ```python
    from optool.logging import timeit

    @timeit
    def my_function_to_time(*args):
        pass
    ```

    To specify a log level other than `DEBUG`, specify the desired level (here `INFO`) as an argument:

    ```python
    from optool.logging import timeit

    @timeit(log_level='INFO')
    def my_function_to_time(*args):
        pass
    ```
    ::::
    """

    def func_wrapper(*args, **kwargs):
        return time_function(func, log_level, *args, **kwargs)

    if func is not None:
        return func_wrapper

    # Need to wrap it one more time as func is None
    # noinspection PyShadowingNames
    def timeit_decorator(func):

        @wraps(func)
        def function_wrapper(*args, **kwargs):
            return time_function(func, log_level, *args, **kwargs)

        return function_wrapper

    return timeit_decorator
