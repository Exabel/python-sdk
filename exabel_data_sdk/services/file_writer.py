import abc
from typing import Iterable, Union

import pandas as pd


class FileWriter(abc.ABC):
    """Base class for file writers."""

    @staticmethod
    @abc.abstractmethod
    def write_file(df: Union[pd.DataFrame, Iterable[pd.DataFrame]], filepath: str) -> None:
        """Write the DataFrame or iterable of DataFrames to a file."""
