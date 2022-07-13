import logging
from typing import Mapping, Optional, Union

from pandas import DataFrame, Index
from pandas.core.arrays import ExtensionArray

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.bulk_insert import BulkInsertFailedError
from exabel_data_sdk.client.api.data_classes.entity import Entity
from exabel_data_sdk.services.csv_exception import CsvLoadingException
from exabel_data_sdk.services.csv_loading_constants import (
    DEFAULT_NUMBER_OF_RETRIES,
    DEFAULT_NUMBER_OF_THREADS,
)
from exabel_data_sdk.services.csv_loading_result import CsvLoadingResult
from exabel_data_sdk.services.csv_reader import CsvReader
from exabel_data_sdk.util.exceptions import TypeConvertionError
from exabel_data_sdk.util.resource_name_normalization import normalize_resource_name
from exabel_data_sdk.util.type_converter import type_converter

logger = logging.getLogger(__name__)


class CsvEntityLoader:
    """
    Processes a CSV file with entities and creates them in the Exabel Data API.
    """

    def __init__(self, client: ExabelClient):
        self._client = client

    def load_entities(
        self,
        *,
        filename: str,
        separator: str = ",",
        namespace: str,
        entity_type: str = None,
        name_column: str = None,
        display_name_column: str = None,
        description_column: str = None,
        property_columns: Mapping[str, type] = None,
        threads: int = DEFAULT_NUMBER_OF_THREADS,
        upsert: bool,
        dry_run: bool = False,
        error_on_any_failure: bool = False,
        retries: int = DEFAULT_NUMBER_OF_RETRIES,
        abort_threshold: Optional[float] = 0.5,
    ) -> CsvLoadingResult:
        """
        Load a CSV file and upload the entities specified therein to the Exabel Data API.

        Args:
            filename: the location of the CSV file
            separator: the separator used in the CSV file
            namespace: an Exabel namespace
            entity_type: the type of entities to be loaded (which must already exist in the data
                model); if not specified, it defaults to the name of the name column header
            name_column: the column for the entity name; if not specified, defaults to the first
                column in the file
            display_name_column: the column name for the entity’s display name; if not specified,
                the entity name is used
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
        """
        if dry_run:
            logger.info("Running dry-run...")

        logger.info("Loading entities from %s", filename)
        name_col_ref = name_column or 0
        if property_columns is None:
            property_columns = {}
        string_columns = {
            name_col_ref,
            display_name_column or name_col_ref,
        }
        string_columns.update(property_columns)
        if description_column:
            string_columns.add(description_column)
        entities_df = CsvReader.read_csv(
            filename, separator, string_columns=string_columns, keep_default_na=False
        )

        name_col = name_column or entities_df.columns[0]
        display_name_col = display_name_column or name_col
        description_col = description_column

        entity_type_name = f"entityTypes/{entity_type or name_col}"
        if not self._client.entity_api.get_entity_type(entity_type_name):
            raise CsvLoadingException(
                f"Did not find entity type {entity_type_name}.\n"
                f"The available entity types are: {self._client.entity_api.list_entity_types()}"
            )

        if not set(property_columns).issubset(entities_df.columns):
            raise CsvLoadingException(
                "Property columns must be a subset of columns present in the file. Columns "
                f"missing in the file: {set(property_columns) - set(entities_df.columns)}"
            )
        CsvEntityLoader.detect_duplicate_entities(entities_df, name_col, filename)
        try:
            entities = [
                Entity(
                    name=f"{entity_type_name}/entities/{namespace}."
                    f"{normalize_resource_name(row[name_col])}",
                    display_name=row[display_name_col],
                    description=row[description_col] if description_col else "",
                    properties={
                        property_key: type_converter(row[property_key], property_type)
                        for property_key, property_type in property_columns.items()
                        if row[property_key]
                    },
                )
                for _, row in entities_df.iterrows()
            ]
        except TypeConvertionError as e:
            raise CsvLoadingException("An error occurred while converting property types.") from e

        if dry_run:
            logger.info("Loading %d entities", len(entities))
            logger.info(entities)
            return CsvLoadingResult()

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
                raise CsvLoadingException(
                    "An error occurred while uploading entities.",
                    failures=result.get_failures(),
                )
            return CsvLoadingResult(result)
        except BulkInsertFailedError as e:
            # An error summary has already been printed.
            if error_on_any_failure:
                raise CsvLoadingException("An error occurred while uploading entities.") from e
            return CsvLoadingResult(aborted=True)

    @staticmethod
    def detect_duplicate_entities(
        entities_dataframe: DataFrame,
        name_col: Union[str, None, ExtensionArray, Index],
        filename: str,
    ) -> None:
        """Detects duplicate entities"""
        duplicated_original_names = entities_dataframe[name_col][
            entities_dataframe[name_col].duplicated(keep=False)
        ]
        if not duplicated_original_names.empty:
            logger.error("Fix these duplicate entities in the CSV file: %s", filename)
            logger.error(duplicated_original_names)
            raise ValueError(f"Duplicate entities in {filename}")
