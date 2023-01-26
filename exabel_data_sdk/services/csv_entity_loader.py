import logging
from typing import Mapping, Optional, Set, Union

from pandas import DataFrame, Index
from pandas.core.arrays import ExtensionArray

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.bulk_insert import BulkInsertFailedError
from exabel_data_sdk.client.api.data_classes.entity import Entity
from exabel_data_sdk.services.csv_loading_constants import (
    DEFAULT_NUMBER_OF_RETRIES,
    DEFAULT_NUMBER_OF_THREADS,
)
from exabel_data_sdk.services.csv_reader import CsvReader
from exabel_data_sdk.services.file_loading_exception import FileLoadingException
from exabel_data_sdk.services.file_loading_result import FileLoadingResult
from exabel_data_sdk.util.case_insensitive_column import get_case_insensitive_column
from exabel_data_sdk.util.deprecate_arguments import deprecate_arguments
from exabel_data_sdk.util.exceptions import TypeConversionError
from exabel_data_sdk.util.resource_name_normalization import normalize_resource_name
from exabel_data_sdk.util.type_converter import type_converter

logger = logging.getLogger(__name__)


class CsvEntityLoader:
    """
    Processes a CSV file with entities and creates them in the Exabel Data API.
    """

    def __init__(self, client: ExabelClient):
        self._client = client

    @deprecate_arguments(name_column="entity_column", namespace=None)
    def load_entities(
        self,
        *,
        filename: str,
        separator: str = ",",
        entity_type: Optional[str] = None,
        entity_column: Optional[str] = None,
        display_name_column: Optional[str] = None,
        description_column: Optional[str] = None,
        property_columns: Optional[Mapping[str, type]] = None,
        threads: int = DEFAULT_NUMBER_OF_THREADS,
        upsert: bool = False,
        dry_run: bool = False,
        error_on_any_failure: bool = False,
        retries: int = DEFAULT_NUMBER_OF_RETRIES,
        abort_threshold: Optional[float] = 0.5,
        batch_size: Optional[int] = None,
        # Deprecated arguments
        name_column: Optional[str] = None,  # pylint: disable=unused-argument
        namespace: Optional[str] = None,  # pylint: disable=unused-argument
    ) -> FileLoadingResult:
        """
        Load a CSV file and upload the entities specified therein to the Exabel Data API.

        Args:
            filename: the location of the CSV file
            separator: the separator used in the CSV file
            entity_type: the type of entities to be loaded (which must already exist in the data
                model); if not specified, it defaults to the name of the name column header
            entity_column: the column for the entity name; if not specified, defaults to the first
                column in the file
            display_name_column: the column name for the entity’s display name; if not specified,
                defaults to the second column in the file, or the entity name if the file only
                contains one column.
            description_column: the column name for the entity description; if not specified, no
                description is provided
            property_columns: a mapping of column names to data types for the entity properties;
                if not specified, no properties are provided
            threads: the number of parallel upload threads to run
            upsert: whether entities should be updated if they already exist
            dry_run: if True, the file is processed, but no entities are actually uploaded
            error_on_any_failure: if True, an exception is raised if any entity failed to be created
            retries: the maximum number of retries to make for each failed request
            abort_threshold: the threshold for the proportion of failed requests that will cause the
                 upload to be aborted; if it is `None`, the upload is never aborted
            batch_size: the number of entities to upload in each batch; if not specified, the
                entire file will be read into memory and uploaded in a single batch
        """
        if dry_run:
            logger.info("Running dry-run...")

        logger.info("Loading entities from %s", filename)
        preview_df = CsvReader.read_file(
            filename, separator, string_columns=[], keep_default_na=False, nrows=0
        )

        string_columns: Set[Union[str, int]] = set()
        name_col_ref = entity_column or 0
        display_name_col_ref = (
            display_name_column or preview_df.columns[1]
            if len(preview_df.columns) > 1
            else name_col_ref
        )
        string_columns.add(get_case_insensitive_column(name_col_ref, preview_df.columns))
        string_columns.add(get_case_insensitive_column(display_name_col_ref, preview_df.columns))
        if property_columns is not None:
            for pc in property_columns:
                string_columns.add(get_case_insensitive_column(pc, preview_df.columns))
        else:
            property_columns = {}
        if description_column:
            string_columns.add(get_case_insensitive_column(description_column, preview_df.columns))
        entities_dfs = CsvReader.read_file(
            filename,
            separator,
            string_columns=string_columns,
            keep_default_na=False,
            chunksize=batch_size,
        )
        if isinstance(entities_dfs, DataFrame):
            entities_dfs = iter((entities_dfs,))
        else:
            logger.info(
                "Processing file in chunks of %d rows. Duplicate detection will be best effort.",
                batch_size,
            )
        combined_result = FileLoadingResult()
        for batch_no, entity_df in enumerate(entities_dfs, start=1):
            logger.info("Processing batch no: %d", batch_no)
            entity_df.columns = entity_df.columns.str.lower()

            name_col = entity_column or entity_df.columns[0]
            display_name_col = (
                display_name_column or entity_df.columns[1]
                if len(entity_df.columns) > 1
                else name_col
            )
            description_col = description_column
            result = self._load_entities(
                data_frame=entity_df,
                name_col=name_col,
                display_name_col=display_name_col,
                description_col=description_col,
                entity_type=entity_type,
                property_columns=property_columns,
                threads=threads,
                upsert=upsert,
                dry_run=dry_run,
                error_on_any_failure=error_on_any_failure,
                retries=retries,
                abort_threshold=abort_threshold,
            )
            combined_result.update(result)

        return combined_result

    def _load_entities(
        self,
        *,
        data_frame: DataFrame,
        entity_type: Optional[str],
        name_col: str,
        display_name_col: str,
        description_col: Optional[str],
        property_columns: Mapping[str, type],
        threads: int = DEFAULT_NUMBER_OF_THREADS,
        upsert: bool = False,
        dry_run: bool = False,
        error_on_any_failure: bool = False,
        retries: int = DEFAULT_NUMBER_OF_RETRIES,
        abort_threshold: Optional[float] = 0.5,
    ) -> FileLoadingResult:
        # Entity types are reversed because we want to match the first entity type returned by the
        # API lexicographically.
        entity_types = {
            et.name.lower(): et
            for et in reversed(list(self._client.entity_api.get_entity_type_iterator()))
        }
        entity_type = entity_type or name_col
        entity_type_name = f"entityTypes/{entity_type}"
        try:
            entity_type_name = entity_types[entity_type_name.lower()].name
        except KeyError as e:
            raise FileLoadingException(f"Did not find entity type: {entity_type_name}") from e
        if not set(property_columns).issubset(data_frame.columns):
            raise FileLoadingException(
                "Property columns must be a subset of columns present in the file. Columns "
                f"missing in the file: {set(property_columns) - set(data_frame.columns)}"
            )
        self.detect_duplicate_entities(data_frame, name_col)
        try:
            entities = [
                Entity(
                    name=f"{entity_type_name}/entities/{self._client.namespace}."
                    f"{normalize_resource_name(row[name_col])}",
                    display_name=row[display_name_col],
                    description=row[description_col] if description_col else "",
                    properties={
                        property_key: type_converter(row[property_key], property_type)
                        for property_key, property_type in property_columns.items()
                        if row[property_key]
                    },
                )
                for _, row in data_frame.iterrows()
            ]
        except TypeConversionError as e:
            raise FileLoadingException("An error occurred while converting property types.") from e

        if dry_run:
            logger.info("Loading %d entities", len(entities))
            logger.info(entities)
            return FileLoadingResult()

        try:
            result = self._client.entity_api.bulk_create_entities(
                entities,
                entity_type_name,
                threads=threads,
                upsert=upsert,
                retries=retries,
                abort_threshold=abort_threshold,
            )
            if error_on_any_failure and result.has_failure():
                raise FileLoadingException(
                    "An error occurred while uploading entities.",
                    failures=result.get_failures(),
                )
            return FileLoadingResult(result)
        except BulkInsertFailedError as e:
            # An error summary has already been printed.
            if error_on_any_failure:
                raise FileLoadingException("An error occurred while uploading entities.") from e
            return FileLoadingResult(aborted=True)

    @staticmethod
    def detect_duplicate_entities(
        entities_dataframe: DataFrame,
        name_col: Union[str, None, ExtensionArray, Index],
    ) -> None:
        """Detects duplicate entities"""
        duplicated_original_names = entities_dataframe[name_col][
            entities_dataframe[name_col].duplicated(keep=False)
        ]
        if not duplicated_original_names.empty:
            logger.error(
                "Fix these duplicate entities:\n%s",
                duplicated_original_names,
            )
            raise ValueError("Duplicate entities detected")
