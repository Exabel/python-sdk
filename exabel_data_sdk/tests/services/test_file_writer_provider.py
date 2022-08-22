import unittest

from exabel_data_sdk.services.csv_writer import CsvWriter
from exabel_data_sdk.services.excel_writer import ExcelWriter
from exabel_data_sdk.services.file_writer_provider import (
    EXCEL_EXTENSIONS,
    FULL_CSV_EXTENSIONS,
    FileWriterProvider,
)


class TestFileWriterProvider(unittest.TestCase):
    def test_full_csv_extensions(self):
        self.assertSetEqual(
            {".csv.gz", ".csv.bz2", ".csv.zip", ".csv.xz", ".csv.zst", ".csv"},
            FULL_CSV_EXTENSIONS,
        )

    def test_get_extension(self):
        self.assertEqual(".csv", FileWriterProvider.get_file_extension("test.csv"))
        self.assertEqual(".csv.gz", FileWriterProvider.get_file_extension("test.csv.gz"))
        self.assertEqual("", FileWriterProvider.get_file_extension(".a"))
        self.assertEqual(".b", FileWriterProvider.get_file_extension(".a.b"))
        self.assertEqual(".b.c", FileWriterProvider.get_file_extension(".a.b.c"))
        self.assertEqual(".b.c.d", FileWriterProvider.get_file_extension(".a.b.c.d"))
        self.assertEqual(".d", FileWriterProvider.get_file_extension("a.b/c.d"))

    def test_provide_csv_writer(self):
        for extension in FULL_CSV_EXTENSIONS:
            self.assertEqual(CsvWriter, FileWriterProvider.get_file_writer(f"test{extension}"))

    def test_provide_excel_writer(self):
        for extension in EXCEL_EXTENSIONS:
            self.assertEqual(ExcelWriter, FileWriterProvider.get_file_writer(f"test{extension}"))

    def test_provide_file_writer_should_fail(self):
        self.assertRaises(ValueError, FileWriterProvider.get_file_writer, "test.a")
        self.assertRaises(ValueError, FileWriterProvider.get_file_writer, ".csv")
        self.assertRaises(ValueError, FileWriterProvider.get_file_writer, "test.parquet")
        self.assertRaises(ValueError, FileWriterProvider.get_file_writer, "test.csv.a")
