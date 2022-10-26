from typing import Iterable, Union

import pandas as pd

from exabel_data_sdk.services.file_writer import FileWriter


class ExcelWriter(FileWriter):
    """Stores a DataFrame in an Excel file."""

    @staticmethod
    def write_file(df: Union[pd.DataFrame, Iterable[pd.DataFrame]], filepath: str) -> None:
        if isinstance(df, pd.DataFrame):
            df.to_excel(filepath, index=False)
            return
        raise NotImplementedError("Writing multiple DataFrames to Excel is not supported.")
