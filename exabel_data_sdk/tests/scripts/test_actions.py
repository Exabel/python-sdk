import argparse
import unittest

from exabel_data_sdk.scripts.actions import CaseInsensitiveArgumentAction, DeprecatedArgumentAction
from exabel_data_sdk.util.warnings import ExabelDeprecationWarning


class TestActions(unittest.TestCase):
    def test_deprecated_argument_action(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--foo", action=DeprecatedArgumentAction)
        args = parser.parse_args(["--foo", "bar"])
        self.assertEqual("bar", args.foo)

    def test_deprecated_argument_action__raises_warning(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--foo", action=DeprecatedArgumentAction)
        with self.assertWarns(ExabelDeprecationWarning):
            parser.parse_args(["--foo", "bar"])

    def test_deprecated_argument_action__override_dest(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--foo", dest="bar", action=DeprecatedArgumentAction)
        args = parser.parse_args(["--foo", "baz"])
        self.assertEqual("baz", args.bar)

    def test_deprecated_argument_action__miscellaneous_types(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--int", type=int, action=DeprecatedArgumentAction)
        parser.add_argument("--floats", type=float, nargs="*", action=DeprecatedArgumentAction)
        args = parser.parse_args(["--int", "1", "--floats", "2.0", "3"])
        self.assertEqual(1, args.int)
        self.assertSequenceEqual([2.0, 3.0], args.floats)

    def test_deprecated_argument_action__case_insensitive_value(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--foo", action=DeprecatedArgumentAction, case_insensitive=True)
        args = parser.parse_args(["--foo", "BAR"])
        self.assertEqual("bar", args.foo)

    def test_deprecated_argument_action__replace_with_none(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--foo", action=DeprecatedArgumentAction, replace_with_none=True)
        args = parser.parse_args(["--foo", "BAR"])
        self.assertIsNone(args.foo)

    def test_case_insensitive_argument_action(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--foo", type=str, action=CaseInsensitiveArgumentAction)
        parser.add_argument("--bar", type=str, nargs="*", action=CaseInsensitiveArgumentAction)
        args = parser.parse_args(["--foo", "FOO", "--bar", "Bar1", "BAR2", "bar3"])
        self.assertEqual("foo", args.foo)
        self.assertEqual(["bar1", "bar2", "bar3"], args.bar)

    def test_case_insensitive_argument_action__type_not_string(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--foo", type=int, action=CaseInsensitiveArgumentAction)
        with self.assertRaises(AssertionError):
            parser.parse_args(["--foo", "1"])

    def test_case_insensitive_argument_action__type_not_list_of_string(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--foo", type=float, nargs="*", action=CaseInsensitiveArgumentAction)
        with self.assertRaises(AssertionError):
            parser.parse_args(["--foo", "1", "2.0", "3"])
