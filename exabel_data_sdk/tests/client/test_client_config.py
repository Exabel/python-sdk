import unittest

from exabel_data_sdk.client.client_config import ClientConfig


class TestExabelClient(unittest.TestCase):
    def test_default_config(self):
        config = ClientConfig(api_key="123")
        self.assertEqual("123", config.api_key)
        self.assertEqual("Exabel Python SDK", config.client_name)
        self.assertEqual("data.api.exabel.com", config.data_api_host)
        self.assertEqual("analytics.api.exabel.com", config.analytics_api_host)
        self.assertEqual("management.api.exabel.com", config.management_api_host)
        self.assertEqual(21443, config.data_api_port)
        self.assertEqual(60, config.timeout)

    def test_non_default_values(self):
        config = ClientConfig(
            api_key="123",
            client_name="my client",
            data_api_host="foo.bar.com",
            data_api_port=1234,
            timeout=45,
        )
        self.assertEqual("123", config.api_key)
        self.assertEqual("my client", config.client_name)
        self.assertEqual("foo.bar.com", config.data_api_host)
        self.assertEqual(1234, config.data_api_port)
        self.assertEqual(45, config.timeout)
