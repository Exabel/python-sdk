import sys
import unittest
from unittest import mock

import pandas as pd
from dateutil import tz

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.scripts.load_time_series_from_csv import LoadTimeSeriesFromCsv
from exabel_data_sdk.util.resource_name_normalization import validate_signal_name

common_args = ["script-name", "--sep", ";", "--api-key", "123"]


class TestUploadTimeSeries(unittest.TestCase):
    def test_one_signal(self):
        loader = LoadTimeSeriesFromCsv(sys.argv, "Load")
        data = [["a", "2021-01-01", 1], ["a", "2021-01-02", 2], ["b", "2021-01-01", 3]]

        data_frame = pd.DataFrame(data, columns=["entity", "date", "signal1"])

        time_series = loader.get_time_series(data_frame, "signals/acme.")
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
        loader = LoadTimeSeriesFromCsv(sys.argv, "Load")

        data = [
            ["a", "2021-01-01", 1, 100],
            ["a", "2021-01-02", 2, 200],
            ["b", "2021-01-01", 3, 300],
        ]
        data_frame = pd.DataFrame(data, columns=["entity", "date", "signal1", "signal2"])

        time_series = loader.get_time_series(data_frame, "signals/acme.")

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

    def test_read_file_use_header_for_signal(self):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/timeseries.csv",
            "--namespace",
            "",
        ]

        script = LoadTimeSeriesFromCsv(args, "LoadTest1")
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
        ]
        script = LoadTimeSeriesFromCsv(args, "LoadTest3")
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

    def test_read_file_with_integer_identifiers(self):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/timeseries_with_integer_identifiers.csv",
            "--namespace",
            "acme",
        ]

        script = LoadTimeSeriesFromCsv(args, "LoadTest4")
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


if __name__ == "__main__":
    unittest.main()
