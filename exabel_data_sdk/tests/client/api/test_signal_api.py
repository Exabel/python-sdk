import unittest
from unittest import mock

from exabel_data_sdk.client.api.data_classes.paging_result import PagingResult
from exabel_data_sdk.client.api.data_classes.signal import Signal
from exabel_data_sdk.client.api.signal_api import SignalApi
from exabel_data_sdk.client.client_config import ClientConfig


class TestSignalApi(unittest.TestCase):
    def test_get_signal_iterator(self):
        signal_api = SignalApi(ClientConfig("api-key"))
        signal_1 = mock.create_autospec(Signal)
        signal_2 = mock.create_autospec(Signal)
        signal_3 = mock.create_autospec(Signal)
        signal_api.list_signals = mock.MagicMock()
        signal_api.list_signals.side_effect = [
            PagingResult([signal_1], next_page_token="1", total_size=3),
            PagingResult([signal_2], next_page_token="2", total_size=3),
            PagingResult([signal_3], next_page_token=None, total_size=3),
            AssertionError("Should not be called"),
        ]
        signals = list(signal_api.get_signal_iterator())
        self.assertEqual(3, len(signals))
        self.assertSequenceEqual([signal_1, signal_2, signal_3], signals)
        signal_api.list_signals.assert_has_calls(
            [
                mock.call(page_token=None),
                mock.call(page_token="1"),
                mock.call(page_token="2"),
            ]
        )
