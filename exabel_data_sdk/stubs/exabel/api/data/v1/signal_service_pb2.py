"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 28, 1, '', 'exabel/api/data/v1/signal_service.proto')
_sym_db = _symbol_database.Default()
from .....exabel.api.data.v1 import signal_messages_pb2 as exabel_dot_api_dot_data_dot_v1_dot_signal__messages__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from .....protoc_gen_openapiv2.options import annotations_pb2 as protoc__gen__openapiv2_dot_options_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\'exabel/api/data/v1/signal_service.proto\x12\x12exabel.api.data.v1\x1a(exabel/api/data/v1/signal_messages.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x1fgoogle/api/field_behavior.proto\x1a\x1bgoogle/protobuf/empty.proto\x1a google/protobuf/field_mask.proto\x1a.protoc_gen_openapiv2/options/annotations.proto";\n\x12ListSignalsRequest\x12\x11\n\tpage_size\x18\x01 \x01(\x05\x12\x12\n\npage_token\x18\x02 \x01(\t"o\n\x13ListSignalsResponse\x12+\n\x07signals\x18\x01 \x03(\x0b2\x1a.exabel.api.data.v1.Signal\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\x12\x12\n\ntotal_size\x18\x03 \x01(\x05"8\n\x10GetSignalRequest\x12$\n\x04name\x18\x01 \x01(\tB\x16\x92A\x10\xca>\r\xfa\x02\nsignalName\xe0A\x02"e\n\x13CreateSignalRequest\x12/\n\x06signal\x18\x01 \x01(\x0b2\x1a.exabel.api.data.v1.SignalB\x03\xe0A\x02\x12\x1d\n\x15create_library_signal\x18\x02 \x01(\x08"\xad\x01\n\x13UpdateSignalRequest\x12/\n\x06signal\x18\x01 \x01(\x0b2\x1a.exabel.api.data.v1.SignalB\x03\xe0A\x02\x12/\n\x0bupdate_mask\x18\x02 \x01(\x0b2\x1a.google.protobuf.FieldMask\x12\x15\n\rallow_missing\x18\x03 \x01(\x08\x12\x1d\n\x15create_library_signal\x18\x04 \x01(\x08";\n\x13DeleteSignalRequest\x12$\n\x04name\x18\x01 \x01(\tB\x16\x92A\x10\xca>\r\xfa\x02\nsignalName\xe0A\x02"B\n\x19ListDerivedSignalsRequest\x12\x11\n\tpage_size\x18\x01 \x01(\x05\x12\x12\n\npage_token\x18\x02 \x01(\t"\x85\x01\n\x1aListDerivedSignalsResponse\x12:\n\x0fderived_signals\x18\x01 \x03(\x0b2!.exabel.api.data.v1.DerivedSignal\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\x12\x12\n\ntotal_size\x18\x03 \x01(\x05"3\n\x1bFilterDerivedSignalsRequest\x12\x14\n\x0centity_names\x18\x01 \x03(\t"\xd8\x01\n\x1cFilterDerivedSignalsResponse\x12]\n\x0fderived_signals\x18\x01 \x03(\x0b2D.exabel.api.data.v1.FilterDerivedSignalsResponse.DerivedSignalsEntry\x1aY\n\x13DerivedSignalsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x121\n\x05value\x18\x02 \x01(\x0b2".exabel.api.data.v1.DerivedSignals:\x028\x01"F\n\x17GetDerivedSignalRequest\x12+\n\x04name\x18\x01 \x01(\tB\x1d\x92A\x17\xca>\x14\xfa\x02\x11derivedSignalName\xe0A\x022\xb3\t\n\rSignalService\x12\x84\x01\n\x0bListSignals\x12&.exabel.api.data.v1.ListSignalsRequest\x1a\'.exabel.api.data.v1.ListSignalsResponse"$\x92A\x0e\x12\x0cList signals\x82\xd3\xe4\x93\x02\r\x12\x0b/v1/signals\x12z\n\tGetSignal\x12$.exabel.api.data.v1.GetSignalRequest\x1a\x1a.exabel.api.data.v1.Signal"+\x92A\x0c\x12\nGet signal\x82\xd3\xe4\x93\x02\x16\x12\x14/v1/{name=signals/*}\x12\x82\x01\n\x0cCreateSignal\x12\'.exabel.api.data.v1.CreateSignalRequest\x1a\x1a.exabel.api.data.v1.Signal"-\x92A\x0f\x12\rCreate signal\x82\xd3\xe4\x93\x02\x15"\x0b/v1/signals:\x06signal\x12\x92\x01\n\x0cUpdateSignal\x12\'.exabel.api.data.v1.UpdateSignalRequest\x1a\x1a.exabel.api.data.v1.Signal"=\x92A\x0f\x12\rUpdate signal\x82\xd3\xe4\x93\x02%2\x1b/v1/{signal.name=signals/*}:\x06signal\x12\x7f\n\x0cDeleteSignal\x12\'.exabel.api.data.v1.DeleteSignalRequest\x1a\x16.google.protobuf.Empty".\x92A\x0f\x12\rDelete signal\x82\xd3\xe4\x93\x02\x16*\x14/v1/{name=signals/*}\x12\xa8\x01\n\x12ListDerivedSignals\x12-.exabel.api.data.v1.ListDerivedSignalsRequest\x1a..exabel.api.data.v1.ListDerivedSignalsResponse"3\x92A\x16\x12\x14List derived signals\x82\xd3\xe4\x93\x02\x14\x12\x12/v1/derivedSignals\x12\xb7\x01\n\x14FilterDerivedSignals\x12/.exabel.api.data.v1.FilterDerivedSignalsRequest\x1a0.exabel.api.data.v1.FilterDerivedSignalsResponse"<\x92A\x18\x12\x16Filter derived signals\x82\xd3\xe4\x93\x02\x1b\x12\x19/v1/derivedSignals:filter\x12\x9e\x01\n\x10GetDerivedSignal\x12+.exabel.api.data.v1.GetDerivedSignalRequest\x1a!.exabel.api.data.v1.DerivedSignal":\x92A\x14\x12\x12Get derived signal\x82\xd3\xe4\x93\x02\x1d\x12\x1b/v1/{name=derivedSignals/*}BF\n\x16com.exabel.api.data.v1B\x12SignalServiceProtoP\x01Z\x16exabel.com/api/data/v1b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'exabel.api.data.v1.signal_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'\n\x16com.exabel.api.data.v1B\x12SignalServiceProtoP\x01Z\x16exabel.com/api/data/v1'
    _globals['_GETSIGNALREQUEST'].fields_by_name['name']._loaded_options = None
    _globals['_GETSIGNALREQUEST'].fields_by_name['name']._serialized_options = b'\x92A\x10\xca>\r\xfa\x02\nsignalName\xe0A\x02'
    _globals['_CREATESIGNALREQUEST'].fields_by_name['signal']._loaded_options = None
    _globals['_CREATESIGNALREQUEST'].fields_by_name['signal']._serialized_options = b'\xe0A\x02'
    _globals['_UPDATESIGNALREQUEST'].fields_by_name['signal']._loaded_options = None
    _globals['_UPDATESIGNALREQUEST'].fields_by_name['signal']._serialized_options = b'\xe0A\x02'
    _globals['_DELETESIGNALREQUEST'].fields_by_name['name']._loaded_options = None
    _globals['_DELETESIGNALREQUEST'].fields_by_name['name']._serialized_options = b'\x92A\x10\xca>\r\xfa\x02\nsignalName\xe0A\x02'
    _globals['_FILTERDERIVEDSIGNALSRESPONSE_DERIVEDSIGNALSENTRY']._loaded_options = None
    _globals['_FILTERDERIVEDSIGNALSRESPONSE_DERIVEDSIGNALSENTRY']._serialized_options = b'8\x01'
    _globals['_GETDERIVEDSIGNALREQUEST'].fields_by_name['name']._loaded_options = None
    _globals['_GETDERIVEDSIGNALREQUEST'].fields_by_name['name']._serialized_options = b'\x92A\x17\xca>\x14\xfa\x02\x11derivedSignalName\xe0A\x02'
    _globals['_SIGNALSERVICE'].methods_by_name['ListSignals']._loaded_options = None
    _globals['_SIGNALSERVICE'].methods_by_name['ListSignals']._serialized_options = b'\x92A\x0e\x12\x0cList signals\x82\xd3\xe4\x93\x02\r\x12\x0b/v1/signals'
    _globals['_SIGNALSERVICE'].methods_by_name['GetSignal']._loaded_options = None
    _globals['_SIGNALSERVICE'].methods_by_name['GetSignal']._serialized_options = b'\x92A\x0c\x12\nGet signal\x82\xd3\xe4\x93\x02\x16\x12\x14/v1/{name=signals/*}'
    _globals['_SIGNALSERVICE'].methods_by_name['CreateSignal']._loaded_options = None
    _globals['_SIGNALSERVICE'].methods_by_name['CreateSignal']._serialized_options = b'\x92A\x0f\x12\rCreate signal\x82\xd3\xe4\x93\x02\x15"\x0b/v1/signals:\x06signal'
    _globals['_SIGNALSERVICE'].methods_by_name['UpdateSignal']._loaded_options = None
    _globals['_SIGNALSERVICE'].methods_by_name['UpdateSignal']._serialized_options = b'\x92A\x0f\x12\rUpdate signal\x82\xd3\xe4\x93\x02%2\x1b/v1/{signal.name=signals/*}:\x06signal'
    _globals['_SIGNALSERVICE'].methods_by_name['DeleteSignal']._loaded_options = None
    _globals['_SIGNALSERVICE'].methods_by_name['DeleteSignal']._serialized_options = b'\x92A\x0f\x12\rDelete signal\x82\xd3\xe4\x93\x02\x16*\x14/v1/{name=signals/*}'
    _globals['_SIGNALSERVICE'].methods_by_name['ListDerivedSignals']._loaded_options = None
    _globals['_SIGNALSERVICE'].methods_by_name['ListDerivedSignals']._serialized_options = b'\x92A\x16\x12\x14List derived signals\x82\xd3\xe4\x93\x02\x14\x12\x12/v1/derivedSignals'
    _globals['_SIGNALSERVICE'].methods_by_name['FilterDerivedSignals']._loaded_options = None
    _globals['_SIGNALSERVICE'].methods_by_name['FilterDerivedSignals']._serialized_options = b'\x92A\x18\x12\x16Filter derived signals\x82\xd3\xe4\x93\x02\x1b\x12\x19/v1/derivedSignals:filter'
    _globals['_SIGNALSERVICE'].methods_by_name['GetDerivedSignal']._loaded_options = None
    _globals['_SIGNALSERVICE'].methods_by_name['GetDerivedSignal']._serialized_options = b'\x92A\x14\x12\x12Get derived signal\x82\xd3\xe4\x93\x02\x1d\x12\x1b/v1/{name=derivedSignals/*}'
    _globals['_LISTSIGNALSREQUEST']._serialized_start = 279
    _globals['_LISTSIGNALSREQUEST']._serialized_end = 338
    _globals['_LISTSIGNALSRESPONSE']._serialized_start = 340
    _globals['_LISTSIGNALSRESPONSE']._serialized_end = 451
    _globals['_GETSIGNALREQUEST']._serialized_start = 453
    _globals['_GETSIGNALREQUEST']._serialized_end = 509
    _globals['_CREATESIGNALREQUEST']._serialized_start = 511
    _globals['_CREATESIGNALREQUEST']._serialized_end = 612
    _globals['_UPDATESIGNALREQUEST']._serialized_start = 615
    _globals['_UPDATESIGNALREQUEST']._serialized_end = 788
    _globals['_DELETESIGNALREQUEST']._serialized_start = 790
    _globals['_DELETESIGNALREQUEST']._serialized_end = 849
    _globals['_LISTDERIVEDSIGNALSREQUEST']._serialized_start = 851
    _globals['_LISTDERIVEDSIGNALSREQUEST']._serialized_end = 917
    _globals['_LISTDERIVEDSIGNALSRESPONSE']._serialized_start = 920
    _globals['_LISTDERIVEDSIGNALSRESPONSE']._serialized_end = 1053
    _globals['_FILTERDERIVEDSIGNALSREQUEST']._serialized_start = 1055
    _globals['_FILTERDERIVEDSIGNALSREQUEST']._serialized_end = 1106
    _globals['_FILTERDERIVEDSIGNALSRESPONSE']._serialized_start = 1109
    _globals['_FILTERDERIVEDSIGNALSRESPONSE']._serialized_end = 1325
    _globals['_FILTERDERIVEDSIGNALSRESPONSE_DERIVEDSIGNALSENTRY']._serialized_start = 1236
    _globals['_FILTERDERIVEDSIGNALSRESPONSE_DERIVEDSIGNALSENTRY']._serialized_end = 1325
    _globals['_GETDERIVEDSIGNALREQUEST']._serialized_start = 1327
    _globals['_GETDERIVEDSIGNALREQUEST']._serialized_end = 1397
    _globals['_SIGNALSERVICE']._serialized_start = 1400
    _globals['_SIGNALSERVICE']._serialized_end = 2603