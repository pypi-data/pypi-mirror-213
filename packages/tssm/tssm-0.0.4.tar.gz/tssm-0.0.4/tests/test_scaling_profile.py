"""
test the scaling profile approach and its same sum function
"""

from os.path import dirname, realpath

import numpy as np
from pandas import DataFrame, read_csv
from pytest import raises

from tssm import Period
from tssm import TimeSeriesScalingModule as tssm
from tssm.utils import calculate_indexes

FOLDER = dirname(realpath(__file__))


def test_scaling_profile() -> None:
    """
    test scaling profile calculation using a 8760 hours year.
    """
    df_test = tssm(12, 0.96234)
    df_test.data.read_profile_from_csv_with_date(f"{FOLDER}/test_data/profiles/data.csv", "Electricity", "Date")
    df_test.data.read_scaling_profile_from_csv(f"{FOLDER}/test_data/Profile_1h_scaling.csv", "H0")
    validation_df: DataFrame = read_csv(f"{FOLDER}/test_data/Validation_scaled_1.csv")
    linked_dict: dict = {
        Period.YEARLY: "year",
        Period.MONTHLY: "month",
        Period.WEEKLY: "weekly",
        Period.DAILY: "daily",
        Period.HOURLY: "hourly",
        Period.HOURLY_AND_MONTHLY: "hourly_monthly",
    }
    for idx in Period:
        calculated_values = df_test.calculate_using_scaling_profile(idx)
        head = f"{linked_dict[idx]}_normal"
        validation = validation_df[head].to_numpy() * 12
        indexes = calculate_indexes(idx, df_test.data.date)
        for index in indexes:
            assert np.isclose(max(df_test.data.original[index] * 12 * 0.96234), max(calculated_values[index]))
        for time_idx, (j, k) in enumerate(zip(df_test.data.new, validation)):
            if not np.isclose(j, k):
                print(time_idx, j, k)
        assert np.allclose(df_test.data.new, validation)


def test_scaling_profile_property() -> None:
    """
    test scaling profile calculation using a 8760 hours year.
    """
    df_test = tssm(202, 0.96234)
    df_test.data.read_profile_from_csv_with_date(f"{FOLDER}/test_data/profiles/data.csv", "Electricity", "Date")
    df_test.data.read_scaling_profile_from_csv(f"{FOLDER}/test_data/Profile_1h_scaling.csv", "H0")
    for idx in Period:
        calculated_values_up = df_test.calculate_using_scaling_profile(idx, same_sum=False)

        df_test_down = tssm(202, 0.96234, one_2_many=False)
        df_test_down.data.set_profile_from_numpy_array(calculated_values_up)
        df_test_down.data.date = df_test.data.date
        df_test_down.data.read_scaling_profile_from_csv(f"{FOLDER}/test_data/Profile_1h_scaling.csv", "H0")
        calculated_values_down = df_test_down.calculate_using_scaling_profile(idx, scaling_factor=df_test.simultaneity_factor.new, same_sum=False)
        # determine column name
        for time_idx, (j, k) in enumerate(zip(df_test.data.original, calculated_values_down)):
            if not np.isclose(j, k):
                print(time_idx, j, k, idx, df_test.data.date[time_idx])
        # check values
        assert np.allclose(df_test.data.original, calculated_values_down)

        df_test_down = tssm(202, 0.96234, one_2_many=False)
        df_test_down.data.set_profile_from_numpy_array(calculated_values_up)
        df_test_down.data.date = df_test.data.date
        df_test_down.data.read_scaling_profile_from_csv(f"{FOLDER}/test_data/Profile_1h_scaling.csv", "H0")
        calculated_values_down = df_test_down.calculate_using_scaling_profile(idx, same_sum=False)

        assert np.isclose(max(calculated_values_up) / 202 / 0.96234, max(calculated_values_down))

        assert np.isclose(max(df_test.data.original), max(calculated_values_down))

        # determine column name
        for time_idx, (j, k) in enumerate(zip(df_test.data.original, calculated_values_down)):
            if not np.isclose(j, k):
                print(time_idx, j, k, idx, df_test.data.date[time_idx])
        # check values
        assert np.allclose(df_test.data.original, calculated_values_down)


