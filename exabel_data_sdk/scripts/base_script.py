import abc
import argparse
import os
from typing import Callable, Sequence

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.scripts.command_line_script import CommandLineScript


class BaseScript(CommandLineScript, abc.ABC):
    """Base class for scripts using the Exabel Python SDK."""

    def __init__(
        self,
        argv: Sequence[str],
        description: str,
        api_key_retriever: Callable[[argparse.Namespace], str] = None,
    ):
        super().__init__(argv, description)
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
            "--exabel-data-api-host",
            required=False,
            default="data.api.exabel.com",
            help="Data API host",
        )
        self.parser.add_argument(
            "--exabel-analytics-api-host",
            required=False,
            default="analytics.api.exabel.com",
            help="Analytics API host",
        )
        self.parser.add_argument(
            "--exabel-management-api-host",
            required=False,
            default="management.api.exabel.com",
            help="Management API host",
        )
        self.parser.add_argument(
            "--use-json",
            required=False,
            action="store_true",
            default=False,
            help="If set, send requests as JSON over HTTP rather than gRPC",
        )

    def run(self) -> None:
        args = self.parse_arguments()
        api_key = (
            self.api_key_retriever(args) if self.api_key_retriever is not None else args.api_key
        )
        client = ExabelClient(
            data_api_host=args.exabel_data_api_host,
            analytics_api_host=args.exabel_analytics_api_host,
            management_api_host=args.exabel_management_api_host,
            api_key=api_key,
            use_json=args.use_json,
        )
        self.run_script(client, args)

    @abc.abstractmethod
    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        """
        Runs the script.

        Args:
            client: Exabel API client.
            args:   Parsed command line arguments.
        """
