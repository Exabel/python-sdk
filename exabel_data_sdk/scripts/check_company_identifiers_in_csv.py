import argparse
import sys
from typing import Optional, Sequence

import pandas as pd

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.search_service import COMPANY_SEARCH_TERM_FIELDS
from exabel_data_sdk.scripts.csv_script import CsvScript
from exabel_data_sdk.util.resource_name_normalization import (
    EntityResourceNames,
    to_entity_resource_names,
)


class CheckCompanyIdentifiersInCsv(CsvScript):
    """
    Processes a file and checks if the identifiers in the file are mappable and prints out a table
    with identifiers that cannot be mapped and identifiers that map to the same company.
    """

    def __init__(self, argv: Sequence[str]):
        super().__init__(argv, self.__doc__ or "")
        self.parser.add_argument(
            "--identifier-column",
            required=True,
            type=str,
            help="The column name for the identifiers to look up.",
        )
        self.parser.add_argument(
            "--identifier-type",
            type=str,
            help="The type of the identifiers to look up. Defaults to the same as the column name.",
        )
        self.parser.add_argument(
            "--print-all-identifiers",
            action="store_true",
            help=(
                "Print all identifier mappings in the file, not just the ones that map to the same "
                "company."
            ),
        )

    def _get_identifier_type(
        self, identifier_column: str, identifier_type: Optional[str] = None
    ) -> str:
        _identifier_type = identifier_type or identifier_column
        given_explicit_identifier_type = identifier_type is not None
        if _identifier_type not in COMPANY_SEARCH_TERM_FIELDS:
            message = "The " if given_explicit_identifier_type else "The inferred "
            message += (
                f"identifier type '{_identifier_type}' is not a valid company identifier type. "
                f"Valid types are: {', '.join(COMPANY_SEARCH_TERM_FIELDS)}. "
            )
            if not given_explicit_identifier_type:
                message += "Please specify the identifier type using --identifier-type."
            raise ValueError(message)
        return _identifier_type

    def _process_entity_resource_names(
        self,
        entity_resource_names: EntityResourceNames,
        identifier_type: str,
        keep_all_identifiers: bool,
    ) -> pd.DataFrame:
        all_rows = [
            {identifier_type: warning.query, "entity": None, "warning": str(warning)}
            for warning in entity_resource_names.warnings
        ]
        all_rows.extend(
            {identifier_type: identifier, "entity": entity, "warning": None}
            for identifier, entity in entity_resource_names.mapping.items()
        )
        df = pd.DataFrame(all_rows)
        df.loc[
            (df["entity"].duplicated(keep=False) & ~df["entity"].isna()), "warning"
        ] = "Multiple identifiers mapping to the same company"
        if not keep_all_identifiers:
            df = df[df["warning"].notnull()]
        df = df.fillna("").sort_values(["entity", identifier_type])
        return df

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        data_frame = self.read_csv(args, string_columns=[args.identifier_column])
        data_frame = data_frame[[args.identifier_column]]
        identifiers = data_frame[args.identifier_column].drop_duplicates()
        identifier_type = self._get_identifier_type(args.identifier_column, args.identifier_type)
        identifiers = identifiers.rename(identifier_type)
        entity_resource_names = to_entity_resource_names(
            client.entity_api, identifiers=identifiers, check_entity_types=False
        )
        checked_data_frame = self._process_entity_resource_names(
            entity_resource_names, identifier_type, args.print_all_identifiers
        )
        with pd.option_context(
            "display.max_rows", None, "display.max_columns", None, "display.width", None
        ):
            print(checked_data_frame.to_string(index=False))
            print(
                f"{len(identifiers) - len(checked_data_frame[checked_data_frame['warning']!=''])} "
                f"identifiers successfully mapped to companies out of {len(identifiers)} "
                "identifiers in total"
            )


if __name__ == "__main__":
    CheckCompanyIdentifiersInCsv(sys.argv).run()
