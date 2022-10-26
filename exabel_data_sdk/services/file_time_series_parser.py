import abc
import collections
import logging
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Iterator, Mapping, NamedTuple, Optional, Sequence, Set, Tuple

import numpy as np
import pandas as pd
from dateutil import tz
from pandas.core.dtypes.common import is_numeric_dtype

from exabel_data_sdk.client.api.entity_api import EntityApi
from exabel_data_sdk.client.api.resource_creation_result import (
    ResourceCreationResult,
    ResourceCreationStatus,
)
from exabel_data_sdk.services import file_constants
from exabel_data_sdk.services.file_loading_exception import FileLoadingException
from exabel_data_sdk.util.handle_missing_imports import handle_missing_imports
from exabel_data_sdk.util.resource_name_normalization import (
    EntityResourceNames,
    to_entity_resource_names,
    validate_signal_name,
)

logger = logging.getLogger(__name__)

ENTITY_COLUMNS = {
    "entity",
    "isin",
    "factset_identifier",
    "bloomberg_symbol",
    "bloomberg_ticker",
    "figi",
    "mic:ticker",
}
EMPTY_HEADER_PATTERN = re.compile(r"^[Uu]nnamed: ([0-9]+)$")


@dataclass
class TimeSeriesFileParser:
    """
    A parser for a file containing time series.

    For CSV imports, we force the first column to be a string column. This means that signal values
    should not be put in this column. Entity identifiers which start with numbers must be in the
    first column.
    """

    filename: str
    separator: Optional[str]
    worksheet: Any

    def __post_init__(self) -> None:
        self._preview: Optional[pd.DataFrame] = None

    @classmethod
    def from_file(cls, filename: str, separator: str = None) -> Sequence["TimeSeriesFileParser"]:
        """
        Construct a sequence of parsers from a file.

        Multiple parser may be returned for example if the file is an Excel file with multiple
        worksheets.
        """
        if Path(filename).suffix.lower() in file_constants.EXCEL_EXTENSIONS:
            with handle_missing_imports(
                warning="'openpyxl' must be installed to import Excel files", reraise=True
            ):
                import openpyxl
            workbook = openpyxl.load_workbook(filename, read_only=True)
            return [TimeSeriesFileParser(filename, None, s) for s in workbook.sheetnames]
        return [TimeSeriesFileParser(filename, separator, None)]

    @property
    def preview(self) -> pd.DataFrame:
        """Return a preview of the first ten rows of the file."""
        if self._preview is None:
            self._preview = self.parse_file(nrows=10)
        return self._preview

    def sheet_name(self) -> Optional[str]:
        """Return the name of the worksheet, when applicable."""
        return str(self.worksheet) if self.worksheet is not None else None

    def parse_file(self, nrows: int = None, header: Sequence[int] = None) -> pd.DataFrame:
        """Parse the file as a Pandas data frame."""
        extension = Path(self.filename).suffix.lower()
        if extension in file_constants.FULL_CSV_EXTENSIONS:
            df = pd.read_csv(
                self.filename,
                nrows=nrows,
                header=header or [0],
                sep=self.separator or ",",
                keep_default_na=True,
                dtype={0: str},
            )
        elif extension in file_constants.EXCEL_EXTENSIONS:
            df = pd.read_excel(
                self.filename,
                nrows=nrows,
                header=header or [0],
                keep_default_na=True,
                sheet_name=self.worksheet,
                dtype={0: str},
                engine="openpyxl",
            )
        else:
            raise FileLoadingException(f"Unknown file extension '{extension}'")
        if not df.empty:
            df = df.rename(lambda n: n.lower(), axis="columns", level=0)
        return df

    def check_columns(self) -> None:
        """
        Checks that the columns of the file are valid.

        Note that the different subclasses of `ParsedTimeSeriesFile` have stricter validation rules,
        so this check is only a generic check used to give better error messages in cases where the
        data is not valid for any of the formats.

        This function does encode some of the specifics of the different formats we support, so it
        may need to be changed if we want to support more formats.
        """
        reserved = {"date", "known_time", "signal", "value"}
        invalid = []
        entity_column = None
        for column in self.preview.columns:
            if column in ENTITY_COLUMNS:
                entity_column = column
                break
        for column in self.preview.columns:
            if entity_column is not None and column == entity_column:
                continue
            if entity_column is None and _is_valid_entity_column(column, reserved):
                continue
            if column in reserved or _is_valid_signal_name(column, reserved, allow_duplicates=True):
                continue
            if EMPTY_HEADER_PATTERN.match(column):
                raise FileLoadingException("Column with empty header found.")
            invalid.append(column)
        if invalid:
            raise FileLoadingException(
                f"Parsing failed, invalid column(s) found: " f"{', '.join(invalid)}."
            )
        if "date" in self.preview.columns and _has_duplicate_columns(self.preview.columns):
            raise FileLoadingException(
                "File contains duplicate columns: "
                f"{', '.join(_get_duplicate_columns(self.preview.columns))}."
            )


