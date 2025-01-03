"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 28, 1, '', 'exabel/api/analytics/v1/derived_signal_messages.proto')
_sym_db = _symbol_database.Default()
from .....exabel.api.data.v1 import common_messages_pb2 as exabel_dot_api_dot_data_dot_v1_dot_common__messages__pb2
from .....exabel.api.math import aggregation_pb2 as exabel_dot_api_dot_math_dot_aggregation__pb2
from .....exabel.api.math import change_pb2 as exabel_dot_api_dot_math_dot_change__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from .....protoc_gen_openapiv2.options import annotations_pb2 as protoc__gen__openapiv2_dot_options_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n5exabel/api/analytics/v1/derived_signal_messages.proto\x12\x17exabel.api.analytics.v1\x1a(exabel/api/data/v1/common_messages.proto\x1a!exabel/api/math/aggregation.proto\x1a\x1cexabel/api/math/change.proto\x1a\x1fgoogle/api/field_behavior.proto\x1a\x1egoogle/protobuf/wrappers.proto\x1a.protoc_gen_openapiv2/options/annotations.proto"\xe1\x02\n\rDerivedSignal\x12A\n\x04name\x18\x01 \x01(\tB3\x92A-J\x14"derivedSignals/123"\xca>\x14\xfa\x02\x11derivedSignalName\xe0A\x05\x12;\n\x05label\x18\x02 \x01(\tB,\x92A)J\x11"close_price_ma7"\x8a\x01\x13^[a-zA-Z_]\\w{0,99}$\x12:\n\nexpression\x18\x03 \x01(\tB&\x92A#J!"close_price().moving_average(7)"\x12<\n\x0bdescription\x18\x04 \x01(\tB\'\x92A$J""Close price 7 day moving average"\x12\x14\n\x0cdisplay_name\x18\x06 \x01(\t\x12@\n\x08metadata\x18\x05 \x01(\x0b2..exabel.api.analytics.v1.DerivedSignalMetadata"\xd6\x02\n\x15DerivedSignalMetadata\x12-\n\x08decimals\x18\x01 \x01(\x0b2\x1b.google.protobuf.Int32Value\x128\n\x04unit\x18\x02 \x01(\x0e2*.exabel.api.analytics.v1.DerivedSignalUnit\x12=\n\x04type\x18\x03 \x01(\x0e2*.exabel.api.analytics.v1.DerivedSignalTypeB\x03\xe0A\x03\x129\n\x13downsampling_method\x18\x04 \x01(\x0e2\x1c.exabel.api.math.Aggregation\x12\'\n\x06change\x18\x05 \x01(\x0e2\x17.exabel.api.math.Change\x121\n\nentity_set\x18\x06 \x01(\x0b2\x1d.exabel.api.data.v1.EntitySet*a\n\x11DerivedSignalUnit\x12\x1f\n\x1bDERIVED_SIGNAL_UNIT_INVALID\x10\x00\x12\n\n\x06NUMBER\x10\x01\x12\t\n\x05RATIO\x10\x02\x12\x14\n\x10RATIO_DIFFERENCE\x10\x03*\x9a\x01\n\x11DerivedSignalType\x12\x1f\n\x1bDERIVED_SIGNAL_TYPE_INVALID\x10\x00\x12\x12\n\x0eDERIVED_SIGNAL\x10\x01\x12\x18\n\x14FILE_UPLOADED_SIGNAL\x10\x02\x12 \n\x1cFILE_UPLOADED_COMPANY_SIGNAL\x10\x03\x12\x14\n\x10PERSISTED_SIGNAL\x10\x04BX\n\x1bcom.exabel.api.analytics.v1B\x1aDerivedSignalMessagesProtoP\x01Z\x1bexabel.com/api/analytics/v1b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'exabel.api.analytics.v1.derived_signal_messages_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'\n\x1bcom.exabel.api.analytics.v1B\x1aDerivedSignalMessagesProtoP\x01Z\x1bexabel.com/api/analytics/v1'
    _globals['_DERIVEDSIGNAL'].fields_by_name['name']._loaded_options = None
    _globals['_DERIVEDSIGNAL'].fields_by_name['name']._serialized_options = b'\x92A-J\x14"derivedSignals/123"\xca>\x14\xfa\x02\x11derivedSignalName\xe0A\x05'
    _globals['_DERIVEDSIGNAL'].fields_by_name['label']._loaded_options = None
    _globals['_DERIVEDSIGNAL'].fields_by_name['label']._serialized_options = b'\x92A)J\x11"close_price_ma7"\x8a\x01\x13^[a-zA-Z_]\\w{0,99}$'
    _globals['_DERIVEDSIGNAL'].fields_by_name['expression']._loaded_options = None
    _globals['_DERIVEDSIGNAL'].fields_by_name['expression']._serialized_options = b'\x92A#J!"close_price().moving_average(7)"'
    _globals['_DERIVEDSIGNAL'].fields_by_name['description']._loaded_options = None
    _globals['_DERIVEDSIGNAL'].fields_by_name['description']._serialized_options = b'\x92A$J""Close price 7 day moving average"'
    _globals['_DERIVEDSIGNALMETADATA'].fields_by_name['type']._loaded_options = None
    _globals['_DERIVEDSIGNALMETADATA'].fields_by_name['type']._serialized_options = b'\xe0A\x03'
    _globals['_DERIVEDSIGNALUNIT']._serialized_start = 1003
    _globals['_DERIVEDSIGNALUNIT']._serialized_end = 1100
    _globals['_DERIVEDSIGNALTYPE']._serialized_start = 1103
    _globals['_DERIVEDSIGNALTYPE']._serialized_end = 1257
    _globals['_DERIVEDSIGNAL']._serialized_start = 303
    _globals['_DERIVEDSIGNAL']._serialized_end = 656
    _globals['_DERIVEDSIGNALMETADATA']._serialized_start = 659
    _globals['_DERIVEDSIGNALMETADATA']._serialized_end = 1001