from dataclasses import dataclass
from typing import Optional

import pandas as pd

from exabel_data_sdk.client.api.data_classes.kpi_mapping_group_reference import (
    KpiMappingGroupReference,
)
from exabel_data_sdk.client.api.data_classes.model_quality import ModelQuality
from exabel_data_sdk.stubs.exabel.api.analytics.v1.kpi_messages_pb2 import (
    KpiMappingResultData as ProtoKpiMappingResultData,
)
from exabel_data_sdk.stubs.exabel.api.analytics.v1.kpi_messages_pb2 import (
    ModelQuality as ProtoModelQuality,
)


@dataclass
class KpiMappingResultData:
    """Data for a KPI mapping result.

    Attributes:
        model_mape:             The MAPE (mean absolute percentage error) for a model built using
                                only this KPI mapping.
        model_mae:              The model MAE (mean absolute error) for a model built using only
                                this KPI mapping.
        model_hit_rate:         The hit rate for a model built using only this KPI mapping.
        model_quality:          The quality of the model built using only this KPI mapping.
        number_of_data_points:  The number of data points.
        mae_pop:                The period-over-period MAE (mean absolute error).
        mae_yoy:                The year-over-year MAE (mean absolute error).
        correlation_abs:        The absolute correlation.
        correlation_pop:        The period-over-period correlation.
        correlation_yoy:        The year-over-year correlation.
        p_value_abs:            The absolute p-value.
        p_value_pop:            The period-over-period p-value.
        p_value_yoy:            The year-over-year p-value.
        last_value_date:        The last date with a value for the KPI mapping proxy signal.
    """

    source: KpiMappingGroupReference
    model_mape: Optional[float]
    model_mae: Optional[float]
    model_hit_rate: Optional[float]
    model_quality: Optional[ModelQuality]
    number_of_data_points: Optional[int]
    mae_pop: Optional[float]
    mae_yoy: Optional[float]
    correlation_abs: Optional[float]
    correlation_pop: Optional[float]
    correlation_yoy: Optional[float]
    p_value_abs: Optional[float]
    p_value_pop: Optional[float]
    p_value_yoy: Optional[float]
    last_value_date: Optional[pd.Timestamp]

    @staticmethod
    def from_proto(proto: ProtoKpiMappingResultData) -> "KpiMappingResultData":
        """Create a KpiMappingResultData from the given protobuf KpiMappingResultData."""
        return KpiMappingResultData(
            source=KpiMappingGroupReference.from_proto(proto.source),
            model_mape=proto.model_mape if proto.HasField("model_mape") else None,
            model_mae=proto.model_mae if proto.HasField("model_mae") else None,
            model_hit_rate=proto.model_hit_rate if proto.HasField("model_hit_rate") else None,
            model_quality=(
                ModelQuality.from_proto(proto.model_quality)
                if proto.model_quality != ProtoModelQuality.MODEL_QUALITY_UNSPECIFIED
                else None
            ),
            number_of_data_points=(
                proto.number_of_data_points if proto.HasField("number_of_data_points") else None
            ),
            mae_pop=(
                proto.period_over_period_mae if proto.HasField("period_over_period_mae") else None
            ),
            mae_yoy=(proto.year_over_year_mae if proto.HasField("year_over_year_mae") else None),
            correlation_abs=(
                proto.absolute_correlation if proto.HasField("absolute_correlation") else None
            ),
            correlation_pop=(
                proto.period_over_period_correlation
                if proto.HasField("period_over_period_correlation")
                else None
            ),
            correlation_yoy=(
                proto.year_over_year_correlation
                if proto.HasField("year_over_year_correlation")
                else None
            ),
            p_value_abs=proto.absolute_p_value if proto.HasField("absolute_p_value") else None,
            p_value_pop=(
                proto.period_over_period_p_value
                if proto.HasField("period_over_period_p_value")
                else None
            ),
            p_value_yoy=(
                proto.year_over_year_p_value if proto.HasField("year_over_year_p_value") else None
            ),
            last_value_date=(
                pd.Timestamp(
                    year=proto.last_value_date.year,
                    month=proto.last_value_date.month,
                    day=proto.last_value_date.day,
                )
                if proto.HasField("last_value_date")
                else None
            ),
        )
