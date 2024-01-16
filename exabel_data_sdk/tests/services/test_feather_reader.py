import tempfile
import unittest
from typing import Iterable

import pandas as pd

from exabel_data_sdk.tests.decorators import requires_modules


@requires_modules("pyarrow")
class TestFeatherReader(unittest.TestCase):
    def _read_feather(
        self,
        content: str,
        string_columns: Iterable[int],
    ):
        with tempfile.TemporaryDirectory() as tmp:
            from exabel_data_sdk.services.feather_reader import FeatherReader

            file = f"{tmp}/file.feather"
            pd.DataFrame(content[1:], columns=content[0]).to_feather(file)
            return FeatherReader.read_file(filename=file, string_columns=string_columns)

    def test_read_feather(self):
        content = [("Column A", "Integer"), ("a1", 1), ("a2", 2)]
        result = self._read_feather(content, string_columns=[0])
        expected = pd.DataFrame({"Column A": ["a1", "a2"], "Integer": [1, 2]})
        pd.testing.assert_frame_equal(expected, result)

    def test_read_feather_with_obvious_string_columns(self):
        content = [("Column A", "Column B"), ("a1", "a2"), ("b1", "b2")]
        result = self._read_feather(content, string_columns=[])
        expected = pd.DataFrame({"Column A": ["a1", "b1"], "Column B": ["a2", "b2"]})
        pd.testing.assert_frame_equal(expected, result)

    def test_read_feather_with_integer_columns_interpreted_as_string(self):
        content = [("Column A", "Integer"), ("a1", 2), ("b1", 3)]
        result = self._read_feather(content, string_columns=[0, 1])
        expected = pd.DataFrame({"Column A": ["a1", "b1"], "Integer": ["2", "3"]})
        pd.testing.assert_frame_equal(expected, result)

    def test_read_feather_with_empty_value(self):
        content = [("Column A", "Column B"), ("a1", "a2"), ("b1", "")]
        result = self._read_feather(content, string_columns=[0, 1])
        expected = pd.DataFrame({"Column A": ["a1", "b1"], "Column B": ["a2", ""]})
        pd.testing.assert_frame_equal(expected, result)

    def test_read_feather_in_batches(self):
        df = pd.DataFrame({"A": range(100000), "B": range(100000)})
        with tempfile.TemporaryDirectory() as tmp:
            from exabel_data_sdk.services.feather_reader import FeatherReader

            file = f"{tmp}/file_for_batch_reading.feather"
            df.to_feather(file)
            df = df.astype({"A": str})
            result = FeatherReader.read_file_in_batches(file, string_columns=[0])
            for batch in result:
                df_batch = df.iloc[: len(batch)]
                pd.testing.assert_frame_equal(df_batch, batch)
                df = df.iloc[len(batch) :]
                df.reset_index(drop=True, inplace=True)
