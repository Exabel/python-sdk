import argparse
import unittest

from exabel_data_sdk.services.sql.sql_reader_configuration import EngineArgs, SqlReaderConfiguration


class MockSqlReaderConfiguration(SqlReaderConfiguration):
    """Mock implementation of SqlReaderConfiguration."""

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> "SqlReaderConfiguration":
        raise NotImplementedError

    def get_connection_string(self):
        return "connection-string"


class TestBigQueryReaderConfiguration(unittest.TestCase):
    def test_get_connection_string_and_kwargs(self):
        engine_args = MockSqlReaderConfiguration().get_connection_string_and_kwargs()
        self.assertSequenceEqual(
            ("connection-string", {}),
            engine_args,
        )
        self.assertEqual(
            EngineArgs("connection-string", {}),
            engine_args,
        )
