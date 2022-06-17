import unittest
from unittest import mock

import pandas as pd
import pandas.testing as pdt

from exabel_data_sdk.services.file_writer import FileWriter
from exabel_data_sdk.services.sql.sql_reader import SqlReader
from exabel_data_sdk.services.sql.sql_reader_configuration import ConnectionString
from exabel_data_sdk.tests.decorators import requires_modules
from exabel_data_sdk.util.handle_missing_imports import handle_missing_imports

with handle_missing_imports():
    from sqlalchemy.engine import Engine


@requires_modules("sqlalchemy")
class TestSqlReader(unittest.TestCase):
    class _MockFileWriter(FileWriter):
        @staticmethod
        def write_file(df: pd.DataFrame, filepath: str) -> None:
            raise NotImplementedError()

    def setUp(self) -> None:
        self.reader = SqlReader(ConnectionString("sqlite:///:memory:"))

    def test_engine(self):
        self.assertIsInstance(self.reader.engine, Engine)
        self.assertEqual("sqlite:///:memory:", str(self.reader.engine.url))

    def test_read_sql_query(self):
        df = self.reader.read_sql_query("SELECT 1 as a UNION SELECT 2")
        pdt.assert_frame_equal(
            pd.DataFrame({"a": [1, 2]}),
            df,
        )

    @mock.patch("exabel_data_sdk.services.sql.sql_reader.FileWriterProvider")
    def test_read_sql_query_and_write_result_without_output_file(self, mock_provider):
        self.reader.read_sql_query_and_write_result("SELECT 1 as a UNION SELECT 2")
        mock_provider.get_file_writer.assert_not_called()

    @mock.patch("exabel_data_sdk.services.sql.sql_reader.FileWriterProvider")
    def test_read_sql_query_and_write_result_with_output_file(self, mock_provider):
        mock_writer = mock.create_autospec(self._MockFileWriter)
        mock_provider.get_file_writer.return_value = mock_writer
        self.reader.read_sql_query_and_write_result("SELECT 1 as a UNION SELECT 2", "output-file")
        mock_provider.get_file_writer.assert_called_once_with("output-file")
        call_args = mock_writer.write_file.call_args[0]
        pdt.assert_frame_equal(
            pd.DataFrame({"a": [1, 2]}),
            call_args[0],
        )
        self.assertEqual(
            "output-file",
            call_args[1],
        )
