"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings
from .....exabel.api.data.v1 import signal_messages_pb2 as exabel_dot_api_dot_data_dot_v1_dot_signal__messages__pb2
from .....exabel.api.data.v1 import signal_service_pb2 as exabel_dot_api_dot_data_dot_v1_dot_signal__service__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
GRPC_GENERATED_VERSION = '1.68.1'
GRPC_VERSION = grpc.__version__
_version_not_supported = False
try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True
if _version_not_supported:
    raise RuntimeError(f'The grpc package installed is at version {GRPC_VERSION},' + f' but the generated code in exabel/api/data/v1/signal_service_pb2_grpc.py depends on' + f' grpcio>={GRPC_GENERATED_VERSION}.' + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}' + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.')

class SignalServiceStub(object):
    """Service for managing raw data signals. See the User Guide for more information about raw data
    signals: https://help.exabel.com/docs/signals
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ListSignals = channel.unary_unary('/exabel.api.data.v1.SignalService/ListSignals', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_signal__service__pb2.ListSignalsRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_data_dot_v1_dot_signal__service__pb2.ListSignalsResponse.FromString, _registered_method=True)
        self.GetSignal = channel.unary_unary('/exabel.api.data.v1.SignalService/GetSignal', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_signal__service__pb2.GetSignalRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_data_dot_v1_dot_signal__messages__pb2.Signal.FromString, _registered_method=True)
        self.CreateSignal = channel.unary_unary('/exabel.api.data.v1.SignalService/CreateSignal', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_signal__service__pb2.CreateSignalRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_data_dot_v1_dot_signal__messages__pb2.Signal.FromString, _registered_method=True)
        self.UpdateSignal = channel.unary_unary('/exabel.api.data.v1.SignalService/UpdateSignal', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_signal__service__pb2.UpdateSignalRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_data_dot_v1_dot_signal__messages__pb2.Signal.FromString, _registered_method=True)
        self.DeleteSignal = channel.unary_unary('/exabel.api.data.v1.SignalService/DeleteSignal', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_signal__service__pb2.DeleteSignalRequest.SerializeToString, response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString, _registered_method=True)
        self.ListDerivedSignals = channel.unary_unary('/exabel.api.data.v1.SignalService/ListDerivedSignals', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_signal__service__pb2.ListDerivedSignalsRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_data_dot_v1_dot_signal__service__pb2.ListDerivedSignalsResponse.FromString, _registered_method=True)
        self.FilterDerivedSignals = channel.unary_unary('/exabel.api.data.v1.SignalService/FilterDerivedSignals', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_signal__service__pb2.FilterDerivedSignalsRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_data_dot_v1_dot_signal__service__pb2.FilterDerivedSignalsResponse.FromString, _registered_method=True)
        self.GetDerivedSignal = channel.unary_unary('/exabel.api.data.v1.SignalService/GetDerivedSignal', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_signal__service__pb2.GetDerivedSignalRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_data_dot_v1_dot_signal__messages__pb2.DerivedSignal.FromString, _registered_method=True)

class SignalServiceServicer(object):
    """Service for managing raw data signals. See the User Guide for more information about raw data
    signals: https://help.exabel.com/docs/signals
    """

    def ListSignals(self, request, context):
        """Lists all known signals.

        Lists all raw data signals available to your customer, including those created by you, in the
        global catalog, and from data sets you are subscribed to.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetSignal(self, request, context):
        """Gets one signal.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateSignal(self, request, context):
        """Creates one signal and returns it.

        It is also possible to create a signal by calling `UpdateSignal`
        with `allow_missing` set to `true`.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateSignal(self, request, context):
        """Updates one signal and returns it.

        This can also be used to create a signal by setting `allow_missing` to `true`.

        Note that this method will update all fields unless `update_mask` is set.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteSignal(self, request, context):
        """Deletes one signal. ALL time series for this signal will also be deleted.

        This will delete ***all*** time series for this signal.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListDerivedSignals(self, request, context):
        """Lists all known derived signals.

        Lists all derived data signals available to your customer, including those created by you, in the
        global catalog, and from data sets you are subscribed to.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def FilterDerivedSignals(self, request, context):
        """Gets all derived signals that apply to at least one of several entities.

        Selects from all derived data signals available to your customer (including those created by you, in the
        global catalog, and from data sets you are subscribed to), those signals that apply to at least one of the
        requested entities.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetDerivedSignal(self, request, context):
        """Gets one derived signal.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_SignalServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {'ListSignals': grpc.unary_unary_rpc_method_handler(servicer.ListSignals, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_signal__service__pb2.ListSignalsRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_signal__service__pb2.ListSignalsResponse.SerializeToString), 'GetSignal': grpc.unary_unary_rpc_method_handler(servicer.GetSignal, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_signal__service__pb2.GetSignalRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_signal__messages__pb2.Signal.SerializeToString), 'CreateSignal': grpc.unary_unary_rpc_method_handler(servicer.CreateSignal, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_signal__service__pb2.CreateSignalRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_signal__messages__pb2.Signal.SerializeToString), 'UpdateSignal': grpc.unary_unary_rpc_method_handler(servicer.UpdateSignal, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_signal__service__pb2.UpdateSignalRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_signal__messages__pb2.Signal.SerializeToString), 'DeleteSignal': grpc.unary_unary_rpc_method_handler(servicer.DeleteSignal, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_signal__service__pb2.DeleteSignalRequest.FromString, response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString), 'ListDerivedSignals': grpc.unary_unary_rpc_method_handler(servicer.ListDerivedSignals, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_signal__service__pb2.ListDerivedSignalsRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_signal__service__pb2.ListDerivedSignalsResponse.SerializeToString), 'FilterDerivedSignals': grpc.unary_unary_rpc_method_handler(servicer.FilterDerivedSignals, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_signal__service__pb2.FilterDerivedSignalsRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_signal__service__pb2.FilterDerivedSignalsResponse.SerializeToString), 'GetDerivedSignal': grpc.unary_unary_rpc_method_handler(servicer.GetDerivedSignal, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_signal__service__pb2.GetDerivedSignalRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_signal__messages__pb2.DerivedSignal.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('exabel.api.data.v1.SignalService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('exabel.api.data.v1.SignalService', rpc_method_handlers)

class SignalService(object):
    """Service for managing raw data signals. See the User Guide for more information about raw data
    signals: https://help.exabel.com/docs/signals
    """

    @staticmethod
    def ListSignals(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.SignalService/ListSignals', exabel_dot_api_dot_data_dot_v1_dot_signal__service__pb2.ListSignalsRequest.SerializeToString, exabel_dot_api_dot_data_dot_v1_dot_signal__service__pb2.ListSignalsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def GetSignal(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.SignalService/GetSignal', exabel_dot_api_dot_data_dot_v1_dot_signal__service__pb2.GetSignalRequest.SerializeToString, exabel_dot_api_dot_data_dot_v1_dot_signal__messages__pb2.Signal.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def CreateSignal(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.SignalService/CreateSignal', exabel_dot_api_dot_data_dot_v1_dot_signal__service__pb2.CreateSignalRequest.SerializeToString, exabel_dot_api_dot_data_dot_v1_dot_signal__messages__pb2.Signal.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def UpdateSignal(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.SignalService/UpdateSignal', exabel_dot_api_dot_data_dot_v1_dot_signal__service__pb2.UpdateSignalRequest.SerializeToString, exabel_dot_api_dot_data_dot_v1_dot_signal__messages__pb2.Signal.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def DeleteSignal(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.SignalService/DeleteSignal', exabel_dot_api_dot_data_dot_v1_dot_signal__service__pb2.DeleteSignalRequest.SerializeToString, google_dot_protobuf_dot_empty__pb2.Empty.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def ListDerivedSignals(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.SignalService/ListDerivedSignals', exabel_dot_api_dot_data_dot_v1_dot_signal__service__pb2.ListDerivedSignalsRequest.SerializeToString, exabel_dot_api_dot_data_dot_v1_dot_signal__service__pb2.ListDerivedSignalsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def FilterDerivedSignals(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.SignalService/FilterDerivedSignals', exabel_dot_api_dot_data_dot_v1_dot_signal__service__pb2.FilterDerivedSignalsRequest.SerializeToString, exabel_dot_api_dot_data_dot_v1_dot_signal__service__pb2.FilterDerivedSignalsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)

    @staticmethod
    def GetDerivedSignal(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.SignalService/GetDerivedSignal', exabel_dot_api_dot_data_dot_v1_dot_signal__service__pb2.GetDerivedSignalRequest.SerializeToString, exabel_dot_api_dot_data_dot_v1_dot_signal__messages__pb2.DerivedSignal.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)