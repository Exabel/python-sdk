import argparse
from dataclasses import dataclass, fields
from typing import Mapping, NewType, Optional

from exabel_data_sdk.services.sql.sql_reader_configuration import (
    ConnectionString,
    SqlReaderConfiguration,
)
from exabel_data_sdk.util.handle_missing_imports import handle_missing_imports

with handle_missing_imports():
    from snowflake.sqlalchemy import URL


Account = NewType("Account", str)
Username = NewType("Username", str)
Password = NewType("Password", str)
Warehouse = NewType("Warehouse", str)
Database = NewType("Database", str)
Schema = NewType("Schema", str)
Role = NewType("Role", str)


@dataclass
class SnowflakeReaderConfiguration(SqlReaderConfiguration):
    """SQL configuration for Snowflake."""

    account: Account
    user: Username
    password: Password
    warehouse: Optional[Warehouse] = None
    database: Optional[Database] = None
    schema: Optional[Schema] = None
    role: Optional[Role] = None

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

    def get_connection_string(self) -> ConnectionString:
        """Return the connection string."""
        return URL(**self._get_url_kwargs())

    def _get_url_kwargs(self) -> Mapping[str, str]:
        """Return the keyword arguments."""
        return {
            field.name: getattr(self, field.name)
            for field in fields(self)
            if getattr(self, field.name)
        }
