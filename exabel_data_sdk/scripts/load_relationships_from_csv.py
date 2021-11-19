import argparse
import sys
from typing import Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.bulk_insert import BulkInsertFailedError
from exabel_data_sdk.client.api.data_classes.relationship import Relationship
from exabel_data_sdk.client.api.data_classes.relationship_type import RelationshipType
from exabel_data_sdk.scripts.csv_script_with_entity_mapping import CsvScriptWithEntityMapping
from exabel_data_sdk.util.resource_name_normalization import to_entity_resource_names


class LoadRelationshipsFromCsv(CsvScriptWithEntityMapping):
    """
    Processes a CSV file with relationships and creates them in the Exabel API.

    The CSV file should have a header line specifying the column names.

    The command line arguments --entity_from_column and --entity_to_column specify the columns
    in which the related entities are given. The entity names are automatically normalized to
    form the corresponding resource names (consistently with the load_entities_from_csv script).

    Optionally, another column may give a description for the relationship.

    The type of the relationship must be specified as a command line argument.
    If the relationship type does not already exist, it is created automatically.

    A sample of a CSV file may look like this:
        brand,product,description
        Spring & Vine,Grapefruit Shampoo,Volumizing Grapefruit & Rosemary Shampoo Bar
        Spring & Vine,Oatmeal Shampoo,Moisturizing Oatmeal Shampoo Bar
        Beyond Meat,Beyond Burger,Plant-based patties

    which would be loaded by specifying:
        --relationship_type my_namespace.HAS_PRODUCT
        --entity_from_column brand
        --entity_to_column product
        --description_column description
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--relationship_type",
            required=True,
            type=str,
            help="The type of the relationships to be loaded. Created if it doesn't already exist.",
        )
        self.parser.add_argument(
            "--entity_from_column",
            required=True,
            type=str,
            help="The column name for the entity from which the relationship originates.",
        )
        self.parser.add_argument(
            "--entity_to_column",
            required=True,
            type=str,
            help="The column name for the entity name to which the relationship goes.",
        )
        self.parser.add_argument(
            "--description_column",
            required=False,
            type=str,
            help="The column name for the relationship description. "
            "If not specified, no description is provided.",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:

        if args.dry_run:
            print("Running dry-run...")

        print(
            f"Loading {args.relationship_type} relationships from {args.entity_from_column} "
            f"to {args.entity_to_column} from {args.filename}"
        )

        string_columns = {args.entity_from_column, args.entity_to_column}
        if args.description_column:
            string_columns.add(args.description_column)

        relationships_df = self.read_csv(args, string_columns=string_columns)

        entity_from_col = args.entity_from_column
        entity_to_col = args.entity_to_column
        description_col = args.description_column

        relationship_type_name = f"relationshipTypes/{args.namespace}.{args.relationship_type}"
        relationship_type = client.relationship_api.get_relationship_type(relationship_type_name)

        if not relationship_type:
            print(f"Did not find relationship type {relationship_type_name}, creating it...")
            relationship_type = RelationshipType(name=relationship_type_name)
            client.relationship_api.create_relationship_type(relationship_type)
            print("Available relationship types are:")
            for rel_type in client.relationship_api.list_relationship_types().results:
                print("   ", rel_type)

        entity_mapping = self.read_entity_mapping_file(args)
        relationships_df[entity_from_col] = to_entity_resource_names(
            client.entity_api,
            relationships_df[entity_from_col],
            namespace=args.namespace,
            entity_mapping=entity_mapping,
        )
        relationships_df[entity_to_col] = to_entity_resource_names(
            client.entity_api,
            relationships_df[entity_to_col],
            namespace=args.namespace,
            entity_mapping=entity_mapping,
        )

        # Drop rows where either the from or to entity is missing
        relationships_df.dropna(subset=[entity_from_col, entity_to_col], inplace=True)

        relationships = [
            Relationship(
                relationship_type=relationship_type_name,
                from_entity=row[entity_from_col],
                to_entity=row[entity_to_col],
                description=row[description_col] if description_col else "",
            )
            for _, row in relationships_df.iterrows()
        ]

        if args.dry_run:
            print("Loading", len(relationships), "relationships")
            print(relationships)
            return

        try:
            client.relationship_api.bulk_create_relationships(relationships, threads=args.threads)
        except BulkInsertFailedError:
            # An error summary has already been printed.
            pass


if __name__ == "__main__":
    LoadRelationshipsFromCsv(sys.argv, "Upload relationships file.").run()
