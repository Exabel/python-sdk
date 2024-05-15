import abc
from dataclasses import dataclass
from typing import Iterable, Optional, Union

import pandas as pd


@dataclass
class FileWritingResult:
    """
    Contains summary of result after writing to a file or a set of files.

    Attributes:
        rows: Number of rows written to a file or a set of files.
    """

    rows: Optional[int] = None


class FileWriter(abc.ABC):
    """Base class for file writers."""

    @staticmethod
    @abc.abstractmethod
    def write_file(
        df: Union[pd.DataFrame, Iterable[pd.DataFrame]], filepath: str
    ) -> FileWritingResult:
        """Write the DataFrame or iterable of DataFrames to a file."""
