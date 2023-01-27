import sys
from typing import Sequence

from exabel_data_sdk.scripts.sql.sql_script import SqlScript
from exabel_data_sdk.services.sql.bigquery_reader_configuration import BigQueryReaderConfiguration


class ReadBigQuery(SqlScript):
    """Perform a query against BigQuery and optionally store the result to a file."""

    def __init__(self, argv: Sequence[str]):
        description: str = self.__doc__  # type: ignore
        super().__init__(argv, description, BigQueryReaderConfiguration)
        self.parser.add_argument(
            "--project",
            help="The Google Cloud Project where the Google BigQuery instance to query is located.",
        )
        self.parser.add_argument(
            "--dataset",
            help=(
                "The Google BigQuery dataset to query. Can optionally be specified in the query "
                "as [dataset.]table."
            ),
        )
        credentials_group = self.parser.add_mutually_exclusive_group()
        credentials_group.add_argument(
            "--credentials-path",
            help=(
                "Path and filename to the json file that will be used to authenticate the service "
                "account to use for the querying against Google BigQuery. Credentials can be "
                "downloaded using a command like this: 'gcloud iam service-accounts keys create "
                "<key-file> --iam-account=<service-account>@<project>.iam.gserviceaccount.com'. "
                "If no credentials are specified, the authentication will be attempted using the "
                "Google Cloud SDK. A service account can also be authenticated using the Google "
                "Cloud SDK with the command 'gcloud auth activate-service-account "
                "<service-account>@<project>.iam.gserviceaccount.com --key-file=<key-file>'"
            ),
        )
        credentials_group.add_argument(
            "--credentials-string",
            help=(
                "Same as --credentials-path, but the credentials are passed as a string instead "
                "of a path to a file."
            ),
        )


if __name__ == "__main__":
    ReadBigQuery(sys.argv).run()
