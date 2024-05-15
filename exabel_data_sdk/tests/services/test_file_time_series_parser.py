import math
import unittest
from itertools import zip_longest
from typing import Sequence
from unittest import mock

import pandas as pd
import pandas.testing as pdt
from dateutil import tz

from exabel_data_sdk.client.api.data_classes.time_series import Dimension, TimeSeries, Unit, Units
from exabel_data_sdk.client.api.entity_api import EntityApi
from exabel_data_sdk.client.api.search_service import SearchService
from exabel_data_sdk.client.exabel_client import ExabelClient
from exabel_data_sdk.services.file_time_series_parser import (
    MetaDataSignalNamesInRows,
    ParsedTimeSeriesFile,
    SignalNamesInColumns,
    SignalNamesInRows,
    TimeSeriesFileParser,
    _remove_dot_int,
)
from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import (
    Entity,
    SearchEntitiesResponse,
    SearchTerm,
)
from exabel_data_sdk.util.resource_name_normalization import (
    EntityResourceNames,
    EntitySearchResultWarning,
)

# pylint: disable=protected-access

BLOOMBERG_TICKER_MAPPING = {"AAPL US": "F_000C7F-E", "MSFT US": "F_000Q07-E"}


class TestTimeSeriesFileParser(unittest.TestCase):
    def test_from_file__excel_with_batch_size_should_fail(self):
        with self.assertRaises(ValueError) as cm:
            TimeSeriesFileParser.from_file(
                "file.xlsx",
                batch_size=100,
            )
        self.assertEqual(
            "Cannot specify batch size when uploading Excel files.",
            str(cm.exception),
        )

    @mock.patch("exabel_data_sdk.services.file_time_series_parser.CsvReader.read_file")
    def test_from_file__with_batch_size(self, mock_read_file):
        mock_read_file.return_value = (pd.DataFrame() for _ in range(2))
        parsers = TimeSeriesFileParser.from_file(
            "file.csv",
            batch_size=100,
        )
        dfs = [parser.data_frame for parser in parsers]
        mock_read_file.assert_called_once_with(
            "file.csv",
            None,
            (0,),
            keep_default_na=True,
            chunksize=100,
        )
        self.assertEqual(2, len(dfs))
        for df in dfs:
            self.assertTrue(df.empty)

    def test_parse_file__with_data_frame(self):
        df = pd.DataFrame(
            [{"a": 1}, {"a": 2}],
        )
        parser = TimeSeriesFileParser("file", None, None, df)
        actual_df = parser.parse_file()
        pdt.assert_frame_equal(df, actual_df)
        nrows_df = parser.parse_file(nrows=1)
        pdt.assert_frame_equal(df.iloc[:1], nrows_df)

    def test_parse_file__with_data_frame__with_header_should_fail(self):
        parser = TimeSeriesFileParser("file", None, None, pd.DataFrame())
        with self.assertRaises(ValueError) as cm:
            parser.parse_file(header=True)
        self.assertEqual(
            "Cannot specify header when uploading in batches.",
            str(cm.exception),
        )


