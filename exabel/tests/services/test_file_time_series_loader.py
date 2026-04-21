from unittest import mock

import pandas as pd
import pytest
from dateutil import tz

from exabel import ExabelClient
from exabel.client.api.data_classes.entity import Entity
from exabel.client.api.data_classes.entity_type import EntityType
from exabel.client.api.data_classes.signal import Signal
from exabel.services.file_loading_exception import FileLoadingException
from exabel.services.file_loading_result import FileLoadingResult
from exabel.services.file_time_series_loader import FileTimeSeriesLoader
from exabel.stubs.exabel.api.data.v1.all_pb2 import SearchEntitiesResponse, SearchTerm
from exabel.tests.client.exabel_mock_client import ExabelMockClient
from exabel.tests.decorators import requires_modules


class TestFileTimeSeriesLoader:
    def test_read_csv_should_failed_by_non_numeric_signal_values(self):
        client: ExabelClient = ExabelMockClient()
        with pytest.raises(FileLoadingException) as context:
            FileTimeSeriesLoader(client).load_time_series(
                filename="exabel/tests/resources/"
                "data/time_series_with_non_numeric_values.csv",
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

    @mock.patch("exabel.services.file_time_series_parser.TimeSeriesFileParser.parse_file")
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

    @mock.patch("exabel.services.file_time_series_parser.TimeSeriesFileParser.parse_file")
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
        expected_terms = [SearchTerm(field="isin", query="identifier")]
        actual_terms = search_kwargs.get("terms")
        assert sorted(expected_terms) == sorted(actual_terms)

        create_ts_args = client.time_series_api.bulk_upsert_time_series.call_args[0]
        pd.testing.assert_series_equal(
            pd.Series(
                [9001],
                index=[pd.Timestamp("2022-01-01T00:00:00+0000", tz="UTC")],
                name="entityTypes/company/entities/the_company/signals/ns.my_signal",
            ),
            create_ts_args[0][0],
        )

    @mock.patch("exabel.services.file_time_series_parser.TimeSeriesFileParser.parse_file")
    def test_override_entity_type__security_with_identifier_type(self, mock_parse_file):
        mock_parse_file.return_value = pd.DataFrame(
            [{"arbitrary_column_name": "identifier", "date": "2022-01-01", "my_signal": 9001}]
        )

        client: ExabelClient = ExabelMockClient(namespace="ns")
        client.entity_api.create_entity_type(
            EntityType("entityTypes/read_only", "", "", read_only=True)
        )
        client.signal_api.create_signal(Signal("signals/ns.my_signal", ""))
        security1 = Entity("entityTypes/security/entities/the_security", "")
        client.entity_api.search.entities_by_terms.return_value = [
            SearchEntitiesResponse.SearchResult(entities=[security1.to_proto()]),
        ]
        FileTimeSeriesLoader(client).load_time_series(
            filename="filename",
            entity_type="security",
            identifier_type="cusip",
            pit_current_time=True,
        )
        search_kwargs = client.entity_api.search.entities_by_terms.call_args[1]
        expected_terms = [SearchTerm(field="cusip", query="identifier")]
        actual_terms = search_kwargs.get("terms")
        assert len(expected_terms) == len(actual_terms)
        for expected in expected_terms:
            assert expected in actual_terms

        create_ts_args = client.time_series_api.bulk_upsert_time_series.call_args[0]
        pd.testing.assert_series_equal(
            pd.Series(
                [9001],
                index=[pd.Timestamp("2022-01-01T00:00:00+0000", tz="UTC")],
                name="entityTypes/security/entities/the_security/signals/ns.my_signal",
            ),
            create_ts_args[0][0],
        )

    @mock.patch("exabel.services.file_time_series_parser.TimeSeriesFileParser.parse_file")
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

    @mock.patch("exabel.services.file_time_series_parser.TimeSeriesFileParser.parse_file")
    def test_override_entity_type__with_global_entity__wrong_entity_type_should_fail(
        self, mock_parse_file
    ):
        mock_parse_file.return_value = pd.DataFrame([{"date": "2022-01-01", "my_signal": 9001}])

        client: ExabelClient = ExabelMockClient(namespace="ns")
        client.signal_api.create_signal(Signal("signals/ns.my_signal", ""))
        with pytest.raises(FileLoadingException) as cm:
            FileTimeSeriesLoader(client).load_time_series(
                filename="filename",
                entity_type="not_global",
                global_time_series=True,
                pit_current_time=True,
            )
        assert (
            "Entity type must be set to 'global' when loading time series to the global entity."
            == cm.value.args[0]
        )

    @mock.patch("exabel.services.file_time_series_parser.TimeSeriesFileParser.parse_file")
    def test_override_entity_type__with_security_entity__unsupported_identifier_type_should_fail(
        self, mock_parse_file
    ):
        mock_parse_file.return_value = pd.DataFrame(
            [{"arbitrary_column_name": "identifier", "date": "2022-01-01", "my_signal": 9001}]
        )

        client: ExabelClient = ExabelMockClient(namespace="ns")
        client.signal_api.create_signal(Signal("signals/ns.my_signal", ""))
        with pytest.raises(FileLoadingException) as cm:
            FileTimeSeriesLoader(client).load_time_series(
                filename="filename",
                entity_type="security",
                identifier_type="figi",
                pit_current_time=True,
            )
        assert "Unsupported identifier_type (figi) for security." == cm.value.args[0]

    @mock.patch("exabel.services.file_time_series_loader.TimeSeriesFileParser.from_file")
    def test_batch_size(self, mock_from_file):
        batch_size = 1
        no_batches = 2
        mock_parser = mock.Mock()
        mock_parser.sheet_name.return_value = None
        mock_from_file.return_value = (mock_parser for _ in range(no_batches))
        client = mock.create_autospec(ExabelClient)
        loader = FileTimeSeriesLoader(client)
        with mock.patch.object(
            loader, "_load_time_series", return_value=FileLoadingResult()
        ) as mock_load:
            results = loader.load_time_series(
                filename="filename",
                batch_size=batch_size,
            )
        assert batch_size == mock_from_file.call_args[0][2]
        assert no_batches == mock_load.call_count
        assert no_batches == len(results)

    def test_missing_known_time_in_file(self):
        client: ExabelClient = ExabelMockClient()
        with pytest.raises(FileLoadingException) as context:
            FileTimeSeriesLoader(client).batch_delete_time_series_points(
                filename="exabel/tests/resources/"
                "data/timeseries_delete_points_missing_known_time.csv",
                separator=";",
            )
        exception = context.value
        actual = str(exception)
        assert "To delete data points the 'known_time' must be specified in file." in actual

    @mock.patch("exabel.services.file_time_series_parser.TimeSeriesFileParser.parse_file")
    def test_read_file(self, mock_parse_file):
        def timestamp(t: str):
            return pd.Timestamp(t, tz=tz.tzutc())

        mock_parse_file.return_value = pd.DataFrame(
            [
                {
                    "arbitrary_column_name": "identifier",
                    "date": "2022-01-01",
                    "known_time": "2022-02-01",
                    "my_signal": 1,
                }
            ]
        )

        client: ExabelClient = ExabelMockClient(namespace="ns")
        client.entity_api.create_entity_type(EntityType("entityTypes/ns.brand", "", ""))
        client.signal_api.create_signal(Signal("signals/ns.my_signal", ""))
        FileTimeSeriesLoader(client).batch_delete_time_series_points(
            filename="filename",
            entity_type="ns.brand",
        )
        delete_ts_args = client.time_series_api.batch_delete_time_series_points.call_args[0]
        pd.testing.assert_series_equal(
            pd.Series(
                [1],
                index=pd.MultiIndex.from_tuples(
                    [(timestamp("2022-01-01"), timestamp("2022-02-01"))]
                ),
                name="entityTypes/ns.brand/entities/ns.identifier/signals/ns.my_signal",
            ),
            delete_ts_args[0][0],
        )


@requires_modules("openpyxl")
class TestFileTimeSeriesLoaderExcelFiles:
    def test_read_excel__signal_in_column_example_2(self):
        client: ExabelClient = ExabelMockClient()
        with pytest.raises(FileLoadingException) as context:
            FileTimeSeriesLoader(client).load_time_series(
                filename="./exabel/tests/resources/data/signal_in_column_example_2.xlsx",
                pit_current_time=True,
            )
        assert "1 signal(s) contain non-numeric values." in str(context.value)

    def test_read_excel__numbers_in_identifiers_error(self):
        client: ExabelClient = ExabelMockClient()
        with pytest.raises(FileLoadingException) as context:
            FileTimeSeriesLoader(client).load_time_series(
                filename="./exabel/tests/resources/data/"
                "numbers_in_identifier_error_example.xlsx",
            )
        assert "Entity identifiers were not strings." in str(context.value)

    def test_read_excel__global_time_series_with_wrong_option_true(self):
        client: ExabelClient = ExabelMockClient()
        with pytest.raises(FileLoadingException) as context:
            FileTimeSeriesLoader(client).load_time_series(
                filename="./exabel/tests/resources/data/signal_in_row_example_2.xlsx",
                create_missing_signals=True,
                global_time_series=True,
            )
        assert "The global time series option was set" in str(context.value)

    def test_read_excel__global_time_series_with_wrong_option_false(self):
        client: ExabelClient = ExabelMockClient()
        with pytest.raises(FileLoadingException) as context:
            FileTimeSeriesLoader(client).load_time_series(
                filename="./exabel/tests/resources/data/signal_in_row_example_4.xlsx",
                create_missing_signals=True,
                global_time_series=False,
            )
        assert "The global time series option was not set" in str(context.value)

    def test_read_excel__unsupported_format_1(self):
        client: ExabelClient = ExabelMockClient()
        with pytest.raises(FileLoadingException) as context:
            FileTimeSeriesLoader(client).load_time_series(
                filename="./exabel/tests/resources/data/unsupported_format_1.xlsx",
            )
        assert "Column and row setup not recognized." in str(context.value)

    def test_read_excel__unsupported_format_2(self):
        client: ExabelClient = ExabelMockClient()
        with pytest.raises(FileLoadingException) as context:
            FileTimeSeriesLoader(client).load_time_series(
                filename="./exabel/tests/resources/data/unsupported_format_2.xlsx",
            )
        assert "Column with empty header found." in str(context.value)

    def test_read_excel__invalid_date_columns(self):
        client: ExabelClient = ExabelMockClient()
        with pytest.raises(FileLoadingException) as context:
            FileTimeSeriesLoader(client).load_time_series(
                filename="./exabel/tests/resources/data/corrupt_dates_1.xlsx",
            )
        assert "Failed parsing 'date' column as dates." in str(context.value)

    def test_read_excel__column_with_number_name(self):
        client: ExabelClient = ExabelMockClient()
        with pytest.raises(FileLoadingException) as context:
            FileTimeSeriesLoader(client).load_time_series(
                filename="./exabel/tests/resources/data/column_with_number_name_1.xlsx",
            )
        assert "invalid column(s) found: 1sales." in str(context.value)

    def test_read_excel__empty_rows_inbetween(self):
        client: ExabelClient = ExabelMockClient()
        with pytest.raises(FileLoadingException) as context:
            FileTimeSeriesLoader(client).load_time_series(
                filename="./exabel/tests/resources/data/with_empty_rows_1.xlsx",
            )
        assert "The 'date' column has missing values, which is not permitted." in str(context.value)

    def test_read_excel__duplicate_columns(self):
        client: ExabelClient = ExabelMockClient()
        with pytest.raises(FileLoadingException) as context:
            FileTimeSeriesLoader(client).load_time_series(
                filename="./exabel/tests/resources/data/multiple_columns_same_name_1.xlsx",
            )
        assert "File contains duplicate columns: rocks, water." in str(context.value)
