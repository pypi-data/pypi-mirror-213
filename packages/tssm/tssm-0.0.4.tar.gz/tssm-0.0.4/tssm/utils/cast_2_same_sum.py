"""
cast the scaling profile to the same yearly sum as the original profile
"""
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from typing import Protocol

    from numpy.typing import NDArray

    class DataStorage(Protocol):
        reference: NDArray[np.float64]
        scaling: NDArray[np.float64]
        original: NDArray[np.float64]


def scale_scaling_profile_2_same_sum(
    values: DataStorage, one_2_many: bool, same_sum: bool, number_of_buildings: int | float, indexes: list[NDArray[np.int64]] | list[slice]
) -> None:
    """
    scales the scaling profile to the same sum of the original load
    Parameters
    ----------
    values: DataStorage
        values to be cast to the same sum
    one_2_many: bool
        upscale or downscale values
    same_sum: bool
        scale to the same sum?
    number_of_buildings: int | float
        amount of buildings
    indexes: list[NDArray[np.int64]] | list[slice]
        indexes for same sum calculation
    Returns
    -------
        None
    """
    if not same_sum:
        values.reference = values.scaling
        return
    # calculating the average loads
    sums_original: NDArray[np.float64] = np.zeros(values.original.size, dtype=np.float64)
    sums_scaling: NDArray[np.float64] = np.zeros(values.original.size, dtype=np.float64)

    for idx in indexes:
        sums_original[idx] = values.original[idx].sum()
        sums_scaling[idx] = values.scaling[idx].sum()
    values.reference = values.scaling / sums_scaling * sums_original / (1 if one_2_many else number_of_buildings)
