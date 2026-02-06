from typing import Iterable, Iterator, Mapping, overload

import pandas as pd


class CsvReader:
    """Reader of CSV files."""

    @overload
    @staticmethod
    def read_file(
        filename: str,
        separator: str | None,
        string_columns: Iterable[str | int],
        *,
        keep_default_na: bool,
        nrows: int | None,
    ) -> pd.DataFrame: ...

    @overload
    @staticmethod
    def read_file(
        filename: str,
        separator: str | None,
        string_columns: Iterable[str | int],
        *,
        keep_default_na: bool,
    ) -> pd.DataFrame: ...

    @overload
    @staticmethod
    def read_file(
        filename: str,
        separator: str | None,
        string_columns: Iterable[str | int],
        *,
        keep_default_na: bool,
        chunksize: int,
    ) -> Iterator[pd.DataFrame]: ...

    @overload
    @staticmethod
    def read_file(
        filename: str,
        separator: str | None,
        string_columns: Iterable[str | int],
        *,
        keep_default_na: bool,
        chunksize: int | None,
    ) -> pd.DataFrame | Iterator[pd.DataFrame]: ...

    @staticmethod
    def read_file(
        filename: str,
        separator: str | None,
        string_columns: Iterable[str | int],
        *,
        keep_default_na: bool,
        nrows: int | None = None,
        chunksize: int | None = None,
    ) -> pd.DataFrame | Iterator[pd.DataFrame]:
        """
        Read the given file and return the content as a pandas DataFrame.

        Args:
            filename: the location of the CSV file
            separator: the separator used in the CSV file
            string_columns: the columns which contain general strings
            keep_default_na: whether to parse default nan values as nan
            nrows: how many rows to parse
        """
        dtype: Mapping[str | int, type] | None = None
        if string_columns:
            dtype = {column: str for column in string_columns}
        return pd.read_csv(
            filename,
            header=0,
            sep=separator,
            dtype=dtype,
            keep_default_na=keep_default_na,
            nrows=nrows,
            chunksize=chunksize,
        )
