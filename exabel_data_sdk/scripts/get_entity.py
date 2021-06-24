import argparse
import sys
from typing import Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.scripts.base_script import BaseScript


class GetEntity(BaseScript):
    """
    Get an entity.
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--name",
            required=True,
            type=str,
            help=(
                "The resource name of the entity, "
                "for example 'entityTypes/company/entities/identifier'"
            ),
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        entity = client.entity_api.get_entity(name=args.name)
        print(entity)


if __name__ == "__main__":
    GetEntity(sys.argv, "Get an entity.").run()
