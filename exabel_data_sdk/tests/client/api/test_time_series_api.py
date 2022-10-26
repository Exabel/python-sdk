import unittest

import pandas as pd
from dateutil import tz
from google.protobuf import timestamp_pb2
from google.protobuf.wrappers_pb2 import DoubleValue

from exabel_data_sdk.client.api.time_series_api import TimeSeriesApi
from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import (
    ImportTimeSeriesRequest,
    TimeSeries,
    TimeSeriesPoint,
)

# pylint: disable=protected-access


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

    def test_estimate_size_constants(self):
        point_without_known_time = TimeSeriesPoint(
            value=DoubleValue(value=2),
            time=TimeSeriesApi._pandas_timestamp_to_proto(pd.Timestamp("2022-01-01")),
        )
        self.assertEqual(19, point_without_known_time.ByteSize())

        point_with_known_time = TimeSeriesPoint(
            value=DoubleValue(value=2),
            time=TimeSeriesApi._pandas_timestamp_to_proto(pd.Timestamp("2022-01-01")),
            known_time=TimeSeriesApi._pandas_timestamp_to_proto(pd.Timestamp("2023-01-01")),
        )
        self.assertEqual(27, point_with_known_time.ByteSize())

    def test_estimate_size_calculation(self):
        series_without_known_time = pd.Series(
            name=self._ts_name(),
            data=1.0,
            index=pd.DatetimeIndex(["2021-01-01", "2022-01-01"], tz=tz.tzutc()),
        )

        self.assertEqual(
            TimeSeries(
                name=str(series_without_known_time.name),
                points=TimeSeriesApi._series_to_time_series_points(series_without_known_time),
            ).ByteSize(),
            TimeSeriesApi._estimate_size(series_without_known_time),
        )

        series_with_known_time = pd.Series(
            name=self._ts_name(),
            data=1.0,
            index=pd.MultiIndex.from_arrays(
                [
                    pd.DatetimeIndex(["2021-01-01", "2022-01-01"], tz=tz.tzutc()),
                    pd.DatetimeIndex(["2021-01-01", "2022-01-01"], tz=tz.tzutc()),
                ]
            ),
        )
        self.assertEqual(
            TimeSeries(
                name=str(series_with_known_time.name),
                points=TimeSeriesApi._series_to_time_series_points(series_with_known_time),
            ).ByteSize(),
            TimeSeriesApi._estimate_size(series_with_known_time),
        )

    def test_get_batches_for_import(self):
        index = pd.DatetimeIndex(["2021-01-01", "2022-01-01"], tz=tz.tzutc())
        series = [pd.Series(name=self._ts_name(), data=1.0, index=index)] * 10000
        batches = TimeSeriesApi._get_batches_for_import(series)

        # There are 10.000 series.
        # Each series has 365 points and adds 227 bytes to the request.
        # The maximum limit for a single request is 1.048.576 bytes (1MB).
        # 1.048.576 / 227 ~= 4619 series per request.
        self.assertEqual(3, len(batches))
        self.assertEqual(4619, len(batches[0]))
        self.assertEqual(4619, len(batches[1]))
        self.assertEqual(762, len(batches[2]))

        request = ImportTimeSeriesRequest(
            time_series=[
                TimeSeries(
                    name=str(series.name),
                    points=TimeSeriesApi._series_to_time_series_points(series),
                )
                for series in batches[0]
            ]
        )
        self.assertEqual(1062370, request.ByteSize())

    def _ts_name(self) -> str:
        ns = "customer_namespace"
        entity_type_name = f"{ns}.customer_entity_type"
        entity_name = f"{ns}.{'a' * 32}"
        signal_name = f"{ns}.custom_signal_name_with_lots_of_characters"
        return f"entityTypes/{entity_type_name}/entities/{entity_name}/signals/{signal_name}"
