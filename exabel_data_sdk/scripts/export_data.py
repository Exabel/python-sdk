import argparse
import sys
from typing import Sequence

from exabel_data_sdk.client.api.export_api import ExportApi
from exabel_data_sdk.client.user_login import UserLogin


class ExportData:
    """Script for exporting data from the Exabel API."""

    def __init__(self, argv: Sequence[str]):
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
            "--reauthenticate",
            action="store_true",
            help="Reauthenticate the user, for example to login to a different tenant",
        )
        parser.add_argument(
            "--backend",
            required=False,
            type=str,
            default="endpoints.exabel.com",
            help=argparse.SUPPRESS,
        )
        parser.add_argument(
            "--auth0",
            default="auth.exabel.com",
            help=argparse.SUPPRESS,
        )
        parser.add_argument(
            "--client-id",
            default="6OoAPIEgqz1CQokkBuwtBcYKgNiLKsMF",
            help=argparse.SUPPRESS,
        )
        return parser.parse_args(self.argv[1:])

    def run(self) -> None:
        """Download data from the Exabel API and store it to file."""
        args = self.parse_arguments()
        login = UserLogin(args.auth0, args.client_id, args.backend, args.reauthenticate)
        headers = login.get_auth_headers()
        export_api = ExportApi(headers)
        content = export_api.run_query_bytes(query=args.query, file_format=args.format)
        with open(args.filename, "wb") as file:
            file.write(content)


if __name__ == "__main__":
    ExportData(sys.argv).run()
