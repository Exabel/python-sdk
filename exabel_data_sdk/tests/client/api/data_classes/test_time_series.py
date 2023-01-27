import unittest

from exabel_data_sdk.client.api.data_classes.time_series import TimeSeriesResourceName


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
