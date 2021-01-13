from typing import Any, Callable, TypeVar, cast

from grpc import RpcError, StatusCode

from exabel_data_sdk.client.api.data_classes.request_error import ErrorType, RequestError

TFunction = TypeVar("TFunction", bound=Callable)


def grpc_status_to_error_type(status_code: StatusCode) -> ErrorType:
    """
    Map a gRPC status code to an ErrorType.
    """
    if status_code == StatusCode.NOT_FOUND:
        return ErrorType.NOT_FOUND
    if status_code == StatusCode.ALREADY_EXISTS:
        return ErrorType.ALREADY_EXISTS
    if status_code == StatusCode.INVALID_ARGUMENT:
        return ErrorType.INVALID_ARGUMENT
    if status_code == StatusCode.FAILED_PRECONDITION:
        return ErrorType.FAILED_PRECONDITION
    if status_code == StatusCode.PERMISSION_DENIED:
        return ErrorType.PERMISSION_DENIED
    if status_code == StatusCode.UNAVAILABLE:
        return ErrorType.UNAVAILABLE
    if status_code == StatusCode.DEADLINE_EXCEEDED:
        return ErrorType.TIMEOUT
    return ErrorType.INTERNAL


def handle_grpc_error(function: TFunction) -> TFunction:
    """Convert any gRPC error raised by the decorated function into a RequestError."""

    def error_handler_decorator(*args: Any, **kwargs: Any) -> Any:
        try:
            return function(*args, **kwargs)
        except RpcError as error:
            error_type = grpc_status_to_error_type(error.code())
            raise RequestError(error_type, error.details()) from error

    return cast(TFunction, error_handler_decorator)
