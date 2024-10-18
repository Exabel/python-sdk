import argparse
import sys
from typing import Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.scripts import utils
from exabel_data_sdk.scripts.base_script import BaseScript


class DeleteDataSet(BaseScript):
    """
    Delete a data set.
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--name",
            required=True,
            type=utils.data_set_resource_name,
            help="The resource name of the data set, for example 'dataSets/ns.transactions'",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        client.data_set_api.delete_data_set(data_set=args.name)
        print("Successfully deleted the data set.")


if __name__ == "__main__":
    DeleteDataSet(sys.argv, "Delete a data set.").run()
