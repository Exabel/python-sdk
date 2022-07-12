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
        expected_error_message_beginning = (
            "2 signal column(s) contain non-numeric values. "
            "Please ensure all values can be parsed to numeric values\n\n\n"
            "Signal 'production' contains 6 non-numeric values, check the first five as examples:\n"
            "     entity       date known_time      production\n"
            "small_brand 2022-02-01 2022-02-01 three_thousands\n"
            "small_brand 2022-02-04 2022-02-05  four_thousands\n "
            "mini_brand 2022-02-05 2022-02-06  five_thousands\n "
            "mini_brand 2022-02-06 2022-02-07   six_thousands\n "
            "mini_brand 2022-02-07 2022-02-08 seven_thousands\n\n"
            "Signal 'price' contains 3 non-numeric values:\n      "
            "entity       date known_time     price\n"
            "middle_brand 2022-02-01 2022-02-01   fifteen\n"
            "middle_brand 2022-01-01 2022-01-01   sixteen\n "
            "small_brand 2022-02-02 2022-02-03 seventeen"
        )
        self.assertEqual(expected_error_message_beginning, str(exception))
