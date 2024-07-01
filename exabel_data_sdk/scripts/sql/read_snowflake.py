import sys
from getpass import getpass
from os import path
from typing import Optional, Sequence

from exabel_data_sdk.scripts.sql.sql_script import SqlScript
from exabel_data_sdk.services.sql.snowflake_reader import SnowflakeReader
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
        group = self.parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            "--password",
            help="The password of the Snowflake user to authenticate.",
        )
        group.add_argument(
            "--key-file",
            help="File with the private key of the Snowflake user to authenticate in PEM format.",
        )
        self.parser.add_argument(
            "--passphrase",
            help="Passphrase for the key file. May be an empty string. "
            "If not provided, you will be prompted for a passphrase when using --key-file.",
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

    def read_key(self, file: str, passphrase: Optional[str]) -> bytes:
        """Read the key from given file. Use the provided passphrase to decrypt the file.
        If not passphrase is provided, promt the user to enter one. Provide an empty
        string as passphrase for unencrypted keys."""
        from cryptography.hazmat.primitives import serialization

        if not path.isfile(file):
            print(f"Key file '{file}' does not exist.")
            sys.exit(1)
        if passphrase is None:
            passphrase = getpass(f"Passphrase for '{file}': ")
        encoded = None if passphrase == "" else passphrase.encode()
        with open(file, "rb") as key:
            p_key = serialization.load_pem_private_key(key.read(), password=encoded)
        return p_key.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

    def run(self) -> None:
        args = self.parse_arguments()
        self.setup_logging()
        if args.key_file is not None:
            args.private_key = self.read_key(args.key_file, args.passphrase)
            args.key_file = None
            args.passphrase = None
        configuration = self.reader_configuration_class.from_args(args)
        reader = SnowflakeReader(configuration.get_connection_args())
        reader.read_sql_query_and_write_result(
            args.query, args.output_file, batch_size=args.batch_size
        )


if __name__ == "__main__":
    ReadSnowflake(sys.argv).run()
