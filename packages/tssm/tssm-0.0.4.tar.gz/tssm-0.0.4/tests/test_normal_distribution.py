"""
test the normal distribution calculation approach
"""

from math import erf, sqrt
from os.path import dirname, realpath
from typing import List

import numpy as np
from numpy import allclose, append, arange, float32, isclose, ndarray, zeros
from pytest import raises

from tssm import TimeSeriesScalingModule as tssm
from tssm.calculation_models import SimultaneityFactor
from tssm.calculation_models.normal_distribution_model import NoNumpyArrayError
from tssm.time_series_scaling_module import CalculationUsingNormalDistribution

FOLDER = dirname(realpath(__file__))


def test_normal_distribution():
    """
    test the normal distribution calculation approach for a 8760 hours year with a variance determination
    """
    # set values
    simultaneity_factor = [0.95, 0.8914, 0.7146, 0.5123]
    sigma = [0.6406650602817532, 1.1595687866210942, 4.822046089172372, 15.041768264770537]
    # check correct calculation for every entry
    for s_f, sig in zip(simultaneity_factor, sigma):
        check_normal_distribution(s_f, sig)


def test_normal_distribution_property():
    """
    test the normal distribution calculation approach for a 8760 hours year with a given variance
    """
    # set values
    simultaneity_factor = [0.95, 0.8914, 0.6432]
    sigma = [0.6406650602817532, 1.1595687866210942, 15.041768264770537]
    # check correct calculation for every entry
    for s_f, sig in zip(simultaneity_factor, sigma):
        check_normal_distribution_property(s_f, sig)


def test_normal_distribution_with_date():
    """
    test the normal distribution calculation approach for a 8760 hours year with a variance determination and a provided date
    """
    # set values
    simultaneity_factor = [0.95, 0.8914, 0.7146, 0.5123]
    sigma = [0.6406650602817532, 1.1595687866210942, 4.822046089172372, 15.041768264770537]
    # check correct calculation for every entry
    for s_f, sig in zip(simultaneity_factor, sigma):
        check_normal_distribution(s_f, sig, False, True)


def test_normal_distribution_with_given_sigma():
    """
    test the normal distribution calculation approach for a 8760 hours year with a given variance
    """
    # set values
    sigma: List[float] = list(arange(0.2, 1, 0.1)) + list(arange(1, 5, 0.5)) + list(arange(5, 25, 1))
    simultaneity_factor = [1] * len(sigma)
    # check correct calculation for every entry
    for s_f, sig in zip(simultaneity_factor, sigma):
        check_normal_distribution(s_f, sig, True)


def test_normal_distribution_with_given_sigma_property():
    """
    test the normal distribution calculation approach for a 8760 hours year with a given variance
    """
    # set values
    sigma: List[float] = list(arange(0.2, 1, 0.1)) + list(arange(1, 5, 0.5)) + list(arange(5, 25, 1))
    simultaneity_factor = [1] * len(sigma)
    # check correct calculation for every entry
    for s_f, sig in zip(simultaneity_factor, sigma):
        check_normal_distribution_property(s_f, sig, True, False)


def test_normal_distribution_with_given_sigma_and_date():
    """
    test the normal distribution calculation approach for a 8760 hours year with a given variance and date
    """
    # set values
    sigma: List[float] = list(arange(0.2, 1, 0.1)) + list(arange(1, 5, 0.5)) + list(arange(5, 25, 1))
    simultaneity_factor = [1] * len(sigma)
    # check correct calculation for every entry
    for s_f, sig in zip(simultaneity_factor, sigma):
        check_normal_distribution(s_f, sig, True, True)


def test_normal_distribution_fail_maximal_variance():
    """
    test if the normal distribution calculation fails due to a too small simultaneity factor
    """
    with raises(ValueError):
        check_normal_distribution(0.05, 5)


def test_normal_distribution_fail_minimal_variance():
    """
    test if the normal distribution calculation fails due to a too high simultaneity factor
    """
    with raises(ValueError):
        check_normal_distribution(1.01, 5)


