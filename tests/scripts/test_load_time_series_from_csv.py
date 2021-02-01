import sys
import unittest

import pandas as pd
from dateutil import tz

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


if __name__ == "__main__":
    unittest.main()
