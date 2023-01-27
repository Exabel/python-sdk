import unittest
from unittest.mock import MagicMock

from grpc import RpcError, StatusCode

from exabel_data_sdk.client.api.data_classes.request_error import ErrorType, RequestError
from exabel_data_sdk.client.api.error_handler import (
    grpc_status_to_error_type,
    handle_grpc_error,
    is_status_detail,
)


class TestHttpStatusToErrorType(unittest.TestCase):
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

    def test_grpc_status_to_error_type(self):
        self.assertEqual(ErrorType.NOT_FOUND, grpc_status_to_error_type(StatusCode.NOT_FOUND))
        self.assertEqual(
            ErrorType.ALREADY_EXISTS, grpc_status_to_error_type(StatusCode.ALREADY_EXISTS)
        )
        self.assertEqual(
            ErrorType.INVALID_ARGUMENT, grpc_status_to_error_type(StatusCode.INVALID_ARGUMENT)
        )
        self.assertEqual(
            ErrorType.PERMISSION_DENIED, grpc_status_to_error_type(StatusCode.PERMISSION_DENIED)
        )
        self.assertEqual(ErrorType.UNAVAILABLE, grpc_status_to_error_type(StatusCode.UNAVAILABLE))
        self.assertEqual(ErrorType.TIMEOUT, grpc_status_to_error_type(StatusCode.DEADLINE_EXCEEDED))
        self.assertEqual(ErrorType.INTERNAL, grpc_status_to_error_type(StatusCode.INTERNAL))
        self.assertEqual(ErrorType.INTERNAL, grpc_status_to_error_type(StatusCode.DATA_LOSS))

    def test_handle_grpc_error(self):
        @handle_grpc_error
        def raise_grpc_error(status_code: StatusCode):
            error = RpcError()
            error.code = MagicMock(return_value=status_code)
            error.details = MagicMock(return_value="Error details")
            error.trailing_metadata = MagicMock(return_value=[])
            raise error

        for status_code in StatusCode:
            with self.assertRaises(RequestError) as context:
                raise_grpc_error(status_code)
            self.assertEqual(grpc_status_to_error_type(status_code), context.exception.error_type)
            self.assertEqual("Error details", context.exception.message)

    def test_reraise_non_grpc_error_as_request_error(self):
        @handle_grpc_error
        def raise_value_error():
            raise ValueError("Not an RPC error")

        with self.assertRaises(RequestError) as context:
            raise_value_error()
        self.assertEqual(ErrorType.INTERNAL, context.exception.error_type)
        self.assertEqual("Not an RPC error", context.exception.message)