def check_normal_distribution(simultaneity_factor: float, sigma: float, sigma_given: bool = False, use_date: bool = False):
    """
    checks if the normal distribution approach for a 8760 hours data works correctly for the provided inputs.\n
    :param simultaneity_factor: simultaneity factor
    :param sigma: variance
    :param sigma_given: True if the variance should be considered as given
    :param use_date:  True if the date should be considered
    """
    number_of_buildings = 61
    # init class and calculate_average_scaling normal distribution up scaling
    tssm_test = tssm(number_of_buildings, simultaneity_factor)
    if use_date:
        tssm_test.data.read_profile_from_csv_with_date(f"{FOLDER}/test_data/profiles/data.csv", "Heating", "Date")
    else:
        tssm_test.data.read_profile_from_csv(f"{FOLDER}/test_data/profiles/data.csv", "Heating")
    calculated_values = tssm_test.calculate_using_normal_distribution(sigma=sigma) if sigma_given else tssm_test.calculate_using_normal_distribution()

    if not sigma_given:
        # check if the maximal value is not exceeding the maximal value times the simultaneity factor
        assert isclose(max(calculated_values) / max(tssm_test.data.original * number_of_buildings), simultaneity_factor)

    # check if the sum is equal
    assert isclose(sum(calculated_values), sum(tssm_test.data.original * number_of_buildings), rtol=0.0005)

    # calculate_average_scaling normal distribution up scaling manually
    values = zeros(len(tssm_test.data.original))
    idx = append(arange(len(tssm_test.data.original)), arange(len(tssm_test.data.original)))
    for i, values_original in enumerate(tssm_test.data.original):
        for j in range(i - 4 * int(sigma + 0.5) - 1, i + 4 * int(sigma + 0.5) + 2):
            values[idx[j]] += values_original * (erf((j + 0.5 - i) / sqrt(2) / sigma) - erf((j - 0.5 - i) / sqrt(2) / sigma)) / 2

    values = values * number_of_buildings
    # check if all values are nearly equal / correct
    assert allclose(values, calculated_values)


def check_normal_distribution_property(simultaneity_factor: float, sigma: float, sigma_given: bool = False, use_date: bool = False):
    """
    checks if the normal distribution approach for a 8760 hours data works correctly for the provided inputs.\n
    :param simultaneity_factor: simultaneity factor
    :param sigma: variance
    :param sigma_given: True if the variance should be considered as given
    :param use_date:  True if the date should be considered
    """
    number_of_buildings = 61
    # init class and calculate_average_scaling normal distribution up scaling
    tssm_test_up = tssm(number_of_buildings, simultaneity_factor)
    if use_date:
        tssm_test_up.data.read_profile_from_csv_with_date(f"{FOLDER}/test_data/profiles/data.csv", "Heating", "Date")
    else:
        tssm_test_up.data.read_profile_from_csv(f"{FOLDER}/test_data/profiles/data.csv", "Heating")
    calculated_values_up = tssm_test_up.calculate_using_normal_distribution(**{"sigma": sigma} if sigma_given else {})
    tssm_test_down = tssm(number_of_buildings, simultaneity_factor, one_2_many=False)
    tssm_test_down.data.set_profile_from_numpy_array(calculated_values_up)
    calculated_values_down = tssm_test_down.calculate_using_normal_distribution(**{"sigma": sigma} if sigma_given else {})

    if not sigma_given:
        assert np.isclose(max(calculated_values_up) / number_of_buildings / simultaneity_factor, max(calculated_values_down))

    assert np.isclose(max(tssm_test_up.data.original), max(calculated_values_down))

    for time_1, (j, i) in enumerate(zip(tssm_test_up.data.original, calculated_values_down)):
        if not isclose(j, i, atol=0.01):
            print(time_1, j, i)
    assert np.allclose(tssm_test_up.data.original, calculated_values_down, atol=0.01)


def test_normal_distribution_with_15_min_time_step_and_given_sigma():
    """
    test the normal distribution calculation approach for a 15-min hour year with a given variance
    """
    # set values
    sigma: List[float] = list(arange(0.2, 1, 0.1)) + list(arange(1, 5, 0.5)) + list(arange(5, 25, 5))
    simultaneity_factor = [1] * len(sigma)
    # check correct calculation for every entry
    for s_f, sig in zip(simultaneity_factor, sigma):
        check_normal_distribution_with_15_min_time_step(s_f, sig, True)


def test_normal_distribution_with_15_min_time_step():
    """
    test the normal distribution calculation approach for a 15-min hour year with a variance determination
    """
    # set values
    sigma: List[float] = [0.2204484939575188, 0.45064792633056594, 0.9463764190673827, 1.8090370178222674]
    simultaneity_factor = [0.9517, 0.8802, 0.7108, 0.5043]
    # check correct calculation for every entry
    for s_f, sig in zip(simultaneity_factor, sigma):
        check_normal_distribution_with_15_min_time_step(s_f, sig)


