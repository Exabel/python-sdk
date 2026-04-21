import pytest

from exabel import ExabelClient
from exabel.services.csv_exception import CsvLoadingException
from exabel.services.csv_time_series_loader import CsvTimeSeriesLoader
from exabel.services.file_loading_exception import FileLoadingException
from exabel.tests.client.exabel_mock_client import ExabelMockClient


class TestCsvTimeSeriesLoader:
    def test_read_csv_should_failed_by_non_numeric_signal_values(self):
        client: ExabelClient = ExabelMockClient()
        with pytest.raises(FileLoadingException) as context:
            CsvTimeSeriesLoader(client).load_time_series(
                filename="exabel/tests/resources/data/time_series_with_non_numeric_values.csv",
            )
        exception = context.value
        actual = str(exception)
        assert (
            "2 signal(s) contain non-numeric values. "
            "Please ensure all values can be parsed to numeric values" in actual
        )
        assert (
            "Signal 'production' contains 6 non-numeric values, check the first five as examples:"
            in actual
        )
        assert "Signal 'price' contains 3 non-numeric values" in actual

    def test_exeption_alias(self):
        client: ExabelClient = ExabelMockClient()
        with pytest.raises(CsvLoadingException):
            CsvTimeSeriesLoader(client).load_time_series(
                filename="exabel/tests/resources/data/time_series_with_non_numeric_values.csv",
            )
