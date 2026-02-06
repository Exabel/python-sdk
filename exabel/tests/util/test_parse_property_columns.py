import pytest

from exabel.util.exceptions import ParsePropertyColumnsError
from exabel.util.parse_property_columns import parse_property_columns


class TestParsePropertyColumns:
    def test_parse_property_columns(self):
        assert {
            "boolean_prop": bool,
            "string_prop": str,
            "integer_prop": int,
            "float_prop": float,
        } == parse_property_columns(
            "boolean_prop:bool", "string_prop:str", "integer_prop:int", "float_prop:float"
        )

    def test_parse_property_columns_with_no_input(self):
        assert {} == parse_property_columns(*[])

    def test_parse_property_columns_should_fail(self):
        with pytest.raises(ParsePropertyColumnsError):
            parse_property_columns("prop:not_a_type")
        with pytest.raises(ParsePropertyColumnsError):
            parse_property_columns("missing_type")
