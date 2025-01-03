"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings
from .....exabel.api.data.v1 import import_job_service_pb2 as exabel_dot_api_dot_data_dot_v1_dot_import__job__service__pb2
GRPC_GENERATED_VERSION = '1.68.1'
GRPC_VERSION = grpc.__version__
_version_not_supported = False
try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True
if _version_not_supported:
    raise RuntimeError(f'The grpc package installed is at version {GRPC_VERSION},' + f' but the generated code in exabel/api/data/v1/import_job_service_pb2_grpc.py depends on' + f' grpcio>={GRPC_GENERATED_VERSION}.' + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}' + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.')

class ImportJobServiceStub(object):
    """Service for managing import jobs.

    As set of import job stages is run as a single import job task. See the User Guide for more
    information on import jobs: https://help.exabel.com/docs/importing-via-import-jobs

    The only current supported operation is run a given import job task.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.RunTask = channel.unary_unary('/exabel.api.data.v1.ImportJobService/RunTask', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_import__job__service__pb2.RunTaskRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_data_dot_v1_dot_import__job__service__pb2.RunTaskResponse.FromString, _registered_method=True)

class ImportJobServiceServicer(object):
    """Service for managing import jobs.

    As set of import job stages is run as a single import job task. See the User Guide for more
    information on import jobs: https://help.exabel.com/docs/importing-via-import-jobs

    The only current supported operation is run a given import job task.
    """

    def RunTask(self, request, context):
        """Runs an import task.

        Runs all the stages of an import job task.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_ImportJobServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {'RunTask': grpc.unary_unary_rpc_method_handler(servicer.RunTask, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_import__job__service__pb2.RunTaskRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_import__job__service__pb2.RunTaskResponse.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('exabel.api.data.v1.ImportJobService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('exabel.api.data.v1.ImportJobService', rpc_method_handlers)

class ImportJobService(object):
    """Service for managing import jobs.

    As set of import job stages is run as a single import job task. See the User Guide for more
    information on import jobs: https://help.exabel.com/docs/importing-via-import-jobs

    The only current supported operation is run a given import job task.
    """

    @staticmethod
    def RunTask(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.ImportJobService/RunTask', exabel_dot_api_dot_data_dot_v1_dot_import__job__service__pb2.RunTaskRequest.SerializeToString, exabel_dot_api_dot_data_dot_v1_dot_import__job__service__pb2.RunTaskResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata, _registered_method=True)