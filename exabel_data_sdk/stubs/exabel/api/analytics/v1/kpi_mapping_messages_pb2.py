"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'exabel/api/analytics/v1/kpi_mapping_messages.proto')
_sym_db = _symbol_database.Default()
from .....exabel.api.analytics.v1 import common_messages_pb2 as exabel_dot_api_dot_analytics_dot_v1_dot_common__messages__pb2
from .....exabel.api.analytics.v1 import derived_signal_messages_pb2 as exabel_dot_api_dot_analytics_dot_v1_dot_derived__signal__messages__pb2
from .....exabel.api.analytics.v1 import kpi_messages_pb2 as exabel_dot_api_dot_analytics_dot_v1_dot_kpi__messages__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from .....protoc_gen_openapiv2.options import annotations_pb2 as protoc__gen__openapiv2_dot_options_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n2exabel/api/analytics/v1/kpi_mapping_messages.proto\x12\x17exabel.api.analytics.v1\x1a-exabel/api/analytics/v1/common_messages.proto\x1a5exabel/api/analytics/v1/derived_signal_messages.proto\x1a*exabel/api/analytics/v1/kpi_messages.proto\x1a\x1fgoogle/api/field_behavior.proto\x1a.protoc_gen_openapiv2/options/annotations.proto"\x9c\x03\n\x0fKpiMappingGroup\x12I\n\x04name\x18\x01 \x01(\tB;\x92A5J\x1a"kpiMappings/123/groups/4"\xca>\x16\xfa\x02\x13kpiMappingGroupName\xe0A\x05\x12\x14\n\x0cdisplay_name\x18\x02 \x01(\t\x12)\n\x03kpi\x18\x03 \x01(\x0b2\x1c.exabel.api.analytics.v1.Kpi\x12<\n\x0cproxy_signal\x18\x04 \x01(\x0b2&.exabel.api.analytics.v1.DerivedSignal\x12?\n\x04type\x18\x05 \x01(\x0e2,.exabel.api.analytics.v1.KpiMappingGroupTypeB\x03\xe0A\x05\x126\n\nentity_set\x18\x06 \x01(\x0b2".exabel.api.analytics.v1.EntitySet\x12F\n\x15proxy_resample_method\x18\x07 \x01(\x0e2\'.exabel.api.analytics.v1.ResampleMethod*]\n\x13KpiMappingGroupType\x12&\n"KPI_MAPPING_GROUP_TYPE_UNSPECIFIED\x10\x00\x12\x08\n\x04BULK\x10\x01\x12\x14\n\x10COMPANY_SPECIFIC\x10\x02*\xad\x01\n\x0eResampleMethod\x12\x1f\n\x1bRESAMPLE_METHOD_UNSPECIFIED\x10\x00\x12\x0f\n\x0bNO_RESAMPLE\x10\x01\x12\x11\n\rRESAMPLE_MEAN\x10\x02\x12\x10\n\x0cRESAMPLE_SUM\x10\x03\x12\x13\n\x0fRESAMPLE_MEDIAN\x10\x04\x12\x1c\n\x18RESAMPLE_MEAN_TIMES_DAYS\x10\x05\x12\x11\n\rRESAMPLE_LAST\x10\x06BZ\n\x1bcom.exabel.api.analytics.v1B\x1cKpiMappingGroupMessagesProtoP\x01Z\x1bexabel.com/api/analytics/v1b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'exabel.api.analytics.v1.kpi_mapping_messages_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'\n\x1bcom.exabel.api.analytics.v1B\x1cKpiMappingGroupMessagesProtoP\x01Z\x1bexabel.com/api/analytics/v1'
    _globals['_KPIMAPPINGGROUP'].fields_by_name['name']._loaded_options = None
    _globals['_KPIMAPPINGGROUP'].fields_by_name['name']._serialized_options = b'\x92A5J\x1a"kpiMappings/123/groups/4"\xca>\x16\xfa\x02\x13kpiMappingGroupName\xe0A\x05'
    _globals['_KPIMAPPINGGROUP'].fields_by_name['type']._loaded_options = None
    _globals['_KPIMAPPINGGROUP'].fields_by_name['type']._serialized_options = b'\xe0A\x05'
    _globals['_KPIMAPPINGGROUPTYPE']._serialized_start = 721
    _globals['_KPIMAPPINGGROUPTYPE']._serialized_end = 814
    _globals['_RESAMPLEMETHOD']._serialized_start = 817
    _globals['_RESAMPLEMETHOD']._serialized_end = 990
    _globals['_KPIMAPPINGGROUP']._serialized_start = 307
    _globals['_KPIMAPPINGGROUP']._serialized_end = 719