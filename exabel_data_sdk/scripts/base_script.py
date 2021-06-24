import abc
import argparse
from typing import Sequence

from exabel_data_sdk import ExabelClient


class BaseScript:
    """Base class for scripts using the Exabel Python SDK."""

    def __init__(self, argv: Sequence[str], description: str):
        self.argv = argv
        self.parser = argparse.ArgumentParser(description=description)
        self.parser.add_argument("--api-key", required=False, type=str, help="The API key to use")
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
        api_key = self.get_api_key(args)
        client = ExabelClient(host=args.exabel_api_host, api_key=api_key, use_json=args.use_json)
        self.run_script(client, args)

    def get_api_key(self, args: argparse.Namespace) -> str:
        """Extracts the API key from the arguments."""
        if not args.api_key:
            raise ValueError("API key not provided.")
        return args.api_key

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
