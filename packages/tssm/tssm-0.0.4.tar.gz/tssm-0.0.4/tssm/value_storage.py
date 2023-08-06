"""
python script for the value storage dataclass and its functions
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import numpy as np
import pandas as pd

from tssm.utils.dict_casting import from_dict, to_dict

if TYPE_CHECKING:
    from pathlib import Path

    from numpy.typing import NDArray


class NoColumnError(KeyError):
    """Error raised if column is not in dataframe"""

    def __init__(self, key: str):
        super().__init__(f"no such column {key} in pandas Dataframe")


class NoDataFrameError(FileNotFoundError):
    """Error if dataframe can not be located"""

    def __init__(self, path: str):
        super().__init__(f"pandas Dataframe not found: {path}")


@dataclass
class DataStorage:
    """class to store the original, new, average, scaling and date values"""

    reference: NDArray[np.float64] = field(default_factory=lambda: np.zeros(0))
    original: NDArray[np.float64] = field(default_factory=lambda: np.zeros(0))
    scaling: NDArray[np.float64] = field(default_factory=lambda: np.zeros(0))
    new: NDArray[np.float64] = field(default_factory=lambda: np.zeros(0))
    _date: NDArray[np.float64] = field(default_factory=lambda: np.zeros(0))
    time_step: NDArray[np.float64] | float | None = None

    def _get_date(self) -> NDArray[np.float64]:
        """
        get date
        """
        return self._date

    def _set_date(self, value: NDArray[np.float64]):
        """
        set date and determine time step
        """
        self._date = value
        self._determine_time_step()

    date = property(fget=_get_date, fset=_set_date, doc="date of original time series")

    def read_profile_from_csv_with_date(
        self,
        path: str,
        column_of_load: str,
        column_of_date: str,
        *,
        separator: str = ",",
        decimal: str = ".",
        date_format: str = "%Y-%m-%d %H:%M:%S",
    ) -> None:
        """
        read profile to be scaled from csv file and also the date of profile\n
        :param path: path of csv file from which the dataframe should be read
        :param column_of_load: column name of load profile in csv
        :param column_of_date: column name of date in csv
        :param separator: seperator sign between csv columns (default is ,)
        :param decimal: decimal sign in csv file (default is .)
        :param date_format: date time format if necessary (default YYYY-MM-DD hh:mm:ss)
        Link for date format https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
        """
        data_frame = self._read_dataframe_from_csv(path, separator, decimal)
        self._get_profile_from_dataframe(data_frame, column_of_load)
        date = self._get_date_from_dataframe(data_frame, column_of_date)
        self._reformat_date(date, date_format=date_format)

    def read_profile_from_csv(
        self,
        path: str,
        column_of_load: str,
        *,
        separator: str = ",",
        decimal: str = ".",
    ) -> None:
        """
        read profile to be scaled from csv file\n
        :param path: path of csv file from which the dataframe should be read
        :param column_of_load: column name of load profile in csv
        :param separator: seperator sign between csv columns (default is ,)
        :param decimal: decimal sign in csv file (default is .)
        """
        data_frame = self._read_dataframe_from_csv(path, separator, decimal)
        self._get_profile_from_dataframe(data_frame, column_of_load)

    def read_profile_from_dataframe(self, data_frame: pd.DataFrame, column_of_load: str) -> None:
        """
        read profile to be scaled from pandas dataframe\n
        :param data_frame: pandas dataframe to read profile from
        :param column_of_load: column name of load profile in pandas dataframe
        """
        self._get_profile_from_dataframe(data_frame, column_of_load)

    def read_profile_from_dataframe_with_date(
        self, data_frame: pd.DataFrame, column_of_load: str, column_of_date: str, *, date_format: str = "%Y-%m-%d %H:%M:%S"
    ) -> None:
        """
        read profile to be scaled from pandas dataframe including the date\n
        :param data_frame: pandas dataframe to read profile from
        :param column_of_load: column name of load profile in pandas dataframe
        :param column_of_date: column name of date in pandas dataframe
        :param date_format: date time format if necessary (default YYYY-MM-DD hh:mm:ss)
        Link for date format https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
        """
        self._get_profile_from_dataframe(data_frame, column_of_load)
        date = self._get_date_from_dataframe(data_frame, column_of_date)
        self._reformat_date(date, date_format=date_format)

    def set_profile_from_series_with_date(self, load_profile: pd.Series, date: pd.Series) -> None:
        """
        set load profile and date from pandas Series
        :param load_profile: load profile as pandas Series
        :param date: Date as pandas Series
        """
        self.original = load_profile.to_numpy(dtype=np.float64)
        self.date = date.to_numpy(dtype="datetime64[s]")

    def set_profile_from_series(self, load_profile: pd.Series) -> None:
        """
        set load profile from pandas Series
        :param load_profile: load profile as pandas Series
        """
        self.original = load_profile.to_numpy(dtype=np.float64)

    def set_profile_from_numpy_array(self, load_profile: NDArray[np.float64]) -> None:
        """
        set load profile from numpy array
        :param load_profile: load profile as numpy array
        """
        self.original = load_profile

    @staticmethod
    def _read_dataframe_from_csv(path: str | Path, separator: str = ",", decimal: str = ".") -> pd.DataFrame:
        """
        read dataframe from csv file\n
        :param path: path of csv file from which the dataframe should be read
        :param separator: seperator sign between csv columns (default is ,)
        :param decimal: decimal sign in csv file (default is .)
        """
        # try to read csv file if not found raise an exception
        try:
            data_frame: pd.DataFrame = pd.read_csv(path, sep=separator, decimal=decimal)
        except FileNotFoundError as exception:
            raise NoDataFrameError(f"{path}") from exception
        return data_frame

    @staticmethod
    def _get_date_from_dataframe(data_frame: pd.DataFrame, column_of_date: str) -> pd.Series:
        """
        get date from pandas Dataframe and check if column exists\n
        :param data_frame: pandas DataFrame to read the date from
        :param column_of_date: column name of date in Dataframe
        :return: pandas series of date
        """
        # try to get date from column otherwise raise column not found error
        try:
            date = data_frame[column_of_date]
        except KeyError as exception:
            raise NoColumnError(column_of_date) from exception
        return date

    def _get_profile_from_dataframe(self, data_frame: pd.DataFrame, column_of_load: str) -> None:
        """
        get profile from pandas Dataframe and check if column exists\n
        :param data_frame: pandas DataFrame to read the profile from
        :param column_of_load: column name of profile in Dataframe
        :return: pandas series of profile
        """
        # try to get load profile from column otherwise raise column not found error
        try:
            self.original = data_frame[column_of_load].to_numpy(dtype=np.float64)
        except KeyError as exception:
            raise NoColumnError(column_of_load) from exception

    def _reformat_date(self, date: pd.Series, *, date_format: str = "%Y-%m-%d %H:%M:%S") -> None:
        """
        reformat date input as pandas Dataframe to a numpy array\n
        :param date: pandas series including the date
        :param date_format: date time format if necessary (default YYYY-MM-DD hh:mm:ss)
        Link for date format https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
        """
        date = pd.to_datetime(date, format=date_format)
        self.date = date.to_numpy(dtype="datetime64[s]")

    def set_scaling_profile_from_numpy_array(self, load_profile: NDArray[np.float64]) -> None:
        """
        set scaling profile from numpy array
        :param load_profile: load profile as numpy array
        """
        # set scaling profile
        self.scaling = load_profile

    def set_scaling_profile_from_pandas_series(self, load_profile: pd.Series) -> None:
        """
        set scaling profile from pandas series
        :param load_profile: load profile as pandas series
        """
        # set scaling profile
        self.scaling = load_profile.to_numpy(dtype=np.float64)

    def read_scaling_profile_from_dataframe(self, data_frame: pd.DataFrame, column_of_scaled_profile: str) -> None:
        """
        read scaling profile from pandas dataframe
        :param data_frame: pandas dataframe to read profile from
        :param column_of_scaled_profile: column name of scaling profile in pandas dataframe
        """
        # set scaling profile
        self.scaling = data_frame[column_of_scaled_profile].to_numpy(dtype=np.float64)

    def read_scaling_profile_from_csv(self, path: str, column_of_scaled_profile: str, *, separator: str = ",", decimal: str = ".") -> None:
        """
        read profile to be scaled from csv file\n
        :param path: path of csv file from which the dataframe should be read
        :param column_of_scaled_profile: column name of scaling profile in csv
        :param separator: seperator sign between csv columns (default is ,)
        :param decimal: decimal sign in csv file (default is .)
        """
        # get pandas dataframe from csv file
        data_frame = self._read_dataframe_from_csv(path, separator, decimal)
        # set scaling profile
        self.scaling = data_frame[column_of_scaled_profile].to_numpy(dtype=np.float64)

    def _determine_time_step(self) -> None:
        """
        determine the time step of the date array
        """
        # if the length of the date is longer then one determine the time step
        if len(self.date) > 1:
            # determine the time step as an array
            time_step = np.array(np.diff(self.date), dtype=np.float64)
            # if all time steps are the same return the time step as a float
            if np.allclose(time_step, time_step[0]):
                self.time_step = time_step[0] / 3600
                return
            # otherwise append the first entry at the end and return the array
            self.time_step = np.append(time_step, time_step[0]) / 3600
            return

    def delete_zero_values(self) -> None:
        """
        delete the values in the data where the timestep is zero\n
        """
        # check if time step is an array (so different for every timestep)
        if isinstance(self.time_step, np.ndarray):
            # delete values in the original data
            self.original = np.delete(self.original, np.isclose(self.time_step, 0))
            # delete values in the date data
            self._date = np.delete(self._date, np.isclose(self.time_step, 0))
            # delete zero entries in the time step array
            self.time_step = np.delete(self.time_step, np.isclose(self.time_step, 0))

    def to_dict(self) -> dict:
        return to_dict(self)

    def from_dict(self, dictionary: dict) -> None:
        from_dict(self, dictionary)
        self.date = self.date.astype("datetime64[s]")
