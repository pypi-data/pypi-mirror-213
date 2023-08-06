"""
script to start the GUI
"""
# pragma: no cover
from __future__ import annotations

import datetime
from pathlib import Path

import pandas as pd

import logging
import sys
from functools import partial
from platform import system
from sys import argv
from sys import exit as sys_exit

from tssm import TimeSeriesScalingModule
from tssm.gui.gui_structure import GUI
from tssm.gui.translation_class import Translations

os_system = system()
is_frozen = getattr(sys, "frozen", False) and os_system == "Windows"  # pragma: no cover


def detect_date_format(csv_file: str | Path) -> str | None:
    df = pd.read_csv(csv_file)
    date_columns = df.select_dtypes(include=["object"]).columns
    if len(date_columns) > 0:
        formats = [
            "%Y-%m-%d %H:%M:%S",
            "%d-%m-%Y %H:%M:%S",
            "%m-%d-%Y %H:%M:%S",
            "%Y.%m.%d %H:%M:%S",
            "%d.%m.%Y %H:%M:%S",
            "%m.%d.%Y %H:%M:%S",
            "%Y/%m/%d %H:%M:%S",
            "%d/%m/%Y %H:%M:%S",
            "%m/%d/%Y %H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%d-%m-%Y %H:%M",
            "%m-%d-%Y %H:%M",
            "%Y.%m.%d %H:%M",
            "%d.%m.%Y %H:%M",
            "%m.%d.%Y %H:%M",
            "%Y/%m/%d %H:%M",
            "%d/%m/%Y %H:%M",
            "%m/%d/%Y %H:%M",
            "%Y-%m-%d %M:%S",
            "%d-%m-%Y %M:%S",
            "%m-%d-%Y %M:%S",
            "%Y.%m.%d %M:%S",
            "%d.%m.%Y %M:%S",
            "%m.%d.%Y %M:%S",
            "%Y/%m/%d %M:%S",
            "%d/%m/%Y %M:%S",
            "%m/%d/%Y %M:%S",
            "%Y-%m-%d %H",
            "%d-%m-%Y %H",
            "%m-%d-%Y %H",
            "%Y.%m.%d %H",
            "%d.%m.%Y %H",
            "%m.%d.%Y %H",
            "%Y/%m/%d %H",
            "%d/%m/%Y %H",
            "%m/%d/%Y %H",
            "%Y-%m-%d",
            "%d-%m-%Y",
            "%m-%d-%Y",
            "%Y.%m.%d",
            "%d.%m.%Y",
            "%m.%d.%Y",
            "%Y/%m/%d",
            "%d/%m/%Y",
            "%m/%d/%Y",
        ]

        for date_format in formats:
            valid_format = True
            for column in date_columns:
                for date in df[column]:
                    try:
                        datetime.datetime.strptime(date, date_format)
                    except ValueError:
                        valid_format = False
                        break
                if valid_format:
                    return date_format


def data_2_results(data) -> tuple[TimeSeriesScalingModule, partial[[], None]]:
    # test linear approach for day
    scaling = TimeSeriesScalingModule(data.option_number_buildings, data.option_simultaneity_factor)
    detected_format = detect_date_format(data.option_filename)
    if detected_format:
        logging.info(f"Recognized format: {detected_format}")
    else:
        detected_format = ""
        logging.info("No valid format.")
    if data.option_column_load[1] == data.option_column_date[1]:
        logging.exception(f"Error: Load Column == date Column: {data.option_column_load[1]} == {data.option_column_date[1]}")
        raise ValueError(f"Error: Load Column == date Column: {data.option_column_load[1]} == {data.option_column_date[1]}")
    try:
        scaling.data.read_profile_from_csv_with_date(
            data.option_filename,
            data.option_column_load[1],
            data.option_column_date[1],
            date_format=detected_format
            if data.option_date_format[0] == 0
            else "%Y-%m-%d %H:%M:%S"
            if data.option_date_format[0] == 1
            else "%d.%m.%Y %H:%M:%S"
            if data.option_date_format[0] == 2
            else "%m/%d/%Y %H:%M:%S"
            if data.option_date_format[0] == 3
            else data.input_date_format_box,
        )

    except ValueError as err:
        logging.exception("Error:")
        raise err

    if data.aim_average:
        func = partial(scaling.calculate_using_average_values, data.option_period[0] + 1)
        return scaling, func
    if data.aim_normal:
        func = scaling.calculate_using_normal_distribution
        return scaling, func
    scaling.data.read_scaling_profile_from_csv(data.option_scaling_filename, data.option_scaling_column_load[1])
    if data.aim_scaling:
        func = partial(scaling.calculate_using_scaling_profile, data.option_period[0] + 1)
        return scaling, func
    func = scaling.calculate_using_scaling_and_normal_distribution
    return scaling, func


from tssm import TimeSeriesScalingModule


def run(path_list=None):  # pragma: no cover
    import PySide6.QtWidgets as QtW
    from ScenarioGUI import MainWindow, load_config
    from ScenarioGUI.global_settings import FILE_EXTENSION

    load_config("gui_config.ini")

    # init application
    app = QtW.QApplication()
    # init window
    window = QtW.QMainWindow()
    # init gui window
    main_window = MainWindow(window, app, GUI, Translations, result_creating_class=TimeSeriesScalingModule, data_2_results_function=data_2_results)
    # load file if it is in path list
    if path_list is not None:
        main_window.option_filename = (
            [path for path in path_list if path.endswith(f".{FILE_EXTENSION}")][0],
            0,
        )
        main_window.fun_load_known_filename()

    # show window
    window.showMaximized()
    # close app
    sys_exit(app.exec())


if __name__ == "__main__":  # pragma: no cover
    # pass system args like a file to read
    run(argv if len(argv) > 1 else None)
