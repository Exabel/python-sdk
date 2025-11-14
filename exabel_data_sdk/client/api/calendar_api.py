from collections.abc import Sequence
from typing import Optional

from exabel_data_sdk.client.api.api_client.grpc.calendar_grpc_client import CalendarGrpcClient
from exabel_data_sdk.client.client_config import ClientConfig
from exabel_data_sdk.stubs.exabel.api.data.v1.calendar_messages_pb2 import FiscalPeriod, Frequency
from exabel_data_sdk.stubs.exabel.api.data.v1.calendar_service_pb2 import (
    BatchCreateFiscalPeriodsRequest,
    DeleteFiscalPeriodRequest,
    ListCompaniesWithFiscalPeriodsRequest,
    ListFiscalPeriodsRequest,
)
from exabel_data_sdk.stubs.exabel.api.time.date_pb2 import Date


class CalendarApi:
    """API class for CRUD operations on companies’ fiscal periods."""

    def __init__(self, config: ClientConfig):
        self.client = CalendarGrpcClient(config)

    def create_fiscal_periods(
        self,
        company: str,
        *,
        quarterly: Sequence[Date] = (),
        semiannual: Sequence[Date] = (),
        annual: Sequence[Date] = (),
    ) -> None:
        """
        Create fiscal periods for a company.

        Args:
            company: The resource name of the company.
            quarterly: The end dates of the quarterly fiscal periods.
            semiannual: The end dates of the semi-annual fiscal periods.
            annual: The end dates of the annual fiscal periods.
        """
        periods = self._to_fiscal_periods(quarterly=quarterly, semiannual=semiannual, annual=annual)
        if not periods:
            return
        request = BatchCreateFiscalPeriodsRequest(parent=company, periods=periods)
        self.client.batch_create_fiscal_periods(request)

    def list_fiscal_periods(
        self, company: str, frequency: Optional[Frequency.ValueType] = None
    ) -> Sequence[FiscalPeriod]:
        """
        List the fiscal periods for a company.

        Args:
            company: The resource name of the company.
            frequency: The frequency of the returned fiscal periods. If not provided, the fiscal
                periods for all the frequencies are returned.
        """
        request = ListFiscalPeriodsRequest(parent=company, frequency=frequency)
        return self.client.list_company_fiscal_periods(request).periods

    def delete_fiscal_period(
        self,
        company: str,
        date: Date,
        frequency: Frequency.ValueType,
    ) -> None:
        """
        Delete a previously added fiscal period for a company.

        Args:
            company: The resource name of the company.
            date: The end date of the fiscal period which should be deleted.
            frequency: The frequency of the fiscal period which should be deleted.
        """
        request = DeleteFiscalPeriodRequest(
            parent=company, period=FiscalPeriod(frequency=frequency, end_date=date)
        )
        self.client.delete_fiscal_periods(request)

    def delete_fiscal_periods(self, company: str) -> None:
        """
        Deletes all previously added fiscal periods for a company.

        Args:
            company: The resource name of the company.
        """
        request = DeleteFiscalPeriodRequest(parent=company)
        self.client.delete_fiscal_periods(request)

    def _to_fiscal_periods(
        self, *, quarterly: Sequence[Date], semiannual: Sequence[Date], annual: Sequence[Date]
    ) -> Sequence[FiscalPeriod]:
        periods = []
        for dates, frequency in (
            (quarterly, Frequency.QUARTERLY),
            (semiannual, Frequency.SEMIANNUAL),
            (annual, Frequency.ANNUAL),
        ):
            periods.extend([FiscalPeriod(frequency=frequency, end_date=d) for d in dates])
        return periods

    def list_companies_with_fiscal_periods(self) -> Sequence[str]:
        """
        Return a list of companies which have fiscal periods.

        Returns:
            A list containing the resource names of all the companies for which the customer has
            uploaded fiscal periods
        """
        request = ListCompaniesWithFiscalPeriodsRequest()
        return self.client.list_companies_with_fiscal_periods(request).companies
