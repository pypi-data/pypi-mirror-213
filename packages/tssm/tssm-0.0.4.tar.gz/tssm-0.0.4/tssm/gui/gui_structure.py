from __future__ import annotations

from functools import partial
from pathlib import Path
from typing import TYPE_CHECKING
from pandas import DataFrame as pd_DataFrame
from pandas import read_csv as pd_read_csv
from ScenarioGUI.gui_classes.gui_structure import GuiStructure
from ScenarioGUI.gui_classes.gui_structure_classes import (
    Aim,
    ButtonBox,
    Category,
    FigureOption,
    FileNameBox,
    FloatBox,
    IntBox,
    ListBox,
    Page,
    ResultFigure,
    ResultText,
    TextBox,
)
from detect_delimiter import detect

if TYPE_CHECKING:
    import PySide6.QtWidgets as QtW

    from tssm.gui.translation_class import Translations


class GUI(GuiStructure):
    def __init__(self, default_parent: QtW.QWidget, translations: Translations):
        super().__init__(default_parent, translations)
        self.page_aim = Page(name=translations.page_aim, button_name="Aim", icon="Aim_Inv.svg")
        self.aim_average = Aim(label=translations.aim_average, icon="average", page=self.page_aim)
        self.aim_scaling = Aim(label=translations.aim_scaling, icon="Parameters", page=self.page_aim)
        self.aim_normal = Aim(label=translations.aim_normal, icon="normal", page=self.page_aim)
        self.aim_normal_and_scaling = Aim(label=translations.aim_normal_and_scaling, icon="normal_scaling", page=self.page_aim)
        self.page_inputs = Page(name=translations.page_inputs, button_name="Input", icon="Options.svg")

        self.category_general = Category(page=self.page_inputs, label=translations.category_general)
        self.option_number_buildings = IntBox(
            label=translations.option_number_buildings,
            default_value=2,
            minimal_value=0,
            maximal_value=2_000_000_000,
            step=1,
            category=self.category_general,
        )

        self.option_simultaneity_factor = FloatBox(
            label=translations.option_simultaneity_factor,
            default_value=0.84,
            minimal_value=0,
            maximal_value=10,
            decimal_number=4,
            step=0.05,
            category=self.category_general,
        )

        self.option_period = ListBox(
            label=translations.option_period,
            default_index=0,
            category=self.category_general,
            entries=["yearly", "monthly", "weekly", "daily", "hourly", "hourly and monthly"],
        )
        self.aim_average.add_link_2_show(self.option_period)
        self.aim_scaling.add_link_2_show(self.option_period)
        self.aim_normal_and_scaling.add_link_2_show(self.option_period)

        self.category_data = Category(page=self.page_inputs, label=translations.category_data)

        self.option_seperator_csv = ButtonBox(
            label=translations.option_seperator_csv, default_index=1, entries=['Semicolon ";"', 'Comma ","', "Automatic"], category=self.category_data
        )
        self.option_decimal_csv = ButtonBox(
            label=translations.option_decimal_csv, default_index=0, entries=['Point "."', 'Comma ","'], category=self.category_data
        )
        folder: Path = Path(__file__).parent.parent.parent
        file = f'{folder.joinpath("./examples/data.csv")}'

        # self.option_date_format = TextBox(category=self.category_data, label="Date format", default_text="%Y-%m-%d %H:%M:%S")
        self.option_date_format = ListBox(
            label=translations.option_date_format,
            default_index=0,
            entries=["Automatic", "2020-12-31 23:59:59", "31.12.2020 23:59:59", "12/31/2020 23:59:59", "Input"],
            category=self.category_data,
        )

        self.option_date_format.change_event(self.on_date_format_changed)  # ed.connect(self.on_date_format_changed)

        self.input_date_format_box = TextBox(category=self.category_data, label=translations.input_date_format_box, default_text="...")
        """:param date_format: date time format if necessary (default YYYY-MM-DD hh:mm:ss)
        Link for date format https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior"""
        self.input_date_format_box.set_value("...")

        self.option_filename = FileNameBox(
            label=translations.option_filename,
            default_value=file,
            category=self.category_data,
            dialog_text="please select a csv file",
            error_text="no file found",
        )

        self.option_column_date = ListBox(category=self.category_data, label=translations.option_column_date, default_index=0, entries=[])
        self.option_column_load = ListBox(category=self.category_data, label=translations.option_column_load, default_index=0, entries=[])

        # add change events
        self.option_seperator_csv.change_event(
            partial(
                self.fun_update_combo_box_data_file,
                option_filename=self.option_filename,
                option_seperator=self.option_seperator_csv,
                option_decimal=self.option_decimal_csv,
                options_columns=[self.option_column_load, self.option_column_date],
            )
        )
        self.option_decimal_csv.change_event(
            partial(
                self.fun_update_combo_box_data_file,
                option_filename=self.option_filename,
                option_seperator=self.option_seperator_csv,
                option_decimal=self.option_decimal_csv,
                options_columns=[self.option_column_load, self.option_column_date],
            )
        )
        self.option_filename.change_event(
            partial(
                self.fun_update_combo_box_data_file,
                option_filename=self.option_filename,
                option_seperator=self.option_seperator_csv,
                option_decimal=self.option_decimal_csv,
                options_columns=[self.option_column_load, self.option_column_date],
            )
        )

        self.category_scaling_profile = Category(page=self.page_inputs, label=translations.category_scaling_profile)

        self.option_scale = ButtonBox(label=translations.option_scale, default_index=0, entries=["Yes", "No"], category=self.category_scaling_profile)

        self.option_scaling_seperator_csv = ButtonBox(
            label=translations.option_scaling_seperator_csv,
            default_index=1,
            entries=['Semicolon ";"', 'Comma ","', "Automatic"],
            category=self.category_scaling_profile,
        )

        self.option_scaling_decimal_csv = ButtonBox(
            label=translations.option_scaling_decimal_csv, default_index=0, entries=['Point "."', 'Comma ","'], category=self.category_scaling_profile
        )
        folder: Path = Path(__file__).parent.parent.parent
        file = f'{folder.joinpath("./examples/data.csv")}'
        self.option_scaling_filename = FileNameBox(
            label=translations.option_scaling_filename,
            default_value=file,
            category=self.category_scaling_profile,
            dialog_text="please select a csv file",
            error_text="no file found",
        )

        self.option_scaling_column_load = ListBox(
            category=self.category_scaling_profile, label=translations.option_scaling_column_load, default_index=0, entries=[]
        )

        self.option_scaling_seperator_csv.change_event(
            partial(
                self.fun_update_combo_box_data_file,
                option_filename=self.option_scaling_filename,
                option_seperator=self.option_scaling_seperator_csv,
                option_decimal=self.option_scaling_decimal_csv,
                options_columns=[self.option_scaling_column_load],
            )
        )
        self.option_scaling_decimal_csv.change_event(
            partial(
                self.fun_update_combo_box_data_file,
                option_filename=self.option_scaling_filename,
                option_seperator=self.option_scaling_seperator_csv,
                option_decimal=self.option_scaling_decimal_csv,
                options_columns=[self.option_scaling_column_load],
            )
        )
        self.option_scaling_filename.change_event(
            partial(
                self.fun_update_combo_box_data_file,
                option_filename=self.option_scaling_filename,
                option_seperator=self.option_scaling_seperator_csv,
                option_decimal=self.option_scaling_decimal_csv,
                options_columns=[self.option_scaling_column_load],
            )
        )
        self.aim_scaling.add_link_2_show(self.category_scaling_profile)
        self.aim_normal_and_scaling.add_link_2_show(self.category_scaling_profile)

        self.create_results_page()
        self.numerical_results = Category(page=self.page_result, label="Numerical results")

        self.result_text_variance = ResultText("Variance", category=self.numerical_results, prefix="Variance: ", suffix="")
        self.result_text_variance.text_to_be_shown("ResultsClass", "get_factor")
        self.result_text_variance.function_to_convert_to_text(lambda x: round(x, 2))

        self.figure_results = ResultFigure(label=self.translations.figure_results, page=self.page_result)
        self.legend_figure = FigureOption(
            category=self.figure_results, label="Legend on", param="legend", default=0, entries=["No", "Yes"], entries_values=[False, True]
        )
        self.scaled_figure = FigureOption(
            category=self.figure_results, label="Scaled values?", param="scaled", default=0, entries=["No", "Yes"], entries_values=[False, True]
        )
        self.original_max = FigureOption(
            category=self.figure_results,
            label="Show around which maximal value?",
            param="max_original",
            default=1,
            entries=["new", "original"],
            entries_values=[False, True],
        )

        self.aim_normal.add_link_2_show(self.original_max)
        self.aim_normal_and_scaling.add_link_2_show(self.original_max)

        self.figure_results.fig_to_be_shown(class_name="TimeSeriesScalingModule", function_name="plot_values")

        self.aim_normal.add_link_2_show(self.result_text_variance)
        self.aim_normal_and_scaling.add_link_2_show(self.result_text_variance)
        self.aim_average.add_link_2_show(self.figure_results)
        self.aim_normal.add_link_2_show(self.figure_results)
        self.aim_scaling.add_link_2_show(self.figure_results)
        self.aim_normal_and_scaling.add_link_2_show(self.figure_results)

        self.create_settings_page()
        self.create_lists()
        self.page_inputs.set_next_page(self.page_result)
        self.page_result.set_previous_page(self.page_inputs)
        self.page_result.set_next_page(self.page_settings)
        self.page_settings.set_previous_page(self.page_result)

    def on_date_format_changed(self, text):
        text = self.option_date_format.get_value()[1]
        if text == "Input":
            self.input_date_format_box.set_value("...")
            self.input_date_format_box.show()
        else:
            self.input_date_format_box.hide()

    def fun_update_combo_box_data_file(
        self, *args, option_filename: FileNameBox, option_seperator: ButtonBox, option_decimal: ButtonBox, options_columns: list[ListBox]
    ) -> None:
        """
        This function updates the combo box of the file selector when a new file is selected.

        Parameters
        ----------
        filename : str
            Location of the file

        Returns
        -------
        None
        """
        filename = option_filename.get_value()

        with open(filename) as f:
            firstline = f.readline()
            delimiter = detect(firstline)

        # get decimal and column seperator
        sep: str = ";" if option_seperator.get_value() == 0 else "," if option_seperator.get_value() == 1 else delimiter
        dec: str = "." if option_decimal.get_value() == 0 else ","
        # try to read CSV-File
        try:
            data: pd_DataFrame = pd_read_csv(filename, sep=sep, decimal=dec)
        except FileNotFoundError:
            self.status_bar.showMessage(self.no_file_selected, 5000)
            return
        except PermissionError:  # pragma: no cover
            self.status_bar.showMessage(self.no_file_selected, 5000)
            return

        # get data column names to set them to comboBoxes
        columns = data.columns
        # clear comboBoxes and add column names
        for list_box in options_columns:
            idx = list_box.get_value()[0]
            list_box.widget.clear()
            list_box.widget.addItems(columns)
            if len(columns) > idx:
                list_box.set_value(idx)
