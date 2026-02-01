from dataclasses import dataclass

import pandas as pd

from exabel_data_sdk.stubs.exabel.api.analytics.v1.kpi_messages_pb2 import (
    FiscalPeriod as ProtoFiscalPeriod,
)


@dataclass
class FiscalPeriod:
    """
    Represents a fiscal period.

    Attributes:
        period_end:  The end date of the fiscal period.
        label:       The label of the fiscal period.
        report_date: The report date of the fiscal period.
    """

    period_end: pd.Timestamp | None
    label: str | None
    report_date: pd.Timestamp | None

    @staticmethod
    def from_proto(proto: ProtoFiscalPeriod) -> "FiscalPeriod":
        """Create a FiscalPeriod from the given ProtoFiscalPeriod."""
        return FiscalPeriod(
            period_end=(
                pd.Timestamp(
                    year=proto.end_date.year,
                    month=proto.end_date.month,
                    day=proto.end_date.day,
                )
                if proto.HasField("end_date")
                else None
            ),
            label=proto.label if proto.label else None,
            report_date=(
                pd.Timestamp(
                    year=proto.report_date.year,
                    month=proto.report_date.month,
                    day=proto.report_date.day,
                )
                if proto.HasField("report_date")
                else None
            ),
        )
