import argparse
import sys
from typing import Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.scripts.actions import CaseInsensitiveArgumentAction, DeprecatedArgumentAction
from exabel_data_sdk.scripts.csv_script import CsvScript
from exabel_data_sdk.services.csv_entity_loader import CsvEntityLoader
from exabel_data_sdk.services.file_loading_exception import FileLoadingException
from exabel_data_sdk.util.exceptions import ParsePropertyColumnsError
from exabel_data_sdk.util.parse_property_columns import parse_property_columns


class LoadEntitiesFromCsv(CsvScript):
    """
    Processes a CSV file with entities and creates them in the Exabel API.

    The CSV file should have a header line specifying the column names.

    The command line argument --name-column specifies the column from which to read
    the entity names. The entity names are automatically normalized to create a valid
    resource name for the entity.

    For instance, if the entity type is "brand", and the namespace is "acme", and the entity name
    is "Spring & Vine", the generated resource name will be:
        entityTypes/brand/entities/acme.Spring_Vine

    Optionally, another column may specify a display name for the entity, and another column
    may give a description for the entity.

    All column names are lower cased after the file is read. For instance, "BRAND" or "BranD"
    becomes "brand".

    Resource lookup in the Exabel API supports case-insensitivity. If there exists a resource where
    a resource identifier matches the lower case column name, this resource will be used.
    If there are multiple resources that match the same column name, the first lexicographical
    match is used.

    Example: The column name "BRAND" matches the entity type with resource identifier "brand"
    and "Brand". If both exist, "brand" is chosen.
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--entity-type",
            required=False,
            type=str,
            help=(
                "The type of the entities to be loaded. Must already exist in the data model. "
                "If not specified, defaults to the same value as the name_column argument."
            ),
        )
        entity_group = self.parser.add_mutually_exclusive_group()
        entity_group.add_argument(
            "--entity-column",
            type=str,
            action=CaseInsensitiveArgumentAction,
            help=(
                "The column name for the entity name. "
                "If not specified, defaults to the first column in the file. "
                "Supports case-insensitive column names."
            ),
        )
        entity_group.add_argument(
            "--name-column",
            dest="entity_column",
            type=str,
            help=argparse.SUPPRESS,
            action=DeprecatedArgumentAction,
            case_insensitive=True,
        )
        self.parser.add_argument(
            "--display-name-column",
            required=False,
            type=str,
            action=CaseInsensitiveArgumentAction,
            help=(
                "The column name for the entity's display name. The value is case insensitive. "
                "If not specified, defaults to the second column in the file, or the entity name "
                "if the file only contains one column."
            ),
        )
        self.parser.add_argument(
            "--description-column",
            required=False,
            type=str,
            action=CaseInsensitiveArgumentAction,
            help=(
                "The column name for the entity description. The value is case insensitive. "
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
                "Mappings of column name to data type for the entity properties. If not "
                "specified, no properties are provided. Should be specified in the following "
                "format: 'column_name:type'. The 'column_name' part is case insensitive. "
                "Supported types are bool, str, int, float."
            ),
        )
        self.parser.add_argument(
            "--upsert",
            required=False,
            action="store_true",
            default=False,
            help="Update entities if they already exist.",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        try:
            CsvEntityLoader(client).load_entities(
                filename=args.filename,
                separator=args.sep,
                entity_type=args.entity_type,
                entity_column=args.entity_column,
                display_name_column=args.display_name_column,
                description_column=args.description_column,
                property_columns=parse_property_columns(*args.property_columns),
                threads=args.threads,
                upsert=args.upsert,
                dry_run=args.dry_run,
                retries=args.retries,
            )
        except (FileLoadingException, ParsePropertyColumnsError) as e:
            print(e)
            sys.exit(1)


if __name__ == "__main__":
    LoadEntitiesFromCsv(sys.argv, "Upload entities file.").run()
