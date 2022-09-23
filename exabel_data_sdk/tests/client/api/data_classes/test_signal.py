import unittest

from exabel_data_sdk.client.api.data_classes.signal import Signal


class TestSignal(unittest.TestCase):
    def test_proto_conversion(self):
        signal = Signal(
            name="signals/customerA.revenue",
            display_name="Revenue per store.",
            description="description",
            read_only=True,
        )
        self.assertEqual(signal, Signal.from_proto(signal.to_proto()))

    def test_equality(self):
        signal1 = Signal(
            name="signals/customerA.revenue",
            display_name="Revenue per store.",
            description="description",
            entity_types=["entityType1", "entityType2"],
        )
        signal2 = Signal(
            name="signals/customerA.revenue",
            display_name="Revenue per store.",
            description="description",
        )
        self.assertEqual(signal1, signal2)
