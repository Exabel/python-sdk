import unittest
from typing import Optional

from exabel_data_sdk.util.deprecate_arguments import deprecate_arguments
from exabel_data_sdk.util.warnings import ExabelDeprecationWarning


@deprecate_arguments(old_arg="new_arg")
def _test_func(*, new_arg: Optional[str] = None, old_arg: Optional[str] = None) -> Optional[str]:
    return new_arg or old_arg


class TestDeprecateArguments(unittest.TestCase):
    @deprecate_arguments(old_arg="new_arg")
    def _test_method(
        self, *, new_arg: Optional[str] = None, old_arg: Optional[str] = None
    ) -> Optional[str]:
        return new_arg or old_arg

    def test_deprecate_arguments(self):
        self.assertEqual(_test_func(new_arg="test"), "test")
        self.assertEqual(_test_func(old_arg="test"), "test")
        self.assertIsNone(_test_func())

        self.assertEqual(self._test_method(new_arg="test"), "test")
        self.assertEqual(self._test_method(old_arg="test"), "test")
        self.assertIsNone(self._test_method())

    def test_deprecate_argument__raises_warning(self):
        with self.assertWarns(ExabelDeprecationWarning) as cm:
            _test_func(old_arg="test")
        self.assertRegex(
            str(cm.warning),
            r"Argument 'old_arg' is deprecated in '.*_test_func' and will be removed in a future "
            r"release. Use 'new_arg' instead.",
        )

        with self.assertWarns(ExabelDeprecationWarning) as cm:
            self._test_method(old_arg="test")
        self.assertRegex(
            str(cm.warning),
            r"Argument 'old_arg' is deprecated in '.*TestDeprecateArguments._test_method' and will "
            r"be removed in a future release. Use 'new_arg' instead.",
        )

    def test_deprecate_argument__both_arguments_provided_should_fail(self):
        with self.assertRaises(ValueError):
            _test_func(new_arg="test", old_arg="test")
        with self.assertRaises(ValueError):
            self._test_method(new_arg="test", old_arg="test")

    def test_deprecate_argument__no_deprecations_provided_should_fail(self):
        with self.assertRaises(ValueError):

            @deprecate_arguments()
            def _no_deprecation() -> None:
                ...

    def test_deprecate_argument__removed_argument(self):
        @deprecate_arguments(deprecated_arg=None)
        def _test_func(*, deprecated_arg: Optional[str] = None) -> Optional[str]:
            return deprecated_arg

        self.assertIsNone(_test_func(deprecated_arg="test"))

    def test_deprecate_argument__with_function_as_arg(self):
        def _test_func(
            new_arg: Optional[str] = None, old_arg: Optional[str] = None
        ) -> Optional[str]:
            return new_arg or old_arg

        wrapped_local_func = deprecate_arguments(_test_func, old_arg="new_arg")
        self.assertEqual(wrapped_local_func(new_arg="test"), "test")
