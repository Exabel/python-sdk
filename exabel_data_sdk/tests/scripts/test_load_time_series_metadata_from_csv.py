import unittest
from unittest import mock

import numpy as np
import pandas as pd

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.entity_type import EntityType
from exabel_data_sdk.client.api.data_classes.signal import Signal
from exabel_data_sdk.client.api.data_classes.time_series import Dimension, TimeSeries, Unit, Units
from exabel_data_sdk.client.api.entity_api import EntityApi
from exabel_data_sdk.client.api.signal_api import SignalApi
from exabel_data_sdk.client.api.time_series_api import TimeSeriesApi
from exabel_data_sdk.scripts.load_time_series_metadata_from_file import (
    LoadTimeSeriesMetaDataFromFile,
)
from exabel_data_sdk.services.file_time_series_parser import MetaDataSignalNamesInRows

common_args = ["script-name", "--sep", ";", "--api-key", "123"]


class TestUploadTimeSeries(unittest.TestCase):
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
            ["a", "signal2", "EUR"],
            ["b", "signal1", "NOK"],
            ["b", "signal1", np.nan],
        ]
        ts_data = pd.DataFrame(data, columns=["entity", "signal", "unit"])

        parser = MetaDataSignalNamesInRows.from_data_frame(ts_data, self.client.entity_api, "")
        time_series = parser.get_series(prefix="signals/acme.", unit_type="currency")
        self.assertEqual(2, len(time_series.failures))
        self.assertEqual(2, len(time_series.valid_series))

        self.assertEqual(
            TimeSeries(
                series=pd.Series([], name="b/signals/acme.signal1", dtype=object),
                units=Units(units=[Unit(dimension=Dimension.DIMENSION_CURRENCY, unit="NOK")]),
            ),
            time_series.failures[0].resource,
        )
        self.assertEqual(
            TimeSeries(
                series=pd.Series([], name="b/signals/acme.signal1", dtype=object),
            ),
            time_series.failures[1].resource,
        )
        self.assertEqual(
            TimeSeries(
                series=pd.Series([], name="a/signals/acme.signal1", dtype=object),
                units=Units(units=[Unit(dimension=Dimension.DIMENSION_CURRENCY, unit="USD")]),
            ),
            time_series.valid_series[0],
        )

        self.assertEqual(
            TimeSeries(
                series=pd.Series([], name="a/signals/acme.signal2", dtype=object),
                units=Units(units=[Unit(dimension=Dimension.DIMENSION_CURRENCY, unit="EUR")]),
            ),
            time_series.valid_series[1],
        )

    def test_get_series__skip_validation(self):
        data = [
            ["a", "signal1", "USD"],
            ["a", "signal2", "EUR"],
            ["b", "signal1", "NOK"],
            ["b", "signal1", np.nan],
        ]

        ts_data = pd.DataFrame(data, columns=["entity", "signal", "unit"])
        parser = MetaDataSignalNamesInRows.from_data_frame(ts_data, self.client.entity_api, "")
        time_series = parser.get_series("signals/acme.", skip_validation=True, unit_type="currency")
        self.assertSequenceEqual([], time_series.failures)
        self.assertEqual(4, len(time_series.valid_series))

        self.assertEqual(
            TimeSeries(series=pd.Series([], name="b/signals/acme.signal1", dtype=object)),
            time_series.valid_series[3],
        )

    def test_read_file__no_unit_type_argument(self):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/timeseries_no_unit_type.csv",
        ]
        script = LoadTimeSeriesMetaDataFromFile(args)
        script.run_script(self.client, script.parse_arguments())

        call_args_list = self.client.time_series_api.bulk_upsert_time_series.call_args_list
        self.assertEqual(1, len(call_args_list))
        series = call_args_list[0][0][0]
        self.assertEqual(2, len(series))
        series_by_name = {s.name: s for s in series}

        ts = TimeSeries(
            series=pd.Series(
                [], name="entityTypes/company/entities/company_A/signals/ns.signal1", dtype=object
            ),
            units=Units(description="percent"),
        )
        self.assertEqual(
            ts,
            series_by_name["entityTypes/company/entities/company_A/signals/ns.signal1"],
        )
        ts = TimeSeries(
            series=pd.Series(
                [], name="entityTypes/company/entities/company_A/signals/ns.signal2", dtype=object
            ),
            units=Units(description="ratio"),
        )
        self.assertEqual(
            ts,
            series_by_name["entityTypes/company/entities/company_A/signals/ns.signal2"],
        )

    def test_read_file__unit_type_currency_column(self):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/timeseries_unit_type_currency.csv",
        ]
        script = LoadTimeSeriesMetaDataFromFile(args)
        script.run_script(self.client, script.parse_arguments())

        call_args_list = self.client.time_series_api.bulk_upsert_time_series.call_args_list
        self.assertEqual(1, len(call_args_list))
        series = call_args_list[0][0][0]
        self.assertEqual(3, len(series))
        series_by_name = {s.name: s for s in series}

        ts = TimeSeries(
            series=pd.Series(
                [], name="entityTypes/company/entities/company_A/signals/ns.signal1", dtype=object
            ),
            units=Units(
                units=[Unit(dimension=Dimension.DIMENSION_CURRENCY, unit="USD")],
            ),
        )
        self.assertEqual(
            ts,
            series_by_name["entityTypes/company/entities/company_A/signals/ns.signal1"],
        )
        ts = TimeSeries(
            series=pd.Series(
                [], name="entityTypes/company/entities/company_A/signals/ns.signal2", dtype=object
            ),
            units=Units(
                units=[Unit(dimension=Dimension.DIMENSION_CURRENCY, unit="EUR")],
                description="millions",
            ),
        )
        self.assertEqual(
            ts,
            series_by_name["entityTypes/company/entities/company_A/signals/ns.signal2"],
        )
        ts = TimeSeries(
            series=pd.Series(
                [], name="entityTypes/company/entities/company_B/signals/ns.signal1", dtype=object
            ),
            units=Units(units=[Unit(dimension=Dimension.DIMENSION_CURRENCY, unit="NOK")]),
        )
        self.assertEqual(
            ts,
            series_by_name["entityTypes/company/entities/company_B/signals/ns.signal1"],
        )

    def test_read_file__unit_type_argument(self):
        args = common_args + [
            "--filename",
            "./exabel_data_sdk/tests/resources/data/timeseries_unit_type_argument.csv",
            "--unit-type",
            "unknown",
        ]
        script = LoadTimeSeriesMetaDataFromFile(args)
        script.run_script(self.client, script.parse_arguments())

        call_args_list = self.client.time_series_api.bulk_upsert_time_series.call_args_list
        self.assertEqual(1, len(call_args_list))
        series = call_args_list[0][0][0]
        self.assertEqual(3, len(series))
        series_by_name = {s.name: s for s in series}

        ts = TimeSeries(
            series=pd.Series(
                [], name="entityTypes/company/entities/company_A/signals/ns.signal1", dtype=object
            ),
            units=Units(
                units=[Unit(dimension=Dimension.DIMENSION_UNKNOWN, unit="percent")],
            ),
        )
        self.assertEqual(
            ts,
            series_by_name["entityTypes/company/entities/company_A/signals/ns.signal1"],
        )
        ts = TimeSeries(
            series=pd.Series(
                [], name="entityTypes/company/entities/company_A/signals/ns.signal2", dtype=object
            ),
            units=Units(
                units=[Unit(dimension=Dimension.DIMENSION_UNKNOWN, unit="bps")],
            ),
        )
        self.assertEqual(
            ts,
            series_by_name["entityTypes/company/entities/company_A/signals/ns.signal2"],
        )
        ts = TimeSeries(
            series=pd.Series(
                [], name="entityTypes/company/entities/company_B/signals/ns.signal1", dtype=object
            ),
            units=Units(
                units=[Unit(dimension=Dimension.DIMENSION_UNKNOWN, unit="ratio")],
            ),
        )
        self.assertEqual(
            ts,
            series_by_name["entityTypes/company/entities/company_B/signals/ns.signal1"],
        )

    def _list_signal(self):
        return iter(
            [
                Signal("signals/ns.signal1", "The Signal", "A description of the signal"),
                Signal("signals/ns.signal2", "The Other Signal", "A description of the signal"),
            ]
        )

    def _list_entity_types(self):
        return iter([EntityType("entityTypes/brand", "", "", False)])


if __name__ == "__main__":
    unittest.main()
