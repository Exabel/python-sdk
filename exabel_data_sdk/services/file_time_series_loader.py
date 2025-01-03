import logging
from typing import List, Mapping, MutableSequence, Optional, Sequence, Tuple, Type

from google.protobuf.duration_pb2 import Duration
from google.protobuf.field_mask_pb2 import FieldMask

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.bulk_insert import BulkInsertFailedError
from exabel_data_sdk.client.api.data_classes.signal import Signal
from exabel_data_sdk.client.api.resource_creation_result import ResourceCreationResults
from exabel_data_sdk.client.api.search_service import (
    COMPANY_SEARCH_TERM_FIELDS,
    SECURITY_SEARCH_TERM_FIELDS,
)
from exabel_data_sdk.services.csv_loading_constants import (
    DEFAULT_ABORT_THRESHOLD,
    DEFAULT_NUMBER_OF_RETRIES,
    DEFAULT_NUMBER_OF_THREADS,
    DEFAULT_NUMBER_OF_THREADS_FOR_IMPORT,
)
from exabel_data_sdk.services.entity_mapping_file_reader import EntityMappingFileReader
from exabel_data_sdk.services.file_constants import GLOBAL_ENTITY_NAME
from exabel_data_sdk.services.file_loading_exception import FileLoadingException
from exabel_data_sdk.services.file_loading_result import (
    EntityMappingResult,
    FileLoadingResult,
    TimeSeriesFileLoadingResult,
)
from exabel_data_sdk.services.file_time_series_parser import (
    EMPTY_HEADER_PATTERN,
    EntitiesInColumns,
    MetaDataSignalNamesInRows,
    ParsedTimeSeriesFile,
    SignalNamesInColumns,
    SignalNamesInColumnsGlobalEntity,
    SignalNamesInRows,
    TimeSeriesFileParser,
)
from exabel_data_sdk.stubs.exabel.api.data.v1.time_series_messages_pb2 import DefaultKnownTime
from exabel_data_sdk.util.deprecate_arguments import deprecate_arguments
from exabel_data_sdk.util.resource_name_normalization import validate_signal_name

logger = logging.getLogger(__name__)

SIGNAL_PREFIX = "signals/"


