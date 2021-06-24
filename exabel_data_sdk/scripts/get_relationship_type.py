import argparse
import sys
from typing import Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.scripts.base_script import BaseScript


class GetRelationshipType(BaseScript):
    """
    Gets a relationship type.
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--name",
            required=True,
            type=str,
            help=(
                "The resource name of the relationship type, "
                "for example 'reltionshipTypes/ns.RELTYPE'"
            ),
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        entity_type = client.relationship_api.get_relationship_type(name=args.name)
        print(entity_type)


if __name__ == "__main__":
    GetRelationshipType(sys.argv, "Get a relationship type.").run()
