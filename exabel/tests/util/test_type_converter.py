from math import isinf, isnan

import pytest

from exabel.util.exceptions import TypeConversionError
from exabel.util.type_converter import type_converter


class TestTypeConverter:
    def test_type_converter_with_string(self):
        assert type_converter("string", str) == "string"

    def test_type_converter_with_int(self):
        assert type_converter("1", int) == 1

    def test_type_converter_with_float(self):
        assert type_converter("1.0", float) == 1.0
        assert type_converter("1", float) == 1.0
        assert isnan(type_converter("nan", float))
        assert isinf(type_converter("inf", float))
        assert isinf(type_converter("-inf", float))

    def test_type_converter_with_bool(self):
        assert type_converter("true", bool)
        assert type_converter("TRUE", bool)
        assert not type_converter("false", bool)
        assert not type_converter("FALSE", bool)

    def test_type_converter_with_int_should_fail(self):
        with pytest.raises(TypeConversionError):
            type_converter("1.0", int)

    def test_type_converter_with_float_should_fail(self):
        with pytest.raises(TypeConversionError):
            type_converter("not-a-float", float)

    def test_type_converter_with_bool_should_fail(self):
        with pytest.raises(TypeConversionError):
            type_converter("not-a-bool", bool)

    def test_type_converter_with_invalid_type_should_fail(self):
        with pytest.raises(TypeConversionError):
            type_converter("string", list)