class FileTimeSeriesLoader:
    """
    Processes files with time series and uploads the time series to the Exabel Data API.
    """

    def __init__(self, client: ExabelClient):
        self._client = client
        self._time_series_parser: Optional[Type[ParsedTimeSeriesFile]] = None

    @deprecate_arguments(namespace=None, create_tag=None)
    def load_time_series(
        self,
        *,
        filename: str,
        entity_mapping_filename: Optional[str] = None,
        separator: str = ",",
        entity_type: Optional[str] = None,
        identifier_type: Optional[str] = None,
        pit_current_time: Optional[bool] = False,
        pit_offset: Optional[int] = None,
        create_missing_signals: bool = False,
        create_library_signal: bool = True,
        global_time_series: Optional[bool] = None,
        threads: int = DEFAULT_NUMBER_OF_THREADS_FOR_IMPORT,
        dry_run: bool = False,
        error_on_any_failure: bool = False,
        retries: int = DEFAULT_NUMBER_OF_RETRIES,
        abort_threshold: Optional[float] = DEFAULT_ABORT_THRESHOLD,
        batch_size: Optional[int] = None,
        skip_validation: bool = False,
        case_sensitive_signals: bool = False,
        replace_existing_time_series: bool = False,
        replace_existing_data_points: bool = False,
        should_optimise: Optional[bool] = None,
        return_results: bool = True,
        processed_rows: int = 0,
        total_rows: Optional[int] = None,
        # Deprecated arguments
        create_tag: Optional[bool] = None,  # pylint: disable=unused-argument
        namespace: Optional[str] = None,  # pylint: disable=unused-argument
    ) -> Sequence[TimeSeriesFileLoadingResult]:
        """
        Load a file and upload the time series to the Exabel Data API

        If the file has multiple sheets, time series from all the sheets are loaded.

        Args:
            filename: the location of the file, either a CSV or Excel file
            entity_mapping_filename: the location of the entity mapping file to use; only *.json and
                *.csv extensions are supported
            separator: the separator used in the file (only applicable to csv files)
            entity_type: the entity type of the entities in the file. If not specified, the entity
                type is inferred from the column name.
            identifier_type: the identifier type of the entities in the file
            pit_current_time: set the known time of the uploaded data to be the time at which it is
                inserted into the Exabel system
            pit_offset: set the known time of the uploaded data to be the timestamp of each data
                point, plus the specified number of days as an offset; for example, if the data is
                available to the user the day after, this value should be 1
            create_missing_signals: whether signals that are not already present should be
                automatically created
            create_library_signal: whether a library signal should be automatically created
            global_time_series: whether to import the time series on the global entity, if not set
                                this will be inferred from the file; an exception is raised if the
                                setting does not match what is found in the file
            threads: the number of parallel upload threads to run
            dry_run: if True, the file is processed, but no time series are actually uploaded
            error_on_any_failure: if True, an exception is raised if any time series failed to be
                created
            retries: the maximum number of retries to make for each failed request
            abort_threshold: the threshold for the proportion of failed requests that will cause the
                 upload to be aborted; if it is `None`, the upload is never aborted
            batch_size: the number of rows to read and upload in each batch; if not specified, the
                entire file will be read into memory and uploaded in a single batch
            skip_validation: if True, the time series are not validated before uploading
            case_sensitive_signals: if True, signals are case sensitive
            replace_existing_time_series: if True, any existing time series are replaced
            replace_existing_data_points: if True, any existing time series data points are replaced
            should_optimise: Whether time series storage optimisation should be enabled or not. If
                not set, optimisation is at the discretion of the server.
            return_results: if True, returns a list of TimeSeriesFileLoadingResults
                or otherwise an empty list.
            processed_rows: the number of rows already processed
            total_rows: the total number of rows to be processed
        """
        if replace_existing_time_series and replace_existing_data_points:
            raise ValueError(
                "Only one of replace_existing_time_series or replace_existing_data_points can be "
                "true"
            )
        if batch_size is not None:
            logger.info(
                "File format with entities in columns is not supported. Duplicate detection is "
                "best effort."
            )
        entity_mapping = EntityMappingFileReader.read_entity_mapping_file(
            entity_mapping_filename, separator=separator
        )
        results = []
        replaced_time_series: List[str] = []
        for batch_no, parser in enumerate(
            TimeSeriesFileParser.from_file(filename, separator, batch_size), 1
        ):
            if parser.sheet_name():
                logger.info("Uploading sheet: %s", parser.sheet_name())
            elif batch_size is not None:
                logger.info("Uploading batch no: %d", batch_no)
            result = self._load_time_series(
                parser=parser,
                entity_mapping=entity_mapping,
                entity_type=entity_type,
                identifier_type=identifier_type,
                pit_current_time=pit_current_time,
                pit_offset=pit_offset,
                create_missing_signals=create_missing_signals,
                create_library_signal=create_library_signal,
                global_time_series=global_time_series,
                threads=threads,
                dry_run=dry_run,
                error_on_any_failure=error_on_any_failure,
                retries=retries,
                abort_threshold=abort_threshold,
                skip_validation=skip_validation,
                case_sensitive_signals=case_sensitive_signals,
                replace_existing_time_series=replace_existing_time_series,
                replace_existing_data_points=replace_existing_data_points,
                replaced_time_series=replaced_time_series,
                should_optimise=should_optimise,
            )
            if result.processed_rows is not None and total_rows:
                processed_rows = processed_rows + result.processed_rows
                logger.info(
                    "Rows processed: %d / %d. %.1f %%",
                    processed_rows,
                    total_rows,
                    100 * processed_rows / total_rows,
                )
            if replace_existing_time_series and result.replaced:
                replaced_time_series.extend(result.replaced)
            if return_results:
                results.append(result)
        return results

    def _load_time_series(
        self,
        *,
        parser: TimeSeriesFileParser,
        entity_mapping: Optional[Mapping[str, Mapping[str, str]]] = None,
        entity_type: Optional[str] = None,
        identifier_type: Optional[str] = None,
        pit_current_time: Optional[bool] = False,
        pit_offset: Optional[int] = None,
        create_missing_signals: bool = False,
        create_library_signal: bool = True,
        global_time_series: Optional[bool] = None,
        threads: int = DEFAULT_NUMBER_OF_THREADS,
        dry_run: bool = False,
        error_on_any_failure: bool = False,
        retries: int = DEFAULT_NUMBER_OF_RETRIES,
        abort_threshold: Optional[float] = DEFAULT_ABORT_THRESHOLD,
        skip_validation: bool = False,
        case_sensitive_signals: bool = False,
        replace_existing_time_series: bool = False,
        replace_existing_data_points: bool = False,
        replaced_time_series: Optional[Sequence[str]] = None,
        should_optimise: Optional[bool] = None,
    ) -> TimeSeriesFileLoadingResult:
        """
        Load time series from a parser.
        """
        if dry_run:
            logger.info("Running dry-run...")
        if identifier_type:
            if not entity_type:
                raise FileLoadingException(
                    "entity_type must be specified if identifier_type is specified"
                )
            if entity_type == "security" and identifier_type not in SECURITY_SEARCH_TERM_FIELDS:
                raise FileLoadingException(
                    f"Unsupported identifier_type ({identifier_type}) for security."
                )
            if entity_type == "company" and identifier_type not in COMPANY_SEARCH_TERM_FIELDS:
                raise FileLoadingException(
                    f"Unsupported identifier_type ({identifier_type}) for company."
                )
        if pit_offset is not None and pit_current_time:
            raise FileLoadingException(
                "Cannot specify both pit_current_time and pit_offset, it is one or the other"
            )
        if replace_existing_time_series and replace_existing_data_points:
            raise FileLoadingException(
                "Cannot specify both replace_existing_time_series and replace_existing_data_points,"
                " it is one or the other"
            )
        default_known_time = None
        if pit_current_time:
            default_known_time = DefaultKnownTime(current_time=True)
        elif pit_offset is not None:
            time_offset = Duration(seconds=86400 * pit_offset)
            default_known_time = DefaultKnownTime(time_offset=time_offset)
        elif pit_current_time is None and pit_offset is None:
            default_known_time = DefaultKnownTime(current_time=True)

        candidate_parsers: MutableSequence[Type[ParsedTimeSeriesFile]] = []
        if parser.data_frame is None:
            candidate_parsers.append(EntitiesInColumns)
        candidate_parsers += [
            SignalNamesInRows,
            SignalNamesInColumns,
            SignalNamesInColumnsGlobalEntity,
        ]

        parsed_file = None
        for candidate_class in candidate_parsers:
            if candidate_class.can_parse(parser):
                parsed_file = candidate_class.from_file(
                    parser,
                    self._client.entity_api,
                    self._client.namespace,
                    entity_mapping,
                    entity_type=entity_type,
                    case_sensitive_signals=case_sensitive_signals,
                    identifier_type=identifier_type,
                )
                break
        if parsed_file is None:
            parser.check_columns()
            raise FileLoadingException("Column and row setup not recognized.")

        if parsed_file.has_known_time():
            if pit_current_time:
                raise FileLoadingException(
                    "Specified pit_current_time on the command line, but file contains known_time"
                    " column.\nEither drop the pit_current_time command line argument, or remove"
                    " the known_time column from the file."
                )
            if pit_offset is not None:
                raise FileLoadingException(
                    "Specified pit_offset on the command line, but file contains known_time column."
                    "\nEither drop the pit_offset command line argument, or remove the known_time"
                    " column from the file."
                )
        else:
            if default_known_time is None:
                raise FileLoadingException(
                    "The Known-Time of the data must be specified.\nPlease add a column called"
                    " known_time in the input file, or specify a default policy with the"
                    " pit_current_time or pit_offset command line arguments."
                )

        entity_names = parsed_file.get_entity_names()
        check_global_time_series(entity_names, global_time_series)

        file_warnings = parsed_file.get_warnings()
        parsed_file.validate_numeric()
        parsed_file, missing_signals = self._handle_signals(
            create_missing_signals,
            create_library_signal,
            dry_run,
            case_sensitive_signals,
            parsed_file,
        )

        entity_mapping_result = EntityMappingResult(
            parsed_file.get_entity_lookup_result().mapping,
            parsed_file.get_entity_lookup_result().identifier_type,
            parsed_file.get_entity_names(),
            [w.query for w in parsed_file.get_entity_lookup_result().warnings],
        )
        series, invalid_series = parsed_file.get_series(
            prefix=self._get_signal_prefix(),
            skip_validation=skip_validation,
            replace_existing_time_series=replace_existing_time_series,
        )

        if dry_run:
            logger.info("Running the script would create the following time series:")
            for ts in series:
                logger.info("    %s", ts.name)
            if error_on_any_failure and invalid_series:
                raise FileLoadingException(
                    "An error occurred while uploading time series.", failures=invalid_series
                )
            return TimeSeriesFileLoadingResult(
                warnings=file_warnings,
                entity_mapping_result=entity_mapping_result,
                created_data_signals=missing_signals,
                dry_run_results=[str(ts.name) for ts in series],
                sheet_name=parser.sheet_name(),
                has_known_time=parsed_file.has_known_time(),
                processed_rows=len(parsed_file.data),
            )
        try:
            replaced_in_this_batch = []
            if replace_existing_time_series:
                if replaced_time_series is None:
                    replaced_time_series = []
                series_to_replace = []
                series_to_not_replace = []
                result = ResourceCreationResults(0, abort_threshold=abort_threshold)
                for ts in series:
                    if ts.name in replaced_time_series:
                        series_to_not_replace.append(ts)
                    else:
                        series_to_replace.append(ts)
                if series_to_not_replace:
                    logger.info("Uploading already replaced time series")
                    dont_replace_result = self._client.time_series_api.bulk_upsert_time_series(
                        series_to_not_replace,
                        threads=threads,
                        default_known_time=default_known_time,
                        retries=retries,
                        abort_threshold=abort_threshold,
                    )
                    if error_on_any_failure and (
                        dont_replace_result.has_failure() or invalid_series
                    ):
                        raise FileLoadingException(
                            "An error occurred while uploading time series.",
                            failures=[*dont_replace_result.get_failures(), *invalid_series],
                        )
                    result.update(dont_replace_result)
                if series_to_replace:
                    logger.info("Uploading time series to be replaced")
                    replace_result = self._client.time_series_api.bulk_upsert_time_series(
                        series_to_replace,
                        threads=threads,
                        default_known_time=default_known_time,
                        retries=retries,
                        abort_threshold=abort_threshold,
                        replace_existing_time_series=True,
                        should_optimise=should_optimise,
                    )
                    if error_on_any_failure and (replace_result.has_failure() or invalid_series):
                        raise FileLoadingException(
                            "An error occurred while uploading time series.",
                            failures=[*replace_result.get_failures(), *invalid_series],
                        )
                    replaced_in_this_batch = [series.name for series in series_to_replace]
                    result.update(replace_result)
            else:
                result = self._client.time_series_api.bulk_upsert_time_series(
                    series,
                    threads=threads,
                    default_known_time=default_known_time,
                    retries=retries,
                    abort_threshold=abort_threshold,
                    replace_existing_data_points=replace_existing_data_points,
                    should_optimise=should_optimise,
                )
                if error_on_any_failure and (result.has_failure() or invalid_series):
                    raise FileLoadingException(
                        "An error occurred while uploading time series.",
                        failures=[*result.get_failures(), *invalid_series],
                    )
            return TimeSeriesFileLoadingResult(
                result,
                warnings=file_warnings,
                entity_mapping_result=entity_mapping_result,
                created_data_signals=missing_signals,
                sheet_name=parser.sheet_name(),
                has_known_time=parsed_file.has_known_time(),
                replaced=replaced_in_this_batch,
                processed_rows=len(parsed_file.data),
            )
        except BulkInsertFailedError as e:
            # An error summary has already been printed.
            if error_on_any_failure:
                raise FileLoadingException("An error occurred while uploading time series.") from e
            return TimeSeriesFileLoadingResult(
                warnings=file_warnings,
                aborted=True,
                entity_mapping_result=entity_mapping_result,
                created_data_signals=missing_signals,
                sheet_name=parser.sheet_name(),
                has_known_time=parsed_file.has_known_time(),
            )

    def batch_delete_time_series_points(
        self,
        *,
        filename: str,
        entity_mapping_filename: Optional[str] = None,
        separator: str = ",",
        entity_type: Optional[str] = None,
        identifier_type: Optional[str] = None,
        global_time_series: Optional[bool] = None,
        threads: int = DEFAULT_NUMBER_OF_THREADS_FOR_IMPORT,
        dry_run: bool = False,
        retries: int = DEFAULT_NUMBER_OF_RETRIES,
        abort_threshold: Optional[float] = DEFAULT_ABORT_THRESHOLD,
        batch_size: Optional[int] = None,
        skip_validation: bool = False,
        case_sensitive_signals: bool = False,
        return_results: bool = True,
        processed_rows: int = 0,
        total_rows: Optional[int] = None,
    ) -> Sequence[FileLoadingResult]:
        """
        Load a CSV file to delete the time series data points represented in it.

        Args:
            filename: the location of the CSV file
            entity_mapping_filename: the location of the entity mapping file to use; only *.json and
                *.csv extensions are supported
            separator: the separator used in the CSV file
            identifier_type: the identifier type of the entities in the file
            global_time_series: whether to delete the time series data points on the global entity,
                                if not set this will be inferred from the file; an exception is
                                raised if the setting does not match what is found in the file
            threads: the number of parallel delete data points threads to run
            dry_run: if True, the file is processed, but no time series data points are actually
                     deleted
            retries: the maximum number of retries to make for each failed request
            abort_threshold: the threshold for the proportion of failed requests that will cause the
                 process to be aborted; if it is `None`, the upload is never aborted
            skip_validation: if True, the time series are not validated before deletion
            case_sensitive_signals: if True, signals are case sensitive
            return_results: if True, returns a list of FileLoadingResults
                or otherwise an empty list.
            processed_rows: the number of rows already processed
            total_rows: the total number of rows to be processed
        """
        if dry_run:
            logger.info("Running dry-run...")

        logger.info("Deleting time series data points from %s", filename)
        entity_mapping = EntityMappingFileReader.read_entity_mapping_file(
            entity_mapping_filename, separator=separator
        )
        results: List[FileLoadingResult] = []
        for batch_no, parser in enumerate(
            TimeSeriesFileParser.from_file(filename, separator, batch_size), 1
        ):
            if batch_size is not None:
                logger.info("Processing batch no: %d", batch_no)

            candidate_parsers: MutableSequence[Type[ParsedTimeSeriesFile]] = []
            if parser.data_frame is None:
                candidate_parsers.append(EntitiesInColumns)
            candidate_parsers += [
                SignalNamesInRows,
                SignalNamesInColumns,
                SignalNamesInColumnsGlobalEntity,
            ]

            parsed_file = None
            for candidate_class in candidate_parsers:
                if candidate_class.can_parse(parser):
                    parsed_file = candidate_class.from_file(
                        parser,
                        self._client.entity_api,
                        self._client.namespace,
                        entity_mapping,
                        entity_type=entity_type,
                        case_sensitive_signals=case_sensitive_signals,
                        identifier_type=identifier_type,
                    )
                    break

            if parsed_file is None:
                parser.check_columns()
                raise FileLoadingException("Column and row setup not recognized.")

            if not parsed_file.has_known_time():
                raise FileLoadingException(
                    "To delete data points the 'known_time' must be specified in file."
                )

            entity_names = parsed_file.get_entity_names()
            check_global_time_series(entity_names, global_time_series)

            file_warnings = parsed_file.get_warnings()
            parsed_file.validate_numeric()
            signals = parsed_file.get_signals()
            signals_in_rows = isinstance(parsed_file, SignalNamesInRows)

            check_signal_name_errors(signals)

            missing_signals, signals_to_rename = self._check_signals_to_rename(
                signals, case_sensitive_signals, signals_in_rows
            )

            if missing_signals:
                logger.info("The following signals are missing:\n%s", missing_signals)
                raise FileLoadingException("Aborting script. There are unknown signals.")

            if signals_to_rename:
                if signals_in_rows:
                    parsed_file.data["signal"] = parsed_file.data["signal"].replace(
                        signals_to_rename
                    )
                else:
                    parsed_file.data = parsed_file.data.rename(columns=signals_to_rename)

            series, invalid_series = parsed_file.get_series(
                prefix=self._get_signal_prefix(), skip_validation=skip_validation
            )
            if invalid_series:
                # accept failures from API but not invalid_series
                raise FileLoadingException(
                    "An error occurred while deleting time series data points.",
                    failures=[*invalid_series],
                )

            result = self._client.time_series_api.batch_delete_time_series_points(
                series, threads, retries, abort_threshold
            )
            if return_results:
                results.append(
                    FileLoadingResult(
                        result,
                        warnings=list(map(str, file_warnings)),
                        processed_rows=len(parsed_file.data),
                    )
                )
            if len(parsed_file.data) is not None and total_rows:
                processed_rows += len(parsed_file.data)
                logger.info(
                    "Rows processed: %d / %d. %.1f %%",
                    processed_rows,
                    total_rows,
                    100 * processed_rows / total_rows,
                )
        return results

    def load_time_series_metadata(
        self,
        *,
        filename: str,
        entity_mapping_filename: Optional[str] = None,
        separator: str = ",",
        entity_type: Optional[str] = None,
        identifier_type: Optional[str] = None,
        create_missing_signals: bool = False,
        create_library_signal: bool = True,
        global_time_series: Optional[bool] = None,
        threads: int = DEFAULT_NUMBER_OF_THREADS,
        dry_run: bool = False,
        error_on_any_failure: bool = False,
        retries: int = DEFAULT_NUMBER_OF_RETRIES,
        abort_threshold: Optional[float] = DEFAULT_ABORT_THRESHOLD,
        batch_size: Optional[int] = None,
        skip_validation: bool = False,
        case_sensitive_signals: bool = False,
        return_results: bool = True,
        processed_rows: int = 0,
        total_rows: Optional[int] = None,
    ) -> Sequence[TimeSeriesFileLoadingResult]:
        """
        Load a file and upload the time series metadata to the Exabel Data API

        If the file has multiple sheets, time series from all the sheets are loaded.

        Args:
            filename: the location of the file, either a CSV or Excel file
            entity_mapping_filename: the location of the entity mapping file to use; only *.json and
                *.csv extensions are supported
            separator: the separator used in the file (only applicable to csv files)
            entity_type: the entity type of the entities in the file. If not specified, the entity
                type is inferred from the column name.
            identifier_type: the identifier type of the entities in the file
            create_missing_signals: whether signals that are not already present should be
                automatically created
            create_library_signal: whether a library signal should be automatically created
            global_time_series: whether to import the time series on the global entity, if not set
                                this will be inferred from the file; an exception is raised if the
                                setting does not match what is found in the file
            threads: the number of parallel upload threads to run
            dry_run: if True, the file is processed, but no time series are actually uploaded
            error_on_any_failure: if True, an exception is raised if any time series failed to be
                created
            retries: the maximum number of retries to make for each failed request
            abort_threshold: the threshold for the proportion of failed requests that will cause the
                 upload to be aborted; if it is `None`, the upload is never aborted
            batch_size: the number of rows to read and upload in each batch; if not specified, the
                entire file will be read into memory and uploaded in a single batch
            skip_validation: if True, the time series are not validated before uploading
            case_sensitive_signals: if True, signals are case sensitive
            return_results: if True, returns a list of FileLoadingResults
                or otherwise an empty list.
            processed_rows: the number of rows already processed
            total_rows: the total number of rows to be processed
        """
        if dry_run:
            logger.info("Running dry-run...")

        logger.info("Uploading time series metadata from %s", filename)
        if identifier_type and not entity_type:
            raise FileLoadingException(
                "entity_type must be specified if identifier_type is specified"
            )
        entity_mapping = EntityMappingFileReader.read_entity_mapping_file(
            entity_mapping_filename, separator=separator
        )
        results = []

        for batch_no, parser in enumerate(
            TimeSeriesFileParser.from_file(filename, separator, batch_size), 1
        ):
            if parser.sheet_name():
                logger.info("Uploading sheet: %s", parser.sheet_name())
            elif batch_size is not None:
                logger.info("Uploading batch no: %d", batch_no)

            parsed_file = None
            if MetaDataSignalNamesInRows.can_parse(parser):
                parsed_file = MetaDataSignalNamesInRows.from_file(
                    parser,
                    self._client.entity_api,
                    self._client.namespace,
                    entity_mapping,
                    entity_type=entity_type,
                    case_sensitive_signals=case_sensitive_signals,
                    identifier_type=identifier_type,
                )

            if parsed_file is None:
                parser.check_columns()
                raise FileLoadingException("Column and row setup not recognized.")

            entity_names = parsed_file.get_entity_names()
            check_global_time_series(entity_names, global_time_series)

            file_warnings = parsed_file.get_warnings()
            parsed_file.validate_numeric()
            parsed_file, missing_signals = self._handle_signals(
                create_missing_signals,
                create_library_signal,
                dry_run,
                case_sensitive_signals,
                parsed_file,
            )

            entity_mapping_result = EntityMappingResult(
                parsed_file.get_entity_lookup_result().mapping,
                parsed_file.get_entity_lookup_result().identifier_type,
                parsed_file.get_entity_names(),
                [w.query for w in parsed_file.get_entity_lookup_result().warnings],
            )

            series, invalid_series = parsed_file.get_series(
                prefix=self._get_signal_prefix(),
                skip_validation=skip_validation,
            )
            if dry_run:
                logger.info("Running the script would upsert the following time series:")
                for ts in series:
                    logger.info(ts.name)
                    logger.info(ts.units)
                if error_on_any_failure and invalid_series:
                    raise FileLoadingException(
                        "An error occurred while uploading time series.", failures=invalid_series
                    )
                if return_results:
                    results.append(
                        TimeSeriesFileLoadingResult(
                            warnings=file_warnings,
                            entity_mapping_result=entity_mapping_result,
                            created_data_signals=missing_signals,
                            dry_run_results=[str(ts.name) for ts in series],
                            sheet_name=parser.sheet_name(),
                        )
                    )
            else:
                try:
                    result = self._client.time_series_api.bulk_upsert_time_series(
                        series,
                        threads=threads,
                        retries=retries,
                        abort_threshold=abort_threshold,
                    )
                    if error_on_any_failure and (result.has_failure() or invalid_series):
                        raise FileLoadingException(
                            "An error occurred while uploading time series.",
                            failures=[*result.get_failures(), *invalid_series],
                        )
                    if return_results:
                        results.append(
                            TimeSeriesFileLoadingResult(
                                result,
                                warnings=file_warnings,
                                entity_mapping_result=entity_mapping_result,
                                created_data_signals=missing_signals,
                                sheet_name=parser.sheet_name(),
                                processed_rows=len(parsed_file.data),
                            )
                        )
                except BulkInsertFailedError as e:
                    # An error summary has already been printed.
                    if error_on_any_failure:
                        raise FileLoadingException(
                            "An error occurred while uploading time series."
                        ) from e
                    results.append(
                        TimeSeriesFileLoadingResult(
                            warnings=file_warnings,
                            aborted=True,
                            entity_mapping_result=entity_mapping_result,
                            created_data_signals=missing_signals,
                            sheet_name=parser.sheet_name(),
                            has_known_time=parsed_file.has_known_time(),
                        )
                    )
            if len(parsed_file.data) is not None and total_rows:
                processed_rows += len(parsed_file.data)
                logger.info(
                    "Rows processed: %d / %d. %.1f %%",
                    processed_rows,
                    total_rows,
                    100 * processed_rows / total_rows,
                )

        return results

    def _get_signal_prefix(self) -> str:
        """Get signal prefix."""
        if self._client.namespace:
            return SIGNAL_PREFIX + self._client.namespace + "."
        return SIGNAL_PREFIX

    def _check_signals_to_rename(
        self, signals: Sequence[str], case_sensitive_signals: bool, signals_in_rows: bool
    ) -> Tuple[Sequence[str], dict]:
        """
        Check which signals are missing and which signals can be renamed according to case
        sensitivity rules.
        """

        # Signals are reversed because we want to match the first signal returned by the API
        # lexicographically.
        all_signals = {
            signal.name if case_sensitive_signals else signal.name.lower(): signal
            for signal in reversed(list(self._client.signal_api.get_signal_iterator()))
        }

        prefix = self._get_signal_prefix()

        missing_signals = []
        signals_to_rename = {}
        for signal in signals:
            signal_name = prefix + signal if case_sensitive_signals else prefix + signal.lower()
            if signal_name not in all_signals:
                missing_signals.append(signal_name)
                if not case_sensitive_signals and signals_in_rows and signal != signal.lower():
                    signals_to_rename[signal] = signal.lower()
            else:
                signal_match = all_signals[signal_name]
                signal_name = signal_match.name.split(".")[-1]
                if signal_name != signal_match.name or (signals_in_rows and signal != signal_name):
                    signals_to_rename[signal] = signal_name
        return (missing_signals, signals_to_rename)

    def _handle_signals(
        self,
        create_missing_signals: bool,
        create_library_signal: bool,
        dry_run: bool,
        case_sensitive_signals: bool,
        parsed_file: ParsedTimeSeriesFile,
    ) -> Tuple[ParsedTimeSeriesFile, Sequence[str]]:
        """
        Handle signals in a time series file by:
            1. Checking for missing signals
            2. Creating missing signals if necessary
            3. Renaming signals if necessary
        """
        signals = parsed_file.get_signals()
        signals_in_rows = isinstance(parsed_file, SignalNamesInRows)

        check_signal_name_errors(signals)

        missing_signals, signals_to_rename = self._check_signals_to_rename(
            signals, case_sensitive_signals, signals_in_rows
        )

        if missing_signals:
            logger.info("The following signals are missing:\n%s", missing_signals)
            if create_missing_signals:
                logger.info("Creating the missing signals.")
                if not dry_run:
                    for signal in missing_signals:
                        self._client.signal_api.update_signal(
                            Signal(name=signal, display_name=signal),
                            update_mask=FieldMask(paths=["name"]),
                            allow_missing=True,
                            create_library_signal=create_library_signal,
                        )
            else:
                raise FileLoadingException(
                    "Aborting script. Please create the missing signals, and try again."
                )

        if signals_to_rename:
            if signals_in_rows:
                parsed_file.data["signal"] = parsed_file.data["signal"].replace(signals_to_rename)
            else:
                parsed_file.data = parsed_file.data.rename(columns=signals_to_rename)
        return (parsed_file, missing_signals)


