import argparse
import os
import sys
from typing import Optional, Sequence

from exabel_data_sdk.client.api.export_api import ExportApi
from exabel_data_sdk.client.user_login import UserLogin
from exabel_data_sdk.scripts.command_line_script import CommandLineScript


class ExportData(CommandLineScript):
    """Script for exporting data from the Exabel API with a user-provided query string."""

    def __init__(self, argv: Sequence[str], description: str = "Export data from Exabel"):
        super().__init__(argv, description)
        self.argv = argv

    def parse_arguments(self) -> argparse.Namespace:
        """Parse the command-line input arguments."""
        parser = argparse.ArgumentParser(description="Export data")
        parser.add_argument(
            "--query",
            required=True,
            type=str,
            help="The query to execute",
        )
        parser.add_argument(
            "--filename",
            required=True,
            type=str,
            help="The filename where the exported data should be saved",
        )
        parser.add_argument(
            "--format",
            required=True,
            type=str,
            help="The format",
        )
        parser.add_argument(
            "--retries",
            type=int,
            help="The number of times to retry each request.",
            default=0,
        )
        auth_group = parser.add_mutually_exclusive_group()
        auth_group.add_argument(
            "--reauthenticate",
            action="store_true",
            help="Reauthenticate the default user, for example to login to a different tenant",
        )
        auth_group.add_argument(
            "--api-key",
            type=str,
            help="Authenticate with an API key instead of an Exabel user account",
        )
        auth_group.add_argument(
            "--user",
            type=str,
            help="The Exabel user to log in as, e.g. `my_user@enterprise.com`",
        )
        parser.add_argument(
            "--use-test-backend",
            action="store_true",
            help=argparse.SUPPRESS,
        )
        return parser.parse_args(self.argv[1:])

    @staticmethod
    def get_export_api(
        api_key: Optional[str] = None,
        reauthenticate: bool = False,
        use_test_backend: bool = False,
        user: Optional[str] = None,
        retries: int = 0,
    ) -> ExportApi:
        """Get an `ExportApi` from an API key or user authentication."""
        api_key = api_key or os.getenv("EXABEL_API_KEY")
        if api_key:
            return ExportApi.from_api_key(api_key, use_test_backend, retries=retries)
        login = UserLogin(reauthenticate, use_test_backend, user)
        headers = login.get_auth_headers()
        return ExportApi(auth_headers=headers, backend=login.backend, retries=retries)

    def run(self) -> None:
        """Download data from the Exabel API and store it to file."""
        args = self.parse_arguments()
        self.setup_logging()
        export_api = ExportData.get_export_api(
            args.api_key, args.reauthenticate, args.use_test_backend, args.user, args.retries
        )
        content = export_api.run_query_bytes(query=args.query, file_format=args.format)
        with open(args.filename, "wb") as file:
            file.write(content)


if __name__ == "__main__":
    ExportData(sys.argv).run()
