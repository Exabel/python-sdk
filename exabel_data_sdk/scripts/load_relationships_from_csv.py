import argparse
import sys
from typing import Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.scripts.csv_script_with_entity_mapping import CsvScriptWithEntityMapping
from exabel_data_sdk.services.csv_exception import CsvLoadingException
from exabel_data_sdk.services.csv_relationship_loader import CsvRelationshipLoader
from exabel_data_sdk.util.parse_property_columns import parse_property_columns


class LoadRelationshipsFromCsv(CsvScriptWithEntityMapping):
    """
    Processes a CSV file with relationships and creates them in the Exabel API.

    The CSV file should have a header line specifying the column names.

    The command line arguments --entity-from-column and --entity-to-column specify the columns
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
        --relationship-type my_namespace.HAS_PRODUCT
        --entity-from-column brand
        --entity-to-column product
        --description-column description
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--relationship-type",
            required=True,
            type=str,
            help="The type of the relationships to be loaded.",
        )
        self.parser.add_argument(
            "--entity-from-column",
            required=True,
            type=str,
            help="The column name for the entity from which the relationship originates.",
        )
        self.parser.add_argument(
            "--entity-to-column",
            required=True,
            type=str,
            help="The column name for the entity name to which the relationship goes.",
        )
        self.parser.add_argument(
            "--description-column",
            required=False,
            type=str,
            help=(
                "The column name for the relationship description. "
                "If not specified, no description is provided."
            ),
        )
        self.parser.add_argument(
            "--property-columns",
            nargs="+",
            required=False,
            type=str,
            default=[],
            help=(
                "Mappings of column name to data type for the relationship properties. If not "
                "specified, no properties are provided. Should be specified in the following "
                "format: 'column_name:type'. Supported types are bool, str, int, float."
            ),
        )
        self.parser.add_argument(
            "--upsert",
            required=False,
            action="store_true",
            default=False,
            help="Update relationships if they already exist.",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        try:
            CsvRelationshipLoader(client).load_relationships(
                filename=args.filename,
                entity_mapping_filename=args.entity_mapping_filename,
                separator=args.sep,
                namespace=args.namespace,
                relationship_type=args.relationship_type,
                entity_from_column=args.entity_from_column,
                entity_to_column=args.entity_to_column,
                description_column=args.description_column,
                property_columns=parse_property_columns(*args.property_columns),
                threads=args.threads,
                upsert=args.upsert,
                dry_run=args.dry_run,
                retries=args.retries,
            )
        except CsvLoadingException as e:
            print(e)
            sys.exit(1)


if __name__ == "__main__":
    LoadRelationshipsFromCsv(sys.argv, "Upload relationships file.").run()
