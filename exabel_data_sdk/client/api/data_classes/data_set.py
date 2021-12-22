from typing import Sequence

from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import DataSet as ProtoDataSet


class DataSet:
    """
    A data set resource in the Data API.

    Attributes:
        name (str):         The resource name of the data set, for example "dataSets/ns.mydata".
        display_name (str): The display name of the data set.
        description (str):  One or more paragraphs of text description.
        signals ([str]):    Resource names of signals this data set contains.
        read_only (bool):   Whether this resource is read only.
    """

    def __init__(
        self,
        name: str,
        display_name: str,
        description: str = "",
        signals: Sequence[str] = None,
        read_only: bool = False,
    ):
        """
        Create a data set resource in the Data API.

        Args:
            name (str):     The resource name of the data set, for example "dataSets/ns.mydata".
            display_name:   The display name of the data set.
            description:    One or more paragraphs of text description.
            signals:        Resource names of signals this data set contains.
            read_only:      Whether this resource is read only.
        """
        self.name = name
        self.display_name = display_name
        self.description = description
        self.read_only = read_only
        self.signals = signals or []

    @staticmethod
    def from_proto(data_set: ProtoDataSet) -> "DataSet":
        """Create an DataSet from the given protobuf DataSet."""
        return DataSet(
            name=data_set.name,
            display_name=data_set.display_name,
            description=data_set.description,
            signals=list(data_set.signals),
            read_only=data_set.read_only,
        )

    def to_proto(self) -> ProtoDataSet:
        """Create a protobuf DataSet from this DataSet."""
        return ProtoDataSet(
            name=self.name,
            display_name=self.display_name,
            description=self.description,
            signals=self.signals if self.signals else None,
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DataSet):
            return False
        return (
            self.name == other.name
            and self.display_name == other.display_name
            and self.description == other.description
            and self.read_only == other.read_only
            and sorted(self.signals) == sorted(other.signals)
        )

    def __repr__(self) -> str:
        return (
            f"DataSet(name='{self.name}', display_name='{self.display_name}', "
            f"description='{self.description}', signals={self.signals}, "
            f"read_only={self.read_only})"
        )

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, DataSet):
            raise ValueError(f"Cannot compare DataSet to non-DataSet: {other}")
        return self.name < other.name
