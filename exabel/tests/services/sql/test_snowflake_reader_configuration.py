import argparse
import unittest

import pytest

from exabel.services.sql.snowflake_reader_configuration import (
    Account,
    Database,
    Password,
    PrivateKey,
    Role,
    Schema,
    SnowflakeReaderConfiguration,
    Username,
    Warehouse,
)
from exabel.tests.decorators import requires_modules


@requires_modules("snowflake.sqlalchemy")
class TestSnowflakeReaderConfiguration(unittest.TestCase):
    def setUp(self) -> None:
        self.config = SnowflakeReaderConfiguration(
            account=Account("account"),
            user=Username("username"),
            password=Password("password"),
            private_key=PrivateKey("private_key".encode()),
            warehouse=Warehouse("warehouse"),
            database=Database("database"),
            schema=Schema("schema"),
            role=Role("role"),
        )

    def test_snowflake_reader_configuration_should_fail(self):
        with pytest.raises(ValueError):
            SnowflakeReaderConfiguration(
                account=Account("account"),
                user=Username("username"),
                password=Password("password"),
                schema=Schema("schema"),
            )

    def test_snowflake_reader_configuration_from_args(self):
        args = argparse.Namespace(
            account="account",
            username="username",
            password="password",
            private_key="private_key".encode(),
            warehouse="warehouse",
            database="database",
            schema="schema",
            role="role",
            ignored="ignored",
        )
        snowflake_reader_configuration = SnowflakeReaderConfiguration.from_args(args)
        assert self.config == snowflake_reader_configuration

    def test_snowflake_reader_configuration_get_connection_string_and_kwargs(self):
        assert (
            "snowflake://username:password@account/database/schema"
            "?login_timeout=15&role=role&warehouse=warehouse",
            {"connect_args": {"private_key": "private_key".encode()}},
        ) == self.config.get_connection_string_and_kwargs()
        assert (
            "snowflake://username:password@account/?login_timeout=15",
            {},
        ) == SnowflakeReaderConfiguration(
            account=Account("account"), user=Username("username"), password=Password("password")
        ).get_connection_string_and_kwargs()

    def test_snowflake_reader_configuration_get_connection_args(self):
        assert {
            "account": "account",
            "user": "username",
            "password": "password",
            "private_key": "private_key".encode(),
            "warehouse": "warehouse",
            "database": "database",
            "schema": "schema",
            "role": "role",
            "login_timeout": 15,
        } == self.config.get_connection_args()
