import logging
import os
from typing import Iterable, Union

import pandas as pd

from exabel_data_sdk.services.file_writer import FileWriter

logger = logging.getLogger(__name__)


class CsvWriter(FileWriter):
    """Stores a DataFrame in a CSV file."""

    @staticmethod
    def write_file(df: Union[pd.DataFrame, Iterable[pd.DataFrame]], filepath: str) -> None:
        if isinstance(df, pd.DataFrame):
            df.to_csv(filepath, index=False)
        else:
            mode = "w"
            for chunk in df:
                header = mode == "w"
                chunk.to_csv(filepath, header=header, index=False, mode=mode)
                mode = "a"

        if os.path.isfile(filepath):
            logger.info("Wrote CSV file to: %s", filepath)