class ParsedTimeSeriesFile(abc.ABC):
    """
    A parsed file containing time series, with a set of helper methods.

    Note that the state of this class is changed by the `set_index()` and `map_entities()` methods,
    and the `set_index()` method should be called before `map_entities()`. These methods must be
    called before the time series can be read through the `get_series()` method.
    """

    class ValidatedTimeSeries(NamedTuple):
        """A tuple of valid time series and failures that did not pass validation."""

        valid_series: Sequence[pd.Series]
        failures: Sequence[ResourceCreationResult[pd.Series]]

    def __init__(self, data: pd.DataFrame, entity_lookup_result: EntityResourceNames):
        self._data = data
        self._entity_lookup_result = entity_lookup_result

    @property
    def data(self) -> pd.DataFrame:
        """Return the data frame containing the time series."""
        return self._data

    @data.setter
    def data(self, data: pd.DataFrame) -> None:
        """Set the data frame containing the time series."""
        self._data = data

    @classmethod
    def from_file(
        cls,
        file_parser: TimeSeriesFileParser,
        entity_api: EntityApi,
        namespace: str,
        entity_mapping: Mapping[str, Mapping[str, str]] = None,
        entity_type: str = None,
    ) -> "ParsedTimeSeriesFile":
        """Read a file and construct a parsed file from the contents."""
        data = file_parser.parse_file()
        return cls.from_data_frame(data, entity_api, namespace, entity_mapping, entity_type)

    @classmethod
    def from_data_frame(
        cls,
        data: pd.DataFrame,
        entity_api: EntityApi,
        namespace: str,
        entity_mapping: Mapping[str, Mapping[str, str]] = None,
        entity_type: str = None,
    ) -> "ParsedTimeSeriesFile":
        """Construct a new parsed file from a data frame."""
        data = cls._set_index(data)
        data, entity_lookup_result = cls._map_entities(
            data, entity_api, namespace, entity_mapping, entity_type
        )
        return cls(data, entity_lookup_result)

    @classmethod
    def can_parse(cls, file_parser: TimeSeriesFileParser) -> bool:
        """Read the first lines of the file and checks whether it is parse-able by this parser."""
        return cls.is_valid(file_parser.preview)

    @classmethod
    @abc.abstractmethod
    def is_valid(cls, data: pd.DataFrame) -> bool:
        """Check whether this parser can parse the data in the file."""

    @abc.abstractmethod
    def get_signals(self) -> Sequence[str]:
        """Get the signals."""

    @abc.abstractmethod
    def get_entity_names(self) -> Sequence[str]:
        """Get the entity resource names."""

    @abc.abstractmethod
    def _get_series_with_potential_duplicate_data_points(self, prefix: str) -> Sequence[pd.Series]:
        """Get the time series, with potential duplicate data points."""

    def get_series(self, prefix: str) -> ValidatedTimeSeries:
        """Get the time series."""
        series = self._get_series_with_potential_duplicate_data_points(prefix)
        series_without_duplicate_data_points = [self._drop_duplicate_data_points(s) for s in series]
        series_with_duplicate_indexes = list(
            self._get_time_series_with_duplicates_in_index(series_without_duplicate_data_points)
        )
        series_with_duplicate_indexes_names = set(s.name for s in series_with_duplicate_indexes)
        series = [
            ts
            for ts in series_without_duplicate_data_points
            if ts.name not in series_with_duplicate_indexes_names
        ]
        return self.ValidatedTimeSeries(
            series,
            [
                ResourceCreationResult(ResourceCreationStatus.FAILED, ts)
                for ts in series_with_duplicate_indexes
            ],
        )

    def get_warnings(self) -> Sequence[str]:
        """Get the warnings generated during mapping of entities."""
        return list(map(str, self._entity_lookup_result.warnings))

    def get_entity_lookup_result(self) -> EntityResourceNames:
        """Get the result from the entity lookup."""
        return self._entity_lookup_result

    def has_known_time(self) -> bool:
        """Check whether the data contains 'known_time' timestamps."""
        return isinstance(self._data.index, pd.MultiIndex)

    @abc.abstractmethod
    def validate_numeric(self) -> None:
        """Validate the numeric column(s) of the data."""

    @classmethod
    @abc.abstractmethod
    def _set_index(cls, data: pd.DataFrame) -> pd.DataFrame:
        """Update the index of the data."""

    @classmethod
    @abc.abstractmethod
    def _map_entities(
        cls,
        data: pd.DataFrame,
        entity_api: EntityApi,
        namespace: str,
        entity_mapping: Mapping[str, Mapping[str, str]] = None,
        entity_type: str = None,
    ) -> Tuple[pd.DataFrame, EntityResourceNames]:
        """Map the entities of the data, and return any warnings."""

    @staticmethod
    def _drop_duplicate_data_points(series: pd.Series) -> pd.Series:
        """Drop duplicate data points from the series."""
        duplicates: pd.Series = series.index.duplicated() & series.duplicated()
        if duplicates.any():
            logger.warning(
                "Dropping %d duplicate data point(s) from time series with name: '%s'",
                duplicates.sum(),
                series.name,
            )
        return series[~duplicates]

    @staticmethod
    def _get_time_series_with_duplicates_in_index(
        series: Iterable[pd.Series],
    ) -> Iterator[pd.Series]:
        """Get the time series with duplicates in the index."""
        for ts in series:
            duplicates: np.ndarray = ts.index.duplicated()
            if duplicates.any():
                logger.error(
                    "%d duplicate data point(s) detected in time series with name: '%s'. The time "
                    "series will not be uploaded. This could be a result of multiple identifiers "
                    "mapping to the same entity, or multiple data points exist for the same signal "
                    "and entity at the same date and known time.",
                    duplicates.sum(),
                    ts.name,
                )
                yield ts

    @staticmethod
    def _lookup_entities(
        identifiers: pd.Series,
        entity_api: EntityApi,
        namespace: str,
        entity_mapping: Mapping[str, Mapping[str, str]] = None,
        preserve_namespace: bool = False,
    ) -> EntityResourceNames:
        """Look up the entity identifier, and throw an exception if no entities are found."""
        if not all(isinstance(i, str) for i in identifiers):
            example = next(i for i in identifiers if not isinstance(i, str))
            if example is np.nan:
                raise FileLoadingException("A cell in the entity column was empty.")
            raise FileLoadingException(
                "Entity identifiers were not strings. If there are entity identifiers which are "
                f"numbers, the first column must be the entity column. Example: '{example}'."
            )
        try:
            entity_resource_names = to_entity_resource_names(
                entity_api,
                identifiers,
                namespace=namespace,
                entity_mapping=entity_mapping,
                preserve_namespace=preserve_namespace,
            )
        except ValueError as e:
            raise FileLoadingException(str(e)) from e
        if not identifiers.empty and entity_resource_names.names.dropna().empty:
            raise FileLoadingException("Not able to identify any of the entities.")
        return entity_resource_names


