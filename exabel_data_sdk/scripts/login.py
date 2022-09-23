"""Script for logging in to Auth0 in order to get an access token."""

import argparse
import sys
from typing import List

from exabel_data_sdk.client.user_login import UserLogin


def main(argv: List[str]) -> None:
    """Set up the environment and login process."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--reauthenticate",
        action="store_true",
        help="Reauthenticate the user, for example to login to a different tenant",
    )
    parser.add_argument(
        "--use-test-backend",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    args = parser.parse_args(argv[1:])

    login = UserLogin(args.reauthenticate, args.use_test_backend)
    success = login.log_in()
    if success:
        print("Successfully logged in.")
    else:
        print("Failed to log in.")


if __name__ == "__main__":
    main(sys.argv)
