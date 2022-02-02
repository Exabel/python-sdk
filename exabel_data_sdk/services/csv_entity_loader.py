from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.bulk_insert import BulkInsertFailedError
from exabel_data_sdk.client.api.data_classes.entity import Entity
from exabel_data_sdk.services.csv_exception import CsvLoadingException
from exabel_data_sdk.services.csv_loading_constants import (
    DEFAULT_NUMBER_OF_RETRIES,
    DEFAULT_NUMBER_OF_THREADS,
)
from exabel_data_sdk.services.csv_reader import CsvReader
from exabel_data_sdk.util.resource_name_normalization import normalize_resource_name


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
        threads: int = DEFAULT_NUMBER_OF_THREADS,
        upsert: bool,
        dry_run: bool = False,
        error_on_any_failure: bool = False,
        retries: int = DEFAULT_NUMBER_OF_RETRIES,
    ) -> None:
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
            threads: the number of parallel upload threads to run
            upsert: whether entities should be updated if they already exist
            dry_run: if True, the file is processed, but no entities are actually uploaded
            error_on_any_failure: if True, an exception is raised if any entity failed to be created
            retries: the maximum number of retries to make for each failed request
        """
        if dry_run:
            print("Running dry-run...")

        print("Loading entities from", filename)
        name_col_ref = name_column or 0
        string_columns = {
            name_col_ref,
            display_name_column or name_col_ref,
        }
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

        entities = [
            Entity(
                name=f"{entity_type_name}/entities/{namespace}."
                f"{normalize_resource_name(row[name_col])}",
                display_name=row[display_name_col],
                description=row[description_col] if description_col else "",
            )
            for _, row in entities_df.iterrows()
        ]

        if dry_run:
            print("Loading", len(entities), "entities")
            print(entities)
            return

        try:
            result = self._client.entity_api.bulk_create_entities(
                entities, entity_type_name, threads=threads, upsert=upsert, retries=retries
            )
            if error_on_any_failure and result.has_failure():
                raise CsvLoadingException("An error occurred while uploading entities.")
        except BulkInsertFailedError as e:
            # An error summary has already been printed.
            if error_on_any_failure:
                raise CsvLoadingException("An error occurred while uploading entities.") from e
