import unittest
from math import isinf, isnan

from exabel_data_sdk.util.exceptions import TypeConvertionError
from exabel_data_sdk.util.type_converter import type_converter


class TestTypeConverter(unittest.TestCase):
    def test_type_converter_with_string(self):
        self.assertEqual(type_converter("string", str), "string")

    def test_type_converter_with_int(self):
        self.assertEqual(type_converter("1", int), 1)

    def test_type_converter_with_float(self):
        self.assertEqual(type_converter("1.0", float), 1.0)
        self.assertEqual(type_converter("1", float), 1.0)
        self.assertTrue(isnan(type_converter("nan", float)))
        self.assertTrue(isinf(type_converter("inf", float)))
        self.assertTrue(isinf(type_converter("-inf", float)))

    def test_type_converter_with_bool(self):
        self.assertEqual(type_converter("true", bool), True)
        self.assertEqual(type_converter("TRUE", bool), True)
        self.assertEqual(type_converter("false", bool), False)
        self.assertEqual(type_converter("FALSE", bool), False)

    def test_type_converter_with_int_should_fail(self):
        with self.assertRaises(TypeConvertionError):
            type_converter("1.0", int)

    def test_type_converter_with_float_should_fail(self):
        with self.assertRaises(TypeConvertionError):
            type_converter("not-a-float", float)

    def test_type_converter_with_bool_should_fail(self):
        with self.assertRaises(TypeConvertionError):
            type_converter("not-a-bool", bool)

    def test_type_converter_with_invalid_type_should_fail(self):
        with self.assertRaises(TypeConvertionError):
            type_converter("string", list)
