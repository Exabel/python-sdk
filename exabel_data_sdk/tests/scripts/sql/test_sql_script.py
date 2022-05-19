import argparse
import unittest
from unittest import mock

from exabel_data_sdk.scripts.sql.sql_script import SqlScript
from exabel_data_sdk.services.file_writer import FileWriter
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
    @mock.patch("exabel_data_sdk.scripts.sql.sql_script.FileWriterProvider")
    def test_sql_script_without_output_file(self, mock_provider, mock_reader):
        mock_config_class = mock.create_autospec(SqlReaderConfiguration)
        mock_config_instance = mock_config_class()
        mock_config_class.from_args.return_value = mock_config_instance
        mock_reader.return_value.read_sql_query.return_value = "the-data-frame"
        mock_writer_instance = mock.create_autospec(FileWriter)()
        mock_provider.get_file_writer.return_value = mock_writer_instance
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
        mock_reader.return_value.read_sql_query.assert_called_once_with(
            "SELECT 1 AS A",
        )
        mock_provider.get_file_writer.assert_not_called()

    @mock.patch("exabel_data_sdk.scripts.sql.sql_script.SqlReader")
    @mock.patch("exabel_data_sdk.scripts.sql.sql_script.FileWriterProvider")
    def test_sql_script_with_output_file(self, mock_provider, mock_reader):
        mock_config_class = mock.create_autospec(SqlReaderConfiguration)
        mock_config_instance = mock_config_class()
        mock_config_class.from_args.return_value = mock_config_instance
        mock_reader.return_value.read_sql_query.return_value = "the-data-frame"
        mock_writer_instance = mock.create_autospec(FileWriter)()
        mock_provider.get_file_writer.return_value = mock_writer_instance
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
        mock_reader.return_value.read_sql_query.assert_called_once_with(
            "SELECT 1 AS A",
        )
        mock_provider.get_file_writer.assert_called_once_with("output_file")
        mock_writer_instance.write_file.assert_called_once_with(
            "the-data-frame",
            "output_file",
        )
