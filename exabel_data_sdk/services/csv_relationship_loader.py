import logging
from itertools import chain
from typing import Mapping, Optional, Set, Union

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.bulk_insert import BulkInsertFailedError
from exabel_data_sdk.client.api.data_classes.relationship import Relationship
from exabel_data_sdk.services.csv_exception import CsvLoadingException
from exabel_data_sdk.services.csv_loading_constants import (
    DEFAULT_NUMBER_OF_RETRIES,
    DEFAULT_NUMBER_OF_THREADS,
)
from exabel_data_sdk.services.csv_loading_result import CsvLoadingResult
from exabel_data_sdk.services.csv_reader import CsvReader
from exabel_data_sdk.services.entity_mapping_file_reader import EntityMappingFileReader
from exabel_data_sdk.util.exceptions import TypeConvertionError
from exabel_data_sdk.util.resource_name_normalization import to_entity_resource_names
from exabel_data_sdk.util.type_converter import type_converter

logger = logging.getLogger(__name__)


class CsvRelationshipLoader:
    """
    Processes a CSV file with relationships and creates them in the Exabel Data API.
    """

    def __init__(self, client: ExabelClient):
        self._client = client

    def load_relationships(
        self,
        *,
        filename: str,
        entity_mapping_filename: str = None,
        separator: str = ",",
        namespace: str,
        relationship_type: str,
        entity_from_column: str = None,
        entity_to_column: str = None,
        description_column: str = None,
        property_columns: Mapping[str, type] = None,
        threads: int = DEFAULT_NUMBER_OF_THREADS,
        upsert: bool = False,
        dry_run: bool = False,
        error_on_any_failure: bool = False,
        retries: int = DEFAULT_NUMBER_OF_RETRIES,
        abort_threshold: Optional[float] = 0.5,
    ) -> CsvLoadingResult:
        """
        Load a CSV file and upload the relationships specified therein to the Exabel Data API.

        Args:
            filename: the location of the CSV file
            entity_mapping_filename: the location of the entity mapping file to use; only *.json and
                *.csv extensions are supported
            separator: the separator used in the CSV file
            namespace: an Exabel namespace
            relationship_type: the type of relationships to be loaded
            entity_from_column: the column name for the origin entity of the relationship.
                Defaults to the name of the first column in the file if not specified.
            entity_to_column: the column name for the destination entity of the relationship.
                Defaults to the name of the second column in the file if not specified.
            description_column: the column name for the relationship description; if not specified,
                no description is provided
            property_columns: a mapping of column names to data types for the relationship
                properties; if not specified, no properties are provided
            threads: the number of parallel upload threads to run
            upsert: whether relationships should be updated if they already exist
            dry_run: if True, the file is processed, but no relationships are actually uploaded
            error_on_any_failure: if True, an exception is raised if any relationship failed to be
                created
            retries: the maximum number of retries to make for each failed request
            abort_threshold: the threshold for the proportion of failed requests that will cause the
                 upload to be aborted; if it is `None`, the upload is never aborted
        """
        if dry_run:
            logger.info("Running dry-run...")
        use_default_entity_from_to_columns = False
        string_columns: Set[Union[str, int]] = set()
        if entity_from_column is None and entity_to_column is None:
            string_columns.update([0, 1])
            use_default_entity_from_to_columns = True
        elif entity_from_column is not None and entity_to_column is not None:
            string_columns.update([entity_from_column, entity_to_column])
        else:
            raise CsvLoadingException(
                "Both entity_from_column and entity_to_column must be None, or both must be set. "
                f"Got: entity_from_column={entity_from_column}, entity_to_column={entity_to_column}"
            )
        if property_columns is None:
            property_columns = {}
        if description_column:
            string_columns.add(description_column)
        string_columns.update(property_columns)

        relationships_df = CsvReader.read_csv(
            filename, separator, string_columns=string_columns, keep_default_na=False
        )
        if use_default_entity_from_to_columns:
            entity_from_col = relationships_df.columns[0]
            entity_to_col = relationships_df.columns[1]
        else:
            entity_from_col = entity_from_column
            entity_to_col = entity_to_column
        logger.info(
            "Loading %s relationships from %s to %s from %s",
            relationship_type,
            entity_from_col,
            entity_to_col,
            filename,
        )

        description_col = description_column

        relationship_type_name = f"relationshipTypes/{namespace}.{relationship_type}"

        if not self._client.relationship_api.get_relationship_type(relationship_type_name):
            logger.info("Available relationship types are:")
            for rel_type in self._client.relationship_api.list_relationship_types().results:
                logger.info("   %s", rel_type)

            raise CsvLoadingException(
                f"Did not find relationship type {relationship_type_name}, "
                "please create it by running:\n"
                "python -m exabel_data_sdk.scripts.create_relationship_type "
                f"--name={relationship_type_name} [args]"
            )

        entity_mapping = EntityMappingFileReader.read_entity_mapping_file(
            filename=entity_mapping_filename, separator=separator
        )
        # pylint: disable=unsupported-assignment-operation,unsubscriptable-object
        relationships_df[entity_from_col], from_warnings = to_entity_resource_names(
            self._client.entity_api,
            relationships_df[entity_from_col],
            namespace=namespace,
            entity_mapping=entity_mapping,
        )
        relationships_df[entity_to_col], to_warnings = to_entity_resource_names(
            self._client.entity_api,
            relationships_df[entity_to_col],
            namespace=namespace,
            entity_mapping=entity_mapping,
        )
        # pylint: enable=unsupported-assignment-operation,unsubscriptable-object
        warnings = list(chain(from_warnings, to_warnings))

        # Drop rows where either the from or to entity is missing
        relationships_df.dropna(subset=[entity_from_col, entity_to_col], inplace=True)

        if not set(property_columns).issubset(relationships_df.columns):
            raise CsvLoadingException(
                "Property columns must be a subset of columns present in the file. Columns "
                f"missing in the file: {set(property_columns) - set(relationships_df.columns)}"
            )
        try:
            relationships = [
                Relationship(
                    relationship_type=relationship_type_name,
                    from_entity=row[entity_from_col],
                    to_entity=row[entity_to_col],
                    description=row[description_col] if description_col else "",
                    properties={
                        property_key: type_converter(row[property_key], property_type)
                        for property_key, property_type in property_columns.items()
                        if row[property_key]
                    },
                )
                for _, row in relationships_df.iterrows()
            ]
        except TypeConvertionError as e:
            raise CsvLoadingException("An error occurred while converting property types.") from e

        if dry_run:
            logger.info("Loading %d relationships", len(relationships))
            logger.info(relationships)
            return CsvLoadingResult(warnings=warnings)

        try:
            result = self._client.relationship_api.bulk_create_relationships(
                relationships,
                threads=threads,
                upsert=upsert,
                retries=retries,
                abort_threshold=abort_threshold,
            )
            if error_on_any_failure and result.has_failure():
                raise CsvLoadingException(
                    "An error occurred while uploading relationships.",
                    failures=result.get_failures(),
                )
            return CsvLoadingResult(result, warnings=warnings)
        except BulkInsertFailedError as e:
            # An error summary has already been printed.
            if error_on_any_failure:
                raise CsvLoadingException("An error occurred while uploading relationships.") from e
            return CsvLoadingResult(warnings=warnings, aborted=True)
