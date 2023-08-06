"""
test simultaneity factor calculation
"""

from os.path import dirname, realpath
from typing import List, Tuple

import numpy as np
from pandas import DataFrame
from pytest import raises

from tssm import Period, TimeSeriesScalingModule
from tssm.calculation_models import calculate_average_model
from tssm.utils import calculate_indexes

FOLDER = dirname(realpath(__file__))


def test_simultaneity_factor_calculation(data: Tuple[List[TimeSeriesScalingModule], DataFrame]) -> None:
    """
    test the simultaneity factor calculation for a year with 8760 hours\n
    """
    validation_df: DataFrame = data[1]
    link_dict: dict = {
        Period.YEARLY: "year",
        Period.MONTHLY: "month",
        Period.WEEKLY: "week",
        Period.DAILY: "day",
        Period.HOURLY: "hour",
        Period.HOURLY_AND_MONTHLY: "hour_month",
    }
    for tssm_test, period in zip(data[0], Period):
        column = f"gzf_{link_dict[period]}"
        new_time_series, simultaneity_fac = calculate_average_model(tssm_test.data, period, tssm_test.simultaneity_factor.old, tssm_test.number_of_buildings)
        indexes = calculate_indexes(period, tssm_test.data.date)

        validation_list = [validation_df[column][j.start] if isinstance(j, slice) else validation_df[column][j[0]] for j in indexes]
        assert np.allclose(simultaneity_fac, validation_list)


def test_wrong_simultaneity_factor():
    """
    check if a value error is raised if the simultaneity factor is too small.\n
    """
    df_test = TimeSeriesScalingModule(4, 0.1)
    df_test.data.read_profile_from_csv_with_date(f"{FOLDER}/test_data/profiles/data.csv", "Heating", "Date")
    with raises(ValueError):
        df_test.calculate_using_scaling_profile(Period.DAILY)
