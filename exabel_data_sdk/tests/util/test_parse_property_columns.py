import unittest

from exabel_data_sdk.util.exceptions import ParsePropertyColumnsError
from exabel_data_sdk.util.parse_property_columns import parse_property_columns


class TestParsePropertyColumns(unittest.TestCase):
    def test_parse_property_columns(self):
        self.assertEqual(
            {
                "boolean_prop": bool,
                "string_prop": str,
                "integer_prop": int,
                "float_prop": float,
            },
            parse_property_columns(
                "boolean_prop:bool", "string_prop:str", "integer_prop:int", "float_prop:float"
            ),
        )

    def test_parse_property_columns_with_no_input(self):
        self.assertEqual({}, parse_property_columns(*[]))

    def test_parse_property_columns_should_fail(self):
        with self.assertRaises(ParsePropertyColumnsError):
            parse_property_columns("prop:not_a_type")
        with self.assertRaises(ParsePropertyColumnsError):
            parse_property_columns("missing_type")
