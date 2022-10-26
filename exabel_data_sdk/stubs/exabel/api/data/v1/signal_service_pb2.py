"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from .....exabel.api.data.v1 import signal_messages_pb2 as exabel_dot_api_dot_data_dot_v1_dot_signal__messages__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from .....protoc_gen_openapiv2.options import annotations_pb2 as protoc__gen__openapiv2_dot_options_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\'exabel/api/data/v1/signal_service.proto\x12\x12exabel.api.data.v1\x1a(exabel/api/data/v1/signal_messages.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x1fgoogle/api/field_behavior.proto\x1a\x1bgoogle/protobuf/empty.proto\x1a google/protobuf/field_mask.proto\x1a.protoc_gen_openapiv2/options/annotations.proto";\n\x12ListSignalsRequest\x12\x11\n\tpage_size\x18\x01 \x01(\x05\x12\x12\n\npage_token\x18\x02 \x01(\t"o\n\x13ListSignalsResponse\x12+\n\x07signals\x18\x01 \x03(\x0b2\x1a.exabel.api.data.v1.Signal\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\x12\x12\n\ntotal_size\x18\x03 \x01(\x05"8\n\x10GetSignalRequest\x12$\n\x04name\x18\x01 \x01(\tB\x16\xe0A\x02\x92A\x10\xca>\r\xfa\x02\nsignalName"e\n\x13CreateSignalRequest\x12/\n\x06signal\x18\x01 \x01(\x0b2\x1a.exabel.api.data.v1.SignalB\x03\xe0A\x02\x12\x1d\n\x15create_library_signal\x18\x02 \x01(\x08"\xad\x01\n\x13UpdateSignalRequest\x12/\n\x06signal\x18\x01 \x01(\x0b2\x1a.exabel.api.data.v1.SignalB\x03\xe0A\x02\x12/\n\x0bupdate_mask\x18\x02 \x01(\x0b2\x1a.google.protobuf.FieldMask\x12\x15\n\rallow_missing\x18\x03 \x01(\x08\x12\x1d\n\x15create_library_signal\x18\x04 \x01(\x08";\n\x13DeleteSignalRequest\x12$\n\x04name\x18\x01 \x01(\tB\x16\xe0A\x02\x92A\x10\xca>\r\xfa\x02\nsignalName2\xad\x05\n\rSignalService\x12\x84\x01\n\x0bListSignals\x12&.exabel.api.data.v1.ListSignalsRequest\x1a\'.exabel.api.data.v1.ListSignalsResponse"$\x82\xd3\xe4\x93\x02\r\x12\x0b/v1/signals\x92A\x0e\x12\x0cList signals\x12z\n\tGetSignal\x12$.exabel.api.data.v1.GetSignalRequest\x1a\x1a.exabel.api.data.v1.Signal"+\x82\xd3\xe4\x93\x02\x16\x12\x14/v1/{name=signals/*}\x92A\x0c\x12\nGet signal\x12\x82\x01\n\x0cCreateSignal\x12\'.exabel.api.data.v1.CreateSignalRequest\x1a\x1a.exabel.api.data.v1.Signal"-\x82\xd3\xe4\x93\x02\x15"\x0b/v1/signals:\x06signal\x92A\x0f\x12\rCreate signal\x12\x92\x01\n\x0cUpdateSignal\x12\'.exabel.api.data.v1.UpdateSignalRequest\x1a\x1a.exabel.api.data.v1.Signal"=\x82\xd3\xe4\x93\x02%2\x1b/v1/{signal.name=signals/*}:\x06signal\x92A\x0f\x12\rUpdate signal\x12\x7f\n\x0cDeleteSignal\x12\'.exabel.api.data.v1.DeleteSignalRequest\x1a\x16.google.protobuf.Empty".\x82\xd3\xe4\x93\x02\x16*\x14/v1/{name=signals/*}\x92A\x0f\x12\rDelete signalBF\n\x16com.exabel.api.data.v1B\x12SignalServiceProtoP\x01Z\x16exabel.com/api/data/v1b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'exabel.api.data.v1.signal_service_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n\x16com.exabel.api.data.v1B\x12SignalServiceProtoP\x01Z\x16exabel.com/api/data/v1'
    _GETSIGNALREQUEST.fields_by_name['name']._options = None
    _GETSIGNALREQUEST.fields_by_name['name']._serialized_options = b'\xe0A\x02\x92A\x10\xca>\r\xfa\x02\nsignalName'
    _CREATESIGNALREQUEST.fields_by_name['signal']._options = None
    _CREATESIGNALREQUEST.fields_by_name['signal']._serialized_options = b'\xe0A\x02'
    _UPDATESIGNALREQUEST.fields_by_name['signal']._options = None
    _UPDATESIGNALREQUEST.fields_by_name['signal']._serialized_options = b'\xe0A\x02'
    _DELETESIGNALREQUEST.fields_by_name['name']._options = None
    _DELETESIGNALREQUEST.fields_by_name['name']._serialized_options = b'\xe0A\x02\x92A\x10\xca>\r\xfa\x02\nsignalName'
    _SIGNALSERVICE.methods_by_name['ListSignals']._options = None
    _SIGNALSERVICE.methods_by_name['ListSignals']._serialized_options = b'\x82\xd3\xe4\x93\x02\r\x12\x0b/v1/signals\x92A\x0e\x12\x0cList signals'
    _SIGNALSERVICE.methods_by_name['GetSignal']._options = None
    _SIGNALSERVICE.methods_by_name['GetSignal']._serialized_options = b'\x82\xd3\xe4\x93\x02\x16\x12\x14/v1/{name=signals/*}\x92A\x0c\x12\nGet signal'
    _SIGNALSERVICE.methods_by_name['CreateSignal']._options = None
    _SIGNALSERVICE.methods_by_name['CreateSignal']._serialized_options = b'\x82\xd3\xe4\x93\x02\x15"\x0b/v1/signals:\x06signal\x92A\x0f\x12\rCreate signal'
    _SIGNALSERVICE.methods_by_name['UpdateSignal']._options = None
    _SIGNALSERVICE.methods_by_name['UpdateSignal']._serialized_options = b'\x82\xd3\xe4\x93\x02%2\x1b/v1/{signal.name=signals/*}:\x06signal\x92A\x0f\x12\rUpdate signal'
    _SIGNALSERVICE.methods_by_name['DeleteSignal']._options = None
    _SIGNALSERVICE.methods_by_name['DeleteSignal']._serialized_options = b'\x82\xd3\xe4\x93\x02\x16*\x14/v1/{name=signals/*}\x92A\x0f\x12\rDelete signal'
    _LISTSIGNALSREQUEST._serialized_start = 279
    _LISTSIGNALSREQUEST._serialized_end = 338
    _LISTSIGNALSRESPONSE._serialized_start = 340
    _LISTSIGNALSRESPONSE._serialized_end = 451
    _GETSIGNALREQUEST._serialized_start = 453
    _GETSIGNALREQUEST._serialized_end = 509
    _CREATESIGNALREQUEST._serialized_start = 511
    _CREATESIGNALREQUEST._serialized_end = 612
    _UPDATESIGNALREQUEST._serialized_start = 615
    _UPDATESIGNALREQUEST._serialized_end = 788
    _DELETESIGNALREQUEST._serialized_start = 790
    _DELETESIGNALREQUEST._serialized_end = 849
    _SIGNALSERVICE._serialized_start = 852
    _SIGNALSERVICE._serialized_end = 1537