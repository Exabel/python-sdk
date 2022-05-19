import abc

import pandas as pd


class FileWriter(abc.ABC):
    """Base class for file writers."""

    @staticmethod
    @abc.abstractmethod
    def write_file(df: pd.DataFrame, filepath: str) -> None:
        """Write the DataFrame to a file."""