class DateParsingMixin:
    """
    A mixin for those `ParsedTimeSeriesFile` classes which support "date" and "known_time" columns.
    """

    @classmethod
    def _set_index(cls, data: pd.DataFrame) -> pd.DataFrame:
        date_index = cls._try_parsing_date_column(data, "date")
        date_index.name = None
        if "known_time" in data.columns:
            known_time_index = cls._try_parsing_date_column(data, "known_time")
            known_time_index.name = None
            data.set_index([date_index, known_time_index], inplace=True)
            data.drop(columns=["date", "known_time"], inplace=True)
        else:
            data.set_index(date_index, inplace=True)
            data.drop(columns="date", inplace=True)
        return data

    @classmethod
    def _try_parsing_date_column(cls, data: pd.DataFrame, column: str) -> pd.DatetimeIndex:
        try:
            return pd.DatetimeIndex(data[column], tz=tz.tzutc())
        except Exception as e:
            raise FileLoadingException(f"Failed parsing '{column}' column as dates.") from e


class SignalNamesInRows(DateParsingMixin, ParsedTimeSeriesFile):
    """
    Container for files which have a column containing the signal name.

    +-----------------------+------------+-----------+-------------+-------------+
    | entity / figi / etc   | date       | value     | signal      | known_time  |
    +-----------------------+------------+-----------+-------------+-------------+
    | AAPL US               | 2020-01-01 | 10.0      | my_sig      | 2020-01-04  |
    | MSFT US               | 2020-01-02 | 11.0      | my_sig      | 2020-01-05  |
    +-----------------------+------------+-----------+-------------+-------------+

    This format is the only format which allows the user to import empty values for a signal and
    entity, which is useful if an old value should be deleted.

    The entity column and known_time columns are optional.
    """

    RESERVED_COLUMNS = {"date", "value", "signal", "known_time"}
    VALID_COLUMNS = RESERVED_COLUMNS

    @classmethod
    def is_valid(cls, data: pd.DataFrame) -> bool:
        if "signal" not in data.columns:
            return False
        if "value" not in data.columns:
            return False
        if "date" not in data.columns:
            return False
        entity_column = None
        for column in data.columns:
            if column in cls.VALID_COLUMNS:
                continue
            if entity_column is None and _is_valid_entity_column(column, cls.RESERVED_COLUMNS):
                entity_column = column
                continue
            return False
        if _has_duplicate_columns(data.columns):
            return False
        return True

    @classmethod
    def _entity_column(cls, data: pd.DataFrame) -> str:
        for column in data:
            if _is_valid_entity_column(column, cls.RESERVED_COLUMNS):
                return column
        raise ValueError("Entity column not found.")

    def get_signals(self) -> Sequence[str]:
        return list(set(self._data["signal"]))

    def get_entity_names(self) -> Sequence[str]:
        return list(set(self._data["entity"]))

    def validate_numeric(self) -> None:
        values = self._data["value"]
        if not is_numeric_dtype(values) and any(~values.apply(_is_float)):
            raise FileLoadingException("Found at least one non-numeric value in the value column.")

    def _get_series_with_potential_duplicate_data_points(self, prefix: str) -> Sequence[pd.Series]:
        series = []

        for entity, entity_group in self._data.groupby("entity"):
            for signal in self.get_signals():
                ts = entity_group[entity_group["signal"] == signal]
                # Do not drop nan values, as this format is the only way to actually delete values
                # by explicitly importing empty values.
                ts = ts["value"]
                if ts.empty:
                    continue

                ts.name = f"{entity}/{prefix}{signal}"
                series.append(ts)
        return series

    @classmethod
    def _map_entities(
        cls,
        data: pd.DataFrame,
        entity_api: EntityApi,
        namespace: str,
        entity_mapping: Mapping[str, Mapping[str, str]] = None,
        entity_type: str = None,
    ) -> Tuple[pd.DataFrame, EntityResourceNames]:
        if not any(
            _is_valid_entity_column(column, cls.RESERVED_COLUMNS) for column in data.columns
        ):
            data.insert(0, "entity", "entityTypes/global/entities/global")
        entity_column = cls._entity_column(data)
        identifiers = data[entity_column]
        identifiers.name = entity_type or entity_column
        lookup_result = cls._lookup_entities(
            identifiers,
            entity_api,
            namespace,
            entity_mapping,
            preserve_namespace=entity_type is not None,
        )
        data[entity_column] = lookup_result.names
        data.rename(columns={entity_column: "entity"}, inplace=True)
        return data, lookup_result


