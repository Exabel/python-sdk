import argparse
import sys
from time import time
from typing import Sequence

import requests

from exabel_data_sdk.scripts.login import CliLogin


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
        login = CliLogin(args.auth0, args.client_id, args.backend)
        login.log_in()
        headers = {"Authorization": f"Bearer {login.access_token}"}
        data = {"format": args.format, "query": args.query}
        url = f"https://{args.backend}/v1/export/file"
        start_time = time()
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            with open(args.filename, "wb") as file:
                file.write(response.content)
        else:
            error_message = response.content.decode()
            if error_message.startswith('"') and error_message.endswith('"'):
                error_message = error_message[1:-1]
            print(f"{response.status_code}: {error_message}")
        spent_time = time() - start_time
        print(f"Query completed in {int(spent_time)} seconds")


if __name__ == "__main__":
    ExportData(sys.argv).run()
