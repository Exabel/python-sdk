import tempfile

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from exabel.services.excel_writer import ExcelWriter
from exabel.tests.decorators import requires_modules


@requires_modules("openpyxl")
class TestExcelWriter:
    def test_excel_writer(self):
        test_df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        with tempfile.NamedTemporaryFile(suffix=".xlsx") as file:
            ExcelWriter.write_file(test_df, file.name)
            actual_df = pd.read_excel(file.name, engine="openpyxl")
        assert_frame_equal(test_df, actual_df)

    def test_excel_writer__iterable_should_fail(self):
        with tempfile.NamedTemporaryFile(suffix=".xlsx") as file:
            with pytest.raises(NotImplementedError):
                ExcelWriter.write_file([], file.name)
