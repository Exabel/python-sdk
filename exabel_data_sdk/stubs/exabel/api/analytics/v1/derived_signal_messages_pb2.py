"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from .....protoc_gen_openapiv2.options import annotations_pb2 as protoc__gen__openapiv2_dot_options_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n5exabel/api/analytics/v1/derived_signal_messages.proto\x12\x17exabel.api.analytics.v1\x1a\x1fgoogle/api/field_behavior.proto\x1a\x1egoogle/protobuf/wrappers.proto\x1a.protoc_gen_openapiv2/options/annotations.proto"\xcb\x02\n\rDerivedSignal\x12A\n\x04name\x18\x01 \x01(\tB3\xe0A\x05\x92A-J\x14"derivedSignals/123"\xca>\x14\xfa\x02\x11derivedSignalName\x12;\n\x05label\x18\x02 \x01(\tB,\x92A)J\x11"close_price_ma7"\x8a\x01\x13^[a-zA-Z_]\\w{0,99}$\x12:\n\nexpression\x18\x03 \x01(\tB&\x92A#J!"close_price().moving_average(7)"\x12<\n\x0bdescription\x18\x04 \x01(\tB\'\x92A$J""Close price 7 day moving average"\x12@\n\x08metadata\x18\x05 \x01(\x0b2..exabel.api.analytics.v1.DerivedSignalMetadata"\xbf\x01\n\x15DerivedSignalMetadata\x12-\n\x08decimals\x18\x01 \x01(\x0b2\x1b.google.protobuf.Int32Value\x128\n\x04unit\x18\x02 \x01(\x0e2*.exabel.api.analytics.v1.DerivedSignalUnit\x12=\n\x04type\x18\x03 \x01(\x0e2*.exabel.api.analytics.v1.DerivedSignalTypeB\x03\xe0A\x03*a\n\x11DerivedSignalUnit\x12\x1f\n\x1bDERIVED_SIGNAL_UNIT_INVALID\x10\x00\x12\n\n\x06NUMBER\x10\x01\x12\t\n\x05RATIO\x10\x02\x12\x14\n\x10RATIO_DIFFERENCE\x10\x03*\x9a\x01\n\x11DerivedSignalType\x12\x1f\n\x1bDERIVED_SIGNAL_TYPE_INVALID\x10\x00\x12\x12\n\x0eDERIVED_SIGNAL\x10\x01\x12\x18\n\x14FILE_UPLOADED_SIGNAL\x10\x02\x12 \n\x1cFILE_UPLOADED_COMPANY_SIGNAL\x10\x03\x12\x14\n\x10PERSISTED_SIGNAL\x10\x04BX\n\x1bcom.exabel.api.analytics.v1B\x1aDerivedSignalMessagesProtoP\x01Z\x1bexabel.com/api/analytics/v1b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'exabel.api.analytics.v1.derived_signal_messages_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n\x1bcom.exabel.api.analytics.v1B\x1aDerivedSignalMessagesProtoP\x01Z\x1bexabel.com/api/analytics/v1'
    _DERIVEDSIGNAL.fields_by_name['name']._options = None
    _DERIVEDSIGNAL.fields_by_name['name']._serialized_options = b'\xe0A\x05\x92A-J\x14"derivedSignals/123"\xca>\x14\xfa\x02\x11derivedSignalName'
    _DERIVEDSIGNAL.fields_by_name['label']._options = None
    _DERIVEDSIGNAL.fields_by_name['label']._serialized_options = b'\x92A)J\x11"close_price_ma7"\x8a\x01\x13^[a-zA-Z_]\\w{0,99}$'
    _DERIVEDSIGNAL.fields_by_name['expression']._options = None
    _DERIVEDSIGNAL.fields_by_name['expression']._serialized_options = b'\x92A#J!"close_price().moving_average(7)"'
    _DERIVEDSIGNAL.fields_by_name['description']._options = None
    _DERIVEDSIGNAL.fields_by_name['description']._serialized_options = b'\x92A$J""Close price 7 day moving average"'
    _DERIVEDSIGNALMETADATA.fields_by_name['type']._options = None
    _DERIVEDSIGNALMETADATA.fields_by_name['type']._serialized_options = b'\xe0A\x03'
    _DERIVEDSIGNALUNIT._serialized_start = 723
    _DERIVEDSIGNALUNIT._serialized_end = 820
    _DERIVEDSIGNALTYPE._serialized_start = 823
    _DERIVEDSIGNALTYPE._serialized_end = 977
    _DERIVEDSIGNAL._serialized_start = 196
    _DERIVEDSIGNAL._serialized_end = 527
    _DERIVEDSIGNALMETADATA._serialized_start = 530
    _DERIVEDSIGNALMETADATA._serialized_end = 721