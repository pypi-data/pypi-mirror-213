"""
test different ways to import data to TSSM
"""
from os.path import dirname, realpath

from numpy import allclose, isclose, zeros
from numpy import any as np_any
from pandas import read_csv, to_datetime
from pytest import raises

from tssm.time_series_scaling_module import DataStorage

FOLDER = dirname(realpath(__file__))


def test_profile_import():
    """
    test the profile import functions\n
    """
    path_data = f"{FOLDER}/test_data/profiles/data.csv"
    data = read_csv(path_data)
    column_load = "Heating"
    column_date = "Date"
    profile_series = data[column_load]
    profile_array = profile_series.to_numpy()
    date_series = to_datetime(data[column_date], format="%Y-%m-%d %H:%M:%S")
    date_array = date_series.to_numpy(dtype="datetime64[s]")
    #
    # unit test for Values Storage
    #
    value_storage = DataStorage()
    value_storage.set_profile_from_series_with_date(profile_series, date_series)
    assert allclose(profile_array, value_storage.original)
    assert all(date_array == value_storage.date)
    value_storage = DataStorage()
    value_storage.read_profile_from_csv_with_date(path_data, column_load, column_date)
    assert allclose(profile_array, value_storage.original)
    assert all(date_array == value_storage.date)
    value_storage = DataStorage()
    value_storage.set_profile_from_numpy_array(profile_array)
    assert allclose(profile_array, value_storage.original)
    value_storage = DataStorage()
    value_storage.read_profile_from_dataframe_with_date(data, column_load, column_date)
    assert allclose(profile_array, value_storage.original)
    assert all(date_array == value_storage.date)
    value_storage = DataStorage()
    value_storage.set_profile_from_series(profile_series)
    assert allclose(profile_array, value_storage.original)
    assert all(zeros(0) == value_storage.date)
    value_storage = DataStorage()
    value_storage.read_profile_from_csv(path_data, column_load)
    assert allclose(profile_array, value_storage.original)
    assert all(zeros(0) == value_storage.date)


def test_scaling_profile_import():
    """
    test scaling data import
    """
    path_data = f"{FOLDER}/test_data/profiles/data.csv"
    data = read_csv(path_data)
    column_load = "Heating"
    profile_array = data[column_load].to_numpy()
    path_scaled_data = f"{FOLDER}/test_data/Profile_1h_scaling.csv"
    scaled_data = read_csv(path_scaled_data)
    column_scaling_profile = "H0"
    profile_series = scaled_data[column_scaling_profile]
    scaling_profile_array = profile_series.to_numpy()
    # read scaling data csv as pandas Dataframe
    scaling_data = read_csv(path_scaled_data)
    value_storage = DataStorage()
    value_storage.set_profile_from_numpy_array(profile_array)
    # read scaling profile from Profile_1h_scaling.csv and use H0 column
    # optionally the separator is set to , which is the default, decimal sign is set to ., which is the default
    value_storage.read_scaling_profile_from_csv(path_scaled_data, column_scaling_profile, separator=",", decimal=".")
    assert allclose(profile_array, value_storage.original)
    assert allclose(scaling_profile_array, value_storage.scaling)
    assert not isclose(sum(value_storage.original), sum(value_storage.scaling))
    # read scaling profile from pandas Dataframe
    value_storage.read_scaling_profile_from_dataframe(scaling_data, "H0")
    assert allclose(profile_array, value_storage.original)
    assert allclose(scaling_profile_array, value_storage.scaling)
    assert not isclose(sum(value_storage.original), sum(value_storage.scaling))
    # set scaling profile from pandas Series
    value_storage.set_scaling_profile_from_pandas_series(scaling_data["H0"])
    assert allclose(profile_array, value_storage.original)
    assert allclose(scaling_profile_array, value_storage.scaling)
    assert not isclose(sum(value_storage.original), sum(value_storage.scaling))
    # set scaling profile from numpy array
    value_storage.set_scaling_profile_from_numpy_array(scaling_data["H0"].to_numpy())
    assert allclose(profile_array, value_storage.original)
    assert allclose(scaling_profile_array, value_storage.scaling)
    assert not isclose(sum(value_storage.original), sum(value_storage.scaling))