def test_scaling_profile_same_sum_property() -> None:
    """
    test scaling profile calculation using a 8760 hours year.
    """
    df_test = tssm(202, 0.96234)
    df_test.data.read_profile_from_csv_with_date(f"{FOLDER}/test_data/profiles/data.csv", "Electricity", "Date")
    df_test.data.read_scaling_profile_from_csv(f"{FOLDER}/test_data/Profile_1h_scaling.csv", "H0")
    for idx in [Period.WEEKLY, Period.MONTHLY, Period.YEARLY]:
        calculated_values_up = df_test.calculate_using_scaling_profile(idx, same_sum=True)

        df_test_down = tssm(202, 0.96234, one_2_many=False)
        df_test_down.data.set_profile_from_numpy_array(calculated_values_up)
        df_test_down.data.date = df_test.data.date
        df_test_down.data.read_scaling_profile_from_csv(f"{FOLDER}/test_data/Profile_1h_scaling.csv", "H0")
        calculated_values_down = df_test_down.calculate_using_scaling_profile(idx, scaling_factor=df_test.simultaneity_factor.new, same_sum=True)
        # determine column name
        for time_idx, (j, k) in enumerate(zip(df_test.data.original, calculated_values_down)):
            if not np.isclose(j, k):
                print(time_idx, j, k, idx, df_test.data.date[time_idx])
        # check values
        assert np.allclose(df_test.data.original, calculated_values_down)

        df_test_down = tssm(202, 0.96234, one_2_many=False)
        df_test_down.data.set_profile_from_numpy_array(calculated_values_up)
        df_test_down.data.date = df_test.data.date
        df_test_down.data.read_scaling_profile_from_csv(f"{FOLDER}/test_data/Profile_1h_scaling.csv", "H0")
        calculated_values_down = df_test_down.calculate_using_scaling_profile(idx, same_sum=True)

        assert np.isclose(max(calculated_values_up) / 202 / 0.96234, max(calculated_values_down))
        assert np.isclose(max(df_test.data.original), max(calculated_values_down))

        # determine column name
        for time_idx, (j, k) in enumerate(zip(df_test.data.original, calculated_values_down)):
            if not np.isclose(j, k):
                print(time_idx, j, k, idx, df_test.data.date[time_idx])
        # check values
        assert np.allclose(df_test.data.original, calculated_values_down)


def test_scaling_profile_same_sum() -> None:
    """
    test scaling profile calculation using a 8760 hours year and the scaling to the same sum function.\n
    """
    df_test = tssm(13, 0.96234)
    df_test.data.read_profile_from_csv_with_date(f"{FOLDER}/test_data/profiles/data.csv", "Electricity", "Date")
    df_test.data.read_scaling_profile_from_csv(f"{FOLDER}/test_data/Profile_1h_scaling.csv", "H0")
    validation_df: DataFrame = read_csv(f"{FOLDER}/test_data/Validation_scaled_1.csv")
    linked_dict: dict = {
        Period.YEARLY: "year",
        Period.MONTHLY: "month",
        Period.WEEKLY: "weekly",
        Period.DAILY: "daily",
        Period.HOURLY: "hourly",
        Period.HOURLY_AND_MONTHLY: "hourly_monthly",
    }
    for idx in Period:
        calculated_values = df_test.calculate_using_scaling_profile(idx, same_sum=True)

        if idx not in [Period.DAILY, Period.HOURLY, Period.HOURLY_AND_MONTHLY]:
            indexes = calculate_indexes(idx, df_test.data.date)
            for index in indexes:
                assert np.isclose(max(df_test.data.original[index] * 13 * 0.96234), max(calculated_values[index]))

        indexes = calculate_indexes(idx, df_test.data.date)
        for index in indexes:
            assert np.isclose(df_test.data.reference[index].sum(), df_test.data.original[index].sum())

        column = f"H0_scaled_{linked_dict[idx]}"
        for time_idx, (j, k) in enumerate(zip(df_test.data.reference, validation_df[column])):
            if not np.isclose(j, k, atol=0.001):
                print(time_idx, j, k, idx, df_test.data.date[time_idx])

        assert np.allclose(df_test.data.reference, validation_df[column], atol=0.001)

        assert np.isclose(df_test.data.original.sum(), calculated_values.sum() / 13, atol=0.001)

        column = f"{linked_dict[idx]}_scaled"

        for time_idx, (j, k) in enumerate(zip(df_test.data.new, validation_df[column].to_numpy() * 13)):
            if not np.isclose(j, k):
                print(time_idx, j, k, idx)
        assert np.allclose(df_test.data.new, validation_df[column].to_numpy() * 13)


