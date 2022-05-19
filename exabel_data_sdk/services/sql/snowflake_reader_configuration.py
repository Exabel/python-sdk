import argparse
from dataclasses import dataclass, fields
from typing import Mapping, Optional

from exabel_data_sdk.services.sql.sql_reader_configuration import SqlReaderConfiguration
from exabel_data_sdk.util.handle_missing_imports import handle_missing_imports

with handle_missing_imports():
    from snowflake.sqlalchemy import URL


@dataclass
class SnowflakeReaderConfiguration(SqlReaderConfiguration):
    """SQL configuration for Snowflake."""

    account: str
    user: str
    password: str
    warehouse: Optional[str] = None
    database: Optional[str] = None
    schema: Optional[str] = None
    role: Optional[str] = None

    def __post_init__(self) -> None:
        if self.schema and not self.database:
            raise ValueError("Cannot specify schema without specifying database")

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> "SnowflakeReaderConfiguration":
        return cls(
            account=args.account,
            user=args.username,
            password=args.password,
            warehouse=args.warehouse,
            database=args.database,
            schema=args.schema,
            role=args.role,
        )

    def get_connection_string(self) -> str:
        """Return the connection string."""
        return URL(**self._get_url_kwargs())

    def _get_url_kwargs(self) -> Mapping[str, str]:
        """Return the keyword arguments."""
        return {
            field.name: getattr(self, field.name)
            for field in fields(self)
            if getattr(self, field.name)
        }
