import unittest

from exabel_data_sdk.client.api.data_classes.data_set import DataSet


class TestDataSet(unittest.TestCase):
    def test_proto_conversion(self):
        data_set = DataSet(
            name="dataSet/customerA.MyData",
            display_name="Revenue per store.",
            description="description",
            signals=["signals/ns.sig1", "signals/ns.sig2"],
        )
        self.assertEqual(data_set, DataSet.from_proto(data_set.to_proto()))

    def test_constructor_without_signals(self):
        data_set = DataSet(
            name="dataSet/customerA.MyData",
            display_name="Revenue per store.",
            description="description",
        )
        self.assertEqual([], data_set.signals)

    def test_equals(self):
        data_set_1 = DataSet(
            name="dataSet/customerA.MyData",
            display_name="Revenue per store.",
            description="description",
            signals=["signals/ns.sig1", "signals/ns.sig2"],
        )
        data_set_2 = DataSet(
            name="dataSet/customerA.MyData",
            display_name="Revenue per store.",
            description="description",
            signals=["signals/ns.sig2", "signals/ns.sig1"],
        )
        data_set_3 = DataSet(
            name="dataSet/customerA.MyData",
            display_name="Revenue per store.",
            description="description",
            signals=["signals/ns.sig2"],
        )
        self.assertEqual(data_set_1, data_set_2)
        self.assertNotEqual(data_set_1, data_set_3)
