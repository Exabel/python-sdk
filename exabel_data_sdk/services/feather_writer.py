import logging
from pathlib import Path
from typing import Iterable, Union

import pandas as pd

from exabel_data_sdk.services.file_writer import FileWriter, FileWritingResult

logger = logging.getLogger(__name__)


class FeatherWriter(FileWriter):
    """Stores a DataFrame in a Feather file."""

    @staticmethod
    def write_file(
        df: Union[pd.DataFrame, Iterable[pd.DataFrame]], filepath: str
    ) -> FileWritingResult:
        rows = 0
        if isinstance(df, pd.DataFrame):
            df.to_feather(filepath)
            rows = len(df)
        else:
            filepath_stem = Path(filepath).stem
            for batch_no, chunk in enumerate(df, 1):
                feather_file = f"{filepath_stem}_{batch_no}.feather"
                chunk.to_feather(feather_file)
                rows += len(chunk)

        return FileWritingResult(rows)
