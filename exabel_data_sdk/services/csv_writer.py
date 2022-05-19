import pandas as pd

from exabel_data_sdk.services.file_writer import FileWriter


class CsvWriter(FileWriter):
    """Stores a DataFrame in a CSV file."""

    @staticmethod
    def write_file(df: pd.DataFrame, filepath: str) -> None:
        df.to_csv(filepath, index=False)
