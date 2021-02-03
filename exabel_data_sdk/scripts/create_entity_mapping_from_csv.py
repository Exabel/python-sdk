import argparse
import sys
from typing import List, Sequence

import pandas as pd

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.scripts.base_script import BaseScript


class CreateEntityMappingFromCsv(BaseScript):
    """
    Processes an input CSV file containing client id's to lookup and add Exabel id's mapping

    The CSV file should have a header line on the format
        id1;...;idN
    subsequently followed by rows of id values. The separator is configurable using the
    script argument '--sep' and defaults to ';'

    Example:
        ticker;market
        C;XNAS
        FL;XNYS
        M:US

    Supported id types are:

        * ticker - a company ticker string
        * market - a market identifier code (MIC) or a literal to support lookup
          on several MICs. Supported literals are:
              * 'US' - lookup on "XNYS" and "XNAS"

    Output is on the same format as the input but with 'entity' added as a column.

    Example:
        ticker;market;entity
        C;XNAS;entityTypes/company/entities/company_A
        FL;XNYS;entityTypes/company/entities/company_B
        M;US;entityTypes/company/entities/company_C

    What to do if we can't find a mapping?
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--filename-input",
            required=True,
            type=str,
            help="The URL of the file to parse.",
        )
        self.parser.add_argument(
            "--filename-output",
            required=True,
            type=str,
            help="The URL of the mapping file to write.",
        )
        self.parser.add_argument(
            "--sep", required=False, type=str, default=";", help="Delimiter to use between cells."
        )
        self.parser.add_argument(
            "--entity-type",
            required=False,
            type=str,
            default="entityTypes/company",
            help="The entity type to search for in the mapping",
        )
        self.parser.add_argument(
            "--dry-run",
            required=False,
            action="store_true",
            default=False,
            help="Only print to console instead of mapping.",
        )

    def get_mapping(
        self, client: ExabelClient, args: argparse.Namespace, mapping_input: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Entry method for creating mapping. Will sniff mapping_input to find id's to create
        mappings for

        Args:
              client:        ExabelClient instance
              args:          Command line arguments
              mapping_input: the input ids to lookup mappings for
        """
        if hasattr(mapping_input, "ticker"):
            return self.get_mapping_by_ticker(client, args, mapping_input)
        else:
            print("No recognized id field in input file")
            return mapping_input

    def get_mapping_by_ticker(
        self, client: ExabelClient, args: argparse.Namespace, mapping_input: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Implementation for looking up mappings on ticker / market pairs.
        This will return a DataFrame with the entity mapping added

        Args:
              client:        ExabelClient instance
              args:          Command line arguments
              mapping_input: the input ids to lookup mappings for
        """
        if hasattr(mapping_input, "ticker") and hasattr(mapping_input, "market"):
            print("columns", mapping_input.columns.tolist())
            mapping_output = mapping_input.reindex(
                columns=mapping_input.columns.tolist() + ["entity"], fill_value=""
            )
            print(f"mapping_output : {mapping_output}")

            for i, r in mapping_input.iterrows():
                markets = self.get_markets(r["market"])

                found = False
                for market in markets:
                    print("check on market", market)

                    if args.dry_run:
                        mapping_output.at[i, "entity"] = "dry-run"
                        break

                    entity = client.entity_api.search_for_entities(
                        entity_type=args.entity_type, mic=market, ticker=r["ticker"]
                    )
                    if entity:
                        print(f"found {r['ticker']} on market {market}: {entity[0].name}")
                        mapping_output.at[i, "entity"] = entity[0].name
                        found = True
                        break

                if not found:
                    print("could not find entity mapping for {r}")

        else:
            print("mapping by 'ticker' requires 'market'")
            return mapping_input

        return mapping_output

    def get_markets(self, market: str) -> List[str]:
        """
        Find the list of mic codes we will use to lookup for a given market

        Args:
            market - the market to translate to list of MICs
        """
        if market == "US":
            markets = ["XNAS", "XNYS"]
        else:
            markets = [market]
        return markets

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:

        if args.dry_run:
            print("Running dry-run...")

        mapping_input = pd.read_csv(args.filename_input, header=0, sep=args.sep)
        print(f"input {mapping_input}")
        mapping_input = mapping_input.loc[0:, mapping_input.columns].drop_duplicates()

        mapping_output = self.get_mapping(client, args, mapping_input)

        if args.dry_run:
            print(f"output: {mapping_output}")
        else:
            print(f"output: {mapping_output}")
            mapping_output.to_csv(args.filename_output, sep=args.sep, index=False)


if __name__ == "__main__":
    CreateEntityMappingFromCsv(sys.argv, "Create entity mapping.").run()
