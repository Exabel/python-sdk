import argparse
import sys
from typing import Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.scripts.base_script import BaseScript


class SearchEntities(BaseScript):
    """
    Search for entities.
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--entity-type",
            required=False,
            default="entityTypes/company",
            type=str,
            help="The entity type, for example 'entityTypes/company'",
        )
        self.parser.add_argument(
            "--isin",
            required=False,
            type=str,
            help="The ISIN (International Securities Identification Number)",
        )
        self.parser.add_argument(
            "--mic",
            required=False,
            type=str,
            help="The MIC (Market Identifier Code)",
        )
        self.parser.add_argument(
            "--ticker",
            required=False,
            type=str,
            help="The ticker",
        )
        self.parser.add_argument(
            "--bloomberg-ticker",
            required=False,
            type=str,
            help="The Bloomberg ticker",
        )
        self.parser.add_argument(
            "--bloomberg-symbol",
            required=False,
            type=str,
            help="The Bloomberg symbol",
        )
        self.parser.add_argument(
            "--figi",
            required=False,
            type=str,
            help="The FIGI",
        )
        self.parser.add_argument(
            "--factset-identifier",
            required=False,
            type=str,
            help="The FactSet identifier",
        )
        self.parser.add_argument(
            "--text",
            required=False,
            type=str,
            help="Term for free text search",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        terms = {}
        if args.mic is not None:
            terms["mic"] = args.mic
        if args.ticker is not None:
            terms["ticker"] = args.ticker
        if args.isin is not None:
            terms["isin"] = args.isin
        if args.bloomberg_ticker is not None:
            terms["bloomberg_ticker"] = args.bloomberg_ticker
        if args.bloomberg_symbol is not None:
            terms["bloomberg_symbol"] = args.bloomberg_symbol
        if args.figi is not None:
            terms["figi"] = args.figi
        if args.factset_identifier is not None:
            terms["factset_identifier"] = args.factset_identifier
        if args.text is not None:
            terms["text"] = args.text

        entities = client.entity_api.search_for_entities(entity_type=args.entity_type, **terms)

        if not entities:
            print("No entity matches the search criteria.")

        for entity in entities:
            print(entity)


if __name__ == "__main__":
    SearchEntities(sys.argv, "Search for entities.").run()
