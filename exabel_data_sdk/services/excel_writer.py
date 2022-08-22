import pandas as pd

from exabel_data_sdk.services.file_writer import FileWriter


class ExcelWriter(FileWriter):
    """Stores a DataFrame in an Excel file."""

    @staticmethod
    def write_file(df: pd.DataFrame, filepath: str) -> None:
        df.to_excel(filepath, index=False)
