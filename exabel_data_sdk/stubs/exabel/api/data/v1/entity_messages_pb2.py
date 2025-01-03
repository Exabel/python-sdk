"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 28, 1, '', 'exabel/api/data/v1/entity_messages.proto')
_sym_db = _symbol_database.Default()
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from .....protoc_gen_openapiv2.options import annotations_pb2 as protoc__gen__openapiv2_dot_options_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n(exabel/api/data/v1/entity_messages.proto\x12\x12exabel.api.data.v1\x1a\x1fgoogle/api/field_behavior.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a.protoc_gen_openapiv2/options/annotations.proto"\xe2\x01\n\nEntityType\x12B\n\x04name\x18\x01 \x01(\tB4\x92A+J\x15"entityTypes/company"\xca>\x11\xfa\x02\x0eentityTypeName\xe0A\x05\xe0A\x02\x12&\n\x0cdisplay_name\x18\x02 \x01(\tB\x10\x92A\rJ\x0b"Companies"\x12,\n\x0bdescription\x18\x03 \x01(\tB\x17\x92A\x14J\x12"Public companies"\x12\x16\n\tread_only\x18\x04 \x01(\x08B\x03\xe0A\x03\x12"\n\x0eis_associative\x18\x05 \x01(\x08B\n\x92A\x07J\x05false"\xf7\x01\n\x06Entity\x12@\n\x04name\x18\x01 \x01(\tB2\x92A)J\x17"entities/ns.my_entity"\xca>\r\xfa\x02\nentityName\xe0A\x05\xe0A\x02\x12&\n\x0cdisplay_name\x18\x02 \x01(\tB\x10\x92A\rJ\x0b"My Entity"\x12>\n\x0bdescription\x18\x03 \x01(\tB)\x92A&J$"This is a description of My Entity"\x12\x16\n\tread_only\x18\x04 \x01(\x08B\x03\xe0A\x03\x12+\n\nproperties\x18d \x01(\x0b2\x17.google.protobuf.StructBG\n\x16com.exabel.api.data.v1B\x13EntityMessagesProtoP\x01Z\x16exabel.com/api/data/v1b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'exabel.api.data.v1.entity_messages_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'\n\x16com.exabel.api.data.v1B\x13EntityMessagesProtoP\x01Z\x16exabel.com/api/data/v1'
    _globals['_ENTITYTYPE'].fields_by_name['name']._loaded_options = None
    _globals['_ENTITYTYPE'].fields_by_name['name']._serialized_options = b'\x92A+J\x15"entityTypes/company"\xca>\x11\xfa\x02\x0eentityTypeName\xe0A\x05\xe0A\x02'
    _globals['_ENTITYTYPE'].fields_by_name['display_name']._loaded_options = None
    _globals['_ENTITYTYPE'].fields_by_name['display_name']._serialized_options = b'\x92A\rJ\x0b"Companies"'
    _globals['_ENTITYTYPE'].fields_by_name['description']._loaded_options = None
    _globals['_ENTITYTYPE'].fields_by_name['description']._serialized_options = b'\x92A\x14J\x12"Public companies"'
    _globals['_ENTITYTYPE'].fields_by_name['read_only']._loaded_options = None
    _globals['_ENTITYTYPE'].fields_by_name['read_only']._serialized_options = b'\xe0A\x03'
    _globals['_ENTITYTYPE'].fields_by_name['is_associative']._loaded_options = None
    _globals['_ENTITYTYPE'].fields_by_name['is_associative']._serialized_options = b'\x92A\x07J\x05false'
    _globals['_ENTITY'].fields_by_name['name']._loaded_options = None
    _globals['_ENTITY'].fields_by_name['name']._serialized_options = b'\x92A)J\x17"entities/ns.my_entity"\xca>\r\xfa\x02\nentityName\xe0A\x05\xe0A\x02'
    _globals['_ENTITY'].fields_by_name['display_name']._loaded_options = None
    _globals['_ENTITY'].fields_by_name['display_name']._serialized_options = b'\x92A\rJ\x0b"My Entity"'
    _globals['_ENTITY'].fields_by_name['description']._loaded_options = None
    _globals['_ENTITY'].fields_by_name['description']._serialized_options = b'\x92A&J$"This is a description of My Entity"'
    _globals['_ENTITY'].fields_by_name['read_only']._loaded_options = None
    _globals['_ENTITY'].fields_by_name['read_only']._serialized_options = b'\xe0A\x03'
    _globals['_ENTITYTYPE']._serialized_start = 176
    _globals['_ENTITYTYPE']._serialized_end = 402
    _globals['_ENTITY']._serialized_start = 405
    _globals['_ENTITY']._serialized_end = 652