def test_import_new_file():
    """
    test import of data comma as decimal sign and separated by semicolon\n
    """
    path_data = f"{FOLDER}/test_data/data_comma_semicolon.csv"
    sep = ";"
    decimal = ","
    data = read_csv(path_data, sep=sep, decimal=decimal)
    column_load = "Heating"
    column_date = "Date"
    date_format = "%d,%m,%Y %H:%M"
    profile_series = data[column_load]
    profile_array = profile_series.to_numpy()
    date_series = to_datetime(data[column_date], format=date_format)
    date_array = date_series.to_numpy(dtype="datetime64[s]")
    #
    # unit test for Values Storage
    #
    value_storage = DataStorage()
    value_storage.set_profile_from_series_with_date(profile_series, date_series)
    assert allclose(profile_array, value_storage.original)
    assert all(date_array == value_storage.date)
    value_storage = DataStorage()
    value_storage.read_profile_from_csv_with_date(path_data, column_load, column_date, separator=sep, decimal=decimal, date_format=date_format)
    assert allclose(profile_array, value_storage.original)
    assert all(date_array == value_storage.date)
    value_storage = DataStorage()
    value_storage.read_profile_from_dataframe_with_date(data, column_load, column_date, date_format=date_format)
    assert allclose(profile_array, value_storage.original)
    assert all(date_array == value_storage.date)
    value_storage = DataStorage()
    value_storage.set_profile_from_series(profile_series)
    assert allclose(profile_array, value_storage.original)
    assert all(zeros(0) == value_storage.date)
    value_storage = DataStorage()
    value_storage.read_profile_from_csv(path_data, column_load, separator=sep, decimal=decimal)
    assert allclose(profile_array, value_storage.original)
    assert all(zeros(0) == value_storage.date)
    value_storage = DataStorage()
    value_storage.read_profile_from_dataframe(data, column_load)
    assert allclose(profile_array, value_storage.original)
    assert all(zeros(0) == value_storage.date)


def test_read_profile_from_csv_fails():
    """
    check if an error is raised if a not existing csv file link is provided.
    """
    with raises(FileNotFoundError):
        value_storage = DataStorage()
        value_storage.read_profile_from_csv("no_data.csv", "Heating")


def test_key_error_on_data():
    """
    test if an error is raised if a not existing column name is provided.
    """
    with raises(KeyError):
        path_data = f"{FOLDER}/test_data/profiles/data.csv"
        value_storage = DataStorage()
        value_storage.read_profile_from_csv(path_data, "NotExistingColumn")


def test_key_error_on_date():
    """
    test if an error is raised if a not existing column name for the date is provided.
    """
    with raises(KeyError):
        path_data = f"{FOLDER}/test_data/profiles/data.csv"
        value_storage = DataStorage()
        value_storage.read_profile_from_csv_with_date(path_data, "Heating", "NotExistingColumn")


def test_zero_deletion():
    """
    test if for a year with flexible time steps the zero time steps are deleted\n
    """
    path_data = f"{FOLDER}/test_data/profiles/data_flex_time_step_short.csv"
    value_storage = DataStorage()
    value_storage.read_profile_from_csv_with_date(path_data, "Heating", "Date")
    len_before = len(value_storage.original)
    value_storage.delete_zero_values()
    assert value_storage.time_step is not None
    assert not np_any(value_storage.time_step < 0.000_000_1)
    assert not isinstance(value_storage.time_step, float)
    assert not isinstance(value_storage.original, float)
    assert not isinstance(value_storage.date, float)
    assert value_storage.time_step.size < len_before
    assert value_storage.time_step.size == value_storage.original.size
    assert value_storage.time_step.size == value_storage.date.size
