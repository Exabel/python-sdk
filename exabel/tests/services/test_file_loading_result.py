import unittest
from unittest import mock

import pytest

from exabel.client.api.resource_creation_result import ResourceCreationResults
from exabel.services.file_loading_result import (
    EntityMappingResult,
    FileLoadingResult,
    TimeSeriesFileLoadingResult,
)


class TestFileLoadingResult(unittest.TestCase):
    def test_update_result(self):
        results = mock.create_autospec(ResourceCreationResults)
        result = FileLoadingResult(results)
        other_results = mock.create_autospec(ResourceCreationResults)
        other = FileLoadingResult(other_results)
        result.update(other)
        results.update.assert_called_once_with(other_results)
        assert result.results == results
        assert list(result.warnings) == []
        assert not result.aborted

    def test_update_result__empty_self_results(self):
        result = FileLoadingResult()
        other_results = mock.create_autospec(ResourceCreationResults)
        other = FileLoadingResult(other_results)
        result.update(other)
        assert result.results == other_results
        assert list(result.warnings) == []
        assert not result.aborted

    def test_update_result__aborted(self):
        results = mock.create_autospec(ResourceCreationResults)
        result = FileLoadingResult(results)
        other_results = mock.create_autospec(ResourceCreationResults)
        other = FileLoadingResult(other_results)
        other.aborted = True
        result.update(other)
        results.update.assert_called_once_with(other_results)
        assert result.results == results
        assert list(result.warnings) == []
        assert result.aborted

    def test_update_result__warnings(self):
        results = mock.create_autospec(ResourceCreationResults)
        result = FileLoadingResult(results)
        result.warnings = ["warning"]
        other_results = mock.create_autospec(ResourceCreationResults)
        other = FileLoadingResult(other_results)
        other.warnings = ["other_warning"]
        result.update(other)
        results.update.assert_called_once_with(other_results)
        assert result.results == results
        assert list(result.warnings) == ["warning", "other_warning"]
        assert not result.aborted

    def test_update_result__empty(self):
        result = FileLoadingResult()
        other = FileLoadingResult()
        result.update(other)
        assert result.results is None
        assert list(result.warnings) == []
        assert not result.aborted

    def test_update_time_series_result__should_fail(self):
        entity_mapping_result = mock.create_autospec(EntityMappingResult)
        result = TimeSeriesFileLoadingResult(
            entity_mapping_result=entity_mapping_result, created_data_signals=[]
        )
        other = mock.create_autospec(TimeSeriesFileLoadingResult)
        with pytest.raises(NotImplementedError):
            result.update(other)
