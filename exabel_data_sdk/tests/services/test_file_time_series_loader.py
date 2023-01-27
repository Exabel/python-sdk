import unittest
from unittest import mock

import pandas as pd

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.entity import Entity
from exabel_data_sdk.client.api.data_classes.entity_type import EntityType
from exabel_data_sdk.client.api.data_classes.signal import Signal
from exabel_data_sdk.services.file_loading_exception import FileLoadingException
from exabel_data_sdk.services.file_time_series_loader import FileTimeSeriesLoader
from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import SearchEntitiesResponse, SearchTerm
from exabel_data_sdk.tests.client.exabel_mock_client import ExabelMockClient
from exabel_data_sdk.tests.decorators import requires_modules


class TestFileTimeSeriesLoader(unittest.TestCase):
    def test_read_csv_should_failed_by_non_numeric_signal_values(self):
        client: ExabelClient = ExabelMockClient()
        with self.assertRaises(FileLoadingException) as context:
            FileTimeSeriesLoader(client).load_time_series(
                filename="exabel_data_sdk/tests/resources/"
                "data/time_series_with_non_numeric_values.csv",
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

    @mock.patch("exabel_data_sdk.services.file_time_series_parser.TimeSeriesFileParser.parse_file")
    def test_override_entity_type(self, mock_parse_file):
        mock_parse_file.return_value = pd.DataFrame(
            [{"arbitrary_column_name": "entity", "date": "2022-01-01", "my_signal": 9001}]
        )

        client: ExabelClient = ExabelMockClient(namespace="ns")
        client.entity_api.create_entity_type(EntityType("entityTypes/ns.brand", "", ""))
        client.signal_api.create_signal(Signal("signals/ns.my_signal", ""))
        FileTimeSeriesLoader(client).load_time_series(
            filename="filename",
            entity_type="ns.brand",
            pit_current_time=True,
        )
        create_ts_args = client.time_series_api.bulk_upsert_time_series.call_args[0]
        pd.testing.assert_series_equal(
            pd.Series(
                [9001],
                index=[pd.Timestamp("2022-01-01T00:00:00+0000", tz="UTC")],
                name="entityTypes/ns.brand/entities/ns.entity/signals/ns.my_signal",
            ),
            create_ts_args[0][0],
        )

    @mock.patch("exabel_data_sdk.services.file_time_series_parser.TimeSeriesFileParser.parse_file")
    def test_override_entity_type__with_identifier_type(self, mock_parse_file):
        mock_parse_file.return_value = pd.DataFrame(
            [{"arbitrary_column_name": "identifier", "date": "2022-01-01", "my_signal": 9001}]
        )

        client: ExabelClient = ExabelMockClient(namespace="ns")
        client.entity_api.create_entity_type(
            EntityType("entityTypes/read_only", "", "", read_only=True)
        )
        client.signal_api.create_signal(Signal("signals/ns.my_signal", ""))
        company1 = Entity("entityTypes/company/entities/the_company", "")
        client.entity_api.search.entities_by_terms.return_value = [
            SearchEntitiesResponse.SearchResult(entities=[company1.to_proto()]),
        ]
        FileTimeSeriesLoader(client).load_time_series(
            filename="filename",
            entity_type="company",
            identifier_type="isin",
            pit_current_time=True,
        )
        search_kwargs = client.entity_api.search.entities_by_terms.call_args[1]
        self.assertCountEqual(
            [SearchTerm(field="isin", query="identifier")],
            search_kwargs.get("terms"),
        )

        create_ts_args = client.time_series_api.bulk_upsert_time_series.call_args[0]
        pd.testing.assert_series_equal(
            pd.Series(
                [9001],
                index=[pd.Timestamp("2022-01-01T00:00:00+0000", tz="UTC")],
                name="entityTypes/company/entities/the_company/signals/ns.my_signal",
            ),
            create_ts_args[0][0],
        )

    @mock.patch("exabel_data_sdk.services.file_time_series_parser.TimeSeriesFileParser.parse_file")
    def test_override_entity_type__with_global_entity(self, mock_parse_file):
        mock_parse_file.return_value = pd.DataFrame([{"date": "2022-01-01", "my_signal": 9001}])

        client: ExabelClient = ExabelMockClient(namespace="ns")
        client.signal_api.create_signal(Signal("signals/ns.my_signal", ""))
        FileTimeSeriesLoader(client).load_time_series(
            filename="filename",
            entity_type="global",
            global_time_series=True,
            pit_current_time=True,
        )
        create_ts_args = client.time_series_api.bulk_upsert_time_series.call_args[0]
        pd.testing.assert_series_equal(
            pd.Series(
                [9001],
                index=[pd.Timestamp("2022-01-01T00:00:00+0000", tz="UTC")],
                name="entityTypes/global/entities/global/signals/ns.my_signal",
            ),
            create_ts_args[0][0],
        )

    @mock.patch("exabel_data_sdk.services.file_time_series_parser.TimeSeriesFileParser.parse_file")
    def test_override_entity_type__with_global_entity__wrong_entity_type_should_fail(
        self, mock_parse_file
    ):
        mock_parse_file.return_value = pd.DataFrame([{"date": "2022-01-01", "my_signal": 9001}])

        client: ExabelClient = ExabelMockClient(namespace="ns")
        client.signal_api.create_signal(Signal("signals/ns.my_signal", ""))
        with self.assertRaises(FileLoadingException) as cm:
            FileTimeSeriesLoader(client).load_time_series(
                filename="filename",
                entity_type="not_global",
                global_time_series=True,
                pit_current_time=True,
            )
        self.assertEqual(
            "Entity type must be set to 'global' when loading time series to the global entity.",
            cm.exception.args[0],
        )

    @mock.patch("exabel_data_sdk.services.file_time_series_loader.TimeSeriesFileParser.from_file")
    def test_batch_size(self, mock_from_file):
        batch_size = 1
        no_batches = 2
        mock_parser = mock.Mock()
        mock_parser.sheet_name.return_value = None
        mock_from_file.return_value = (mock_parser for _ in range(no_batches))
        client = mock.create_autospec(ExabelClient)
        loader = FileTimeSeriesLoader(client)
        with mock.patch.object(loader, "_load_time_series", return_value="result") as mock_load:
            results = loader.load_time_series(
                filename="filename",
                batch_size=batch_size,
            )
        self.assertEqual(batch_size, mock_from_file.call_args[0][2])
        self.assertEqual(no_batches, mock_load.call_count)
        self.assertEqual(no_batches, len(results))


@requires_modules("openpyxl")
class TestFileTimeSeriesLoaderExcelFiles(unittest.TestCase):
    def test_read_excel__signal_in_column_example_2(self):
        client: ExabelClient = ExabelMockClient()
        with self.assertRaises(FileLoadingException) as context:
            FileTimeSeriesLoader(client).load_time_series(
                filename="./exabel_data_sdk/tests/resources/data/signal_in_column_example_2.xlsx",
                pit_current_time=True,
            )
        self.assertIn("1 signal(s) contain non-numeric values.", str(context.exception))

    def test_read_excel__numbers_in_identifiers_error(self):
        client: ExabelClient = ExabelMockClient()
        with self.assertRaises(FileLoadingException) as context:
            FileTimeSeriesLoader(client).load_time_series(
                filename="./exabel_data_sdk/tests/resources/data/"
                "numbers_in_identifier_error_example.xlsx",
            )
        self.assertIn("Entity identifiers were not strings.", str(context.exception))

    def test_read_excel__global_time_series_with_wrong_option_true(self):
        client: ExabelClient = ExabelMockClient()
        with self.assertRaises(FileLoadingException) as context:
            FileTimeSeriesLoader(client).load_time_series(
                filename="./exabel_data_sdk/tests/resources/data/signal_in_row_example_2.xlsx",
                create_missing_signals=True,
                global_time_series=True,
            )
        self.assertIn("The global time series option was set", str(context.exception))

    def test_read_excel__global_time_series_with_wrong_option_false(self):
        client: ExabelClient = ExabelMockClient()
        with self.assertRaises(FileLoadingException) as context:
            FileTimeSeriesLoader(client).load_time_series(
                filename="./exabel_data_sdk/tests/resources/data/signal_in_row_example_4.xlsx",
                create_missing_signals=True,
                global_time_series=False,
            )
        self.assertIn("The global time series option was not set", str(context.exception))

    def test_read_excel__unsupported_format_1(self):
        client: ExabelClient = ExabelMockClient()
        with self.assertRaises(FileLoadingException) as context:
            FileTimeSeriesLoader(client).load_time_series(
                filename="./exabel_data_sdk/tests/resources/data/unsupported_format_1.xlsx",
            )
        self.assertIn("Column and row setup not recognized.", str(context.exception))

    def test_read_excel__unsupported_format_2(self):
        client: ExabelClient = ExabelMockClient()
        with self.assertRaises(FileLoadingException) as context:
            FileTimeSeriesLoader(client).load_time_series(
                filename="./exabel_data_sdk/tests/resources/data/unsupported_format_2.xlsx",
            )
        self.assertIn("Column with empty header found.", str(context.exception))

    def test_read_excel__invalid_date_columns(self):
        client: ExabelClient = ExabelMockClient()
        with self.assertRaises(FileLoadingException) as context:
            FileTimeSeriesLoader(client).load_time_series(
                filename="./exabel_data_sdk/tests/resources/data/corrupt_dates_1.xlsx",
            )
        self.assertIn("Failed parsing 'date' column as dates.", str(context.exception))

    def test_read_excel__column_with_number_name(self):
        client: ExabelClient = ExabelMockClient()
        with self.assertRaises(FileLoadingException) as context:
            FileTimeSeriesLoader(client).load_time_series(
                filename="./exabel_data_sdk/tests/resources/data/column_with_number_name_1.xlsx",
            )
        self.assertIn("invalid column(s) found: 1sales.", str(context.exception))

    def test_read_excel__empty_rows_inbetween(self):
        client: ExabelClient = ExabelMockClient()
        with self.assertRaises(FileLoadingException) as context:
            FileTimeSeriesLoader(client).load_time_series(
                filename="./exabel_data_sdk/tests/resources/data/with_empty_rows_1.xlsx",
            )
        self.assertIn("A cell in the entity column was empty.", str(context.exception))

    def test_read_excel__duplicate_columns(self):
        client: ExabelClient = ExabelMockClient()
        with self.assertRaises(FileLoadingException) as context:
            FileTimeSeriesLoader(client).load_time_series(
                filename="./exabel_data_sdk/tests/resources/data/multiple_columns_same_name_1.xlsx",
            )
        self.assertIn("File contains duplicate columns: rocks, water.", str(context.exception))
