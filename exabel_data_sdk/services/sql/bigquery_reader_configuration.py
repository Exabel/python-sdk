import argparse
import json
import urllib.parse
from dataclasses import dataclass
from typing import MutableMapping, NewType, Optional

from exabel_data_sdk.services.sql.exceptions import InvalidServiceAccountCredentialsError
from exabel_data_sdk.services.sql.sql_reader_configuration import (
    ConnectionString,
    EngineArgs,
    SqlReaderConfiguration,
)
from exabel_data_sdk.util.handle_missing_imports import handle_missing_imports

with handle_missing_imports():
    from google.cloud.bigquery import Client as BigQueryClient
with handle_missing_imports():
    from google.oauth2.service_account import Credentials as ServiceAccountCredentials

Project = NewType("Project", str)
Dataset = NewType("Dataset", str)
CredentialsPath = NewType("CredentialsPath", str)
Credentials = NewType("Credentials", str)


@dataclass
class BigQueryReaderConfiguration(SqlReaderConfiguration):
    """SQL configuration for BigQuery."""

    project: Optional[Project] = None
    credentials_path: Optional[CredentialsPath] = None
    dataset: Optional[Dataset] = None
    credentials: Optional[Credentials] = None

    def __post_init__(self) -> None:
        if self.credentials_path and self.credentials:
            raise ValueError("Only one of credentials_path and credentials can be set")

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> "BigQueryReaderConfiguration":
        return cls(
            project=args.project,
            dataset=args.dataset,
            credentials_path=args.credentials_path,
            credentials=args.credentials_string,
        )

    def get_connection_string(self) -> ConnectionString:
        """Return the connection string."""
        params: MutableMapping[str, str] = {}
        if self.credentials_path is not None:
            params["credentials_path"] = self.credentials_path
        if self.credentials is not None:
            params["user_supplied_client"] = "true"
        connection_string = f"bigquery://{self.project or ''}/{self.dataset or ''}" + (
            f"?{urllib.parse.urlencode(params)}" if len(params) > 0 else ""
        )
        return ConnectionString(connection_string)

    def get_connection_string_and_kwargs(self) -> EngineArgs:
        if self.credentials is not None:
            try:
                credentials = ServiceAccountCredentials.from_service_account_info(
                    json.loads(self.credentials)
                )
            except ValueError as e:
                raise InvalidServiceAccountCredentialsError(
                    "Failed to parse service account credentials. Please check that the credentials"
                    " are valid."
                ) from e
            client = BigQueryClient(credentials=credentials)
            return EngineArgs(self.get_connection_string(), {"connect_args": {"client": client}})
        return super().get_connection_string_and_kwargs()
