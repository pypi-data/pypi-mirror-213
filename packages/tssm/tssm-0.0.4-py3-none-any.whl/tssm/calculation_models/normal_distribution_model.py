"""
Time series scaling module script with the used calculation model classes
"""
from __future__ import annotations

import gc
from typing import TYPE_CHECKING

import numpy as np
from scipy import optimize
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve
from scipy.special import erf

from .calculation_base_class import CalculationClass
from .maximum_class import Maximum

if TYPE_CHECKING:
    from numpy.typing import NDArray

    from tssm.value_storage import DataStorage

    from .simultaneity_factor import SimultaneityFactor


class NoNumpyArrayError(TypeError):
    """Error raised if time steps are no numpy array"""

    def __init__(self, time_step: str):
        super().__init__(f"time_step: {time_step} is no numpy array")


class CalculationUsingNormalDistribution(CalculationClass):
    """
    class to calculate scaled profile using the normal distribution approach\n
    """

    __slots__ = ("maximum", "len_yr", "idx", "complete_year", "cum_val", "memory_range")

    # set maximal variance, and its corresponding indexes
    max_sigma: int = 90
    # predetermine sqrt of 2 * pi to save calculation time
    sqrt_2: float = 2**0.5
    # use minimal value
    use_min: bool = True
    # idx_variance
    idx_variance: int = 2500
    # min_time_step
    min_time_step: float = 0.000_1
    # min_error
    min_error: float = 0.1

    def __init__(self, values: DataStorage, simultaneity_factor: SimultaneityFactor, number_of_buildings: int, one_2_many: bool = True):
        """
        init of CalculationUsingNormalDistribution class\n
        :param values: ValueStorage to get original values from
        :param simultaneity_factor: simultaneity factor to be up-scaled
        :param number_of_buildings: number of buildings
        :param one_2_many: should the profile be scaled form one profile to many (True) or many to one (False)
        """
        # get original values
        super().__init__(values, simultaneity_factor, number_of_buildings, one_2_many=one_2_many)
        # determine maximum in the original values and its index as well as the length of original values
        self.maximum: Maximum = Maximum(self.data.original.max(initial=0), self.data.original.argmax(0))
        self.len_yr = self.data.original.size
        # create index for the length of the year so that the indexes > len_yr start at the beginning and indexes < 0 at the end
        self.idx: NDArray[np.uint64] = np.tile(np.arange(self.len_yr), 3)
        # should a complete year be considered? smaller for the determination of variance
        self.complete_year: bool = True

        self.memory_range: dict = {}

        if self.data.time_step is not None:
            cum_val = np.tile(self.data.time_step, 3).cumsum()
            self.cum_val = np.insert(cum_val, 0, 0)

    def calculate(self, *, scaling_factor: float | None = None, complete_year: bool = False) -> tuple[NDArray[np.float64], SimultaneityFactor]:
        """
        calculate_average_scaling up-scaled profile using the normal distribution method\n
        :param complete_year: should the complete year be considered during variance finding
        :param scaling_factor: variance of normal distribution. If None it is calculated depending on the simultaneity factor
        :return: scaled values
        """

        self.complete_year = complete_year

        sigma = self.determine_variance() if scaling_factor is None else scaling_factor
        self.simultaneity_factor.new = np.ones(1) * sigma
        self.calculate_new_values()

        # check if the maximal value has changed to a different time step so that the optimization has to be performed for the complete year
        # check if the maximal value index has changed
        if (
            not np.isclose(self.maximum.value * self.simultaneity_factor.use, np.max(self.data.new))
            and self.data.new.argmax(0) != self.data.original.argmax(0)
            and not complete_year
        ):
            # check if it has already changed and then calculate_average_scaling the complete year
            if self.data.original.argmax(0) != self.maximum.idx:
                return self.calculate(complete_year=True)
            # otherwise change the maximal value index and calculate_average_scaling again
            self.maximum.idx = self.data.new.argmax(0)
            return self.calculate(complete_year=False)
        # return the new values up-scaled by the number of buildings
        return self.data.new, self.simultaneity_factor

    def calculate_new_values(self) -> None:
        """
        Calculates the new value for each timestamp.\n
        """
        # calculate_average_scaling normal distribution
        values: NDArray[np.float64] = self.calculate_normal_distributed_values(range(self.len_yr), self.simultaneity_factor.new[0])

        self.data.new = values * (self.number_of_buildings if self.one_2_many else 1 / self.number_of_buildings)

    def determine_variance(self) -> float:
        """
        determine the variance by minimizing the difference to maximal value times simultaneity factor\n
        :return: variance as float
        """
        res = optimize.minimize(
            self.calculate_error,
            np.ones(1) * 1,
            method="Nelder-Mead",
            bounds=((0.01, self.max_sigma if isinstance(self.data.time_step, float) or self.data.time_step is None else 10),),
            tol=1e-5 if self.one_2_many else 1e-3,
        )
        if res.fun > self.min_error:
            for start_value in range(2, 30):
                res_i = optimize.minimize(
                    self.calculate_error,
                    np.ones(1) * start_value,
                    method="Nelder-Mead",
                    bounds=((0.01, self.max_sigma if isinstance(self.data.time_step, float) or self.data.time_step is None else 10),),
                    tol=1e-5 if self.one_2_many else 1e-3,
                )
                if res_i.fun < self.min_error:
                    res = res_i
                    break
                res = res_i if res_i.fun < res.fun else res
        # get variance from minimization results
        sigma = res.x[0]
        print(f"sigma: {sigma}, {res.fun}, {self.simultaneity_factor.use}")
        # raise an error if the variance is at the limits
        if np.isclose(sigma, 0.01) or np.isclose(sigma, self.max_sigma) or (res.fun > self.min_error > sigma):
            raise ValueError(
                f"For the selected simultaneity factor ({self.simultaneity_factor.use}) no normal distribution can be calculated (sigma:" f" {sigma})!"
            )
        return sigma

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
        if self.one_2_many:
            return arr.dot(self.data.original)
        return spsolve(arr, self.data.original)

    def calculate_array_flexible_time_steps(self, ran_yr: range, sigma: float) -> csr_matrix:
        """
        calculate sparse array for flexible time steps to calculate values\n
        :param ran_yr: range of the year for which the new values should be calculated
        :param sigma: variance of normal distribution
        :return: csr_matrix for the normal distribution values calculation
        """
        if not isinstance(self.data.time_step, np.ndarray):
            raise NoNumpyArrayError(f"{self.data.time_step}")
        values = [
            (i, j, self.data.time_step[i], self.data.time_step[self.idx[j]])
            for i in ran_yr
            for j in self._determine_start_end_range_for_flexible_time_step(i, sigma)
            if self.data.time_step[self.idx[j]] > self.min_time_step
        ]
        time_1 = np.array([self.cum_val[self.data.original.size + j] - self.cum_val[self.data.original.size + i] for i, j, _, _ in values])
        dtj = np.array([dt_j for _, _, _, dt_j in values])
        dti = np.array([dt_i for _, _, dt_i, _ in values])
        time = time_1 + dtj
        value = dti / dtj * (erf(time / (sigma * self.sqrt_2)) - erf(time_1 / (sigma * self.sqrt_2))) / 2
        row = [self.idx[j] for _, j, _, _ in values]
        column = [self.idx[i] for i, _, _, _ in values]

        return csr_matrix((value, (row, column)), shape=(self.data.original.size, self.data.original.size))

    def calculate_array_normal_time_steps(self, ran_yr: range, sigma: float) -> csr_matrix:
        """
        calculate sparse array for normal fixed time steps to calculate values\n
        :param ran_yr: range of the year for which the new values should be calculated
        :param sigma: variance of normal distribution
        :return: csr_matrix for the normal distribution values calculation
        """
        # cut sigma into int
        sigma_int = int(sigma + 0.5) if self.data.time_step is None else int(sigma / self.data.time_step + 0.5)

        factor: int = int(1 / (1 if self.data.time_step is None else self.data.time_step))
        # create maximal sigma range
        maximal_range: NDArray[np.float64] = np.arange(-4 * sigma_int - 2 * factor, 4 * sigma_int + 2 * factor) * (
            1 if self.data.time_step is None else self.data.time_step
        )
        # determine the idx range for the negative values
        idx_sigma: int = sigma_int * 4 + 2 * factor
        # pre calculate_average_scaling value to increase calculation speed
        if self.data.time_step is None:
            erf_values = np.array((erf((maximal_range + 0.5) / (sigma * self.sqrt_2)) - erf((maximal_range - 0.5) / (sigma * self.sqrt_2))) / 2)
        else:
            erf_values = (
                erf((maximal_range + self.data.time_step / 2) / (sigma * self.sqrt_2)) - erf((maximal_range - self.data.time_step / 2) / (sigma * self.sqrt_2))
            ) / 2
        start = 4 * sigma_int + 1 * factor
        ending = 4 * sigma_int + 2 * factor
        gc.collect()
        value = [erf_values[idx_sigma + (j - i)] for i in ran_yr for j in range(i - start, i + ending)]
        gc.collect()
        row = [self.idx[j] for i in ran_yr for j in range(i - start, i + ending)]
        gc.collect()
        column = [self.idx[i] for i in ran_yr for _ in range(i - start, i + ending)]
        gc.collect()
        return csr_matrix((value, (row, column)), shape=(self.data.original.size, self.data.original.size))

    def calculate_error(self, sigma: NDArray[np.float64]) -> float:
        """
        calculate_average_scaling normal distribution error for the input sigma\n
        :param sigma: Variance of normal distribution as array because scipy minimize is working with arrays
        :return: absolute difference of maximal values with simultaneity factor consideration
        """
        # get variance from array
        sigma_val = sigma[0] if not isinstance(sigma, (float, int)) else sigma
        # create either a complete year or an around the maximal value range
        ran: range = self._determine_range(sigma_val, self.complete_year) if self.one_2_many else self._determine_range(sigma_val, True)
        # determine normal distributed values
        values: NDArray[np.float64] = self.calculate_normal_distributed_values(ran, sigma_val)
        # return absolute difference between maximum of original values considering the simultaneity factor and tha maximum of new values
        min_val = (min(values) - min(values[values > 0])) if self.use_min else 0
        # print(sigma, str(abs(self.maximum.value * self.simultaneity_factor.old[0] - max(values)) + abs(min_val)))
        return float(abs(self.maximum.value * self.simultaneity_factor.use - np.max(values)) + abs(min_val))

    def _determine_range(self, sigma_val: float, complete_year: bool) -> range:
        if complete_year:
            return range(self.len_yr)
        if self.data.time_step is None:
            return range(self.maximum.idx - 4 * int(sigma_val + 0.5) - 1, self.maximum.idx + 4 * int(sigma_val + 0.5) + 2)
        if isinstance(self.data.time_step, float):
            return range(
                self.maximum.idx - 4 * int(sigma_val / self.data.time_step + self.data.time_step / 2) - 1 * int(1 / self.data.time_step),
                self.maximum.idx + 4 * int(sigma_val / self.data.time_step + self.data.time_step / 2 * int(1 / self.data.time_step)) + 2,
            )
        return self._determine_start_end_range_for_flexible_time_step(self.maximum.idx, sigma_val)

    def _determine_start_end_range_for_flexible_time_step(self, index: int, sigma_val: float) -> range:
        """
        determine the range for a flexible time step
        """
        if not isinstance(self.data.time_step, np.ndarray):
            raise NoNumpyArrayError(f"{self.data.time_step}")
        key = f"{index}_{sigma_val:.3f}"
        if key in self.memory_range:
            return self.memory_range[key]
        sl_start = slice(self.data.original.size + index, self.data.original.size + index - self.idx_variance, -1)
        sl_end = slice(self.data.original.size + index, self.data.original.size + index + self.idx_variance)
        idx_start = self.idx[sl_start]
        idx_end = self.idx[sl_end]
        start_index: int = idx_start[self.cum_val[self.data.original.size + index] - self.cum_val[sl_start] <= (5 * sigma_val + 2)][-1] - 1
        if start_index > self.idx_variance and index - self.idx_variance < 0:
            start_index -= self.data.original.size
        end_index: int = idx_end[self.cum_val[sl_end] - self.cum_val[self.data.original.size + index] <= (5 * sigma_val + 2)][-1]
        if end_index < start_index:
            end_index += self.data.original.size

        self.memory_range[key] = range(start_index, end_index)

        return self.memory_range[key]
