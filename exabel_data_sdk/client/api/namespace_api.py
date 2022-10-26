import logging
from typing import Sequence

from exabel_data_sdk.client.api.api_client.grpc.namespace_grpc_client import NamespaceGrpcClient
from exabel_data_sdk.client.api.data_classes.namespace import Namespace
from exabel_data_sdk.client.client_config import ClientConfig
from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import ListNamespacesRequest
from exabel_data_sdk.util.exceptions import NoWriteableNamespaceError

logger = logging.getLogger(__name__)


class NamespaceApi:
    """
    API class for retrieving namespace info from the Data API.
    """

    def __init__(self, config: ClientConfig):
        self.client = NamespaceGrpcClient(config)

    def list_namespaces(self) -> Sequence[Namespace]:
        """Lists the namespaces available to the client."""
        response = self.client.list_namespaces(ListNamespacesRequest())
        return [Namespace.from_proto(n) for n in response.namespaces]

    def get_writeable_namespace(self) -> Namespace:
        """Return the writable namespace of the current customer."""
        namespaces = self.list_namespaces()
        writable_namespaces = [ns for ns in namespaces if ns.writeable]
        if len(writable_namespaces) == 0:
            raise NoWriteableNamespaceError(
                "Current customer is not authorized to write to any namespace."
            )
        writable_namespace = writable_namespaces[0]
        if len(writable_namespaces) > 1:
            logger.warning(
                "Current customer is authorized to write to %d namespaces. Using the first "
                "lexicographical result: '%s'.",
                len(writable_namespaces),
                writable_namespace.name,
            )
        return writable_namespace
