import unittest
from unittest import mock

import pandas as pd

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.time_series_api import TimeSeriesApi
from exabel_data_sdk.scripts.delete_time_series_point import DeleteTimeSeriesPoint

common_args = [
    "script-name",
    "--api-key",
    "123",
    "--name",
    "entityTypes/a.entity_type/entities/a.entity_name/signals/a.signal_name",
    "--date",
    "2020-10-31",
    "--known-time",
    "2020-11-15",
]


class TestDeleteTimeSeriesPoint(unittest.TestCase):
    def test_delete_time_series_point(self):
        script = DeleteTimeSeriesPoint(common_args, "Delete a time series point.")
        mock_client = mock.create_autospec(ExabelClient)
        mock_client.time_series_api = mock.create_autospec(TimeSeriesApi)
        script.run_script(mock_client, script.parse_arguments())

        call_args_list = mock_client.time_series_api.batch_delete_time_series_points.call_args_list
        self.assertEqual(1, len(call_args_list))

        series = {series.name: series for series in call_args_list[0][1]["series"]}
        self.assertEqual(1, len(series))

        pd.testing.assert_series_equal(
            pd.Series(
                dtype="float64",
                name="entityTypes/a.entity_type/entities/a.entity_name/signals/a.signal_name",
                index=[(pd.Timestamp("2020-10-31"), pd.Timestamp("2020-11-15"))],
            ),
            series["entityTypes/a.entity_type/entities/a.entity_name/signals/a.signal_name"],
            check_freq=False,
        )
