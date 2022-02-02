import unittest
from unittest import mock

import pandas as pd
from dateutil import tz

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.scripts.load_time_series_from_csv import LoadTimeSeriesFromCsv
from exabel_data_sdk.services.csv_time_series_loader import CsvTimeSeriesLoader
from exabel_data_sdk.util.resource_name_normalization import validate_signal_name

common_args = ["script-name", "--sep", ";", "--api-key", "123"]


class TestUploadTimeSeries(unittest.TestCase):
    def test_one_signal(self):
        data = [["a", "2021-01-01", 1], ["a", "2021-01-02", 2], ["b", "2021-01-01", 3]]

        ts_data = pd.DataFrame(data, columns=["entity", "date", "signal1"])
        CsvTimeSeriesLoader.set_time_index(ts_data)
        time_series = CsvTimeSeriesLoader.get_time_series(ts_data, "signals/acme.")
        pd.testing.assert_series_equal(
            pd.Series(
                [1, 2],
                index=pd.DatetimeIndex(["2021-01-01", "2021-01-02"], tz=tz.tzutc()),
                name="a/signals/acme.signal1",
            ),
            time_series[0],
        )
        pd.testing.assert_series_equal(
            pd.Series(
                [3],
                index=pd.DatetimeIndex(["2021-01-01"], tz=tz.tzutc()),
                name="b/signals/acme.signal1",
            ),
            time_series[1],
        )

    def test_two_signals(self):
        data = [
            ["a", "2021-01-01", 1, 100],
            ["a", "2021-01-02", 2, 200],
            ["b", "2021-01-01", 3, 300],
        ]
        ts_data = pd.DataFrame(data, columns=["entity", "date", "signal1", "signal2"])

        CsvTimeSeriesLoader.set_time_index(ts_data)
        time_series = CsvTimeSeriesLoader.get_time_series(ts_data, "signals/acme.")

        pd.testing.assert_series_equal(
            pd.Series(
                [1, 2],
                index=pd.DatetimeIndex(["2021-01-01", "2021-01-02"], tz=tz.tzutc()),
                name="a/signals/acme.signal1",
            ),
            time_series[0],
        )
        pd.testing.assert_series_equal(
            pd.Series(
                [100, 200],
                index=pd.DatetimeIndex(["2021-01-01", "2021-01-02"], tz=tz.tzutc()),
                name="a/signals/acme.signal2",
            ),
            time_series[1],
        )
        pd.testing.assert_series_equal(
            pd.Series(
                [3],
                index=pd.DatetimeIndex(["2021-01-01"], tz=tz.tzutc()),
                name="b/signals/acme.signal1",
            ),
            time_series[2],
        )
        pd.testing.assert_series_equal(
            pd.Series(
                [300],
                index=pd.DatetimeIndex(["2021-01-01"], tz=tz.tzutc()),
                name="b/signals/acme.signal2",
            ),
            time_series[3],
        )

    def test_read_file_without_pit(self):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/timeseries.csv",
            "--namespace",
            "",
        ]
        script = LoadTimeSeriesFromCsv(args)
        client = mock.create_autospec(ExabelClient(host="host", api_key="123"))
        with self.assertRaises(SystemExit):
            script.run_script(client, script.parse_arguments())

    def test_read_file_use_header_for_signal(self):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/timeseries.csv",
            "--namespace",
            "",
            "--pit-current-time",
        ]

        script = LoadTimeSeriesFromCsv(args)
        client = mock.create_autospec(ExabelClient(host="host", api_key="123"))
        script.run_script(client, script.parse_arguments())

        call_args_list = client.time_series_api.bulk_upsert_time_series.call_args_list
        self.assertEqual(1, len(call_args_list))
        series = call_args_list[0][0][0]
        self.assertEqual(2, len(series))

        pd.testing.assert_series_equal(
            pd.Series(
                range(1, 6),
                pd.date_range("2021-01-01", periods=5, tz=tz.tzutc()),
                name="entityTypes/company/entities/company_A/signals/signal1",
            ),
            series[0],
            check_freq=False,
        )
        pd.testing.assert_series_equal(
            pd.Series(
                [4, 5],
                pd.DatetimeIndex(["2021-01-01", "2021-01-03"], tz=tz.tzutc()),
                name="entityTypes/company/entities/company_B/signals/signal1",
            ),
            series[1],
            check_freq=False,
        )

    def test_read_file_with_multiple_signals(self):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/timeseries_multiple_signals.csv",
            "--namespace",
            "acme",
            "--pit-offset",
            "0",
        ]
        script = LoadTimeSeriesFromCsv(args)
        client = mock.create_autospec(ExabelClient(host="host", api_key="123"))
        script.run_script(client, script.parse_arguments())

        call_args_list = client.time_series_api.bulk_upsert_time_series.call_args_list
        self.assertEqual(1, len(call_args_list))
        series = call_args_list[0][0][0]
        self.assertEqual(4, len(series))
        pd.testing.assert_series_equal(
            pd.Series(
                [1, 2],
                pd.DatetimeIndex(["2021-01-01", "2021-01-02"], tz=tz.tzutc()),
                name="entityTypes/company/entities/company_A/signals/acme.signal1",
            ),
            series[0],
        )
        pd.testing.assert_series_equal(
            pd.Series(
                [10, 20],
                pd.DatetimeIndex(["2021-01-01", "2021-01-02"], tz=tz.tzutc()),
                name="entityTypes/company/entities/company_A/signals/acme.signal2",
            ),
            series[1],
        )
        pd.testing.assert_series_equal(
            pd.Series(
                [4, 5],
                pd.DatetimeIndex(["2021-01-01", "2021-01-03"], tz=tz.tzutc()),
                name="entityTypes/company/entities/company_B/signals/acme.signal1",
            ),
            series[2],
        )
        pd.testing.assert_series_equal(
            pd.Series(
                [40, 50],
                pd.DatetimeIndex(["2021-01-01", "2021-01-03"], tz=tz.tzutc()),
                name="entityTypes/company/entities/company_B/signals/acme.signal2",
            ),
            series[3],
        )

    def test_read_file_with_known_time(self):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/timeseries_known_time.csv",
            "--namespace",
            "acme",
        ]
        script = LoadTimeSeriesFromCsv(args)
        client = mock.create_autospec(ExabelClient(host="host", api_key="123"))
        script.run_script(client, script.parse_arguments())

        call_args_list = client.time_series_api.bulk_upsert_time_series.call_args_list
        self.assertEqual(1, len(call_args_list))
        series = call_args_list[0][0][0]
        self.assertEqual(4, len(series))

        index_A = pd.MultiIndex.from_arrays(
            [
                pd.DatetimeIndex(["2021-01-01", "2021-01-02"], tz=tz.tzutc()),
                pd.DatetimeIndex(["2021-01-01", "2021-01-05"], tz=tz.tzutc()),
            ]
        )
        index_B = pd.MultiIndex.from_arrays(
            [
                pd.DatetimeIndex(["2021-01-01", "2021-01-03"], tz=tz.tzutc()),
                pd.DatetimeIndex(["2021-01-10", "2019-12-31"], tz=tz.tzutc()),
            ]
        )
        pd.testing.assert_series_equal(
            pd.Series(
                [1, 2],
                index_A,
                name="entityTypes/company/entities/company_A/signals/acme.signal1",
            ),
            series[0],
        )
        pd.testing.assert_series_equal(
            pd.Series(
                [10, 20],
                index_A,
                name="entityTypes/company/entities/company_A/signals/acme.signal2",
            ),
            series[1],
        )
        pd.testing.assert_series_equal(
            pd.Series(
                [4, 5],
                index_B,
                name="entityTypes/company/entities/company_B/signals/acme.signal1",
            ),
            series[2],
        )
        pd.testing.assert_series_equal(
            pd.Series(
                [40, 50],
                index_B,
                name="entityTypes/company/entities/company_B/signals/acme.signal2",
            ),
            series[3],
        )

    def test_read_file_with_integer_identifiers(self):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/timeseries_with_integer_identifiers.csv",
            "--namespace",
            "acme",
            "--pit-offset",
            "30",
        ]

        script = LoadTimeSeriesFromCsv(args)
        client = mock.create_autospec(ExabelClient(host="host", api_key="123"))
        script.run_script(client, script.parse_arguments())

        call_args_list = client.time_series_api.bulk_upsert_time_series.call_args_list
        self.assertEqual(1, len(call_args_list))
        series = call_args_list[0][0][0]
        self.assertEqual(2, len(series))

        pd.testing.assert_series_equal(
            pd.Series(
                range(1, 6),
                pd.date_range("2021-01-01", periods=5, tz=tz.tzutc()),
                name="entityTypes/brand/entities/acme.0001/signals/acme.signal1",
            ),
            series[0],
            check_freq=False,
        )
        pd.testing.assert_series_equal(
            pd.Series(
                [4, 5],
                pd.DatetimeIndex(["2021-01-01", "2021-01-03"], tz=tz.tzutc()),
                name="entityTypes/brand/entities/acme.0002/signals/acme.signal1",
            ),
            series[1],
            check_freq=False,
        )

    def test_should_fail_with_invalid_signal_names(self):
        signals_errors = {
            "0_starts_with_0": "Signal name must start with a letter, "
            'contain only letters, numbers, and underscores, but got "0_starts_with_0"',
            "contains_!llegal_chars": "Signal name must start with a letter, "
            'contain only letters, numbers, and underscores, but got "contains_!llegal_chars"',
            "": "Signal name cannot be empty",
            "signal_with_sixty_five_characters_in_length_which_more_than_max__": "Signal name "
            "cannot be longer than 64 characters, but got "
            '"signal_with_sixty_five_characters_in_length_which_more_than_max__"',
        }

        for signal, error in signals_errors.items():
            with self.assertRaises(ValueError) as cm:
                validate_signal_name(signal)
            self.assertEqual(str(cm.exception), error)

    def test_valid_signal_names(self):
        valid_signals = [
            "signal",
            "SIGNAL",
            "signal_with_underscores",
            "signal_1_with_underscores_and_numbers",
            "signal_with_sixty_four_characters_in_length_which_is_the_maximum",
        ]

        for signal in valid_signals:
            validate_signal_name(signal)

    def test_should_fail_with_invalid_data_points(self):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/time_series_with_invalid_data_points.csv",
            "--namespace",
            "acme",
        ]

        script = LoadTimeSeriesFromCsv(args)
        client = mock.create_autospec(ExabelClient(host="host", api_key="123"))
        with self.assertRaises(SystemExit):
            script.run_script(client, script.parse_arguments())

    def test_valid_no_create_tag(self):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/timeseries_known_time.csv",
            "--namespace",
            "acme",
            "--no-create-tag",
        ]
        script = LoadTimeSeriesFromCsv(args)
        client = mock.create_autospec(ExabelClient(host="host", api_key="123"))
        script.run_script(client, script.parse_arguments())

        call_args_list = client.time_series_api.bulk_upsert_time_series.call_args_list
        create_tag_status = call_args_list[0][1]["create_tag"]
        self.assertEqual(False, create_tag_status)

    def test_valid_create_tag(self):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/timeseries_known_time.csv",
            "--namespace",
            "acme",
        ]
        script = LoadTimeSeriesFromCsv(args)
        client = mock.create_autospec(ExabelClient(host="host", api_key="123"))
        script.run_script(client, script.parse_arguments())

        call_args_list = client.time_series_api.bulk_upsert_time_series.call_args_list
        create_tag_status = call_args_list[0][1]["create_tag"]
        self.assertEqual(True, create_tag_status)

    def test_valid_no_create_library_signal(self):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/timeseries_known_time.csv",
            "--namespace",
            "acme",
            "--create-missing-signals",
            "--no-create-library-signal",
        ]
        script = LoadTimeSeriesFromCsv(args)
        client = mock.create_autospec(ExabelClient(host="host", api_key="123"))
        client.signal_api.get_signal.return_value = None
        script.run_script(client, script.parse_arguments())

        call_args_list = client.signal_api.create_signal.call_args_list
        create_library_signal_status = call_args_list[0][1]["create_library_signal"]
        self.assertEqual(False, create_library_signal_status)

    def test_valid_create_library_signal(self):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/timeseries_known_time.csv",
            "--namespace",
            "acme",
            "--create-missing-signals",
        ]
        script = LoadTimeSeriesFromCsv(args)
        client = mock.create_autospec(ExabelClient(host="host", api_key="123"))
        client.signal_api.get_signal.return_value = None
        script.run_script(client, script.parse_arguments())

        call_args_list = client.signal_api.create_signal.call_args_list
        create_library_signal_status = call_args_list[0][1]["create_library_signal"]
        self.assertEqual(True, create_library_signal_status)


if __name__ == "__main__":
    unittest.main()
