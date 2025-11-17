"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'exabel/api/analytics/v1/kpi_mapping_service.proto')
_sym_db = _symbol_database.Default()
from .....exabel.api.analytics.v1 import kpi_mapping_messages_pb2 as exabel_dot_api_dot_analytics_dot_v1_dot_kpi__mapping__messages__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from .....protoc_gen_openapiv2.options import annotations_pb2 as protoc__gen__openapiv2_dot_options_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n1exabel/api/analytics/v1/kpi_mapping_service.proto\x12\x17exabel.api.analytics.v1\x1a2exabel/api/analytics/v1/kpi_mapping_messages.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x1fgoogle/api/field_behavior.proto\x1a google/protobuf/field_mask.proto\x1a.protoc_gen_openapiv2/options/annotations.proto"\x94\x01\n\x1cCreateKpiMappingGroupRequest\x12*\n\x06parent\x18\x01 \x01(\tB\x1a\x92A\x14\xca>\x11\xfa\x02\x0ekpiMappingName\xe0A\x02\x12H\n\x11kpi_mapping_group\x18\x02 \x01(\x0b2(.exabel.api.analytics.v1.KpiMappingGroupB\x03\xe0A\x02"J\n\x19GetKpiMappingGroupRequest\x12-\n\x04name\x18\x01 \x01(\tB\x1f\x92A\x19\xca>\x16\xfa\x02\x13kpiMappingGroupName\xe0A\x02"\xcd\x01\n\x1bListKpiMappingGroupsRequest\x12*\n\x06parent\x18\x01 \x01(\tB\x1a\x92A\x14\xca>\x11\xfa\x02\x0ekpiMappingName\xe0A\x02\x12:\n\x04type\x18\x02 \x01(\x0e2,.exabel.api.analytics.v1.KpiMappingGroupType\x12\x11\n\tcompanies\x18\x03 \x03(\t\x12\x11\n\tpage_size\x18\x04 \x01(\x05\x12\x12\n\npage_token\x18\x05 \x01(\t\x12\x0c\n\x04skip\x18\x06 \x01(\x05"\x85\x01\n\x1cListKpiMappingGroupsResponse\x128\n\x06groups\x18\x01 \x03(\x0b2(.exabel.api.analytics.v1.KpiMappingGroup\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\x12\x12\n\ntotal_size\x18\x03 \x01(\x05"\x99\x01\n\x1cUpdateKpiMappingGroupRequest\x12H\n\x11kpi_mapping_group\x18\x01 \x01(\x0b2(.exabel.api.analytics.v1.KpiMappingGroupB\x03\xe0A\x02\x12/\n\x0bupdate_mask\x18\x02 \x01(\x0b2\x1a.google.protobuf.FieldMask2\xd8\x06\n\x11KpiMappingService\x12\xd3\x01\n\x15CreateKpiMappingGroup\x125.exabel.api.analytics.v1.CreateKpiMappingGroupRequest\x1a(.exabel.api.analytics.v1.KpiMappingGroup"Y\x92A\x1a\x12\x18Create KPI mapping group\x82\xd3\xe4\x93\x026"!/v1/{parent=kpiMappings/*}/groups:\x11kpi_mapping_group\x12\xb7\x01\n\x12GetKpiMappingGroup\x122.exabel.api.analytics.v1.GetKpiMappingGroupRequest\x1a(.exabel.api.analytics.v1.KpiMappingGroup"C\x92A\x17\x12\x15Get KPI mapping group\x82\xd3\xe4\x93\x02#\x12!/v1/{name=kpiMappings/*/groups/*}\x12\xca\x01\n\x14ListKpiMappingGroups\x124.exabel.api.analytics.v1.ListKpiMappingGroupsRequest\x1a5.exabel.api.analytics.v1.ListKpiMappingGroupsResponse"E\x92A\x19\x12\x17List KPI mapping groups\x82\xd3\xe4\x93\x02#\x12!/v1/{parent=kpiMappings/*}/groups\x12\xe5\x01\n\x15UpdateKpiMappingGroup\x125.exabel.api.analytics.v1.UpdateKpiMappingGroupRequest\x1a(.exabel.api.analytics.v1.KpiMappingGroup"k\x92A\x1a\x12\x18Update KPI mapping group\x82\xd3\xe4\x93\x02H23/v1/{kpi_mapping_group.name=kpiMappings/*/groups/*}:\x11kpi_mapping_groupBY\n\x1bcom.exabel.api.analytics.v1B\x1bKpiMappingGroupServiceProtoP\x01Z\x1bexabel.com/api/analytics/v1b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'exabel.api.analytics.v1.kpi_mapping_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'\n\x1bcom.exabel.api.analytics.v1B\x1bKpiMappingGroupServiceProtoP\x01Z\x1bexabel.com/api/analytics/v1'
    _globals['_CREATEKPIMAPPINGGROUPREQUEST'].fields_by_name['parent']._loaded_options = None
    _globals['_CREATEKPIMAPPINGGROUPREQUEST'].fields_by_name['parent']._serialized_options = b'\x92A\x14\xca>\x11\xfa\x02\x0ekpiMappingName\xe0A\x02'
    _globals['_CREATEKPIMAPPINGGROUPREQUEST'].fields_by_name['kpi_mapping_group']._loaded_options = None
    _globals['_CREATEKPIMAPPINGGROUPREQUEST'].fields_by_name['kpi_mapping_group']._serialized_options = b'\xe0A\x02'
    _globals['_GETKPIMAPPINGGROUPREQUEST'].fields_by_name['name']._loaded_options = None
    _globals['_GETKPIMAPPINGGROUPREQUEST'].fields_by_name['name']._serialized_options = b'\x92A\x19\xca>\x16\xfa\x02\x13kpiMappingGroupName\xe0A\x02'
    _globals['_LISTKPIMAPPINGGROUPSREQUEST'].fields_by_name['parent']._loaded_options = None
    _globals['_LISTKPIMAPPINGGROUPSREQUEST'].fields_by_name['parent']._serialized_options = b'\x92A\x14\xca>\x11\xfa\x02\x0ekpiMappingName\xe0A\x02'
    _globals['_UPDATEKPIMAPPINGGROUPREQUEST'].fields_by_name['kpi_mapping_group']._loaded_options = None
    _globals['_UPDATEKPIMAPPINGGROUPREQUEST'].fields_by_name['kpi_mapping_group']._serialized_options = b'\xe0A\x02'
    _globals['_KPIMAPPINGSERVICE'].methods_by_name['CreateKpiMappingGroup']._loaded_options = None
    _globals['_KPIMAPPINGSERVICE'].methods_by_name['CreateKpiMappingGroup']._serialized_options = b'\x92A\x1a\x12\x18Create KPI mapping group\x82\xd3\xe4\x93\x026"!/v1/{parent=kpiMappings/*}/groups:\x11kpi_mapping_group'
    _globals['_KPIMAPPINGSERVICE'].methods_by_name['GetKpiMappingGroup']._loaded_options = None
    _globals['_KPIMAPPINGSERVICE'].methods_by_name['GetKpiMappingGroup']._serialized_options = b'\x92A\x17\x12\x15Get KPI mapping group\x82\xd3\xe4\x93\x02#\x12!/v1/{name=kpiMappings/*/groups/*}'
    _globals['_KPIMAPPINGSERVICE'].methods_by_name['ListKpiMappingGroups']._loaded_options = None
    _globals['_KPIMAPPINGSERVICE'].methods_by_name['ListKpiMappingGroups']._serialized_options = b'\x92A\x19\x12\x17List KPI mapping groups\x82\xd3\xe4\x93\x02#\x12!/v1/{parent=kpiMappings/*}/groups'
    _globals['_KPIMAPPINGSERVICE'].methods_by_name['UpdateKpiMappingGroup']._loaded_options = None
    _globals['_KPIMAPPINGSERVICE'].methods_by_name['UpdateKpiMappingGroup']._serialized_options = b'\x92A\x1a\x12\x18Update KPI mapping group\x82\xd3\xe4\x93\x02H23/v1/{kpi_mapping_group.name=kpiMappings/*/groups/*}:\x11kpi_mapping_group'
    _globals['_CREATEKPIMAPPINGGROUPREQUEST']._serialized_start = 276
    _globals['_CREATEKPIMAPPINGGROUPREQUEST']._serialized_end = 424
    _globals['_GETKPIMAPPINGGROUPREQUEST']._serialized_start = 426
    _globals['_GETKPIMAPPINGGROUPREQUEST']._serialized_end = 500
    _globals['_LISTKPIMAPPINGGROUPSREQUEST']._serialized_start = 503
    _globals['_LISTKPIMAPPINGGROUPSREQUEST']._serialized_end = 708
    _globals['_LISTKPIMAPPINGGROUPSRESPONSE']._serialized_start = 711
    _globals['_LISTKPIMAPPINGGROUPSRESPONSE']._serialized_end = 844
    _globals['_UPDATEKPIMAPPINGGROUPREQUEST']._serialized_start = 847
    _globals['_UPDATEKPIMAPPINGGROUPREQUEST']._serialized_end = 1000
    _globals['_KPIMAPPINGSERVICE']._serialized_start = 1003
    _globals['_KPIMAPPINGSERVICE']._serialized_end = 1859