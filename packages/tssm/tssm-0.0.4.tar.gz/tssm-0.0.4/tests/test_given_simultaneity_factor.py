"""
test the linear approach and scaling profile approach with a provided scaling factor.
"""

from os.path import dirname, realpath

import numpy as np
from pytest import raises

from tssm import TimeSeriesScalingModule as tssm
from tssm import Period
from tssm.utils import calculate_indexes

FOLDER = dirname(realpath(__file__))


def test_given_simultaneity_factor_linear() -> None:
    """
    test the linear approach with a provided scaling factor for a 8760 hours year.
    """
    tssm_test = tssm(4)
    tssm_test.data.read_profile_from_csv_with_date(f"{FOLDER}/test_data/profiles/data.csv", "Heating", "Date")
    linked_dict: dict = {Period.DAILY: 365, Period.WEEKLY: 53, Period.MONTHLY: 12, Period.YEARLY: 1, Period.HOURLY: 24, Period.HOURLY_AND_MONTHLY: 24 * 12}
    for idx in Period:
        scaling_factor = list(np.arange(0.1, 0.9, 0.8 / linked_dict[idx]))
        tssm_test.calculate_using_average_values(idx, scaling_factor=scaling_factor)
        indexes_calculated = calculate_indexes(idx, tssm_test.data.date)
        # check maximal value
        values = tssm_test.data.original
        scaling_factor_long = np.zeros(len(tssm_test.data.original), dtype=np.float64)
        average = np.zeros(len(tssm_test.data.original), dtype=np.float64)
        for indexes, avg in zip(indexes_calculated, tssm_test.data.reference):
            average[indexes] = avg
        for indexes, s_f in zip(indexes_calculated, scaling_factor):
            scaling_factor_long[indexes] = s_f
        for time_idx, (s_f, avg) in enumerate(zip(scaling_factor_long, average)):
            values[time_idx] = values[time_idx] * s_f + (1 - s_f) * avg

        assert np.allclose(values * 4, tssm_test.data.new)


def test_given_simultaneity_factor_linear_15_min() -> None:
    """
    test the linear approach with a provided scaling factor for a 15-min hour year.
    """
    tssm_test = tssm(4)
    tssm_test.data.read_profile_from_csv_with_date(f"{FOLDER}/test_data/profiles/data_profiles_15_min.csv", "profile_0", "Date", date_format="%Y-%m-%d %H:%M")
    linked_dict: dict = {Period.DAILY: 366, Period.WEEKLY: 53, Period.MONTHLY: 12, Period.YEARLY: 1, Period.HOURLY: 24, Period.HOURLY_AND_MONTHLY: 24 * 12}
    for idx in Period:
        scaling_factor = list(np.arange(0.1, 0.9, 0.8 / linked_dict[idx]))
        tssm_test.calculate_using_average_values(idx, scaling_factor=scaling_factor)
        indexes_calculated = calculate_indexes(idx, tssm_test.data.date)
        # check maximal value
        values = tssm_test.data.original
        scaling_factor_long = np.zeros(len(tssm_test.data.original), dtype=np.float64)
        average = np.zeros(len(tssm_test.data.original), dtype=np.float64)
        for indexes, avg in zip(indexes_calculated, tssm_test.data.reference):
            average[indexes] = avg
        for indexes, s_f in zip(indexes_calculated, scaling_factor):
            scaling_factor_long[indexes] = s_f
        for time_idx, (s_f, avg) in enumerate(zip(scaling_factor_long, average)):
            values[time_idx] = values[time_idx] * s_f + (1 - s_f) * avg

        assert np.allclose(values * 4, tssm_test.data.new)


def test_given_simultaneity_factor_linear_flex_time_step() -> None:
    """
    test the linear approach with a provided scaling factor for a flexible time step year.
    """
    tssm_test = tssm(4)
    tssm_test.data.read_profile_from_csv_with_date(f"{FOLDER}/test_data/profiles/data_flex_time_step.csv", "Heating", "Date")
    linked_dict: dict = {Period.DAILY: 365, Period.WEEKLY: 53, Period.MONTHLY: 12, Period.YEARLY: 1, Period.HOURLY: 24, Period.HOURLY_AND_MONTHLY: 24 * 12}
    for idx in Period:
        scaling_factor = list(np.arange(0.1, 0.9, 0.8 / linked_dict[idx]))
        tssm_test.calculate_using_average_values(idx, scaling_factor=scaling_factor)
        indexes_calculated = calculate_indexes(idx, tssm_test.data.date)
        # check maximal value
        values = tssm_test.data.original
        scaling_factor_long = np.zeros(len(tssm_test.data.original), dtype=np.float64)
        average = np.zeros(len(tssm_test.data.original), dtype=np.float64)
        for indexes, avg in zip(indexes_calculated, tssm_test.data.reference):
            average[indexes] = avg
        for indexes, s_f in zip(indexes_calculated, scaling_factor):
            scaling_factor_long[indexes] = s_f
        for time_idx, (s_f, avg) in enumerate(zip(scaling_factor_long, average)):
            values[time_idx] = values[time_idx] * s_f + (1 - s_f) * avg

        assert np.allclose(values * 4, tssm_test.data.new)


