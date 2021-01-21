from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import Signal as ProtoSignal
from exabel_data_sdk.stubs.exabel.api.math.aggregation_pb2 import Aggregation


class Signal:
    r"""
    A signal resource in the Data API.

    Attributes:
        name:         The resource name of the signal, for example "signals/signalIdentifier" or
                      "signals/namespace.signalIdentifier". The namespace must be empty (being
                      global) or one of the predetermined namespaces the customer has access to. The
                      signal identifier must match the regex [a-zA-Z]\w{0,63}.
        entity_type:  The entity type this signal is related to, for example "entityTypes/ns.type1".
                      This cannot be changed after the signal has been created. If the entity type
                      namespace is not empty, it must be equal to the signal's namespace.
        display_name: The display name of the signal.
        description:  One or more paragraphs of text description.
        read_only:    Whether this Signal is read only.
    """

    def __init__(
        self,
        name: str,
        entity_type: str,
        display_name: str,
        description: str,
        read_only: bool = False,
    ):
        self.name = name
        self.entity_type = entity_type
        self.display_name = display_name
        self.description = description
        self.read_only = read_only

    @staticmethod
    def from_proto(signal: ProtoSignal) -> "Signal":
        """Create a Signal from the given protobuf Signal."""
        return Signal(
            name=signal.name,
            display_name=signal.display_name,
            description=signal.description,
            read_only=signal.read_only,
            entity_type=signal.entity_type,
        )

    def to_proto(self) -> ProtoSignal:
        """Create a protobuf Signal from this Signal."""
        return ProtoSignal(
            name=self.name,
            display_name=self.display_name,
            description=self.description,
            entity_type=self.entity_type,
            downsampling_method=Aggregation.LAST,
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Signal):
            return False
        return (
            self.name == other.name
            and self.entity_type == other.entity_type
            and self.display_name == other.display_name
            and self.description == other.description
            and self.read_only == other.read_only
        )

    def __repr__(self) -> str:
        return (
            f"Signal(name='{self.name}', entity_type='{self.entity_type}', "
            f"display_name='{self.display_name}', description='{self.description}', "
            f"read_only={self.read_only})"
        )
