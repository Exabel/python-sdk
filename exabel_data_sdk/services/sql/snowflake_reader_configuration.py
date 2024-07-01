import argparse
from dataclasses import asdict, dataclass
from typing import NewType, Optional

from exabel_data_sdk.services.sql.sql_reader_configuration import (
    ConnectionString,
    EngineArgs,
    SqlReaderConfiguration,
)
from exabel_data_sdk.util.handle_missing_imports import handle_missing_imports

with handle_missing_imports():
    from snowflake.sqlalchemy import URL


Account = NewType("Account", str)
Username = NewType("Username", str)
Password = NewType("Password", str)
PrivateKey = NewType("PrivateKey", bytes)
Warehouse = NewType("Warehouse", str)
Database = NewType("Database", str)
Schema = NewType("Schema", str)
Role = NewType("Role", str)
LoginTimeout = NewType("LoginTimeout", int)


@dataclass
class SnowflakeReaderConfiguration(SqlReaderConfiguration):
    """SQL configuration for Snowflake."""

    account: Account
    user: Username
    password: Optional[Password] = None
    private_key: Optional[PrivateKey] = None
    warehouse: Optional[Warehouse] = None
    database: Optional[Database] = None
    schema: Optional[Schema] = None
    role: Optional[Role] = None
    login_timeout: LoginTimeout = LoginTimeout(15)

    def __post_init__(self) -> None:
        if self.schema and not self.database:
            raise ValueError("Cannot specify schema without specifying database")

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> "SnowflakeReaderConfiguration":
        return cls(
            account=args.account,
            user=args.username,
            password=args.password,
            private_key=args.private_key,
            warehouse=args.warehouse,
            database=args.database,
            schema=args.schema,
            role=args.role,
        )

    def get_connection_string_and_kwargs(self) -> EngineArgs:
        """Return the connection string and additional key-word arguments."""
        if self.private_key is not None:
            return EngineArgs(
                self.get_connection_string(), {"connect_args": {"private_key": self.private_key}}
            )
        return EngineArgs(self.get_connection_string(), {})

    def get_connection_string(self) -> ConnectionString:
        """Return the connection string."""
        return URL(
            **{k: v for k, v in asdict(self).items() if v is not None and k != "private_key"}
        )
