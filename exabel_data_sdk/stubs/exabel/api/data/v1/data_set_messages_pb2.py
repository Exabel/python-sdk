"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 28, 1, '', 'exabel/api/data/v1/data_set_messages.proto')
_sym_db = _symbol_database.Default()
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from .....protoc_gen_openapiv2.options import annotations_pb2 as protoc__gen__openapiv2_dot_options_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n*exabel/api/data/v1/data_set_messages.proto\x12\x12exabel.api.data.v1\x1a\x1fgoogle/api/field_behavior.proto\x1a.protoc_gen_openapiv2/options/annotations.proto"\xde\x03\n\x07DataSet\x12>\n\x04name\x18\x01 \x01(\tB0\x92A\'J\x14"dataSets/ns.stores"\xca>\x0e\xfa\x02\x0bdataSetName\xe0A\x05\xe0A\x02\x12\x18\n\x0blegacy_name\x18\x08 \x01(\tB\x03\xe0A\x03\x12#\n\x0cdisplay_name\x18\x02 \x01(\tB\r\x92A\nJ\x08"Stores"\x12>\n\x0bdescription\x18\x03 \x01(\tB)\x92A&J$"The data set of all store entities"\x12N\n\x07signals\x18\x04 \x03(\tB=\x92A7J5["signals/ns.customer_amount", "signals/ns.visitors"]\xe0A\x06\x12J\n\x0fderived_signals\x18\x07 \x03(\tB1\x92A.J,["derivedSignals/321", "derivedSignals/432"]\x12V\n\x13highlighted_signals\x18\x06 \x03(\tB9\x92A3J1["signals/ns.average_data", "derivedSignals/321"]\xe0A\x06\x12 \n\tread_only\x18\x05 \x01(\x08B\r\x92A\x07J\x05false\xe0A\x03BH\n\x16com.exabel.api.data.v1B\x14DataSetMessagesProtoP\x01Z\x16exabel.com/api/data/v1b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'exabel.api.data.v1.data_set_messages_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'\n\x16com.exabel.api.data.v1B\x14DataSetMessagesProtoP\x01Z\x16exabel.com/api/data/v1'
    _globals['_DATASET'].fields_by_name['name']._loaded_options = None
    _globals['_DATASET'].fields_by_name['name']._serialized_options = b'\x92A\'J\x14"dataSets/ns.stores"\xca>\x0e\xfa\x02\x0bdataSetName\xe0A\x05\xe0A\x02'
    _globals['_DATASET'].fields_by_name['legacy_name']._loaded_options = None
    _globals['_DATASET'].fields_by_name['legacy_name']._serialized_options = b'\xe0A\x03'
    _globals['_DATASET'].fields_by_name['display_name']._loaded_options = None
    _globals['_DATASET'].fields_by_name['display_name']._serialized_options = b'\x92A\nJ\x08"Stores"'
    _globals['_DATASET'].fields_by_name['description']._loaded_options = None
    _globals['_DATASET'].fields_by_name['description']._serialized_options = b'\x92A&J$"The data set of all store entities"'
    _globals['_DATASET'].fields_by_name['signals']._loaded_options = None
    _globals['_DATASET'].fields_by_name['signals']._serialized_options = b'\x92A7J5["signals/ns.customer_amount", "signals/ns.visitors"]\xe0A\x06'
    _globals['_DATASET'].fields_by_name['derived_signals']._loaded_options = None
    _globals['_DATASET'].fields_by_name['derived_signals']._serialized_options = b'\x92A.J,["derivedSignals/321", "derivedSignals/432"]'
    _globals['_DATASET'].fields_by_name['highlighted_signals']._loaded_options = None
    _globals['_DATASET'].fields_by_name['highlighted_signals']._serialized_options = b'\x92A3J1["signals/ns.average_data", "derivedSignals/321"]\xe0A\x06'
    _globals['_DATASET'].fields_by_name['read_only']._loaded_options = None
    _globals['_DATASET'].fields_by_name['read_only']._serialized_options = b'\x92A\x07J\x05false\xe0A\x03'
    _globals['_DATASET']._serialized_start = 148
    _globals['_DATASET']._serialized_end = 626