from __future__ import annotations

import numpy as np
import pandas as pd
import datetime

from numpy.typing import NDArray

from tssm.calculation_models.profile_generation.hour_dict import HourFactors

WeekDayFactors: dict[str, tuple[float, float, float, float, float, float, float]] = {"EFH": (1.,) * 7, "MFH": (1.,) * 7, "GMK": (1.070, 1.037, 0.993, 0.995,
                                                                                                                                 1.066, 0.936, 0.903),
                                                                                     "GPD": (1.021, 1.087, 1.072, 1.056, 1.012, 0.900, 0.851), "GHA": (1.036,
                                                                                                                                                       1.023,
                                                                                                                                                       1.025,
                                                                                                                                                       1.030,
                                                                                                                                                       1.025,
                                                                                                                                                       0.967,
                                                                                                                                                       0.893),
                                                                                     "GBD": (1.105, 1.086, 1.038, 1.062, 1.027, 0.763, 0.898),
                                                                                     "GKO": (1.035, 1.052, 1.045, 1.049, 0.988, 0.886, 0.944),
                                                                                     "GBH": (0.977, 1.039, 1.003, 1.016, 1.002, 1.004, 0.958),
                                                                                     "GGA": (0.932, 0.989, 1.003, 1.011, 1.018, 1.036, 1.009),
                                                                                     "GBA": (1.085, 1.121, 1.077, 1.135, 1.140, 0.485, 0.958),
                                                                                     "GWA": (1.246, 1.261, 1.271, 1.243, 1.128, 0.388, 0.462),
                                                                                     "GGB": (0.990, 0.963, 1.051, 1.055, 1.030, 0.977, 0.936),
                                                                                     "GMF": (1.035, 1.052, 1.045, 1.049, 0.988, 0.886, 0.944),
                                                                                     "GHD": (1.030, 1.030, 1.020, 1.030, 1.010, 0.930, 0.940)}

