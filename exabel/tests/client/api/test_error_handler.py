from unittest.mock import MagicMock

import pytest
from grpc import RpcError, StatusCode

from exabel.client.api.data_classes.request_error import ErrorType, RequestError
from exabel.client.api.error_handler import (
    grpc_status_to_error_type,
    handle_grpc_error,
    is_status_detail,
)


class TestHttpStatusToErrorType:
    def test_is_status_detail(self):
        status_detail = MagicMock(spec=["key", "value"])
        status_detail.key = "grpc-status-details-anything"
        assert is_status_detail(status_detail)
        status_detail.key = "not-grpc-status-details-anything"
        assert not is_status_detail(status_detail)
        status_detail = MagicMock(spec=["key"])
        assert not is_status_detail(status_detail)
        status_detail = MagicMock(spec=["value"])
        assert not is_status_detail(status_detail)

    def test_grpc_status_to_error_type(self):
        assert ErrorType.NOT_FOUND == grpc_status_to_error_type(StatusCode.NOT_FOUND)
        assert ErrorType.ALREADY_EXISTS == grpc_status_to_error_type(StatusCode.ALREADY_EXISTS)
        assert ErrorType.INVALID_ARGUMENT == grpc_status_to_error_type(StatusCode.INVALID_ARGUMENT)
        assert ErrorType.PERMISSION_DENIED == grpc_status_to_error_type(
            StatusCode.PERMISSION_DENIED
        )
        assert ErrorType.UNAVAILABLE == grpc_status_to_error_type(StatusCode.UNAVAILABLE)
        assert ErrorType.TIMEOUT == grpc_status_to_error_type(StatusCode.DEADLINE_EXCEEDED)
        assert ErrorType.RESOURCE_EXHAUSTED == grpc_status_to_error_type(
            StatusCode.RESOURCE_EXHAUSTED
        )
        assert ErrorType.INTERNAL == grpc_status_to_error_type(StatusCode.INTERNAL)
        assert ErrorType.INTERNAL == grpc_status_to_error_type(StatusCode.DATA_LOSS)

    def test_handle_grpc_error(self):
        @handle_grpc_error
        def raise_grpc_error(status_code: StatusCode):
            error = RpcError()
            error.code = MagicMock(return_value=status_code)
            error.details = MagicMock(return_value="Error details")
            error.trailing_metadata = MagicMock(return_value=[])
            raise error

        for status_code in StatusCode:
            with pytest.raises(RequestError) as context:
                raise_grpc_error(status_code)
            assert grpc_status_to_error_type(status_code) == context.value.error_type
            assert "Error details" == context.value.message

    def test_reraise_non_grpc_error_as_request_error(self):
        @handle_grpc_error
        def raise_value_error():
            raise ValueError("Not an RPC error")

        with pytest.raises(RequestError) as context:
            raise_value_error()
        assert ErrorType.INTERNAL == context.value.error_type
        assert "Not an RPC error" == context.value.message
