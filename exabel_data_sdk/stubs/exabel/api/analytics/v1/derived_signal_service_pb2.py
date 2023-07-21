"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from .....exabel.api.analytics.v1 import derived_signal_messages_pb2 as exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__messages__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from .....protoc_gen_openapiv2.options import annotations_pb2 as protoc__gen__openapiv2_dot_options_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n4exabel/api/analytics/v1/derived_signal_service.proto\x12\x17exabel.api.analytics.v1\x1a5exabel/api/analytics/v1/derived_signal_messages.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x1fgoogle/api/field_behavior.proto\x1a\x1bgoogle/protobuf/empty.proto\x1a google/protobuf/field_mask.proto\x1a.protoc_gen_openapiv2/options/annotations.proto"G\n\x17GetDerivedSignalRequest\x12,\n\x04name\x18\x01 \x01(\tB\x1e\x92A\x17\xca>\x14\xfa\x02\x11derivedSignalName\xe2A\x01\x02"j\n\x1aCreateDerivedSignalRequest\x12<\n\x06signal\x18\x01 \x01(\x0b2&.exabel.api.analytics.v1.DerivedSignalB\x04\xe2A\x01\x02\x12\x0e\n\x06folder\x18\x02 \x01(\t"\x8b\x01\n\x1aUpdateDerivedSignalRequest\x12<\n\x06signal\x18\x01 \x01(\x0b2&.exabel.api.analytics.v1.DerivedSignalB\x04\xe2A\x01\x02\x12/\n\x0bupdate_mask\x18\x02 \x01(\x0b2\x1a.google.protobuf.FieldMask"J\n\x1aDeleteDerivedSignalRequest\x12,\n\x04name\x18\x01 \x01(\tB\x1e\x92A\x17\xca>\x14\xfa\x02\x11derivedSignalName\xe2A\x01\x022\xdb\x05\n\x14DerivedSignalService\x12\xa8\x01\n\x10GetDerivedSignal\x120.exabel.api.analytics.v1.GetDerivedSignalRequest\x1a&.exabel.api.analytics.v1.DerivedSignal":\x92A\x14\x12\x12Get derived signal\x82\xd3\xe4\x93\x02\x1d\x12\x1b/v1/{name=derivedSignals/*}\x12\xb0\x01\n\x13CreateDerivedSignal\x123.exabel.api.analytics.v1.CreateDerivedSignalRequest\x1a&.exabel.api.analytics.v1.DerivedSignal"<\x92A\x17\x12\x15Create derived signal\x82\xd3\xe4\x93\x02\x1c"\x12/v1/derivedSignals:\x06signal\x12\xc0\x01\n\x13UpdateDerivedSignal\x123.exabel.api.analytics.v1.UpdateDerivedSignalRequest\x1a&.exabel.api.analytics.v1.DerivedSignal"L\x92A\x17\x12\x15Update derived signal\x82\xd3\xe4\x93\x02,2"/v1/{signal.name=derivedSignals/*}:\x06signal\x12\xa1\x01\n\x13DeleteDerivedSignal\x123.exabel.api.analytics.v1.DeleteDerivedSignalRequest\x1a\x16.google.protobuf.Empty"=\x92A\x17\x12\x15Delete derived signal\x82\xd3\xe4\x93\x02\x1d*\x1b/v1/{name=derivedSignals/*}BW\n\x1bcom.exabel.api.analytics.v1B\x19DerivedSignalServiceProtoP\x01Z\x1bexabel.com/api/analytics/v1b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'exabel.api.analytics.v1.derived_signal_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n\x1bcom.exabel.api.analytics.v1B\x19DerivedSignalServiceProtoP\x01Z\x1bexabel.com/api/analytics/v1'
    _GETDERIVEDSIGNALREQUEST.fields_by_name['name']._options = None
    _GETDERIVEDSIGNALREQUEST.fields_by_name['name']._serialized_options = b'\x92A\x17\xca>\x14\xfa\x02\x11derivedSignalName\xe2A\x01\x02'
    _CREATEDERIVEDSIGNALREQUEST.fields_by_name['signal']._options = None
    _CREATEDERIVEDSIGNALREQUEST.fields_by_name['signal']._serialized_options = b'\xe2A\x01\x02'
    _UPDATEDERIVEDSIGNALREQUEST.fields_by_name['signal']._options = None
    _UPDATEDERIVEDSIGNALREQUEST.fields_by_name['signal']._serialized_options = b'\xe2A\x01\x02'
    _DELETEDERIVEDSIGNALREQUEST.fields_by_name['name']._options = None
    _DELETEDERIVEDSIGNALREQUEST.fields_by_name['name']._serialized_options = b'\x92A\x17\xca>\x14\xfa\x02\x11derivedSignalName\xe2A\x01\x02'
    _DERIVEDSIGNALSERVICE.methods_by_name['GetDerivedSignal']._options = None
    _DERIVEDSIGNALSERVICE.methods_by_name['GetDerivedSignal']._serialized_options = b'\x92A\x14\x12\x12Get derived signal\x82\xd3\xe4\x93\x02\x1d\x12\x1b/v1/{name=derivedSignals/*}'
    _DERIVEDSIGNALSERVICE.methods_by_name['CreateDerivedSignal']._options = None
    _DERIVEDSIGNALSERVICE.methods_by_name['CreateDerivedSignal']._serialized_options = b'\x92A\x17\x12\x15Create derived signal\x82\xd3\xe4\x93\x02\x1c"\x12/v1/derivedSignals:\x06signal'
    _DERIVEDSIGNALSERVICE.methods_by_name['UpdateDerivedSignal']._options = None
    _DERIVEDSIGNALSERVICE.methods_by_name['UpdateDerivedSignal']._serialized_options = b'\x92A\x17\x12\x15Update derived signal\x82\xd3\xe4\x93\x02,2"/v1/{signal.name=derivedSignals/*}:\x06signal'
    _DERIVEDSIGNALSERVICE.methods_by_name['DeleteDerivedSignal']._options = None
    _DERIVEDSIGNALSERVICE.methods_by_name['DeleteDerivedSignal']._serialized_options = b'\x92A\x17\x12\x15Delete derived signal\x82\xd3\xe4\x93\x02\x1d*\x1b/v1/{name=derivedSignals/*}'
    _globals['_GETDERIVEDSIGNALREQUEST']._serialized_start = 310
    _globals['_GETDERIVEDSIGNALREQUEST']._serialized_end = 381
    _globals['_CREATEDERIVEDSIGNALREQUEST']._serialized_start = 383
    _globals['_CREATEDERIVEDSIGNALREQUEST']._serialized_end = 489
    _globals['_UPDATEDERIVEDSIGNALREQUEST']._serialized_start = 492
    _globals['_UPDATEDERIVEDSIGNALREQUEST']._serialized_end = 631
    _globals['_DELETEDERIVEDSIGNALREQUEST']._serialized_start = 633
    _globals['_DELETEDERIVEDSIGNALREQUEST']._serialized_end = 707
    _globals['_DERIVEDSIGNALSERVICE']._serialized_start = 710
    _globals['_DERIVEDSIGNALSERVICE']._serialized_end = 1441