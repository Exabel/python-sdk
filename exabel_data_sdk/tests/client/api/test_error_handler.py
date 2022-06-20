import unittest
from unittest.mock import MagicMock

from exabel_data_sdk.client.api.data_classes.request_error import ErrorType
from exabel_data_sdk.client.api.error_handler import http_status_to_error_type, is_status_detail


class TestHttpStatusToErrorType(unittest.TestCase):
    def test_not_found(self):
        self.assertEqual(ErrorType.NOT_FOUND, http_status_to_error_type(404))

    def test_conflict(self):
        self.assertEqual(ErrorType.ALREADY_EXISTS, http_status_to_error_type(409))

    def test_bad_request(self):
        self.assertEqual(ErrorType.INVALID_ARGUMENT, http_status_to_error_type(400))

    def test_forbidden(self):
        self.assertEqual(ErrorType.PERMISSION_DENIED, http_status_to_error_type(403))

    def test_service_unavailable(self):
        self.assertEqual(ErrorType.UNAVAILABLE, http_status_to_error_type(503))

    def test_gateway_timeout(self):
        self.assertEqual(ErrorType.TIMEOUT, http_status_to_error_type(504))

    def test_other(self):
        self.assertEqual(ErrorType.INTERNAL, http_status_to_error_type(418))

    def test_is_status_detail(self):
        status_detail = MagicMock(spec=["key", "value"])
        status_detail.key = "grpc-status-details-anything"
        self.assertTrue(is_status_detail(status_detail))
        status_detail.key = "not-grpc-status-details-anything"
        self.assertFalse(is_status_detail(status_detail))
        status_detail = MagicMock(spec=["key"])
        self.assertFalse(is_status_detail(status_detail))
        status_detail = MagicMock(spec=["value"])
        self.assertFalse(is_status_detail(status_detail))
