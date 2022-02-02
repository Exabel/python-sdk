import tempfile
import unittest
from typing import Iterable, Union

import pandas as pd

from exabel_data_sdk.services.csv_reader import CsvReader


class TestCsvReader(unittest.TestCase):
    def _read_csv(self, content: str, string_columns: Iterable[Union[str, int]]):
        with tempfile.TemporaryDirectory() as tmp:
            file = f"{tmp}/file.csv"
            with open(file, "w", encoding="utf-8") as f:
                for line in content:
                    f.write(",".join(map(str, line)) + "\n")
            return CsvReader.read_csv(
                file, separator=",", string_columns=string_columns, keep_default_na=False
            )

    def test_read_csv(self):
        content = [("Column A", "Column B"), ("a1", "a2"), ("b1", "b2")]
        result = self._read_csv(content, string_columns=["Column A", "Column B"])
        expected = pd.DataFrame({"Column A": ["a1", "b1"], "Column B": ["a2", "b2"]})
        pd.testing.assert_frame_equal(expected, result)

    def test_read_csv_with_obvious_string_columns(self):
        content = [("Column A", "Column B"), ("a1", "a2"), ("b1", "b2")]
        result = self._read_csv(content, string_columns=[])
        expected = pd.DataFrame({"Column A": ["a1", "b1"], "Column B": ["a2", "b2"]})
        pd.testing.assert_frame_equal(expected, result)

    def test_read_csv_with_integer_column(self):
        content = [("Column A", "Integer"), ("a1", 2), ("b1", 3)]
        result = self._read_csv(content, string_columns=["Column A"])
        expected = pd.DataFrame({"Column A": ["a1", "b1"], "Integer": [2, 3]})
        pd.testing.assert_frame_equal(expected, result)

    def test_read_csv_with_integer_columns_interpreted_as_string(self):
        content = [("Column A", "Integer"), ("a1", 2), ("b1", 3)]
        result = self._read_csv(content, string_columns=["Column A", "Integer"])
        expected = pd.DataFrame({"Column A": ["a1", "b1"], "Integer": ["2", "3"]})
        pd.testing.assert_frame_equal(expected, result)

    def test_read_csv_with_integer_column_interpreted_as_string_referred_to_with_index(self):
        content = [("Column A", "Integer"), ("a1", 2), ("b1", 3)]
        result = self._read_csv(content, string_columns=["Column A", 1])
        expected = pd.DataFrame({"Column A": ["a1", "b1"], "Integer": ["2", "3"]})
        pd.testing.assert_frame_equal(expected, result)

    def test_read_csv_with_empty_value(self):
        content = [("Column A", "Column B"), ("a1", "a2"), ("b1", "")]
        result = self._read_csv(content, string_columns=["Column A", "Column B"])
        expected = pd.DataFrame({"Column A": ["a1", "b1"], "Column B": ["a2", ""]})
        pd.testing.assert_frame_equal(expected, result)
