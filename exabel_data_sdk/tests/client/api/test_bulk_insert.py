import unittest

from exabel_data_sdk.client.api.bulk_insert import _get_backoff


class TestEntityApi(unittest.TestCase):
    def test_get_backoff(self):
        self.assertEqual(1.0, _get_backoff(0))
        self.assertEqual(2.0, _get_backoff(1))
        self.assertEqual(4.0, _get_backoff(2))
        self.assertEqual(8.0, _get_backoff(3))
        self.assertEqual(16.0, _get_backoff(4))
        self.assertEqual(32.0, _get_backoff(5))
        self.assertEqual(60.0, _get_backoff(6))
