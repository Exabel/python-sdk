import unittest

import pandas as pd
from dateutil import tz
from google.protobuf import timestamp_pb2
from google.protobuf.wrappers_pb2 import DoubleValue

from exabel_data_sdk.client.api.time_series_api import TimeSeriesApi

# pylint: disable=protected-access
from exabel_data_sdk.stubs.exabel.api.data.v1.time_series_messages_pb2 import TimeSeriesPoint


class TestTimeSeriesApi(unittest.TestCase):
    def test_time_series_conversion(self):
        series = pd.Series(
            [1.0, 2.0, 3.0],
            index=pd.DatetimeIndex(["2019-01-01", "2019-02-01", "2019-03-01"], tz=tz.tzutc()),
        )

        pd.testing.assert_series_equal(
            series,
            TimeSeriesApi._time_series_points_to_series(
                TimeSeriesApi._series_to_time_series_points(series)
            ),
        )

    def test_time_series_conversion_known_time(self):
        index = pd.MultiIndex.from_arrays(
            [
                pd.DatetimeIndex(["2021-01-01", "2021-01-02"], tz=tz.tzutc()),
                pd.DatetimeIndex(["2021-01-01", "2021-01-05"], tz=tz.tzutc()),
            ]
        )
        series = pd.Series([1.0, 2.0], index=index)
        points = TimeSeriesApi._series_to_time_series_points(series)
        pd.testing.assert_series_equal(
            series.droplevel(1),
            TimeSeriesApi._time_series_points_to_series(points),
        )
        base_time = pd.Timestamp("2021-01-01").value // 1000000000
        self.assertEqual(1609459200, base_time)
        expected_points = [
            TimeSeriesPoint(
                time=timestamp_pb2.Timestamp(seconds=base_time),
                value=DoubleValue(value=1.0),
                known_time=timestamp_pb2.Timestamp(seconds=base_time),
            ),
            TimeSeriesPoint(
                time=timestamp_pb2.Timestamp(seconds=base_time + 86400),
                value=DoubleValue(value=2.0),
                known_time=timestamp_pb2.Timestamp(seconds=base_time + 86400 * 4),
            ),
        ]
        self.assertSequenceEqual(expected_points, points)

    def test_time_series_conversion_without_time_zone(self):
        series = pd.Series(
            [1.0, 2.0, 3.0],
            index=pd.DatetimeIndex(["2019-01-01", "2019-02-01", "2019-03-01"]),
        )
        expected = pd.Series(
            [1.0, 2.0, 3.0],
            index=pd.DatetimeIndex(["2019-01-01", "2019-02-01", "2019-03-01"], tz=tz.tzutc()),
        )

        pd.testing.assert_series_equal(
            expected,
            TimeSeriesApi._time_series_points_to_series(
                TimeSeriesApi._series_to_time_series_points(series)
            ),
        )

    def test_time_series_conversion_with_different_time_zone(self):
        series = pd.Series(
            [1.0, 2.0, 3.0],
            index=pd.DatetimeIndex(["2019-01-01", "2019-02-01", "2019-03-01"], tz="US/Eastern"),
        )
        expected = pd.Series(
            [1.0, 2.0, 3.0],
            index=pd.DatetimeIndex(
                ["2019-01-01 05:00:00", "2019-02-01 05:00:00", "2019-03-01 05:00:00"], tz=tz.tzutc()
            ),
        )

        pd.testing.assert_series_equal(
            expected,
            TimeSeriesApi._time_series_points_to_series(
                TimeSeriesApi._series_to_time_series_points(series)
            ),
        )
