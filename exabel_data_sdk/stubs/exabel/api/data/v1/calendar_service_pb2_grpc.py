"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings
from .....exabel.api.data.v1 import calendar_service_pb2 as exabel_dot_api_dot_data_dot_v1_dot_calendar__service__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
GRPC_GENERATED_VERSION = '1.71.2'
GRPC_VERSION = grpc.__version__
_version_not_supported = False
try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True
if _version_not_supported:
    raise RuntimeError(f'The grpc package installed is at version {GRPC_VERSION},' + f' but the generated code in exabel/api/data/v1/calendar_service_pb2_grpc.py depends on' + f' grpcio>={GRPC_GENERATED_VERSION}.' + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}' + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.')

class CalendarServiceStub(object):
    """Service for managing custom fiscal calendar data.

    Custom fiscal calendar data will supplement calendar data provided by Exabel.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.BatchCreateFiscalPeriods = channel.unary_unary('/exabel.api.data.v1.CalendarService/BatchCreateFiscalPeriods', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_calendar__service__pb2.BatchCreateFiscalPeriodsRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_data_dot_v1_dot_calendar__service__pb2.BatchCreateFiscalPeriodsResponse.FromString, _registered_method=True)
        self.ListFiscalPeriods = channel.unary_unary('/exabel.api.data.v1.CalendarService/ListFiscalPeriods', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_calendar__service__pb2.ListFiscalPeriodsRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_data_dot_v1_dot_calendar__service__pb2.ListFiscalPeriodsResponse.FromString, _registered_method=True)
        self.DeleteFiscalPeriod = channel.unary_unary('/exabel.api.data.v1.CalendarService/DeleteFiscalPeriod', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_calendar__service__pb2.DeleteFiscalPeriodRequest.SerializeToString, response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString, _registered_method=True)
        self.ListCompaniesWithFiscalPeriods = channel.unary_unary('/exabel.api.data.v1.CalendarService/ListCompaniesWithFiscalPeriods', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_calendar__service__pb2.ListCompaniesWithFiscalPeriodsRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_data_dot_v1_dot_calendar__service__pb2.ListCompaniesWithFiscalPeriodsResponse.FromString, _registered_method=True)

class CalendarServiceServicer(object):
    """Service for managing custom fiscal calendar data.

    Custom fiscal calendar data will supplement calendar data provided by Exabel.
    """

    def BatchCreateFiscalPeriods(self, request, context):
        """Creates multiple custom fiscal periods for a company.

        Creates multiple custom fiscal periods for a given company.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListFiscalPeriods(self, request, context):
        """Lists the custom fiscal periods for a company.

        Lists the custom fiscal periods for a given company.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteFiscalPeriod(self, request, context):
        """Deletes one or all fiscal period for a company.

        Deletes one or all fiscal period for a given company.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListCompaniesWithFiscalPeriods(self, request, context):
        """Lists all the companies with custom fiscal periods.

        Lists all the companies for which there are custom fiscal periods.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_CalendarServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {'BatchCreateFiscalPeriods': grpc.unary_unary_rpc_method_handler(servicer.BatchCreateFiscalPeriods, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_calendar__service__pb2.BatchCreateFiscalPeriodsRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_calendar__service__pb2.BatchCreateFiscalPeriodsResponse.SerializeToString), 'ListFiscalPeriods': grpc.unary_unary_rpc_method_handler(servicer.ListFiscalPeriods, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_calendar__service__pb2.ListFiscalPeriodsRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_calendar__service__pb2.ListFiscalPeriodsResponse.SerializeToString), 'DeleteFiscalPeriod': grpc.unary_unary_rpc_method_handler(servicer.DeleteFiscalPeriod, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_calendar__service__pb2.DeleteFiscalPeriodRequest.FromString, response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString), 'ListCompaniesWithFiscalPeriods': grpc.unary_unary_rpc_method_handler(servicer.ListCompaniesWithFiscalPeriods, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_calendar__service__pb2.ListCompaniesWithFiscalPeriodsRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_calendar__service__pb2.ListCompaniesWithFiscalPeriodsResponse.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('exabel.api.data.v1.CalendarService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('exabel.api.data.v1.CalendarService', rpc_method_handlers)

class CalendarService(object):
    """Service for managing custom fiscal calendar data.

    Custom fiscal calendar data will supplement calendar data provided by Exabel.
    """

    @staticmethod
    def BatchCreateFiscalPeriods(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.CalendarService/BatchCreateFiscalPeriods', exabel_dot_api_dot_data_dot_v1_dot_calendar__service__pb2.BatchCreateFiscalPeriodsRequest.SerializeToString, exabel_dot_api_dot_data_dot_v1_dot_calendar__service__pb2.BatchCreateFiscalPeriodsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def ListFiscalPeriods(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.CalendarService/ListFiscalPeriods', exabel_dot_api_dot_data_dot_v1_dot_calendar__service__pb2.ListFiscalPeriodsRequest.SerializeToString, exabel_dot_api_dot_data_dot_v1_dot_calendar__service__pb2.ListFiscalPeriodsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def DeleteFiscalPeriod(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.CalendarService/DeleteFiscalPeriod', exabel_dot_api_dot_data_dot_v1_dot_calendar__service__pb2.DeleteFiscalPeriodRequest.SerializeToString, google_dot_protobuf_dot_empty__pb2.Empty.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def ListCompaniesWithFiscalPeriods(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.CalendarService/ListCompaniesWithFiscalPeriods', exabel_dot_api_dot_data_dot_v1_dot_calendar__service__pb2.ListCompaniesWithFiscalPeriodsRequest.SerializeToString, exabel_dot_api_dot_data_dot_v1_dot_calendar__service__pb2.ListCompaniesWithFiscalPeriodsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)