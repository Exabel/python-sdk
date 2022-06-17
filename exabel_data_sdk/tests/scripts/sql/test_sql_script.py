import argparse
import unittest
from unittest import mock

from exabel_data_sdk.scripts.sql.sql_script import SqlScript
from exabel_data_sdk.services.sql.sql_reader_configuration import SqlReaderConfiguration
from exabel_data_sdk.tests.decorators import requires_modules


@requires_modules("sqlalchemy")
class TestSqlScript(unittest.TestCase):
    class SqlScriptImpl(SqlScript):
        """Mock implementation"""

    def setUp(self) -> None:
        self.common_args = [
            "sql_script",
            "--query",
            "SELECT 1 AS A",
        ]

    @mock.patch("exabel_data_sdk.scripts.sql.sql_script.SqlReader")
    def test_sql_script_without_output_file(self, mock_reader):
        mock_config_class = mock.create_autospec(SqlReaderConfiguration)
        mock_config_instance = mock_config_class()
        mock_config_class.from_args.return_value = mock_config_instance
        mock_reader.return_value.read_sql_query_and_write_result.return_value = None
        script = self.SqlScriptImpl(self.common_args, "sql_script", mock_config_class)
        script.run()
        mock_config_class.from_args.assert_called_once_with(
            argparse.Namespace(
                query="SELECT 1 AS A",
                output_file=None,
            )
        )
        mock_reader.assert_called_once_with(
            mock_config_instance.get_connection_string.return_value,
        )
        mock_reader.return_value.read_sql_query_and_write_result.assert_called_once_with(
            "SELECT 1 AS A", None
        )

    @mock.patch("exabel_data_sdk.scripts.sql.sql_script.SqlReader")
    def test_sql_script_with_output_file(self, mock_reader):
        mock_config_class = mock.create_autospec(SqlReaderConfiguration)
        mock_config_instance = mock_config_class()
        mock_config_class.from_args.return_value = mock_config_instance
        mock_reader.return_value.read_sql_query_and_write_result.return_value = None
        script = self.SqlScriptImpl(
            self.common_args + ["--output-file", "output_file"], "sql_script", mock_config_class
        )
        script.run()
        mock_config_class.from_args.assert_called_once_with(
            argparse.Namespace(
                query="SELECT 1 AS A",
                output_file="output_file",
            )
        )
        mock_reader.assert_called_once_with(
            mock_config_instance.get_connection_string.return_value,
        )
        mock_reader.return_value.read_sql_query_and_write_result.assert_called_once_with(
            "SELECT 1 AS A",
            "output_file",
        )
