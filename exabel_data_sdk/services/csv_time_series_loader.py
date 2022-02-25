import re
from typing import List, Optional, Sequence

import pandas as pd
from dateutil import tz
from google.protobuf.duration_pb2 import Duration
from pandas.api.types import is_numeric_dtype

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.bulk_insert import BulkInsertFailedError
from exabel_data_sdk.client.api.data_classes.signal import Signal
from exabel_data_sdk.services.csv_exception import CsvLoadingException
from exabel_data_sdk.services.csv_loading_constants import (
    DEFAULT_NUMBER_OF_RETRIES,
    DEFAULT_NUMBER_OF_THREADS,
)
from exabel_data_sdk.services.csv_loading_result import CsvLoadingResult
from exabel_data_sdk.services.csv_reader import CsvReader
from exabel_data_sdk.services.entity_mapping_file_reader import EntityMappingFileReader
from exabel_data_sdk.stubs.exabel.api.data.v1.time_series_messages_pb2 import DefaultKnownTime
from exabel_data_sdk.util.resource_name_normalization import (
    to_entity_resource_names,
    validate_signal_name,
)

# pylint: disable=unsubscriptable-object


class CsvTimeSeriesLoader:
    """
    Processes CSV file with time series and uploads the time series to the Exabel Data API.
    """

    def __init__(self, client: ExabelClient):
        self._client = client

    def load_time_series(
        self,
        *,
        filename: str,
        entity_mapping_filename: str = None,
        separator: str = ",",
        namespace: str,
        pit_current_time: bool = False,
        pit_offset: int = False,
        create_missing_signals: bool = False,
        create_tag: bool = True,
        create_library_signal: bool = True,
        threads: int = DEFAULT_NUMBER_OF_THREADS,
        dry_run: bool = False,
        error_on_any_failure: bool = False,
        retries: int = DEFAULT_NUMBER_OF_RETRIES,
        abort_threshold: Optional[float] = 0.5,
    ) -> CsvLoadingResult:
        """
        Load a CSV file and upload the time series to the Exabel Data API

        Args:
            filename: the location of the CSV file
            entity_mapping_filename: the location of the entity mapping file to use; only *.json and
                *.csv extensions are supported
            separator: the separator used in the CSV file
            namespace: an Exabel namespace
            pit_current_time: set the known time of the uploaded data to be the time at which it is
                inserted into the Exabel system
            pit_offset: set the known time of the uploaded data to be the timestamp of each data
                point, plus the specified number of days as an offset; for example, if the data is
                available to the user the day after, this value should be 1
            create_missing_signals: whether signals that are not already present should be
                automatically created§
            threads: the number of parallel upload threads to run
            dry_run: if True, the file is processed, but no time series are actually uploaded
            error_on_any_failure: if True, an  exception is raised if any time series failed to be
                created
            retries: the maximum number of retries to make for each failed request
            abort_threshold: the threshold for the proportion of failed requests that will cause the
                 upload to be aborted; if it is `None`, the upload is never aborted
        """
        if dry_run:
            print("Running dry-run...")

        default_known_time = None
        if pit_current_time:
            default_known_time = DefaultKnownTime(current_time=True)
        if pit_offset is not None:
            if default_known_time:
                raise CsvLoadingException(
                    "Cannot specify both pit_current_time and pit_offset, it is one or the other"
                )
            time_offset = Duration(seconds=86400 * pit_offset)
            default_known_time = DefaultKnownTime(time_offset=time_offset)

        ts_data = CsvReader.read_csv(
            filename, separator=separator, string_columns=[0], keep_default_na=True
        )
        if ts_data.empty:
            print("No data in time series file.")
            return CsvLoadingResult()
        entity_mapping = EntityMappingFileReader.read_entity_mapping_file(
            entity_mapping_filename, separator=separator
        )
        if ts_data.columns[1] != "date":
            print("Expected second column to be named 'date', got", ts_data.columns[1])

        # signals to produce from this csv file
        signals = list(ts_data.columns[2:])

        if "known_time" in ts_data.columns:
            if pit_current_time:
                raise CsvLoadingException(
                    "Specified pit_current_time on the command line, but file contains known_time"
                    " column.\nEither drop the pit_current_time command line argument, or"
                    " remove the known_time column from the file."
                )
            if pit_offset:
                raise CsvLoadingException(
                    "Specified pit_offset on the command line, but file contains known_time"
                    " column.\nEither drop the pit_offset command line argument, or"
                    " remove the known_time column from the file."
                )
            # This column shall not be loaded as a signal
            signals.remove("known_time")
        else:
            if default_known_time is None:
                raise CsvLoadingException(
                    "The Known-Time of the data must be specified.\n"
                    "Please add a column called known_time in the input file, or specify a "
                    "default policy with the pit_current_time or pit_offset command line "
                    "arguments."
                )
        ts_data.iloc[:, 0], warnings = to_entity_resource_names(
            self._client.entity_api,
            ts_data.iloc[:, 0],
            namespace=namespace,
            entity_mapping=entity_mapping,
        )
        ts_data.rename(columns={ts_data.columns[0]: "entity"}, inplace=True)

        # validate all data points are numeric
        columns_with_invalid_data_points = {}
        for col in signals:
            if not is_numeric_dtype(ts_data[col]):
                examples = {
                    index: ts_data[col][index]
                    for index in ts_data[col][~ts_data[col].str.isnumeric()][:5].index
                }
                columns_with_invalid_data_points[col] = examples

        if columns_with_invalid_data_points:
            error_message = (
                "Signal column(s) contain non-numeric values. Please ensure all values "
                "can be parsed to numeric values.\n"
            )
            error_message += "Columns with non-numeric values (with up to 5 examples):"
            for col, examples in columns_with_invalid_data_points.items():
                pretty_examples = ", ".join(
                    f"'{value}' at index {index}" for index, value in examples.items()
                )
                error_message += f"  {col}: {pretty_examples}"
            raise CsvLoadingException(error_message)

        print("Loading signals", ", ".join(str(s) for s in signals), "...")

        # validate signal names
        missing_header_pattern = re.compile(r"^Unnamed: ([0-9]+)$")
        missing_headers: List[str] = []
        invalid_signals: List[str] = []
        for signal in signals:
            try:
                validate_signal_name(signal)
            except ValueError:
                # Pandas eats up any blank column names and replaces them with "Unnamed: N". Since
                # this is invalid but not the actual column name, we give the end user a more
                # precise error message
                missing_header_match = missing_header_pattern.match(signal)
                if missing_header_match:
                    missing_headers.append(missing_header_match.group(1))
                else:
                    invalid_signals.append(signal)
        if invalid_signals or missing_headers:
            error_message = (
                "Encountered invalid signal names. Signal names must start with a letter, "
                "and can only consist of letters, numbers, and underscore (_), and be "
                "at most 64 characters"
            )
            if invalid_signals:
                error_message += f"Invalid signal names: {', '.join(invalid_signals)}"
            if missing_headers:
                error_message += (
                    f"The following column(s) are missing headers: {', '.join(missing_headers)}"
                )
            raise CsvLoadingException(error_message)

        prefix = "signals/"
        if namespace:
            prefix += namespace + "."

        missing_signals = [
            signal for signal in signals if not self._client.signal_api.get_signal(prefix + signal)
        ]
        if missing_signals:
            print("Available signals are:")
            print(self._client.signal_api.list_signals())
            print("The following signals are missing:")
            print(missing_signals)
            if create_missing_signals and not dry_run:
                print("Creating the missing signals.")
                if not dry_run:
                    for signal in missing_signals:
                        self._client.signal_api.create_signal(
                            Signal(name=prefix + signal, display_name=signal),
                            create_library_signal=create_library_signal,
                        )
            else:
                raise CsvLoadingException(
                    "Aborting script. Please create the missing signals, and try again."
                )

        self.set_time_index(ts_data)
        series = self.get_time_series(ts_data, prefix)

        if dry_run:
            print("Running the script would create the following time series:")
            for ts in series:
                print(f"    {ts.name}")
            return CsvLoadingResult(warnings=warnings)

        try:
            result = self._client.time_series_api.bulk_upsert_time_series(
                series,
                create_tag=create_tag,
                threads=threads,
                default_known_time=default_known_time,
                retries=retries,
                abort_threshold=abort_threshold,
            )
            if error_on_any_failure and result.has_failure():
                raise CsvLoadingException(
                    "An error occurred while uploading time series.",
                    failures=result.get_failures(),
                )
            return CsvLoadingResult(result, warnings=warnings)
        except BulkInsertFailedError as e:
            # An error summary has already been printed.
            if error_on_any_failure:
                raise CsvLoadingException("An error occurred while uploading time series.") from e
            return CsvLoadingResult(warnings=warnings, aborted=True)

    @staticmethod
    def get_time_series(ts_data: pd.DataFrame, prefix: str) -> Sequence[pd.Series]:
        """Extract all the time series from the given data frame."""
        signals = ts_data.columns[1:]
        series = []
        for entity, group in ts_data.groupby("entity"):
            for signal in signals:
                ts = group[signal].dropna()
                if ts.empty:
                    # Skip empty series
                    continue
                ts.name = f"{entity}/{prefix}{signal}"
                series.append(ts)
        return series

    @staticmethod
    def set_time_index(ts_data: pd.DataFrame) -> None:
        """
        Creates a new index for the given data frame.
        There must be a 'date' column, which will be used as (the first level of) the new index.
        If there is a 'known_time' column, then the new index will be a MultiIndex with two levels,
        where the first level is 'date' and the second level is 'known_time'.
        If not, the new index will be a DatetimeIndex.
        The 'date' column is removed from the DataFrame, and so is the 'known_time' column,
        if present.
        """
        date_index = pd.DatetimeIndex(ts_data.date, tz=tz.tzutc())
        date_index.name = None
        if "known_time" in ts_data.columns:
            known_time_index = pd.DatetimeIndex(ts_data.known_time, tz=tz.tzutc())
            known_time_index.name = None
            ts_data.set_index([date_index, known_time_index], inplace=True)
            ts_data.drop(columns=["date", "known_time"], inplace=True)
        else:
            ts_data.set_index(date_index, inplace=True)
            ts_data.drop(columns="date", inplace=True)
