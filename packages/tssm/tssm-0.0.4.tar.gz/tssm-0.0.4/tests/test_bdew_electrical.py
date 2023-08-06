from __future__ import annotations
import datetime

import numpy as np
import pandas as pd

from tssm.calculation_models.profile_generation.bdew_electrical import create_bdew_electrical_profile


def test_bdew_electrical_profile():
    holiday_sundays: list[datetime.datetime] = [
        datetime.datetime(1996, 1, 1),
        datetime.datetime(1996, 3, 28),
        datetime.datetime(1996, 3, 30),
        datetime.datetime(1996, 3, 31),
        datetime.datetime(1996, 5, 19),
        datetime.datetime(1996, 5, 1),
        datetime.datetime(1996, 6, 6),
        datetime.datetime(1996, 12, 25),
        datetime.datetime(1996, 12, 26),
        datetime.datetime(1996, 10, 3),
        datetime.datetime(1996, 5, 8),
        datetime.datetime(1996, 11, 1),
        datetime.datetime(1996, 5, 29),
    ]
    holiday_saturday = [datetime.datetime(1996, 3, 29), datetime.datetime(1996, 12, 24), datetime.datetime(1996, 12, 31)]
    results = create_bdew_electrical_profile("H0", 1996, holidays_as_sundays=holiday_sundays, holidays_as_saturdays=holiday_saturday)
    reference = pd.read_csv("./test_data/BDEW_Profiles.csv", sep=";", index_col=0)

    for idx, (ref, new) in enumerate(zip(reference["H0"][153 * 24 * 4:], results[154 * 24 * 4:])):
        if not np.isclose(ref, new):
            print(reference.index[154 * 24 * 4 + idx], ref, new)
    assert np.allclose(reference["H0"][153 * 24 * 4:], results[154 * 24 * 4:])

    results = create_bdew_electrical_profile("H0", 1996, holidays_as_sundays=holiday_sundays, holidays_as_saturdays=holiday_saturday, dynamic=True)
    results = results.round(1)

    for idx, (ref, new) in enumerate(zip(reference["H0_dyn"][153 * 24 * 4:], results[154 * 24 * 4:])):
        if not np.isclose(ref, new):
            print(reference.index[154 * 24 * 4 + idx], ref, new)
    assert np.allclose(reference["H0_dyn"][153 * 24 * 4:], results[154 * 24 * 4:])

    holiday_sundays = [datetime.datetime(1997, date.month, date.day) for date in holiday_sundays]
    holiday_saturday = [datetime.datetime(1997, date.month, date.day) for date in holiday_saturday]
    results = create_bdew_electrical_profile("H0", 1997, holidays_as_sundays=holiday_sundays, holidays_as_saturdays=holiday_saturday)

    for idx, (ref, new) in enumerate(zip(reference["H0"][: 151 * 24 * 4], results[: 151 * 24 * 4])):
        if not np.isclose(ref, new):
            print(reference.index[idx], ref, new)
    assert np.allclose(reference["H0"][: 151 * 24 * 4], results[: 151 * 24 * 4])

    results = create_bdew_electrical_profile("H0", 1997, holidays_as_sundays=holiday_sundays, holidays_as_saturdays=holiday_saturday, dynamic=True)
    results = results.round(1)

    for idx, (ref, new) in enumerate(zip(reference["H0_dyn"][: 151 * 24 * 4], results[: 151 * 24 * 4])):
        if not np.isclose(ref, new):
            print(reference.index[idx], ref, new)
    assert np.allclose(reference["H0_dyn"][: 151 * 24 * 4], results[: 151 * 24 * 4])