def test_scaling_with_15_min_time_step():
    """
    test scaling profile calculation using a 15-min hour year.
    """
    validation_results = read_csv(f"{FOLDER}/test_data/Validation_scaled_15_min.csv")
    linked_dict: dict = {
        Period.YEARLY: "year",
        Period.MONTHLY: "month",
        Period.WEEKLY: "weekly",
        Period.DAILY: "daily",
        Period.HOURLY: "hourly",
        Period.HOURLY_AND_MONTHLY: "hourly_monthly",
    }
    for idx in Period:
        # initialize class with a number of buildings of 202 with a simultaneity factor of 0.786
        df_test = tssm(202, 0.91045)
        # read profile from data.csv file and use the Electricity column
        df_test.data.read_profile_from_csv_with_date(f"{FOLDER}/test_data/profiles/data_profiles_15_min.csv", "profile_0", "Date", date_format="%Y-%m-%d %H:%M")

        df_test.data.read_scaling_profile_from_csv(f"{FOLDER}/test_data/profiles/data_profiles_15_min.csv", "G0")
        # calculate linear scaled values with a daily simultaneity factor and average value
        calculated_values = df_test.calculate_using_scaling_profile(idx)

        column = f"{linked_dict[idx]}_normal"
        indexes = calculate_indexes(Period.YEARLY, df_test.data.date)
        for index in indexes:
            assert np.isclose(max(df_test.data.original[index] * 202 * 0.91045), max(calculated_values[index]))

        for time_idx, (j, k) in enumerate(zip(calculated_values / 202, validation_results[column])):
            if not np.isclose(j, k, atol=0.001):
                print(time_idx, j, k, idx, df_test.data.date[time_idx])

        assert np.allclose(calculated_values / 202, validation_results[column], atol=0.001)


def test_scaling_with_15_min_time_step_property():
    """
    test scaling profile calculation using a 15-min hour year.
    """
    # initialize class with a number of buildings of 202 with a simultaneity factor of 0.786
    df_test = tssm(202, 0.91045)
    # read profile from data.csv file and use the Electricity column
    df_test.data.read_profile_from_csv_with_date(f"{FOLDER}/test_data/profiles/data_profiles_15_min.csv", "profile_0", "Date", date_format="%Y-%m-%d %H:%M")

    df_test.data.read_scaling_profile_from_csv(f"{FOLDER}/test_data/profiles/data_profiles_15_min.csv", "G0")
    for idx in [Period.WEEKLY, Period.MONTHLY, Period.YEARLY]:
        # calculate linear scaled values with a daily simultaneity factor and average value
        calculated_values_up = df_test.calculate_using_scaling_profile(idx)

        df_test_down = tssm(202, 0.91045, one_2_many=False)
        df_test_down.data.set_profile_from_numpy_array(calculated_values_up)
        df_test_down.data.date = df_test.data.date
        df_test_down.data.scaling = df_test.data.scaling
        calculated_values_down = df_test_down.calculate_using_scaling_profile(idx, scaling_factor=df_test.simultaneity_factor.new)
        # determine column name
        for time_idx, (j, k) in enumerate(zip(df_test.data.original, calculated_values_down)):
            if not np.isclose(j, k):
                print(time_idx, j, k, idx, df_test.data.date[time_idx])
        # check values
        assert np.allclose(df_test.data.original, calculated_values_down)

        df_test_down = tssm(202, 0.91045, one_2_many=False)
        df_test_down.data.set_profile_from_numpy_array(calculated_values_up)
        df_test_down.data.date = df_test.data.date
        df_test_down.data.scaling = df_test.data.scaling
        calculated_values_down = df_test_down.calculate_using_scaling_profile(idx)

        assert np.isclose(max(calculated_values_up) / 202 / 0.91045, max(calculated_values_down))

        assert np.isclose(max(df_test.data.original), max(calculated_values_down))

        # determine column name
        for time_idx, (j, k) in enumerate(zip(df_test.data.original, calculated_values_down)):
            if not np.isclose(j, k):
                print(time_idx, j, k, idx, df_test.data.date[time_idx])
        # check values
        assert np.allclose(df_test.data.original, calculated_values_down)


