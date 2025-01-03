"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 28, 1, '', 'exabel/api/management/v1/user_messages.proto')
_sym_db = _symbol_database.Default()
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n,exabel/api/management/v1/user_messages.proto\x12\x18exabel.api.management.v1\x1a\x1fgoogle/api/field_behavior.proto"9\n\x04User\x12\x11\n\x04name\x18\x01 \x01(\tB\x03\xe0A\x03\x12\r\n\x05email\x18\x02 \x01(\t\x12\x0f\n\x07blocked\x18\x03 \x01(\x08"_\n\x05Group\x12\x11\n\x04name\x18\x01 \x01(\tB\x03\xe0A\x03\x12\x14\n\x0cdisplay_name\x18\x02 \x01(\t\x12-\n\x05users\x18\x03 \x03(\x0b2\x1e.exabel.api.management.v1.UserBQ\n\x1ccom.exabel.api.management.v1B\x11UserMessagesProtoP\x01Z\x1cexabel.com/api/management/v1b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'exabel.api.management.v1.user_messages_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'\n\x1ccom.exabel.api.management.v1B\x11UserMessagesProtoP\x01Z\x1cexabel.com/api/management/v1'
    _globals['_USER'].fields_by_name['name']._loaded_options = None
    _globals['_USER'].fields_by_name['name']._serialized_options = b'\xe0A\x03'
    _globals['_GROUP'].fields_by_name['name']._loaded_options = None
    _globals['_GROUP'].fields_by_name['name']._serialized_options = b'\xe0A\x03'
    _globals['_USER']._serialized_start = 107
    _globals['_USER']._serialized_end = 164
    _globals['_GROUP']._serialized_start = 166
    _globals['_GROUP']._serialized_end = 261