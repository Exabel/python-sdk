import unittest

from exabel_data_sdk.client.api.data_classes.derived_signal import (
    DerivedSignal,
    DerivedSignalMetaData,
    DerivedSignalUnit,
)
from exabel_data_sdk.stubs.exabel.api.data.v1.signal_messages_pb2 import (
    DerivedSignal as ProtoDataApiDerivedSignal,
)
from exabel_data_sdk.stubs.exabel.api.math.aggregation_pb2 import Aggregation
from exabel_data_sdk.stubs.exabel.api.math.change_pb2 import Change


class TestDerivedSignal(unittest.TestCase):
    def test_from_analytics_api_proto(self):
        derived_signal = DerivedSignal(
            name="derivedSignals/456",
            label="enhanced_signal",
            expression="va_actual(123)",
            description="enhanced signal with full metadata",
            display_name="Enhanced Signal",
            metadata=DerivedSignalMetaData(
                unit=DerivedSignalUnit.NUMBER,
                decimals=3,
                downsampling_method=Aggregation.MEAN,
                change=Change.RELATIVE,
            ),
        )
        converted = DerivedSignal.from_analytics_api_proto(derived_signal.to_analytics_api_proto())
        self.assertEqual(derived_signal, converted)
        self.assertEqual(converted.metadata.downsampling_method, Aggregation.MEAN)
        self.assertEqual(converted.metadata.change, Change.RELATIVE)

    def test_from_data_api_proto(self):
        data_api_signal = ProtoDataApiDerivedSignal(
            name="derivedSignals/456",
            label="enum_signal",
            expression="va_actual(123)",
            description="signal with enums",
            display_name="Enum Signal",
            downsampling_method=Aggregation.MEAN,
            change=Change.RELATIVE,
        )
        signal = DerivedSignal.from_data_api_proto(data_api_signal)
        self.assertEqual(signal.metadata.downsampling_method, Aggregation.MEAN)
        self.assertEqual(signal.metadata.change, Change.RELATIVE)
