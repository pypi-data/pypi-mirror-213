from tssm.gui.start_gui import detect_date_format


def test_date_format_check():
    data = [("example_file1", "%Y-%m-%d %H:%M:%S"),
            ("example_file2", "%d-%m-%Y %H:%M:%S"),
            ("example_file3", "%m-%d-%Y %H:%M:%S"),
            ("example_file4", "%Y.%m.%d %H:%M:%S"),
            ("example_file5", "%d.%m.%Y %H:%M:%S"),
            ("example_file6", "%m.%d.%Y %H:%M:%S"),
            ("example_file7", "%Y/%m/%d %H:%M:%S"),
            ("example_file8", "%d/%m/%Y %H:%M:%S"),
            ("example_file9", "%m/%d/%Y %H:%M:%S"),

            ("example_file10", "%Y-%m-%d %H:%M"),
            ("example_file11", "%d-%m-%Y %H:%M"),
            ("example_file12", "%m-%d-%Y %H:%M"),
            ("example_file13", "%Y.%m.%d %H:%M"),
            ("example_file14", "%d.%m.%Y %H:%M"),
            ("example_file15", "%m.%d.%Y %H:%M"),
            ("example_file16", "%Y/%m/%d %H:%M"),
            ("example_file17", "%d/%m/%Y %H:%M"),
            ("example_file18", "%m/%d/%Y %H:%M"),

            ("example_file19", "%Y-%m-%d %H"),
            ("example_file20", "%d-%m-%Y %H"),
            ("example_file21", "%m-%d-%Y %H"),
            ("example_file22", "%Y.%m.%d %H"),
            ("example_file23", "%d.%m.%Y %H"),
            ("example_file24", "%m.%d.%Y %H"),
            ("example_file25", "%Y/%m/%d %H"),
            ("example_file26", "%d/%m/%Y %H"),
            ("example_file27", "%m/%d/%Y %H"),

            ("example_file28", "%Y-%m-%d %M:%S"),
            ("example_file29", "%d-%m-%Y %M:%S"),
            ("example_file30", "%m-%d-%Y %M:%S"),
            ("example_file31", "%Y.%m.%d %M:%S"),
            ("example_file32", "%d.%m.%Y %M:%S"),
            ("example_file33", "%m.%d.%Y %M:%S"),
            ("example_file34", "%Y/%m/%d %M:%S"),
            ("example_file35", "%d/%m/%Y %M:%S"),
            ("example_file36", "%m/%d/%Y %M:%S"),

            ("example_file37", "%Y-%m-%d"),
            ("example_file38", "%d-%m-%Y"),
            ("example_file39", "%m-%d-%Y"),
            ("example_file40", "%Y.%m.%d"),
            ("example_file41", "%d.%m.%Y"),
            ("example_file42", "%m.%d.%Y"),
            ("example_file43", "%Y/%m/%d"),
            ("example_file44", "%d/%m/%Y"),
            ("example_file45", "%m/%d/%Y")
            ]
    for file, date_format in data:
        res = detect_date_format(f"test_data/profiles/example_data_profiles_15_min/{file}.csv")
        assert res == date_format