SigmoidFactors: dict[str, dict[int, dict[bool, tuple[float, float, float, float]]]] = {'EFH': {1: {True: (3.2279446, -37.42148, 6.2222288, 0.0828441),
                                                                                                   False: (3.0890721,
                                                                                                           -37.1849497,
                                                                                                           5.7137959,
                                                                                                           0.1071295)},
                                                                                               2: {True: (3.2107659, -37.4178801, 6.2024, 0.0865217),
                                                                                                   False: (3.0722215, -37.1842844, 5.6975234, 0.1108074)},
                                                                                               3: {True: (3.1935978, -37.4142478, 6.1824021, 0.0901957),
                                                                                                   False: (3.0553842, -37.1836374, 5.6810825, 0.11448)},
                                                                                               4: {True: (3.1764404, -37.4105832, 6.1622336, 0.0938662),
                                                                                                   False: (3.0385547, -37.1829908, 5.6644869, 0.1181514)},
                                                                                               5: {True: (3.159294, -37.406886, 6.1418926, 0.0975329),
                                                                                                   False: (3.0217399, -37.18236, 5.647717, 0.1218169)},
                                                                                               6: {True: (3.1421588, -37.4031563, 6.1213773, 0.1011959),
                                                                                                   False: (3.0049303, -37.1817595, 5.6308191, 0.1254825)},
                                                                                               7: {True: (3.1250349, -37.3993941, 6.1006859, 0.104855),
                                                                                                   False: (2.9881355, -37.1811865, 5.6137482, 0.1291431)},
                                                                                               8: {True: (3.1079226, -37.3955994, 6.0798166, 0.1085103),
                                                                                                   False: (2.9713479, -37.1806299, 5.5965242, 0.1328015)},
                                                                                               9: {True: (3.0908222, -37.3917722, 6.0587677, 0.1121617),
                                                                                                   False: (2.9545709, -37.1800956, 5.5791367, 0.1364576)},
                                                                                               10: {True: (3.0737337, -37.3879125, 6.0375374, 0.1158091),
                                                                                                    False: (2.9378047, -37.1795853, 5.5615838, 0.1401107)},
                                                                                               11: {True: (3.1850191, -37.4124155, 6.1723179, 0.0920309),
                                                                                                    False: (3.0469695, -37.1833141, 5.6727847, 0.1163157)}},
                                                                                       'MFH': {1: {True: (2.5736652, -35.0169442, 6.131814, 0.0996851),
                                                                                                   False: (2.4428072, -34.7321438, 5.7347347, 0.1236492)},
                                                                                               2: {True: (2.5516882, -35.0234219, 6.1680699, 0.108708),
                                                                                                   False: (2.4207684, -34.7277917, 5.7668252, 0.1326318)},
                                                                                               3: {True: (2.529738, -35.0300145, 6.2051109, 0.1177216),
                                                                                                   False: (2.3987552, -34.7234878, 5.7996446, 0.1416084)},
                                                                                               4: {True: (2.507817, -35.0367363, 6.2430159, 0.1267238),
                                                                                                   False: (2.3767684, -34.7192333, 5.8332162, 0.1505787)},
                                                                                               5: {True: (2.4859161, -35.0435978, 6.2818214, 0.1357193),
                                                                                                   False: (2.3548083, -34.7150299, 5.8675639, 0.1595427)},
                                                                                               6: {True: (2.4640414, -35.0505874, 6.321514, 0.1447056),
                                                                                                   False: (2.3328756, -34.7108776, 5.9027152, 0.1685)},
                                                                                               7: {True: (2.4421941, -35.0577078, 6.3621285, 0.153682),
                                                                                                   False: (2.3109709, -34.7067802, 5.9386943, 0.1774504)},
                                                                                               8: {True: (2.4203748, -35.0649619, 6.4036973, 0.1626484),
                                                                                                   False: (2.2890947, -34.7027395, 5.9755295, 0.1863939)},
                                                                                               9: {True: (2.398584, -35.0723524, 6.446253, 0.1716044),
                                                                                                   False: (2.2672475, -34.6987574, 6.0132489, 0.1953302)},
                                                                                               10: {True: (2.3768224, -35.0798821, 6.4898289, 0.1805499),
                                                                                                    False: (2.2454319, -34.6948549, 6.0518709, 0.2042586)},
                                                                                               11: {True: (2.5187775, -35.0333754, 6.2240634, 0.1222227),
                                                                                                    False: (2.3877618, -34.7213605, 5.8164304, 0.1460936)}},
                                                                                       'GMK': {0: {True: (3.1177248, -35.8715062, 7.5186829, 0.0343301),
                                                                                                   False: (2.7882424, -34.880613, 6.5951899, 0.0540329)}},
                                                                                       'GPD': {0: {True: (3.85, -37.0, 10.2405021, 0.0469243),
                                                                                                   False: (2.5784173, -34.7321261, 6.4805035, 0.1407729)}},
                                                                                       'GHA': {0: {True: (4.0196902, -37.8282037, 8.1593369, 0.0472845),
                                                                                                   False: (3.5811214, -36.9650065, 7.2256947, 0.0448416)}},
                                                                                       'GBD': {0: {True: (3.75, -37.5, 6.8, 0.0609113),
                                                                                                   False: (2.9177027, -36.1794117, 5.9265162, 0.1151912)}},
                                                                                       'GKO': {0: {True: (3.4428943, -36.6590504, 7.6083226, 0.074685),
                                                                                                   False: (2.7172288, -35.1412563, 7.1303395, 0.1418472)}},
                                                                                       'GBH': {0: {True: (2.4595181, -35.2532123, 6.0587001, 0.164737),
                                                                                                   False: (2.0102472, -35.2532123, 6.1544406, 0.3294741)}},
                                                                                       'GGA': {0: {True: (2.8195656, -36.0, 7.7368518, 0.157281),
                                                                                                   False: (2.2850165, -36.2878584, 6.5885126, 0.3150535)}},
                                                                                       'GBA': {0: {True: (0.9315889, -33.35, 5.7212303, 0.6656494),
                                                                                                   False: (0.6522601, -37.1729781, 5.5973647, 0.8220629)}},
                                                                                       'GWA': {0: {True: (1.0535875, -35.3, 4.8662747, 0.6811042),
                                                                                                   False: (0.765729, -36.0237911, 4.8662747, 0.8049425)}},
                                                                                       'GGB': {0: {True: (3.6017736, -37.8825368, 6.983607, 0.0548262),
                                                                                                   False: (3.3904645, -39.2875216, 4.490574, 0.0834783)}},
                                                                                       'GMF': {0: {True: (2.5187775, -35.0333754, 6.2240634, 0.0977782),
                                                                                                   False: (2.3877618, -34.7213605, 5.8164304, 0.1168748)}},
                                                                                       'GHD': {0: {True: (2.579251014, -35.6816144, 6.685797612, 0.199554099),
                                                                                                   False: (
                                                                                                       3.008434556, -36.60784527, 7.321186953, 0.154966031)}}}

