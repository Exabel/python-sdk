import tempfile
import unittest

import pandas as pd
from pandas.testing import assert_frame_equal

from exabel_data_sdk.services.excel_writer import ExcelWriter
from exabel_data_sdk.tests.decorators import requires_modules


@requires_modules("openpyxl")
class TestExcelWriter(unittest.TestCase):
    def test_excel_writer(self):
        test_df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        with tempfile.NamedTemporaryFile(suffix=".xlsx") as file:
            ExcelWriter.write_file(test_df, file.name)
            actual_df = pd.read_excel(file.name)
        assert_frame_equal(test_df, actual_df)
