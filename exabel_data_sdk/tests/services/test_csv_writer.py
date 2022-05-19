import gzip
import tempfile
import unittest

import pandas as pd

from exabel_data_sdk.services.csv_writer import CsvWriter


class TestCsvWriter(unittest.TestCase):
    def test_csv_writer(self):
        test_df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        with tempfile.NamedTemporaryFile() as file:
            CsvWriter.write_file(test_df, file.name)
            file.seek(0)
            file_content = file.read()
        self.assertEqual("a,b\n1,4\n2,5\n3,6\n", file_content.decode("utf-8"))

    def test_csv_writer_with_compression(self):
        test_df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        with tempfile.NamedTemporaryFile(suffix=".csv.gz") as file:
            CsvWriter.write_file(test_df, file.name)
            file.seek(0)
            file_content = file.read()
        self.assertEqual("a,b\n1,4\n2,5\n3,6\n", gzip.decompress(file_content).decode("utf-8"))
