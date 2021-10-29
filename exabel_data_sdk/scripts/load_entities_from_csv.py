import argparse
import sys
from typing import Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.bulk_insert import BulkInsertFailedError
from exabel_data_sdk.client.api.data_classes.entity import Entity
from exabel_data_sdk.scripts.csv_script import CsvScript
from exabel_data_sdk.util.resource_name_normalization import normalize_resource_name


class LoadEntitiesFromCsv(CsvScript):
    """
    Processes a CSV file with entities and creates them in the Exabel API.

    The CSV file should have a header line specifying the column names.

    The command line argument --name_column specifies the column from which to read
    the entity names. The entity names are automatically normalized to create a valid
    resource name for the entity.

    For instance, if the entity type is "brand", and the namespace is "acme", and the entity name
    is "Spring & Vine", the generated resource name will be:
        entityTypes/brand/entities/acme.Spring_Vine

    Optionally, another column may specify a display name for the entity, and another column
    may give a description for the entity.
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--entity_type",
            required=False,
            type=str,
            help="The type of the entities to be loaded. Must already exist in the data model. "
            "If not specified, defaults to the same value as the name_column argument.",
        )
        self.parser.add_argument(
            "--name_column",
            required=False,
            type=str,
            help="The column name for the entity name. "
            "If not specified, defaults to the first column in the file.",
        )
        self.parser.add_argument(
            "--display_name_column",
            required=False,
            type=str,
            help="The column name for the entity's display name. "
            "If not specified, uses the entity name",
        )
        self.parser.add_argument(
            "--description_column",
            required=False,
            type=str,
            help="The column name for the entity description. "
            "If not specified, no description is provided.",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:

        if args.dry_run:
            print("Running dry-run...")

        print("Loading entities from", args.filename)
        name_col_ref = args.name_column or 0
        string_columns = {
            name_col_ref,
            args.display_name_column or name_col_ref,
        }
        if args.description_column:
            string_columns.add(args.description_column)
        entities_df = self.read_csv(args, string_columns=string_columns)

        name_col = args.name_column or entities_df.columns[0]
        display_name_col = args.display_name_column or name_col
        description_col = args.description_column

        entity_type_name = f"entityTypes/{args.entity_type or name_col}"
        entity_type = client.entity_api.get_entity_type(entity_type_name)
        if not entity_type:
            print("Failure: Did not find entity type", entity_type_name)
            print("Available entity types are:")
            print(client.entity_api.list_entity_types())
            sys.exit(1)

        entities = [
            Entity(
                name=f"{entity_type_name}/entities/{args.namespace}."
                f"{normalize_resource_name(row[name_col])}",
                display_name=row[display_name_col],
                description=row[description_col] if description_col else "",
            )
            for _, row in entities_df.iterrows()
        ]

        if args.dry_run:
            print("Loading", len(entities), "entities")
            print(entities)
            return

        try:
            client.entity_api.bulk_create_entities(entities, entity_type_name, threads=args.threads)
        except BulkInsertFailedError:
            # An error summary has already been printed.
            pass


if __name__ == "__main__":
    LoadEntitiesFromCsv(sys.argv, "Upload entities file.").run()
