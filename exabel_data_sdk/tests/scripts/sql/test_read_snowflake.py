import argparse
import unittest

from exabel_data_sdk.scripts.sql.read_snowflake import ReadSnowflake
from exabel_data_sdk.tests.decorators import requires_modules


@requires_modules("snowflake.sqlalchemy", "sqlalchemy")
class TestReadSnowflake(unittest.TestCase):
    def test_read_snowflake_parse_args(self):
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
        ]
        script = ReadSnowflake(args)
        self.assertEqual(
            argparse.Namespace(
                account="account",
                username="username",
                password="password",
                warehouse="warehouse",
                database="database",
                schema="schema",
                role="role",
                query="SELECT 1 AS A",
                output_file="output_file",
            ),
            script.parse_arguments(),
        )
