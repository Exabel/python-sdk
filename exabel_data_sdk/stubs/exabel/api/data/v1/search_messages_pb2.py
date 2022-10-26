"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from .....protoc_gen_openapiv2.options import annotations_pb2 as protoc__gen__openapiv2_dot_options_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n(exabel/api/data/v1/search_messages.proto\x12\x12exabel.api.data.v1\x1a\x1fgoogle/api/field_behavior.proto\x1a.protoc_gen_openapiv2/options/annotations.proto"O\n\nSearchTerm\x12\x1d\n\x05field\x18\x01 \x01(\tB\x0e\xe0A\x02\x92A\x08J\x06"text"\x12"\n\x05query\x18\x02 \x01(\tB\x13\xe0A\x02\x92A\rJ\x0b"microsoft"BG\n\x16com.exabel.api.data.v1B\x13SearchMessagesProtoP\x01Z\x16exabel.com/api/data/v1b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'exabel.api.data.v1.search_messages_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n\x16com.exabel.api.data.v1B\x13SearchMessagesProtoP\x01Z\x16exabel.com/api/data/v1'
    _SEARCHTERM.fields_by_name['field']._options = None
    _SEARCHTERM.fields_by_name['field']._serialized_options = b'\xe0A\x02\x92A\x08J\x06"text"'
    _SEARCHTERM.fields_by_name['query']._options = None
    _SEARCHTERM.fields_by_name['query']._serialized_options = b'\xe0A\x02\x92A\rJ\x0b"microsoft"'
    _SEARCHTERM._serialized_start = 145
    _SEARCHTERM._serialized_end = 224