import sys
from typing import Sequence

from exabel_data_sdk.scripts.sql.sql_script import SqlScript
from exabel_data_sdk.services.sql.athena_reader_configuration import AthenaReaderConfiguration


class ReadAthena(SqlScript):
    """Perform a query against Athena and optionally store the result to a file."""

    def __init__(self, argv: Sequence[str]):
        description: str = self.__doc__  # type: ignore
        super().__init__(argv, description, AthenaReaderConfiguration)
        self.parser.add_argument(
            "--region",
            help="The name of the AWS region to run the query in.",
            required=True,
        )
        self.parser.add_argument(
            "--s3-staging-dir",
            help=(
                "The S3 bucket and path to use for staging the query results. E.g. "
                "'s3://my-bucket/path/to/dir/'."
            ),
            required=True,
        )
        self.parser.add_argument(
            "--workgroup",
            help="The name of the Athena workgroup to use.",
        )
        self.parser.add_argument(
            "--catalog",
            help="The catalog (data source) to use. Defaults PyAthena's default: 'awsdatacatalog'.",
        )
        self.parser.add_argument(
            "--schema",
            help="The schema (database) to use. Defaults PyAthena's default: 'default'.",
        )
        self.parser.add_argument(
            "--aws-access-key-id",
            help="The AWS access key ID to use. If set, --aws-secret-access-key must also be set.",
        )
        self.parser.add_argument(
            "--aws-secret-access-key",
            help="The AWS secret access key to use. If set, --aws-access-key-id must also be set.",
        )
        self.parser.add_argument(
            "--profile",
            help=(
                "The AWS config profile to use. Must be present in the shared credentials file "
                "located at '~/.aws/credentials'. If set, --aws-access-key-id and "
                "--aws-secret-access-key cannot be set."
            ),
        )


if __name__ == "__main__":
    ReadAthena(sys.argv).run()