class SignalNamesInColumns(DateParsingMixin, ParsedTimeSeriesFile):
    """
    Container for files which have one column for each signal.

    +------------------+------------+----------+----------+-------------+
    | bloomberg_symbol | date       | my_sig1  | my_sig2  | known_time  |
    +------------------+------------+----------+----------+-------------+
    | AAPL US          | 2020-01-01 | 10.0     | 22.1     | 2020-01-04  |
    | MSFT US          | 2020-01-02 | 11.0     | 23.1     | 2020-01-05  |
    +------------------+------------+----------+----------+-------------+

    The entities must be in the first column. The `known_time` column is optional.
    """

    RESERVED_COLUMNS = {"date", "known_time", "value", "signal"}
    VALID_COLUMNS = {"date", "known_time"}

    @classmethod
    def is_valid(cls, data: pd.DataFrame) -> bool:
        if "date" not in data:
            return False
        if len(data.columns) < 3:
            return False
        if not _is_valid_entity_column(data.columns[0], cls.RESERVED_COLUMNS):
            return False
        # Check that all columns are valid:
        for column in data.columns[1:]:
            if column not in cls.VALID_COLUMNS and not _is_valid_signal_name(
                column, cls.RESERVED_COLUMNS
            ):
                return False
        # Check that there is at least one possible signal column:
        if not any(
            _is_valid_signal_name(column, cls.RESERVED_COLUMNS) for column in data.columns[1:]
        ):
            return False
        if _has_duplicate_columns(data.columns):
            return False
        return True

    def get_signals(self) -> Sequence[str]:
        columns = set(self._data.columns)
        columns.remove("entity")
        return list(columns)

    def get_entity_names(self) -> Sequence[str]:
        return list(set(self._data["entity"]))

    def validate_numeric(self) -> None:
        non_numeric_signals = {}
        for signal in self.get_signals():
            values = self._data[signal]
            if not is_numeric_dtype(values) and any(~values.apply(_is_float)):
                non_numeric_signals[signal] = self._data.loc[~values.apply(_is_float)][
                    "entity"
                ].values
        _check_non_numeric_error(non_numeric_signals)

    def _get_series_with_potential_duplicate_data_points(self, prefix: str) -> Sequence[pd.Series]:
        series = []

        for entity, entity_group in self._data.groupby("entity"):
            for signal in self.get_signals():
                ts = entity_group[signal].dropna()
                if ts.empty:
                    continue

                ts.name = f"{entity}/{prefix}{signal}"
                series.append(ts)
        return series

    @classmethod
    def _map_entities(
        cls,
        data: pd.DataFrame,
        entity_api: EntityApi,
        namespace: str,
        entity_mapping: Mapping[str, Mapping[str, str]] = None,
        entity_type: str = None,
    ) -> Tuple[pd.DataFrame, EntityResourceNames]:
        entity_column = data.columns[0]
        identifiers = data[entity_column]
        identifiers.name = entity_type or entity_column
        lookup_result = cls._lookup_entities(
            identifiers,
            entity_api,
            namespace,
            entity_mapping,
            preserve_namespace=entity_type is not None,
        )
        data[entity_column] = lookup_result.names
        data = data.loc[~data[entity_column].isnull()]
        data = data.rename(columns={entity_column: "entity"})
        return data, lookup_result


