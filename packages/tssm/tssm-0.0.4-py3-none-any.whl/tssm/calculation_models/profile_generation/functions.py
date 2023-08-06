from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pandas as pd

if TYPE_CHECKING:
    from numpy.typing import NDArray

intervals = {
    -20: 1,
    -19: 1,
    -18: 1,
    -17: 1,
    -16: 1,
    -15: 1,
    -14: 2,
    -13: 2,
    -12: 2,
    -11: 2,
    -10: 2,
    -9: 3,
    -8: 3,
    -7: 3,
    -6: 3,
    -5: 3,
    -4: 4,
    -3: 4,
    -2: 4,
    -1: 4,
    0: 4,
    1: 5,
    2: 5,
    3: 5,
    4: 5,
    5: 5,
    6: 6,
    7: 6,
    8: 6,
    9: 6,
    10: 6,
    11: 7,
    12: 7,
    13: 7,
    14: 7,
    15: 7,
    16: 8,
    17: 8,
    18: 8,
    19: 8,
    20: 8,
    21: 9,
    22: 9,
    23: 9,
    24: 9,
    25: 9,
    26: 10,
    27: 10,
    28: 10,
    29: 10,
    30: 10,
    31: 10,
    32: 10,
    33: 10,
    34: 10,
    35: 10,
    36: 10,
    37: 10,
    38: 10,
    39: 10,
    40: 10,
}


def get_temperature_interval(temperatures: NDArray[np.float64]):
    """Appoints the corresponding temperature interval to each temperature
    in the temperature vector.
    """
    return np.array([intervals[i] for i in np.ceil(temperatures).astype(np.int64)])


def weighted_temperature(temperatures: NDArray[np.float64], how="geometric_series"):
    """
    A new temperature vector is generated containing a multi-day
    average temperature as needed in the load profile function.

    Parameters
    ----------
    how : string
        string which type to return ("geometric_series" or "mean")

    Notes
    -----
    Equation for the mathematical series of the average
    temperature [1]_:

    .. math::
        T=\frac{T_{D}+0.5\cdot T_{D-1}+0.25\cdot T_{D-2}+
                0.125\cdot T_{D-3}}{1+0.5+0.25+0.125}

    with :math:`T_D` = Average temperature on the present day
         :math:`T_{D-i}` = Average temperature on the day - i

    References
    ----------
    .. [1] `BDEW <https://www.avacon-netz.de/content/dam/revu-global/avacon-netz/documents/Energie_anschliessen/netzzugang-gas/Leitfaden_20180329_Abwicklung-Standardlastprofile-Gas.pdf>`_,  # noqa: E501
        BDEW Documentation for heat profiles.
    """

    # calculate daily mean temperature
    temperature = (
        pd.DataFrame(temperatures, column="temperatures")["temperatures"]
        .resample("D")
        .mean()
        .reindex(self.df.index)
        .fillna(method="ffill")
        .fillna(method="bfill")
    )

    if how == "geometric_series":
        temperature_mean = (temperature + 0.5 * np.roll(temperature, 24) + 0.25 * np.roll(temperature, 48) + 0.125 * np.roll(temperature, 72)) / 1.875
    elif how == "mean":
        temperature_mean = temperature
    else:
        temperature_mean = None

    return temperature_mean


def test_get_temperature_interval():
    """
    test the temperature interval function
    """
    temperatures = np.arange(-20, 40, 0.1)

    results = np.zeros_like(temperatures)

    for idx, temp in enumerate(temperatures):
        results[idx] = intervals[int(np.ceil(temp))]

    res = get_temperature_interval(temperatures)

    assert np.allclose(res, results)
