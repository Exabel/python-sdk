from __future__ import annotations

import logging
import unittest
from dataclasses import dataclass
from typing import Sequence
from unittest import mock

import pandas as pd

from exabel_data_sdk.client.api.bulk_import import _bulk_insert_with_retry
from exabel_data_sdk.client.api.bulk_insert import _get_backoff
from exabel_data_sdk.client.api.data_classes.request_error import ErrorType, RequestError
from exabel_data_sdk.client.api.resource_creation_result import (
    ResourceCreationResult,
    ResourceCreationResults,
    ResourceCreationStatus,
)

logger = logging.getLogger(__name__)


class TestEntityApi(unittest.TestCase):
    def test_get_backoff(self):
        self.assertEqual(1.0, _get_backoff(0))
        self.assertEqual(2.0, _get_backoff(1))
        self.assertEqual(4.0, _get_backoff(2))
        self.assertEqual(8.0, _get_backoff(3))
        self.assertEqual(16.0, _get_backoff(4))
        self.assertEqual(32.0, _get_backoff(5))
        self.assertEqual(60.0, _get_backoff(6))


@dataclass(frozen=True)
class SeriesRaisingError:
    """Class for representing a series that will fail on upload."""

    name: str
    error_type: ErrorType

    @property
    def error(self) -> RequestError:
        """The error that should be raised when uploading this series."""
        return RequestError(error_type=self.error_type)

    @property
    def series(self) -> pd.Series:
        """Return the series that should be uploaded."""
        mock_series = mock.Mock()
        mock_series.name = self.name
        return mock_series

    @staticmethod
    def from_error_type(error_type: ErrorType) -> SeriesRaisingError:
        """Return a SeriesRaisingError with the given error type."""
        return SeriesRaisingError(name=error_type.name, error_type=error_type)

    @staticmethod
    def from_name(name: str) -> SeriesRaisingError:
        """Return a SeriesRaisingError with the given name."""
        return SeriesRaisingError(name=name, error_type=getattr(ErrorType, name))


class TestTimeSeriesApi(unittest.TestCase):
    @mock.patch("exabel_data_sdk.client.api.bulk_import._bulk_insert")
    def test_bulk_insert_with_retry(self, bulk_insert_mock):
        series_raising_errors = [
            SeriesRaisingError.from_error_type(error_type) for error_type in ErrorType
        ]
        insert_func = mock.Mock()

        def bulk_insert_side_effect(
            results: ResourceCreationResults[pd.Series],
            resources: Sequence[pd.Series],
            *_,
            **__,
        ) -> None:
            for series in resources:
                error = SeriesRaisingError.from_name(series.name).error
                status = (
                    ResourceCreationStatus.EXISTS
                    if error.error_type == ErrorType.ALREADY_EXISTS
                    else ResourceCreationStatus.FAILED
                )
                results.add(ResourceCreationResult(status, series, error))

        bulk_insert_mock.side_effect = bulk_insert_side_effect

        _bulk_insert_with_retry(
            [series.series for series in series_raising_errors],
            ResourceCreationResults(len(series_raising_errors)),
            insert_func,
            retries=1,
            threads=1,
        )
        self.assertEqual(
            2, bulk_insert_mock.call_count, "Expecting two calls in total to _bulk_insert."
        )
        self.assertEqual(
            len(series_raising_errors),
            len(bulk_insert_mock.call_args_list[0][0][1]),
            "Expecting all series to be attempted uploaded in the first call.",
        )
        self.assertEqual(
            len([e for e in series_raising_errors if e.error_type.retryable()]),
            len(bulk_insert_mock.call_args_list[1][0][1]),
            "Expecting only retryable series to be attempted uploaded in the second call.",
        )