def test_many_normal_distribution_with_15_min_time_step():
    """
    test the normal distribution calculation approach for many 15-min hour year with a variance determination
    """
    number_of_buildings = 701
    for i in range(30):
        # init class and calculate_average_scaling normal distribution up scaling
        tssm_test = tssm(number_of_buildings, 0.9)
        tssm_test.data.read_profile_from_csv_with_date(f"{FOLDER}/test_data/profiles/data_profiles_15_min.csv", f"profile_{i}", "Date", date_format="%Y-%m-%d %H:%M")
        try:
            tssm_test.calculate_using_normal_distribution()
        except ValueError:
            continue


def check_normal_distribution_with_15_min_time_step(simultaneity_factor: float, sigma: float, sigma_given: bool = False):
    """
    checks if the normal distribution approach for a 15-min hour data works correctly for the provided inputs.\n
    :param simultaneity_factor: simultaneity factor
    :param sigma: variance
    :param sigma_given: True if the variance should be considered as given
    """
    number_of_buildings = 701
    # init class and calculate_average_scaling normal distribution up scaling
    tssm_test = tssm(number_of_buildings, simultaneity_factor)
    tssm_test.data.read_profile_from_csv_with_date(f"{FOLDER}/test_data/profiles/data_profiles_15_min.csv", "profile_0", "Date", date_format="%Y-%m-%d %H:%M")
    calculated_values = tssm_test.calculate_using_normal_distribution(**{"sigma": sigma} if sigma_given else {})

    if not sigma_given:
        # check if the maximal value is not exceeding the maximal value times the simultaneity factor
        print(max(calculated_values) / max(tssm_test.data.original * number_of_buildings), simultaneity_factor)
        assert isclose(max(calculated_values) / max(tssm_test.data.original * number_of_buildings), simultaneity_factor, rtol=0.00005)

    # check if the sum is equal
    # print(sum(calculated_values), sum(tssm_test.values.original * number_of_buildings / 4))
    assert isclose(sum(calculated_values), sum(tssm_test.data.original * number_of_buildings), rtol=0.00005)

    # calculate_average_scaling normal distribution up scaling manually
    values = zeros(len(tssm_test.data.original))
    idx = append(arange(len(tssm_test.data.original)), arange(len(tssm_test.data.original)))
    for i, values_original in enumerate(tssm_test.data.original):
        for j in range(i - 4 * int(sigma / 0.25 + 0.5) - 1 * 4, i + 4 * int(sigma / 0.25 + 0.5) + 2 * 4):
            values[idx[j]] += values_original * (erf((j / 4 + 0.125 - i / 4) / sqrt(2) / sigma) - erf((j / 4 - 0.125 - i / 4) / sqrt(2) / sigma)) / 2

    values = values * number_of_buildings
    assert isclose(sum(values), sum(tssm_test.data.original * number_of_buildings), rtol=0.00005)
    assert isclose(sum(calculated_values), sum(values), rtol=0.00005)
    # check if all values are nearly equal / correct
    assert allclose(values, calculated_values)


def test_normal_distribution_with_flex_time_step_and_given_sigma():
    """
    test the normal distribution calculation approach for a flexible time step year with a given variance
    """
    # set values
    sigma: List[float] = [0.23, 1, 5]
    simultaneity_factor = [1] * len(sigma)
    # check correct calculation for every entry
    for s_f, sig in zip(simultaneity_factor, sigma):
        check_normal_distribution_with_flex_time_step(s_f, sig, True)


def test_normal_distribution_with_flex_time_step():
    """
    test the normal distribution calculation approach for a flexible time step year with a variance determination
    """
    # set values
    sigma: List[float] = [0.6177145004272457]
    simultaneity_factor = [0.9843]
    # check correct calculation for every entry
    for s_f, sig in zip(simultaneity_factor, sigma):
        check_normal_distribution_with_flex_time_step(s_f, sig)


