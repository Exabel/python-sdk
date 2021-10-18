from enum import Enum, unique


@unique
class ErrorType(Enum):
    """
    Error types.
    """

    # Resource was not found.
    NOT_FOUND = 0
    # Resource already exists.
    ALREADY_EXISTS = 1
    # An invalid argument was provided.
    INVALID_ARGUMENT = 2
    # The operation was rejected because the system is not in
    # a state required for the operation's execution.
    FAILED_PRECONDITION = 3
    # Missing access to resource.
    PERMISSION_DENIED = 4
    # Not able to connect to Exabel API.
    UNAVAILABLE = 5
    # Timeout.
    TIMEOUT = 6
    # Any internal error.
    INTERNAL = 10

    def retryable(self) -> bool:
        """Return whether it makes sense to retry the request if this error is given."""
        return self in (ErrorType.UNAVAILABLE, ErrorType.TIMEOUT, ErrorType.INTERNAL)


class RequestError(Exception):
    """
    Represents an error returned from the Exabel Api.

    Attributes:
        error_type (ErrorType): Type of error.
        message (str):          Exception message.
    """

    def __init__(self, error_type: ErrorType, message: str = None):
        """
        Create a new RequestError.

        Args:
            error_type: Type of error.
            message:    Exception message.
        """
        super().__init__(message)
        self.error_type = error_type
        self.message = message
