"""
Time series scaling module main script
"""
from __future__ import annotations

from typing import TYPE_CHECKING

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from tssm.calculation_models import (
    CalculationUsingNormalDistribution,
    calculate_using_scaling_profile_model,
    CalculationUsingScalingProfileAndNormalDistribution,
    SimultaneityFactor,
    calculate_average_model,
)
from tssm.utils import Period, from_dict, to_dict, cast_input_2_period
from tssm.value_storage import DataStorage

if TYPE_CHECKING:
    from numpy.typing import NDArray


class NoProfileSelectedError(ValueError):
    """Error raised if no profile is selected"""

    def __init__(self) -> None:
        super().__init__("No profile selected")


class TimeSeriesScalingModule:
    """
    class to calculate_average_scaling an up-scaling profile
    """

    __slots__ = ("data", "number_of_buildings", "simultaneity_factor", "new_simultaneity_factor", "one_2_many")

    def __init__(self, number_of_buildings: float, simultaneity_factor: float | None = None, *, one_2_many: bool = True) -> None:
        """
        initialize time series scaling module\n
        :param number_of_buildings: number of houses
        :param simultaneity_factor: the simultaneity factor for (default = 1)
        :param one_2_many: should the profile be scaled form one profile to many (True) or many to one (False) (default = True)
        """
        self.number_of_buildings: float = number_of_buildings
        self.simultaneity_factor: SimultaneityFactor = SimultaneityFactor(1 if simultaneity_factor is None else simultaneity_factor)
        self.new_simultaneity_factor: NDArray[np.float64] = np.zeros(0)
        self.data: DataStorage = DataStorage()
        self.one_2_many: bool = one_2_many

    def check_for_profile(self):
        """check if a profile has been selected otherwise raise an Error"""
        if len(self.data.original) < 1:
            raise NoProfileSelectedError()

    def calculate_using_scaling_profile(
        self, period: Period | str | int, *, scaling_factor: pd.Series | NDArray[np.float64] | list[float] | None = None, same_sum: bool = False
    ) -> NDArray[np.float64]:
        """
        calculate new time series by using the scaling approach\n
        :param period: period of time(1: day; 2:week; 3: month; 4:year) for which average is going to be calculated
        calculate_average_scaling load using the scaling profile
        :param scaling_factor: scaling factor if simultaneity factor should not be considered
        :param same_sum: size scaling profile to the same sum as the original profile (default=False)
        :return: new time series as numpy array
        """
        self.check_for_profile()
        period = cast_input_2_period(period)
        self.data.new, self.simultaneity_factor.new = calculate_using_scaling_profile_model(
            self.data, period, self.one_2_many, self.number_of_buildings, self.simultaneity_factor.old, scaling_factor=scaling_factor, same_sum=same_sum
        )
        return self.data.new

    def calculate_using_average_values(
        self, period: Period | str | int, *, scaling_factor: pd.Series | NDArray[np.float64] | list[float] | None = None
    ) -> NDArray[np.float64]:
        """
        calculate new time series by using the linear approach\n
        :param period: period of time(1: day; 2:week; 3: month; 4:year) for which average is going to be calculated
        calculate_average_scaling load using the scaling profile
        :param scaling_factor: scaling factor if simultaneity factor should not be considered
        :return: new time series as numpy array
        """
        self.check_for_profile()
        period = cast_input_2_period(period)
        self.data.new, self.simultaneity_factor.new = calculate_average_model(
            self.data, period, self.simultaneity_factor.old, self.number_of_buildings, one_2_many=self.one_2_many, scaling_factor=scaling_factor
        )
        return self.data.new

    def calculate_using_normal_distribution(self, *, sigma: float | None = None) -> NDArray[np.float64]:
        """
        calculate_average_scaling new profile using the normal distribution approach.\n
        :param sigma: variance if it should not be calculated
        :return: new time series as numpy array
        """
        self.check_for_profile()
        calc_model = CalculationUsingNormalDistribution(self.data, self.simultaneity_factor, self.number_of_buildings, one_2_many=self.one_2_many)
        self.data.new, self.simultaneity_factor = calc_model.calculate(scaling_factor=sigma, complete_year=sigma is not None)
        return self.data.new

    def calculate_using_scaling_and_normal_distribution(self, *, sigma: float | None = None) -> NDArray[np.float64]:
        """
        calculate_average_scaling new profile using the normal distribution approach.\n
        :param sigma: variance if it should not be calculated
        :return: new time series as numpy array
        """
        self.check_for_profile()
        calc_model = CalculationUsingScalingProfileAndNormalDistribution(
            self.data, self.simultaneity_factor, self.number_of_buildings, one_2_many=self.one_2_many
        )
        self.data.new, self.simultaneity_factor = calc_model.calculate(scaling_factor=sigma, complete_year=sigma is not None)
        return self.data.new

    def save_2_csv(self, data_name: str | None = None) -> str:
        """
        exports result Dataframe to csv.\n
        :param data_name: name of file with results
        :return: data name string
        """
        # create results array
        result_array: NDArray[np.float64] = np.column_stack(
            [
                self.data.original,
                self.data.original * self.number_of_buildings,
                self.data.new,
            ]
        )
        # create pandas dataframe
        result_df: pd.DataFrame = pd.DataFrame(
            result_array,
            columns=[
                "original values",
                "original values times number of buildings",
                "new values",
            ],
        )
        # add Date to Dataframe
        result_df["Date"] = pd.Series(self.data.date)
        result_df.set_index("Date")
        # save time series to csv file by default or given data name
        data_name = "scaled_time_series.csv" if data_name is None else data_name
        result_df.to_csv(data_name, index=True)
        return data_name

    def get_factor(self) -> float:
        return self.simultaneity_factor.new[0]

    def plot_values(self, max_original: bool = True, legend: bool = False, scaled: bool = False) -> tuple[plt.Figure, plt.Axes]:
        plt.rc("figure")
        fig = plt.figure()
        ax = fig.add_subplot(111)
        max_idx = self.data.original.argmax() if max_original else self.data.new.argmax()
        time_steps = list(range(max_idx - 12, max_idx + 12))

        ax.set_xlabel(r"Time")
        ax.set_ylabel(r"Power")

        ax.plot(self.data.date[time_steps], self.data.original[time_steps], "b-", linewidth=1.5, label="original")
        new_data = self.data.new[time_steps] if not scaled else self.data.new[time_steps] / self.number_of_buildings
        ax.plot(self.data.date[time_steps], new_data, "g-", linewidth=1.5, label="new")
        if len(self.data.scaling) > 20:
            new_data = self.data.reference[time_steps] if not scaled else self.data.reference[time_steps] / self.number_of_buildings
            ax.plot(self.data.date[time_steps], new_data, "r-", linewidth=1.5, label="scaling")

        date_formatter = mdates.DateFormatter("%d.%m.%Y %H:%M")
        ax.xaxis.set_major_formatter(date_formatter)

        # Plot legend
        if legend:
            ax.legend()

        return fig, ax

    def to_dict(self) -> dict:
        return to_dict(self)

    @staticmethod
    def from_dict(dictionary) -> TimeSeriesScalingModule:
        res = TimeSeriesScalingModule(4, 1)
        from_dict(res, dictionary)
        return res
