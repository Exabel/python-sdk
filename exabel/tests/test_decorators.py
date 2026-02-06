import sys
import unittest

from exabel.tests.decorators import requires_modules


@requires_modules("unittest")
class TestDecoratorsShouldBeRun(unittest.TestCase):
    def test_should_be_run(self):
        assert "unittest" in sys.modules


@requires_modules("unittest", "sys")
class TestDecoratorsShouldBeRunAsWell(unittest.TestCase):
    def test_should_be_run(self):
        assert {"unittest", "sys"}.issubset(sys.modules)


@requires_modules("invalid module name")
class TestDecoratorsShouldBeSkipped(unittest.TestCase):
    def test_should_be_skipped(self):
        raise AssertionError


@requires_modules("invalid module name", "unittest")
class TestDecoratorsShouldBeSkippedAsWell(unittest.TestCase):
    def test_should_be_skipped(self):
        raise AssertionError
