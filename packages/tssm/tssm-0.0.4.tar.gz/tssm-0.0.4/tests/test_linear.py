"""
test the linear scaling approach
"""

from os.path import dirname, realpath
from typing import List, Tuple, Union

import numpy as np
from pandas import DataFrame, read_csv
from pytest import raises

from tssm import Period
from tssm.utils import cast_input_2_period
from tssm import TimeSeriesScalingModule as tssm

FOLDER = dirname(realpath(__file__))


def test_linear() -> None:
    """
    test the linear approach for a 8760 hours year.
    """
    df_test = tssm(4, 0.95)
    df_test.data.read_profile_from_csv_with_date(f"{FOLDER}/test_data/profiles/data.csv", "Heating", "Date")
    validation_df: DataFrame = read_csv(f"{FOLDER}/test_data/validation.csv")
    link_dict: dict = {
        Period.YEARLY: "year",
        Period.MONTHLY: "month",
        Period.WEEKLY: "week",
        Period.DAILY: "day",
        Period.HOURLY: "hour",
        Period.HOURLY_AND_MONTHLY: "hour_month",
    }
    for i in Period:
        df_test.calculate_using_average_values(i)
        # check maximal value
        assert np.isclose(max(df_test.data.new), max(df_test.data.original) * df_test.simultaneity_factor.old * df_test.number_of_buildings)
        # check total sum
        assert np.isclose(sum(df_test.data.new), sum(df_test.data.original) * df_test.number_of_buildings)
        # determine column name
        column = f"profile_{link_dict[i]}"
        for time_idx, (j, k) in enumerate(zip(df_test.data.new, validation_df[column])):
            if not np.isclose(j, k):
                print(time_idx, j, k, i, df_test.data.date[time_idx])
        # check values
        assert np.allclose(df_test.data.new, validation_df[column])


def test_linear_property() -> None:
    """
    test the linear approach for a 8760 hours year.
    """
    df_test = tssm(4, 0.95)
    df_test.data.read_profile_from_csv_with_date(f"{FOLDER}/test_data/profiles/data.csv", "Heating", "Date")
    for i in Period:
        calculated_values_up = df_test.calculate_using_average_values(i)

        df_test_down = tssm(4, 0.95, one_2_many=False)
        df_test_down.data.set_profile_from_numpy_array(calculated_values_up)
        df_test_down.data.date = df_test.data.date
        calculated_values_down = df_test_down.calculate_using_average_values(i, scaling_factor=df_test.simultaneity_factor.new)
        # determine column name
        for time_idx, (j, k) in enumerate(zip(df_test.data.original, calculated_values_down)):
            if not np.isclose(j, k):
                print(time_idx, j, k, i, df_test.data.date[time_idx])
        # check values
        assert np.allclose(df_test.data.original, calculated_values_down)

        df_test_down = tssm(4, 0.95, one_2_many=False)
        df_test_down.data.set_profile_from_numpy_array(calculated_values_up)
        df_test_down.data.date = df_test.data.date
        calculated_values_down = df_test_down.calculate_using_average_values(i)
        # determine column name
        for time_idx, (j, k) in enumerate(zip(df_test.data.original, calculated_values_down)):
            if not np.isclose(j, k):
                print(time_idx, j, k, i, df_test.data.date[time_idx])
        # check values
        assert np.allclose(df_test.data.original, calculated_values_down)


