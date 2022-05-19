import argparse
import unittest

from exabel_data_sdk.scripts.command_line_script import CommandLineScript


class TestCommandLineScript(unittest.TestCase):
    class MockCommandLineScript(CommandLineScript):
        """Mock implementation of CommandLineScript."""

        def __init__(self, argv, description):
            super().__init__(argv, description)
            self.parser.add_argument("--the-argument")

        def run(self):
            raise NotImplementedError from None

    def setUp(self) -> None:
        self.script = self.MockCommandLineScript(
            ["the-script-name", "--the-argument", "123"], "The description."
        )

    def test_command_line_script(self):
        self.assertEqual(["the-script-name", "--the-argument", "123"], self.script.argv)
        self.assertEqual("The description.", self.script.parser.description)

    def test_parse_arguments(self):
        args = self.script.parse_arguments()
        self.assertEqual(argparse.Namespace(the_argument="123"), args)
