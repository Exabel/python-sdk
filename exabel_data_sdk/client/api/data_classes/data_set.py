from typing import Optional, Sequence

from exabel_data_sdk.stubs.exabel.api.data.v1.all_pb2 import DataSet as ProtoDataSet


class DataSet:
    """
    A data set resource in the Data API.

    Attributes:
        name (str):                  The resource name of the data set, for example,
                                     "dataSets/ns.mydata".
        display_name (str):          The display name of the data set.
        description (str):           One or more paragraphs of text description.
        signals ([str]):             Resource names of signals this data set contains.
        read_only (bool):            Whether this resource is read only.
        derived_signals ([str]):     Resource names of signals this data set contains.
        highlighted_signals ([str]): Resource names of signals this data set contains.
    """

    def __init__(
        self,
        name: str,
        display_name: str,
        description: str = "",
        signals: Optional[Sequence[str]] = None,
        read_only: bool = False,
        derived_signals: Optional[Sequence[str]] = None,
        highlighted_signals: Optional[Sequence[str]] = None,
    ):
        """
        Create a data set resource in the Data API.

        Args:
            name (str):          The resource name of the data set, for example,
                                 "dataSets/ns.mydata".
            display_name:        The display name of the data set.
            description:         One or more paragraphs of text description.
            signals:             Resource names of signals this data set contains.
            read_only:           Whether this resource is read only.
            derived_signals:     Resource names of derived signals for this data set.
            highlighted_signals: Resource names of highlighted signals for this data set.
        """
        self.name = name
        self.display_name = display_name
        self.description = description
        self.read_only = read_only
        self.signals = signals or []
        self.derived_signals = derived_signals or []
        self.highlighted_signals = highlighted_signals or []

    @staticmethod
    def from_proto(data_set: ProtoDataSet) -> "DataSet":
        """Create a DataSet from the given protobuf DataSet."""
        return DataSet(
            name=data_set.name,
            display_name=data_set.display_name,
            description=data_set.description,
            signals=list(data_set.signals),
            derived_signals=list(data_set.derived_signals),
            highlighted_signals=list(data_set.highlighted_signals),
            read_only=data_set.read_only,
        )

    def to_proto(self) -> ProtoDataSet:
        """Create a protobuf DataSet from this DataSet."""
        return ProtoDataSet(
            name=self.name,
            display_name=self.display_name,
            description=self.description,
            signals=self.signals if self.signals else None,
            derived_signals=self.derived_signals if self.derived_signals else None,
            highlighted_signals=self.highlighted_signals if self.highlighted_signals else None,
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
            and self.derived_signals == other.derived_signals
            and sorted(self.highlighted_signals) == sorted(other.highlighted_signals)
        )

    def __repr__(self) -> str:
        return (
            f"DataSet(name='{self.name}', display_name='{self.display_name}', "
            f"description='{self.description}', signals={self.signals}, "
            f"derived_signals={self.derived_signals}, "
            f"highlighted_signals={self.highlighted_signals}, "
            f"read_only={self.read_only})"
        )

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, DataSet):
            raise ValueError(f"Cannot compare DataSet to non-DataSet: {other}")
        return self.name < other.name


def print_data_set(data_set: DataSet) -> None:
    """Print a data set."""
    print(f"Resource name:\t{data_set.name}")
    print(f"Display name:\t{data_set.display_name}")
    print(f"Description:\t{data_set.description}")
    print("Signals:")
    for signal in sorted(data_set.signals):
        print(f"\t{signal}")
    print("Derived signals:")
    for signal in sorted(data_set.derived_signals):
        print(f"\t{signal}")
    print("Highlighted signals:")
    for signal in sorted(data_set.highlighted_signals):
        print(f"\t{signal}")
