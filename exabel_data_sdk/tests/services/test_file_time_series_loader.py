import unittest

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.services.file_loading_exception import FileLoadingException
from exabel_data_sdk.services.file_time_series_loader import FileTimeSeriesLoader
from exabel_data_sdk.tests.client.exabel_mock_client import ExabelMockClient
from exabel_data_sdk.tests.decorators import requires_modules


class TestFileTimeSeriesLoader(unittest.TestCase):
    def test_read_csv_should_failed_by_non_numeric_signal_values(self):
        client: ExabelClient = ExabelMockClient()
        with self.assertRaises(FileLoadingException) as context:
            FileTimeSeriesLoader(client).load_time_series(
                filename="exabel_data_sdk/tests/resources/"
                "data/time_series_with_non_numeric_values.csv",
                namespace="test",
            )
        exception = context.exception
        actual = str(exception)
        self.assertIn(
            "2 signal(s) contain non-numeric values. "
            "Please ensure all values can be parsed to numeric values",
            actual,
        )
        self.assertIn(
            "Signal 'production' contains 6 non-numeric values, check the first five as examples:",
            actual,
        )
        self.assertIn("Signal 'price' contains 3 non-numeric values", actual)


@requires_modules("openpyxl")
class TestFileTimeSeriesLoaderExcelFiles(unittest.TestCase):
    def test_read_excel__signal_in_column_example_2(self):
        client: ExabelClient = ExabelMockClient()
        with self.assertRaises(FileLoadingException) as context:
            FileTimeSeriesLoader(client).load_time_series(
                filename="./exabel_data_sdk/tests/resources/data/signal_in_column_example_2.xlsx",
                namespace="test",
                pit_current_time=True,
            )
        self.assertIn("1 signal(s) contain non-numeric values.", str(context.exception))

    def test_read_excel__numbers_in_identifiers_error(self):
        client: ExabelClient = ExabelMockClient()
        with self.assertRaises(FileLoadingException) as context:
            FileTimeSeriesLoader(client).load_time_series(
                filename="./exabel_data_sdk/tests/resources/data/"
                "numbers_in_identifier_error_example.xlsx",
                namespace="test",
            )
        self.assertIn("Entity identifiers were not strings.", str(context.exception))

    def test_read_excel__global_time_series_with_wrong_option_true(self):
        client: ExabelClient = ExabelMockClient()
        with self.assertRaises(FileLoadingException) as context:
            FileTimeSeriesLoader(client).load_time_series(
                filename="./exabel_data_sdk/tests/resources/data/signal_in_row_example_2.xlsx",
                create_missing_signals=True,
                namespace="test",
                global_time_series=True,
            )
        self.assertIn("The global time series option was set", str(context.exception))

    def test_read_excel__global_time_series_with_wrong_option_false(self):
        client: ExabelClient = ExabelMockClient()
        with self.assertRaises(FileLoadingException) as context:
            FileTimeSeriesLoader(client).load_time_series(
                filename="./exabel_data_sdk/tests/resources/data/signal_in_row_example_4.xlsx",
                create_missing_signals=True,
                namespace="test",
                global_time_series=False,
            )
        self.assertIn("The global time series option was not set", str(context.exception))

    def test_read_excel__unsupported_format_1(self):
        client: ExabelClient = ExabelMockClient()
        with self.assertRaises(FileLoadingException) as context:
            FileTimeSeriesLoader(client).load_time_series(
                filename="./exabel_data_sdk/tests/resources/data/unsupported_format_1.xlsx",
                namespace="test",
            )
        self.assertIn("Column and row setup not recognized.", str(context.exception))

    def test_read_excel__unsupported_format_2(self):
        client: ExabelClient = ExabelMockClient()
        with self.assertRaises(FileLoadingException) as context:
            FileTimeSeriesLoader(client).load_time_series(
                filename="./exabel_data_sdk/tests/resources/data/unsupported_format_2.xlsx",
                namespace="test",
            )
        self.assertIn("Column and row setup not recognized.", str(context.exception))
