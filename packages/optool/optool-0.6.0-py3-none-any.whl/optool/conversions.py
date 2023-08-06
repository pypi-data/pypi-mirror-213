"""
Date and time conversions for time-series data.

This module is dedicated to providing reliable conversions between common time-series data representations.
It offers functions that transform {py:class}`pandas.DatetimeIndex` objects into sample times or intervals expressed in
seconds and vice versa.
"""

from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from pandas import DatetimeIndex

from optool.uom import UNITS, Quantity


def datetime_index_to_samples(timestamps: DatetimeIndex) -> Quantity:
    """
    Converts a {py:class}`~pandas.DatetimeIndex` to a {py:data}`~optool.uom.Quantity` object representing the sample
    times in seconds.

    :param timestamps: The absolute timestamps.
    :return: A quantity object with the sample times in seconds since the first timestamp.
    """
    duration = (timestamps - timestamps[0]).to_pytimedelta()
    sample_times_seconds = np.array([val.total_seconds() for val in duration])
    return Quantity(sample_times_seconds, UNITS.second)


def datetime_index_to_intervals(timestamps: DatetimeIndex) -> Quantity:
    """
    Converts a {py:class}`~pandas.DatetimeIndex` to a {py:data}`~optool.uom.Quantity` object representing the intervals
    between timestamps in seconds.

    :param timestamps: The absolute timestamps.
    :return: A Quantity object with the intervals between the timestamps in seconds.
    """
    intervals_seconds = np.diff(timestamps.astype(np.int64)) / 10**9
    return Quantity(intervals_seconds, UNITS.second)


def samples_to_datetime_index(start: datetime, sample_times: Quantity) -> DatetimeIndex:
    """
    Converts a {py:data}`~optool.uom.Quantity` object representing sample times into a {py:class}`~pandas.DatetimeIndex`
    object.

    :param start: The starting date and time.
    :param sample_times: A quantity object with the sample times in seconds since the start time.
    :return: The absolute timestamps.
    """
    sample_times_seconds = sample_times.m_as(UNITS.second)
    duration = [timedelta(0, float(second)) for second in sample_times_seconds]
    datetime_values = [start + val for val in duration]
    return pd.DatetimeIndex(datetime_values)
