import argparse
import unittest

from exabel_data_sdk.scripts.sql.read_snowflake import ReadSnowflake
from exabel_data_sdk.tests.decorators import requires_modules


@requires_modules("snowflake.connector")
class TestReadSnowflake(unittest.TestCase):
    def test_read_snowflake_parse_args_password(self):
        args = [
            "read_snowflake",
            "--account",
            "account",
            "--username",
            "username",
            "--password",
            "password",
            "--warehouse",
            "warehouse",
            "--database",
            "database",
            "--schema",
            "schema",
            "--role",
            "role",
            "--query",
            "SELECT 1 AS A",
            "--output-file",
            "output_file",
            "--batch-size",
            "100",
        ]
        script = ReadSnowflake(args)
        self.assertEqual(
            argparse.Namespace(
                account="account",
                username="username",
                password="password",
                key_file=None,
                passphrase=None,
                warehouse="warehouse",
                database="database",
                schema="schema",
                role="role",
                query="SELECT 1 AS A",
                output_file="output_file",
                batch_size=100,
            ),
            script.parse_arguments(),
        )

    def test_read_snowflake_parse_args_key_file(self):
        args = [
            "read_snowflake",
            "--account",
            "account",
            "--username",
            "username",
            "--key-file",
            "mykey.p8",
            "--passphrase",
            "passphrase",
            "--warehouse",
            "warehouse",
            "--database",
            "database",
            "--schema",
            "schema",
            "--role",
            "role",
            "--query",
            "SELECT 1 AS A",
            "--output-file",
            "output_file",
            "--batch-size",
            "100",
        ]
        script = ReadSnowflake(args)
        self.assertEqual(
            argparse.Namespace(
                account="account",
                username="username",
                password=None,
                key_file="mykey.p8",
                passphrase="passphrase",
                warehouse="warehouse",
                database="database",
                schema="schema",
                role="role",
                query="SELECT 1 AS A",
                output_file="output_file",
                batch_size=100,
            ),
            script.parse_arguments(),
        )
