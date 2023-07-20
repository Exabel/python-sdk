"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
Copyright (c) 2019-2022 Exabel AS. All rights reserved."""
import builtins
import google.protobuf.descriptor
import google.protobuf.message
import google.protobuf.struct_pb2
import sys
if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions
DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class EntityType(google.protobuf.message.Message):
    """An entity type resource in the Data API."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NAME_FIELD_NUMBER: builtins.int
    DISPLAY_NAME_FIELD_NUMBER: builtins.int
    DESCRIPTION_FIELD_NUMBER: builtins.int
    READ_ONLY_FIELD_NUMBER: builtins.int
    IS_ASSOCIATIVE_FIELD_NUMBER: builtins.int
    name: builtins.str
    'Unique resource name of the entity type, e.g. `entityTypes/entityTypeIdentifier` or\n    `entityTypes/namespace.entityTypeIdentifier`. The namespace must be empty (being global) or\n    a namespace accessible to the customer.\n    The entity type identifier must match the regex `\\w[\\w-]{0,63}`.\n    '
    display_name: builtins.str
    'Used when showing the entity type in the Exabel app. Required when creating an entity type.'
    description: builtins.str
    'Used when showing the entity type in the Exabel app.'
    read_only: builtins.bool
    'Global entity types and those from data sets that you subscribe to will be read-only.'
    is_associative: builtins.bool
    'Associative entity types connect multiple entity types - e.g. `company_occupation` to connect\n    `company` and `occupation` entity types. These are typically used to hold time series data\n    that is defined by the combination of 2 or more entities.\n    '

    def __init__(self, *, name: builtins.str | None=..., display_name: builtins.str | None=..., description: builtins.str | None=..., read_only: builtins.bool | None=..., is_associative: builtins.bool | None=...) -> None:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['description', b'description', 'display_name', b'display_name', 'is_associative', b'is_associative', 'name', b'name', 'read_only', b'read_only']) -> None:
        ...
global___EntityType = EntityType

@typing_extensions.final
class Entity(google.protobuf.message.Message):
    """An entity resource in the Data API. All entities have one entity type as its parent."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NAME_FIELD_NUMBER: builtins.int
    DISPLAY_NAME_FIELD_NUMBER: builtins.int
    DESCRIPTION_FIELD_NUMBER: builtins.int
    READ_ONLY_FIELD_NUMBER: builtins.int
    PROPERTIES_FIELD_NUMBER: builtins.int
    name: builtins.str
    'Unique resource name of the entity,\n    e.g. `entityTypes/entityTypeIdentifier/entities/entityIdentifier` or\n    `entityTypes/namespace1.entityTypeIdentifier/entities/namespace2.entityIdentifier`.\n    The namespaces must be empty (being global) or one of the predetermined namespaces the customer\n    has access to. If `namespace1` is not empty, it must be equal to `namespace2`.\n    The entity identifier must match the regex `\\w[\\w-]{0,63}`.\n    '
    display_name: builtins.str
    'Used when showing the entity in the Exabel app. Required when creating an entity.'
    description: builtins.str
    'Used when showing the entity in the Exabel app.'
    read_only: builtins.bool
    'Global entities and those from data sets that you subscribe to will be read-only.'

    @property
    def properties(self) -> google.protobuf.struct_pb2.Struct:
        """Additional properties of this entity. This is currently not used in the Exabel app, but may be
        in future.
        """

    def __init__(self, *, name: builtins.str | None=..., display_name: builtins.str | None=..., description: builtins.str | None=..., read_only: builtins.bool | None=..., properties: google.protobuf.struct_pb2.Struct | None=...) -> None:
        ...

    def HasField(self, field_name: typing_extensions.Literal['properties', b'properties']) -> builtins.bool:
        ...

    def ClearField(self, field_name: typing_extensions.Literal['description', b'description', 'display_name', b'display_name', 'name', b'name', 'properties', b'properties', 'read_only', b'read_only']) -> None:
        ...
global___Entity = Entity