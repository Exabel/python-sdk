import unittest

from exabel_data_sdk.client.client_config import ClientConfig


class TestExabelClient(unittest.TestCase):
    def test_default_config(self):
        config = ClientConfig(api_key="123")
        self.assertEqual("123", config.api_key)
        self.assertEqual("Exabel Python SDK", config.client_name)
        self.assertEqual("data.api.exabel.com", config.host)
        self.assertEqual(21443, config.port)
        self.assertEqual(30, config.timeout)

    def test_non_default_values(self):
        config = ClientConfig(
            api_key="123", client_name="my client", host="foo.bar.com", port=1234, timeout=45
        )
        self.assertEqual("123", config.api_key)
        self.assertEqual("my client", config.client_name)
        self.assertEqual("foo.bar.com", config.host)
        self.assertEqual(1234, config.port)
        self.assertEqual(45, config.timeout)
