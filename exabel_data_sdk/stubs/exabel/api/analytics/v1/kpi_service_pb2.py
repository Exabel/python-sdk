"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'exabel/api/analytics/v1/kpi_service.proto')
_sym_db = _symbol_database.Default()
from .....exabel.api.analytics.v1 import kpi_messages_pb2 as exabel_dot_api_dot_analytics_dot_v1_dot_kpi__messages__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from .....protoc_gen_openapiv2.options import annotations_pb2 as protoc__gen__openapiv2_dot_options_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n)exabel/api/analytics/v1/kpi_service.proto\x12\x17exabel.api.analytics.v1\x1a*exabel/api/analytics/v1/kpi_messages.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x1fgoogle/api/field_behavior.proto\x1a.protoc_gen_openapiv2/options/annotations.proto"\x9e\x01\n\x1cListKpiMappingResultsRequest\x12*\n\x06parent\x18\x01 \x01(\tB\x1a\x92A\x14\xca>\x11\xfa\x02\x0ekpiMappingName\xe0A\x02\x12>\n\tpage_size\x18\x02 \x01(\x05B+\x92A(2&Maximum number of companies to return.\x12\x12\n\npage_token\x18\x03 \x01(\t"\x90\x01\n\x1dListKpiMappingResultsResponse\x12B\n\x07results\x18\x01 \x03(\x0b21.exabel.api.analytics.v1.CompanyKpiMappingResults\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\x12\x12\n\ntotal_size\x18\x03 \x01(\x05"\xc4\x01\n"ListCompanyBaseModelResultsRequest\x12\'\n\x06parent\x18\x01 \x01(\tB\x17\x92A\x11\xca>\x0e\xfa\x02\x0bcompanyName\xe0A\x02\x12=\n\x06period\x18\x02 \x01(\x0b2-.exabel.api.analytics.v1.FiscalPeriodSelector\x126\n\nkpi_source\x18\x03 \x01(\x0e2".exabel.api.analytics.v1.KpiSource"\x9d\x01\n#ListCompanyBaseModelResultsResponse\x12?\n\x07results\x18\x01 \x03(\x0b2..exabel.api.analytics.v1.CompanyKpiModelResult\x125\n\x06period\x18\x02 \x01(\x0b2%.exabel.api.analytics.v1.FiscalPeriod"\xcc\x01\n*ListCompanyHierarchicalModelResultsRequest\x12\'\n\x06parent\x18\x01 \x01(\tB\x17\x92A\x11\xca>\x0e\xfa\x02\x0bcompanyName\xe0A\x02\x12=\n\x06period\x18\x02 \x01(\x0b2-.exabel.api.analytics.v1.FiscalPeriodSelector\x126\n\nkpi_source\x18\x03 \x01(\x0e2".exabel.api.analytics.v1.KpiSource"\xe3\x01\n+ListCompanyHierarchicalModelResultsResponse\x12?\n\x07results\x18\x01 \x03(\x0b2..exabel.api.analytics.v1.CompanyKpiModelResult\x12<\n\rkpi_hierarchy\x18\x02 \x01(\x0b2%.exabel.api.analytics.v1.KpiHierarchy\x125\n\x06period\x18\x03 \x01(\x0b2%.exabel.api.analytics.v1.FiscalPeriod"~\n#ListCompanyKpiMappingResultsRequest\x12\'\n\x06parent\x18\x01 \x01(\tB\x17\x92A\x11\xca>\x0e\xfa\x02\x0bcompanyName\xe0A\x02\x12.\n\x03kpi\x18\x02 \x01(\x0b2\x1c.exabel.api.analytics.v1.KpiB\x03\xe0A\x02"f\n$ListCompanyKpiMappingResultsResponse\x12>\n\x07results\x18\x01 \x03(\x0b2-.exabel.api.analytics.v1.KpiMappingResultData"|\n!ListCompanyKpiModelResultsRequest\x12\'\n\x06parent\x18\x01 \x01(\tB\x17\x92A\x11\xca>\x0e\xfa\x02\x0bcompanyName\xe0A\x02\x12.\n\x03kpi\x18\x02 \x01(\x0b2\x1c.exabel.api.analytics.v1.KpiB\x03\xe0A\x02"\x9c\x02\n"ListCompanyKpiModelResultsResponse\x127\n\x0cexabel_model\x18\x01 \x01(\x0b2!.exabel.api.analytics.v1.KpiModel\x12=\n\x12hierarchical_model\x18\x02 \x01(\x0b2!.exabel.api.analytics.v1.KpiModel\x128\n\rcustom_models\x18\x03 \x03(\x0b2!.exabel.api.analytics.v1.KpiModel\x12D\n\x12kpi_mapping_models\x18\x04 \x03(\x0b2(.exabel.api.analytics.v1.KpiMappingModel2\x9a\n\n\nKpiService\x12\xcf\x01\n\x15ListKpiMappingResults\x125.exabel.api.analytics.v1.ListKpiMappingResultsRequest\x1a6.exabel.api.analytics.v1.ListKpiMappingResultsResponse"G\x92A\x1a\x12\x18List KPI mapping results\x82\xd3\xe4\x93\x02$\x12"/v1/{parent=kpiMappings/*}/results\x12\x82\x02\n\x1bListCompanyBaseModelResults\x12;.exabel.api.analytics.v1.ListCompanyBaseModelResultsRequest\x1a<.exabel.api.analytics.v1.ListCompanyBaseModelResultsResponse"h\x92A!\x12\x1fList company base model results\x82\xd3\xe4\x93\x02>\x12</v1/{parent=entityTypes/company/entities/*}/baseModelResults\x12\xaa\x02\n#ListCompanyHierarchicalModelResults\x12C.exabel.api.analytics.v1.ListCompanyHierarchicalModelResultsRequest\x1aD.exabel.api.analytics.v1.ListCompanyHierarchicalModelResultsResponse"x\x92A)\x12\'List company hierarchical model results\x82\xd3\xe4\x93\x02F\x12D/v1/{parent=entityTypes/company/entities/*}/hierarchicalModelResults\x12\x87\x02\n\x1cListCompanyKpiMappingResults\x12<.exabel.api.analytics.v1.ListCompanyKpiMappingResultsRequest\x1a=.exabel.api.analytics.v1.ListCompanyKpiMappingResultsResponse"j\x92A"\x12 List company KPI mapping results\x82\xd3\xe4\x93\x02?\x12=/v1/{parent=entityTypes/company/entities/*}/kpiMappingResults\x12\xfd\x01\n\x1aListCompanyKpiModelResults\x12:.exabel.api.analytics.v1.ListCompanyKpiModelResultsRequest\x1a;.exabel.api.analytics.v1.ListCompanyKpiModelResultsResponse"f\x92A \x12\x1eList company KPI model results\x82\xd3\xe4\x93\x02=\x12;/v1/{parent=entityTypes/company/entities/*}/kpiModelResultsBM\n\x1bcom.exabel.api.analytics.v1B\x0fKpiServiceProtoP\x01Z\x1bexabel.com/api/analytics/v1b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'exabel.api.analytics.v1.kpi_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'\n\x1bcom.exabel.api.analytics.v1B\x0fKpiServiceProtoP\x01Z\x1bexabel.com/api/analytics/v1'
    _globals['_LISTKPIMAPPINGRESULTSREQUEST'].fields_by_name['parent']._loaded_options = None
    _globals['_LISTKPIMAPPINGRESULTSREQUEST'].fields_by_name['parent']._serialized_options = b'\x92A\x14\xca>\x11\xfa\x02\x0ekpiMappingName\xe0A\x02'
    _globals['_LISTKPIMAPPINGRESULTSREQUEST'].fields_by_name['page_size']._loaded_options = None
    _globals['_LISTKPIMAPPINGRESULTSREQUEST'].fields_by_name['page_size']._serialized_options = b'\x92A(2&Maximum number of companies to return.'
    _globals['_LISTCOMPANYBASEMODELRESULTSREQUEST'].fields_by_name['parent']._loaded_options = None
    _globals['_LISTCOMPANYBASEMODELRESULTSREQUEST'].fields_by_name['parent']._serialized_options = b'\x92A\x11\xca>\x0e\xfa\x02\x0bcompanyName\xe0A\x02'
    _globals['_LISTCOMPANYHIERARCHICALMODELRESULTSREQUEST'].fields_by_name['parent']._loaded_options = None
    _globals['_LISTCOMPANYHIERARCHICALMODELRESULTSREQUEST'].fields_by_name['parent']._serialized_options = b'\x92A\x11\xca>\x0e\xfa\x02\x0bcompanyName\xe0A\x02'
    _globals['_LISTCOMPANYKPIMAPPINGRESULTSREQUEST'].fields_by_name['parent']._loaded_options = None
    _globals['_LISTCOMPANYKPIMAPPINGRESULTSREQUEST'].fields_by_name['parent']._serialized_options = b'\x92A\x11\xca>\x0e\xfa\x02\x0bcompanyName\xe0A\x02'
    _globals['_LISTCOMPANYKPIMAPPINGRESULTSREQUEST'].fields_by_name['kpi']._loaded_options = None
    _globals['_LISTCOMPANYKPIMAPPINGRESULTSREQUEST'].fields_by_name['kpi']._serialized_options = b'\xe0A\x02'
    _globals['_LISTCOMPANYKPIMODELRESULTSREQUEST'].fields_by_name['parent']._loaded_options = None
    _globals['_LISTCOMPANYKPIMODELRESULTSREQUEST'].fields_by_name['parent']._serialized_options = b'\x92A\x11\xca>\x0e\xfa\x02\x0bcompanyName\xe0A\x02'
    _globals['_LISTCOMPANYKPIMODELRESULTSREQUEST'].fields_by_name['kpi']._loaded_options = None
    _globals['_LISTCOMPANYKPIMODELRESULTSREQUEST'].fields_by_name['kpi']._serialized_options = b'\xe0A\x02'
    _globals['_KPISERVICE'].methods_by_name['ListKpiMappingResults']._loaded_options = None
    _globals['_KPISERVICE'].methods_by_name['ListKpiMappingResults']._serialized_options = b'\x92A\x1a\x12\x18List KPI mapping results\x82\xd3\xe4\x93\x02$\x12"/v1/{parent=kpiMappings/*}/results'
    _globals['_KPISERVICE'].methods_by_name['ListCompanyBaseModelResults']._loaded_options = None
    _globals['_KPISERVICE'].methods_by_name['ListCompanyBaseModelResults']._serialized_options = b'\x92A!\x12\x1fList company base model results\x82\xd3\xe4\x93\x02>\x12</v1/{parent=entityTypes/company/entities/*}/baseModelResults'
    _globals['_KPISERVICE'].methods_by_name['ListCompanyHierarchicalModelResults']._loaded_options = None
    _globals['_KPISERVICE'].methods_by_name['ListCompanyHierarchicalModelResults']._serialized_options = b"\x92A)\x12'List company hierarchical model results\x82\xd3\xe4\x93\x02F\x12D/v1/{parent=entityTypes/company/entities/*}/hierarchicalModelResults"
    _globals['_KPISERVICE'].methods_by_name['ListCompanyKpiMappingResults']._loaded_options = None
    _globals['_KPISERVICE'].methods_by_name['ListCompanyKpiMappingResults']._serialized_options = b'\x92A"\x12 List company KPI mapping results\x82\xd3\xe4\x93\x02?\x12=/v1/{parent=entityTypes/company/entities/*}/kpiMappingResults'
    _globals['_KPISERVICE'].methods_by_name['ListCompanyKpiModelResults']._loaded_options = None
    _globals['_KPISERVICE'].methods_by_name['ListCompanyKpiModelResults']._serialized_options = b'\x92A \x12\x1eList company KPI model results\x82\xd3\xe4\x93\x02=\x12;/v1/{parent=entityTypes/company/entities/*}/kpiModelResults'
    _globals['_LISTKPIMAPPINGRESULTSREQUEST']._serialized_start = 226
    _globals['_LISTKPIMAPPINGRESULTSREQUEST']._serialized_end = 384
    _globals['_LISTKPIMAPPINGRESULTSRESPONSE']._serialized_start = 387
    _globals['_LISTKPIMAPPINGRESULTSRESPONSE']._serialized_end = 531
    _globals['_LISTCOMPANYBASEMODELRESULTSREQUEST']._serialized_start = 534
    _globals['_LISTCOMPANYBASEMODELRESULTSREQUEST']._serialized_end = 730
    _globals['_LISTCOMPANYBASEMODELRESULTSRESPONSE']._serialized_start = 733
    _globals['_LISTCOMPANYBASEMODELRESULTSRESPONSE']._serialized_end = 890
    _globals['_LISTCOMPANYHIERARCHICALMODELRESULTSREQUEST']._serialized_start = 893
    _globals['_LISTCOMPANYHIERARCHICALMODELRESULTSREQUEST']._serialized_end = 1097
    _globals['_LISTCOMPANYHIERARCHICALMODELRESULTSRESPONSE']._serialized_start = 1100
    _globals['_LISTCOMPANYHIERARCHICALMODELRESULTSRESPONSE']._serialized_end = 1327
    _globals['_LISTCOMPANYKPIMAPPINGRESULTSREQUEST']._serialized_start = 1329
    _globals['_LISTCOMPANYKPIMAPPINGRESULTSREQUEST']._serialized_end = 1455
    _globals['_LISTCOMPANYKPIMAPPINGRESULTSRESPONSE']._serialized_start = 1457
    _globals['_LISTCOMPANYKPIMAPPINGRESULTSRESPONSE']._serialized_end = 1559
    _globals['_LISTCOMPANYKPIMODELRESULTSREQUEST']._serialized_start = 1561
    _globals['_LISTCOMPANYKPIMODELRESULTSREQUEST']._serialized_end = 1685
    _globals['_LISTCOMPANYKPIMODELRESULTSRESPONSE']._serialized_start = 1688
    _globals['_LISTCOMPANYKPIMODELRESULTSRESPONSE']._serialized_end = 1972
    _globals['_KPISERVICE']._serialized_start = 1975
    _globals['_KPISERVICE']._serialized_end = 3281