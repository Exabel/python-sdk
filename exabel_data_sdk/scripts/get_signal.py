import argparse
import sys
from typing import Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.scripts.base_script import BaseScript


class GetSignal(BaseScript):
    """
    Get a signal.
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--name",
            required=True,
            type=str,
            help="The resource name of the signal, for example 'signals/ns.signalIdentifier'",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        signal = client.signal_api.get_signal(name=args.name)
        print(signal)


if __name__ == "__main__":
    GetSignal(sys.argv, "Get a signal.").run()
