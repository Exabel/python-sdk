import logging
from dataclasses import dataclass
from itertools import chain
from typing import Mapping, Optional, Sequence, Set, Tuple, Union

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.bulk_insert import BulkInsertFailedError
from exabel_data_sdk.client.api.data_classes.relationship import Relationship
from exabel_data_sdk.services.csv_loading_constants import (
    DEFAULT_NUMBER_OF_RETRIES,
    DEFAULT_NUMBER_OF_THREADS,
)
from exabel_data_sdk.services.csv_reader import CsvReader
from exabel_data_sdk.services.entity_mapping_file_reader import EntityMappingFileReader
from exabel_data_sdk.services.file_loading_exception import FileLoadingException
from exabel_data_sdk.services.file_loading_result import FileLoadingResult
from exabel_data_sdk.util.case_insensitive_column import get_case_insensitive_column
from exabel_data_sdk.util.deprecate_arguments import deprecate_arguments
from exabel_data_sdk.util.exceptions import TypeConvertionError
from exabel_data_sdk.util.resource_name_normalization import to_entity_resource_names
from exabel_data_sdk.util.type_converter import type_converter

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class EntityColumnConfiguration:
    """
    The configuration for a column of entities in a data frame.

    Args:
        entity_type:    The entity type of the entities in this column, if `None` the entity type
                        should be inferred from the column name or index.
        name:           The name of the column.
        index:          The index of the column.
    """

    entity_type: Optional[str] = None
    name: Optional[str] = None
    index: Optional[int] = None

    @property
    def reference(self) -> Union[str, int]:
        """
        The column reference, either the column name or the column index.
        """
        if self.name is not None:
            return self.name
        if self.index is not None:
            return self.index
        raise AssertionError

    def __post_init__(self) -> None:
        if self.name is None and self.index is None:
            raise ValueError("Either name or index must be specified")
        if self.name is not None and self.index is not None:
            raise ValueError("Only one of name or index can be specified")