def check_normal_distribution_with_flex_time_step(simultaneity_factor: float, sigma: float, sigma_given: bool = False):
    """
    checks if the normal distribution approach for flexible time step data works correctly for the provided inputs.\n
    :param simultaneity_factor: simultaneity factor
    :param sigma: variance
    :param sigma_given: True if the variance should be considered as given
    """
    number_of_buildings = 701
    # init class and calculate_average_scaling normal distribution up scaling
    tssm_test = tssm(number_of_buildings, simultaneity_factor)
    tssm_test.data.read_profile_from_csv_with_date(f"{FOLDER}/test_data/profiles/data_flex_time_step_short.csv", "Heating", "Date")
    calculated_values = tssm_test.calculate_using_normal_distribution(**{"sigma": sigma} if sigma_given else {})

    if not isinstance(tssm_test.data.time_step, ndarray):
        raise ValueError("time step not correct")

    if not sigma_given:
        # check if the maximal value is not exceeding the maximal value times the simultaneity factor
        print(max(calculated_values) / max(tssm_test.data.original * number_of_buildings), simultaneity_factor)
        assert isclose(max(calculated_values) / max(tssm_test.data.original * number_of_buildings), simultaneity_factor, rtol=0.00005)

    # check if the sum is equal
    # print(
    #    sum(calculated_values * tssm_test.values.time_step),
    #    sum(tssm_test.values.original * number_of_buildings * tssm_test.values.time_step),
    #    sum(tssm_test.values.original * number_of_buildings * tssm_test.values.time_step) - sum(calculated_values * tssm_test.values.time_step),
    # )
    assert isclose(
        sum(calculated_values * tssm_test.data.time_step), sum(tssm_test.data.original * number_of_buildings * tssm_test.data.time_step), rtol=0.005
    )

    # calculate_average_scaling normal distribution up scaling manually
    values = zeros(len(tssm_test.data.original))
    idx = append(arange(len(tssm_test.data.original)), arange(len(tssm_test.data.original)))

    for i in range(len(tssm_test.data.original)):
        start_index: int = i
        end_index: int = i
        while sum(tssm_test.data.time_step[idx[j]] for j in range(start_index, i)) < (5 * sigma + 1):
            start_index -= 1
        while sum(tssm_test.data.time_step[idx[j]] for j in range(i, end_index)) < (5 * sigma + 1):
            end_index += 1
        for j in range(start_index, end_index):
            if 0 <= j < len(tssm_test.data.original) - 1:
                start_date = ((tssm_test.data.date[idx[j]] - tssm_test.data.date[idx[i]]).astype(float32)) / 3600
                end_date = ((tssm_test.data.date[idx[j + 1]] - tssm_test.data.date[idx[i]]).astype(float32)) / 3600
                # determine the new values using the precalculated exponential values
                if (end_date - start_date) > 0.000_000_1:
                    values[idx[j]] += (
                        tssm_test.data.time_step[i]
                        / (end_date - start_date)
                        * tssm_test.data.original[idx[i]]
                        * (erf(end_date / (sigma * sqrt(2))) - erf(start_date / (sigma * sqrt(2))))
                        / 2
                    )
                continue
            time_1 = sum((-1 if j < i else 1) * tssm_test.data.time_step[idx[idx_i]] for idx_i in (range(j, i) if j < i else range(i, j)))
            # determine the new values using the precalculated exponential values
            if tssm_test.data.time_step[idx[j]] > 0.000_000_1:
                values[idx[j]] += (
                    tssm_test.data.time_step[i]
                    / tssm_test.data.time_step[idx[j]]
                    * tssm_test.data.original[idx[i]]
                    * (erf((time_1 + tssm_test.data.time_step[idx[j]]) / (sigma * sqrt(2))) - erf(time_1 / (sigma * sqrt(2))))
                    / 2
                )

    values = values * number_of_buildings
    assert isclose(sum(values * tssm_test.data.time_step), sum(tssm_test.data.original * number_of_buildings * tssm_test.data.time_step), rtol=0.00005)
    assert isclose(sum(calculated_values * tssm_test.data.time_step), sum(values * tssm_test.data.time_step), rtol=0.005)
    # check if all values are nearly equal / correct
    for time_1, (j, i) in enumerate(zip(calculated_values, values)):
        if not isclose(j, i):
            print(time_1, j, i, round((1 - j / i) * 100, 4))
    assert allclose(values, calculated_values, rtol=0.0005)


def test_time_step_fail():
    """
    test if _determine_start_end_range_for_flexible_time_step fails with a wrong time step.
    """
    # initialize class with a number of buildings of 202 with a simultaneity factor of 0.786
    tssm_test = tssm(202, 0.98431)
    # read profile from data.csv file and use the Electricity column
    tssm_test.data.read_profile_from_csv_with_date(f"{FOLDER}/test_data/profiles/data_flex_time_step_short.csv", "Heating", "Date")

    ndc = CalculationUsingNormalDistribution(tssm_test.data, SimultaneityFactor(0.95), 4)

    ndc.data.time_step = 0
    with raises(NoNumpyArrayError):
        ndc.calculate_array_flexible_time_steps(range(8760), 1.54)  # pylint: disable=W0212
    with raises(NoNumpyArrayError):
        ndc._determine_start_end_range_for_flexible_time_step(5, 1.54)  # pylint: disable=W0212


def test_no_profile_selected_normal_distribution():
    """test that an error is raised if no profile is selected"""
    df_test = tssm(202, 0.98431)
    with raises(ValueError):
        df_test.calculate_using_normal_distribution()
