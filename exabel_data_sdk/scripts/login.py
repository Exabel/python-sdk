"""Script for logging in to Auth0 in order to get an access token."""

import argparse
import base64
import errno
import json
import os
import sys
import threading
import uuid
import webbrowser
from datetime import datetime
from functools import partial
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, List
from urllib.parse import parse_qs, urlparse

import requests


class CliLogin:
    """
    Class for command-line interfaces that need to log in to the API as a user.

    Stores a refresh token in '~/.exabel'. If the token is missing or expired, the script starts a
    local web server and opens the user’s web browser to log in to Auth0 to get a refresh token.

    Get access token (to be used as “Bearer” authentication):
    login.log_in()
    login.access_token
    """

    def __init__(
        self,
        auth0: str,
        client_id: str,
        backend: str,
    ):
        self.auth0 = auth0
        self.client_id = client_id
        self.backend = backend
        self.authorization_code = ""
        self.access_token = ""
        self.redirect_uri = ""
        self.refresh_token = ""
        self.state = ""
        self.expires = datetime.utcnow()
        self.callback_received = threading.Event()

    def start_http_server(self) -> HTTPServer:
        """Start a local web server."""
        httpd = None
        for port in range(8090, 8100):
            try:
                server_address = ("localhost", port)
                handler = partial(TokenHandler, self)
                httpd = HTTPServer(server_address, handler)
            except OSError as error:
                if error.errno != errno.EADDRINUSE:
                    raise error
        if httpd is None:
            raise Exception("Cannot start a local HTTP server to receive the login token.")

        thread = threading.Thread(target=httpd.serve_forever)
        thread.setDaemon(True)
        thread.start()
        return httpd

    def read_refresh_token(self) -> None:
        """Read the refresh token from the user’s home directory."""
        filename = os.path.expanduser("~/.exabel")
        if os.path.isfile(filename):
            with open(filename, encoding="utf-8") as file:
                self.refresh_token = file.read()

    def write_refresh_token(self) -> None:
        """Write the refresh token to the user’s home directory."""
        filename = os.path.expanduser("~/.exabel")
        with open(filename, "w", encoding="utf-8") as file:
            file.write(self.refresh_token)

    def get_access_token(self) -> bool:
        """Get an access token from Auth0 using a refresh token."""
        if self.refresh_token == "":
            return False

        url = f"https://{self.auth0}/oauth/token"
        data = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "refresh_token": self.refresh_token,
        }
        response = requests.post(url, data=data)
        if response.status_code == 200:
            parsed = response.json()
            self.access_token = parsed["access_token"]
            return True
        return False

    def get_tokens(self) -> bool:
        """Get refresh and access tokens from Auth0 using an authorization code."""
        if self.authorization_code == "":
            return False

        url = f"https://{self.auth0}/oauth/token"
        data = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "code": self.authorization_code,
            "redirect_uri": self.redirect_uri,
        }
        response = requests.post(url, data=data)
        if response.status_code == 200:
            parsed = response.json()
            self.access_token = parsed["access_token"]
            self.refresh_token = parsed["refresh_token"]
            self.write_refresh_token()
            return True
        return False

    def get_authorization_code(self) -> None:
        """
        Get an authorization code by opening a browser to Auth0 login.
        """
        self.state = uuid.uuid4().hex
        httpd = self.start_http_server()
        self.redirect_uri = f"http://localhost:{httpd.server_port}/callback"
        webbrowser.open(
            f"https://{self.auth0}/authorize"
            f"?audience=https://{self.backend}/"
            "&scope=offline_access"
            "&response_type=code"
            f"&client_id={self.client_id}"
            f"&redirect_uri={self.redirect_uri}"
            f"&state={self.state}"
        )
        self.callback_received.wait()
        httpd.shutdown()

    def log_in(self) -> bool:
        """
        Get an access token, asking the user to log in if necessary.

        Returns whether the user successfully logged in.
        """
        self.read_refresh_token()
        if not self.get_access_token():
            # None or expired refresh token
            self.get_authorization_code()
            self.get_tokens()
        logged_in = self.access_token is not None
        if logged_in:
            payload = self.access_token.split(".")[1]
            # base64.urlsafe_b64decode requires padding, but will truncate any unnecessary ones
            parsed = json.loads(base64.urlsafe_b64decode(payload + "==="))
            self.expires = datetime.utcfromtimestamp(parsed["exp"])
        return logged_in

    @property
    def is_expired(self) -> bool:
        """Whether the current access token has expired."""
        return self.expires < datetime.utcnow()


class TokenHandler(BaseHTTPRequestHandler):
    """HTTP reponse handler for Auth0 callbacks."""

    def __init__(self, login: CliLogin, *args: Any, **kwargs: Any):
        self.login = login
        # BaseHTTPRequestHandler calls do_GET **inside** __init__,
        # so we have to call super().__init__ after setting attributes.
        super().__init__(*args, **kwargs)

    def log_message(self, format: str, *args: Any) -> None:  # pylint: disable=redefined-builtin
        return

    def do_GET(self) -> None:  # pylint: disable=invalid-name
        """Handle a GET request."""
        req = urlparse(self.path)
        if req.path == "/callback":
            query = parse_qs(req.query)
            if "state" in query:
                if query["state"][0] != self.login.state:
                    self.send_error(500)
            if "code" in query:
                self.login.authorization_code = query["code"][0]

                self.send_response(200)
                self.send_header("content-type", "text/plain")
                self.end_headers()
                self.wfile.write(
                    bytes(
                        "The Python SDK is now logged in. Please close this window.",
                        "utf-8",
                    )
                )
            else:
                self.send_error(400)
            self.login.callback_received.set()
            return
        self.send_response(404)


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

    login = CliLogin(args.auth0, args.client_id, args.backend)
    success = login.log_in()
    if success:
        print("Successfully logged in.")
    else:
        print("Failed to log in.")


if __name__ == "__main__":
    main(sys.argv)
