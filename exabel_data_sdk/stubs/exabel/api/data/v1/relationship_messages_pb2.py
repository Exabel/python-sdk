"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from .....protoc_gen_openapiv2.options import annotations_pb2 as protoc__gen__openapiv2_dot_options_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n.exabel/api/data/v1/relationship_messages.proto\x12\x12exabel.api.data.v1\x1a\x1fgoogle/api/field_behavior.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a.protoc_gen_openapiv2/options/annotations.proto"\xd7\x01\n\x10RelationshipType\x12S\n\x04name\x18\x01 \x01(\tBE\xe0A\x05\xe0A\x02\x92A<J "relationshipTypes/ns.HAS_STORE"\xca>\x17\xfa\x02\x14relationshipTypeName\x12\x13\n\x0bdescription\x18\x02 \x01(\t\x12\x16\n\tread_only\x18\x03 \x01(\x08B\x03\xe0A\x03\x12\x14\n\x0cis_ownership\x18\x04 \x01(\x08\x12+\n\nproperties\x18d \x01(\x0b2\x17.google.protobuf.Struct"\xd0\x02\n\x0cRelationship\x12R\n\x06parent\x18\x01 \x01(\tBB\xe0A\x02\x92A<J "relationshipTypes/ns.HAS_STORE"\xca>\x17\xfa\x02\x14relationshipTypeName\x12E\n\x0bfrom_entity\x18\x02 \x01(\tB0\xe0A\x02\x92A*J("entityTypes/company/entities/F_12345-E"\x12K\n\tto_entity\x18\x03 \x01(\tB8\xe0A\x02\x92A2J0"entityTypes/ns.store/entities/ns.some_store_id"\x12\x13\n\x0bdescription\x18\x04 \x01(\t\x12\x16\n\tread_only\x18\x05 \x01(\x08B\x03\xe0A\x03\x12+\n\nproperties\x18d \x01(\x0b2\x17.google.protobuf.StructBM\n\x16com.exabel.api.data.v1B\x19RelationshipMessagesProtoP\x01Z\x16exabel.com/api/data/v1b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'exabel.api.data.v1.relationship_messages_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n\x16com.exabel.api.data.v1B\x19RelationshipMessagesProtoP\x01Z\x16exabel.com/api/data/v1'
    _RELATIONSHIPTYPE.fields_by_name['name']._options = None
    _RELATIONSHIPTYPE.fields_by_name['name']._serialized_options = b'\xe0A\x05\xe0A\x02\x92A<J "relationshipTypes/ns.HAS_STORE"\xca>\x17\xfa\x02\x14relationshipTypeName'
    _RELATIONSHIPTYPE.fields_by_name['read_only']._options = None
    _RELATIONSHIPTYPE.fields_by_name['read_only']._serialized_options = b'\xe0A\x03'
    _RELATIONSHIP.fields_by_name['parent']._options = None
    _RELATIONSHIP.fields_by_name['parent']._serialized_options = b'\xe0A\x02\x92A<J "relationshipTypes/ns.HAS_STORE"\xca>\x17\xfa\x02\x14relationshipTypeName'
    _RELATIONSHIP.fields_by_name['from_entity']._options = None
    _RELATIONSHIP.fields_by_name['from_entity']._serialized_options = b'\xe0A\x02\x92A*J("entityTypes/company/entities/F_12345-E"'
    _RELATIONSHIP.fields_by_name['to_entity']._options = None
    _RELATIONSHIP.fields_by_name['to_entity']._serialized_options = b'\xe0A\x02\x92A2J0"entityTypes/ns.store/entities/ns.some_store_id"'
    _RELATIONSHIP.fields_by_name['read_only']._options = None
    _RELATIONSHIP.fields_by_name['read_only']._serialized_options = b'\xe0A\x03'
    _RELATIONSHIPTYPE._serialized_start = 182
    _RELATIONSHIPTYPE._serialized_end = 397
    _RELATIONSHIP._serialized_start = 400
    _RELATIONSHIP._serialized_end = 736