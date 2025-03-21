import unittest
from functools import partial
from typing import Callable
from unittest import mock

import numpy as np
import pandas as pd
from dateutil import tz

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.entity_type import EntityType
from exabel_data_sdk.client.api.data_classes.paging_result import PagingResult
from exabel_data_sdk.client.api.data_classes.signal import Signal
from exabel_data_sdk.client.api.entity_api import EntityApi
from exabel_data_sdk.client.api.resource_creation_result import ResourceCreationResults
from exabel_data_sdk.client.api.signal_api import SignalApi
from exabel_data_sdk.client.api.time_series_api import TimeSeriesApi
from exabel_data_sdk.scripts.load_time_series_from_file import LoadTimeSeriesFromFile
from exabel_data_sdk.services.file_loading_exception import FileLoadingException
from exabel_data_sdk.services.file_time_series_loader import FileTimeSeriesLoader
from exabel_data_sdk.services.file_time_series_parser import (
    SignalNamesInColumns,
    SignalNamesInRows,
    TimeSeriesFileParser,
)
from exabel_data_sdk.util.resource_name_normalization import validate_signal_name

common_args = ["script-name", "--sep", ";", "--api-key", "123"]


# pylint: disable=protected-access


class TestUploadTimeSeries(unittest.TestCase):
    def setUp(self) -> None:
        self.client = mock.create_autospec(ExabelClient)
        self.client.entity_api = mock.create_autospec(EntityApi)
        self.client.signal_api = mock.create_autospec(SignalApi)
        self.client.time_series_api = mock.create_autospec(TimeSeriesApi)

        self.client.namespace = "ns"
        self.client.signal_api.get_signal_iterator.side_effect = self._list_signal
        self.client.entity_api.get_entity_type_iterator.side_effect = self._list_entity_types

    def test_one_signal(self):
        data = [["a", "2021-01-01", 1], ["a", "2021-01-02", 2], ["b", "2021-01-01", 3]]

        ts_data = pd.DataFrame(data, columns=["entity", "date", "signal1"])
        parser = SignalNamesInColumns.from_data_frame(ts_data, self.client.entity_api, "")
        time_series = parser.get_series("signals/acme.").valid_series
        pd.testing.assert_series_equal(
            pd.Series(
                [1, 2],
                index=pd.DatetimeIndex(["2021-01-01", "2021-01-02"], tz=tz.tzutc()),
                name="a/signals/acme.signal1",
            ),
            time_series[0],
        )
        pd.testing.assert_series_equal(
            pd.Series(
                [3],
                index=pd.DatetimeIndex(["2021-01-01"], tz=tz.tzutc()),
                name="b/signals/acme.signal1",
            ),
            time_series[1],
        )

    def test_two_signals(self):
        data = [
            ["a", "2021-01-01", 1, 100],
            ["a", "2021-01-02", 2, 200],
            ["b", "2021-01-01", 3, 300],
        ]
        ts_data = pd.DataFrame(data, columns=["entity", "date", "signal1", "signal2"])

        parser = SignalNamesInColumns.from_data_frame(ts_data, self.client.entity_api, "")
        time_series = {s.name: s for s in parser.get_series("signals/acme.").valid_series}

        pd.testing.assert_series_equal(
            pd.Series(
                [1, 2],
                index=pd.DatetimeIndex(["2021-01-01", "2021-01-02"], tz=tz.tzutc()),
                name="a/signals/acme.signal1",
            ),
            time_series["a/signals/acme.signal1"],
        )
        pd.testing.assert_series_equal(
            pd.Series(
                [100, 200],
                index=pd.DatetimeIndex(["2021-01-01", "2021-01-02"], tz=tz.tzutc()),
                name="a/signals/acme.signal2",
            ),
            time_series["a/signals/acme.signal2"],
        )
        pd.testing.assert_series_equal(
            pd.Series(
                [3],
                index=pd.DatetimeIndex(["2021-01-01"], tz=tz.tzutc()),
                name="b/signals/acme.signal1",
            ),
            time_series["b/signals/acme.signal1"],
        )
        pd.testing.assert_series_equal(
            pd.Series(
                [300],
                index=pd.DatetimeIndex(["2021-01-01"], tz=tz.tzutc()),
                name="b/signals/acme.signal2",
            ),
            time_series["b/signals/acme.signal2"],
        )

    def test_two_signals_long_formatted(self):
        data = [
            ["a", "2021-01-01", "signal1", 1.0],
            ["a", "2021-01-02", "signal1", 2.0],
            ["b", "2021-01-01", "signal1", 3.0],
            ["a", "2021-01-01", "signal2", 100.0],
            ["a", "2021-01-02", "signal2", 200.0],
            ["b", "2021-01-01", "signal2", 300.0],
            ["b", "2021-01-02", "signal2", np.nan],
        ]
        ts_data = pd.DataFrame(data, columns=["entity", "date", "signal", "value"])

        parser = SignalNamesInRows.from_data_frame(ts_data, self.client.entity_api, "")
        time_series = {s.name: s for s in parser.get_series("signals/acme.").valid_series}

        pd.testing.assert_series_equal(
            pd.Series(
                [1.0, 2.0],
                index=pd.DatetimeIndex(["2021-01-01", "2021-01-02"], tz=tz.tzutc()),
                name="a/signals/acme.signal1",
            ),
            time_series["a/signals/acme.signal1"],
        )
        pd.testing.assert_series_equal(
            pd.Series(
                [100.0, 200.0],
                index=pd.DatetimeIndex(["2021-01-01", "2021-01-02"], tz=tz.tzutc()),
                name="a/signals/acme.signal2",
            ),
            time_series["a/signals/acme.signal2"],
        )
        pd.testing.assert_series_equal(
            pd.Series(
                [3.0],
                index=pd.DatetimeIndex(["2021-01-01"], tz=tz.tzutc()),
                name="b/signals/acme.signal1",
            ),
            time_series["b/signals/acme.signal1"],
        )
        pd.testing.assert_series_equal(
            pd.Series(
                [300.0, np.nan],
                index=pd.DatetimeIndex(["2021-01-01", "2021-01-02"], tz=tz.tzutc()),
                name="b/signals/acme.signal2",
            ),
            time_series["b/signals/acme.signal2"],
        )

    def test_get_series(self):
        data = [
            ["a", "2021-01-01", 1],
            ["a", "2021-01-01", 2],
            ["b", "2021-01-01", 3],
            ["b", "2021-01-01", 3],
        ]

        ts_data = pd.DataFrame(data, columns=["entity", "date", "signal1"])
        parser = SignalNamesInColumns.from_data_frame(ts_data, self.client.entity_api, "")
        time_series = parser.get_series("signals/acme.")
        self.assertEqual(1, len(time_series.failures))
        self.assertEqual(1, len(time_series.valid_series))
        pd.testing.assert_series_equal(
            pd.Series(
                [1, 2],
                index=pd.DatetimeIndex(["2021-01-01", "2021-01-01"], tz=tz.tzutc()),
                name="a/signals/acme.signal1",
            ),
            time_series.failures[0].resource,
        )
        pd.testing.assert_series_equal(
            pd.Series(
                [3],
                index=pd.DatetimeIndex(["2021-01-01"], tz=tz.tzutc()),
                name="b/signals/acme.signal1",
            ),
            time_series.valid_series[0],
        )

    def test_get_series__skip_validation(self):
        data = [
            ["a", "2021-01-01", 1],
            ["a", "2021-01-01", 2],
            ["b", "2021-01-01", 3],
            ["b", "2021-01-01", 3],
        ]

        ts_data = pd.DataFrame(data, columns=["entity", "date", "signal1"])
        parser = SignalNamesInColumns.from_data_frame(ts_data, self.client.entity_api, "")
        time_series = parser.get_series("signals/acme.", skip_validation=True)
        self.assertSequenceEqual([], time_series.failures)
        self.assertEqual(2, len(time_series.valid_series))
        pd.testing.assert_series_equal(
            pd.Series(
                [1, 2],
                index=pd.DatetimeIndex(["2021-01-01", "2021-01-01"], tz=tz.tzutc()),
                name="a/signals/acme.signal1",
            ),
            time_series.valid_series[0],
        )
        pd.testing.assert_series_equal(
            pd.Series(
                [3, 3],
                index=pd.DatetimeIndex(["2021-01-01", "2021-01-01"], tz=tz.tzutc()),
                name="b/signals/acme.signal1",
            ),
            time_series.valid_series[1],
        )

    def test_read_file_without_pit(self):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/timeseries.csv",
        ]
        script = LoadTimeSeriesFromFile(args)
        with self.assertRaises(SystemExit):
            script.run_script(self.client, script.parse_arguments())

    def test_read_file_use_header_for_signal(self):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/timeseries.csv",
            "--pit-current-time",
        ]

        script = LoadTimeSeriesFromFile(args)
        script.run_script(self.client, script.parse_arguments())

        call_args_list = self.client.time_series_api.bulk_upsert_time_series.call_args_list
        self.assertEqual(1, len(call_args_list))
        series = {s.name: s for s in call_args_list[0][0][0]}
        self.assertEqual(2, len(series))

        pd.testing.assert_series_equal(
            pd.Series(
                range(1, 6),
                pd.date_range("2021-01-01", periods=5, tz=tz.tzutc()),
                name="entityTypes/company/entities/company_A/signals/ns.signal1",
            ),
            series["entityTypes/company/entities/company_A/signals/ns.signal1"],
            check_freq=False,
        )
        pd.testing.assert_series_equal(
            pd.Series(
                [4, 5],
                pd.DatetimeIndex(["2021-01-01", "2021-01-03"], tz=tz.tzutc()),
                name="entityTypes/company/entities/company_B/signals/ns.signal1",
            ),
            series["entityTypes/company/entities/company_B/signals/ns.signal1"],
            check_freq=False,
        )

    def test_read_file_with_multiple_signals(self):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/timeseries_multiple_signals.csv",
            "--pit-offset",
            "0",
        ]
        script = LoadTimeSeriesFromFile(args)
        script.run_script(self.client, script.parse_arguments())

        call_args_list = self.client.time_series_api.bulk_upsert_time_series.call_args_list
        self.assertEqual(1, len(call_args_list))
        series_by_key = {s.name: s for s in call_args_list[0][0][0]}
        self.assertEqual(4, len(series_by_key))
        pd.testing.assert_series_equal(
            pd.Series(
                [1, 2],
                pd.DatetimeIndex(["2021-01-01", "2021-01-02"], tz=tz.tzutc()),
                name="entityTypes/company/entities/company_A/signals/ns.signal1",
            ),
            series_by_key["entityTypes/company/entities/company_A/signals/ns.signal1"],
        )
        pd.testing.assert_series_equal(
            pd.Series(
                [10, 20],
                pd.DatetimeIndex(["2021-01-01", "2021-01-02"], tz=tz.tzutc()),
                name="entityTypes/company/entities/company_A/signals/ns.signal2",
            ),
            series_by_key["entityTypes/company/entities/company_A/signals/ns.signal2"],
        )
        pd.testing.assert_series_equal(
            pd.Series(
                [4, 5],
                pd.DatetimeIndex(["2021-01-01", "2021-01-03"], tz=tz.tzutc()),
                name="entityTypes/company/entities/company_B/signals/ns.signal1",
            ),
            series_by_key["entityTypes/company/entities/company_B/signals/ns.signal1"],
        )
        pd.testing.assert_series_equal(
            pd.Series(
                [40, 50],
                pd.DatetimeIndex(["2021-01-01", "2021-01-03"], tz=tz.tzutc()),
                name="entityTypes/company/entities/company_B/signals/ns.signal2",
            ),
            series_by_key["entityTypes/company/entities/company_B/signals/ns.signal2"],
        )

    def test_read_file_in_long_format(self):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/timeseries_long_format.csv",
            "--pit-offset",
            "0",
        ]
        script = LoadTimeSeriesFromFile(args)
        script.run_script(self.client, script.parse_arguments())

        call_args_list = self.client.time_series_api.bulk_upsert_time_series.call_args_list
        self.assertEqual(1, len(call_args_list))
        series = call_args_list[0][0][0]
        self.assertEqual(4, len(series))
        series_by_name = {s.name: s for s in series}
        pd.testing.assert_series_equal(
            pd.Series(
                [1.0, 2.0],
                pd.DatetimeIndex(["2021-01-01", "2021-01-02"], tz=tz.tzutc()),
                name="entityTypes/company/entities/company_A/signals/ns.signal1",
            ),
            series_by_name["entityTypes/company/entities/company_A/signals/ns.signal1"],
        )
        pd.testing.assert_series_equal(
            pd.Series(
                [10.0, 20.0],
                pd.DatetimeIndex(["2021-01-01", "2021-01-02"], tz=tz.tzutc()),
                name="entityTypes/company/entities/company_A/signals/ns.signal2",
            ),
            series_by_name["entityTypes/company/entities/company_A/signals/ns.signal2"],
        )
        pd.testing.assert_series_equal(
            pd.Series(
                [4.0, 5.0],
                pd.DatetimeIndex(["2021-01-01", "2021-01-03"], tz=tz.tzutc()),
                name="entityTypes/company/entities/company_B/signals/ns.signal1",
            ),
            series_by_name["entityTypes/company/entities/company_B/signals/ns.signal1"],
        )
        pd.testing.assert_series_equal(
            pd.Series(
                [40.0, 50.0, np.nan],
                pd.DatetimeIndex(["2021-01-01", "2021-01-03", "2021-01-04"], tz=tz.tzutc()),
                name="entityTypes/company/entities/company_B/signals/ns.signal2",
            ),
            series_by_name["entityTypes/company/entities/company_B/signals/ns.signal2"],
        )

    def test_read_file_with_known_time(self):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/timeseries_known_time.csv",
        ]
        script = LoadTimeSeriesFromFile(args)
        script.run_script(self.client, script.parse_arguments())

        call_args_list = self.client.time_series_api.bulk_upsert_time_series.call_args_list
        self.assertEqual(1, len(call_args_list))
        series_by_name = {s.name: s for s in call_args_list[0][0][0]}
        self.assertEqual(4, len(series_by_name))

        index_a = pd.MultiIndex.from_arrays(
            [
                pd.DatetimeIndex(["2021-01-01", "2021-01-02"], tz=tz.tzutc()),
                pd.DatetimeIndex(["2021-01-01", "2021-01-05"], tz=tz.tzutc()),
            ]
        )
        index_b = pd.MultiIndex.from_arrays(
            [
                pd.DatetimeIndex(["2021-01-01", "2021-01-03"], tz=tz.tzutc()),
                pd.DatetimeIndex(["2021-01-10", "2019-12-31"], tz=tz.tzutc()),
            ]
        )
        pd.testing.assert_series_equal(
            pd.Series(
                [1, 2],
                index_a,
                name="entityTypes/company/entities/company_A/signals/ns.signal1",
            ),
            series_by_name["entityTypes/company/entities/company_A/signals/ns.signal1"],
        )
        pd.testing.assert_series_equal(
            pd.Series(
                [10, 20],
                index_a,
                name="entityTypes/company/entities/company_A/signals/ns.signal2",
            ),
            series_by_name["entityTypes/company/entities/company_A/signals/ns.signal2"],
        )
        pd.testing.assert_series_equal(
            pd.Series(
                [4, 5],
                index_b,
                name="entityTypes/company/entities/company_B/signals/ns.signal1",
            ),
            series_by_name["entityTypes/company/entities/company_B/signals/ns.signal1"],
        )
        pd.testing.assert_series_equal(
            pd.Series(
                [40, 50],
                index_b,
                name="entityTypes/company/entities/company_B/signals/ns.signal2",
            ),
            series_by_name["entityTypes/company/entities/company_B/signals/ns.signal2"],
        )

    def test_read_file_with_integer_identifiers(self):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/timeseries_with_integer_identifiers.csv",
            "--pit-offset",
            "30",
        ]

        script = LoadTimeSeriesFromFile(args)
        script.run_script(self.client, script.parse_arguments())

        call_args_list = self.client.time_series_api.bulk_upsert_time_series.call_args_list
        self.assertEqual(1, len(call_args_list))
        series = call_args_list[0][0][0]
        self.assertEqual(2, len(series))

        pd.testing.assert_series_equal(
            pd.Series(
                range(1, 6),
                pd.date_range("2021-01-01", periods=5, tz=tz.tzutc()),
                name="entityTypes/brand/entities/ns.0001/signals/ns.signal1",
            ),
            series[0],
            check_freq=False,
        )
        pd.testing.assert_series_equal(
            pd.Series(
                [4, 5],
                pd.DatetimeIndex(["2021-01-01", "2021-01-03"], tz=tz.tzutc()),
                name="entityTypes/brand/entities/ns.0002/signals/ns.signal1",
            ),
            series[1],
            check_freq=False,
        )

    def test_read_file_with_nan_identifiers(self):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/timeseries_with_empty_identifiers.csv",
            "--pit-offset",
            "30",
        ]
        with self.assertRaises(SystemExit):
            script = LoadTimeSeriesFromFile(args)
            script.run_script(self.client, script.parse_arguments())

    def test_should_fail_with_invalid_signal_names(self):
        signals_errors = {
            "0_starts_with_0": "Signal name must start with a letter, "
            'contain only letters, numbers, and underscores, but got "0_starts_with_0"',
            "contains_!llegal_chars": "Signal name must start with a letter, "
            'contain only letters, numbers, and underscores, but got "contains_!llegal_chars"',
            "": "Signal name cannot be empty",
            "signal_with_length_of_one_hundred_and_twenty_nine_characters_in_identifier_part_of_"
            "resource_name_which_is_more_than_maximum_129__": "Signal name "
            "cannot be longer than 128 characters, but got "
            '"signal_with_length_of_one_hundred_and_twenty_nine_characters_in_identifier_part_of_'
            'resource_name_which_is_more_than_maximum_129__"',
        }

        for signal, error in signals_errors.items():
            with self.assertRaises(ValueError) as cm:
                validate_signal_name(signal)
            self.assertEqual(str(cm.exception), error)

    def test_valid_signal_names(self):
        valid_signals = [
            "signal",
            "SIGNAL",
            "signal_with_underscores",
            "signal_1_with_underscores_and_numbers",
            "signal_with_length_of_one_hundred_and_twenty_eight_characters_in_identifier_part_of_"
            "resource_name_which_is_the_maximum_128_chars",
        ]

        for signal in valid_signals:
            validate_signal_name(signal)

    def test_should_fail_with_invalid_data_points(self):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/time_series_with_invalid_data_points.csv",
        ]

        script = LoadTimeSeriesFromFile(args)
        with self.assertRaises(SystemExit):
            script.run_script(self.client, script.parse_arguments())

    def test_valid_no_create_library_signal(self):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/timeseries_known_time.csv",
            "--create-missing-signals",
            "--no-create-library-signal",
        ]
        script = LoadTimeSeriesFromFile(args)
        self.client.namespace = "acme"
        script.run_script(self.client, script.parse_arguments())

        call_args_list = self.client.signal_api.update_signal.call_args_list
        create_library_signal_status = call_args_list[0][1]["create_library_signal"]
        self.assertFalse(create_library_signal_status)

    def test_valid_create_library_signal(self):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/timeseries_known_time.csv",
            "--create-missing-signals",
        ]
        script = LoadTimeSeriesFromFile(args)
        self.client.namespace = "acme"
        script.run_script(self.client, script.parse_arguments())

        call_args_list = self.client.signal_api.update_signal.call_args_list
        create_library_signal_status = call_args_list[0][1]["create_library_signal"]
        self.assertTrue(create_library_signal_status)

    def test_valid_replace_existing_time_series(self):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/timeseries_known_time.csv",
            "--create-missing-signals",
            "--replace-existing-time-series",
        ]
        script = LoadTimeSeriesFromFile(args)
        self.client.namespace = "acme"
        script.run_script(self.client, script.parse_arguments())

        call_args_list = self.client.time_series_api.bulk_upsert_time_series.call_args_list
        replace_existing_time_series_status = call_args_list[0][1]["replace_existing_time_series"]
        self.assertTrue(replace_existing_time_series_status)

    def test_replace_existing_time_series_across_batches(self):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/timeseries.csv",
            "--create-missing-signals",
            "--pit-offset",
            "0",
            "--replace-existing-time-series",
            "--batch-size",
            "3",
        ]
        script = LoadTimeSeriesFromFile(args)
        self.client.namespace = "acme"
        script.run_script(self.client, script.parse_arguments())

        call_args_list = self.client.time_series_api.bulk_upsert_time_series.call_args_list
        self.assertEqual(4, len(call_args_list))
        self.assertTrue(call_args_list[0][1]["replace_existing_time_series"])
        self.assertEqual(
            "entityTypes/company/entities/company_A/signals/acme.signal1",
            call_args_list[0][0][0][0].name,
        )
        self.assertFalse("replace_existing_time_series" in call_args_list[1][1])
        self.assertEqual(
            "entityTypes/company/entities/company_A/signals/acme.signal1",
            call_args_list[1][0][0][0].name,
        )
        self.assertTrue(call_args_list[2][1]["replace_existing_time_series"])
        self.assertEqual(
            "entityTypes/company/entities/company_B/signals/acme.signal1",
            call_args_list[2][0][0][0].name,
        )
        self.assertFalse("replace_existing_time_series" in call_args_list[3][1])
        self.assertEqual(
            "entityTypes/company/entities/company_B/signals/acme.signal1",
            call_args_list[3][0][0][0].name,
        )

    def test_replace_existing_data_points_across_batches(self):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/timeseries.csv",
            "--create-missing-signals",
            "--pit-offset",
            "0",
            "--replace-existing-data-points",
            "--batch-size",
            "3",
        ]
        script = LoadTimeSeriesFromFile(args)
        self.client.namespace = "acme"
        script.run_script(self.client, script.parse_arguments())

        call_args_list = self.client.time_series_api.bulk_upsert_time_series.call_args_list
        self.assertEqual(3, len(call_args_list))
        self.assertTrue(call_args_list[0][1]["replace_existing_data_points"])
        self.assertEqual(
            "entityTypes/company/entities/company_A/signals/acme.signal1",
            call_args_list[0][0][0][0].name,
        )
        self.assertTrue(call_args_list[2][1]["replace_existing_data_points"])
        self.assertEqual(
            "entityTypes/company/entities/company_B/signals/acme.signal1",
            call_args_list[2][0][0][0].name,
        )

    @property
    def _partial_load_time_series(self) -> Callable:
        parse_file_result = pd.DataFrame(
            data={
                "entity": ["entity1", "entity1", "entity2"],
                "date": ["2022-01-01", "2022-01-01", "2022-01-01"],
                "signal1": [1.0, 2.0, 1.0],
            }
        )
        results = mock.create_autospec(ResourceCreationResults)
        results.has_failure.return_value = False
        self.client.time_series_api.bulk_upsert_time_series.return_value = results
        parser = mock.create_autospec(TimeSeriesFileParser)
        parser.preview = parse_file_result
        parser.parse_file.return_value = parse_file_result
        parser.data_frame = None
        loader = FileTimeSeriesLoader(client=self.client)
        return partial(
            loader._load_time_series,
            parser=parser,
            error_on_any_failure=True,
            pit_current_time=True,
        )

    def test_load_time_series_with_duplicate_indexes_should_fail(self):
        with self.assertRaises(FileLoadingException) as cm:
            self._partial_load_time_series()
        self.assertEqual(1, len(cm.exception.failures))
        self.assertEqual([1.0, 2.0], cm.exception.failures[0].resource.to_list())

    def test_load_time_series_with_duplicate_indexes_with_dry_run_should_fail(self):
        with self.assertRaises(FileLoadingException) as cm:
            self._partial_load_time_series(dry_run=True)
        self.assertEqual(1, len(cm.exception.failures))
        self.assertEqual([1.0, 2.0], cm.exception.failures[0].resource.to_list())

    def test_load_time_series_with_uppercase_signals_not_existing(self):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/timeseries_with_uppercase_columns.csv",
            "--create-missing-signals",
        ]
        script = LoadTimeSeriesFromFile(args)
        self.client.signal_api.get_signal.return_value = None
        self.client.signal_api.get_signal_iterator.side_effect = lambda *_: PagingResult([], "", 0)
        self.client.entity_api.get_entity_type_iterator.side_effect = (
            self._list_entity_types_uppercase
        )

        script.run_script(self.client, script.parse_arguments())

        call_args_list = self.client.time_series_api.bulk_upsert_time_series.call_args_list
        self.assertEqual(1, len(call_args_list))
        series = call_args_list[0][0][0]
        self.assertEqual(1, len(series))
        call_args_list_update_signal = self.client.signal_api.update_signal.call_args_list
        self.assertEqual(1, len(call_args_list_update_signal))
        signal = call_args_list_update_signal[0][0][0]
        self.assertEqual("signals/ns.signal1", signal.name)

        pd.testing.assert_series_equal(
            pd.Series(
                [1, 2, 3, 4, 5],
                pd.MultiIndex.from_arrays(
                    [
                        pd.date_range("2021-01-01", periods=5, tz=tz.tzutc()),
                        pd.date_range("2021-01-01", periods=5, tz=tz.tzutc()),
                    ]
                ),
                name="entityTypes/BRAND/entities/ns.A_brand/signals/ns.signal1",
            ),
            series[0],
            check_freq=False,
        )

    def test_load_time_series_with_uppercase_signals_existing(self):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/timeseries_with_uppercase_columns.csv",
            "--create-missing-signals",
        ]
        script = LoadTimeSeriesFromFile(args)
        self.client.signal_api.get_signal_iterator.side_effect = self._list_signal_uppercase
        self.client.entity_api.get_entity_type_iterator.side_effect = (
            self._list_entity_types_uppercase
        )
        script.run_script(self.client, script.parse_arguments())

        call_args_list = self.client.time_series_api.bulk_upsert_time_series.call_args_list
        self.assertEqual(1, len(call_args_list))
        self.assertEqual(0, len(self.client.signal_api.update_signal.call_args_list))
        series = call_args_list[0][0][0]
        self.assertEqual(1, len(series))

        pd.testing.assert_series_equal(
            pd.Series(
                [1, 2, 3, 4, 5],
                pd.MultiIndex.from_arrays(
                    [
                        pd.date_range("2021-01-01", periods=5, tz=tz.tzutc()),
                        pd.date_range("2021-01-01", periods=5, tz=tz.tzutc()),
                    ]
                ),
                name="entityTypes/BRAND/entities/ns.A_brand/signals/ns.SIGNAL1",
            ),
            series[0],
            check_freq=False,
        )

    def test_load_time_series_with_uppercase_signals_existing_and_uppercase_entity_type_nonexisting(
        self,
    ):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/timeseries_with_uppercase_columns.csv",
            "--create-missing-signals",
        ]
        script = LoadTimeSeriesFromFile(args)
        self.client.signal_api.get_signal_iterator.side_effect = self._list_signal_uppercase
        self.client.entity_api.get_entity_type_iterator.side_effect = self._list_entity_types

        script.run_script(self.client, script.parse_arguments())

        call_args_list = self.client.time_series_api.bulk_upsert_time_series.call_args_list
        self.assertEqual(1, len(call_args_list))
        self.assertEqual(0, len(self.client.signal_api.update_signal.call_args_list))
        series = call_args_list[0][0][0]
        self.assertEqual(1, len(series))

        pd.testing.assert_series_equal(
            pd.Series(
                [1, 2, 3, 4, 5],
                pd.MultiIndex.from_arrays(
                    [
                        pd.date_range("2021-01-01", periods=5, tz=tz.tzutc()),
                        pd.date_range("2021-01-01", periods=5, tz=tz.tzutc()),
                    ]
                ),
                name="entityTypes/brand/entities/ns.A_brand/signals/ns.SIGNAL1",
            ),
            series[0],
            check_freq=False,
        )

    def test_load_time_series_with_uppercase_signals_not_existing_case_sensitive(self):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/timeseries_with_mixedcase_columns.csv",
            "--create-missing-signals",
            "--case-sensitive-signals",
        ]
        script = LoadTimeSeriesFromFile(args)
        self.client.signal_api.get_signal.return_value = None
        self.client.signal_api.get_signal_iterator.side_effect = lambda *_: PagingResult([], "", 0)
        self.client.entity_api.get_entity_type_iterator.side_effect = (
            self._list_entity_types_uppercase
        )

        script.run_script(self.client, script.parse_arguments())

        call_args_list = self.client.time_series_api.bulk_upsert_time_series.call_args_list
        self.assertEqual(1, len(call_args_list))
        series = call_args_list[0][0][0]
        self.assertEqual(1, len(series))
        call_args_list_update_signal = self.client.signal_api.update_signal.call_args_list
        self.assertEqual(1, len(call_args_list_update_signal))
        signal = call_args_list_update_signal[0][0][0]
        self.assertEqual("signals/ns.Signal1", signal.name)

        pd.testing.assert_series_equal(
            pd.Series(
                [1, 2, 3, 4, 5],
                pd.MultiIndex.from_arrays(
                    [
                        pd.date_range("2021-01-01", periods=5, tz=tz.tzutc()),
                        pd.date_range("2021-01-01", periods=5, tz=tz.tzutc()),
                    ]
                ),
                name="entityTypes/BRAND/entities/ns.A_brand/signals/ns.Signal1",
            ),
            series[0],
            check_freq=False,
        )

    def test_load_time_series_with_uppercase_signals_and_lower_case_existing_case_sensitive(self):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/timeseries_with_mixedcase_columns.csv",
            "--create-missing-signals",
            "--case-sensitive-signals",
        ]
        script = LoadTimeSeriesFromFile(args)
        self.client.signal_api.get_signal_iterator.side_effect = self._list_signal
        self.client.signal_api.get_signal.return_value = None
        self.client.signal_api.get_signal_iterator.side_effect = lambda *_: PagingResult([], "", 0)
        self.client.entity_api.get_entity_type_iterator.side_effect = (
            self._list_entity_types_uppercase
        )

        script.run_script(self.client, script.parse_arguments())

        call_args_list = self.client.time_series_api.bulk_upsert_time_series.call_args_list
        self.assertEqual(1, len(call_args_list))
        series = call_args_list[0][0][0]
        self.assertEqual(1, len(series))
        call_args_list_update_signal = self.client.signal_api.update_signal.call_args_list
        self.assertEqual(1, len(call_args_list_update_signal))
        signal = call_args_list_update_signal[0][0][0]
        self.assertEqual("signals/ns.Signal1", signal.name)

        pd.testing.assert_series_equal(
            pd.Series(
                [1, 2, 3, 4, 5],
                pd.MultiIndex.from_arrays(
                    [
                        pd.date_range("2021-01-01", periods=5, tz=tz.tzutc()),
                        pd.date_range("2021-01-01", periods=5, tz=tz.tzutc()),
                    ]
                ),
                name="entityTypes/BRAND/entities/ns.A_brand/signals/ns.Signal1",
            ),
            series[0],
            check_freq=False,
        )

    def test_load_time_series_with_uppercase_signals_existing_case_sensitive(self):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/timeseries_with_mixedcase_columns.csv",
            "--create-missing-signals",
            "--case-sensitive-signals",
        ]
        script = LoadTimeSeriesFromFile(args)
        self.client.signal_api.get_signal_iterator.side_effect = self._list_signal_mixedcase
        self.client.entity_api.get_entity_type_iterator.side_effect = self._list_entity_types
        script.run_script(self.client, script.parse_arguments())

        call_args_list = self.client.time_series_api.bulk_upsert_time_series.call_args_list
        self.assertEqual(1, len(call_args_list))
        self.assertEqual(0, len(self.client.signal_api.update_signal.call_args_list))
        series = call_args_list[0][0][0]
        self.assertEqual(1, len(series))

        pd.testing.assert_series_equal(
            pd.Series(
                [1, 2, 3, 4, 5],
                pd.MultiIndex.from_arrays(
                    [
                        pd.date_range("2021-01-01", periods=5, tz=tz.tzutc()),
                        pd.date_range("2021-01-01", periods=5, tz=tz.tzutc()),
                    ]
                ),
                name="entityTypes/brand/entities/ns.A_brand/signals/ns.Signal1",
            ),
            series[0],
            check_freq=False,
        )

    def test_load_time_series_with_mixedcase_signals_existing_and_entity_type_nonexisting_cs(
        self,
    ):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/timeseries_with_mixedcase_columns.csv",
            "--create-missing-signals",
            "--case-sensitive",
        ]
        script = LoadTimeSeriesFromFile(args)
        self.client.signal_api.get_signal_iterator.side_effect = self._list_signal_mixedcase
        self.client.entity_api.get_entity_type_iterator.side_effect = self._list_entity_types

        script.run_script(self.client, script.parse_arguments())

        call_args_list = self.client.time_series_api.bulk_upsert_time_series.call_args_list
        self.assertEqual(1, len(call_args_list))
        self.assertEqual(0, len(self.client.signal_api.update_signal.call_args_list))
        series = call_args_list[0][0][0]
        self.assertEqual(1, len(series))

        pd.testing.assert_series_equal(
            pd.Series(
                [1, 2, 3, 4, 5],
                pd.MultiIndex.from_arrays(
                    [
                        pd.date_range("2021-01-01", periods=5, tz=tz.tzutc()),
                        pd.date_range("2021-01-01", periods=5, tz=tz.tzutc()),
                    ]
                ),
                name="entityTypes/brand/entities/ns.A_brand/signals/ns.Signal1",
            ),
            series[0],
            check_freq=False,
        )

    def test_load_time_series_default_optimise(
        self,
    ):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/timeseries_known_time.csv",
        ]
        script = LoadTimeSeriesFromFile(args)

        script.run_script(self.client, script.parse_arguments())

        call_args_list = self.client.time_series_api.bulk_upsert_time_series.call_args_list
        self.assertIsNone(call_args_list[0][1]["should_optimise"])

    def test_load_time_series_optimise(
        self,
    ):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/timeseries_known_time.csv",
            "--optimise",
        ]
        script = LoadTimeSeriesFromFile(args)

        script.run_script(self.client, script.parse_arguments())

        call_args_list = self.client.time_series_api.bulk_upsert_time_series.call_args_list
        self.assertTrue(call_args_list[0][1]["should_optimise"])

    def test_load_time_series_no_optimise(
        self,
    ):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/timeseries_known_time.csv",
            "--no-optimise",
        ]
        script = LoadTimeSeriesFromFile(args)

        script.run_script(self.client, script.parse_arguments())

        call_args_list = self.client.time_series_api.bulk_upsert_time_series.call_args_list
        self.assertFalse(call_args_list[0][1]["should_optimise"])

    def _list_signal(self):
        return iter(
            [
                Signal("signals/ns.signal1", "The Signal", "A description of the signal"),
                Signal("signals/ns.signal2", "The Other Signal", "A description of the signal"),
            ]
        )

    def _list_signal_uppercase(self):
        return iter([Signal("signals/ns.SIGNAL1", "The Signal", "A description of the signal")])

    def _list_signal_mixedcase(self):
        return iter([Signal("signals/ns.Signal1", "The Signal", "A description of the signal")])

    def _list_entity_types(self):
        return iter([EntityType("entityTypes/brand", "", "", False)])

    def _list_entity_types_uppercase(self):
        return iter([EntityType("entityTypes/BRAND", "", "", False)])


if __name__ == "__main__":
    unittest.main()
