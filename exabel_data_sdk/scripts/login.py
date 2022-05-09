"""Script for logging in to Auth0 in order to get an access token."""

import argparse
import sys
from typing import List

from exabel_data_sdk.client.user_login import UserLogin


def main(argv: List[str]) -> None:
    """Set up the environment and login process."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--auth0",
        default="auth.exabel.com",
        help="The domain of the Auth0 log-in page",
    )
    parser.add_argument(
        "--client-id",
        default="6OoAPIEgqz1CQokkBuwtBcYKgNiLKsMF",
        help="The Auth0 client id for the Python SDK",
    )
    parser.add_argument(
        "--backend",
        default="endpoints.exabel.com",
        help="The domain of the Exabel back-end API",
    )
    args = parser.parse_args(argv[1:])

    login = UserLogin(args.auth0, args.client_id, args.backend)
    success = login.log_in()
    if success:
        print("Successfully logged in.")
    else:
        print("Failed to log in.")


if __name__ == "__main__":
    main(sys.argv)
