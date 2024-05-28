from enum import Enum
from typing import Optional

from exabel_data_sdk.stubs.exabel.api.analytics.v1.all_pb2 import (
    PredictionModelRun as ProtoPredictionModelRun,
)
from exabel_data_sdk.stubs.exabel.api.analytics.v1.prediction_model_messages_pb2 import (
    ModelConfiguration as ProtoModelConfiguration,
)


class ModelConfiguration(Enum):
    """Specifies a model configuration."""

    # Latest configuration.
    LATEST = ProtoModelConfiguration.LATEST
    # Configuration of the active run.
    ACTIVE = ProtoModelConfiguration.ACTIVE
    # Configuration of a specific run.
    SPECIFIC_RUN = ProtoModelConfiguration.SPECIFIC_RUN


class PredictionModelRun:
    """
    A prediction model run in the Analytics API.

    Attributes:
        name (str):                         The resource name of the model run, for example
                                            "predictionModels/123/runs/4".
        description (str):                  A description of the run.
        configuration (ModelConfiguration): Which model configuration to use.
        configuration_source (int):         When using ModelConfiguration.SPECIFIC_RUN,
                                            this specifies the run from which to retrieve the
                                            configuration. It is not used for other configurations.
        auto_activate (bool):               Whether to automatically activate the run if it
                                            completes successfully. The run will not be activated
                                            if it fails for any of the entities in the model.
    """

    def __init__(
        self,
        name: Optional[str] = None,
        description: str = "",
        configuration: ModelConfiguration = ModelConfiguration.LATEST,
        configuration_source: Optional[int] = None,
        auto_activate: bool = False,
    ):
        """
        Create a prediction model run in the Analytics API.

        When creating a new prediction model run in the API, the name should be set to None.

        Args:
            name (str):                         The resource name of the model run, for example
                                                "predictionModels/123/runs/4".
            description (str):                  A description of the run.
            configuration (ModelConfiguration): Which model configuration to use.
            configuration_source (int):         When using ModelConfiguration.SPECIFIC_RUN,
                                                this specifies the run from which to retrieve the
                                                configuration. It is not used for other
                                                configurations.
            auto_activate (bool):               Whether to automatically activate the run if it
                                                completes successfully. The run will not be
                                                activated if it fails for any of the entities in
                                                the model.
        """
        self.name = name
        self.description = description
        self.configuration = configuration
        self.configuration_source = configuration_source
        self.auto_activate = auto_activate
        if self.configuration == ModelConfiguration.SPECIFIC_RUN and not self.configuration_source:
            raise ValueError(
                "The argument 'configuration_source' must be specified when using "
                "ModelConfiguration.SPECIFIC_RUN."
            )

    @staticmethod
    def from_proto(model_run: ProtoPredictionModelRun) -> "PredictionModelRun":
        """Create a PredictionModelRun from the given protobuf PredictionModelRun."""
        return PredictionModelRun(
            name=model_run.name,
            description=model_run.description,
            configuration=ModelConfiguration(model_run.configuration),
            configuration_source=(
                model_run.configuration_source
                if model_run.HasField("configuration_source")
                else None
            ),
            auto_activate=model_run.auto_activate,
        )

    def to_proto(self) -> ProtoPredictionModelRun:
        """Create a protobuf PredictionModelRun from this PredictionModelRun."""
        return ProtoPredictionModelRun(
            name=self.name,
            description=self.description,
            configuration=self.configuration.value,
            configuration_source=self.configuration_source,
            auto_activate=self.auto_activate,
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PredictionModelRun):
            return False
        return (
            self.name == other.name
            and self.description == other.description
            and self.configuration == other.configuration
            and self.configuration_source == other.configuration_source
            and self.auto_activate == other.auto_activate
        )

    def __repr__(self) -> str:
        return (
            f"PredictionModelRun(name='{self.name}', description='{self.description}', "
            f"configuration={self.configuration}, "
            f"configuration_source='{self.configuration_source}', "
            f"auto_activate={self.auto_activate})"
        )

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, PredictionModelRun):
            raise ValueError(
                f"Cannot compare PredictionModelRun to non-PredictionModelRun: {other}"
            )
        return (self.name or "") < (other.name or "")
