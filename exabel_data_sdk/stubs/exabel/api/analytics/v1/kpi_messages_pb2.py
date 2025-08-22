"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'exabel/api/analytics/v1/kpi_messages.proto')
_sym_db = _symbol_database.Default()
from .....exabel.api.time import date_pb2 as exabel_dot_api_dot_time_dot_date__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n*exabel/api/analytics/v1/kpi_messages.proto\x12\x17exabel.api.analytics.v1\x1a\x1aexabel/api/time/date.proto"\x9a\x01\n\x18CompanyKpiMappingResults\x120\n\x06entity\x18\x01 \x01(\x0b2 .exabel.api.analytics.v1.Company\x12L\n\x0bkpi_results\x18\x02 \x03(\x0b27.exabel.api.analytics.v1.SingleCompanyKpiMappingResults"G\n\x07Company\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x14\n\x0cdisplay_name\x18\x02 \x01(\t\x12\x18\n\x10bloomberg_ticker\x18\x03 \x01(\t"\x88\x01\n\x1eSingleCompanyKpiMappingResults\x12)\n\x03kpi\x18\x01 \x01(\x0b2\x1c.exabel.api.analytics.v1.Kpi\x12;\n\x04data\x18\x02 \x03(\x0b2-.exabel.api.analytics.v1.KpiMappingResultData"\x87\x01\n\x03Kpi\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\x12\n\x05value\x18\x02 \x01(\tH\x00\x88\x01\x01\x12\x14\n\x0cdisplay_name\x18\x03 \x01(\t\x12\x11\n\x04freq\x18\x04 \x01(\tH\x01\x88\x01\x01\x12\x15\n\x08is_ratio\x18\x05 \x01(\x08H\x02\x88\x01\x01B\x08\n\x06_valueB\x07\n\x05_freqB\x0b\n\t_is_ratio"\xc4\x06\n\x14KpiMappingResultData\x128\n\x06source\x18\x01 \x01(\x0b2(.exabel.api.analytics.v1.KpiMappingGroup\x12\x17\n\nmodel_mape\x18\x02 \x01(\x01H\x00\x88\x01\x01\x12\x16\n\tmodel_mae\x18\x03 \x01(\x01H\x01\x88\x01\x01\x12\x1b\n\x0emodel_hit_rate\x18\x04 \x01(\x01H\x02\x88\x01\x01\x12.\n\x0flast_value_date\x18\x05 \x01(\x0b2\x15.exabel.api.time.Date\x12"\n\x15number_of_data_points\x18\x06 \x01(\x05H\x03\x88\x01\x01\x12#\n\x16period_over_period_mae\x18\x07 \x01(\x01H\x04\x88\x01\x01\x12\x1f\n\x12year_over_year_mae\x18\x08 \x01(\x01H\x05\x88\x01\x01\x12!\n\x14absolute_correlation\x18\t \x01(\x01H\x06\x88\x01\x01\x12+\n\x1eperiod_over_period_correlation\x18\n \x01(\x01H\x07\x88\x01\x01\x12\'\n\x1ayear_over_year_correlation\x18\x0b \x01(\x01H\x08\x88\x01\x01\x12\x1d\n\x10absolute_p_value\x18\x0c \x01(\x01H\t\x88\x01\x01\x12\'\n\x1aperiod_over_period_p_value\x18\r \x01(\x01H\n\x88\x01\x01\x12#\n\x16year_over_year_p_value\x18\x0e \x01(\x01H\x0b\x88\x01\x01B\r\n\x0b_model_mapeB\x0c\n\n_model_maeB\x11\n\x0f_model_hit_rateB\x18\n\x16_number_of_data_pointsB\x19\n\x17_period_over_period_maeB\x15\n\x13_year_over_year_maeB\x17\n\x15_absolute_correlationB!\n\x1f_period_over_period_correlationB\x1d\n\x1b_year_over_year_correlationB\x13\n\x11_absolute_p_valueB\x1d\n\x1b_period_over_period_p_valueB\x19\n\x17_year_over_year_p_value"R\n\x0fKpiMappingGroup\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x14\n\x0cdisplay_name\x18\x02 \x01(\t\x12\x1b\n\x13vendor_display_name\x18\x03 \x01(\t"\xcb\x01\n\x15CompanyKpiModelResult\x12)\n\x03kpi\x18\x01 \x01(\x0b2\x1c.exabel.api.analytics.v1.Kpi\x120\n\x05model\x18\x02 \x01(\x0b2!.exabel.api.analytics.v1.KpiModel\x12!\n\x19accessible_mappings_count\x18\x03 \x01(\x05\x12\x1c\n\x14total_mappings_count\x18\x04 \x01(\x05\x12\x14\n\x0cmodels_count\x18\x05 \x01(\x05"\xaf\x01\n\x08KpiModel\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\n\n\x02id\x18\x02 \x01(\x05\x12\x14\n\x0cdisplay_name\x18\x03 \x01(\t\x123\n\x04data\x18\x04 \x01(\x0b2%.exabel.api.analytics.v1.KpiModelData\x12>\n\x07weights\x18\x05 \x01(\x0b2-.exabel.api.analytics.v1.KpiModelWeightGroups"\x8a\x01\n\x0fKpiMappingModel\x128\n\x06source\x18\x01 \x01(\x0b2(.exabel.api.analytics.v1.KpiMappingGroup\x12=\n\x0ekpi_model_data\x18\x02 \x01(\x0b2%.exabel.api.analytics.v1.KpiModelData"\xac\x06\n\x0cKpiModelData\x12\x17\n\nprediction\x18\x01 \x01(\x01H\x00\x88\x01\x01\x12\x1f\n\x12prediction_yoy_rel\x18\x02 \x01(\x01H\x01\x88\x01\x01\x12\x1f\n\x12prediction_yoy_abs\x18\x03 \x01(\x01H\x02\x88\x01\x01\x12\x16\n\tconsensus\x18\x04 \x01(\x01H\x03\x88\x01\x01\x12\x1e\n\x11consensus_yoy_rel\x18\x05 \x01(\x01H\x04\x88\x01\x01\x12\x1e\n\x11consensus_yoy_abs\x18\x06 \x01(\x01H\x05\x88\x01\x01\x12\x16\n\tdelta_abs\x18\x07 \x01(\x01H\x06\x88\x01\x01\x12\x16\n\tdelta_rel\x18\x08 \x01(\x01H\x07\x88\x01\x01\x12\x1b\n\x0edelta_by_error\x18\t \x01(\x01H\x08\x88\x01\x01\x12<\n\rmodel_quality\x18\n \x01(\x0e2%.exabel.api.analytics.v1.ModelQuality\x12\x11\n\x04mape\x18\x0b \x01(\x01H\t\x88\x01\x01\x12\x15\n\x08mape_pit\x18\x0c \x01(\x01H\n\x88\x01\x01\x12\x10\n\x03mae\x18\r \x01(\x01H\x0b\x88\x01\x01\x12\x14\n\x07mae_pit\x18\x0e \x01(\x01H\x0c\x88\x01\x01\x12\x15\n\x08hit_rate\x18\x0f \x01(\x01H\r\x88\x01\x01\x12\x1c\n\x0frevision_1_week\x18\x10 \x01(\x01H\x0e\x88\x01\x01\x12\x1d\n\x10revision_1_month\x18\x11 \x01(\x01H\x0f\x88\x01\x01\x12#\n\x04date\x18\x12 \x01(\x0b2\x15.exabel.api.time.Date\x12\r\n\x05error\x18d \x01(\tB\r\n\x0b_predictionB\x15\n\x13_prediction_yoy_relB\x15\n\x13_prediction_yoy_absB\x0c\n\n_consensusB\x14\n\x12_consensus_yoy_relB\x14\n\x12_consensus_yoy_absB\x0c\n\n_delta_absB\x0c\n\n_delta_relB\x11\n\x0f_delta_by_errorB\x07\n\x05_mapeB\x0b\n\t_mape_pitB\x06\n\x04_maeB\n\n\x08_mae_pitB\x0b\n\t_hit_rateB\x12\n\x10_revision_1_weekB\x13\n\x11_revision_1_month"t\n\x14KpiModelWeightGroups\x12C\n\rweight_groups\x18\x01 \x03(\x0b2,.exabel.api.analytics.v1.KpiModelWeightGroup\x12\x17\n\x0fis_coefficients\x18\x02 \x01(\x08"\xad\x01\n\x13KpiModelWeightGroup\x12\x14\n\x0cdisplay_name\x18\x01 \x01(\t\x127\n\x05group\x18\x02 \x01(\x0b2(.exabel.api.analytics.v1.KpiMappingGroup\x12G\n\x0ffeature_weights\x18\x03 \x03(\x0b2..exabel.api.analytics.v1.KpiModelFeatureWeight"M\n\x15KpiModelFeatureWeight\x12\x13\n\x06weight\x18\x01 \x01(\x01H\x00\x88\x01\x01\x12\x14\n\x0cdisplay_name\x18\x02 \x01(\tB\t\n\x07_weight"\xa1\x01\n\x14FiscalPeriodSelector\x12P\n\x11relative_selector\x18\x01 \x01(\x0e25.exabel.api.analytics.v1.RelativeFiscalPeriodSelector\x12)\n\nperiod_end\x18\x02 \x01(\x0b2\x15.exabel.api.time.Date\x12\x0c\n\x04freq\x18\x03 \x01(\t"d\n\x0cKpiHierarchy\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04freq\x18\x02 \x01(\t\x128\n\tbreakdown\x18\x03 \x01(\x0b2%.exabel.api.analytics.v1.KpiBreakdown"G\n\x0cKpiBreakdown\x127\n\x04kpis\x18\x01 \x03(\x0b2).exabel.api.analytics.v1.KpiBreakdownNode"\x99\x01\n\x10KpiBreakdownNode\x12+\n\x03kpi\x18\x01 \x01(\x0b2\x1c.exabel.api.analytics.v1.KpiH\x00\x12\x10\n\x06header\x18\x02 \x01(\tH\x00\x12;\n\x08children\x18\x03 \x03(\x0b2).exabel.api.analytics.v1.KpiBreakdownNodeB\t\n\x07content*]\n\tKpiSource\x12\x1a\n\x16KPI_SOURCE_UNSPECIFIED\x10\x00\x12\x1c\n\x18KPI_SOURCE_VISIBLE_ALPHA\x10\x01\x12\x16\n\x12KPI_SOURCE_FACTSET\x10\x02*\x93\x01\n\x0cModelQuality\x12\x1d\n\x19MODEL_QUALITY_UNSPECIFIED\x10\x00\x12\x15\n\x11MODEL_QUALITY_LOW\x10\n\x12\x18\n\x14MODEL_QUALITY_MEDIUM\x10\x14\x12\x16\n\x12MODEL_QUALITY_HIGH\x10\x1e\x12\x1b\n\x17MODEL_QUALITY_VERY_HIGH\x10(*t\n\x1cRelativeFiscalPeriodSelector\x12/\n+RELATIVE_FISCAL_PERIOD_SELECTOR_UNSPECIFIED\x10\x00\x12\x0c\n\x08PREVIOUS\x10\x01\x12\x0b\n\x07CURRENT\x10\x02\x12\x08\n\x04NEXT\x10\x03BN\n\x1bcom.exabel.api.analytics.v1B\x10KpiMessagesProtoP\x01Z\x1bexabel.com/api/analytics/v1b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'exabel.api.analytics.v1.kpi_messages_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'\n\x1bcom.exabel.api.analytics.v1B\x10KpiMessagesProtoP\x01Z\x1bexabel.com/api/analytics/v1'
    _globals['_KPISOURCE']._serialized_start = 3737
    _globals['_KPISOURCE']._serialized_end = 3830
    _globals['_MODELQUALITY']._serialized_start = 3833
    _globals['_MODELQUALITY']._serialized_end = 3980
    _globals['_RELATIVEFISCALPERIODSELECTOR']._serialized_start = 3982
    _globals['_RELATIVEFISCALPERIODSELECTOR']._serialized_end = 4098
    _globals['_COMPANYKPIMAPPINGRESULTS']._serialized_start = 100
    _globals['_COMPANYKPIMAPPINGRESULTS']._serialized_end = 254
    _globals['_COMPANY']._serialized_start = 256
    _globals['_COMPANY']._serialized_end = 327
    _globals['_SINGLECOMPANYKPIMAPPINGRESULTS']._serialized_start = 330
    _globals['_SINGLECOMPANYKPIMAPPINGRESULTS']._serialized_end = 466
    _globals['_KPI']._serialized_start = 469
    _globals['_KPI']._serialized_end = 604
    _globals['_KPIMAPPINGRESULTDATA']._serialized_start = 607
    _globals['_KPIMAPPINGRESULTDATA']._serialized_end = 1443
    _globals['_KPIMAPPINGGROUP']._serialized_start = 1445
    _globals['_KPIMAPPINGGROUP']._serialized_end = 1527
    _globals['_COMPANYKPIMODELRESULT']._serialized_start = 1530
    _globals['_COMPANYKPIMODELRESULT']._serialized_end = 1733
    _globals['_KPIMODEL']._serialized_start = 1736
    _globals['_KPIMODEL']._serialized_end = 1911
    _globals['_KPIMAPPINGMODEL']._serialized_start = 1914
    _globals['_KPIMAPPINGMODEL']._serialized_end = 2052
    _globals['_KPIMODELDATA']._serialized_start = 2055
    _globals['_KPIMODELDATA']._serialized_end = 2867
    _globals['_KPIMODELWEIGHTGROUPS']._serialized_start = 2869
    _globals['_KPIMODELWEIGHTGROUPS']._serialized_end = 2985
    _globals['_KPIMODELWEIGHTGROUP']._serialized_start = 2988
    _globals['_KPIMODELWEIGHTGROUP']._serialized_end = 3161
    _globals['_KPIMODELFEATUREWEIGHT']._serialized_start = 3163
    _globals['_KPIMODELFEATUREWEIGHT']._serialized_end = 3240
    _globals['_FISCALPERIODSELECTOR']._serialized_start = 3243
    _globals['_FISCALPERIODSELECTOR']._serialized_end = 3404
    _globals['_KPIHIERARCHY']._serialized_start = 3406
    _globals['_KPIHIERARCHY']._serialized_end = 3506
    _globals['_KPIBREAKDOWN']._serialized_start = 3508
    _globals['_KPIBREAKDOWN']._serialized_end = 3579
    _globals['_KPIBREAKDOWNNODE']._serialized_start = 3582
    _globals['_KPIBREAKDOWNNODE']._serialized_end = 3735