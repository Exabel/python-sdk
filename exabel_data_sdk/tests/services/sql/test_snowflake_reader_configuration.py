import argparse
import unittest

from exabel_data_sdk.services.sql.snowflake_reader_configuration import (
    Account,
    Database,
    Password,
    Role,
    Schema,
    SnowflakeReaderConfiguration,
    Username,
    Warehouse,
)
from exabel_data_sdk.tests.decorators import requires_modules


@requires_modules("snowflake.sqlalchemy")
class TestSnowflakeReaderConfiguration(unittest.TestCase):
    def setUp(self) -> None:
        self.config = SnowflakeReaderConfiguration(
            account=Account("account"),
            user=Username("username"),
            password=Password("password"),
            warehouse=Warehouse("warehouse"),
            database=Database("database"),
            schema=Schema("schema"),
            role=Role("role"),
        )

    def test_snowflake_reader_configuration_should_fail(self):
        with self.assertRaises(ValueError):
            SnowflakeReaderConfiguration(
                account="account",
                user="username",
                password="password",
                schema="schema",
            )

    def test_snowflake_reader_configuration_from_args(self):
        args = argparse.Namespace(
            account="account",
            username="username",
            password="password",
            warehouse="warehouse",
            database="database",
            schema="schema",
            role="role",
            ignored="ignored",
        )
        snowflake_reader_configuration = SnowflakeReaderConfiguration.from_args(args)
        self.assertEqual(
            self.config,
            snowflake_reader_configuration,
        )

    def test_snowflake_reader_configuration_get_connection_string(self):
        self.assertEqual(
            "snowflake://username:password@account/database/schema"
            "?role=role&warehouse=warehouse",
            self.config.get_connection_string(),
        )
        self.assertEqual(
            "snowflake://username:password@account/",
            SnowflakeReaderConfiguration(
                account="account",
                user="username",
                password="password",
            ).get_connection_string(),
        )
