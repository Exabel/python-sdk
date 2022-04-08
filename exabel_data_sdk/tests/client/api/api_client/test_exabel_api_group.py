import unittest

from exabel_data_sdk.client.api.api_client.exabel_api_group import ExabelApiGroup
from exabel_data_sdk.client.client_config import ClientConfig


class TestExabelApiGroup(unittest.TestCase):
    def test_get_host(self):
        config = ClientConfig(api_key="123", data_api_host="localhost")
        self.assertEqual("localhost", ExabelApiGroup.DATA_API.get_host(config))
        self.assertEqual(
            "management.api.exabel.com", ExabelApiGroup.MANAGEMENT_API.get_host(config)
        )

    def test_get_port(self):
        config = ClientConfig(api_key="123", analytics_api_port=123)
        self.assertEqual(123, ExabelApiGroup.ANALYTICS_API.get_port(config))
        self.assertEqual(21443, ExabelApiGroup.MANAGEMENT_API.get_port(config))
