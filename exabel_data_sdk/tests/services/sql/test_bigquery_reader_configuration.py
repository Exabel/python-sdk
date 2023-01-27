import argparse
import json
import unittest
from unittest import mock

from exabel_data_sdk.services.sql.bigquery_reader_configuration import (
    BigQueryReaderConfiguration,
    Credentials,
    CredentialsPath,
    Dataset,
    Project,
)
from exabel_data_sdk.services.sql.exceptions import InvalidServiceAccountCredentialsError, SqlError
from exabel_data_sdk.tests.decorators import requires_modules


@requires_modules("google.cloud.bigquery")
class TestBigQueryReaderConfiguration(unittest.TestCase):
    def setUp(self) -> None:
        self.config_with_credentials_path = BigQueryReaderConfiguration(
            project=Project("project"),
            dataset=Dataset("dataset-123"),
            credentials_path=CredentialsPath("/path/to/credentials"),
        )
        self.config_with_credentials_string = BigQueryReaderConfiguration(
            project=Project("project"),
            dataset=Dataset("dataset-123"),
            credentials=Credentials("credentials"),
        )

    def test_bigquery_reader_configuration__credentials_path_and_string_should_fail(self):
        with self.assertRaises(ValueError):
            BigQueryReaderConfiguration(
                credentials_path="/path/to/credentials",
                credentials="credentials",
            )

    def test_bigquery_reader_configuration_missing_required_arg(self):
        args = argparse.Namespace()
        with self.assertRaises(AttributeError):
            BigQueryReaderConfiguration.from_args(args)

    def test_bigquery_reader_configuration_from_all_args__credentials_path(self):
        args = argparse.Namespace(
            project="project",
            dataset="dataset-123",
            credentials_path="/path/to/credentials",
            credentials_string=None,
        )
        bigquery_reader_configuration = BigQueryReaderConfiguration.from_args(args)
        self.assertEqual(
            self.config_with_credentials_path,
            bigquery_reader_configuration,
        )

    def test_bigquery_reader_configuration_from_all_args__credentials_string(self):
        args = argparse.Namespace(
            project="project",
            dataset="dataset-123",
            credentials_path=None,
            credentials_string="credentials",
        )
        bigquery_reader_configuration = BigQueryReaderConfiguration.from_args(args)
        self.assertEqual(
            self.config_with_credentials_string,
            bigquery_reader_configuration,
        )

    def test_bigquery_reader_configuration_get_connection_minimal(self):
        self.assertEqual(
            "bigquery:///",
            BigQueryReaderConfiguration().get_connection_string(),
        )

    def test_bigquery_reader_configuration_get_connection_string(self):
        config = BigQueryReaderConfiguration(
            project="project",
            dataset="dataset-123",
            credentials_path="/path/to/credentials",
        )
        self.assertSequenceEqual(
            ("bigquery://project/dataset-123?credentials_path=%2Fpath%2Fto%2Fcredentials", {}),
            config.get_connection_string_and_kwargs(),
        )

    @mock.patch(
        "exabel_data_sdk.services.sql.bigquery_reader_configuration.ServiceAccountCredentials"
    )
    @mock.patch("exabel_data_sdk.services.sql.bigquery_reader_configuration.BigQueryClient")
    def test_bigquery_reader_configuration_get_connection_string__with_credentials_string(
        self, mock_bq_client, mock_sa_credentials
    ):
        mock_bq_client.return_value = "bq_client"
        mock_sa_credentials.from_service_account_info.return_value = "credentials"
        config = BigQueryReaderConfiguration(
            project="project",
            dataset="dataset-123",
            credentials='{"credentials": "string"}',
        )
        self.assertSequenceEqual(
            (
                "bigquery://project/dataset-123?user_supplied_client=true",
                {"connect_args": {"client": "bq_client"}},
            ),
            config.get_connection_string_and_kwargs(),
        )
        mock_sa_credentials.from_service_account_info.assert_called_once_with(
            {"credentials": "string"}
        )
        mock_bq_client.assert_called_once_with(
            credentials="credentials",
        )

    @mock.patch(
        "exabel_data_sdk.services.sql.bigquery_reader_configuration.ServiceAccountCredentials"
    )
    @mock.patch("exabel_data_sdk.services.sql.bigquery_reader_configuration.BigQueryClient")
    def test_bigquery_reader_configuration_get_connection_string__with_invalid_credentials_string(
        self, mock_bq_client, mock_sa_credentials
    ):
        mock_bq_client.return_value = "bq_client"
        config = BigQueryReaderConfiguration(
            project="project",
            dataset="dataset-123",
            credentials="invalid json",
        )
        with self.assertRaises(InvalidServiceAccountCredentialsError) as cm:
            config.get_connection_string_and_kwargs()
        self.assertIsInstance(cm.exception.__cause__, json.JSONDecodeError)
        self.assertIsInstance(cm.exception, SqlError)
        self.assertFalse(mock_sa_credentials.from_service_account_info.called)

        mock_sa_credentials.from_service_account_info.side_effect = ValueError()
        config = BigQueryReaderConfiguration(
            project="project",
            dataset="dataset-123",
            credentials='{"invalid": "credentials"}',
        )
        with self.assertRaises(InvalidServiceAccountCredentialsError):
            config.get_connection_string_and_kwargs()
        self.assertIsInstance(cm.exception, SqlError)
        mock_sa_credentials.from_service_account_info.assert_called_once_with(
            {"invalid": "credentials"}
        )
