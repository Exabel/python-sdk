import unittest

from exabel_data_sdk.client.api.data_classes.signal import Signal


class TestSignal(unittest.TestCase):
    def test_proto_conversion(self):
        signal = Signal(
            name="signals/customerA.revenue",
            entity_type="entityTypes/customerA.store",
            display_name="Revenue per store.",
            description="description",
        )
        self.assertEqual(signal, Signal.from_proto(signal.to_proto()))
