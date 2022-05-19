import unittest

from exabel_data_sdk.util.handle_missing_imports import handle_missing_imports


class TestHandleMissingImports(unittest.TestCase):
    def test_handle_missing_imports(self):
        with self.assertWarns(UserWarning) as cm:
            with handle_missing_imports({"exabel_data_sdk.might_not_exist": "library-name"}):
                import exabel_data_sdk.might_not_exist  # pylint: disable=unused-import
        self.assertTrue(str(cm.warning).startswith("Module 'exabel_data_sdk.might_not_exist'"))

    def test_handle_missing_imports_should_fail(self):
        with self.assertRaises(ImportError) as cm:
            with handle_missing_imports({}):
                import exabel_data_sdk.does_not_exist  # pylint: disable=unused-import
        self.assertEqual("exabel_data_sdk.does_not_exist", str(cm.exception.name))