def test_given_simultaneity_factor_scaling_profile() -> None:
    """
    test the scaling profile approach with a provided scaling factor for a 8760 hours year.
    """
    tssm_test = tssm(4)
    tssm_test.data.read_profile_from_csv_with_date(f"{FOLDER}/test_data/profiles/data.csv", "Heating", "Date")
    tssm_test.data.read_scaling_profile_from_csv(f"{FOLDER}/test_data/Profile_1h_scaling.csv", "H0")
    linked_dict: dict = {Period.DAILY: 365, Period.WEEKLY: 53, Period.MONTHLY: 12, Period.YEARLY: 1, Period.HOURLY: 24, Period.HOURLY_AND_MONTHLY: 24 * 12}
    for idx in Period:
        scaling_factor = list(np.arange(0.1, 0.9, 0.8 / linked_dict[idx]))
        tssm_test.calculate_using_scaling_profile(idx, scaling_factor=scaling_factor)
        indexes_calculated = calculate_indexes(idx, tssm_test.data.date)
        # check maximal value
        values = tssm_test.data.original
        scaling_factor_long = np.zeros(len(tssm_test.data.original), dtype=np.float64)
        for indexes, s_f in zip(indexes_calculated, scaling_factor):
            scaling_factor_long[indexes] = s_f
        for time_idx, (s_f, s_p) in enumerate(zip(scaling_factor_long, tssm_test.data.scaling)):
            values[time_idx] = values[time_idx] * s_f + (1 - s_f) * s_p
        assert np.allclose(values * 4, tssm_test.data.new)


def test_given_simultaneity_factor_scaling_profile_15_min() -> None:
    """
    test the scaling profile approach with a provided scaling factor for a 15-min hour year.
    """
    tssm_test = tssm(4)
    tssm_test.data.read_profile_from_csv_with_date(f"{FOLDER}/test_data/profiles/data_profiles_15_min.csv", "profile_0", "Date", date_format="%Y-%m-%d %H:%M")
    tssm_test.data.read_scaling_profile_from_csv(f"{FOLDER}/test_data/profiles/data_profiles_15_min.csv", "G0")
    linked_dict: dict = {Period.DAILY: 366, Period.WEEKLY: 53, Period.MONTHLY: 12, Period.YEARLY: 1, Period.HOURLY: 24, Period.HOURLY_AND_MONTHLY: 24 * 12}
    for idx in Period:
        scaling_factor = list(np.arange(0.1, 0.9, 0.8 / linked_dict[idx]))
        tssm_test.calculate_using_scaling_profile(idx, scaling_factor=scaling_factor)
        indexes_calculated = calculate_indexes(idx, tssm_test.data.date)
        # check maximal value
        values = tssm_test.data.original
        scaling_factor_long = np.zeros(len(tssm_test.data.original), dtype=np.float64)
        for indexes, s_f in zip(indexes_calculated, scaling_factor):
            scaling_factor_long[indexes] = s_f
        for time_idx, (s_f, s_p) in enumerate(zip(scaling_factor_long, tssm_test.data.scaling)):
            values[time_idx] = values[time_idx] * s_f + (1 - s_f) * s_p
        assert np.allclose(values * 4, tssm_test.data.new)


def test_given_simultaneity_factor_scaling_profile_flex_time_step() -> None:
    """
    test the scaling profile approach with a provided scaling factor for a flexible time step year.
    """
    tssm_test = tssm(4)
    tssm_test.data.read_profile_from_csv_with_date(f"{FOLDER}/test_data/profiles/data_flex_time_step.csv", "Heating", "Date")
    tssm_test.data.read_scaling_profile_from_csv(f"{FOLDER}/test_data/profiles/data_flex_time_step.csv", "Cooling")
    linked_dict: dict = {Period.DAILY: 365, Period.WEEKLY: 53, Period.MONTHLY: 12, Period.YEARLY: 1, Period.HOURLY: 24, Period.HOURLY_AND_MONTHLY: 24 * 12}
    for idx in Period:
        scaling_factor = list(np.arange(0.1, 0.9, 0.8 / linked_dict[idx]))
        tssm_test.calculate_using_scaling_profile(idx, scaling_factor=scaling_factor)
        indexes_calculated = calculate_indexes(idx, tssm_test.data.date)
        # check maximal value
        values = tssm_test.data.original
        scaling_factor_long = np.zeros(len(tssm_test.data.original), dtype=np.float64)
        for indexes, s_f in zip(indexes_calculated, scaling_factor):
            scaling_factor_long[indexes] = s_f
        for time_idx, (s_f, s_p) in enumerate(zip(scaling_factor_long, tssm_test.data.scaling)):
            values[time_idx] = values[time_idx] * s_f + (1 - s_f) * s_p
        assert np.allclose(values * 4, tssm_test.data.new)


def test_to_long_given_simultaneity_factor() -> None:
    """
    test if an error is raised if the provided scaling factor list/array is too long
    """
    tssm_test = tssm(4)
    tssm_test.data.read_profile_from_csv_with_date(f"{FOLDER}/test_data/profiles/data.csv", "Heating", "Date")
    tssm_test.data.read_scaling_profile_from_csv(f"{FOLDER}/test_data/Profile_1h_scaling.csv", "H0")
    scaling_factor = [0.95] * 14
    with raises(ValueError):
        tssm_test.calculate_using_average_values(Period.MONTHLY, scaling_factor=scaling_factor)
    with raises(ValueError):
        tssm_test.calculate_using_scaling_profile(Period.MONTHLY, scaling_factor=scaling_factor)


def test_to_short_given_simultaneity_factor() -> None:
    """
    test if an error is raised if the provided scaling factor list/array is too short
    """
    tssm_test = tssm(4)
    tssm_test.data.read_profile_from_csv_with_date(f"{FOLDER}/test_data/profiles/data.csv", "Heating", "Date")
    tssm_test.data.read_scaling_profile_from_csv(f"{FOLDER}/test_data/Profile_1h_scaling.csv", "H0")
    scaling_factor = [0.95] * 10
    with raises(ValueError):
        tssm_test.calculate_using_average_values(Period.MONTHLY, scaling_factor=scaling_factor)
    with raises(ValueError):
        tssm_test.calculate_using_scaling_profile(Period.MONTHLY, scaling_factor=scaling_factor)
