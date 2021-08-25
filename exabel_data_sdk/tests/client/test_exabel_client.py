import unittest

from exabel_data_sdk import ExabelClient


class TestExabelClient(unittest.TestCase):
    def test_initialize(self):
        client = ExabelClient(api_key="123")
        self.assertIsNotNone(client.entity_api)
        self.assertIsNotNone(client.time_series_api)
        self.assertIsNotNone(client.relationship_api)
        self.assertIsNotNone(client.signal_api)
