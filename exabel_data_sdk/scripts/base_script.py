import abc
import argparse
import os
import urllib.parse
from typing import Optional, Sequence, Tuple

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.scripts.command_line_script import CommandLineScript


class BaseScript(CommandLineScript, abc.ABC):
    """Base class for scripts using the Exabel Python SDK."""

    def __init__(
        self,
        argv: Sequence[str],
        description: str,
    ):
        super().__init__(argv, description)
        api_key = os.getenv("EXABEL_API_KEY")
        access_token = os.getenv("EXABEL_ACCESS_TOKEN")
        group = self.parser.add_mutually_exclusive_group(required=not api_key and not access_token)
        group.add_argument(
            "--api-key",
            type=str,
            help="The API key to use. Can also be specified in the EXABEL_API_KEY environment "
            "variable.",
        )
        group.add_argument(
            "--access-token",
            type=str,
            help="The access token to use. Can also be specified in the EXABEL_ACCESS_TOKEN "
            "environment variable.",
        )
        group.add_argument("--gcp-project-number", type=str, help=argparse.SUPPRESS)
        self.parser.add_argument(
            "--exabel-data-api-host",
            required=False,
            default="data.api.exabel.com",
            help="Data API host on format 'hostname[:port]'",
        )
        self.parser.add_argument(
            "--exabel-analytics-api-host",
            required=False,
            default="analytics.api.exabel.com",
            help="Analytics API host on format 'hostname[:port]'",
        )
        self.parser.add_argument(
            "--exabel-management-api-host",
            required=False,
            default="management.api.exabel.com",
            help="Management API host on format 'hostname[:port]'",
        )

    def run(self) -> None:
        args = self.parse_arguments()
        self.setup_logging()
        api_key = args.api_key
        access_token = args.access_token
        # Command line argument takes precedence over environment variables.
        if not api_key and not access_token and not args.gcp_project_number:
            api_key = os.getenv("EXABEL_API_KEY")
            access_token = os.getenv("EXABEL_ACCESS_TOKEN")
            if api_key and access_token:
                raise ValueError("Only one of EXABEL_API_KEY and EXABEL_ACCESS_TOKEN can be set.")
            if not api_key and not access_token:
                raise ValueError(
                    "No authentication information. Provide an API key or access token."
                )

        extra_headers = []
        if args.gcp_project_number:
            api_key = "NO_KEY"
            extra_headers = [
                ("x-endpoint-api-consumer-type", "PROJECT"),
                ("x-endpoint-api-consumer-number", args.gcp_project_number),
            ]
        data_api_host, data_api_port = self.parse_host_and_port(args.exabel_data_api_host)
        analytics_api_host, analytics_api_port = self.parse_host_and_port(
            args.exabel_analytics_api_host
        )
        management_api_host, management_api_port = self.parse_host_and_port(
            args.exabel_management_api_host
        )
        client = ExabelClient(
            data_api_host=data_api_host,
            data_api_port=data_api_port,
            analytics_api_host=analytics_api_host,
            analytics_api_port=analytics_api_port,
            management_api_host=management_api_host,
            management_api_port=management_api_port,
            api_key=api_key,
            access_token=access_token,
            extra_headers=extra_headers,
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

    @staticmethod
    def parse_host_and_port(host_and_port: str) -> Tuple[str, Optional[int]]:
        """
        Parses a string on format 'hostname[:port]'.
        """
        result = urllib.parse.urlsplit("//" + host_and_port)
        return str(result.hostname), result.port
