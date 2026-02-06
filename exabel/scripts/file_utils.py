from argparse import ArgumentTypeError

import pandas as pd


def supported_formats_message() -> str:
    """Returns a message with the supported file formats."""
    return "Supported file formats are .csv, .xlsx, .pickle, .feather and .parquet."


def validate_file_extension(file: str) -> str:
    """
    Raises ArgumentTypeError if the file extension is not one of those accepted by 'to_file'.
    Otherwise, returns the given file name.
    Intended to be used as the 'type' of an argparse argument.
    """
    extension = file.split(".")[-1]
    if extension not in ("csv", "xlsx", "pickle", "feather", "parquet"):
        raise ArgumentTypeError(
            f"Unknown file extension {extension}. " + supported_formats_message()
        )
    return file


def to_file(data: pd.DataFrame, file: str) -> None:
    """Writes the given data to a file, with the file type dictated by the file extension."""
    extension = file.split(".")[-1]
    if extension == "csv":
        data.to_csv(file)
    elif extension == "xlsx":
        data.to_excel(file)
    elif extension == "pickle":
        data.to_pickle(file)
    elif extension == "feather":
        # feather only supports string column names.
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = [str(column) for column in data.columns]
        if isinstance(data.index, pd.MultiIndex):
            data = data.reset_index()
        data.to_feather(file)
    elif extension == "parquet":
        data.to_parquet(file)
    else:
        raise ValueError(f"Unknown file extension {extension} in file name {file}")
