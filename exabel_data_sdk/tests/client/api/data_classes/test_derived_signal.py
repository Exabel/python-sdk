import unittest

from exabel_data_sdk.client.api.data_classes.derived_signal import (
    DerivedSignal,
    DerivedSignalMetaData,
    DerivedSignalUnit,
)


class TestDerivedSignal(unittest.TestCase):
    def test_proto_conversion(self):
        derived_signal = DerivedSignal(
            name="derivedSignals/123",
            label="test_signal",
            expression="close_price + 1",
            description="price plus one",
            metadata=DerivedSignalMetaData(unit=DerivedSignalUnit.RATIO_DIFFERENCE, decimals=2),
        )
        self.assertEqual(derived_signal, DerivedSignal.from_proto(derived_signal.to_proto()))
