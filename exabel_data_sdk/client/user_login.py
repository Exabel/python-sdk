from __future__ import annotations

import base64
import errno
import json
import os
import threading
import uuid
import webbrowser
from collections import defaultdict
from collections.abc import Mapping as MappingABC
from dataclasses import dataclass
from datetime import datetime
from functools import partial
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Dict, Mapping, MutableMapping, Optional
from urllib.parse import parse_qs, quote_plus, urlparse

import requests

DEFAULT_TOKEN_FILE_PATH = "~/.exabel"
DEFAULT_USER = "__default__"
GET_CURRENT_USER_URL_TEMPLATE = "https://{host}/v1/users/current"


@dataclass(frozen=True)
class RefreshTokens:
    """Holds mappings from Exabel API hosts to mappings of users to refresh tokens."""

    tokens: Mapping[str, Mapping[str, str]]

    def __post_init__(self) -> None:
        """Validate the refresh token file."""
        if not isinstance(self.tokens, MappingABC):
            raise ValueError(f"tokens must be a mapping, got: {self.tokens}")
        for host, users in self.tokens.items():
            if not isinstance(host, str):
                raise ValueError(f"host must be a string, got {host} in tokens {self.tokens}")
            if not isinstance(users, MappingABC):
                raise ValueError(f"users must be a mapping, got {users} in host: {host}")
            for user, refresh_token in users.items():
                if not isinstance(user, str):
                    raise ValueError(f"user must be a string, got {user} in users: {users}")
                if not isinstance(refresh_token, str):
                    raise ValueError(
                        f"refresh_token must be a string, got {refresh_token} in user: {user}"
                    )

    def get_refresh_token(self, host: str, user: str) -> str:
        """Get the refresh token for a given user and host."""
        return self.tokens.get(host, {}).get(user, "")

    def merge_with(self, other: RefreshTokens) -> RefreshTokens:
        """
        Merge two RefreshTokens objects, values in the other RefreshTokens overwrite values in
        this one.
        """
        tokens: MutableMapping[str, MutableMapping[str, str]] = defaultdict(dict)
        hosts = set(self.tokens.keys()).union(other.tokens.keys())
        for host in hosts:
            tokens[host].update(self.tokens.get(host, {}))
            tokens[host].update(other.tokens.get(host, {}))
        return RefreshTokens(tokens)

    def to_json(self) -> str:
        """Convert to JSON."""
        return json.dumps(self.tokens, indent=4)

    @staticmethod
    def from_json(json_string: str) -> RefreshTokens:
        """Create from JSON."""
        return RefreshTokens(json.loads(json_string))

    @staticmethod
    def from_host_user_token(host: str, user: str, token: str) -> RefreshTokens:
        """Create from a host, user and token."""
        return RefreshTokens({host: {user: token}})

    @staticmethod
    def from_host_user(host: str, user: str) -> RefreshTokens:
        """Create from a host and a user with the default empty token."""
        return RefreshTokens.from_host_user_token(host, user, "")