class SignalNamesInColumnsGlobalEntity(SignalNamesInColumns):
    """
    Container for files which have one column for each signal, and no entity column.

    This is the same format as `SignalNamesInColumns` except that there is no entity column.

    +------------+----------+----------+-------------+
    | date       | my_sig1  | my_sig2  | known_time  |
    +------------+----------+----------+-------------+
    | 2020-01-01 | 10.0     | 22.1     | 2020-01-04  |
    | 2020-01-02 | 11.0     | 23.1     | 2020-01-05  |
    +------------+----------+----------+-------------+

    The dates must be in the first column. The `known_time` column is optional.
    """

    RESERVED_COLUMNS = {"date", "known_time", "value", "signal"}
    VALID_COLUMNS = {"date", "known_time"}

    @classmethod
    def is_valid(cls, data: pd.DataFrame) -> bool:
        if data.columns[0] != "date":
            return False
        if len(data.columns) < 2:
            return False
        # Check that all columns are valid:
        for column in data.columns:
            if column not in cls.VALID_COLUMNS and not _is_valid_signal_name(
                column, cls.RESERVED_COLUMNS
            ):
                return False
        # Check that there is at least one possible signal column:
        if not any(_is_valid_signal_name(column, cls.RESERVED_COLUMNS) for column in data.columns):
            return False
        if _has_duplicate_columns(data.columns):
            return False
        return True

    @classmethod
    def _map_entities(
        cls,
        data: pd.DataFrame,
        entity_api: EntityApi,
        namespace: str,
        entity_mapping: Mapping[str, Mapping[str, str]] = None,
        entity_type: str = None,
    ) -> Tuple[pd.DataFrame, EntityResourceNames]:
        if entity_type is not None:
            raise FileLoadingException(
                "entity_type is not supported when loading time series to the global entity."
            )
        data.insert(0, "entity", "entityTypes/global/entities/global")
        identifiers = data.iloc[:, 0]
        lookup_result = cls._lookup_entities(identifiers, entity_api, namespace, entity_mapping)
        return data, lookup_result


