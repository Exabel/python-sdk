"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 28, 1, '', 'exabel/api/analytics/v1/tag_messages.proto')
_sym_db = _symbol_database.Default()
from .....exabel.api.analytics.v1 import item_messages_pb2 as exabel_dot_api_dot_analytics_dot_v1_dot_item__messages__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from .....protoc_gen_openapiv2.options import annotations_pb2 as protoc__gen__openapiv2_dot_options_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n*exabel/api/analytics/v1/tag_messages.proto\x12\x17exabel.api.analytics.v1\x1a+exabel/api/analytics/v1/item_messages.proto\x1a\x1fgoogle/api/field_behavior.proto\x1a.protoc_gen_openapiv2/options/annotations.proto"\xc5\x01\n\x03Tag\x12\x11\n\x04name\x18\x01 \x01(\tB\x03\xe0A\x03\x12#\n\x0cdisplay_name\x18\x02 \x01(\tB\r\x92A\nJ\x08"My tag"\x12.\n\x0bdescription\x18\x03 \x01(\tB\x19\x92A\x16J\x14"My tag description"\x12\x18\n\x0bentity_type\x18\x04 \x01(\tB\x03\xe0A\x03\x12<\n\x08metadata\x18\x05 \x01(\x0b2%.exabel.api.analytics.v1.ItemMetadataB\x03\xe0A\x03BN\n\x1bcom.exabel.api.analytics.v1B\x10TagMessagesProtoP\x01Z\x1bexabel.com/api/analytics/v1b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'exabel.api.analytics.v1.tag_messages_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'\n\x1bcom.exabel.api.analytics.v1B\x10TagMessagesProtoP\x01Z\x1bexabel.com/api/analytics/v1'
    _globals['_TAG'].fields_by_name['name']._loaded_options = None
    _globals['_TAG'].fields_by_name['name']._serialized_options = b'\xe0A\x03'
    _globals['_TAG'].fields_by_name['display_name']._loaded_options = None
    _globals['_TAG'].fields_by_name['display_name']._serialized_options = b'\x92A\nJ\x08"My tag"'
    _globals['_TAG'].fields_by_name['description']._loaded_options = None
    _globals['_TAG'].fields_by_name['description']._serialized_options = b'\x92A\x16J\x14"My tag description"'
    _globals['_TAG'].fields_by_name['entity_type']._loaded_options = None
    _globals['_TAG'].fields_by_name['entity_type']._serialized_options = b'\xe0A\x03'
    _globals['_TAG'].fields_by_name['metadata']._loaded_options = None
    _globals['_TAG'].fields_by_name['metadata']._serialized_options = b'\xe0A\x03'
    _globals['_TAG']._serialized_start = 198
    _globals['_TAG']._serialized_end = 395