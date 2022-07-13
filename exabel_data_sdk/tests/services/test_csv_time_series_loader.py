import unittest

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.services.csv_exception import CsvLoadingException
from exabel_data_sdk.services.csv_time_series_loader import CsvTimeSeriesLoader
from exabel_data_sdk.tests.client.exabel_mock_client import ExabelMockClient


class TestCsvTimeSeriesLoader(unittest.TestCase):
    def test_read_csv_should_failed_by_non_numeric_signal_values(self):
        client: ExabelClient = ExabelMockClient()
        with self.assertRaises(CsvLoadingException) as context:
            CsvTimeSeriesLoader(client).load_time_series(
                filename="exabel_data_sdk/tests/resources/"
                "data/time_series_with_non_numeric_values.csv",
                namespace="test",
            )
        exception = context.exception
        actual = str(exception)
        self.assertIn(
            "2 signal column(s) contain non-numeric values. "
            "Please ensure all values can be parsed to numeric values",
            actual,
        )
        self.assertIn(
            "Signal 'production' contains 6 non-numeric values, check the first five as examples:",
            actual,
        )
        self.assertIn("Signal 'price' contains 3 non-numeric values", actual)
