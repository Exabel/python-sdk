"""Client and server classes corresponding to protobuf-defined services."""
import grpc
from .....exabel.api.data.v1 import data_set_messages_pb2 as exabel_dot_api_dot_data_dot_v1_dot_data__set__messages__pb2
from .....exabel.api.data.v1 import data_set_service_pb2 as exabel_dot_api_dot_data_dot_v1_dot_data__set__service__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2

class DataSetServiceStub(object):
    """Manages data sets in the Data API.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ListDataSets = channel.unary_unary('/exabel.api.data.v1.DataSetService/ListDataSets', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_data__set__service__pb2.ListDataSetsRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_data_dot_v1_dot_data__set__service__pb2.ListDataSetsResponse.FromString)
        self.GetDataSet = channel.unary_unary('/exabel.api.data.v1.DataSetService/GetDataSet', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_data__set__service__pb2.GetDataSetRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_data_dot_v1_dot_data__set__messages__pb2.DataSet.FromString)
        self.CreateDataSet = channel.unary_unary('/exabel.api.data.v1.DataSetService/CreateDataSet', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_data__set__service__pb2.CreateDataSetRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_data_dot_v1_dot_data__set__messages__pb2.DataSet.FromString)
        self.UpdateDataSet = channel.unary_unary('/exabel.api.data.v1.DataSetService/UpdateDataSet', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_data__set__service__pb2.UpdateDataSetRequest.SerializeToString, response_deserializer=exabel_dot_api_dot_data_dot_v1_dot_data__set__messages__pb2.DataSet.FromString)
        self.DeleteDataSet = channel.unary_unary('/exabel.api.data.v1.DataSetService/DeleteDataSet', request_serializer=exabel_dot_api_dot_data_dot_v1_dot_data__set__service__pb2.DeleteDataSetRequest.SerializeToString, response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString)

class DataSetServiceServicer(object):
    """Manages data sets in the Data API.
    """

    def ListDataSets(self, request, context):
        """Lists all data sets.

        Retrieves the data set catalogue.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetDataSet(self, request, context):
        """Gets one data set.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateDataSet(self, request, context):
        """Creates one data set and returns it.

        A data set can explicitly be created using this method, or it can implicitly be created by the
        update method if its `allow_missing` parameter is set to true.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateDataSet(self, request, context):
        """Updates one data set and returns it.

        This method can also be used to create a data set, provided `allow_missing` is set to `true`.
        When this method is used to create a data set, the `update_mask` parameter is ignored.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteDataSet(self, request, context):
        """Deletes one data set.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_DataSetServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {'ListDataSets': grpc.unary_unary_rpc_method_handler(servicer.ListDataSets, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_data__set__service__pb2.ListDataSetsRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_data__set__service__pb2.ListDataSetsResponse.SerializeToString), 'GetDataSet': grpc.unary_unary_rpc_method_handler(servicer.GetDataSet, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_data__set__service__pb2.GetDataSetRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_data__set__messages__pb2.DataSet.SerializeToString), 'CreateDataSet': grpc.unary_unary_rpc_method_handler(servicer.CreateDataSet, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_data__set__service__pb2.CreateDataSetRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_data__set__messages__pb2.DataSet.SerializeToString), 'UpdateDataSet': grpc.unary_unary_rpc_method_handler(servicer.UpdateDataSet, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_data__set__service__pb2.UpdateDataSetRequest.FromString, response_serializer=exabel_dot_api_dot_data_dot_v1_dot_data__set__messages__pb2.DataSet.SerializeToString), 'DeleteDataSet': grpc.unary_unary_rpc_method_handler(servicer.DeleteDataSet, request_deserializer=exabel_dot_api_dot_data_dot_v1_dot_data__set__service__pb2.DeleteDataSetRequest.FromString, response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('exabel.api.data.v1.DataSetService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

class DataSetService(object):
    """Manages data sets in the Data API.
    """

    @staticmethod
    def ListDataSets(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.DataSetService/ListDataSets', exabel_dot_api_dot_data_dot_v1_dot_data__set__service__pb2.ListDataSetsRequest.SerializeToString, exabel_dot_api_dot_data_dot_v1_dot_data__set__service__pb2.ListDataSetsResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetDataSet(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.DataSetService/GetDataSet', exabel_dot_api_dot_data_dot_v1_dot_data__set__service__pb2.GetDataSetRequest.SerializeToString, exabel_dot_api_dot_data_dot_v1_dot_data__set__messages__pb2.DataSet.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateDataSet(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.DataSetService/CreateDataSet', exabel_dot_api_dot_data_dot_v1_dot_data__set__service__pb2.CreateDataSetRequest.SerializeToString, exabel_dot_api_dot_data_dot_v1_dot_data__set__messages__pb2.DataSet.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateDataSet(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.DataSetService/UpdateDataSet', exabel_dot_api_dot_data_dot_v1_dot_data__set__service__pb2.UpdateDataSetRequest.SerializeToString, exabel_dot_api_dot_data_dot_v1_dot_data__set__messages__pb2.DataSet.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteDataSet(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/exabel.api.data.v1.DataSetService/DeleteDataSet', exabel_dot_api_dot_data_dot_v1_dot_data__set__service__pb2.DeleteDataSetRequest.SerializeToString, google_dot_protobuf_dot_empty__pb2.Empty.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)