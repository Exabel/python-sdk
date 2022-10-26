import argparse
import sys
from typing import Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.search_service import COMPANY_SEARCH_TERM_FIELDS
from exabel_data_sdk.scripts.actions import CaseInsensitiveArgumentAction, DeprecatedArgumentAction
from exabel_data_sdk.scripts.csv_script_with_entity_mapping import CsvScriptWithEntityMapping
from exabel_data_sdk.services.csv_relationship_loader import CsvRelationshipLoader
from exabel_data_sdk.services.file_loading_exception import FileLoadingException
from exabel_data_sdk.util.parse_property_columns import parse_property_columns


class LoadRelationshipsFromCsv(CsvScriptWithEntityMapping):
    """
    Processes a CSV file with relationships and creates them in the Exabel API.

    The CSV file should have a header line specifying the column names.

    The command line arguments --from-entity-column and --to-entity-column specify the columns
    in which the related entities are given. Entity types are inferred from the column names, but
    they can also be specified explicitly with the --from-entity-type and --to-entity-type
    arguments. When entity types are explicitly set, the --from-identifier-type and
    --to-identifier-type arguments can be used to specify the identifier type used to look up the
    entities. Currently, only company identifiers are supported.

    If neither --from-entity-column nor --to-entity-column are specified,
    names of the first and second column in the file will be used respectively.
    If either argument is specified, both must be specified.

    The entity names are automatically normalized to
    form the corresponding resource names (consistently with the load_entities_from_csv script).

    Optionally, another column may give a description for the relationship.

    The type of the relationship must be specified as a command line argument.
    If the relationship type does not already exist, you will be prompted how to create it.

    A sample of a CSV file may look like this:
        brand,product,description
        Spring & Vine,Grapefruit Shampoo,Volumizing Grapefruit & Rosemary Shampoo Bar
        Spring & Vine,Oatmeal Shampoo,Moisturizing Oatmeal Shampoo Bar
        Beyond Meat,Beyond Burger,Plant-based patties

    which would be loaded by specifying:
        --relationship-type my_namespace.HAS_PRODUCT
        --from-entity-column brand
            (defaults to the name of the first column in the file if not specified)
        --to-entity-column product
            (defaults to the name of the second column in the file if not specified)
        --description-column description

    All column names are lower cased after the file is read. For instance, "BRAND" or "BranD"
    becomes "brand".

    Resource lookup in the Exabel API supports case-insensitivity. If there exists a resource where
    a resource identifier matches the lower case column name, this resource will be used.
    If there are multiple resources that match the same column name, the first lexicographical
    match is used.

    Example: The column name for entity from column has value "BRAND" and matches the entity type
    with resource identifier "brand" and "Brand". If both exist, "brand" is chosen.
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
            "--from-entity-type",
            type=str,
            action=CaseInsensitiveArgumentAction,
            help=(
                "The entity type of the entity from which the relationship originates. If not "
                "specified, the entity type will be inferred from the column name."
            ),
        )
        self.parser.add_argument(
            "--from-identifier-type",
            type=str,
            choices=COMPANY_SEARCH_TERM_FIELDS,
            action=CaseInsensitiveArgumentAction,
            help=(
                "The identifier type used to map the entity from which the relationship "
                "originates. If '--from-entity-type' is specified, this argument must be set in "
                "order to look up entities by an identifier."
            ),
        )
        from_entity_group = self.parser.add_mutually_exclusive_group()
        from_entity_group.add_argument(
            "--from-entity-column",
            type=str,
            action=CaseInsensitiveArgumentAction,
            help=(
                "The column name for the entity from which the relationship originates. "
                "Defaults to the name of the first column in the file if not specified. "
                "Supports case-insensitive column names."
            ),
        )
        from_entity_group.add_argument(
            "--entity-from-column",
            dest="from_entity_column",
            type=str,
            help=argparse.SUPPRESS,
            action=DeprecatedArgumentAction,
            case_insensitive=True,
        )
        self.parser.add_argument(
            "--to-entity-type",
            type=str,
            action=CaseInsensitiveArgumentAction,
            help=(
                "The entity type of the entity to which the relationship goes. If not specified, "
                "the entity type will be inferred from the column name."
            ),
        )
        self.parser.add_argument(
            "--to-identifier-type",
            type=str,
            choices=COMPANY_SEARCH_TERM_FIELDS,
            action=CaseInsensitiveArgumentAction,
            help=(
                "The identifier type used to map the entity to which the relationship goes. If "
                "'--to-entity-type' is specified, this argument must be set in order to look up "
                "entities by an identifier."
            ),
        )
        to_entity_group = self.parser.add_mutually_exclusive_group()
        to_entity_group.add_argument(
            "--to-entity-column",
            type=str,
            action=CaseInsensitiveArgumentAction,
            help=(
                "The column name for the entity name to which the relationship goes. "
                "Defaults to the name of the second column in the file if not specified."
                "Supports case-insensitive column names."
            ),
        )
        to_entity_group.add_argument(
            "--entity-to-column",
            dest="to_entity_column",
            type=str,
            help=argparse.SUPPRESS,
            action=DeprecatedArgumentAction,
            case_insensitive=True,
        )
        self.parser.add_argument(
            "--description-column",
            required=False,
            type=str,
            action=CaseInsensitiveArgumentAction,
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
            action=CaseInsensitiveArgumentAction,
            default=[],
            help=(
                "Mappings of column name to data type for the relationship properties. If not "
                "specified, no properties are provided. Should be specified in the following "
                "format: 'column_name:type'. column_name is lower cased by default. "
                "Supported types are bool, str, int, float."
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
                relationship_type=args.relationship_type,
                from_entity_type=args.from_entity_type,
                from_identifier_type=args.from_identifier_type,
                from_entity_column=args.from_entity_column,
                to_entity_type=args.to_entity_type,
                to_identifier_type=args.to_identifier_type,
                to_entity_column=args.to_entity_column,
                description_column=args.description_column,
                property_columns=parse_property_columns(*args.property_columns),
                threads=args.threads,
                upsert=args.upsert,
                dry_run=args.dry_run,
                retries=args.retries,
            )
        except FileLoadingException as e:
            print(e)
            sys.exit(1)


if __name__ == "__main__":
    LoadRelationshipsFromCsv(sys.argv, "Upload relationships file.").run()
