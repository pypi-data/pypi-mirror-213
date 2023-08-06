"""
Time series scaling module script with the used calculation model classes
"""
from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from scipy.sparse.linalg import spsolve

from tssm.utils import NoScalingProfileError, Period, calculate_indexes, scale_scaling_profile_2_same_sum

from .maximum_class import Maximum
from .normal_distribution_model import CalculationUsingNormalDistribution

if TYPE_CHECKING:
    from numpy.typing import NDArray

    from tssm.value_storage import DataStorage

    from .simultaneity_factor import SimultaneityFactor


class CalculationUsingScalingProfileAndNormalDistribution(CalculationUsingNormalDistribution):
    """
    class to calculate scaled profile using the normal distribution approach on the difference on the scaling profile and original profile and adding scaling
    profile\n
    """

    __slots__ = ("difference_values", "indexes")

    use_min = False

    def __init__(self, values: DataStorage, simultaneity_factor: SimultaneityFactor, number_of_buildings: int, one_2_many: bool = True):
        """
        init of CalculationUsingNormalDistribution class\n
        :param values: ValueStorage to get original values from
        :param simultaneity_factor: simultaneity factor to be up-scaled
        :param number_of_buildings: number of buildings
        :param one_2_many: should the profile be scaled form one profile to many (True) or many to one (False)
        """
        if values.scaling.size < 1:
            raise NoScalingProfileError()
        # get original values
        super().__init__(values, simultaneity_factor, number_of_buildings, one_2_many)

        self.indexes = calculate_indexes(Period.YEARLY, self.data.date)

        scale_scaling_profile_2_same_sum(values, one_2_many, True, number_of_buildings, self.indexes)

        self.difference_values = self.data.original - self.data.reference
        # determine maximum in the original values and its index as well as the length of original values
        self.maximum: Maximum = Maximum(self.data.original.max(initial=0), self.data.original.argmax(0))

        self.simultaneity_factor.use = simultaneity_factor.old if one_2_many else 1 / simultaneity_factor.old

    def calculate_normal_distributed_values(self, ran_yr: range, sigma: float) -> NDArray[np.float64]:
        """
        calculate normal distributed values\n
        :param ran_yr: range of the year for which the new values should be calculated
        :param sigma: variance of normal distribution
        :return: NDArray[np.float64] of new values
        """
        arr = (
            self.calculate_array_flexible_time_steps(ran_yr, sigma)
            if isinstance(self.data.time_step, np.ndarray)
            else self.calculate_array_normal_time_steps(ran_yr, sigma)
        )
        if self.one_2_many:  # pylint: disable=duplicate-code
            return arr.dot(self.difference_values) + self.data.reference
        return spsolve(arr, self.difference_values) + self.data.reference
