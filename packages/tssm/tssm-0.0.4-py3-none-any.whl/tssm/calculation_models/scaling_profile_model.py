"""
Time series scaling module script with the used calculation model classes
"""
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pandas as pd
from scipy import optimize

from tssm.utils import NoScalingProfileError, Period, calculate_indexes

from tssm.utils import scale_scaling_profile_2_same_sum
from .average_calculation_model import control_simultaneity_factor

if TYPE_CHECKING:
    from numpy.typing import NDArray

    from tssm.value_storage import DataStorage


def calculate_using_scaling_profile_model(
    data: DataStorage,
    period: Period,
    one_2_many: bool,
    number_of_buildings: float | int,
    simultaneity_factor: float,
    *,
    scaling_factor: pd.Series | NDArray[np.float64] | list[float] | None = None,
    same_sum: bool = False,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """
    calculate_average_scaling load using the scaling or average profile
    :param scaling_factor: scaling factor if simultaneity factor should not be considered
    :param same_sum: size scaling profile to the same sum as the original profile (default=False)
    :return: ValueStorage including the results
    """
    simultaneity_factor_use = simultaneity_factor if one_2_many else 1 / simultaneity_factor
    if data.scaling.size < 1:
        raise NoScalingProfileError()
    indexes = calculate_indexes(period, data.date)
    scale_scaling_profile_2_same_sum(data, one_2_many, same_sum, number_of_buildings, indexes)
    if scaling_factor is None:
        simultaneity_factor_new = determine_scaling_profile_simultaneity_factor(data, simultaneity_factor_use, indexes, one_2_many, number_of_buildings)
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
    calculate_scaling_profile_model_values(data, indexes, simultaneity_factor_new, one_2_many, number_of_buildings)
    return data.new, simultaneity_factor_new


def calculate_scaling_profile_model_values(
    data: DataStorage,
    indexes: list[NDArray[np.int64]] | list[slice],
    simultaneity_factor_new: NDArray[np.float64],
    one_2_many: bool,
    number_of_buildings: float | int,
) -> None:
    """
    Calculates the new value for each timestamp.
    :return:
    """
    # calculating new values for timestamps scaled to average of
    simultaneity_factor: NDArray[np.float64] = np.zeros(data.original.size, dtype=np.float64)
    for idx, d_f in zip(indexes, simultaneity_factor_new):
        simultaneity_factor[idx] = d_f

    if one_2_many:
        data.new = (data.original * simultaneity_factor + (1 - simultaneity_factor) * data.reference) * float(number_of_buildings)
        return
    data.new = data.original / simultaneity_factor / number_of_buildings + (1 - 1 / simultaneity_factor) * data.reference


def determine_scaling_profile_simultaneity_factor(
    data: DataStorage, simultaneity_factor: float, indexes: list[NDArray[np.int64]] | list[slice], one_2_many: bool, number_of_buildings: float | int
) -> NDArray[np.float64]:
    """
    determine the simultaneity factors for the scaling profile approach using scipy minimize\n
    """
    start_value = np.ones(1) * simultaneity_factor
    simultaneity_factor_new = np.zeros(len(indexes), dtype=np.float64)
    # determine normal distribution variance which leads to the desired simultaneity factor using scipy minimize
    for idx, idxes in enumerate(indexes):
        scaling_factor, small_error = calculate_with_scaling_profile_simple(simultaneity_factor, data, idxes, one_2_many, number_of_buildings)
        if small_error:
            simultaneity_factor_new[idx] = scaling_factor
            continue
        res = optimize.minimize(
            calculate_with_scaling_profile_complex,
            start_value,
            args=(data, idxes, one_2_many, simultaneity_factor, number_of_buildings),
            method="Nelder-Mead",
            bounds=((-5, 5),) if one_2_many else ((0.01, 5),),
            tol=1e-6,
        )
        simultaneity_factor_new[idx] = res.x[0]
        start_value = (res.x[0] if -0.5 * 0.99999 < res.x[0] < 5 * 0.99999 and not np.isclose(res.x[0], 0) else simultaneity_factor_new) * np.ones(1)
    # pd.DataFrame(self.simultaneity_factor.new).to_csv('s_f.csv')
    return simultaneity_factor_new


def calculate_with_scaling_profile_simple(
    simultaneity_factor: float, data: DataStorage, indexes: list[int] | slice | NDArray[np.int64], one_2_many: bool, number_of_buildings: float | int
):
    """
    calculate error in the maximal value for the start until end index and the given simultaneity factor\n
    :param indexes: indexes to calculate profile for
    :return: absolute error of the maximal values
    """
    maximum_in_period: float = np.max(data.original[indexes])
    idx_max = np.argmax(data.original[indexes])
    new_simultaneity_factor = (maximum_in_period * simultaneity_factor - data.reference[indexes][idx_max]) / (
        data.original[indexes][idx_max] - data.reference[indexes][idx_max]
    )
    if one_2_many:
        data.new = new_simultaneity_factor * data.original[indexes] + (1 - new_simultaneity_factor) * data.reference[indexes]
    else:
        new_simultaneity_factor = 1 / new_simultaneity_factor
        data.new = data.original[indexes] / new_simultaneity_factor + (1 - 1 / new_simultaneity_factor) * data.reference[indexes] * number_of_buildings
    # getting max of period
    return new_simultaneity_factor, abs(np.max(data.new) - maximum_in_period * simultaneity_factor) < 1e-6 * maximum_in_period


def calculate_with_scaling_profile_complex(
    new_simultaneity_factor: NDArray[np.float64],
    data: DataStorage,
    indexes: list[int] | slice,
    one_2_many: bool,
    simultaneity_factor: float,
    number_of_buildings: float | int,
):
    """
    calculate error in the maximal value for the start until end index and the given simultaneity factor\n
    :param new_simultaneity_factor: new guessed simultaneity factor to calculate error for
    :param indexes: indexes to calculate profile for
    :return: absolute error of the maximal values
    """
    # getting max of period
    maximum_in_period: float = np.max(data.original[indexes])
    if one_2_many:
        data.new = new_simultaneity_factor[0] * data.original[indexes] + (1 - new_simultaneity_factor[0]) * data.reference[indexes]
    else:
        data.new = data.original[indexes] / new_simultaneity_factor[0] + (1 - 1 / new_simultaneity_factor[0]) * data.reference[indexes] * number_of_buildings
    return abs(np.max(data.new) - maximum_in_period * simultaneity_factor)
