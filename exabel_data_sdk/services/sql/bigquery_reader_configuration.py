import argparse
import urllib.parse
from dataclasses import dataclass
from typing import MutableMapping, NewType, Optional

from exabel_data_sdk.services.sql.sql_reader_configuration import (
    ConnectionString,
    SqlReaderConfiguration,
)

Project = NewType("Project", str)
Dataset = NewType("Dataset", str)
CredentialsPath = NewType("CredentialsPath", str)


@dataclass
class BigQueryReaderConfiguration(SqlReaderConfiguration):
    """SQL configuration for BigQuery."""

    project: Optional[Project] = None
    credentials_path: Optional[CredentialsPath] = None
    dataset: Optional[Dataset] = None

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> "BigQueryReaderConfiguration":
        return cls(
            project=args.project,
            dataset=args.dataset,
            credentials_path=args.credentials_path,
        )

    def get_connection_string(self) -> ConnectionString:
        """Return the connection string."""
        params: MutableMapping[str, str] = {}
        if self.credentials_path is not None:
            params["credentials_path"] = self.credentials_path
        connection_string = f"bigquery://{self.project or ''}/{self.dataset or ''}" + (
            f"?{urllib.parse.urlencode(params)}" if len(params) > 0 else ""
        )
        return ConnectionString(connection_string)
