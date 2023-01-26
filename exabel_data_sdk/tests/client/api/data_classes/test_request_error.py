import unittest

from exabel_data_sdk.client.api.data_classes.request_error import ErrorType


class TestErrorType(unittest.TestCase):
    def test_from_precondition_failure_violation(self):
        self.assertEqual(
            ErrorType.from_precondition_failure_violation_type("NOT_FOUND"), ErrorType.NOT_FOUND
        )
        self.assertEqual(
            ErrorType.from_precondition_failure_violation_type("FAILED_PRECONDITION"),
            ErrorType.FAILED_PRECONDITION,
        )
        self.assertEqual(
            ErrorType.from_precondition_failure_violation_type("PERMISSION_DENIED"),
            ErrorType.PERMISSION_DENIED,
        )
        self.assertEqual(
            ErrorType.from_precondition_failure_violation_type("UNAVAILABLE"), ErrorType.UNAVAILABLE
        )
        self.assertEqual(
            ErrorType.from_precondition_failure_violation_type("TIMEOUT"), ErrorType.TIMEOUT
        )
        self.assertEqual(
            ErrorType.from_precondition_failure_violation_type("INTERNAL"), ErrorType.INTERNAL
        )
        self.assertEqual(
            ErrorType.from_precondition_failure_violation_type("UNKNOWN"), ErrorType.UNKNOWN
        )
        self.assertEqual(
            ErrorType.from_precondition_failure_violation_type("NOT_A_VALID_TYPE"),
            ErrorType.UNKNOWN,
        )
