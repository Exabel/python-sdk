import unittest
import unittest.mock

import pandas as pd
import pandas.testing as pdt

from exabel_data_sdk.services.sql.sql_reader import SqlReader
from exabel_data_sdk.tests.decorators import requires_modules
from exabel_data_sdk.util.handle_missing_imports import handle_missing_imports

with handle_missing_imports():
    from sqlalchemy.engine import Engine


@requires_modules("sqlalchemy")
class TestSqlReader(unittest.TestCase):
    def setUp(self) -> None:
        self.reader = SqlReader("sqlite:///:memory:")

    def test_engine(self):
        self.assertIsInstance(self.reader.engine, Engine)
        self.assertEqual("sqlite:///:memory:", str(self.reader.engine.url))

    def test_read_sql_query(self):
        df = self.reader.read_sql_query("SELECT 1 as a UNION SELECT 2")
        pdt.assert_frame_equal(
            pd.DataFrame({"a": [1, 2]}),
            df,
        )