def test_scaling_with_15_min_time_step_same_sum():
    """
    test scaling profile calculation using a 15-min hour year and the scaling to the same sum function.
    """
    validation_results = read_csv(f"{FOLDER}/test_data/Validation_scaled_15_min.csv")
    # initialize class with a number of buildings of 202 with a simultaneity factor of 0.786
    df_test = tssm(202, 0.91045)
    # read profile from data.csv file and use the Electricity column
    df_test.data.read_profile_from_csv_with_date(f"{FOLDER}/test_data/profiles/data_profiles_15_min.csv", "profile_0", "Date", date_format="%Y-%m-%d %H:%M")

    df_test.data.read_scaling_profile_from_csv(f"{FOLDER}/test_data/profiles/data_profiles_15_min.csv", "G0")
    linked_dict: dict = {
        Period.YEARLY: "year",
        Period.MONTHLY: "month",
        Period.WEEKLY: "weekly",
        Period.DAILY: "daily",
        Period.HOURLY: "hourly",
        Period.HOURLY_AND_MONTHLY: "hourly_monthly",
    }
    for idx in Period:
        # calculate linear scaled values with a daily simultaneity factor and average value
        calculated_values = df_test.calculate_using_scaling_profile(idx, same_sum=True)

        indexes = calculate_indexes(idx if idx not in [Period.DAILY, Period.HOURLY_AND_MONTHLY] else Period.YEARLY, df_test.data.date)
        for index in indexes:
            assert np.isclose(max(df_test.data.original[index] * 202 * 0.91045), max(calculated_values[index]))

        indexes = calculate_indexes(idx, df_test.data.date)
        for index in indexes:
            assert np.isclose(df_test.data.reference[index].sum(), df_test.data.original[index].sum())

        column = f"G0_scaled_{linked_dict[idx]}"
        for time_idx, (j, k) in enumerate(zip(df_test.data.reference, validation_results[column])):
            if not np.isclose(j, k, atol=0.001):
                print(time_idx, j, k, idx, df_test.data.date[time_idx])

        assert np.allclose(df_test.data.reference, validation_results[column], atol=0.001)

        assert np.isclose(df_test.data.original.sum(), calculated_values.sum() / 202, atol=0.001)

        column = f"{linked_dict[idx]}_scaled"
        for time_idx, (j, k) in enumerate(zip(calculated_values / 202, validation_results[column])):
            if not np.isclose(j, k, atol=0.001):
                print(time_idx, j, k, idx, df_test.data.date[time_idx])

        assert np.allclose(calculated_values, validation_results[column] * 202, atol=0.001)


def test_scaling_with_flexible_time_step():
    """
    test scaling profile calculation using a flexible time step year.
    """
    validation_results = read_csv(f"{FOLDER}/test_data/Validation_scaled_flex.csv")
    linked_dict: dict = {
        Period.YEARLY: "year",
        Period.MONTHLY: "month",
        Period.WEEKLY: "weekly",
        Period.DAILY: "daily",
        Period.HOURLY: "hourly",
        Period.HOURLY_AND_MONTHLY: "hourly_monthly",
    }
    for idx in Period:
        # initialize class with a number of buildings of 202 with a simultaneity factor of 0.786
        df_test = tssm(202, 0.98431)
        # read profile from data.csv file and use the Electricity column
        df_test.data.read_profile_from_csv_with_date(f"{FOLDER}/test_data/profiles/data_flex_time_step.csv", "Heating", "Date")

        df_test.data.read_scaling_profile_from_csv(f"{FOLDER}/test_data/profiles/data_flex_time_step.csv", "Cooling")
        # calculate linear scaled values with a daily simultaneity factor and average value
        calculated_values = df_test.calculate_using_scaling_profile(idx)
        indexes = calculate_indexes(Period.YEARLY, df_test.data.date)
        for index in indexes:
            assert np.isclose(max(df_test.data.original[index] * 202 * 0.98431), max(calculated_values[index]))

        column = f"{linked_dict[idx]}_normal"

        for time_idx, (j, k) in enumerate(zip(calculated_values / 202, validation_results[column])):
            if not np.isclose(j, k):
                print(time_idx, j, k, idx, df_test.data.date[time_idx])

        assert np.allclose(calculated_values, validation_results[column] * 202)


