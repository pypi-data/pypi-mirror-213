"""
test the export function
"""

from os import remove
from os.path import dirname, realpath

from numpy import allclose as np_allclose
from numpy import column_stack
from pandas import read_csv

from tssm import Period
from tssm import TimeSeriesScalingModule as tssm

FOLDER = dirname(realpath(__file__))


def fun_test_export(tssm_test: tssm, name_csv: str):
    """
    checks if the export of tssm_test works correctly\n
    :param tssm_test: TimeSeriesScalingModule to be exported
    :param name_csv: name of csv file
    """
    for name in [name_csv, None]:
        name_res = tssm_test.save_2_csv(name)
        if name is not None:
            assert name == name_res
        data_frame = read_csv(name_res, index_col=0)
        values = column_stack(
            [
                tssm_test.data.original,
                tssm_test.data.original * tssm_test.number_of_buildings,
                tssm_test.data.new,
            ]
        )
        assert np_allclose(data_frame.to_numpy()[:, 0].astype(float), values[:, 0].astype(float), atol=0.01)
        assert np_allclose(data_frame.to_numpy()[:, 1].astype(float), values[:, 1].astype(float), atol=0.01)
        assert np_allclose(data_frame.to_numpy()[:, 2].astype(float), values[:, 2].astype(float), atol=0.01)

        assert all(data_frame.to_numpy()[:, 3].astype("datetime64[s]") == tssm_test.data.date)
        try:
            remove(name_res)
        except PermissionError:
            pass


def test_export() -> None:
    """
    test export for the linear calculation approach
    """
    tssm_test = tssm(4, 0.95)
    tssm_test.data.read_profile_from_csv_with_date(f"{FOLDER}/test_data/profiles/data.csv", "Heating", "Date")
    for idx in Period:
        tssm_test.calculate_using_average_values(idx)
        fun_test_export(tssm_test, "linear.csv")
    """
    test export for the scaling profile calculation approach
    """
    tssm_test = tssm(4, 0.95)
    tssm_test.data.read_profile_from_csv_with_date(f"{FOLDER}/test_data/profiles/data.csv", "Heating", "Date")
    tssm_test.data.read_scaling_profile_from_csv(f"{FOLDER}/test_data/profiles/data.csv", "Cooling")
    for idx in Period:
        tssm_test.calculate_using_scaling_profile(idx)
        fun_test_export(tssm_test, "scaling_profile.csv")
    """
    test export for the normal distribution calculation approach
    """
    tssm_test = tssm(4)
    tssm_test.data.read_profile_from_csv_with_date(f"{FOLDER}/test_data/profiles/data.csv", "Heating", "Date")
    tssm_test.calculate_using_normal_distribution(sigma=0.5)
    fun_test_export(tssm_test, "normal_distribution.csv")
