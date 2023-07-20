"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from .....protoc_gen_openapiv2.options import annotations_pb2 as protoc__gen__openapiv2_dot_options_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n.exabel/api/data/v1/relationship_messages.proto\x12\x12exabel.api.data.v1\x1a\x1fgoogle/api/field_behavior.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a.protoc_gen_openapiv2/options/annotations.proto"\x85\x02\n\x10RelationshipType\x12R\n\x04name\x18\x01 \x01(\tBD\x92A<J "relationshipTypes/ns.HAS_STORE"\xca>\x17\xfa\x02\x14relationshipTypeName\xe2A\x02\x05\x02\x12A\n\x0bdescription\x18\x02 \x01(\tB,\x92A)J\'"Indicates that an entity owns a store"\x12\x17\n\tread_only\x18\x03 \x01(\x08B\x04\xe2A\x01\x03\x12\x14\n\x0cis_ownership\x18\x04 \x01(\x08\x12+\n\nproperties\x18d \x01(\x0b2\x17.google.protobuf.Struct"\xf9\x02\n\x0cRelationship\x12S\n\x06parent\x18\x01 \x01(\tBC\x92A<J "relationshipTypes/ns.HAS_STORE"\xca>\x17\xfa\x02\x14relationshipTypeName\xe2A\x01\x02\x12F\n\x0bfrom_entity\x18\x02 \x01(\tB1\x92A*J("entityTypes/company/entities/F_12345-E"\xe2A\x01\x02\x12L\n\tto_entity\x18\x03 \x01(\tB9\x92A2J0"entityTypes/ns.store/entities/ns.some_store_id"\xe2A\x01\x02\x128\n\x0bdescription\x18\x04 \x01(\tB#\x92A J\x1e"F_12345-E owns some_store_id"\x12\x17\n\tread_only\x18\x05 \x01(\x08B\x04\xe2A\x01\x03\x12+\n\nproperties\x18d \x01(\x0b2\x17.google.protobuf.StructBM\n\x16com.exabel.api.data.v1B\x19RelationshipMessagesProtoP\x01Z\x16exabel.com/api/data/v1b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'exabel.api.data.v1.relationship_messages_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n\x16com.exabel.api.data.v1B\x19RelationshipMessagesProtoP\x01Z\x16exabel.com/api/data/v1'
    _RELATIONSHIPTYPE.fields_by_name['name']._options = None
    _RELATIONSHIPTYPE.fields_by_name['name']._serialized_options = b'\x92A<J "relationshipTypes/ns.HAS_STORE"\xca>\x17\xfa\x02\x14relationshipTypeName\xe2A\x02\x05\x02'
    _RELATIONSHIPTYPE.fields_by_name['description']._options = None
    _RELATIONSHIPTYPE.fields_by_name['description']._serialized_options = b'\x92A)J\'"Indicates that an entity owns a store"'
    _RELATIONSHIPTYPE.fields_by_name['read_only']._options = None
    _RELATIONSHIPTYPE.fields_by_name['read_only']._serialized_options = b'\xe2A\x01\x03'
    _RELATIONSHIP.fields_by_name['parent']._options = None
    _RELATIONSHIP.fields_by_name['parent']._serialized_options = b'\x92A<J "relationshipTypes/ns.HAS_STORE"\xca>\x17\xfa\x02\x14relationshipTypeName\xe2A\x01\x02'
    _RELATIONSHIP.fields_by_name['from_entity']._options = None
    _RELATIONSHIP.fields_by_name['from_entity']._serialized_options = b'\x92A*J("entityTypes/company/entities/F_12345-E"\xe2A\x01\x02'
    _RELATIONSHIP.fields_by_name['to_entity']._options = None
    _RELATIONSHIP.fields_by_name['to_entity']._serialized_options = b'\x92A2J0"entityTypes/ns.store/entities/ns.some_store_id"\xe2A\x01\x02'
    _RELATIONSHIP.fields_by_name['description']._options = None
    _RELATIONSHIP.fields_by_name['description']._serialized_options = b'\x92A J\x1e"F_12345-E owns some_store_id"'
    _RELATIONSHIP.fields_by_name['read_only']._options = None
    _RELATIONSHIP.fields_by_name['read_only']._serialized_options = b'\xe2A\x01\x03'
    _globals['_RELATIONSHIPTYPE']._serialized_start = 182
    _globals['_RELATIONSHIPTYPE']._serialized_end = 443
    _globals['_RELATIONSHIP']._serialized_start = 446
    _globals['_RELATIONSHIP']._serialized_end = 823