def test_linear_with_15_min_time_step():
    """
    test the linear approach for a 15-min hour year.
    """
    validation_results = read_csv(f"{FOLDER}/test_data/Validation_15_minutes.csv")
    link_dict: dict = {
        Period.YEARLY: "year",
        Period.MONTHLY: "month",
        Period.WEEKLY: "week",
        Period.DAILY: "day",
        Period.HOURLY: "hourly",
        Period.HOURLY_AND_MONTHLY: "hourly_monthly",
    }
    for profile, simultaneity_factor in zip(["profile_0", "profile_1", "profile_2", "profile_3"], [0.881, 0.9234, 0.8943, 0.8701]):
        for idx in Period:
            # initialize class with a number of buildings of 202 with a simultaneity factor of 0.786
            df_test = tssm(202, simultaneity_factor)
            # read profile from data.csv file and use the Electricity column
            df_test.data.read_profile_from_csv_with_date(f"{FOLDER}/test_data/profiles/data_profiles_15_min.csv", profile, "Date", date_format="%Y-%m-%d %H:%M")
            # calculate linear scaled values with a daily simultaneity factor and average value
            calculated_values = df_test.calculate_using_average_values(idx)

            column = f"{profile}_{link_dict[idx]}"

            assert np.isclose(sum(df_test.data.original) * 202, sum(calculated_values))

            assert np.isclose(max(df_test.data.original * 202 * simultaneity_factor), max(calculated_values))

            for time_idx, (j, k) in enumerate(zip(calculated_values / 202, validation_results[column])):
                if not np.isclose(j, k):
                    print(time_idx, j, k, idx, df_test.data.date[time_idx], profile)
            print(len(calculated_values), len(validation_results[column]), idx, profile)
            assert np.allclose(calculated_values, validation_results[column] * 202)


def test_linear_with_15_min_time_step_property() -> None:
    """
    test the linear approach for a 8760 hours year.
    """
    for profile, simultaneity_factor in zip(["profile_0", "profile_1", "profile_2", "profile_3"], [0.881, 0.9234, 0.8943, 0.8701]):
        for idx in Period:
            # initialize class with a number of buildings of 202 with a simultaneity factor of 0.786
            df_test = tssm(202, simultaneity_factor)
            # read profile from data.csv file and use the Electricity column
            df_test.data.read_profile_from_csv_with_date(f"{FOLDER}/test_data/profiles/data_profiles_15_min.csv", profile, "Date", date_format="%Y-%m-%d %H:%M")
            # calculate linear scaled values with a daily simultaneity factor and average value
            calculated_values_up = df_test.calculate_using_average_values(idx)

            df_test_down = tssm(202, simultaneity_factor, one_2_many=False)
            df_test_down.data.set_profile_from_numpy_array(calculated_values_up)
            df_test_down.data.date = df_test.data.date
            calculated_values_down = df_test_down.calculate_using_average_values(idx, scaling_factor=df_test.simultaneity_factor.new)
            # determine column name
            for time_idx, (j, k) in enumerate(zip(df_test.data.original, calculated_values_down)):
                if not np.isclose(j, k):
                    print(time_idx, j, k, idx, df_test.data.date[time_idx])
            # check values
            assert np.allclose(df_test.data.original, calculated_values_down)

            df_test_down = tssm(202, simultaneity_factor, one_2_many=False)
            df_test_down.data.set_profile_from_numpy_array(calculated_values_up)
            df_test_down.data.date = df_test.data.date
            calculated_values_down = df_test_down.calculate_using_average_values(idx)
            # determine column name
            for time_idx, (j, k) in enumerate(zip(df_test.data.original, calculated_values_down)):
                if not np.isclose(j, k):
                    print(time_idx, j, k, idx, df_test.data.date[time_idx])
            # check values
            assert np.allclose(df_test.data.original, calculated_values_down)


def test_linear_with_flexible_time_step():
    """
    test the linear approach for a flexible time step year.
    """
    validation_results = read_csv(f"{FOLDER}/test_data/validation_linear_flex.csv")
    link_dict: dict = {
        Period.YEARLY: "year",
        Period.MONTHLY: "month",
        Period.WEEKLY: "week",
        Period.DAILY: "day",
        Period.HOURLY: "hour",
        Period.HOURLY_AND_MONTHLY: "hour_month",
    }
    for profile, simultaneity_factor in zip(["Heating", "Cooling"], [0.9514, 0.9638]):
        for idx in Period:
            # initialize class with a number of buildings of 202 with a simultaneity factor of 0.786
            df_test = tssm(202, simultaneity_factor)
            # read profile from data.csv file and use the Electricity column
            df_test.data.read_profile_from_csv_with_date(f"{FOLDER}/test_data/profiles/data_flex_time_step.csv", profile, "Date")
            # calculate linear scaled values with a daily simultaneity factor and average value
            calculated_values = df_test.calculate_using_average_values(idx)

            assert np.isclose(sum(df_test.data.original) * 202, sum(calculated_values))

            assert np.isclose(max(df_test.data.original * 202 * simultaneity_factor), max(calculated_values))

            column = f"{profile}_{link_dict[idx]}"

            for time_idx, (j, k) in enumerate(zip(calculated_values / 202, validation_results[column])):
                if not np.isclose(j, k):
                    print(time_idx, j, k, idx, df_test.data.date[time_idx], profile)

            assert np.allclose(calculated_values, validation_results[column] * 202)


