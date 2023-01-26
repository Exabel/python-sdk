from typing import Optional

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.services.csv_loading_constants import (
    DEFAULT_NUMBER_OF_RETRIES,
    DEFAULT_NUMBER_OF_THREADS_FOR_IMPORT,
)
from exabel_data_sdk.services.file_loading_result import FileLoadingResult
from exabel_data_sdk.services.file_time_series_loader import FileTimeSeriesLoader
from exabel_data_sdk.util.deprecate_arguments import deprecate_arguments


class CsvTimeSeriesLoader:
    """
    Processes CSV file with time series and uploads the time series to the Exabel Data API.
    """

    def __init__(self, client: ExabelClient):
        self._client = client

    @deprecate_arguments(namespace=None)
    def load_time_series(
        self,
        *,
        filename: str,
        entity_mapping_filename: Optional[str] = None,
        separator: str = ",",
        pit_current_time: bool = False,
        pit_offset: Optional[int] = None,
        create_missing_signals: bool = False,
        create_tag: bool = True,
        create_library_signal: bool = True,
        global_time_series: Optional[bool] = None,
        threads: int = DEFAULT_NUMBER_OF_THREADS_FOR_IMPORT,
        dry_run: bool = False,
        error_on_any_failure: bool = False,
        retries: int = DEFAULT_NUMBER_OF_RETRIES,
        abort_threshold: Optional[float] = 0.5,
        skip_validation: bool = False,
        # Deprecated arguments
        namespace: Optional[str] = None,  # pylint: disable=unused-argument
    ) -> FileLoadingResult:
        """
        Load a CSV file and upload the time series to the Exabel Data API

        Args:
            filename: the location of the CSV file
            entity_mapping_filename: the location of the entity mapping file to use; only *.json and
                *.csv extensions are supported
            separator: the separator used in the CSV file
            pit_current_time: set the known time of the uploaded data to be the time at which it is
                inserted into the Exabel system
            pit_offset: set the known time of the uploaded data to be the timestamp of each data
                point, plus the specified number of days as an offset; for example, if the data is
                available to the user the day after, this value should be 1
            create_missing_signals: whether signals that are not already present should be
                automatically created
            create_tag: whether a tag containing the entities which have time series should be
                automatically created
            create_library_signal: whether a library signal should be automatically created
            global_time_series: whether to import the time series on the global entity, if not set
                                this will be inferred from the file; an exception is raised if the
                                setting does not match what is found in the file
            threads: the number of parallel upload threads to run
            dry_run: if True, the file is processed, but no time series are actually uploaded
            error_on_any_failure: if True, an  exception is raised if any time series failed to be
                created
            retries: the maximum number of retries to make for each failed request
            abort_threshold: the threshold for the proportion of failed requests that will cause the
                 upload to be aborted; if it is `None`, the upload is never aborted
            skip_validation: if True, the time series are not validated before uploading
        """
        results = FileTimeSeriesLoader(self._client).load_time_series(
            filename=filename,
            entity_mapping_filename=entity_mapping_filename,
            separator=separator,
            pit_current_time=pit_current_time,
            pit_offset=pit_offset,
            create_missing_signals=create_missing_signals,
            create_tag=create_tag,
            create_library_signal=create_library_signal,
            global_time_series=global_time_series,
            threads=threads,
            dry_run=dry_run,
            error_on_any_failure=error_on_any_failure,
            retries=retries,
            abort_threshold=abort_threshold,
            skip_validation=skip_validation,
        )
        if len(results) != 1:
            raise ValueError("Unexpected number of results from time series loading.")
        return results[0]
