"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from .....exabel.api.analytics.v1 import item_messages_pb2 as exabel_dot_api_dot_analytics_dot_v1_dot_item__messages__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n*exabel/api/analytics/v1/tag_messages.proto\x12\x17exabel.api.analytics.v1\x1a+exabel/api/analytics/v1/item_messages.proto\x1a\x1fgoogle/api/field_behavior.proto"\x9b\x01\n\x03Tag\x12\x11\n\x04name\x18\x01 \x01(\tB\x03\xe0A\x03\x12\x14\n\x0cdisplay_name\x18\x02 \x01(\t\x12\x13\n\x0bdescription\x18\x03 \x01(\t\x12\x18\n\x0bentity_type\x18\x04 \x01(\tB\x03\xe0A\x03\x12<\n\x08metadata\x18\x05 \x01(\x0b2%.exabel.api.analytics.v1.ItemMetadataB\x03\xe0A\x03BN\n\x1bcom.exabel.api.analytics.v1B\x10TagMessagesProtoP\x01Z\x1bexabel.com/api/analytics/v1b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'exabel.api.analytics.v1.tag_messages_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n\x1bcom.exabel.api.analytics.v1B\x10TagMessagesProtoP\x01Z\x1bexabel.com/api/analytics/v1'
    _TAG.fields_by_name['name']._options = None
    _TAG.fields_by_name['name']._serialized_options = b'\xe0A\x03'
    _TAG.fields_by_name['entity_type']._options = None
    _TAG.fields_by_name['entity_type']._serialized_options = b'\xe0A\x03'
    _TAG.fields_by_name['metadata']._options = None
    _TAG.fields_by_name['metadata']._serialized_options = b'\xe0A\x03'
    _TAG._serialized_start = 150
    _TAG._serialized_end = 305