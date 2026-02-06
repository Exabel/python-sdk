import pytest

from exabel.util.handle_missing_imports import handle_missing_imports

# ruff: noqa: F401


class TestHandleMissingImports:
    def test_handle_missing_imports(self):
        with pytest.warns(UserWarning) as cm:
            with handle_missing_imports({"exabel.might_not_exist": "library-name"}):
                import exabel.might_not_exist
        assert str(cm[0].message).startswith("Module 'exabel.might_not_exist'")

    def test_handle_missing_imports_custom_warning(self):
        with pytest.warns(UserWarning) as cm:
            with handle_missing_imports(
                {"exabel.might_not_exist": "library-name"}, warning="custom warning"
            ):
                import exabel.might_not_exist
        assert str(cm[0].message).startswith("custom warning")

    def test_handle_missing_imports_reraise(self):
        with pytest.raises(ImportError) as cm:
            with handle_missing_imports(
                {"exabel.might_not_exist": "library-name"},
                warning="custom exception",
                reraise=True,
            ):
                import exabel.might_not_exist
        assert str(cm.value).startswith("custom exception")

    def test_handle_missing_imports_should_fail(self):
        with pytest.raises(ImportError) as cm:
            with handle_missing_imports({}):
                import exabel.does_not_exist
        assert "exabel.does_not_exist" == str(cm.value.name)
