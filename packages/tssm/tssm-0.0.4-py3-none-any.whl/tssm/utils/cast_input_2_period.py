"""
cast input to a period function
"""
from __future__ import annotations

from Levenshtein import distance

from tssm.utils.period import Period


MIN_DISTANCE = 5


def cast_input_2_period(value: Period | str | int) -> Period:
    """
    determine from value the period if it is no Period instance\n
    :param value: value for the period either Period enum, string or int.
    :return: Period
    """
    if isinstance(value, Period):
        return value
    if isinstance(value, str):
        min_distance = min(distance(value.upper(), period.name) for period in Period)
        if min_distance > MIN_DISTANCE:
            raise ValueError(f"{value} is no valid period name {[period.name for period in Period]}")
        for period in Period:
            distance_period = distance(value.upper(), period.name)
            if distance_period == min_distance:
                return period
    if isinstance(value, int):
        for period in Period:
            if period.value == value:
                return period
        raise ValueError(f"{value} is no valid period integer {[period.value for period in Period]}")
    raise ValueError(f"{value} is no valid period name, integer or Period")