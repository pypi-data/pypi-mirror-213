class Translations:  # pragma: no cover
    __slots__ = (
        "action_add_scenario",
        "action_delete_scenario",
        "action_new",
        "action_open",
        "action_rename_scenario",
        "action_save",
        "action_save_as",
        "action_start_multiple",
        "action_update_scenario",
        "aim_average",
        "aim_normal",
        "aim_normal_and_scaling",
        "aim_scaling",
        "button_rename_scenario",
        "Calculation_Finished",
        "cat_no_result",
        "category_data",
        "category_general",
        "category_language",
        "category_save_scenario",
        "category_scaling_profile",
        "choose_load",
        "figure_results",
        "hint_saving",
        "icon",
        "input_date_format_box",
        "label_abort",
        "label_cancel",
        "label_CancelText",
        "label_CancelTitle",
        "label_close",
        "label_Language",
        "label_Language_Head",
        "label_LeaveScenario",
        "label_LeaveScenarioText",
        "label_New",
        "label_new_scenario",
        "label_next",
        "label_okay",
        "label_Open",
        "label_previous",
        "label_Save",
        "label_Save_As",
        "label_status",
        "label_StayScenario",
        "legend_figure",
        "Load",
        "menu_calculation",
        "menu_file",
        "menu_language",
        "menu_scenario",
        "menu_settings",
        "new_name",
        "no_backup_file",
        "no_file_selected",
        "no_solution",
        "not_calculated",
        "numerical_results",
        "option_auto_saving",
        "option_column_date",
        "option_column_load",
        "option_date_format",
        "option_decimal_csv",
        "option_filename",
        "option_font_size",
        "option_language",
        "option_n_threads",
        "option_number_buildings",
        "option_period",
        "option_scale",
        "option_scaling_column_load",
        "option_scaling_decimal_csv",
        "option_scaling_filename",
        "option_scaling_loadline",
        "option_scaling_seperator_csv",
        "option_seperator_csv",
        "option_simultaneity_factor",
        "option_toggle_buttons",
        "original_max",
        "page_aim",
        "page_inputs",
        "page_result",
        "page_settings",
        "push_button_add_scenario",
        "push_button_cancel",
        "push_button_delete_scenario",
        "push_button_save_scenario",
        "push_button_start_multiple",
        "Save",
        "SaveFigure",
        "scaled_figure",
        "scenarioString",
        "short_cut",
        "text_no_result",
        "tool_imported",
        "languages",
    )

    def __init__(self):
        self.languages: list[str] = ["English", "German"]
        self.action_add_scenario: list[str] = ["Add scenario", "Szenario hinzufügen"]
        self.action_delete_scenario: list[str] = ["Delete scenario", "Szenario löschen"]
        self.action_new: list[str] = ["New Project", "Neues Projekt"]
        self.action_open: list[str] = ["Open Project", "Öffne Projekt"]
        self.action_rename_scenario: list[str] = ["Rename scenario", "Szenario umbenennen"]
        self.action_save: list[str] = ["Save Project", "Speichere Projekt"]
        self.action_save_as: list[str] = ["Save as", "Speichere Projekt unter ..."]
        self.action_start_multiple: list[str] = ["Calculate all scenarios", "Berechne alle Szenarios"]
        self.action_update_scenario: list[str] = ["Update scenario", "Szenario aktualisieren"]
        self.aim_average: list[str] = ["Average", "Durchschnitt"]
        self.aim_normal: list[str] = ["Normal distribution", "Normalverteilung"]
        self.aim_normal_and_scaling: list[str] = ["Normal distribution and scaling", "Normalverteilung und Skalierung"]
        self.aim_scaling: list[str] = ["Scaling profile", "Skalierungsprofil"]
        self.button_rename_scenario: list[str] = ["Rename scenario", "Szenario umbenennen"]
        self.Calculation_Finished: list[str] = ["Calculation finished", "Berechnung fertiggestellt"]
        self.cat_no_result: list[str] = ["No results", "Keine Ergebnisse"]
        self.category_data: list[str] = ["Original data", "Originaldaten"]
        self.category_general: list[str] = ["Inputs", "Eingaben"]
        self.category_language: list[str] = ["Language: ", "Sprache: "]
        self.category_save_scenario: list[str] = ["Scenario settings", "Szenarioeinstellungen"]
        self.category_scaling_profile: list[str] = ["Scaling profile", "Skalierungsprofil"]
        self.choose_load: list[str] = ["Choose file to load scenarios", "Wählen Sie Datei zum Laden von Szenarien"]
        self.figure_results: list[str] = ["Plot,Time,Power", "Graph,Zeit,Leistung"]
        self.hint_saving: list[str] = [
            "If Auto saving is selected the scenario will automatically saved if a scenario is changed. Otherwise the scenario has to be saved with the Update scenario button in the upper left corner if the changes should not be lost.",
            "Wenn Automatisch speichern ausgewählt ist, wird das Szenario automatisch gespeichert, wenn ein Szenario geändert wird. Andernfalls muss das Szenario mit der Schaltfläche Szenario aktualisieren in der oberen linken Ecke gespeichert werden, wenn die Änderungen nicht verloren gehen sollen.",
        ]
        self.icon: list[str] = ["Flag_English.svg", "Flag_German.svg"]
        self.input_date_format_box: list[str] = ["Date format box", "Datumsformatfeld"]
        self.label_abort: list[str] = ["Abort ", "Abbruch "]
        self.label_cancel: list[str] = ["Cancel", "Abbrechen"]
        self.label_CancelText: list[str] = [
            "Are you sure you want to quit? Any unsaved work will be lost.",
            "Bist du sicher das Programm zu schließen? Alle ungesicherten Änderungen gehen sonst verloren.",
        ]
        self.label_CancelTitle: list[str] = ["Warning", "Warnung"]
        self.label_close: list[str] = ["Close", "Schließen"]
        self.label_Language: list[str] = ["Language: ", "Sprache: "]
        self.label_Language_Head: list[str] = ["Language", "Sprache"]
        self.label_LeaveScenario: list[str] = ["Leave scenario", "Szenario verlassen"]
        self.label_LeaveScenarioText: list[str] = [
            "Are you sure you want to leave scenario? Any unsaved work will be lost.",
            "Bist du sicher das Szenario zu verlasen? Alle ungesicherten Änderungen gehen sonst verloren.",
        ]
        self.label_New: list[str] = ["New Project", "Neues Projekt"]
        self.label_new_scenario: list[str] = ["Enter new scenario name", "Neuer Name für das Szenario"]
        self.label_next: list[str] = ["next", "nächstes"]
        self.label_okay: list[str] = ["Okay ", "Okay "]
        self.label_Open: list[str] = ["Open Project", "Öffne Projekt"]
        self.label_previous: list[str] = ["previous", "vorheriges"]
        self.label_Save: list[str] = ["Save Project", "Speichere Projekt"]
        self.label_Save_As: list[str] = ["Save as", "Speichere Projekt unter ..."]
        self.label_status: list[str] = ["Progress: ", "Fortschritt: "]
        self.label_StayScenario: list[str] = ["Stay by scenario", "Beim Szenario bleiben"]
        self.legend_figure: list[str] = ["Legend on", "Legende zu"]
        self.Load: list[str] = ["Choose file to load scenarios", "Wählen Sie die Datei zum Laden von Szenarien"]
        self.menu_calculation: list[str] = ["Calculation", "Berechnung"]
        self.menu_file: list[str] = ["File", "Datei"]
        self.menu_language: list[str] = ["Language", "Sprache"]
        self.menu_scenario: list[str] = ["Scenario", "Szenario"]
        self.menu_settings: list[str] = ["Settings", "Einstellungen"]
        self.new_name: list[str] = ["New name for ", "Neuer Name für "]
        self.no_backup_file: list[str] = ["no backup fileImport", "Keine Sicherungsdatei gefunden"]
        self.no_file_selected: list[str] = ["No file selected.", "Keine Datei ausgewählt."]
        self.no_solution: list[str] = ["No Solution found", "Keine Lösung gefunden"]
        self.not_calculated: list[str] = ["Not calculated", "Noch nicht berechnet"]
        self.numerical_results: list[str] = ["Numerical results", "Numerische Ergebnisse"]
        self.option_auto_saving: list[str] = ["Use automatic saving?, No , Yes ", "Automatisches speichern nutzen?, Nein, Ja"]
        self.option_column_date: list[str] = ["Date line: ", "Datumszeile: "]
        self.option_column_load: list[str] = ["Load line: ", "Lastprofil: "]
        self.option_date_format: list[str] = ["Date format", "Format des Datums"]
        self.option_decimal_csv: list[str] = ['Decimal sign in CSV-file:, Point "." , Comma "++"', 'Dezimalzeichen in der CSV-Datei:, Punkt "." , Komma "++"']
        self.option_filename: list[str] = ["Filename", "Dateiname"]
        self.option_font_size: list[str] = ["Font Size", "Schriftgröße"]
        self.option_language: list[str] = [
            "Language:,English,German,Dutch,Italian,French,Spanish,Galician",
            "Sprache:,English,German,Dutch,Italian,French,Spanish,Galician",
        ]
        self.option_n_threads: list[str] = ["Number of parallel threads [-]: ", "Anzahl an parallelen Prozessen [-]:"]
        self.option_number_buildings: list[str] = ["Number of buildings [-]:", "Anzahl der Gebäude [-]:"]
        self.option_period: list[str] = [
            "Period, yearly , monthly , weekly , daily , hourly , hourly and monthly",
            "Periode, jährlich , monatlich , wöchentlich , täglich , stündlich , stündlich und monatlich",
        ]
        self.option_scale: list[str] = ["Scale profile to same yearly sum?:, Yes , No", "Profil auf denselben Jahresbetrag skalieren?:, Ja , Nein"]
        self.option_scaling_column_load: list[str] = ["Load line: ", "Lastprofil: "]
        self.option_scaling_decimal_csv: list[str] = [
            'Decimal sign in CSV-file:, Point "." , Comma ","',
            'Dezimalzeichen in der CSV-Datei:, Punkt "." , Komma ","',
        ]
        self.option_scaling_filename: list[str] = ["Filename:", "Dateiname:"]
        self.option_scaling_loadline: list[str] = ["Load line", "Lastprofil"]
        self.option_scaling_seperator_csv: list[str] = [
            'Seperator in CSV-file:, Semicolon ";" , Comma "++", Automatic',
            'Trennzeichen in der CSV-Datei:, Semikolon ";" , Komma "++", Automatisch',
        ]
        self.option_seperator_csv: list[str] = [
            'Seperator in CSV-file:, Semicolon ";" , Comma "++", Automatic',
            'Trennzeichen in der CSV-Datei:, Semikolon ";" , Komma "++", Automatisch',
        ]
        self.option_simultaneity_factor: list[str] = ["Simultaneity factor [-]", "Gleichzeitigkeitsfaktor [-]"]
        self.option_toggle_buttons: list[str] = ["Use toggle buttons?:, no , yes ", "Umschalterbutton?:, Nein , Ja "]
        self.original_max: list[str] = ["Show around which maximal value?", "Um welchen Maximalwert herum zeigen?"]
        self.page_aim: list[str] = ["Aim of @simulation,Aim of simulation", "Ziel der @Simulation,Ziel der Simulation"]
        self.page_inputs: list[str] = ["Inputs,Inputs", "Eingaben,Eingabe"]
        self.page_result: list[str] = ["Results,Results", "Ergebnisse,Ergebnisse"]
        self.page_settings: list[str] = ["Settings,Settings", "Einstellungen,Einstellungen"]
        self.push_button_add_scenario: list[str] = ["Add scenario", "Szenario hinzufügen"]
        self.push_button_cancel: list[str] = ["Exit", "Verlassen"]
        self.push_button_delete_scenario: list[str] = ["Delete scenario", "Szenario löschen"]
        self.push_button_save_scenario: list[str] = ["Update scenario", "Szenario aktualisieren"]
        self.push_button_start_multiple: list[str] = ["Calculate all scenarios", "Berechne alle Szenarios"]
        self.Save: list[str] = ["Choose file location to save scenarios", "Wählen Sie den Dateispeicherort zum Speichern von Szenarien"]
        self.SaveFigure: list[str] = ["Choose png location to save figure", "Wählen Sie einen png-Speicherort für die Abbildung"]
        self.scaled_figure: list[str] = ["Scaled values?", "Skalierte Werte?"]
        self.scenarioString: list[str] = ["Scenario", "Szenario"]
        self.short_cut: list[str] = ["Ctrl+Alt+E", "Ctrl+Alt+G"]
        self.text_no_result: list[str] = ["No results are yet calculated", "Es wurden noch keine Ergebnisse berechnet"]
        self.tool_imported: list[str] = ["scenario gui imported", "scenario gui importiert"]
