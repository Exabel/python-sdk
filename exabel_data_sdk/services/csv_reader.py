from typing import Iterable, Mapping, Optional, Union

import pandas as pd


class CsvReader:
    """Reader of CSV files."""

    @staticmethod
    def read_csv(
        filename: str,
        separator: str,
        string_columns: Iterable[Union[str, int]],
        *,
        keep_default_na: bool
    ) -> pd.DataFrame:
        """
        Read the given file and return the content as a pandas DataFrame.

        Args:
            filename: the location of the CSV file
            separator: the separator used in the CSV file
            string_columns: the columns which contain general strings
        """
        dtype: Optional[Mapping[Union[str, int], type]] = None
        if string_columns:
            dtype = {column: str for column in string_columns}
        return pd.read_csv(
            filename, header=0, sep=separator, dtype=dtype, keep_default_na=keep_default_na
        )
