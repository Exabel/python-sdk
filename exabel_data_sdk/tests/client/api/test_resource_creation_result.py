import unittest
from unittest import mock

import pandas as pd

from exabel_data_sdk.client.api.data_classes.entity import Entity
from exabel_data_sdk.client.api.data_classes.relationship import Relationship
from exabel_data_sdk.client.api.resource_creation_result import (
    ResourceCreationResult,
    ResourceCreationResults,
    ResourceCreationStatus,
    get_resource_name,
)

# pylint: disable=protected-access


class TestResourceCreationResult(unittest.TestCase):
    def test_get_resource_name(self):
        entity = mock.Mock(Entity)
        entity.name = "entity_name"
        relationship = mock.Mock(Relationship)
        relationship.relationship_type = "relationship_type"
        relationship.from_entity = "from_entity"
        relationship.to_entity = "to_entity"
        time_series = mock.Mock(pd.Series)
        time_series.name = "time_series_name"
        self.assertEqual(get_resource_name(entity), "entity_name")
        self.assertEqual(get_resource_name(relationship), "relationship_type/from_entity/to_entity")
        self.assertEqual(get_resource_name(time_series), "time_series_name")

    def test_resource_creation_result(self):
        entity = mock.Mock(Entity)
        entity.name = "entity_name"
        result = ResourceCreationResult(status=ResourceCreationStatus.FAILED, resource=entity)
        self.assertEqual(result.status, ResourceCreationStatus.FAILED)
        self.assertEqual(result.resource, entity)
        self.assertEqual(result.resource_name, "entity_name")

    def test_resource_creation_result__success_should_not_store_resource(self):
        entity = mock.Mock(Entity)
        entity.name = "entity_name"
        for status in ResourceCreationStatus:
            if status != ResourceCreationStatus.FAILED:
                result = ResourceCreationResult(status=status, resource=entity)
                self.assertEqual(result.status, status)
                self.assertIsNone(result.resource)
                self.assertEqual(result.resource_name, "entity_name")

    def test_get_progress_checkpoints(self):
        total = 10
        checkpoints = 5
        expected = {2, 4, 6, 8, 10}
        actual = ResourceCreationResults._get_progress_checkpoints(total, checkpoints)
        self.assertEqual(checkpoints, len(actual))
        self.assertEqual(expected, actual)

    def test_get_progress_checkpoints__total_is_zero(self):
        total = 0
        checkpoints = 10
        expected = {0}
        actual = ResourceCreationResults._get_progress_checkpoints(total, checkpoints)
        self.assertEqual(1, len(actual))
        self.assertEqual(expected, actual)

    def test_update(self):
        total = 10
        results = ResourceCreationResults(
            total_count=total, print_status=False, abort_threshold=0.3
        )
        resource = mock.Mock(Entity)
        resource.name = "entity_name"
        for _ in range(total):
            results.add(
                ResourceCreationResult(status=ResourceCreationStatus.CREATED, resource=resource)
            )
        other_total = 5
        other = ResourceCreationResults(total_count=other_total, print_status=False)
        for _ in range(other_total):
            other.add(
                ResourceCreationResult(status=ResourceCreationStatus.CREATED, resource=resource)
            )
        results.update(other)
        self.assertEqual(total + other_total, results.total_count)
        self.assertEqual(total + other_total, len(results.results))
        self.assertEqual(0.3, results.abort_threshold)