def test_linear_with_flexible_time_step_property():
    """
    test the linear approach for a flexible time step year.
    """
    for profile, simultaneity_factor in zip(["Heating", "Cooling"], [0.9514, 0.9638]):
        for idx in Period:
            # initialize class with a number of buildings of 202 with a simultaneity factor of 0.786
            df_test = tssm(202, simultaneity_factor)
            # read profile from data.csv file and use the Electricity column
            df_test.data.read_profile_from_csv_with_date(f"{FOLDER}/test_data/profiles/data_flex_time_step.csv", profile, "Date")
            # calculate linear scaled values with a daily simultaneity factor and average value

            calculated_values_up = df_test.calculate_using_average_values(idx)

            df_test_down = tssm(202, simultaneity_factor, one_2_many=False)
            df_test_down.data.set_profile_from_numpy_array(calculated_values_up)
            df_test_down.data.date = df_test.data.date
            calculated_values_down = df_test_down.calculate_using_average_values(idx, scaling_factor=df_test.simultaneity_factor.new)
            # determine column name
            for time_idx, (j, k) in enumerate(zip(df_test.data.original, calculated_values_down)):
                if not np.isclose(j, k):
                    print(time_idx, j, k, idx, df_test.data.date[time_idx])
            # check values
            assert np.allclose(df_test.data.original, calculated_values_down)

            df_test_down = tssm(202, simultaneity_factor, one_2_many=False)
            df_test_down.data.set_profile_from_numpy_array(calculated_values_up)
            df_test_down.data.date = df_test.data.date
            calculated_values_down = df_test_down.calculate_using_average_values(idx)
            # determine column name
            for time_idx, (j, k) in enumerate(zip(df_test.data.original, calculated_values_down)):
                if not np.isclose(j, k):
                    print(time_idx, j, k, idx, df_test.data.date[time_idx])
            # check values
            assert np.allclose(df_test.data.original, calculated_values_down)


def test_other_period_names():
    values: List[Tuple[Period, Union[Period, str, int]]] = [
        (Period.YEARLY, Period.YEARLY),
        (Period.YEARLY, "YEARLY"),
        (Period.YEARLY, "YEARyl"),
        (Period.YEARLY, 1),
        (Period.MONTHLY, Period.MONTHLY),
        (Period.MONTHLY, "monthly"),
        (Period.MONTHLY, "monhtly"),
        (Period.MONTHLY, 2),
        (Period.WEEKLY, Period.WEEKLY),
        (Period.WEEKLY, "WEEKLY"),
        (Period.WEEKLY, "WEKLY"),
        (Period.WEEKLY, 3),
        (Period.DAILY, Period.DAILY),
        (Period.DAILY, "daily"),
        (Period.DAILY, "daiyl"),
        (Period.DAILY, 4),
        (Period.HOURLY, Period.HOURLY),
        (Period.HOURLY, "HOURLY"),
        (Period.HOURLY, "HuoRLY"),
        (Period.HOURLY, 5),
        (Period.HOURLY_AND_MONTHLY, Period.HOURLY_AND_MONTHLY),
        (Period.HOURLY_AND_MONTHLY, "HOURLY_AND_MONTHLY"),
        (Period.HOURLY_AND_MONTHLY, "HOURLY mONTHLY"),
        (Period.HOURLY_AND_MONTHLY, 6),
    ]
    for period, other_name in values:
        assert period is cast_input_2_period(other_name)

    wrong_values: List[Union[str, float, int]] = ["Hello WOrld", 1000, "weekly and monthly", 10.1]
    for wrong_names in wrong_values:
        with raises(ValueError):
            cast_input_2_period(wrong_names)  # type: ignore


def test_no_profile_selected():
    """test that an error is raised if no profile is selected"""
    df_test = tssm(202, 0.98431)
    with raises(ValueError):
        df_test.calculate_using_average_values(1)
