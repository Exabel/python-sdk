import unittest

from exabel_data_sdk.client.api.proto_utils import from_struct, to_struct


class TestProtoUtils(unittest.TestCase):
    def test_struct_conversion(self):
        values = {"a": False, "b": 3.5, "c": "c_value"}
        self.assertEqual(values, from_struct(to_struct(values)))