def test_scaling_with_flexible_time_step_property():
    """
    test scaling profile calculation using a flexible time step year.
    """
    # initialize class with a number of buildings of 202 with a simultaneity factor of 0.786
    df_test = tssm(202, 0.98431)
    # read profile from data.csv file and use the Electricity column
    df_test.data.read_profile_from_csv_with_date(f"{FOLDER}/test_data/profiles/data_flex_time_step.csv", "Heating", "Date")

    df_test.data.read_scaling_profile_from_csv(f"{FOLDER}/test_data/profiles/data_flex_time_step.csv", "Cooling")
    for idx in [Period.MONTHLY, Period.YEARLY]:
        # calculate linear scaled values with a daily simultaneity factor and average value
        calculated_values_up = df_test.calculate_using_scaling_profile(idx)

        df_test_down = tssm(202, 0.98431, one_2_many=False)
        df_test_down.data.set_profile_from_numpy_array(calculated_values_up)
        df_test_down.data.date = df_test.data.date
        df_test_down.data.scaling = df_test.data.scaling
        calculated_values_down = df_test_down.calculate_using_scaling_profile(idx, scaling_factor=df_test.simultaneity_factor.new)
        # determine column name
        for time_idx, (j, k) in enumerate(zip(df_test.data.original, calculated_values_down)):
            if not np.isclose(j, k):
                print(time_idx, j, k, idx, df_test.data.date[time_idx])
        # check values
        assert np.allclose(df_test.data.original, calculated_values_down)

        df_test_down = tssm(202, 0.98431, one_2_many=False)
        df_test_down.data.set_profile_from_numpy_array(calculated_values_up)
        df_test_down.data.date = df_test.data.date
        df_test_down.data.scaling = df_test.data.scaling
        calculated_values_down = df_test_down.calculate_using_scaling_profile(idx)

        assert np.isclose(max(calculated_values_up) / 202 / 0.98431, max(calculated_values_down))

        assert np.isclose(max(df_test.data.original), max(calculated_values_down))

        # determine column name
        for time_idx, (j, k) in enumerate(zip(df_test.data.original, calculated_values_down)):
            if not np.isclose(j, k):
                print(time_idx, j, k, idx, df_test.data.date[time_idx])
        # check values
        assert np.allclose(df_test.data.original, calculated_values_down)


def test_scaling_with_flexible_time_step_same_sum():
    """
    test scaling profile calculation using a flexible time step year and the scaling to the same sum function.
    """
    validation_results = read_csv(f"{FOLDER}/test_data/Validation_scaled_flex.csv")
    # initialize class with a number of buildings of 202 with a simultaneity factor of 0.786
    df_test = tssm(202, 0.98431)
    # read profile from data.csv file and use the Electricity column
    df_test.data.read_profile_from_csv_with_date(f"{FOLDER}/test_data/profiles/data_flex_time_step.csv", "Heating", "Date")

    df_test.data.read_scaling_profile_from_csv(f"{FOLDER}/test_data/profiles/data_flex_time_step.csv", "Cooling")
    linked_dict: dict = {
        Period.YEARLY: "year",
        Period.MONTHLY: "month",
        Period.WEEKLY: "weekly",
        Period.DAILY: "daily",
        Period.HOURLY: "hourly",
        Period.HOURLY_AND_MONTHLY: "hourly_monthly",
    }
    for idx in Period:
        # calculate linear scaled values with a daily simultaneity factor and average value
        calculated_values = df_test.calculate_using_scaling_profile(idx, same_sum=True)
        if idx != Period.DAILY and idx != Period.WEEKLY:
            indexes = calculate_indexes(idx, df_test.data.date)
            for index in indexes:
                assert np.isclose(max(df_test.data.original[index] * 202 * 0.98431), max(calculated_values[index]))

        indexes = calculate_indexes(idx, df_test.data.date)
        for index in indexes:
            assert np.isclose(df_test.data.reference[index].sum(), df_test.data.original[index].sum())

        column = f"H0_scaled_{linked_dict[idx]}"
        for time_idx, (j, k) in enumerate(zip(df_test.data.reference, validation_results[column])):
            if not np.isclose(j, k, atol=0.001):
                print(time_idx, j, k, idx, df_test.data.date[time_idx])

        assert np.allclose(df_test.data.reference, validation_results[column], atol=0.001)
        assert np.isclose(df_test.data.original.sum(), calculated_values.sum() / 202, atol=0.001)

        column = f"{linked_dict[idx]}_scaled"

        for time_idx, (j, k) in enumerate(zip(calculated_values / 202, validation_results[column])):
            if not np.isclose(j, k):
                print(time_idx, j, k, idx, df_test.data.date[time_idx])

        assert np.allclose(calculated_values, validation_results[column] * 202, atol=0.0001)


def test_no_profile_selected_scaling_profile():
    """test that an error is raised if no profiles are selected"""
    df_test = tssm(202, 0.98431)
    with raises(ValueError):
        df_test.calculate_using_scaling_profile(Period.DAILY)
    # read profile from data.csv file and use the Electricity column
    df_test.data.read_profile_from_csv_with_date(f"{FOLDER}/test_data/profiles/data_flex_time_step.csv", "Heating", "Date")
    with raises(ValueError):
        df_test.calculate_using_scaling_profile(Period.DAILY)


def test_average_false_input():
    """
    test if an error for a wrong period number (i.e. 5) is raised.\n
    """
    df_test = tssm(4, 0.95)
    df_test.data.read_profile_from_csv_with_date(f"{FOLDER}/test_data/profiles/data.csv", "Heating", "Date")
    with raises(ValueError):
        df_test.calculate_using_scaling_profile(5)
