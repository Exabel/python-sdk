import unittest

from exabel_data_sdk.client.api.data_classes.entity import Entity


class TestEntity(unittest.TestCase):
    def test_proto_conversion(self):
        entity = Entity(
            name="entityTypes/country/entities/no",
            display_name="Norway",
            description="Country Norway",
            properties={"a": False, "b": 3.5, "c": "c_value"},
        )
        self.assertEqual(entity, Entity.from_proto(entity.to_proto()))