class EntitiesInColumns(ParsedTimeSeriesFile):
    """
    Container for files which have one column for each combination of signal and entity.

    The first cell must contain the string "signals", and the second row must contain the entity
    identifiers, with the first cell indicating the company identifier type or entity type. The
    data starts at the third row.

    +------------------+-----------+-------------+
    | signal           | signal_1  | signal_2    |
    +------------------+-----------+-------------+
    | bloomberg_symbol | AAPL US   | MSFT US     |
    +------------------+-----------+-------------+
    | 2020-01-01       | 10.0      | 291.0       |
    | 2020-01-02       | 11.0      | 292.0       |
    +------------------+-----------+-------------+

    Setting known-time is not supported with this format.
    """

    RESERVED_COLUMNS = {"date", "known_time", "signal"}

    @classmethod
    def from_file(
        cls,
        file_parser: TimeSeriesFileParser,
        entity_api: EntityApi,
        namespace: str,
        entity_mapping: Mapping[str, Mapping[str, str]] = None,
        entity_type: str = None,
    ) -> "ParsedTimeSeriesFile":
        """Read a file and construct a new parser from the contents of that file."""
        if entity_type is not None:
            raise FileLoadingException("entity_type is not supported with this format")
        data = file_parser.parse_file(header=[0, 1])
        entity_type = data.columns.get_level_values(1)[0]
        data = cls._set_index(data)
        data, warnings = cls._map_entities(data, entity_api, namespace, entity_mapping, entity_type)
        return cls(data, warnings)

    @classmethod
    def is_valid(cls, data: pd.DataFrame) -> bool:
        if data.columns[0] != "signal":
            return False
        if data.empty:
            return False
        if not _is_valid_entity_column(data.iloc[0, 0], cls.RESERVED_COLUMNS):
            return False
        if not all(data.iloc[0, :].apply(lambda s: isinstance(s, str))):
            return False
        if "known_time" in data:
            return False
        for column in data.columns[1:]:
            # When checking if this file is valid, only the first row of the file is parsed into the
            # header. Columns containing data for the same signals (but different entities) are then
            # considered as duplicated by Pandas.
            if not _is_valid_signal_name(column, cls.RESERVED_COLUMNS, allow_duplicates=True):
                return False
        return True

    def get_signals(self) -> Sequence[str]:
        return list(set(str(c) for c in self._data.columns.get_level_values(0)))

    def get_entity_names(self) -> Sequence[str]:
        return list(set(self._data.columns.get_level_values(1)))

    def has_known_time(self) -> bool:
        return False

    def validate_numeric(self) -> None:
        non_numeric_signals = defaultdict(list)
        for signal, entity in self._data.columns:
            values = self._data[(signal, entity)]
            if not is_numeric_dtype(values) and any(~values.apply(_is_float)):
                non_numeric_signals[signal].append(entity)

        _check_non_numeric_error(non_numeric_signals)

    def _get_series_with_potential_duplicate_data_points(self, prefix: str) -> Sequence[pd.Series]:
        series = []

        for signal, entity in self._data.columns:
            ts = self._data[(signal, entity)].dropna()
            if ts.empty:
                continue

            ts.name = f"{entity}/{prefix}{signal}"
            series.append(ts)
        return series

    @classmethod
    def _set_index(cls, data: pd.DataFrame) -> pd.DataFrame:
        date_index = pd.DatetimeIndex(data.iloc[:, 0], tz=tz.tzutc())
        date_index.name = None
        data.set_index(date_index, inplace=True)
        data.drop(columns=data.columns[0], inplace=True)
        return data

    @classmethod
    def _map_entities(
        cls,
        data: pd.DataFrame,
        entity_api: EntityApi,
        namespace: str,
        entity_mapping: Mapping[str, Mapping[str, str]] = None,
        entity_type: str = None,
    ) -> Tuple[pd.DataFrame, EntityResourceNames]:
        identifiers = pd.Series(data.columns.get_level_values(1))
        identifiers.name = entity_type
        lookup_result = cls._lookup_entities(identifiers, entity_api, namespace, entity_mapping)
        data.columns = pd.MultiIndex.from_tuples(
            [(c[0], e) for c, e in zip(data.columns, lookup_result.names)]
        )
        data = data.loc[:, ~data.columns.get_level_values(1).isnull()]
        return data, lookup_result