def check_global_time_series(
    entity_names: Sequence[str], global_time_series: Optional[bool]
) -> None:
    """
    Perform checks related to global entities and time series.
    """

    if GLOBAL_ENTITY_NAME in entity_names:
        if len(entity_names) > 1:
            raise FileLoadingException(
                "A file cannot contain time series with global and non-global entities."
            )
        if global_time_series is False:
            raise FileLoadingException(
                "The global time series option was not set, but the file contains time series "
                "for the global entity."
            )
    else:
        if global_time_series is True:
            raise FileLoadingException(
                "The global time series option was set, but the file does not contain global "
                "time series."
            )


def check_signal_name_errors(signals: Sequence[str]) -> None:
    """
    Perform checks on signals in a time series file.
    """
    missing_headers: List[str] = []
    invalid_signals: List[str] = []
    for signal in signals:
        try:
            validate_signal_name(signal)
        except ValueError:
            # Pandas eats up any blank column names and replaces them with "Unnamed: N". Since
            # this is invalid but not the actual column name, we give the end user a more
            # precise error message
            missing_header_match = EMPTY_HEADER_PATTERN.match(signal)
            if missing_header_match:
                missing_headers.append(missing_header_match.group(1))
            else:
                invalid_signals.append(signal)

    if invalid_signals or missing_headers:
        error_message = (
            "Encountered invalid signal names. Signal names must start with a letter, "
            "and can only consist of letters, numbers, and underscore (_), and be "
            "at most 64 characters. "
        )
        if invalid_signals:
            error_message += f"Invalid signal names: {', '.join(invalid_signals)}. "
        if missing_headers:
            error_message += (
                f"The following column(s) are missing headers: {', '.join(missing_headers)}."
            )
        raise FileLoadingException(error_message)
