import abc
import argparse
from typing import NewType

ConnectionString = NewType("ConnectionString", str)


class SqlReaderConfiguration(abc.ABC):
    """Base class for SQL reader configurations."""

    @classmethod
    @abc.abstractmethod
    def from_args(cls, args: argparse.Namespace) -> "SqlReaderConfiguration":
        """Construct a SQL reader configuration from the given command-line arguments."""

    @abc.abstractmethod
    def get_connection_string(self) -> ConnectionString:
        """Return the connection string."""