def _check_non_numeric_error(non_numeric_signals: Mapping[str, Sequence[str]]) -> None:
    def extract_entity_name(element: str) -> str:
        return element.split("/entities/")[-1].split(".")[-1]

    if non_numeric_signals:
        error_message = (
            f"{len(non_numeric_signals)} signal(s) contain non-numeric values. Please "
            f"ensure all values can be parsed to numeric values\n"
        )
        for signal, entities in non_numeric_signals.items():
            error_message = (
                f"{error_message}\n\n"
                f"Signal '{signal}' contains {len(entities)} non-numeric values"
                f"{', check the first five as examples' if len(entities) > 5 else ''}:"
                f"\n{', '.join(extract_entity_name(e) for e in entities[:5])}"
            )
        raise FileLoadingException(error_message)


def _is_float(element: Any) -> bool:
    try:
        float(element)
        return True
    except ValueError:
        return False


def _is_int(element: Any) -> bool:
    try:
        int(element)
        return True
    except ValueError:
        return False


def _is_valid_entity_column(column: str, invalid: Set[str]) -> bool:
    if column in invalid:
        return False
    if len(column) == 0:
        return False
    if EMPTY_HEADER_PATTERN.match(column):
        return False
    if column in ENTITY_COLUMNS:
        return True
    return True


def _is_valid_signal_name(column: str, invalid: Set[str], allow_duplicates: bool = False) -> bool:
    # Pandas adds a `.x` to duplicate columns, for example `col`, `col.1`, `col.2`.
    if allow_duplicates:
        column = _remove_dot_int(column)
    if column in invalid:
        return False
    try:
        validate_signal_name(column)
    except ValueError:
        return False
    return True


def _has_duplicate_columns(columns: Sequence[str]) -> bool:
    return len(_get_duplicate_columns(columns)) > 0


def _get_duplicate_columns(columns: Sequence[str]) -> Sequence[str]:
    without_ints = [_remove_dot_int(column) for column in columns]
    return [column for column, count in collections.Counter(without_ints).items() if count > 1]


def _remove_dot_int(column: str) -> str:
    if "." not in column:
        return column
    *first, last = column.split(".")
    if _is_int(last):
        return ".".join(first)
    return column
