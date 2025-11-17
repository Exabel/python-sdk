"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 29, 0, '', 'exabel/api/data/v1/calendar_service.proto')
_sym_db = _symbol_database.Default()
from .....exabel.api.data.v1 import calendar_messages_pb2 as exabel_dot_api_dot_data_dot_v1_dot_calendar__messages__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from .....protoc_gen_openapiv2.options import annotations_pb2 as protoc__gen__openapiv2_dot_options_dot_annotations__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n)exabel/api/data/v1/calendar_service.proto\x12\x12exabel.api.data.v1\x1a*exabel/api/data/v1/calendar_messages.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x1fgoogle/api/field_behavior.proto\x1a\x1bgoogle/protobuf/empty.proto\x1a.protoc_gen_openapiv2/options/annotations.proto"\x82\x01\n\x1fBatchCreateFiscalPeriodsRequest\x12\'\n\x06parent\x18\x01 \x01(\tB\x17\x92A\x11\xca>\x0e\xfa\x02\x0bcompanyName\xe0A\x02\x126\n\x07periods\x18\x02 \x03(\x0b2 .exabel.api.data.v1.FiscalPeriodB\x03\xe0A\x02""\n BatchCreateFiscalPeriodsResponse"v\n\x19DeleteFiscalPeriodRequest\x12\'\n\x06parent\x18\x01 \x01(\tB\x17\x92A\x11\xca>\x0e\xfa\x02\x0bcompanyName\xe0A\x02\x120\n\x06period\x18\x02 \x01(\x0b2 .exabel.api.data.v1.FiscalPeriod"u\n\x18ListFiscalPeriodsRequest\x12\'\n\x06parent\x18\x01 \x01(\tB\x17\x92A\x11\xca>\x0e\xfa\x02\x0bcompanyName\xe0A\x02\x120\n\tfrequency\x18\x02 \x01(\x0e2\x1d.exabel.api.data.v1.Frequency"N\n\x19ListFiscalPeriodsResponse\x121\n\x07periods\x18\x01 \x03(\x0b2 .exabel.api.data.v1.FiscalPeriod"\'\n%ListCompaniesWithFiscalPeriodsRequest";\n&ListCompaniesWithFiscalPeriodsResponse\x12\x11\n\tcompanies\x18\x01 \x03(\t2\x99\x07\n\x0fCalendarService\x12\xf8\x01\n\x18BatchCreateFiscalPeriods\x123.exabel.api.data.v1.BatchCreateFiscalPeriodsRequest\x1a4.exabel.api.data.v1.BatchCreateFiscalPeriodsResponse"q\x92A\x1e\x12\x1cCreate custom fiscal periods\x82\xd3\xe4\x93\x02J"E/v1/{parent=entityTypes/company/entities/*}/fiscalPeriods:batchCreate:\x01*\x12\xd2\x01\n\x11ListFiscalPeriods\x12,.exabel.api.data.v1.ListFiscalPeriodsRequest\x1a-.exabel.api.data.v1.ListFiscalPeriodsResponse"`\x92A\x1c\x12\x1aList custom fiscal periods\x82\xd3\xe4\x93\x02;\x129/v1/{parent=entityTypes/company/entities/*}/fiscalPeriods\x12\xbf\x01\n\x12DeleteFiscalPeriod\x12-.exabel.api.data.v1.DeleteFiscalPeriodRequest\x1a\x16.google.protobuf.Empty"b\x92A\x1e\x12\x1cDelete custom fiscal periods\x82\xd3\xe4\x93\x02;*9/v1/{parent=entityTypes/company/entities/*}/fiscalPeriods\x12\xf3\x01\n\x1eListCompaniesWithFiscalPeriods\x129.exabel.api.data.v1.ListCompaniesWithFiscalPeriodsRequest\x1a:.exabel.api.data.v1.ListCompaniesWithFiscalPeriodsResponse"Z\x92A+\x12)List companies with custom fiscal periods\x82\xd3\xe4\x93\x02&\x12$/v1/companiesWithCustomFiscalPeriodsBH\n\x16com.exabel.api.data.v1B\x14CalendarServiceProtoP\x01Z\x16exabel.com/api/data/v1b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'exabel.api.data.v1.calendar_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    _globals['DESCRIPTOR']._loaded_options = None
    _globals['DESCRIPTOR']._serialized_options = b'\n\x16com.exabel.api.data.v1B\x14CalendarServiceProtoP\x01Z\x16exabel.com/api/data/v1'
    _globals['_BATCHCREATEFISCALPERIODSREQUEST'].fields_by_name['parent']._loaded_options = None
    _globals['_BATCHCREATEFISCALPERIODSREQUEST'].fields_by_name['parent']._serialized_options = b'\x92A\x11\xca>\x0e\xfa\x02\x0bcompanyName\xe0A\x02'
    _globals['_BATCHCREATEFISCALPERIODSREQUEST'].fields_by_name['periods']._loaded_options = None
    _globals['_BATCHCREATEFISCALPERIODSREQUEST'].fields_by_name['periods']._serialized_options = b'\xe0A\x02'
    _globals['_DELETEFISCALPERIODREQUEST'].fields_by_name['parent']._loaded_options = None
    _globals['_DELETEFISCALPERIODREQUEST'].fields_by_name['parent']._serialized_options = b'\x92A\x11\xca>\x0e\xfa\x02\x0bcompanyName\xe0A\x02'
    _globals['_LISTFISCALPERIODSREQUEST'].fields_by_name['parent']._loaded_options = None
    _globals['_LISTFISCALPERIODSREQUEST'].fields_by_name['parent']._serialized_options = b'\x92A\x11\xca>\x0e\xfa\x02\x0bcompanyName\xe0A\x02'
    _globals['_CALENDARSERVICE'].methods_by_name['BatchCreateFiscalPeriods']._loaded_options = None
    _globals['_CALENDARSERVICE'].methods_by_name['BatchCreateFiscalPeriods']._serialized_options = b'\x92A\x1e\x12\x1cCreate custom fiscal periods\x82\xd3\xe4\x93\x02J"E/v1/{parent=entityTypes/company/entities/*}/fiscalPeriods:batchCreate:\x01*'
    _globals['_CALENDARSERVICE'].methods_by_name['ListFiscalPeriods']._loaded_options = None
    _globals['_CALENDARSERVICE'].methods_by_name['ListFiscalPeriods']._serialized_options = b'\x92A\x1c\x12\x1aList custom fiscal periods\x82\xd3\xe4\x93\x02;\x129/v1/{parent=entityTypes/company/entities/*}/fiscalPeriods'
    _globals['_CALENDARSERVICE'].methods_by_name['DeleteFiscalPeriod']._loaded_options = None
    _globals['_CALENDARSERVICE'].methods_by_name['DeleteFiscalPeriod']._serialized_options = b'\x92A\x1e\x12\x1cDelete custom fiscal periods\x82\xd3\xe4\x93\x02;*9/v1/{parent=entityTypes/company/entities/*}/fiscalPeriods'
    _globals['_CALENDARSERVICE'].methods_by_name['ListCompaniesWithFiscalPeriods']._loaded_options = None
    _globals['_CALENDARSERVICE'].methods_by_name['ListCompaniesWithFiscalPeriods']._serialized_options = b'\x92A+\x12)List companies with custom fiscal periods\x82\xd3\xe4\x93\x02&\x12$/v1/companiesWithCustomFiscalPeriods'
    _globals['_BATCHCREATEFISCALPERIODSREQUEST']._serialized_start = 250
    _globals['_BATCHCREATEFISCALPERIODSREQUEST']._serialized_end = 380
    _globals['_BATCHCREATEFISCALPERIODSRESPONSE']._serialized_start = 382
    _globals['_BATCHCREATEFISCALPERIODSRESPONSE']._serialized_end = 416
    _globals['_DELETEFISCALPERIODREQUEST']._serialized_start = 418
    _globals['_DELETEFISCALPERIODREQUEST']._serialized_end = 536
    _globals['_LISTFISCALPERIODSREQUEST']._serialized_start = 538
    _globals['_LISTFISCALPERIODSREQUEST']._serialized_end = 655
    _globals['_LISTFISCALPERIODSRESPONSE']._serialized_start = 657
    _globals['_LISTFISCALPERIODSRESPONSE']._serialized_end = 735
    _globals['_LISTCOMPANIESWITHFISCALPERIODSREQUEST']._serialized_start = 737
    _globals['_LISTCOMPANIESWITHFISCALPERIODSREQUEST']._serialized_end = 776
    _globals['_LISTCOMPANIESWITHFISCALPERIODSRESPONSE']._serialized_start = 778
    _globals['_LISTCOMPANIESWITHFISCALPERIODSRESPONSE']._serialized_end = 837
    _globals['_CALENDARSERVICE']._serialized_start = 840
    _globals['_CALENDARSERVICE']._serialized_end = 1761