import re

import pytest

from exabel.util.deprecate_arguments import deprecate_argument_value, deprecate_arguments
from exabel.util.warnings import ExabelDeprecationWarning


@deprecate_arguments(old_arg="new_arg")
def _test_func(*, new_arg: str | None = None, old_arg: str | None = None) -> str | None:
    return new_arg or old_arg


@deprecate_argument_value(old_arg="illegal")
def _test_func_2(*, new_arg: str | None = None, old_arg: str | None = None) -> str | None:
    return new_arg or old_arg


class TestDeprecateArguments:
    @deprecate_arguments(old_arg="new_arg")
    def _test_method(self, *, new_arg: str | None = None, old_arg: str | None = None) -> str | None:
        return new_arg or old_arg

    def test_deprecate_arguments(self):
        assert _test_func(new_arg="test") == "test"
        with pytest.warns(ExabelDeprecationWarning):
            assert _test_func(old_arg="test") == "test"
        assert _test_func() is None

        assert self._test_method(new_arg="test") == "test"
        with pytest.warns(ExabelDeprecationWarning):
            assert self._test_method(old_arg="test") == "test"
        assert self._test_method() is None

    def test_deprecate_argument__raises_warning(self):
        with pytest.warns(ExabelDeprecationWarning) as record:
            _test_func(old_arg="test")
        assert re.search(
            r"Argument 'old_arg' is deprecated in '.*_test_func' and will be removed in a future "
            r"release. Use 'new_arg' instead.",
            str(record[0].message),
        )

        with pytest.warns(ExabelDeprecationWarning) as record:
            self._test_method(old_arg="test")
        assert re.search(
            r"Argument 'old_arg' is deprecated in '.*TestDeprecateArguments._test_method' and will "
            r"be removed in a future release. Use 'new_arg' instead.",
            str(record[0].message),
        )

    def test_deprecate_argument__both_arguments_provided_should_fail(self):
        with pytest.raises(ValueError):
            _test_func(new_arg="test", old_arg="test")
        with pytest.raises(ValueError):
            self._test_method(new_arg="test", old_arg="test")

    def test_deprecate_argument__no_deprecations_provided_should_fail(self):
        with pytest.raises(ValueError):

            @deprecate_arguments()
            def _no_deprecation() -> None: ...

    def test_deprecate_argument__removed_argument(self):
        @deprecate_arguments(deprecated_arg=None)
        def _test_func(*, deprecated_arg: str | None = None) -> str | None:
            return deprecated_arg

        with pytest.warns(ExabelDeprecationWarning):
            assert _test_func(deprecated_arg="test") is None

    def test_deprecate_argument__with_function_as_arg(self):
        def _test_func(new_arg: str | None = None, old_arg: str | None = None) -> str | None:
            return new_arg or old_arg

        wrapped_local_func = deprecate_arguments(_test_func, old_arg="new_arg")
        assert wrapped_local_func(new_arg="test") == "test"


class TestDeprecateArgumentValue:
    @deprecate_argument_value(old_arg="illegal")
    def _test_method(self, *, new_arg: str | None = None, old_arg: str | None = None) -> str | None:
        return new_arg or old_arg

    def test_deprecate_argument_value(self):
        assert _test_func_2(new_arg="test") == "test"
        with pytest.warns(ExabelDeprecationWarning):
            assert _test_func_2(old_arg="illegal") == "illegal"

        assert self._test_method(new_arg="test") == "test"
        with pytest.warns(ExabelDeprecationWarning):
            assert self._test_method(old_arg="illegal") == "illegal"
        assert self._test_method() is None

    def test_deprecate_argument_value__raises_warning(self):
        with pytest.warns(ExabelDeprecationWarning) as record:
            _test_func_2(old_arg="illegal")
        assert re.search(
            r"Option 'old_arg=illegal' is deprecated in '.*_test_func_2' and will be removed in a "
            r"future release.",
            str(record[0].message),
        )

        with pytest.warns(ExabelDeprecationWarning) as record:
            self._test_method(old_arg="illegal")
        assert re.search(
            r"Option 'old_arg=illegal' is deprecated in '.*TestDeprecateArgumentValue._test_method'"
            r" and will be removed in a future release.",
            str(record[0].message),
        )
