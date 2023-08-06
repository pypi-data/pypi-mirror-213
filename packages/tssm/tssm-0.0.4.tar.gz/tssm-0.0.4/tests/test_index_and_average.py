"""
test for average and index calculation
"""

from os.path import dirname, realpath

import numpy as np
from pytest import raises

from tssm import Period, TimeSeriesScalingModule
from tssm.utils import calculate_indexes

FOLDER = dirname(realpath(__file__))


def test_average_false_input():
    """
    test if an error for a wrong period number (i.e. 5) is raised.\n
    """
    df_test = TimeSeriesScalingModule(4, 0.95)
    df_test.data.read_profile_from_csv_with_date(f"{FOLDER}/test_data/profiles/data.csv", "Heating", "Date")
    with raises(ValueError):
        df_test.calculate_using_average_values(-1)


def test_index():
    """
    test if the indexes for an 8760 hours year are calculated correctly.\n
    """
    df_test = TimeSeriesScalingModule(4)
    df_test.data.read_profile_from_csv_with_date(f"{FOLDER}/test_data/profiles/data.csv", "Heating", "Date")
    for period in Period:
        indexes_calculated = calculate_indexes(period, df_test.data.date)

        val = np.array(
            list(range(24, 8761, 24))
            if period is Period.DAILY
            else list(range(144, 8760, 24 * 7))
            if period is Period.WEEKLY
            else [744, 1416, 2160, 2880, 3624, 4344, 5088, 5832, 6552, 7296, 8016, 8760]
            if period is Period.MONTHLY
            else [[i + j for i in range(0, 8760, 24)] for j in range(24)]  # type: ignore
            if period is Period.HOURLY
            else [
                [i + j for i in range(m_start, m_end, 24)]  # type: ignore
                for m_start, m_end in zip(
                    [0, 744, 1416, 2160, 2880, 3624, 4344, 5088, 5832, 6552, 7296, 8016],
                    [744, 1416, 2160, 2880, 3624, 4344, 5088, 5832, 6552, 7296, 8016, 8760],
                )
                for j in range(24)
            ]
            if period is Period.HOURLY_AND_MONTHLY
            else [8760],  # type: ignore
            dtype=object,
        )
        if period == Period.WEEKLY:
            val = np.append(val, 8760)
        for correct_value, calculated_value in zip(val, indexes_calculated):
            if isinstance(calculated_value, slice):
                assert correct_value == calculated_value.stop
                continue
            if isinstance(calculated_value, np.ndarray):
                assert np.all(calculated_value == correct_value)
                continue

        val = np.array(
            list(range(0, 8760, 24))
            if period is Period.DAILY
            else list(range(144, 8760, 24 * 7))
            if period is Period.WEEKLY
            else [0, 744, 1416, 2160, 2880, 3624, 4344, 5088, 5832, 6552, 7296, 8016]
            if period is Period.MONTHLY
            else [0],
            dtype=np.uint64,
        )
        if period == Period.WEEKLY:
            val = np.insert(val, 0, 0)
        for correct_value, calculated_value in zip(val, indexes_calculated):
            if isinstance(calculated_value, slice):
                assert correct_value == calculated_value.start


def test_index_15_min():
    """
    test if the indexes for an 15-min hour year are calculated correctly.\n
    """
    df_test = TimeSeriesScalingModule(4)
    df_test.data.read_profile_from_csv_with_date(f"{FOLDER}/test_data/profiles/data_profiles_15_min.csv", "profile_0", "Date", date_format="%Y-%m-%d %H:%M")
    for period in Period:
        indexes_calculated = calculate_indexes(period, df_test.data.date)

        val = np.array(
            list(range(24, 8785, 24))
            if period is Period.DAILY
            else list(range(48, 8760, 24 * 7))
            if period is Period.WEEKLY
            else [744, 1440, 2184, 2904, 3648, 4368, 5112, 5856, 6576, 7320, 8040, 8784]
            if period is Period.MONTHLY
            else [[i + k + j * 4 for i in range(0, 8784 * 4, 24 * 4) for k in range(4)] for j in range(24)]  # type: ignore
            if period is Period.HOURLY
            else [
                [i + k + j * 4 for i in range(m_start * 4, m_end * 4, 24 * 4) for k in range(4)]  # type: ignore
                for m_start, m_end in zip(
                    [0, 744, 1440, 2184, 2904, 3648, 4368, 5112, 5856, 6576, 7320, 8040],
                    [744, 1440, 2184, 2904, 3648, 4368, 5112, 5856, 6576, 7320, 8040, 8784],
                )
                for j in range(24)
            ]
            if period is Period.HOURLY_AND_MONTHLY
            else [8784],  # type: ignore
            dtype=object,
        ) * (4 if period in [Period.DAILY, Period.MONTHLY, Period.WEEKLY, Period.YEARLY] else 1)
        if period == 2:
            val = np.append(val, 8784 * 4)
        for correct_value, calculated_value in zip(val, indexes_calculated):
            if isinstance(calculated_value, slice):
                assert correct_value == calculated_value.stop
                continue
            if isinstance(calculated_value, np.ndarray):
                assert np.all(calculated_value == correct_value)
                continue

        val = (
            np.array(
                list(range(0, 8784, 24))
                if period == 1
                else list(range(48, 8760, 24 * 7))
                if period == 2
                else [0, 744, 1440, 2184, 2904, 3648, 4368, 5112, 5856, 6576, 7320, 8040]
                if period == 3
                else [0],
                dtype=np.uint64,
            )
            * 4
        )
        if period == 2:
            val = np.insert(val, 0, 0)
        for correct_value, calculated_value in zip(val, indexes_calculated):
            if isinstance(calculated_value, slice):
                assert correct_value == calculated_value.start