@dataclass(frozen=True)
class RelationshipLoaderColumnConfiguration:
    """
    Configuration for the relationship loader.

    Args:
        from_column:   The column with the entities of which the relationships originate.
        to_column:     The column with the entities of which the relationships goes.
        inferred_entity_types:
                        If `True` the entity type of the entities in the from and to columns will
                        be inferred from the column name or index.
    """

    from_column: EntityColumnConfiguration
    to_column: EntityColumnConfiguration

    @staticmethod
    def _validate_argument_combination(
        from_entity_type: str = None,
        from_identifier_type: str = None,
        from_entity_column: str = None,
        to_entity_type: str = None,
        to_identifier_type: str = None,
        to_entity_column: str = None,
    ) -> None:
        """
        Validate that the argument combination is valid.
        """
        # If either from_entity_type or to_entity_type is specified, both must be specified.
        if not (
            all((from_entity_column, to_entity_column))
            or not any((from_entity_column, to_entity_column))
        ):
            raise ValueError(
                "Either both from_entity_column and to_entity_column must be specified, "
                "or neither of them."
            )

        # If either from_identifier_type or to_identifier_type is specified, both must be specified.
        if not (
            all((from_entity_type, to_entity_type)) or not any((from_entity_type, to_entity_type))
        ):
            raise ValueError(
                "Either both from_entity_type and to_entity_type must be specified, "
                "or neither of them."
            )

        # from and to identifier types can only be specified in combination with from and to entity
        # types.
        if from_identifier_type and from_entity_type != "company":
            if from_entity_type is None:
                raise ValueError(
                    "from_identifier_type can only be specified in combination with "
                    "from_entity_type."
                )
            raise ValueError("Only company entities can be mapped by identifier type.")
        if to_identifier_type and to_entity_type != "company":
            if to_entity_type is None:
                raise ValueError(
                    "to_identifier_type can only be specified in combination with "
                    "to_entity_type."
                )
            raise ValueError("Only company entities can be mapped by identifier type.")

    @classmethod
    def _from_default_values(cls) -> "RelationshipLoaderColumnConfiguration":
        """Create configuration from default arguments (all optional parameters are `None`)."""
        logger.debug("Creating column configuration from default values.")
        return cls(
            from_column=EntityColumnConfiguration(index=0),
            to_column=EntityColumnConfiguration(index=1),
        )

    @classmethod
    def _from_entity_types(
        cls,
        *,
        from_entity_type: str,
        from_identifier_type: str = None,
        from_entity_column: str = None,
        to_entity_type: str,
        to_identifier_type: str = None,
        to_entity_column: str = None,
    ) -> "RelationshipLoaderColumnConfiguration":
        """Create configuration from specified entity types."""
        logger.debug("Creating column configuration from entity types.")
        if from_identifier_type:
            from_entity_type = from_identifier_type
        if to_identifier_type:
            to_entity_type = to_identifier_type
        if from_entity_column and to_entity_column:
            return cls(
                from_column=EntityColumnConfiguration(
                    entity_type=from_entity_type,
                    name=from_entity_column,
                ),
                to_column=EntityColumnConfiguration(
                    entity_type=to_entity_type, name=to_entity_column
                ),
            )
        return cls(
            from_column=EntityColumnConfiguration(entity_type=from_entity_type, index=0),
            to_column=EntityColumnConfiguration(entity_type=to_entity_type, index=1),
        )

    @classmethod
    def _from_specified_columns(
        cls,
        *,
        from_entity_column: str,
        to_entity_column: str,
    ) -> "RelationshipLoaderColumnConfiguration":
        """Create configuration from specified columns."""
        logger.debug("Creating column configuration from specified columns.")
        return cls(
            from_column=EntityColumnConfiguration(name=from_entity_column),
            to_column=EntityColumnConfiguration(name=to_entity_column),
        )

    @classmethod
    def from_arguments(
        cls,
        from_entity_type: str = None,
        from_identifier_type: str = None,
        from_entity_column: str = None,
        to_entity_type: str = None,
        to_identifier_type: str = None,
        to_entity_column: str = None,
    ) -> "RelationshipLoaderColumnConfiguration":
        """
        Create a RelationshipLoaderConfiguration from the given arguments.
        """
        cls._validate_argument_combination(
            from_entity_type,
            from_identifier_type,
            from_entity_column,
            to_entity_type,
            to_identifier_type,
            to_entity_column,
        )
        if from_entity_type and to_entity_type:
            return cls._from_entity_types(
                from_entity_type=from_entity_type,
                from_identifier_type=from_identifier_type,
                from_entity_column=from_entity_column,
                to_entity_type=to_entity_type,
                to_identifier_type=to_identifier_type,
                to_entity_column=to_entity_column,
            )
        if from_entity_column and to_entity_column:
            return cls._from_specified_columns(
                from_entity_column=from_entity_column, to_entity_column=to_entity_column
            )
        if not any(
            (
                from_entity_type,
                from_identifier_type,
                from_entity_column,
                to_entity_type,
                to_identifier_type,
                to_entity_column,
            )
        ):
            return cls._from_default_values()
        raise ValueError("Cannot determine entity types and columns from provided arguments.")

    def get_from_and_to_column_names(self, columns: Sequence[str]) -> Tuple[str, str]:
        """
        Get the from and to column names from the given columns.
        """
        from_entity_column_name = (
            self.from_column.reference
            if isinstance(self.from_column.reference, str)
            else columns[self.from_column.reference]
        )
        to_entity_column_name = (
            self.to_column.reference
            if isinstance(self.to_column.reference, str)
            else columns[self.to_column.reference]
        )
        return from_entity_column_name, to_entity_column_name


