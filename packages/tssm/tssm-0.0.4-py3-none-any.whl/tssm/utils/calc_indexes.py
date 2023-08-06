"""
define calculate index function
"""
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pandas as pd

from tssm.utils.period import Period

if TYPE_CHECKING:
    from numpy.typing import NDArray


def create_slice_list(periods_date: NDArray[np.uint32]) -> list[slice]:
    """
    function creates a list of slices from a period`s date array
    :param periods_date: periods date like zeros for the first 24 hours if a daily resolution is selected
    :return: list of slices
    """
    # create indexes
    test = [idx for idx, (date_0, date_1) in enumerate(zip(periods_date[range(-1, periods_date.size - 1)], periods_date)) if date_0 != date_1]
    test.append(periods_date.size)
    # return list of slices made from indexes
    return [slice(st, en) for st, en in zip(test[:-1], test[1:])]


def calculate_indexes(period: Period, date: NDArray[np.float64]) -> list[NDArray[np.int64]] | list[slice]:
    """
    calculate_average_scaling the indexes for the selected period
    :param period: period to calculate_average_scaling mean for 0: day; 2: week; 3: month; 4: year
    :param date: date of original values
    :return: None
    """
    if not isinstance(period, Period):
        raise TypeError(f"The period ({period}) should be: {list(Period)}")
    # period = day: getting index lists
    if period == Period.DAILY:
        days = date.astype("datetime64[D]").astype(np.uint32)
        return create_slice_list(days)

    # period = week: getting index lists
    if period == Period.WEEKLY:
        week = pd.to_datetime(date).strftime("%W").astype("int").to_numpy(dtype=np.uint32)
        return create_slice_list(week)

    # period = month: getting index lists
    if period == Period.MONTHLY:
        month = (date.astype("datetime64[M]").astype(np.uint32) % 12).astype(np.uint32)
        return create_slice_list(month)

    if period == Period.HOURLY:
        hours = pd.to_datetime(date).hour
        result: list[NDArray[np.int64]] = [np.where(hours == h)[0] for h in range(24)]
        return result

    if period == Period.HOURLY_AND_MONTHLY:
        hours = pd.to_datetime(date).hour
        month = pd.to_datetime(date).month - 1
        result = [np.where((hours == h) & (month == m))[0] for m in range(12) for h in range(24)]

        return result
    # period = year: getting index lists
    return [slice(0, date.size)]
