import argparse
import sys
from typing import List, Sequence

import pandas as pd

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.scripts.base_script import BaseScript


class CreateEntityMappingFromCsv(BaseScript):
    """
    Processes an input CSV file containing client id's to lookup and add Exabel entity mapping.

    The CSV file should have a header line on the format
        id1;...;idN
    subsequently followed by rows of id values. The separator is configurable using the
    script argument '--sep' and defaults to ';'.

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

    def get_entity_mapping_by_ticker(
        self, client: ExabelClient, args: argparse.Namespace, mapping_input: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Create a mapping from ticker / market id to entity.

        Implementation for looking up mappings on ticker / market pairs.
        This will return a DataFrame with the entity mapping added.

        Args:
              client:        ExabelClient instance
              args:          Command line arguments
              mapping_input: the input ids to lookup mappings for
        """

        if "ticker" not in mapping_input or "market" not in mapping_input:
            raise ValueError("The input file must have fields named 'ticker' and 'market'.")

        mapping_output = mapping_input.reindex(
            columns=mapping_input.columns.tolist() + ["entity"], fill_value=""
        )

        for i, row in mapping_input.iterrows():
            ticker = row["ticker"]
            markets = self.get_markets(row["market"])

            found = False
            for market in markets:
                entities = client.entity_api.search_for_entities(
                    entity_type=args.entity_type, mic=market, ticker=ticker
                )
                if len(entities) == 1:
                    mapping_output.at[i, "entity"] = entities[0].name
                    found = True
                    break
                if len(entities) > 1:
                    print(
                        f"Found {len(entities)} entities when searching for {ticker} "
                        f"on market {market} - drop from mapping"
                    )
                    mapping_output = mapping_output.drop(index=i)
                    found = True
                    break

            if not found:
                print(f"Did not find entity for {ticker} in any market - dropping from mapping")
                mapping_output = mapping_output.drop(index=i)

        return mapping_output

    def get_markets(self, market: str) -> List[str]:
        """
        Find the list of MICs we will use in entity search for a given market.

        Args:
            market - the market to translate to list of MICs
        """
        if market == "US":
            markets = ["XNAS", "XNYS"]
        else:
            markets = [market]
        return markets

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:

        mapping_input = pd.read_csv(args.filename_input, header=0, sep=args.sep)
        mapping_input = mapping_input.loc[0:, mapping_input.columns].drop_duplicates()

        try:
            mapping_output = self.get_entity_mapping_by_ticker(client, args, mapping_input)
            mapping_output.to_csv(args.filename_output, sep=args.sep, index=False)
        except ValueError as error:
            print(error)


if __name__ == "__main__":
    CreateEntityMappingFromCsv(sys.argv, "Create entity mapping.").run()
