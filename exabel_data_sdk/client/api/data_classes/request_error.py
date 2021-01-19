from enum import Enum


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


class RequestError(Exception):
    """Represents an error returned from the Exabel Api."""

    def __init__(self, error_type: ErrorType, message: str = None):
        """
        Create a new RequestError.

        Args:
            error_type: type of error
            message:    exception message
        """
        super().__init__(message)
        self.error_type = error_type
        self.message = message
