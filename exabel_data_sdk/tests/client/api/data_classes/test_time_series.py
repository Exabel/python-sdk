import unittest

import pandas as pd
from dateutil import tz

from exabel_data_sdk.client.api.data_classes.time_series import (
    Dimension,
    TimeSeries,
    TimeSeriesResourceName,
    Unit,
    Units,
)


class TestTimeSeriesResourceName(unittest.TestCase):
    def setUp(self) -> None:
        self.ts_name = TimeSeriesResourceName("entity_type", "entity", "signal")

    def test_time_series_resource_name(self) -> None:
        self.assertEqual(self.ts_name.entity_type, "entity_type")
        self.assertEqual(self.ts_name.entity, "entity")
        self.assertEqual(self.ts_name.signal, "signal")

    def test_entity_name(self) -> None:
        self.assertEqual(self.ts_name.entity_name, "entityTypes/entity_type/entities/entity")

    def test_signal_name(self) -> None:
        self.assertEqual(self.ts_name.signal_name, "signals/signal")

    def test_canonical_name(self) -> None:
        ts_name = TimeSeriesResourceName("entity_type", "entity", "signal")
        self.assertEqual(
            ts_name.canonical_name, "entityTypes/entity_type/entities/entity/signals/signal"
        )

    def test_from_string(self) -> None:
        ts_name = TimeSeriesResourceName.from_string(
            "entityTypes/entity_type/entities/entity/signals/signal"
        )
        self.assertEqual(ts_name.entity_type, "entity_type")
        self.assertEqual(ts_name.entity, "entity")
        self.assertEqual(ts_name.signal, "signal")

        ts_name = TimeSeriesResourceName.from_string(
            "signals/signal/entityTypes/entity_type/entities/entity"
        )
        self.assertEqual(ts_name.entity_type, "entity_type")
        self.assertEqual(ts_name.entity, "entity")
        self.assertEqual(ts_name.signal, "signal")

    def test_from_string__unparsable_should_fail(self) -> None:
        with self.assertRaises(ValueError):
            TimeSeriesResourceName.from_string("")
        with self.assertRaises(ValueError):
            TimeSeriesResourceName.from_string("entityTypes/entity_type/entities/entity")
        with self.assertRaises(ValueError):
            TimeSeriesResourceName.from_string("signals/signal")
        with self.assertRaises(ValueError):
            TimeSeriesResourceName.from_string(
                "relationshipTypes/REL_TYPE/entityTypes/entity_type/entities/entity"
            )
        with self.assertRaises(ValueError):
            TimeSeriesResourceName.from_string(
                "entityTypes/entity_type/entities/entity/signals/signal/something"
            )
        with self.assertRaises(ValueError):
            TimeSeriesResourceName.from_string(
                "signals/signal/entityTypes/entity_type/entities/entity/something"
            )


class TestTimeSeries(unittest.TestCase):
    def test_proto_conversion(self):
        time_series = TimeSeries(
            series=pd.Series(
                [1, 2, 3],
                index=pd.MultiIndex.from_arrays(
                    [
                        pd.DatetimeIndex(["2023-01-01", "2023-01-02", "2023-01-03"], tz=tz.tzutc()),
                        pd.DatetimeIndex(["2021-01-02", "2021-01-04", "2023-01-05"], tz=tz.tzutc()),
                    ]
                ),
                name="entityTypes/country/entities/no/signals/customerA.revenue",
                dtype="float64",
            ),
            units=Units(
                units=[Unit(dimension=Dimension.from_string("currency"), unit="USD", exponent=1)],
                description="description",
            ),
        )
        time_series_proto_converted = TimeSeries.from_proto(time_series.to_proto())
        pd.testing.assert_series_equal(time_series.series, time_series_proto_converted.series)
        self.assertEqual(time_series.units, time_series_proto_converted.units)

    def test_proto_conversion__no_known_time(self):
        time_series = TimeSeries(
            series=pd.Series(
                [1, 2, 3],
                index=[
                    pd.Timestamp("2023-10-01", tz=tz.tzutc()),
                    pd.Timestamp("2023-10-02", tz=tz.tzutc()),
                    pd.Timestamp("2023-10-03", tz=tz.tzutc()),
                ],
                name="entityTypes/country/entities/no/signals/customerA.revenue",
                dtype="float64",
            ),
            units=Units(
                units=[Unit(dimension=Dimension.from_string("currency"), unit="USD", exponent=1)],
                description="description",
            ),
        )
        time_series_proto_converted = TimeSeries.from_proto(time_series.to_proto())
        pd.testing.assert_series_equal(time_series.series, time_series_proto_converted.series)
        self.assertEqual(time_series.units, time_series_proto_converted.units)

    def test_time_series_name(self):
        time_series = TimeSeries(
            series=pd.Series([]),
        )
        time_series.name = "entityTypes/country/entities/no/signals/customerA.revenue"
        self.assertEqual(
            time_series.name, "entityTypes/country/entities/no/signals/customerA.revenue"
        )
        self.assertEqual(
            time_series.series.name, "entityTypes/country/entities/no/signals/customerA.revenue"
        )


class TestUnits(unittest.TestCase):
    def test_proto_conversion(self):
        units = Units(
            units=[
                Unit(Dimension.from_string("currency"), "USD", 1),
                Unit(Dimension.from_string("time"), "month", -1),
            ],
            description="description",
        )
        self.assertEqual(units, Units.from_proto(units.to_proto()))
