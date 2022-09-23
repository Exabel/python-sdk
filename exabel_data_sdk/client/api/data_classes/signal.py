from dataclasses import dataclass, field
from typing import Sequence

from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import Signal as ProtoSignal
from exabel_data_sdk.stubs.exabel.api.math.aggregation_pb2 import Aggregation


@dataclass(frozen=True)
class Signal:
    r"""
    A signal resource in the Data API.

    Attributes:
        name (str):         The resource name of the signal, for example
                            "signals/signalIdentifier" or "signals/namespace.signalIdentifier".
                            The namespace must be empty (being global) or one of the
                            predetermined namespaces the customer has access to. The signal
                            identifier must match the regex [a-zA-Z]\w{0,63}.
        display_name (str): The display name of the signal.
        description (str):  One or more paragraphs of text description.
        read_only (bool):   Whether this Signal is read only.
        entity_types (Sequence[str]):
                            The types of entities that this signal has time series for. Ignored
                            when creating a signal, but returned in the response from the API.
    """

    name: str
    display_name: str
    description: str = ""
    read_only: bool = False
    entity_types: Sequence[str] = field(default_factory=list, compare=False)

    @staticmethod
    def from_proto(signal: ProtoSignal) -> "Signal":
        """Create a Signal from the given protobuf Signal."""
        return Signal(
            name=signal.name,
            display_name=signal.display_name,
            description=signal.description,
            read_only=signal.read_only,
            entity_types=signal.entity_types,
        )

    def to_proto(self) -> ProtoSignal:
        """Create a protobuf Signal from this Signal."""
        return ProtoSignal(
            name=self.name,
            display_name=self.display_name,
            description=self.description,
            downsampling_method=Aggregation.LAST,
            read_only=self.read_only,
        )
