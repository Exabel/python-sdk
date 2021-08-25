import sys
import unittest
from unittest import mock

import pandas as pd
from dateutil import tz

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.scripts.load_time_series_from_csv import LoadTimeSeriesFromCsv


class TestUploadTimeSeries(unittest.TestCase):
    def test_one_signal(self):
        loader = LoadTimeSeriesFromCsv(sys.argv, "Load")
        data = [["a", "2021-01-01", 1], ["a", "2021-01-02", 2], ["b", "2021-01-01", 3]]

        data_frame = pd.DataFrame(data, columns=["entity", "date", "signal1"])

        time_series = loader.get_time_series_for_entity(data_frame, "b", ["signal1"])
        pd.testing.assert_series_equal(
            time_series[0],
            pd.Series([3], index=pd.DatetimeIndex(["2021-01-01"], tz=tz.tzutc()), name="b/signal1"),
        )

    def test_two_signals(self):
        loader = LoadTimeSeriesFromCsv(sys.argv, "Load")

        data = [
            ["a", "2021-01-01", 1, 100],
            ["a", "2021-01-02", 2, 200],
            ["b", "2021-01-01", 3, 300],
        ]
        data_frame = pd.DataFrame(data, columns=["entity", "date", "signal1", "signal2"])

        time_series = loader.get_time_series_for_entity(data_frame, "a", ["signal1", "signal2"])

        pd.testing.assert_series_equal(
            time_series[0],
            pd.Series(
                [1, 2],
                index=pd.DatetimeIndex(["2021-01-01", "2021-01-02"], tz=tz.tzutc()),
                name="a/signal1",
            ),
        )

        pd.testing.assert_series_equal(
            time_series[1],
            pd.Series(
                [100, 200],
                index=pd.DatetimeIndex(["2021-01-01", "2021-01-02"], tz=tz.tzutc()),
                name="a/signal2",
            ),
        )

    def test_signal_value(self):
        loader = LoadTimeSeriesFromCsv(sys.argv, "Load")

        data = [["a", "2021-01-01", 1, 100], ["a", "2021-01-02", 2, 200]]

        data_frame = pd.DataFrame(data, columns=["entity", "date", "signal1", "signal2"])

        date_index = pd.DatetimeIndex(["2021-01-01", "2021-01-02"], tz=tz.tzutc())

        series = loader.get_time_series_for_signal(data_frame, "a", "signal2")

        pd.testing.assert_series_equal(
            series, pd.Series([100, 200], index=date_index, name="a/signal2")
        )

    def test_read_file_use_header_for_signal(self):
        args = [
            "script-name",
            "--filename",
            "./exabel_data_sdk/tests/resources/data/timeseries.csv",
        ]

        script = LoadTimeSeriesFromCsv(args, "LoadTest1")
        client = mock.create_autospec(ExabelClient(host="host", api_key="123"))
        script.run_script(client, script.parse_arguments())

        # first call - company_A / signal1
        call_args_first = client.time_series_api.upsert_time_series.call_args_list[0][0]
        self.assertEqual(
            "entityTypes/company/entities/company_A/signal1",
            call_args_first[0],
            "Signal name is wrong",
        )

        pd.testing.assert_series_equal(
            call_args_first[1],
            pd.Series(
                [1, 2, 3, 4, 5],
                index=pd.DatetimeIndex(
                    ["2021-01-01", "2021-01-02", "2021-01-03", "2021-01-04", "2021-01-05"],
                    tz=tz.tzutc(),
                ),
                name="entityTypes/company/entities/company_A/signal1",
            ),
        )

    def test_read_file_with_signal_override(self):

        args = [
            "script-name",
            "--filename",
            "./exabel_data_sdk/tests/resources/data/timeseries.csv",
            "--signals",
            "signal1_o",
        ]

        script = LoadTimeSeriesFromCsv(args, "LoadTest2")
        client = mock.create_autospec(ExabelClient(host="host", api_key="123"))
        script.run_script(client, script.parse_arguments())

        # first call - company_A / signal1_o
        call_args_first = client.time_series_api.upsert_time_series.call_args_list[0][0]
        self.assertEqual(
            "entityTypes/company/entities/company_A/signal1_o",
            call_args_first[0],
            "Signal name is wrong",
        )

        pd.testing.assert_series_equal(
            call_args_first[1],
            pd.Series(
                [1, 2, 3, 4, 5],
                index=pd.DatetimeIndex(
                    ["2021-01-01", "2021-01-02", "2021-01-03", "2021-01-04", "2021-01-05"],
                    tz=tz.tzutc(),
                ),
                name="entityTypes/company/entities/company_A/signal1_o",
            ),
        )

        # second call - company_B / signal1_o
        call_args_second = client.time_series_api.upsert_time_series.call_args_list[1][0]
        self.assertEqual(
            "entityTypes/company/entities/company_B/signal1_o",
            call_args_second[0],
            "Signal name is wrong",
        )

        pd.testing.assert_series_equal(
            call_args_second[1],
            pd.Series(
                [4, 5],
                index=pd.DatetimeIndex(["2021-01-01", "2021-01-03"], tz=tz.tzutc()),
                name="entityTypes/company/entities/company_B/signal1_o",
            ),
        )

    def test_read_file_with_multiple_signals_and_override(self):

        args = [
            "script-name",
            "--filename",
            "./exabel_data_sdk/tests/resources/data/timeseries_multiple_signals.csv",
            "--signals",
            "signal1_o",
            "signal2_o",
        ]

        script = LoadTimeSeriesFromCsv(args, "LoadTest3")
        client = mock.create_autospec(ExabelClient(host="host", api_key="123"))
        script.run_script(client, script.parse_arguments())

        # first call - company_A / signal1_o
        call_args_first = client.time_series_api.upsert_time_series.call_args_list[0][0]
        self.assertEqual(
            "entityTypes/company/entities/company_A/signal1_o",
            call_args_first[0],
            "Signal name is wrong",
        )

        pd.testing.assert_series_equal(
            call_args_first[1],
            pd.Series(
                [1, 2],
                index=pd.DatetimeIndex(["2021-01-01", "2021-01-02"], tz=tz.tzutc()),
                name="entityTypes/company/entities/company_A/signal1_o",
            ),
        )

        # second call - company_A / signal2_o
        call_args_first = client.time_series_api.upsert_time_series.call_args_list[1][0]
        self.assertEqual(
            "entityTypes/company/entities/company_A/signal2_o",
            call_args_first[0],
            f"Signal name {call_args_first[0]} is wrong",
        )

        pd.testing.assert_series_equal(
            call_args_first[1],
            pd.Series(
                [10, 20],
                index=pd.DatetimeIndex(["2021-01-01", "2021-01-02"], tz=tz.tzutc()),
                name="entityTypes/company/entities/company_A/signal2_o",
            ),
        )


if __name__ == "__main__":
    unittest.main()
