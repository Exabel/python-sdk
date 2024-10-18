import argparse
import sys
from typing import Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.data_set import DataSet, print_data_set
from exabel_data_sdk.scripts import utils
from exabel_data_sdk.scripts.base_script import BaseScript


class CreateDataSet(BaseScript):
    """
    Create a data set.
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--name",
            required=True,
            type=utils.data_set_resource_name,
            help="The resource name of the new data set, for example 'dataSets/ns.transactions'.",
        )
        self.parser.add_argument(
            "--display-name",
            required=True,
            type=str,
            help="The display name of the data set",
        )
        self.parser.add_argument(
            "--description",
            required=False,
            type=str,
            default="",
            help="One or more paragraphs of text description",
        )
        signals_group = self.parser.add_mutually_exclusive_group()
        signals_group.add_argument(
            "--signals",
            required=False,
            type=utils.signal_resource_name,
            nargs="+",
            help="Resource names of signals which should be included.",
        )
        signals_group.add_argument(
            "--signals-file",
            required=False,
            type=str,
            help="A plain text file to read signals from, with one signal resource name per line.",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        signals: Sequence[str] = []
        if args.signals:
            signals = args.signals
        elif args.signals_file:
            signals = utils.read_signals_from_file(args.signals_file)

        data_set = DataSet(
            name=args.name,
            display_name=args.display_name,
            description=args.description,
            signals=list(set(signals)),
        )
        result = client.data_set_api.create_data_set(data_set)
        print_data_set(result)


if __name__ == "__main__":
    CreateDataSet(sys.argv, "Create a data set.").run()
