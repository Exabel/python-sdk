import sys
import unittest

from exabel_data_sdk.tests.decorators import requires_modules


@requires_modules("unittest")
class TestDecoratorsShouldBeRun(unittest.TestCase):
    def test_should_be_run(self):
        self.assertTrue("unittest" in sys.modules)


@requires_modules("unittest", "sys")
class TestDecoratorsShouldBeRunAsWell(unittest.TestCase):
    def test_should_be_run(self):
        self.assertTrue({"unittest", "sys"}.issubset(sys.modules))


@requires_modules("invalid module name")
class TestDecoratorsShouldBeSkipped(unittest.TestCase):
    def test_should_be_skipped(self):
        raise AssertionError


@requires_modules("invalid module name", "unittest")
class TestDecoratorsShouldBeSkippedAsWell(unittest.TestCase):
    def test_should_be_skipped(self):
        raise AssertionError
