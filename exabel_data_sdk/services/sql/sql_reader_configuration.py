import abc
import argparse
from typing import Any, Mapping, NamedTuple, NewType

ConnectionString = NewType("ConnectionString", str)


class EngineArgs(NamedTuple):
    """Arguments for creating a SQLAlchemy engine."""

    connection_string: ConnectionString
    kwargs: Mapping[str, Any]


class SqlReaderConfiguration(abc.ABC):
    """Base class for SQL reader configurations."""

    @classmethod
    @abc.abstractmethod
    def from_args(cls, args: argparse.Namespace) -> "SqlReaderConfiguration":
        """Construct a SQL reader configuration from the given command-line arguments."""

    @abc.abstractmethod
    def get_connection_string(self) -> ConnectionString:
        """Return the connection string."""

    def get_connection_string_and_kwargs(self) -> EngineArgs:
        """Return the connection string and additional key-word arguments."""
        return EngineArgs(self.get_connection_string(), {})
