import unittest
from unittest import mock

from exabel_data_sdk.client.api.data_classes.paging_result import PagingResult
from exabel_data_sdk.client.api.data_classes.signal import Signal
from exabel_data_sdk.client.api.signal_api import SignalApi
from exabel_data_sdk.client.client_config import ClientConfig


class TestSignalApi(unittest.TestCase):
    def test_get_signal_iterator(self):
        signal_api = SignalApi(ClientConfig("api-key"))
        signal = mock.create_autospec(Signal)
        signal_api.list_signals = mock.MagicMock()
        signal_api.list_signals.side_effect = [
            PagingResult([signal] * 1000, next_page_token="1000", total_size=1100),
            PagingResult([signal] * 100, next_page_token="~~~", total_size=1100),
            AssertionError("Should not be called"),
        ]
        signals = list(signal_api.get_signal_iterator())
        self.assertEqual(1100, len(signals))
        self.assertSequenceEqual([signal] * 1100, signals)
        signal_api.list_signals.assert_has_calls(
            [
                mock.call(page_token=None, page_size=1000),
                mock.call(page_token="1000", page_size=1000),
            ]
        )
