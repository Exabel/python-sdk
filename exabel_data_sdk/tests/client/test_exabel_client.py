import unittest
from unittest import mock

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.namespace import Namespace


class TestExabelClient(unittest.TestCase):
    def test_initialize(self):
        client = ExabelClient(api_key="123")
        self.assertIsNotNone(client.entity_api)
        self.assertIsNotNone(client.time_series_api)
        self.assertIsNotNone(client.relationship_api)
        self.assertIsNotNone(client.signal_api)

    def test_namespace(self):
        client = ExabelClient(api_key="123")
        with mock.patch.object(client, "namespace_api") as mock_namespace_api:
            mock_namespace_api.get_writeable_namespace.return_value = Namespace(
                name="namespaces/ns", writeable=True
            )
            actual_namespace = client.namespace

        self.assertEqual("ns", actual_namespace)
