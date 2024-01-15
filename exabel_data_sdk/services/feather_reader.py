from typing import Iterable, Iterator

import numpy as np
import pandas as pd

from exabel_data_sdk.util.handle_missing_imports import handle_missing_imports

with handle_missing_imports():
    import pyarrow as pa


class FeatherReader:
    """Reader of Feather files."""

    @staticmethod
    def read_file_in_batches(
        filename: str, string_columns: Iterable[int]
    ) -> Iterator[pd.DataFrame]:
        """
        Read the Feather file and return an iterator of pandas DataFrames.

        Args:
            filename: the location of the Feather file
            string_columns: the indices of the columns that should be interpreted as strings
        """
        reader = pa.ipc.open_file(filename)
        for i in range(reader.num_record_batches):
            batch = reader.get_batch(i).to_pandas().fillna(value=np.nan)
            if string_columns:
                batch = batch.astype({batch.columns[i]: str for i in string_columns})
            yield batch

    @staticmethod
    def read_file(filename: str, string_columns: Iterable[int]) -> pd.DataFrame:
        """
        Read the Feather file and return a pandas DataFrame

        Args:
            filename: the location of the Feather file
            string_columns: the indices of the columns that should be interpreted as strings
        """
        df = pa.ipc.open_file(filename).read_pandas().fillna(value=np.nan)
        if string_columns:
            df = df.astype({df.columns[i]: str for i in string_columns})
        return df
