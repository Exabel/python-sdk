"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n+exabel/api/analytics/v1/item_messages.proto\x12\x17exabel.api.analytics.v1\x1a\x1fgoogle/api/field_behavior.proto\x1a\x1fgoogle/protobuf/timestamp.proto"\xe2\x01\n\x0cItemMetadata\x125\n\x0bcreate_time\x18\x01 \x01(\x0b2\x1a.google.protobuf.TimestampB\x04\xe2A\x01\x03\x125\n\x0bupdate_time\x18\x02 \x01(\x0b2\x1a.google.protobuf.TimestampB\x04\xe2A\x01\x03\x12\x18\n\ncreated_by\x18\x03 \x01(\tB\x04\xe2A\x01\x03\x12\x18\n\nupdated_by\x18\x04 \x01(\tB\x04\xe2A\x01\x03\x12\x1f\n\x0cwrite_access\x18\x05 \x01(\x08B\x04\xe2A\x01\x03H\x00\x88\x01\x01B\x0f\n\r_write_accessBO\n\x1bcom.exabel.api.analytics.v1B\x11ItemMessagesProtoP\x01Z\x1bexabel.com/api/analytics/v1b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'exabel.api.analytics.v1.item_messages_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n\x1bcom.exabel.api.analytics.v1B\x11ItemMessagesProtoP\x01Z\x1bexabel.com/api/analytics/v1'
    _ITEMMETADATA.fields_by_name['create_time']._options = None
    _ITEMMETADATA.fields_by_name['create_time']._serialized_options = b'\xe2A\x01\x03'
    _ITEMMETADATA.fields_by_name['update_time']._options = None
    _ITEMMETADATA.fields_by_name['update_time']._serialized_options = b'\xe2A\x01\x03'
    _ITEMMETADATA.fields_by_name['created_by']._options = None
    _ITEMMETADATA.fields_by_name['created_by']._serialized_options = b'\xe2A\x01\x03'
    _ITEMMETADATA.fields_by_name['updated_by']._options = None
    _ITEMMETADATA.fields_by_name['updated_by']._serialized_options = b'\xe2A\x01\x03'
    _ITEMMETADATA.fields_by_name['write_access']._options = None
    _ITEMMETADATA.fields_by_name['write_access']._serialized_options = b'\xe2A\x01\x03'
    _globals['_ITEMMETADATA']._serialized_start = 139
    _globals['_ITEMMETADATA']._serialized_end = 365