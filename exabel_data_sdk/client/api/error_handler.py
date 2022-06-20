from http import HTTPStatus
from typing import Any, Callable, Optional, TypeVar, cast

from google.rpc.error_details_pb2 import PreconditionFailure as PreconditionFailureProto
from google.rpc.status_pb2 import Status as StatusProto
from grpc import RpcError, StatusCode

from exabel_data_sdk.client.api.data_classes.request_error import (
    ErrorType,
    PreconditionFailure,
    RequestError,
    Violation,
)

TFunction = TypeVar("TFunction", bound=Callable)


def is_status_detail(metadata: Any) -> bool:
    """
    Check if the metadata is a status detail.
    """
    return (
        hasattr(metadata, "key")
        and hasattr(metadata, "value")
        and metadata.key.startswith("grpc-status-details")
    )


def extract_precondition_failure_proto(e: RpcError) -> Optional[PreconditionFailureProto]:
    """
    Try to find a precondition failure in the gRPC exception, which indicates that we have thrown
    the exception with structured precondition failure violations.
    """
    metadata = [m for m in e.trailing_metadata() if is_status_detail(m)]
    statuses = []
    for meta in metadata:
        status = StatusProto()
        status.MergeFromString(meta.value)
        statuses.append(status)

    for detail in [detail for status in statuses for detail in status.details]:
        if detail.Is(PreconditionFailureProto.DESCRIPTOR):
            precondition_failure = PreconditionFailureProto()
            detail.Unpack(precondition_failure)
            return precondition_failure
    return None


def precondition_failure_proto_to_precondition_failure(
    precondition_failure: PreconditionFailureProto = None,
) -> Optional[PreconditionFailure]:
    """Convert PreconditionFailureProto into a PreconditionFailure."""
    if precondition_failure is None:
        return None
    return PreconditionFailure(
        [
            Violation(
                type=violation.type,
                subject=violation.subject,
                description=violation.description,
            )
            for violation in precondition_failure.violations
        ]
    )


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


def http_status_to_error_type(status_code: int) -> ErrorType:
    """
    Map an HTTP status code to an ErrorType.
    """
    if status_code == HTTPStatus.NOT_FOUND:
        return ErrorType.NOT_FOUND
    if status_code == HTTPStatus.CONFLICT:
        return ErrorType.ALREADY_EXISTS
    if status_code == HTTPStatus.BAD_REQUEST:
        return ErrorType.INVALID_ARGUMENT
    if status_code == HTTPStatus.FORBIDDEN:
        return ErrorType.PERMISSION_DENIED
    if status_code == HTTPStatus.SERVICE_UNAVAILABLE:
        return ErrorType.UNAVAILABLE
    if status_code == HTTPStatus.GATEWAY_TIMEOUT:
        return ErrorType.TIMEOUT
    return ErrorType.INTERNAL


def handle_grpc_error(function: TFunction) -> TFunction:
    """Convert any gRPC error raised by the decorated function into a RequestError."""

    def error_handler_decorator(*args: Any, **kwargs: Any) -> Any:
        try:
            return function(*args, **kwargs)
        except RpcError as error:
            error_type = grpc_status_to_error_type(error.code())
            precondition_failure_proto = extract_precondition_failure_proto(error)
            precondition_failure = precondition_failure_proto_to_precondition_failure(
                precondition_failure_proto
            )
            raise RequestError(error_type, error.details(), precondition_failure) from error

    return cast(TFunction, error_handler_decorator)
