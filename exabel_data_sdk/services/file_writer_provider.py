from pathlib import Path
from typing import Type

from exabel_data_sdk.services.csv_writer import CsvWriter
from exabel_data_sdk.services.excel_writer import ExcelWriter
from exabel_data_sdk.services.file_constants import EXCEL_EXTENSIONS, FULL_CSV_EXTENSIONS
from exabel_data_sdk.services.file_writer import FileWriter


class FileWriterProvider:
    """Provides file writers."""

    @staticmethod
    def get_file_extension(filepath: str) -> str:
        """Get the file extension of the given filepath."""
        suffixes = Path(filepath).suffixes
        return "".join(suffixes)

    @classmethod
    def get_file_writer(cls, filepath: str) -> Type[FileWriter]:
        """Return the file writer for the given filepath."""
        extension = cls.get_file_extension(filepath)
        if extension in FULL_CSV_EXTENSIONS:
            return CsvWriter
        if extension in EXCEL_EXTENSIONS:
            return ExcelWriter
        raise ValueError(f"Unknown file extension: {extension}")
