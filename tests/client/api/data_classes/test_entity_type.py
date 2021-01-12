import unittest

from exabel_data_sdk.client.api.data_classes.entity_type import EntityType
from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import EntityType as ProtoEntityType


class TestEntityType(unittest.TestCase):
    def test_from_proto(self):
        proto_entity_type = ProtoEntityType(
            name="entityTypes/country",
            display_name="Country entity type",
            description="description",
            read_only=True,
        )

        entity_type = EntityType(
            name="entityTypes/country",
            display_name="Country entity type",
            description="description",
            read_only=True,
        )
        self.assertEqual(entity_type, EntityType.from_proto(proto_entity_type))
