import argparse
import unittest

from exabel_data_sdk.services.sql.bigquery_reader_configuration import (
    BigQueryReaderConfiguration,
    CredentialsPath,
    Dataset,
    Project,
)


class TestBigQueryReaderConfiguration(unittest.TestCase):
    def setUp(self) -> None:
        self.config = BigQueryReaderConfiguration(
            project=Project("project"),
            dataset=Dataset("dataset-123"),
            credentials_path=CredentialsPath("/path/to/credentials"),
        )

    def test_bigquery_reader_configuration_missing_required_arg(self):
        args = argparse.Namespace()
        with self.assertRaises(AttributeError):
            BigQueryReaderConfiguration.from_args(args)

    def test_bigquery_reader_configuration_from_all_args(self):
        args = argparse.Namespace(
            project="project",
            dataset="dataset-123",
            credentials_path="/path/to/credentials",
        )
        bigquery_reader_configuration = BigQueryReaderConfiguration.from_args(args)
        self.assertEqual(
            self.config,
            bigquery_reader_configuration,
        )

    def test_bigquery_reader_configuration_get_connection_minimal(self):
        self.assertEqual(
            "bigquery:///",
            BigQueryReaderConfiguration().get_connection_string(),
        )

    def test_bigquery_reader_configuration_get_connection_string(self):
        self.assertEqual(
            "bigquery://project/dataset-123" "?credentials_path=%2Fpath%2Fto%2Fcredentials",
            self.config.get_connection_string(),
        )
        self.assertEqual(
            "bigquery://project/dataset-123" "?credentials_path=%2Fpath%2Fto%2Fcredentials",
            BigQueryReaderConfiguration(
                project="project",
                dataset="dataset-123",
                credentials_path="/path/to/credentials",
            ).get_connection_string(),
        )
