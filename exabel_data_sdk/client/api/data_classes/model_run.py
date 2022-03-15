from typing import Optional

from exabel_data_sdk.stubs.exabel.api.analytics.v1.all_pb2 import ModelRun as ProtoModelRun


class ModelRun:
    """
    A model run in the Analytics API.

    Attributes:
        name (str):         The resource name of the model run, for example "models/123/runs/4".
        description (str):  A description of the run.
    """

    def __init__(
        self,
        name: Optional[str] = None,
        description: str = "",
    ):
        """
        Create a model run in the Analytics API.

        When creating a new model run in the API, the name should be set to None.

        Args:
            name (str):         The resource name of the model run, for example "models/123/runs/4".
            description (str):  A description of the run.
        """
        self.name = name
        self.description = description

    @staticmethod
    def from_proto(model_run: ProtoModelRun) -> "ModelRun":
        """Create a ModelRun from the given protobuf ModelRun."""
        return ModelRun(
            name=model_run.name,
            description=model_run.description,
        )

    def to_proto(self) -> ProtoModelRun:
        """Create a protobuf ModelRun from this ModelRun."""
        return ProtoModelRun(
            name=self.name,
            description=self.description,
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ModelRun):
            return False
        return self.name == other.name and self.description == other.description

    def __repr__(self) -> str:
        return f"ModelRun(name='{self.name}', description='{self.description}'"

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, ModelRun):
            raise ValueError(f"Cannot compare ModelRun to non-ModelRun: {other}")
        return (self.name or "") < (other.name or "")
