import unittest
from argparse import ArgumentTypeError

from exabel_data_sdk.scripts.csv_script import abort_threshold


class TestCsvScript(unittest.TestCase):
    def test_abort_threshold_argument(self):
        self.assertEqual(0.0, abort_threshold("0"))
        self.assertEqual(0.5, abort_threshold("0.5"))
        self.assertEqual(1.0, abort_threshold("1"))
        self.assertRaises(ArgumentTypeError, abort_threshold, "1.1")
        self.assertRaises(ArgumentTypeError, abort_threshold, "-0.1")
        self.assertRaises(ArgumentTypeError, abort_threshold, "foo")
