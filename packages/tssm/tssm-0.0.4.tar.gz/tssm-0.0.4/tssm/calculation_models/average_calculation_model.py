"""
Time series scaling module script with the used calculation model classes
"""
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pandas as pd

from tssm.utils import FactorAmountError, Period, calculate_indexes

if TYPE_CHECKING:
    from typing import Protocol

    from numpy.typing import NDArray

    class DataStorage(Protocol):  # pylint: disable=too-few-public-methods
        """DataStorage Protocol class"""
        reference: NDArray[np.float64]
        original: NDArray[np.float64]
        new: NDArray[np.float64]
        date: NDArray[np.float64]

    class SimultaneityFactor(Protocol):  # pylint: disable=too-few-public-methods
        """SimultaneityFactor Protocol class"""
        old: float
        use: float
        new: NDArray[np.float64]


def calculate_average_model(
    values: DataStorage,
    period: Period,
    simultaneity_factor: float,
    number_of_buildings: float | int,
    *,
    one_2_many: bool = True,
    scaling_factor: pd.Series | NDArray[np.float64] | list[float] | None = None,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """
    calculate_average_scaling load using the scaling or average profile

    Parameters
    ----------
    values: DataStorage
        values to calculate results for
    period: Period
        period to calculate average
    simultaneity_factor: SimultaneityFactor
        aim simultaneity factor
    number_of_buildings: int | float
        amount of buildings
    one_2_many: bool
        upscale or downscale values
    scaling_factor: pd.Series | NDArray[np.float64] | list[float] | None
        optional scaling factors then the simultaneity factor is ignored

    Returns
    -------
        tuple[NDArray[np.float64], NDArray[np.float64]]
        new time series and simultaneity factor
    """

    simultaneity_factor_use = simultaneity_factor if one_2_many else 1 / simultaneity_factor
    indexes = calculate_indexes(period, values.date)
    # calculating the average loads
    values.reference = np.array([np.mean(values.original[idx]) for idx in indexes])
    if scaling_factor is None:
        if isinstance(simultaneity_factor_use, (float, int)) or (isinstance(simultaneity_factor_use, np.ndarray) and simultaneity_factor_use.size == 1):
            simultaneity_factor_new = np.multiply(np.ones(len(indexes)), simultaneity_factor_use)
        # getting max of period
        maximum_in_period: NDArray[np.float64] = np.array([np.max(values.original[idx]) for idx in indexes])
        # calculating the min simultaneity factor
        dividend: NDArray[np.float64] = simultaneity_factor_use * maximum_in_period - values.reference
        divisor: NDArray[np.float64] = maximum_in_period - values.reference
        simultaneity_factor_new = np.divide(dividend, divisor, out=np.zeros_like(dividend), where=divisor != 0)
        if not one_2_many:
            simultaneity_factor_new[simultaneity_factor_new == 0] = 1
            simultaneity_factor_new = 1 / simultaneity_factor_new
    else:
        simultaneity_factor_new = (
            np.array(scaling_factor, dtype=np.float64)
            if isinstance(scaling_factor, list)
            else scaling_factor.to_numpy(dtype=np.float64)
            if isinstance(scaling_factor, pd.Series)
            else scaling_factor
        )
        if not one_2_many:
            simultaneity_factor_new[simultaneity_factor_new == 0] = 1
        control_simultaneity_factor(simultaneity_factor_new, indexes)
    calculate_average_model_values(values, simultaneity_factor_new, indexes, one_2_many, number_of_buildings)
    return values.new, simultaneity_factor_new


def control_simultaneity_factor(
    simultaneity_factor: NDArray[np.float64],
    indexes: list[NDArray[np.int64]] | list[slice],
) -> None:
    """
    Calculating if simultaneity factor is smaller than min simultaneity factor
    """
    if simultaneity_factor.size > len(indexes):
        raise FactorAmountError(False)
    if simultaneity_factor.size < len(indexes):
        raise FactorAmountError(True)


def calculate_average_model_values(
    values: DataStorage,
    simultaneity_factor: NDArray[np.float64],
    indexes: list[NDArray[np.int64]] | list[slice],
    one_2_many: bool,
    number_of_buildings: float | int,
) -> None:
    """
    Calculates the new value for each timestamp.
    :return:
    """
    # calculating new values for timestamps scaled to average of
    average: NDArray[np.float64] = np.zeros(values.original.size, dtype=np.float64)
    simultaneity_factor_local: NDArray[np.float64] = np.zeros(values.original.size, dtype=np.float64)
    for idx, avg, s_f in zip(indexes, values.reference, simultaneity_factor):
        average[idx] = avg
        simultaneity_factor_local[idx] = s_f

    if one_2_many:
        values.new = (values.original * simultaneity_factor_local + (1 - simultaneity_factor_local) * average) * number_of_buildings
        return
    values.new = (values.original / simultaneity_factor_local + (1 - 1 / simultaneity_factor_local) * average) / number_of_buildings
