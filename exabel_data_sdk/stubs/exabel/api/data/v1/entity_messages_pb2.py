"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from .....protoc_gen_openapiv2.options import annotations_pb2 as protoc__gen__openapiv2_dot_options_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n(exabel/api/data/v1/entity_messages.proto\x12\x12exabel.api.data.v1\x1a\x1fgoogle/api/field_behavior.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a.protoc_gen_openapiv2/options/annotations.proto"\xe2\x01\n\nEntityType\x12B\n\x04name\x18\x01 \x01(\tB4\xe0A\x05\xe0A\x02\x92A+J\x15"entityTypes/company"\xca>\x11\xfa\x02\x0eentityTypeName\x12&\n\x0cdisplay_name\x18\x02 \x01(\tB\x10\x92A\rJ\x0b"Companies"\x12,\n\x0bdescription\x18\x03 \x01(\tB\x17\x92A\x14J\x12"Public companies"\x12\x16\n\tread_only\x18\x04 \x01(\x08B\x03\xe0A\x03\x12"\n\x0eis_associative\x18\x05 \x01(\x08B\n\x92A\x07J\x05false"\xa1\x01\n\x06Entity\x12\'\n\x04name\x18\x01 \x01(\tB\x19\xe0A\x05\xe0A\x02\x92A\x10\xca>\r\xfa\x02\nentityName\x12\x14\n\x0cdisplay_name\x18\x02 \x01(\t\x12\x13\n\x0bdescription\x18\x03 \x01(\t\x12\x16\n\tread_only\x18\x04 \x01(\x08B\x03\xe0A\x03\x12+\n\nproperties\x18d \x01(\x0b2\x17.google.protobuf.StructBG\n\x16com.exabel.api.data.v1B\x13EntityMessagesProtoP\x01Z\x16exabel.com/api/data/v1b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'exabel.api.data.v1.entity_messages_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n\x16com.exabel.api.data.v1B\x13EntityMessagesProtoP\x01Z\x16exabel.com/api/data/v1'
    _ENTITYTYPE.fields_by_name['name']._options = None
    _ENTITYTYPE.fields_by_name['name']._serialized_options = b'\xe0A\x05\xe0A\x02\x92A+J\x15"entityTypes/company"\xca>\x11\xfa\x02\x0eentityTypeName'
    _ENTITYTYPE.fields_by_name['display_name']._options = None
    _ENTITYTYPE.fields_by_name['display_name']._serialized_options = b'\x92A\rJ\x0b"Companies"'
    _ENTITYTYPE.fields_by_name['description']._options = None
    _ENTITYTYPE.fields_by_name['description']._serialized_options = b'\x92A\x14J\x12"Public companies"'
    _ENTITYTYPE.fields_by_name['read_only']._options = None
    _ENTITYTYPE.fields_by_name['read_only']._serialized_options = b'\xe0A\x03'
    _ENTITYTYPE.fields_by_name['is_associative']._options = None
    _ENTITYTYPE.fields_by_name['is_associative']._serialized_options = b'\x92A\x07J\x05false'
    _ENTITY.fields_by_name['name']._options = None
    _ENTITY.fields_by_name['name']._serialized_options = b'\xe0A\x05\xe0A\x02\x92A\x10\xca>\r\xfa\x02\nentityName'
    _ENTITY.fields_by_name['read_only']._options = None
    _ENTITY.fields_by_name['read_only']._serialized_options = b'\xe0A\x03'
    _ENTITYTYPE._serialized_start = 176
    _ENTITYTYPE._serialized_end = 402
    _ENTITY._serialized_start = 405
    _ENTITY._serialized_end = 566