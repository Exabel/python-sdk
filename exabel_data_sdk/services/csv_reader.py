from typing import Iterable, Iterator, Mapping, Optional, Union, overload

import pandas as pd


class CsvReader:
    """Reader of CSV files."""

    @overload
    @staticmethod
    def read_file(
        filename: str,
        separator: Optional[str],
        string_columns: Iterable[Union[str, int]],
        *,
        keep_default_na: bool,
        nrows: Optional[int],
    ) -> pd.DataFrame:
        ...

    @overload
    @staticmethod
    def read_file(
        filename: str,
        separator: Optional[str],
        string_columns: Iterable[Union[str, int]],
        *,
        keep_default_na: bool,
    ) -> pd.DataFrame:
        ...

    @overload
    @staticmethod
    def read_file(
        filename: str,
        separator: Optional[str],
        string_columns: Iterable[Union[str, int]],
        *,
        keep_default_na: bool,
        chunksize: int,
    ) -> Iterator[pd.DataFrame]:
        ...

    @overload
    @staticmethod
    def read_file(
        filename: str,
        separator: Optional[str],
        string_columns: Iterable[Union[str, int]],
        *,
        keep_default_na: bool,
        chunksize: Optional[int],
    ) -> Union[pd.DataFrame, Iterator[pd.DataFrame]]:
        ...

    @staticmethod
    def read_file(
        filename: str,
        separator: Optional[str],
        string_columns: Iterable[Union[str, int]],
        *,
        keep_default_na: bool,
        nrows: Optional[int] = None,
        chunksize: Optional[int] = None,
    ) -> Union[pd.DataFrame, Iterator[pd.DataFrame]]:
        """
        Read the given file and return the content as a pandas DataFrame.

        Args:
            filename: the location of the CSV file
            separator: the separator used in the CSV file
            string_columns: the columns which contain general strings
            keep_default_na: whether to parse default nan values as nan
            nrows: how many rows to parse
        """
        dtype: Optional[Mapping[Union[str, int], type]] = None
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