class UserLogin:
    """
    Class for interactive programs that need to log in to the API as a user.

    Stores refresh tokens in '~/.exabel'. If a token is missing or expired, or
    `reauthenticate` is set, the script starts a local web server and opens the user’s
    web browser to log in to Auth0 to get a refresh token.

    The argument `use_test_backend` is only for internal engineering use at Exabel.
    Customers and partners should leave it at the default value.

    To login with a specific user, e.g. `my_user@enterprise.com`, use the `user` argument. This is
    useful if you have multiple users in your organization and want to switch between them without
    having to reauthorize for each login.

    Get access token (to be used as “Bearer” authentication):
    login.log_in()
    login.access_token
    """

    def __init__(
        self,
        reauthenticate: bool = False,
        use_test_backend: bool = False,
        user: Optional[str] = None,
    ):
        self.auth0 = "auth-test.exabel.com" if use_test_backend else "auth.exabel.com"
        self.client_id = (
            "VcQvJBLqhsTvKh1KMu6kXDCLWXumlubj"
            if use_test_backend
            else "6OoAPIEgqz1CQokkBuwtBcYKgNiLKsMF"
        )
        self.backend = "endpoints-test.exabel.com" if use_test_backend else "endpoints.exabel.com"
        self.authorization_code = ""
        self.access_token = ""
        self.redirect_uri = ""
        self.state = ""
        self.expires = datetime.utcnow()
        self.callback_received = threading.Event()
        self.reauthenticate = reauthenticate
        self.user = user or DEFAULT_USER
        self.tokens = RefreshTokens({})

    @property
    def refresh_token(self) -> str:
        """The refresh token for the set user and host."""
        return self.tokens.get_refresh_token(host=self.backend, user=self.user)

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
        filename = os.path.expanduser(DEFAULT_TOKEN_FILE_PATH)
        if os.path.isfile(filename):
            with open(filename, encoding="utf-8") as file:
                content = file.read()
                try:
                    self.tokens = self.tokens.merge_with(RefreshTokens.from_json(content))
                except json.decoder.JSONDecodeError:
                    # If the file is not valid JSON, it is an old refresh token. We convert it to
                    # the new JSON format after reading.
                    self.tokens = self.tokens.merge_with(
                        RefreshTokens.from_host_user_token(self.backend, self.user, content)
                    )
                    self.write_refresh_token()

    def write_refresh_token(self) -> None:
        """Write the refresh token to the user’s home directory."""
        filename = os.path.expanduser(DEFAULT_TOKEN_FILE_PATH)
        with open(filename, "w", encoding="utf-8") as file:
            file.write(self.tokens.to_json())

    def get_access_token(self) -> bool:
        """Get an access token from Auth0 using a refresh token."""
        if self.refresh_token == "" or self.reauthenticate:
            self.reauthenticate = False
            return False

        url = f"https://{self.auth0}/oauth/token"
        data = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "refresh_token": self.refresh_token,
        }
        response = requests.post(url, data=data, timeout=10)
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
        response = requests.post(url, data=data, timeout=10)
        if response.status_code == 200:
            parsed = response.json()
            self.access_token = parsed["access_token"]
            self.tokens = self.tokens.merge_with(
                RefreshTokens.from_host_user_token(self.backend, self.user, parsed["refresh_token"])
            )
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
        url = (
            f"https://{self.auth0}/authorize"
            f"?audience=https://{self.backend}/"
            "&scope=offline_access"
            "&response_type=code"
            f"&client_id={self.client_id}"
            f"&redirect_uri={self.redirect_uri}"
            f"&state={self.state}"
            # Auth0 remembers which user you logged in as last time. This parameter forces Auth0 to
            # show the login screen again.
            "&prompt=login"
        )
        if self.user != DEFAULT_USER:
            url += f"&login_hint={quote_plus(self.user)}"
        webbrowser.open(url)
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
            self.verify_logged_in_user()
        return logged_in

    def verify_logged_in_user(self) -> None:
        """Verify the logged in user is the same as the one provided to the instance."""
        if self.user != DEFAULT_USER:
            parsed = requests.get(
                get_current_user_url(host=self.backend), headers=self.auth_headers, timeout=10
            ).json()
            logged_in_user = parsed["email"]
            if self.user != logged_in_user:
                # Delete the refresh token for the wrong user to force reauthentication on next
                # login attempt.
                self.tokens = self.tokens.merge_with(
                    RefreshTokens.from_host_user(self.backend, self.user)
                )
                self.write_refresh_token()
                raise ValueError(
                    f"Logged in as {logged_in_user}, but expected to be logged in as {self.user}."
                )

    @property
    def is_expired(self) -> bool:
        """Whether the current access token has expired."""
        return self.expires < datetime.utcnow()

    @property
    def auth_headers(self) -> Dict[str, str]:
        """The authentication headers for HTTPS requests to the Exabel API."""
        return {"Authorization": f"Bearer {self.access_token}"}

    def get_auth_headers(self) -> Dict[str, str]:
        """Log in and get the authentication headers for HTTPS requests to the Exabel API."""
        if not self.log_in():
            raise Exception("Failed to log in.")
        return self.auth_headers


class TokenHandler(BaseHTTPRequestHandler):
    """HTTP reponse handler for Auth0 callbacks."""

    def __init__(self, login: UserLogin, *args: Any, **kwargs: Any):
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


def get_current_user_url(host: str) -> str:
    """Get the URL to get the current user."""
    return GET_CURRENT_USER_URL_TEMPLATE.format(host=host)
