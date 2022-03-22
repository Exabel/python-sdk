from typing import Optional

from exabel_data_sdk.stubs.exabel.api.analytics.v1.all_pb2 import (
    PredictionModelRun as ProtoPredictionModelRun,
)


class PredictionModelRun:
    """
    A prediction model run in the Analytics API.

    Attributes:
        name (str):         The resource name of the model run, for example
                            "predictionModels/123/runs/4".
        description (str):  A description of the run.
    """

    def __init__(
        self,
        name: Optional[str] = None,
        description: str = "",
    ):
        """
        Create a prediction model run in the Analytics API.

        When creating a new prediction model run in the API, the name should be set to None.

        Args:
            name (str):         The resource name of the prediction model run, for example
                                "predictionModels/123/runs/4".
            description (str):  A description of the run.
        """
        self.name = name
        self.description = description

    @staticmethod
    def from_proto(model_run: ProtoPredictionModelRun) -> "PredictionModelRun":
        """Create a PredictionModelRun from the given protobuf PredictionModelRun."""
        return PredictionModelRun(
            name=model_run.name,
            description=model_run.description,
        )

    def to_proto(self) -> ProtoPredictionModelRun:
        """Create a protobuf PredictionModelRun from this PredictionModelRun."""
        return ProtoPredictionModelRun(
            name=self.name,
            description=self.description,
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PredictionModelRun):
            return False
        return self.name == other.name and self.description == other.description

    def __repr__(self) -> str:
        return f"PredictionModelRun(name='{self.name}', description='{self.description}'"

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, PredictionModelRun):
            raise ValueError(
                f"Cannot compare PredictionModelRun to non-PredictionModelRun: {other}"
            )
        return (self.name or "") < (other.name or "")
