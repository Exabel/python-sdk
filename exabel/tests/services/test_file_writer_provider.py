import pytest

from exabel.services.csv_writer import CsvWriter
from exabel.services.excel_writer import ExcelWriter
from exabel.services.file_constants import EXCEL_EXTENSIONS, FULL_CSV_EXTENSIONS
from exabel.services.file_writer_provider import FileWriterProvider


class TestFileWriterProvider:
    def test_full_csv_extensions(self):
        assert {
            ".csv.gz",
            ".csv.bz2",
            ".csv.zip",
            ".csv.xz",
            ".csv.zst",
            ".csv",
        } == FULL_CSV_EXTENSIONS

    def test_get_extension(self):
        assert ".csv" == FileWriterProvider.get_file_extension("test.csv")
        assert ".csv.gz" == FileWriterProvider.get_file_extension("test.csv.gz")
        assert "" == FileWriterProvider.get_file_extension(".a")
        assert ".b" == FileWriterProvider.get_file_extension(".a.b")
        assert ".b.c" == FileWriterProvider.get_file_extension(".a.b.c")
        assert ".b.c.d" == FileWriterProvider.get_file_extension(".a.b.c.d")
        assert ".d" == FileWriterProvider.get_file_extension("a.b/c.d")

    def test_provide_csv_writer(self):
        for extension in FULL_CSV_EXTENSIONS:
            assert CsvWriter == FileWriterProvider.get_file_writer(f"test{extension}")

    def test_provide_excel_writer(self):
        for extension in EXCEL_EXTENSIONS:
            assert ExcelWriter == FileWriterProvider.get_file_writer(f"test{extension}")

    def test_provide_file_writer_should_fail(self):
        with pytest.raises(ValueError):
            FileWriterProvider.get_file_writer("test.a")
        with pytest.raises(ValueError):
            FileWriterProvider.get_file_writer(".csv")
        with pytest.raises(ValueError):
            FileWriterProvider.get_file_writer("test.parquet")
        with pytest.raises(ValueError):
            FileWriterProvider.get_file_writer("test.csv.a")
