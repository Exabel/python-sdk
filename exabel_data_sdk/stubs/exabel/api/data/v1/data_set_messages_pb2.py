"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from .....protoc_gen_openapiv2.options import annotations_pb2 as protoc__gen__openapiv2_dot_options_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n*exabel/api/data/v1/data_set_messages.proto\x12\x12exabel.api.data.v1\x1a\x1fgoogle/api/field_behavior.proto\x1a.protoc_gen_openapiv2/options/annotations.proto"\xa0\x02\n\x07DataSet\x12>\n\x04name\x18\x01 \x01(\tB0\xe0A\x05\xe0A\x02\x92A\'J\x14"dataSets/ns.stores"\xca>\x0e\xfa\x02\x0bdataSetName\x12#\n\x0cdisplay_name\x18\x02 \x01(\tB\r\x92A\nJ\x08"Stores"\x12>\n\x0bdescription\x18\x03 \x01(\tB)\x92A&J$"The data set of all store entities"\x12N\n\x07signals\x18\x04 \x03(\tB=\xe0A\x06\x92A7J5["signals/ns.customer_amount", "signals/ns.visitors"]\x12 \n\tread_only\x18\x05 \x01(\x08B\r\xe0A\x03\x92A\x07J\x05falseBH\n\x16com.exabel.api.data.v1B\x14DataSetMessagesProtoP\x01Z\x16exabel.com/api/data/v1b\x06proto3')
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'exabel.api.data.v1.data_set_messages_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    DESCRIPTOR._serialized_options = b'\n\x16com.exabel.api.data.v1B\x14DataSetMessagesProtoP\x01Z\x16exabel.com/api/data/v1'
    _DATASET.fields_by_name['name']._options = None
    _DATASET.fields_by_name['name']._serialized_options = b'\xe0A\x05\xe0A\x02\x92A\'J\x14"dataSets/ns.stores"\xca>\x0e\xfa\x02\x0bdataSetName'
    _DATASET.fields_by_name['display_name']._options = None
    _DATASET.fields_by_name['display_name']._serialized_options = b'\x92A\nJ\x08"Stores"'
    _DATASET.fields_by_name['description']._options = None
    _DATASET.fields_by_name['description']._serialized_options = b'\x92A&J$"The data set of all store entities"'
    _DATASET.fields_by_name['signals']._options = None
    _DATASET.fields_by_name['signals']._serialized_options = b'\xe0A\x06\x92A7J5["signals/ns.customer_amount", "signals/ns.visitors"]'
    _DATASET.fields_by_name['read_only']._options = None
    _DATASET.fields_by_name['read_only']._serialized_options = b'\xe0A\x03\x92A\x07J\x05false'
    _DATASET._serialized_start = 148
    _DATASET._serialized_end = 436