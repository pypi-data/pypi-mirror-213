from __future__ import annotations

import numpy as np
import pandas as pd
import datetime

from tssm.calculation_models.profile_generation.bdew_heat import create_bdew_heat_profile


def test_bdew_heat():
    holidays = [
        datetime.datetime(2010, 5, 24),
        datetime.datetime(2010, 4, 5),
        datetime.datetime(2010, 5, 13),
        datetime.datetime(2010, 1, 1),
        datetime.datetime(2010, 10, 3),
        datetime.datetime(2010, 12, 25),
        datetime.datetime(2010, 5, 1),
        datetime.datetime(2010, 4, 2),
        datetime.datetime(2010, 12, 26),
    ]

    temperature = pd.read_csv("test_data/temperature_data.csv", index_col=0)["temperature"].to_numpy()
    efh_profile = create_bdew_heat_profile(temperature, 2010, "EFH", 1, 25_000, wind_impact=True, holidays_as_sundays=holidays)

    reference = pd.read_csv("test_data/heat_demand.csv", index_col=0)

    assert np.allclose(efh_profile, reference["efh"] / reference["efh"].sum() * 25_000)

    mfh_profile = create_bdew_heat_profile(temperature, 2010, "MFH", 2, 80_000, wind_impact=False, include_domestic_hot_water=True, holidays_as_sundays=holidays)

    assert np.allclose(mfh_profile, reference["mfh"] / reference["mfh"].sum() * 80_000)

    ghd_profile = create_bdew_heat_profile(temperature, 2010, "ghd", 0, 140_000, wind_impact=False, include_domestic_hot_water=True,
                                           holidays_as_sundays=holidays)

    assert np.allclose(ghd_profile, reference["ghd"] / reference["ghd"].sum() * 140_000)
