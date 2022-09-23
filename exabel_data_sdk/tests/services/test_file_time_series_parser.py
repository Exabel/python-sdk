import unittest
from itertools import zip_longest

import pandas as pd
import pandas.testing as pdt

from exabel_data_sdk.services.file_time_series_parser import ParsedTimeSeriesFile

# pylint: disable=protected-access


class TestTimeSeriesFileParser(unittest.TestCase):
    def test_drop_duplicate_data_points(self):
        series = pd.Series(
            [0, 1, 1],
            index=[0, 1, 1],
            name="time_series",
        )
        expected = pd.Series(
            [0, 1],
            index=[0, 1],
            name="time_series",
        )
        actual = ParsedTimeSeriesFile._drop_duplicate_data_points(series)
        pdt.assert_series_equal(expected, actual)

    def test_drop_duplicate_data_points__with_multi_index(self):
        series = pd.Series(
            [0, 1, 1],
            index=[(0, 0), (0, 1), (0, 1)],
            name="time_series",
        )
        expected = pd.Series(
            [0, 1],
            index=[(0, 0), (0, 1)],
            name="time_series",
        )
        actual = ParsedTimeSeriesFile._drop_duplicate_data_points(series)
        pdt.assert_series_equal(expected, actual)

    def test_drop_duplicate_data_points__ignores_different_values_for_same_index(self):
        series = pd.Series(
            [0, 1],
            index=[0, 0],
            name="time_series",
        )
        expected = series.copy()
        actual = ParsedTimeSeriesFile._drop_duplicate_data_points(series)
        pdt.assert_series_equal(expected, actual)

    def test_drop_duplicate_data_points__logs_warnings(self):
        series = pd.Series(
            [0, 1, 1],
            index=[0, 1, 1],
            name="time_series",
        )
        logger = "exabel_data_sdk.services.file_time_series_parser"
        with self.assertLogs(logger, level="WARNING") as log:
            ParsedTimeSeriesFile._drop_duplicate_data_points(series)
        self.assertEqual(len(log.output), 1)
        expected_message = (
            "Dropping 1 duplicate data point(s) from time series with name: 'time_series'"
        )
        self.assertEqual(
            expected_message,
            log.output[0][-len(expected_message) :],
        )

    def test_drop_time_series_with_duplicates_in_index(self):
        valid_series = [pd.Series([0, 1], index=[0, 1], name="time_series")]
        invalid_series = [pd.Series([0, 1], index=[0, 0], name="time_series")]
        logger = "exabel_data_sdk.services.file_time_series_parser"
        with self.assertLogs(logger, level="ERROR") as log:
            actual = list(
                ParsedTimeSeriesFile._get_time_series_with_duplicates_in_index(
                    valid_series + invalid_series
                )
            )
        self.assertIn(
            "1 duplicate data point(s) detected in time series with name: 'time_series'.",
            log.output[0],
        )
        for e, a in zip_longest(invalid_series, actual):
            pdt.assert_series_equal(e, a)
