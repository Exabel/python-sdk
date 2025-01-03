"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 28, 1, '', 'exabel/api/data/v1/signal_messages.proto')
_sym_db = _symbol_database.Default()
from .....exabel.api.data.v1 import common_messages_pb2 as exabel_dot_api_dot_data_dot_v1_dot_common__messages__pb2
from .....exabel.api.math import aggregation_pb2 as exabel_dot_api_dot_math_dot_aggregation__pb2
from .....exabel.api.math import change_pb2 as exabel_dot_api_dot_math_dot_change__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from .....protoc_gen_openapiv2.options import annotations_pb2 as protoc__gen__openapiv2_dot_options_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n(exabel/api/data/v1/signal_messages.proto\x12\x12exabel.api.data.v1\x1a(exabel/api/data/v1/common_messages.proto\x1a!exabel/api/math/aggregation.proto\x1a\x1cexabel/api/math/change.proto\x1a\x1fgoogle/api/field_behavior.proto\x1a.protoc_gen_openapiv2/options/annotations.proto"\xdb\x02\n\x06Signal\x12<\n\x04name\x18\x01 \x01(\tB.\x92A%J\x13"signals/ns.signal"\xca>\r\xfa\x02\nsignalName\xe0A\x05\xe0A\x02\x12\x17\n\x0bentity_type\x18\x02 \x01(\tB\x02\x18\x01\x12&\n\x0cdisplay_name\x18\x03 \x01(\tB\x10\x92A\rJ\x0b"My signal"\x12/\n\x0bdescription\x18\x04 \x01(\tB\x1a\x92A\x17J\x15"Describes my signal"\x129\n\x13downsampling_method\x18\x05 \x01(\x0e2\x1c.exabel.api.math.Aggregation\x12\x16\n\tread_only\x18\x06 \x01(\x08B\x03\xe0A\x03\x12N\n\x0centity_types\x18\x07 \x03(\tB8\x92A2J0["entityTypes/ns.type1", "entityTypes/ns.type2"]\xe0A\x03"\xc7\x03\n\rDerivedSignal\x12D\n\x04name\x18\x01 \x01(\tB6\x92A-J\x14"derivedSignals/321"\xca>\x14\xfa\x02\x11derivedSignalName\xe0A\x05\xe0A\x02\x12\x16\n\tdata_sets\x18\x02 \x03(\tB\x03\xe0A\x03\x12)\n\x0cdisplay_name\x18\x03 \x01(\tB\x13\x92A\rJ\x0b"My signal"\xe0A\x03\x12*\n\x05label\x18\n \x01(\tB\x1b\x92A\x15J\x13"signal_expression"\xe0A\x03\x122\n\x0bdescription\x18\x04 \x01(\tB\x1d\x92A\x17J\x15"Describes my signal"\xe0A\x03\x12\x12\n\nexpression\x18\t \x01(\t\x12>\n\x13downsampling_method\x18\x05 \x01(\x0e2\x1c.exabel.api.math.AggregationB\x03\xe0A\x03\x12,\n\x06change\x18\x06 \x01(\x0e2\x17.exabel.api.math.ChangeB\x03\xe0A\x03\x126\n\nentity_set\x18\x07 \x01(\x0b2\x1d.exabel.api.data.v1.EntitySetB\x03\xe0A\x03\x12\x13\n\x0bhighlighted\x18\x08 \x01(\x08"L\n\x0eDerivedSignals\x12:\n\x0fderived_signals\x18\x01 \x03(\x0b2!.exabel.api.data.v1.DerivedSignalBG\n\x16com.exabel.api.data.v1B\x13SignalMessagesProtoP\x01Z\x16exabel.com/api/data/v1b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'exabel.api.data.v1.signal_messages_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'\n\x16com.exabel.api.data.v1B\x13SignalMessagesProtoP\x01Z\x16exabel.com/api/data/v1'
    _globals['_SIGNAL'].fields_by_name['name']._loaded_options = None
    _globals['_SIGNAL'].fields_by_name['name']._serialized_options = b'\x92A%J\x13"signals/ns.signal"\xca>\r\xfa\x02\nsignalName\xe0A\x05\xe0A\x02'
    _globals['_SIGNAL'].fields_by_name['entity_type']._loaded_options = None
    _globals['_SIGNAL'].fields_by_name['entity_type']._serialized_options = b'\x18\x01'
    _globals['_SIGNAL'].fields_by_name['display_name']._loaded_options = None
    _globals['_SIGNAL'].fields_by_name['display_name']._serialized_options = b'\x92A\rJ\x0b"My signal"'
    _globals['_SIGNAL'].fields_by_name['description']._loaded_options = None
    _globals['_SIGNAL'].fields_by_name['description']._serialized_options = b'\x92A\x17J\x15"Describes my signal"'
    _globals['_SIGNAL'].fields_by_name['read_only']._loaded_options = None
    _globals['_SIGNAL'].fields_by_name['read_only']._serialized_options = b'\xe0A\x03'
    _globals['_SIGNAL'].fields_by_name['entity_types']._loaded_options = None
    _globals['_SIGNAL'].fields_by_name['entity_types']._serialized_options = b'\x92A2J0["entityTypes/ns.type1", "entityTypes/ns.type2"]\xe0A\x03'
    _globals['_DERIVEDSIGNAL'].fields_by_name['name']._loaded_options = None
    _globals['_DERIVEDSIGNAL'].fields_by_name['name']._serialized_options = b'\x92A-J\x14"derivedSignals/321"\xca>\x14\xfa\x02\x11derivedSignalName\xe0A\x05\xe0A\x02'
    _globals['_DERIVEDSIGNAL'].fields_by_name['data_sets']._loaded_options = None
    _globals['_DERIVEDSIGNAL'].fields_by_name['data_sets']._serialized_options = b'\xe0A\x03'
    _globals['_DERIVEDSIGNAL'].fields_by_name['display_name']._loaded_options = None
    _globals['_DERIVEDSIGNAL'].fields_by_name['display_name']._serialized_options = b'\x92A\rJ\x0b"My signal"\xe0A\x03'
    _globals['_DERIVEDSIGNAL'].fields_by_name['label']._loaded_options = None
    _globals['_DERIVEDSIGNAL'].fields_by_name['label']._serialized_options = b'\x92A\x15J\x13"signal_expression"\xe0A\x03'
    _globals['_DERIVEDSIGNAL'].fields_by_name['description']._loaded_options = None
    _globals['_DERIVEDSIGNAL'].fields_by_name['description']._serialized_options = b'\x92A\x17J\x15"Describes my signal"\xe0A\x03'
    _globals['_DERIVEDSIGNAL'].fields_by_name['downsampling_method']._loaded_options = None
    _globals['_DERIVEDSIGNAL'].fields_by_name['downsampling_method']._serialized_options = b'\xe0A\x03'
    _globals['_DERIVEDSIGNAL'].fields_by_name['change']._loaded_options = None
    _globals['_DERIVEDSIGNAL'].fields_by_name['change']._serialized_options = b'\xe0A\x03'
    _globals['_DERIVEDSIGNAL'].fields_by_name['entity_set']._loaded_options = None
    _globals['_DERIVEDSIGNAL'].fields_by_name['entity_set']._serialized_options = b'\xe0A\x03'
    _globals['_SIGNAL']._serialized_start = 253
    _globals['_SIGNAL']._serialized_end = 600
    _globals['_DERIVEDSIGNAL']._serialized_start = 603
    _globals['_DERIVEDSIGNAL']._serialized_end = 1058
    _globals['_DERIVEDSIGNALS']._serialized_start = 1060
    _globals['_DERIVEDSIGNALS']._serialized_end = 1136