class TestParsedTimeSeriesFile(unittest.TestCase):
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

    def test_validate_long_format_columns(self):
        self.assertTrue(
            SignalNamesInRows.is_valid(
                pd.DataFrame(columns=["mic:ticker", "signal", "value", "date"])
            )
        )
        self.assertTrue(
            SignalNamesInRows.is_valid(pd.DataFrame(columns=["1brand", "signal", "value", "date"]))
        )
        self.assertFalse(
            SignalNamesInRows.is_valid(
                pd.DataFrame(columns=["mic:ticker", "signal", "brand", "value", "date"])
            )
        )
        self.assertFalse(
            SignalNamesInRows.is_valid(pd.DataFrame(columns=["mic:ticker", "signal", "value"]))
        )

    def test_validate_medium_format_columns(self):
        self.assertTrue(
            SignalNamesInColumns.is_valid(pd.DataFrame(columns=["mic:ticker", "date", "signal1"]))
        )
        self.assertFalse(
            SignalNamesInColumns.is_valid(
                pd.DataFrame(columns=["mic:ticker", "date", "signal1", "1thing"])
            )
        )
        self.assertTrue(
            SignalNamesInColumns.is_valid(pd.DataFrame(columns=["1thing", "date", "signal1"]))
        )
        self.assertFalse(
            SignalNamesInColumns.is_valid(pd.DataFrame(columns=["date", "signal1", "1thing"]))
        )

    def test_remove_dot_int(self):
        self.assertEqual("asdf.fefe", _remove_dot_int("asdf.fefe"))
        self.assertEqual("asdf.", _remove_dot_int("asdf."))
        self.assertEqual(".asdf", _remove_dot_int(".asdf"))
        self.assertEqual("asdf", _remove_dot_int("asdf.1"))
        self.assertEqual("asdf", _remove_dot_int("asdf.10000"))
        self.assertEqual("asdf.1", _remove_dot_int("asdf.1.100"))

    def test_get_series(self):
        names = mock.create_autospec(EntityResourceNames)
        index = pd.DatetimeIndex(
            ["2020-10-10", "2020-10-11", "2020-10-15", "2020-10-15", "2020-10-11"]
        )
        entity_a = "entityTypes/brand/entities/a"
        entity_b = "entityTypes/brand/entities/b"
        parsed = SignalNamesInRows(
            pd.DataFrame(
                {
                    "entity": [entity_a, entity_a, entity_b, entity_b, entity_a],
                    "signal": ["price", "sales", "price", "sales", "price"],
                    "value": [10.0, math.nan, 11.0, 12.0, 11.0],
                },
                index=index,
            ),
            names,
        )
        name_to_series = {s.name: s for s in parsed.get_series("prefix.").valid_series}
        expected = [
            pd.Series(
                [10.0, 11.0],
                index=[pd.Timestamp("2020-10-10"), pd.Timestamp("2020-10-11")],
                name=entity_a + "/prefix.price",
            ),
            pd.Series(
                math.nan, index=[pd.Timestamp("2020-10-11")], name=entity_a + "/prefix.sales"
            ),
            pd.Series(11.0, index=[pd.Timestamp("2020-10-15")], name=entity_b + "/prefix.price"),
            pd.Series(12.0, index=[pd.Timestamp("2020-10-15")], name=entity_b + "/prefix.sales"),
        ]
        for e in expected:
            pd.testing.assert_series_equal(e, name_to_series[e.name])

    def _entities_by_terms(
        self, entity_type: str, terms: Sequence[SearchTerm]
    ) -> Sequence[SearchEntitiesResponse.SearchResult]:
        results = []
        for term in terms:
            entities = []
            if BLOOMBERG_TICKER_MAPPING.get(term.query):
                entities.append(
                    Entity(
                        name=f"{entity_type}/entities/{BLOOMBERG_TICKER_MAPPING[term.query]}",
                        display_name=term.query,
                    )
                )
            results.append(
                SearchEntitiesResponse.SearchResult(
                    terms=[term],
                    entities=entities,
                )
            )

        return results

    def test_from_data_frame_long_and_medium_format(self):
        parsers = [SignalNamesInColumns, SignalNamesInRows]
        data = pd.DataFrame(
            {
                "entity": ["AAPL US", "AAPL US", "MSFT US", "unmapped"],
                "date": ["2021-01-01", "2021-01-02", "2021-01-01", "2021-01-03"],
                "signal": [1, 2, 4, 5],
            }
        )

        client = mock.create_autospec(ExabelClient)
        client.entity_api = mock.create_autospec(EntityApi)
        client.entity_api.search = mock.create_autospec(SearchService)
        client.entity_api.search.entities_by_terms.side_effect = self._entities_by_terms

        for parser in parsers:
            if parser == SignalNamesInRows:
                data = data.rename(columns={"signal": "value"})
                data.loc[:, "signal"] = "signal"
            parsed_file = parser.from_data_frame(
                data.copy(),
                client.entity_api,
                namespace="ns",
                entity_type="company",
                identifier_type="bloomberg_ticker",
            )

            expected_data = data.copy()
            expected_data["entity"] = data["entity"].apply(
                lambda x: (
                    f"entityTypes/company/entities/{BLOOMBERG_TICKER_MAPPING[x]}"
                    if BLOOMBERG_TICKER_MAPPING.get(x)
                    else None
                )
            )
            expected_data = expected_data.set_index("date", drop=True)
            expected_data.index = pd.DatetimeIndex(expected_data.index, tz=tz.tzutc())
            expected_data.index.name = None
            expected_data = expected_data.dropna(subset=["entity"], how="any")
            pdt.assert_frame_equal(parsed_file.data, expected_data)

            lookup_result = parsed_file.get_entity_lookup_result()
            self.assertDictEqual(
                lookup_result.mapping,
                {
                    k: f"entityTypes/company/entities/{v}"
                    for k, v in BLOOMBERG_TICKER_MAPPING.items()
                },
            )
            self.assertListEqual(
                lookup_result.warnings,
                [
                    EntitySearchResultWarning(
                        field="bloomberg_ticker", query="unmapped", matched_entity_names=[]
                    )
                ],
            )


class TestMetaDataSignalNamesInRows(unittest.TestCase):
    def test_get_deduplicated_series(self):
        series = [
            TimeSeries(
                pd.Series([], name="time_series_1", dtype=object),
                units=Units(units=[Unit(Dimension.DIMENSION_CURRENCY, unit="USD")]),
            ),
            TimeSeries(
                pd.Series([], name="time_series_1", dtype=object),
                units=Units(units=[Unit(Dimension.DIMENSION_CURRENCY, unit="USD")]),
            ),
            TimeSeries(
                pd.Series([], name="time_series_2", dtype=object),
                units=Units(units=[Unit(Dimension.DIMENSION_CURRENCY, unit="USD")]),
            ),
            TimeSeries(
                pd.Series([], name="time_series_2", dtype=object),
                units=Units(units=[Unit(Dimension.DIMENSION_CURRENCY, unit="GBP")]),
            ),
        ]
        logger = "exabel_data_sdk.services.file_time_series_parser"
        with self.assertLogs(logger, level="ERROR") as log:
            series_deduplicated, series_with_duplicate_names = (
                MetaDataSignalNamesInRows._get_deduplicated_series(series)
            )
        self.assertIn(
            "Time series time_series_2 detected with the following different metadata",
            log.output[0],
        )
        self.assertListEqual([series[0]], series_deduplicated)
        self.assertListEqual(series[2:], series_with_duplicate_names)
