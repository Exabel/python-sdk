import unittest

from exabel_data_sdk.client.api.data_classes.namespace import Namespace


class TestNamespace(unittest.TestCase):
    def test_proto_conversion(self):
        namespace = Namespace(
            name="namespace/ns",
            writeable=True,
        )
        self.assertEqual(namespace, Namespace.from_proto(namespace.to_proto()))
