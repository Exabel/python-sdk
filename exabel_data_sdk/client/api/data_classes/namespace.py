from dataclasses import dataclass

from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import Namespace as ProtoNamespace


@dataclass
class Namespace:
    """
    A namespace resource in the Data API.

    Attributes:
        name (str):         The resource name of the namespace on the format
                            'namespaces/<namespace_identifier>'.
        writeable (bool):   Whether the namespace is writeable for the client or not.
    """

    name: str
    writeable: bool

    @staticmethod
    def from_proto(namespace: ProtoNamespace) -> "Namespace":
        """Create a Namespace from the given protobuf Namespace."""
        return Namespace(
            name=namespace.name,
            writeable=namespace.writeable,
        )

    def to_proto(self) -> ProtoNamespace:
        """Create a protobuf Namespace from this Namespace."""
        return ProtoNamespace(
            name=self.name,
            writeable=self.writeable,
        )
