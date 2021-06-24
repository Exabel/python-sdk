import argparse
import sys
from typing import Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.scripts.base_script import BaseScript


class GetEntityType(BaseScript):
    """
    Gets an entity type.
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--name",
            required=True,
            type=str,
            help="The resource name of the entity type, for example 'entityTypes/ns.type'",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        entity_type = client.entity_api.get_entity_type(name=args.name)
        print(entity_type)


if __name__ == "__main__":
    GetEntityType(sys.argv, "Get an entity type.").run()
