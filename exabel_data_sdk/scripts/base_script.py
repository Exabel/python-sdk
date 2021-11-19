import abc
import argparse
import os
from typing import Callable, Sequence

from exabel_data_sdk import ExabelClient


class BaseScript(abc.ABC):
    """Base class for scripts using the Exabel Python SDK."""

    def __init__(
        self,
        argv: Sequence[str],
        description: str,
        api_key_retriever: Callable[[argparse.Namespace], str] = None,
    ):
        self.argv = argv
        self.parser = argparse.ArgumentParser(description=description)
        self.api_key_retriever = api_key_retriever
        if api_key_retriever is None:
            api_key = os.getenv("EXABEL_API_KEY")
            help_text = "The API key to use"
            if api_key:
                help_text += " (found in EXABEL_API_KEY environment variable)"
            else:
                help_text += ". Can also be specified in the EXABEL_API_KEY environment variable."
            self.parser.add_argument("--api-key", required=not api_key, type=str, help=help_text)
        self.parser.add_argument(
            "--exabel-api-host",
            required=False,
            default="data.api.exabel.com",
            help="Data API host",
        )
        self.parser.add_argument(
            "--use-json",
            required=False,
            action="store_true",
            default=False,
            help="If set, send requests as JSON over HTTP rather than gRPC",
        )

    def run(self) -> None:
        """Runs the script."""
        args = self.parse_arguments()
        api_key = (
            self.api_key_retriever(args) if self.api_key_retriever is not None else args.api_key
        )
        client = ExabelClient(host=args.exabel_api_host, api_key=api_key, use_json=args.use_json)
        self.run_script(client, args)

    def parse_arguments(self) -> argparse.Namespace:
        """Parse arguments input"""
        return self.parser.parse_args(self.argv[1:])

    @abc.abstractmethod
    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        """
        Runs the script.

        Args:
            client: Exabel API client.
            args:   Parsed command line arguments.
        """
