import unittest

import pandas as pd
from dateutil import tz

from exabel_data_sdk.client.api.time_series_api import TimeSeriesApi

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
