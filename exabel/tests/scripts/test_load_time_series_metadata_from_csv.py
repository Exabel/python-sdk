import unittest
from unittest import mock

import numpy as np
import pandas as pd
import pytest

from exabel import ExabelClient
from exabel.client.api.data_classes.entity_type import EntityType
from exabel.client.api.data_classes.signal import Signal
from exabel.client.api.data_classes.time_series import Dimension, TimeSeries, Unit, Units
from exabel.client.api.entity_api import EntityApi
from exabel.client.api.signal_api import SignalApi
from exabel.client.api.time_series_api import TimeSeriesApi
from exabel.scripts.load_time_series_metadata_from_file import (
    LoadTimeSeriesMetaDataFromFile,
)
from exabel.services.file_time_series_parser import MetaDataSignalNamesInRows

common_args = ["script-name", "--sep", ";", "--api-key", "123"]


class TestUploadTimeSeriesMetadata(unittest.TestCase):
    def setUp(self) -> None:
        self.client = mock.create_autospec(ExabelClient)
        self.client.entity_api = mock.create_autospec(EntityApi)
        self.client.signal_api = mock.create_autospec(SignalApi)
        self.client.time_series_api = mock.create_autospec(TimeSeriesApi)

        self.client.namespace = "ns"
        self.client.signal_api.get_signal_iterator.side_effect = self._list_signal
        self.client.entity_api.get_entity_type_iterator.side_effect = self._list_entity_types

    def test_get_series(self):
        data = [
            ["a", "signal1", "USD"],
            ["a", "signal1", "USD"],
            ["a", "signal2", "EUR"],
            ["b", "signal1", "NOK"],
            ["b", "signal1", np.nan],
        ]
        ts_data = pd.DataFrame(data, columns=["entity", "signal", "currency"])

        parsed_file = MetaDataSignalNamesInRows.from_data_frame(ts_data, self.client.entity_api, "")
        time_series = parsed_file.get_series(prefix="signals/acme.")
        assert 2 == len(time_series.failures)
        assert 2 == len(time_series.valid_series)

        assert (
            TimeSeries(
                series=pd.Series([], name="b/signals/acme.signal1", dtype=object),
                units=Units(units=[Unit(dimension=Dimension.DIMENSION_CURRENCY, unit="NOK")]),
            )
            == time_series.failures[0].resource
        )
        assert (
            TimeSeries(series=pd.Series([], name="b/signals/acme.signal1", dtype=object))
            == time_series.failures[1].resource
        )
        assert (
            TimeSeries(
                series=pd.Series([], name="a/signals/acme.signal1", dtype=object),
                units=Units(units=[Unit(dimension=Dimension.DIMENSION_CURRENCY, unit="USD")]),
            )
            == time_series.valid_series[0]
        )

        assert (
            TimeSeries(
                series=pd.Series([], name="a/signals/acme.signal2", dtype=object),
                units=Units(units=[Unit(dimension=Dimension.DIMENSION_CURRENCY, unit="EUR")]),
            )
            == time_series.valid_series[1]
        )

    def test_get_series__skip_validation(self):
        data = [
            ["a", "signal1", "USD"],
            ["a", "signal2", "EUR"],
            ["b", "signal1", "NOK"],
            ["b", "signal1", np.nan],
        ]

        ts_data = pd.DataFrame(data, columns=["entity", "signal", "currency"])
        parsed_file = MetaDataSignalNamesInRows.from_data_frame(ts_data, self.client.entity_api, "")
        time_series = parsed_file.get_series("signals/acme.", skip_validation=True)
        assert [] == time_series.failures
        assert 4 == len(time_series.valid_series)

        assert (
            TimeSeries(series=pd.Series([], name="b/signals/acme.signal1", dtype=object))
            == time_series.valid_series[3]
        )

    def test_read_file__description(self):
        args = common_args + [
            "--filename",
            "./exabel/tests/resources/data/timeseries_metadata_description.csv",
        ]
        script = LoadTimeSeriesMetaDataFromFile(args)
        script.run_script(self.client, script.parse_arguments())

        call_args_list = self.client.time_series_api.bulk_upsert_time_series.call_args_list
        assert 1 == len(call_args_list)
        series = call_args_list[0][0][0]
        assert 2 == len(series)
        series_by_name = {s.name: s for s in series}

        ts = TimeSeries(
            series=pd.Series(
                [], name="entityTypes/company/entities/company_A/signals/ns.signal1", dtype=object
            ),
            units=Units(description="percent"),
        )
        assert ts == series_by_name["entityTypes/company/entities/company_A/signals/ns.signal1"]
        ts = TimeSeries(
            series=pd.Series(
                [], name="entityTypes/company/entities/company_A/signals/ns.signal2", dtype=object
            ),
            units=Units(description="ratio"),
        )
        assert ts == series_by_name["entityTypes/company/entities/company_A/signals/ns.signal2"]

    def test_read_file__currency(self):
        args = common_args + [
            "--filename",
            "./exabel/tests/resources/data/timeseries_metadata_currency.csv",
        ]
        script = LoadTimeSeriesMetaDataFromFile(args)
        script.run_script(self.client, script.parse_arguments())

        call_args_list = self.client.time_series_api.bulk_upsert_time_series.call_args_list
        assert 1 == len(call_args_list)
        series = call_args_list[0][0][0]
        assert 3 == len(series)
        series_by_name = {s.name: s for s in series}

        ts = TimeSeries(
            series=pd.Series(
                [], name="entityTypes/company/entities/company_A/signals/ns.signal1", dtype=object
            ),
            units=Units(
                units=[Unit(dimension=Dimension.DIMENSION_CURRENCY, unit="USD")],
            ),
        )
        assert ts == series_by_name["entityTypes/company/entities/company_A/signals/ns.signal1"]
        ts = TimeSeries(
            series=pd.Series(
                [], name="entityTypes/company/entities/company_A/signals/ns.signal2", dtype=object
            ),
            units=Units(
                units=[Unit(dimension=Dimension.DIMENSION_CURRENCY, unit="EUR")],
                description="millions",
            ),
        )
        assert ts == series_by_name["entityTypes/company/entities/company_A/signals/ns.signal2"]
        ts = TimeSeries(
            series=pd.Series(
                [], name="entityTypes/company/entities/company_B/signals/ns.signal1", dtype=object
            ),
            units=Units(units=[Unit(dimension=Dimension.DIMENSION_CURRENCY, unit="NOK")]),
        )
        assert ts == series_by_name["entityTypes/company/entities/company_B/signals/ns.signal1"]

    def test_read_file__unit(self):
        args = common_args + [
            "--filename",
            "./exabel/tests/resources/data/timeseries_metadata_unit.csv",
        ]
        script = LoadTimeSeriesMetaDataFromFile(args)
        script.run_script(self.client, script.parse_arguments())

        call_args_list = self.client.time_series_api.bulk_upsert_time_series.call_args_list
        assert 1 == len(call_args_list)
        series = call_args_list[0][0][0]
        assert 5 == len(series)
        series_by_name = {s.name: s for s in series}

        ts = TimeSeries(
            series=pd.Series(
                [], name="entityTypes/company/entities/company_A/signals/ns.signal1", dtype=object
            ),
            units=Units(
                units=[Unit(dimension=Dimension.DIMENSION_RATIO, unit="percent")],
            ),
        )
        assert ts == series_by_name["entityTypes/company/entities/company_A/signals/ns.signal1"]
        ts = TimeSeries(
            series=pd.Series(
                [], name="entityTypes/company/entities/company_A/signals/ns.signal2", dtype=object
            ),
            units=Units(
                units=[Unit(dimension=Dimension.DIMENSION_UNKNOWN, unit="bps")],
            ),
        )
        assert ts == series_by_name["entityTypes/company/entities/company_A/signals/ns.signal2"]
        ts = TimeSeries(
            series=pd.Series(
                [], name="entityTypes/company/entities/company_B/signals/ns.signal1", dtype=object
            ),
            units=Units(
                units=[Unit(dimension=Dimension.DIMENSION_RATIO, unit="ratio")],
            ),
        )
        assert ts == series_by_name["entityTypes/company/entities/company_B/signals/ns.signal1"]
        ts = TimeSeries(
            series=pd.Series(
                [], name="entityTypes/company/entities/company_B/signals/ns.signal2", dtype=object
            ),
            units=Units(
                units=[Unit(dimension=Dimension.DIMENSION_RATIO, unit="%")],
            ),
        )
        assert ts == series_by_name["entityTypes/company/entities/company_B/signals/ns.signal2"]
        ts = TimeSeries(
            series=pd.Series(
                [], name="entityTypes/company/entities/company_A/signals/ns.signal3", dtype=object
            ),
        )
        assert ts == series_by_name["entityTypes/company/entities/company_A/signals/ns.signal3"]

    def test_read_file__unit_and_currency(self):
        args = common_args + [
            "--filename",
            "./exabel/tests/resources/data/timeseries_metadata_unit_and_currency.csv",
        ]
        script = LoadTimeSeriesMetaDataFromFile(args)
        script.run_script(self.client, script.parse_arguments())

        call_args_list = self.client.time_series_api.bulk_upsert_time_series.call_args_list
        assert 1 == len(call_args_list)
        series = call_args_list[0][0][0]
        assert 3 == len(series)
        series_by_name = {s.name: s for s in series}

        ts = TimeSeries(
            series=pd.Series(
                [], name="entityTypes/company/entities/company_A/signals/ns.signal1", dtype=object
            ),
            units=Units(
                units=[Unit(dimension=Dimension.DIMENSION_CURRENCY, unit="NOK")],
            ),
        )
        assert ts == series_by_name["entityTypes/company/entities/company_A/signals/ns.signal1"]
        ts = TimeSeries(
            series=pd.Series(
                [], name="entityTypes/company/entities/company_B/signals/ns.signal1", dtype=object
            ),
            units=Units(
                units=[Unit(dimension=Dimension.DIMENSION_CURRENCY, unit="USD")],
            ),
        )
        assert ts == series_by_name["entityTypes/company/entities/company_B/signals/ns.signal1"]
        ts = TimeSeries(
            series=pd.Series(
                [], name="entityTypes/company/entities/company_A/signals/ns.signal2", dtype=object
            ),
            units=Units(
                units=[Unit(dimension=Dimension.DIMENSION_RATIO, unit="percent")],
            ),
        )
        assert ts == series_by_name["entityTypes/company/entities/company_A/signals/ns.signal2"]

    def test_read_file__invalid(self):
        args = common_args + [
            "--filename",
            "./exabel/tests/resources/data/timeseries_metadata_invalid.csv",
        ]
        script = LoadTimeSeriesMetaDataFromFile(args)

        with pytest.raises(SystemExit):
            script.run_script(self.client, script.parse_arguments())

    def test_read_file__invalid2(self):
        args = common_args + [
            "--filename",
            "./exabel/tests/resources/data/timeseries_metadata_invalid2.csv",
        ]
        script = LoadTimeSeriesMetaDataFromFile(args)

        with pytest.raises(SystemExit):
            script.run_script(self.client, script.parse_arguments())

    def _list_signal(self):
        return iter(
            [
                Signal("signals/ns.signal1", "The Signal", "A description of the signal"),
                Signal("signals/ns.signal2", "The Other Signal", "A description of the signal"),
                Signal("signals/ns.signal3", "Yet Another Signal", "A description of the signal"),
            ]
        )

    def _list_entity_types(self):
        return iter([EntityType("entityTypes/brand", "", "", False)])
