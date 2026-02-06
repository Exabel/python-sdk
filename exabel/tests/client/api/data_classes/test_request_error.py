from exabel.client.api.data_classes.request_error import ErrorType


class TestErrorType:
    def test_from_precondition_failure_violation(self):
        assert (
            ErrorType.from_precondition_failure_violation_type("NOT_FOUND") == ErrorType.NOT_FOUND
        )
        assert (
            ErrorType.from_precondition_failure_violation_type("FAILED_PRECONDITION")
            == ErrorType.FAILED_PRECONDITION
        )
        assert (
            ErrorType.from_precondition_failure_violation_type("PERMISSION_DENIED")
            == ErrorType.PERMISSION_DENIED
        )
        assert (
            ErrorType.from_precondition_failure_violation_type("UNAVAILABLE")
            == ErrorType.UNAVAILABLE
        )
        assert ErrorType.from_precondition_failure_violation_type("TIMEOUT") == ErrorType.TIMEOUT
        assert ErrorType.from_precondition_failure_violation_type("INTERNAL") == ErrorType.INTERNAL
        assert ErrorType.from_precondition_failure_violation_type("UNKNOWN") == ErrorType.UNKNOWN
        assert (
            ErrorType.from_precondition_failure_violation_type("NOT_A_VALID_TYPE")
            == ErrorType.UNKNOWN
        )
