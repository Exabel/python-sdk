import unittest

from exabel_data_sdk.client.api.data_classes.request_error import ErrorType
from exabel_data_sdk.client.api.error_handler import http_status_to_error_type


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
