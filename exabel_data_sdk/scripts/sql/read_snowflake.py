import sys
from typing import Sequence

from exabel_data_sdk.scripts.sql.sql_script import SqlScript
from exabel_data_sdk.services.sql.snowflake_reader_configuration import SnowflakeReaderConfiguration


class ReadSnowflake(SqlScript):
    """Perform a query against Snowflake and optionally store the result to a file."""

    def __init__(self, argv: Sequence[str]):
        description: str = self.__doc__  # type: ignore
        super().__init__(argv, description, SnowflakeReaderConfiguration)
        self.parser.add_argument(
            "--account",
            required=True,
            help=(
                "The Snowflake account, usually on the format `<organization name>-<account name>` "
                "or `<account locator>.<region>.<cloud>`."
            ),
        )
        self.parser.add_argument(
            "--username",
            required=True,
            help="The login name of the Snowflake user to authenticate.",
        )
        self.parser.add_argument(
            "--password",
            required=True,
            help="The password of the Snowflake user to authenticate.",
        )
        self.parser.add_argument(
            "--warehouse",
            help="The warehouse to use. Required if no default is set for the user.",
        )
        self.parser.add_argument(
            "--database",
            help="The default database to use for queries. Required if schema is specified.",
        )
        self.parser.add_argument(
            "--schema",
            help="The default schema to use.",
        )
        self.parser.add_argument(
            "--role",
            help="The role to use. Required if no default is set for the user.",
        )


if __name__ == "__main__":
    ReadSnowflake(sys.argv).run()
