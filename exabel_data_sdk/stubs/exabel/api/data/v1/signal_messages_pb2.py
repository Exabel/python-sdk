"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from .....exabel.api.math import aggregation_pb2 as exabel_dot_api_dot_math_dot_aggregation__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from .....protoc_gen_openapiv2.options import annotations_pb2 as protoc__gen__openapiv2_dot_options_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n(exabel/api/data/v1/signal_messages.proto\x12\x12exabel.api.data.v1\x1a!exabel/api/math/aggregation.proto\x1a\x1fgoogle/api/field_behavior.proto\x1a.protoc_gen_openapiv2/options/annotations.proto"\xbf\x02\n\x06Signal\x12<\n\x04name\x18\x01 \x01(\tB.\xe0A\x05\xe0A\x02\x92A%J\x13"signals/ns.signal"\xca>\r\xfa\x02\nsignalName\x12\x17\n\x0bentity_type\x18\x02 \x01(\tB\x02\x18\x01\x12&\n\x0cdisplay_name\x18\x03 \x01(\tB\x10\x92A\rJ\x0b"My signal"\x12\x13\n\x0bdescription\x18\x04 \x01(\t\x129\n\x13downsampling_method\x18\x05 \x01(\x0e2\x1c.exabel.api.math.Aggregation\x12\x16\n\tread_only\x18\x06 \x01(\x08B\x03\xe0A\x03\x12N\n\x0centity_types\x18\x07 \x03(\tB8\xe0A\x03\x92A2J0["entityTypes/ns.type1", "entityTypes/ns.type2"]BG\n\x16com.exabel.api.data.v1B\x13SignalMessagesProtoP\x01Z\x16exabel.com/api/data/v1b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'exabel.api.data.v1.signal_messages_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n\x16com.exabel.api.data.v1B\x13SignalMessagesProtoP\x01Z\x16exabel.com/api/data/v1'
    _SIGNAL.fields_by_name['name']._options = None
    _SIGNAL.fields_by_name['name']._serialized_options = b'\xe0A\x05\xe0A\x02\x92A%J\x13"signals/ns.signal"\xca>\r\xfa\x02\nsignalName'
    _SIGNAL.fields_by_name['entity_type']._options = None
    _SIGNAL.fields_by_name['entity_type']._serialized_options = b'\x18\x01'
    _SIGNAL.fields_by_name['display_name']._options = None
    _SIGNAL.fields_by_name['display_name']._serialized_options = b'\x92A\rJ\x0b"My signal"'
    _SIGNAL.fields_by_name['read_only']._options = None
    _SIGNAL.fields_by_name['read_only']._serialized_options = b'\xe0A\x03'
    _SIGNAL.fields_by_name['entity_types']._options = None
    _SIGNAL.fields_by_name['entity_types']._serialized_options = b'\xe0A\x03\x92A2J0["entityTypes/ns.type1", "entityTypes/ns.type2"]'
    _SIGNAL._serialized_start = 181
    _SIGNAL._serialized_end = 500