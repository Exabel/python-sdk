from pathlib import Path

from exabel.services.csv_writer import CsvWriter
from exabel.services.excel_writer import ExcelWriter
from exabel.services.feather_writer import FeatherWriter
from exabel.services.file_constants import (
    EXCEL_EXTENSIONS,
    FEATHER_EXTENSIONS,
    FULL_CSV_EXTENSIONS,
)
from exabel.services.file_writer import FileWriter


class FileWriterProvider:
    """Provides file writers."""

    @staticmethod
    def get_file_extension(filepath: str) -> str:
        """Get the file extension of the given filepath."""
        suffixes = Path(filepath).suffixes
        return "".join(suffixes)

    @classmethod
    def get_file_writer(cls, filepath: str) -> type[FileWriter]:
        """Return the file writer for the given filepath."""
        extension = cls.get_file_extension(filepath)
        if extension in FULL_CSV_EXTENSIONS:
            return CsvWriter
        if extension in EXCEL_EXTENSIONS:
            return ExcelWriter
        if extension in FEATHER_EXTENSIONS:
            return FeatherWriter
        raise ValueError(f"Unknown file extension: {extension}")
