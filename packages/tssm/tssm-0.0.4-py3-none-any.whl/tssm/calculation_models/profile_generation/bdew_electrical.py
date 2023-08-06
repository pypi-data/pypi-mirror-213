"""
classes for BDEW electrical profile generation
"""
from __future__ import annotations
import datetime
from abc import abstractmethod

import numpy as np
import pandas as pd
from numpy.typing import NDArray

from tssm.utils.BDEW_class import BDEWElectrical
from tssm.utils.seasons import Season
from tssm.utils.BDEW_day import BDEWDAY


class Seasons:
    __slots__ = "start", "end", "season"

    @abstractmethod
    def __init__(self):
        self.start: datetime.datetime = datetime.datetime(0, 0, 0)
        self.end: datetime.datetime = datetime.datetime(0, 0, 0)
        self.season: Season = Season.Winter

    def set_year(self, year: int):
        self.start = self.start.replace(year=year)
        self.end = self.end.replace(year=year)


class Summer(Seasons):
    def __init__(self):
        self.start: datetime.datetime = datetime.datetime(2000, 5, 15, 0, 0)
        self.end: datetime.datetime = datetime.datetime(2000, 9, 14, 23, 59)
        self.season: Season = Season.Summer


class Spring(Seasons):
    def __init__(self):
        self.start: datetime.datetime = datetime.datetime(2000, 3, 21, 0, 0)
        self.end: datetime.datetime = datetime.datetime(2000, 5, 14, 23, 59)
        self.season: Season = Season.Rest


class Autumn(Seasons):
    def __init__(self):
        self.start: datetime.datetime = datetime.datetime(2000, 9, 15, 0, 0)
        self.end: datetime.datetime = datetime.datetime(2000, 10, 31, 23, 59)
        self.season: Season = Season.Rest


class WinterStart(Seasons):
    def __init__(self):
        self.start: datetime.datetime = datetime.datetime(2000, 1, 1, 0, 0)
        self.end: datetime.datetime = datetime.datetime(2000, 3, 21, 23, 59)
        self.season: Season = Season.Winter


class WinterEnd(Seasons):
    def __init__(self):
        self.start: datetime.datetime = datetime.datetime(2000, 11, 1, 0, 0)
        self.end: datetime.datetime = datetime.datetime(2000, 12, 31, 23, 59)
        self.season: Season = Season.Winter


list_seasons = [WinterStart(), Spring(), Summer(), Autumn(), WinterEnd()]

hour_minute_to_index: dict[int, dict[int, int]] = {}

count: int = 0
for i in range(24):
    hour_minute_to_index[i] = {}
    for j in range(4):
        hour_minute_to_index[i][j * 15] = count
        count += 1


def create_bdew_electrical_profile(
        profile_name: str,
        year: int,
        *,
        holidays_as_sundays: list[datetime.datetime] | None = None,
        holidays_as_saturdays: list[datetime.datetime] | None = None,
        dynamic: bool = False,
) -> NDArray[np.float64]:
    date = pd.DatetimeIndex(pd.date_range(datetime.datetime(year, 1, 1, 0), datetime.datetime(year, 12, 31, 23, 59), freq="15Min"))
    bdew = BDEWElectrical()
    _ = [seas.set_year(date[0].year) for seas in list_seasons]
    list_seasons_i = list_seasons.copy()
    seasons = np.zeros(len(date)).astype(object)
    for seas in list_seasons_i:
        seasons[np.logical_and(seas.start <= date, date < seas.end)] = seas.season

    sunday_holidays = [day.timetuple().tm_yday for day in holidays_as_sundays] if holidays_as_sundays is not None else []
    saturday_holidays = [day.timetuple().tm_yday for day in holidays_as_saturdays] if holidays_as_saturdays is not None else []
    days = [
        BDEWDAY.Sunday
        if date_i.isoweekday() == 7 or date_i.dayofyear in sunday_holidays
        else BDEWDAY.Saturday
        if date_i.isoweekday() == 6 or date_i.dayofyear in saturday_holidays
        else BDEWDAY.Workday
        for date_i in date
    ]

    hour_idx = np.array([hour_minute_to_index[date_i.hour][date_i.minute] for date_i in date]).astype(np.int64)
    profile = getattr(bdew, profile_name)
    results = np.array([profile[seas][day][idx] for seas, day, idx in zip(seasons, days, hour_idx)])
    if dynamic:
        days_of_year = np.array([date_i.dayofyear for date_i in date])
        a_4, a_3, a_2, a_1, a_0 = -3.92e-10, 3.20e-07, -7.02e-05, 2.10e-03, 1.24
        results = results * ((((a_4 * days_of_year + a_3) * days_of_year + a_2) * days_of_year + a_1) * days_of_year + a_0)

    return results