class CsvRelationshipLoader:
    """
    Processes a CSV file with relationships and creates them in the Exabel Data API.
    """

    def __init__(self, client: ExabelClient):
        self._client = client

    @deprecate_arguments(
        entity_from_column="from_entity_column", entity_to_column="to_entity_column"
    )
    def load_relationships(
        self,
        *,
        filename: str,
        entity_mapping_filename: str = None,
        separator: str = ",",
        relationship_type: str,
        from_entity_type: str = None,
        from_identifier_type: str = None,
        from_entity_column: str = None,
        to_entity_type: str = None,
        to_identifier_type: str = None,
        to_entity_column: str = None,
        description_column: str = None,
        property_columns: Mapping[str, type] = None,
        threads: int = DEFAULT_NUMBER_OF_THREADS,
        upsert: bool = False,
        dry_run: bool = False,
        error_on_any_failure: bool = False,
        retries: int = DEFAULT_NUMBER_OF_RETRIES,
        abort_threshold: Optional[float] = 0.5,
        # Deprecated arguments:
        entity_from_column: str = None,  # pylint: disable=unused-argument
        entity_to_column: str = None,  # pylint: disable=unused-argument
        namespace: str = None,  # pylint: disable=unused-argument
    ) -> FileLoadingResult:
        """
        Load a CSV file and upload the relationships specified therein to the Exabel Data API.

        Args:
            filename: the location of the CSV file
            entity_mapping_filename: the location of the entity mapping file to use; only *.json and
                *.csv extensions are supported
            separator: the separator used in the CSV file
            relationship_type: the type of relationships to be loaded
            from_entity_type: the entity type of the origin entity of the relationship. Defaults to
                the `from_entity_column` if not specified.
            from_identifier_type: the identifier type to use for looking up entities when
                `from_entity_type` is specified.
            from_entity_column: the column name for the origin entity of the relationship.
                Defaults to the name of the first column in the file if not specified.
            to_entity_type: the entity type of the destination entity of the relationship. Defaults
                to the `to_entity_column` if not specified.
            to_identifier_type: the identifier type to use for looking up entities when
                `to_entity_type` is specified.
            to_entity_column: the column name for the destination entity of the relationship.
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
        try:
            config = RelationshipLoaderColumnConfiguration.from_arguments(
                from_entity_type=from_entity_type,
                from_identifier_type=from_identifier_type,
                from_entity_column=from_entity_column,
                to_entity_type=to_entity_type,
                to_identifier_type=to_identifier_type,
                to_entity_column=to_entity_column,
            )
        except ValueError as e:
            raise FileLoadingException(
                f"Invalid combination of arguments provided: {e.args[0]}"
            ) from e
        preview_df = CsvReader.read_file(
            filename, separator, string_columns=[], keep_default_na=False, nrows=0
        )
        string_columns: Set[Union[str, int]] = set()
        string_columns.update(
            (
                get_case_insensitive_column(config.from_column.reference, preview_df.columns),
                get_case_insensitive_column(config.to_column.reference, preview_df.columns),
            )
        )
        if description_column:
            string_columns.add(get_case_insensitive_column(description_column, preview_df.columns))
        property_columns = property_columns or {}
        for pc in property_columns:
            string_columns.add(get_case_insensitive_column(pc, preview_df.columns))

        relationships_df = CsvReader.read_file(
            filename, separator, string_columns=string_columns, keep_default_na=False
        )
        relationships_df.columns = [column.lower() for column in relationships_df.columns]

        from_entity_column_name, to_entity_column_name = config.get_from_and_to_column_names(
            relationships_df.columns
        )
        logger.info(
            "Loading %s relationships from %s to %s from %s",
            relationship_type,
            from_entity_column_name,
            to_entity_column_name,
            filename,
        )

        relationship_type_name = self.get_relationship_type_name(
            relationship_type=relationship_type, namespace=self._client.namespace
        )
        entity_mapping = EntityMappingFileReader.read_entity_mapping_file(
            filename=entity_mapping_filename, separator=separator
        )
        # pylint: disable=unsubscriptable-object,unsupported-assignment-operation
        from_entity_series = relationships_df[from_entity_column_name]
        if config.from_column.entity_type is not None:
            from_entity_series = from_entity_series.rename(config.from_column.entity_type)
        from_entity_result = to_entity_resource_names(
            self._client.entity_api,
            from_entity_series,
            namespace=self._client.namespace,
            entity_mapping=entity_mapping,
            preserve_namespace=config.from_column.entity_type is not None,
        )
        relationships_df[from_entity_column_name] = from_entity_result.names
        to_entity_series = relationships_df[to_entity_column_name]
        if config.to_column.entity_type is not None:
            to_entity_series = to_entity_series.rename(config.to_column.entity_type)
        to_entity_result = to_entity_resource_names(
            self._client.entity_api,
            to_entity_series,
            namespace=self._client.namespace,
            entity_mapping=entity_mapping,
            preserve_namespace=config.to_column.entity_type is not None,
        )
        relationships_df[to_entity_column_name] = to_entity_result.names
        # pylint: enable=unsubscriptable-object,unsupported-assignment-operation
        warnings = list(chain(from_entity_result.warnings, to_entity_result.warnings))

        # Drop rows where either the from or to entity is missing
        relationships_df = relationships_df.dropna(
            subset=[from_entity_column_name, to_entity_column_name]
        )

        if not set(property_columns).issubset(relationships_df.columns):
            raise FileLoadingException(
                "Property columns must be a subset of columns present in the file. Columns "
                f"missing in the file: {set(property_columns) - set(relationships_df.columns)}"
            )
        try:
            relationships = [
                Relationship(
                    relationship_type=relationship_type_name,
                    from_entity=row[from_entity_column_name],
                    to_entity=row[to_entity_column_name],
                    description=row[description_column] if description_column else "",
                    properties={
                        property_key: type_converter(row[property_key], property_type)
                        for property_key, property_type in property_columns.items()
                        if row[property_key]
                    },
                )
                for _, row in relationships_df.iterrows()
            ]
        except TypeConvertionError as e:
            raise FileLoadingException("An error occurred while converting property types.") from e

        if dry_run:
            logger.info("Loading %d relationships", len(relationships))
            logger.info(relationships)
            return FileLoadingResult(warnings=list(map(str, warnings)))

        try:
            result = self._client.relationship_api.bulk_create_relationships(
                relationships,
                threads=threads,
                upsert=upsert,
                retries=retries,
                abort_threshold=abort_threshold,
            )
            if error_on_any_failure and result.has_failure():
                raise FileLoadingException(
                    "An error occurred while uploading relationships.",
                    failures=result.get_failures(),
                )
            return FileLoadingResult(result, warnings=list(map(str, warnings)))
        except BulkInsertFailedError as e:
            # An error summary has already been printed.
            if error_on_any_failure:
                raise FileLoadingException(
                    "An error occurred while uploading relationships."
                ) from e
            return FileLoadingResult(warnings=list(map(str, warnings)), aborted=True)

    def get_relationship_type_name(self, relationship_type: str, namespace: str) -> str:
        """Get the relationship type name."""
        if "." not in relationship_type:
            relationship_type_name = f"relationshipTypes/{namespace}.{relationship_type}"
        else:
            relationship_type_name = f"relationshipTypes/{relationship_type}"

        if not self._client.relationship_api.get_relationship_type(relationship_type_name):
            logger.info("Available relationship types are:")
            for rel_type in self._client.relationship_api.list_relationship_types().results:
                logger.info("   %s", rel_type)

            raise FileLoadingException(
                f"Did not find relationship type {relationship_type_name}, "
                "please create it by running:\n"
                "python -m exabel_data_sdk.scripts.create_relationship_type "
                f"--name={relationship_type_name} [args]"
            )

        return relationship_type_name
