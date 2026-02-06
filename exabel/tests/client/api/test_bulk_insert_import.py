from __future__ import annotations

import logging
from collections import Counter
from typing import Mapping, MutableSequence, Sequence
from unittest import mock

import pandas as pd
import pytest

from exabel.client.api.bulk_import import bulk_import
from exabel.client.api.bulk_insert import BulkInsertFailedError, _get_backoff, bulk_insert
from exabel.client.api.data_classes.request_error import (
    ErrorType,
    PreconditionFailure,
    RequestError,
    Violation,
)
from exabel.client.api.data_classes.time_series import TimeSeries, TimeSeriesResourceName
from exabel.client.api.resource_creation_result import ResourceCreationStatus

logger = logging.getLogger(__name__)


def _get_ts_resources_map() -> Mapping[str, pd.Series]:
    resource_map = {
        "entityTypes/valid/entities/valid/signals/valid": mock.create_autospec(pd.Series),
        "entityTypes/__INVALID__/entities/valid/signals/valid": mock.create_autospec(pd.Series),
        "entityTypes/valid/entities/__INVALID__/signals/valid": mock.create_autospec(pd.Series),
        "entityTypes/valid/entities/valid/signals/__INVALID__": mock.create_autospec(pd.Series),
    }
    for name, series in resource_map.items():
        series.name = name
        series.__bool__.side_effect = ValueError("The truth value of a Series is ambiguous")
    return resource_map


class TestBulkInsert:
    def test_get_backoff(self):
        assert 1.0 == _get_backoff(0)
        assert 2.0 == _get_backoff(1)
        assert 4.0 == _get_backoff(2)
        assert 8.0 == _get_backoff(3)
        assert 16.0 == _get_backoff(4)
        assert 32.0 == _get_backoff(5)
        assert 64.0 == _get_backoff(6)
        assert 128.0 == _get_backoff(7)
        assert 256.0 == _get_backoff(8)
        assert 512.0 == _get_backoff(9)
        assert 600.0 == _get_backoff(10)
        assert 600.0 == _get_backoff(11)

    @staticmethod
    def _insert_func_side_effect(resource: pd.Series, *_, **__) -> ResourceCreationStatus:
        if "__INVALID__" in resource.name:
            raise RequestError(
                ErrorType.NOT_FOUND,
                None,
                None,
            )
        return ResourceCreationStatus.UPSERTED

    def test_bulk_insert(self):
        resource_map = _get_ts_resources_map()
        resources = list(resource_map.values())
        insert_func = mock.Mock()
        insert_func.side_effect = self._insert_func_side_effect
        with mock.patch("exabel.client.api.bulk_import._get_backoff", return_value=0):
            results = bulk_insert(
                resources,
                insert_func,
            )
        assert 4 == insert_func.call_count
        assert 4 == results.total_count

        actual_statuses = [result.status for result in results.results]
        expected_statuses = [ResourceCreationStatus.FAILED] * 3 + [ResourceCreationStatus.UPSERTED]
        assert Counter(expected_statuses) == Counter(actual_statuses)
        actual_failed_resources = [
            result.resource
            for result in results.results
            if result.status == ResourceCreationStatus.FAILED
        ]
        expected_failed_resources = resources[1:]
        assert Counter(expected_failed_resources) == Counter(actual_failed_resources)

    def test_bulk_insert_with_invalid_proto_data_points_should_fail(self):
        insert_func = TimeSeries._series_to_time_series_points
        series = [
            pd.Series(
                [1.01, 1.1, "not_numeric", 1.3],
                index=pd.date_range("2020-08-01", "2020-08-04"),
                name=f"ts_name_{i}",
            )
            for i in range(40)
        ]

        with pytest.raises(BulkInsertFailedError):
            bulk_insert(series, insert_func, retries=0, threads=1)
        with pytest.raises(BulkInsertFailedError):
            bulk_insert(series, insert_func, retries=0, threads=4)


class TestBulkImport:
    @staticmethod
    def _import_func_side_effect(
        resources: Sequence[pd.Series], *_, **__
    ) -> Sequence[ResourceCreationStatus]:
        violations: MutableSequence[Violation] = []
        for resource in resources:
            entity_name = TimeSeriesResourceName.from_string(resource.name).entity_name
            if "__INVALID__" in entity_name:
                violations.append(Violation("NOT_FOUND", entity_name, "Entity not found"))
        if not violations:
            for resource in resources:
                signal_name = TimeSeriesResourceName.from_string(resource.name).signal_name
                if "__INVALID__" in signal_name:
                    violations.append(Violation("NOT_FOUND", signal_name, "Signal not found"))
        if violations:
            raise RequestError(
                ErrorType.NOT_FOUND,
                None,
                PreconditionFailure(violations),
            )
        return [ResourceCreationStatus.UPSERTED] * len(resources)

    def test_bulk_import(self):
        resource_map = _get_ts_resources_map()
        resources = list(resource_map.values())
        import_func = mock.Mock()
        import_func.side_effect = self._import_func_side_effect
        with mock.patch("exabel.client.api.bulk_import._get_backoff", return_value=0):
            results = bulk_import(
                resources,
                import_func,
            )
        assert 3 == import_func.call_count
        assert 4 == len(import_func.call_args_list[0][0][0])
        assert 2 == len(import_func.call_args_list[1][0][0])
        assert 1 == len(import_func.call_args_list[2][0][0])

        assert 4 == results.total_count
        actual_statuses = [result.status for result in results.results]
        expected_statuses = [ResourceCreationStatus.FAILED] * 3 + [ResourceCreationStatus.UPSERTED]
        assert Counter(expected_statuses) == Counter(actual_statuses)
        actual_failed_resources = [
            result.resource
            for result in results.results
            if result.status == ResourceCreationStatus.FAILED
        ]
        expected_failed_resources = resources[1:]
        assert Counter(expected_failed_resources) == Counter(actual_failed_resources)

    def test_bulk_import_with_invalid_proto_data_points_should_fail(self):
        def import_func(resources: Sequence[pd.Series]) -> None:
            for resource in resources:
                TimeSeries._series_to_time_series_points(resource)

        no_data_points = 4000
        series = [
            pd.Series(
                [0, 1, "not_numeric", 2] * (no_data_points // 4),
                index=pd.date_range("2010-08-01", freq="D", periods=no_data_points),
                name=f"ts_name_{i}",
            )
            for i in range(300)
        ]

        with pytest.raises(BulkInsertFailedError):
            bulk_import(series, import_func, retries=0, threads=1)
        with pytest.raises(BulkInsertFailedError):
            bulk_import(series, import_func, retries=0, threads=4)

    def test_bulk_import_empty_resources(self):
        import_func = mock.Mock()
        result = bulk_import([], import_func)
        assert 0 == result.total_count
        import_func.assert_called_once_with([])
