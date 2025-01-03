"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 28, 1, '', 'exabel/api/data/v1/search_messages.proto')
_sym_db = _symbol_database.Default()
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from .....protoc_gen_openapiv2.options import annotations_pb2 as protoc__gen__openapiv2_dot_options_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n(exabel/api/data/v1/search_messages.proto\x12\x12exabel.api.data.v1\x1a\x1fgoogle/api/field_behavior.proto\x1a.protoc_gen_openapiv2/options/annotations.proto"O\n\nSearchTerm\x12\x1d\n\x05field\x18\x01 \x01(\tB\x0e\x92A\x08J\x06"text"\xe0A\x02\x12"\n\x05query\x18\x02 \x01(\tB\x13\x92A\rJ\x0b"microsoft"\xe0A\x02"E\n\rSearchOptions\x124\n\x08universe\x18\x01 \x01(\x0e2".exabel.api.data.v1.SearchUniverse*Z\n\x0eSearchUniverse\x12\x1f\n\x1bSEARCH_UNIVERSE_UNSPECIFIED\x10\x00\x12\x14\n\x10EXABEL_COMPANIES\x10\x01\x12\x11\n\rALL_COMPANIES\x10\x02BG\n\x16com.exabel.api.data.v1B\x13SearchMessagesProtoP\x01Z\x16exabel.com/api/data/v1b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'exabel.api.data.v1.search_messages_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'\n\x16com.exabel.api.data.v1B\x13SearchMessagesProtoP\x01Z\x16exabel.com/api/data/v1'
    _globals['_SEARCHTERM'].fields_by_name['field']._loaded_options = None
    _globals['_SEARCHTERM'].fields_by_name['field']._serialized_options = b'\x92A\x08J\x06"text"\xe0A\x02'
    _globals['_SEARCHTERM'].fields_by_name['query']._loaded_options = None
    _globals['_SEARCHTERM'].fields_by_name['query']._serialized_options = b'\x92A\rJ\x0b"microsoft"\xe0A\x02'
    _globals['_SEARCHUNIVERSE']._serialized_start = 297
    _globals['_SEARCHUNIVERSE']._serialized_end = 387
    _globals['_SEARCHTERM']._serialized_start = 145
    _globals['_SEARCHTERM']._serialized_end = 224
    _globals['_SEARCHOPTIONS']._serialized_start = 226
    _globals['_SEARCHOPTIONS']._serialized_end = 295