temp_interval: dict[int, int] = {
    -20: 0,
    -19: 0,
    -18: 0,
    -17: 0,
    -16: 0,
    -15: 0,
    -14: 1,
    -13: 1,
    -12: 1,
    -11: 1,
    -10: 1,
    -9: 2,
    -8: 2,
    -7: 2,
    -6: 2,
    -5: 2,
    -4: 3,
    -3: 3,
    -2: 3,
    -1: 3,
    0: 3,
    1: 4,
    2: 4,
    3: 4,
    4: 4,
    5: 4,
    6: 5,
    7: 5,
    8: 5,
    9: 5,
    10: 5,
    11: 6,
    12: 6,
    13: 6,
    14: 6,
    15: 6,
    16: 7,
    17: 7,
    18: 7,
    19: 7,
    20: 7,
    21: 8,
    22: 8,
    23: 8,
    24: 8,
    25: 8,
    26: 9,
    27: 9,
    28: 9,
    29: 9,
    30: 9,
    31: 9,
    32: 9,
    33: 9,
    34: 9,
    35: 9,
    36: 9,
    37: 9,
    38: 9,
    39: 9,
    40: 9,
}


def create_bdew_heat_profile(temperature: NDArray[np.float64], year: int, building_type: str, building_class: int, annual_heat_demand: float,
                             *, geometric_series: bool = True, include_domestic_hot_water: bool = False, wind_impact: bool = False,
                             holidays_as_sundays: list[datetime.datetime] | None = None,
                             holidays_as_saturdays: list[datetime.datetime] | None = None, ):
    building_type = building_type.upper()
    date = pd.DatetimeIndex(pd.date_range(datetime.datetime(year, 1, 1, 0), datetime.datetime(year, 12, 31, 23, 59), freq="1h"))

    sunday_holidays = [day.timetuple().tm_yday for day in holidays_as_sundays] if holidays_as_sundays is not None else []
    saturday_holidays = [day.timetuple().tm_yday for day in holidays_as_saturdays] if holidays_as_saturdays is not None else []
    day_idx: list[int] = [6 if date_i.dayofyear in sunday_holidays else 5 if date_i.dayofyear in saturday_holidays else (date_i.isoweekday() - 1) for date_i in
                          date]

    daily_mean_temperature = pd.DataFrame(temperature, columns=["temperatures"], index=pd.DatetimeIndex(date)).resample("D").mean().reindex(
        pd.DatetimeIndex(date)).fillna(method="ffill").fillna(method="bfill")["temperatures"].to_numpy()
    if geometric_series:
        daily_mean_temperature = (daily_mean_temperature + 0.5 * np.roll(daily_mean_temperature, 24) + 0.25 * np.roll(daily_mean_temperature,
                                                                                                                      48) + 0.125 * np.roll(
            daily_mean_temperature, 72)) / 1.875

    week_day_factors = WeekDayFactors[building_type]

    hour_factors = HourFactors[building_type][building_class]
    sf = [hour_factors[day][date_i.hour][temp_interval[temp]] for date_i, day, temp in zip(date, day_idx, np.ceil(daily_mean_temperature))]

    f = np.array([week_day_factors[day] for day in day_idx])
    a, b, c, d = SigmoidFactors[building_type][building_class][wind_impact]
    h = a / (1 + (b / (daily_mean_temperature - 40)) ** c) + (d if include_domestic_hot_water else 0)
    kw = 1.0 / (np.sum(h * f) / 24)
    heat_profile_normalized = kw * h * f * sf

    return heat_profile_normalized * annual_heat_demand / np.sum(heat_profile_normalized)