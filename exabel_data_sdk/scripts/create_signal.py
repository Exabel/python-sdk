import argparse
import sys
from typing import Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.signal import Signal
from exabel_data_sdk.scripts.base_script import BaseScript


class CreateSignal(BaseScript):
    """
    Creates a new signal.
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--name",
            required=True,
            type=str,
            help="The resource name of the signal, for example 'signals/ns.signalIdentifier'",
        )
        self.parser.add_argument(
            "--display-name", required=True, type=str, help="The display name of the signal"
        )
        self.parser.add_argument(
            "--description",
            required=False,
            type=str,
            default="",
            help="One or more paragraphs of text description",
        )
        self.parser.add_argument(
            "--create-library-signal",
            required=False,
            type=bool,
            default=False,
            help="Set to true to create a library signal",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        signal = client.signal_api.create_signal(
            Signal(
                name=args.name,
                display_name=args.display_name,
                description=args.description,
            ),
            create_library_signal=args.create_library_signal,
        )
        print("Successfully created signal:")
        print(signal)


if __name__ == "__main__":
    CreateSignal(sys.argv, "Create a new signal.").run()
