from argparse import ArgumentTypeError

import pytest

from exabel.scripts.csv_script import abort_threshold


class TestCsvScript:
    def test_abort_threshold_argument(self):
        assert 0.0 == abort_threshold("0")
        assert 0.5 == abort_threshold("0.5")
        assert 1.0 == abort_threshold("1")
        with pytest.raises(ArgumentTypeError):
            abort_threshold("1.1")
        with pytest.raises(ArgumentTypeError):
            abort_threshold("-0.1")
        with pytest.raises(ArgumentTypeError):
            abort_threshold("foo")
