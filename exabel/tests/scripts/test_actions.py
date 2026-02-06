import argparse

import pytest

from exabel.scripts.actions import CaseInsensitiveArgumentAction, DeprecatedArgumentAction
from exabel.util.warnings import ExabelDeprecationWarning


class TestActions:
    def test_deprecated_argument_action(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--foo", action=DeprecatedArgumentAction)
        with pytest.warns(ExabelDeprecationWarning):
            args = parser.parse_args(["--foo", "bar"])
        assert "bar" == args.foo

    def test_deprecated_argument_action__raises_warning(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--foo", action=DeprecatedArgumentAction)
        with pytest.warns(ExabelDeprecationWarning):
            parser.parse_args(["--foo", "bar"])

    def test_deprecated_argument_action__override_dest(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--foo", dest="bar", action=DeprecatedArgumentAction)
        with pytest.warns(ExabelDeprecationWarning):
            args = parser.parse_args(["--foo", "baz"])
        assert "baz" == args.bar

    def test_deprecated_argument_action__miscellaneous_types(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--int", type=int, action=DeprecatedArgumentAction)
        parser.add_argument("--floats", type=float, nargs="*", action=DeprecatedArgumentAction)
        with pytest.warns(ExabelDeprecationWarning):
            args = parser.parse_args(["--int", "1", "--floats", "2.0", "3"])
        assert 1 == args.int
        assert [2.0, 3.0] == args.floats

    def test_deprecated_argument_action__case_insensitive_value(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--foo", action=DeprecatedArgumentAction, case_insensitive=True)
        with pytest.warns(ExabelDeprecationWarning):
            args = parser.parse_args(["--foo", "BAR"])
        assert "bar" == args.foo

    def test_deprecated_argument_action__replace_with_none(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--foo", action=DeprecatedArgumentAction, replace_with_none=True)
        with pytest.warns(ExabelDeprecationWarning):
            args = parser.parse_args(["--foo", "BAR"])
        assert args.foo is None

    def test_case_insensitive_argument_action(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--foo", type=str, action=CaseInsensitiveArgumentAction)
        parser.add_argument("--bar", type=str, nargs="*", action=CaseInsensitiveArgumentAction)
        args = parser.parse_args(["--foo", "FOO", "--bar", "Bar1", "BAR2", "bar3"])
        assert "foo" == args.foo
        assert ["bar1", "bar2", "bar3"] == args.bar

    def test_case_insensitive_argument_action__type_not_string(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--foo", type=int, action=CaseInsensitiveArgumentAction)
        with pytest.raises(AssertionError):
            parser.parse_args(["--foo", "1"])

    def test_case_insensitive_argument_action__type_not_list_of_string(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--foo", type=float, nargs="*", action=CaseInsensitiveArgumentAction)
        with pytest.raises(AssertionError):
            parser.parse_args(["--foo", "1", "2.0", "3"])
