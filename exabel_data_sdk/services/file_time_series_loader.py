import logging
from typing import List, Mapping, MutableSequence, Optional, Sequence, Type

from google.protobuf.duration_pb2 import Duration

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.bulk_insert import BulkInsertFailedError
from exabel_data_sdk.client.api.data_classes.signal import Signal
from exabel_data_sdk.client.api.resource_creation_result import ResourceCreationResults
from exabel_data_sdk.services.csv_loading_constants import (
    DEFAULT_NUMBER_OF_RETRIES,
    DEFAULT_NUMBER_OF_THREADS,
    DEFAULT_NUMBER_OF_THREADS_FOR_IMPORT,
)
from exabel_data_sdk.services.entity_mapping_file_reader import EntityMappingFileReader
from exabel_data_sdk.services.file_constants import GLOBAL_ENTITY_NAME
from exabel_data_sdk.services.file_loading_exception import FileLoadingException
from exabel_data_sdk.services.file_loading_result import (
    EntityMappingResult,
    TimeSeriesFileLoadingResult,
)
from exabel_data_sdk.services.file_time_series_parser import (
    EMPTY_HEADER_PATTERN,
    EntitiesInColumns,
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


class FileTimeSeriesLoader:
    """
    Processes files with time series and uploads the time series to the Exabel Data API.
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
        entity_type: Optional[str] = None,
        identifier_type: Optional[str] = None,
        pit_current_time: Optional[bool] = False,
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
        batch_size: Optional[int] = None,
        skip_validation: bool = False,
        case_sensitive_signals: bool = False,
        replace_existing_time_series: bool = False,
        return_results: bool = True,
        # Deprecated arguments
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
            create_tag: whether a tag containing the entities which have time series should be
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
        """
        if batch_size is not None:
            logger.info(
                "Reading input data in batches of %d rows. File format with entities in columns is "
                "not supported. Duplicate detection is best effort.",
                batch_size,
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
                create_tag=create_tag,
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
                replaced_time_series=replaced_time_series,
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
        create_tag: bool = True,
        create_library_signal: bool = True,
        global_time_series: Optional[bool] = None,
        threads: int = DEFAULT_NUMBER_OF_THREADS,
        dry_run: bool = False,
        error_on_any_failure: bool = False,
        retries: int = DEFAULT_NUMBER_OF_RETRIES,
        abort_threshold: Optional[float] = 0.5,
        skip_validation: bool = False,
        case_sensitive_signals: bool = False,
        replace_existing_time_series: bool = False,
        replaced_time_series: Optional[Sequence[str]] = None,
    ) -> TimeSeriesFileLoadingResult:
        """
        Load time series from a parser.
        """
        if dry_run:
            logger.info("Running dry-run...")
        if identifier_type and not entity_type:
            raise FileLoadingException(
                "entity_type must be specified if identifier_type is specified"
            )
        if pit_offset is not None and pit_current_time:
            raise FileLoadingException(
                "Cannot specify both pit_current_time and pit_offset, it is one or the other"
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
                    entity_type=identifier_type or entity_type,
                    case_sensitive_signals=case_sensitive_signals,
                )
                break
        if parsed_file is None:
            parser.check_columns()
            raise FileLoadingException("Column and row setup not recognized.")

        if parsed_file.has_known_time():
            if pit_current_time:
                raise FileLoadingException(
                    "Specified pit_current_time on the command line, but file contains known_time"
                    " column.\nEither drop the pit_current_time command line argument, or"
                    " remove the known_time column from the file."
                )
            if pit_offset is not None:
                raise FileLoadingException(
                    "Specified pit_offset on the command line, but file contains known_time"
                    " column.\nEither drop the pit_offset command line argument, or"
                    " remove the known_time column from the file."
                )
        else:
            if default_known_time is None:
                raise FileLoadingException(
                    "The Known-Time of the data must be specified.\n"
                    "Please add a column called known_time in the input file, or specify a "
                    "default policy with the pit_current_time or pit_offset command line "
                    "arguments."
                )

        entity_names = parsed_file.get_entity_names()
        if GLOBAL_ENTITY_NAME in entity_names:
            if len(entity_names) > 1:
                raise FileLoadingException(
                    "A file cannot contain both time series with and without entities."
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

        warnings = parsed_file.get_warnings()
        parsed_file.validate_numeric()
        signals = parsed_file.get_signals()

        logger.info("Loading signals %s ...", ", ".join(str(s) for s in signals))
        self._check_signal_names(signals)

        prefix = "signals/"
        if self._client.namespace:
            prefix += self._client.namespace + "."

        # Signals are reversed because we want to match the first signal returned by the API
        # lexicographically.
        all_signals = {
            signal.name if case_sensitive_signals else signal.name.lower(): signal
            for signal in reversed(list(self._client.signal_api.get_signal_iterator()))
        }

        missing_signals = []
        signals_to_rename = {}
        for signal in signals:
            signal_name = prefix + signal if case_sensitive_signals else prefix + signal.lower()
            if signal_name not in all_signals:
                missing_signals.append(signal_name)
                if (
                    not case_sensitive_signals
                    and isinstance(parsed_file, SignalNamesInRows)
                    and signal != signal.lower()
                ):
                    signals_to_rename[signal] = signal.lower()
            else:
                signal_match = all_signals[signal_name]
                signal_name = signal_match.name.split(".")[-1]
                if signal_name != signal_match.name or (
                    isinstance(parsed_file, SignalNamesInRows) and signal != signal_name
                ):
                    signals_to_rename[signal] = signal_name

        if missing_signals:
            logger.info("The following signals are missing:\n%s", missing_signals)
            if create_missing_signals:
                logger.info("Creating the missing signals.")
                if not dry_run:
                    for signal in missing_signals:
                        self._client.signal_api.create_signal(
                            Signal(name=signal, display_name=signal),
                            create_library_signal=create_library_signal,
                        )
            else:
                raise FileLoadingException(
                    "Aborting script. Please create the missing signals, and try again."
                )

        if signals_to_rename:
            if isinstance(parsed_file, SignalNamesInRows):
                parsed_file.data["signal"] = parsed_file.data["signal"].replace(signals_to_rename)
            else:
                parsed_file.data = parsed_file.data.rename(columns=signals_to_rename)

        entity_mapping_result = EntityMappingResult(
            parsed_file.get_entity_lookup_result().mapping,
            parsed_file.get_entity_lookup_result().identifier_type,
            parsed_file.get_entity_names(),
            [w.query for w in parsed_file.get_entity_lookup_result().warnings],
        )
        series, invalid_series = parsed_file.get_series(
            prefix=prefix, skip_validation=skip_validation
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
                warnings=warnings,
                entity_mapping_result=entity_mapping_result,
                created_data_signals=missing_signals,
                dry_run_results=[str(ts.name) for ts in series],
                sheet_name=parser.sheet_name(),
                has_known_time=parsed_file.has_known_time(),
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
                        create_tag=create_tag,
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
                        create_tag=create_tag,
                        threads=threads,
                        default_known_time=default_known_time,
                        retries=retries,
                        abort_threshold=abort_threshold,
                        replace_existing_time_series=True,
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
                    create_tag=create_tag,
                    threads=threads,
                    default_known_time=default_known_time,
                    retries=retries,
                    abort_threshold=abort_threshold,
                )
                if error_on_any_failure and (result.has_failure() or invalid_series):
                    raise FileLoadingException(
                        "An error occurred while uploading time series.",
                        failures=[*result.get_failures(), *invalid_series],
                    )
            return TimeSeriesFileLoadingResult(
                result,
                warnings=warnings,
                entity_mapping_result=entity_mapping_result,
                created_data_signals=missing_signals,
                sheet_name=parser.sheet_name(),
                has_known_time=parsed_file.has_known_time(),
                replaced=replaced_in_this_batch,
            )
        except BulkInsertFailedError as e:
            # An error summary has already been printed.
            if error_on_any_failure:
                raise FileLoadingException("An error occurred while uploading time series.") from e
            return TimeSeriesFileLoadingResult(
                warnings=warnings,
                aborted=True,
                entity_mapping_result=entity_mapping_result,
                created_data_signals=missing_signals,
                sheet_name=parser.sheet_name(),
                has_known_time=parsed_file.has_known_time(),
            )

    @staticmethod
    def _check_signal_names(signals: Sequence[str]) -> None:
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
