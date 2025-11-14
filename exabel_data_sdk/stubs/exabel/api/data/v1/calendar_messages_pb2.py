"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'exabel/api/data/v1/calendar_messages.proto')
_sym_db = _symbol_database.Default()
from .....exabel.api.time import date_pb2 as exabel_dot_api_dot_time_dot_date__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n*exabel/api/data/v1/calendar_messages.proto\x12\x12exabel.api.data.v1\x1a\x1aexabel/api/time/date.proto"i\n\x0cFiscalPeriod\x120\n\tfrequency\x18\x01 \x01(\x0e2\x1d.exabel.api.data.v1.Frequency\x12\'\n\x08end_date\x18\x02 \x01(\x0b2\x15.exabel.api.time.Date*Q\n\tFrequency\x12\x19\n\x15FREQUENCY_UNSPECIFIED\x10\x00\x12\r\n\tQUARTERLY\x10\x01\x12\x0e\n\nSEMIANNUAL\x10\x02\x12\n\n\x06ANNUAL\x10\x03BI\n\x16com.exabel.api.data.v1B\x15CalendarMessagesProtoP\x01Z\x16exabel.com/api/data/v1b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'exabel.api.data.v1.calendar_messages_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'\n\x16com.exabel.api.data.v1B\x15CalendarMessagesProtoP\x01Z\x16exabel.com/api/data/v1'
    _globals['_FREQUENCY']._serialized_start = 201
    _globals['_FREQUENCY']._serialized_end = 282
    _globals['_FISCALPERIOD']._serialized_start = 94
    _globals['_FISCALPERIOD']._serialized_end = 199