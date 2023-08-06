"""
test the normal distribution calculation approach
"""

from math import erf, sqrt
from os.path import dirname, realpath

import numpy as np
from numpy import allclose, append, arange, zeros
from pytest import raises

from tssm import TimeSeriesScalingModule as tssm

FOLDER = dirname(realpath(__file__))


def test_scaling_normal_distribution():
    for i in [0.6, 0.7, 0.8, 0.9]:
        check_scaling_normal_distribution(i)


def check_scaling_normal_distribution(simultaneity_factor: float):
    number_of_buildings = 4
    scaling_module = tssm(number_of_buildings, simultaneity_factor)
    scaling_module.data.read_profile_from_csv_with_date(f"{FOLDER}/test_data/profiles/data.csv", "Heating", "Date")
    scaling_module.data.read_scaling_profile_from_csv(f"{FOLDER}/test_data/Profile_1h_scaling.csv", "H0")
    calculated_values = scaling_module.calculate_using_scaling_and_normal_distribution()
    assert np.isclose(scaling_module.data.original.max(initial=0) * simultaneity_factor * number_of_buildings, calculated_values.max(initial=0))

    assert np.isclose(scaling_module.data.original.sum() * number_of_buildings, calculated_values.sum())

    sigma = scaling_module.simultaneity_factor.new[0]

    # calculate_average_scaling normal distribution up scaling manually
    values = zeros(len(scaling_module.data.original))
    idx = append(arange(len(scaling_module.data.original)), arange(len(scaling_module.data.original)))
    for i, (values_original, ref) in enumerate(zip(scaling_module.data.original - scaling_module.data.reference, scaling_module.data.reference)):
        values[idx[i]] += ref
        for j in range(i - 4 * int(sigma + 0.5) - 1, i + 4 * int(sigma + 0.5) + 2):
            values[idx[j]] += values_original * (erf((j + 0.5 - i) / sqrt(2) / sigma) - erf((j - 0.5 - i) / sqrt(2) / sigma)) / 2

    values = values * number_of_buildings
    # check if all values are nearly equal / correct
    assert allclose(values, calculated_values)

    new_calculated_values = scaling_module.calculate_using_scaling_and_normal_distribution(sigma=sigma)

    assert np.allclose(new_calculated_values, calculated_values)

    scaling_module_down = tssm(number_of_buildings, simultaneity_factor, one_2_many=False)
    scaling_module_down.data.read_profile_from_csv_with_date(f"{FOLDER}/test_data/profiles/data.csv", "Heating", "Date")
    scaling_module_down.data.read_scaling_profile_from_csv(f"{FOLDER}/test_data/Profile_1h_scaling.csv", "H0")
    scaling_module_down.data.set_profile_from_numpy_array(calculated_values)
    calculated_values_down = scaling_module_down.calculate_using_scaling_and_normal_distribution(sigma=sigma)

    np.allclose(calculated_values_down, scaling_module.data.original)

    calculated_values_down = scaling_module_down.calculate_using_scaling_and_normal_distribution()

    np.allclose(calculated_values_down, scaling_module.data.original)


def test_no_profile_selected_scaling_normal_distribution():
    """test that an error is raised if no profiles are selected"""
    df_test = tssm(202, 0.98431)
    with raises(ValueError):
        df_test.calculate_using_scaling_and_normal_distribution()
    # read profile from data.csv file and use the Electricity column
    df_test.data.read_profile_from_csv_with_date(f"{FOLDER}/test_data/profiles/data_flex_time_step.csv", "Heating", "Date")
    with raises(ValueError):
        df_test.calculate_using_scaling_and_normal_distribution()


def test_scaling_normal_distribution_fail_maximal_variance():
    """
    test if the normal distribution calculation fails due to a too small simultaneity factor
    """
    with raises(ValueError):
        check_scaling_normal_distribution(0.001)


def test_scaling_normal_distribution_fail_minimal_variance():
    """
    test if the normal distribution calculation fails due to a too high simultaneity factor
    """
    with raises(ValueError):
        check_scaling_normal_distribution(1.01)
