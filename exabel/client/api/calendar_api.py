from collections.abc import Sequence

from exabel.client.api.api_client.grpc.calendar_grpc_client import CalendarGrpcClient
from exabel.client.client_config import ClientConfig
from exabel.stubs.exabel.api.data.v1.calendar_messages_pb2 import FiscalPeriod, Frequency
from exabel.stubs.exabel.api.data.v1.calendar_service_pb2 import (
    BatchCreateFiscalPeriodsRequest,
    DeleteFiscalPeriodRequest,
    GetCompanyCalendarRequest,
    ListCompaniesWithFiscalPeriodsRequest,
    ListFiscalPeriodsRequest,
)
from exabel.stubs.exabel.api.time.date_pb2 import Date
from exabel.stubs.exabel.api.time.time_range_pb2 import TimeRange


class CalendarApi:
    """API class for CRUD operations on companies’ fiscal periods."""

    def __init__(self, config: ClientConfig):
        self.client = CalendarGrpcClient(config)

    def get_company_calendar(
        self,
        company: str,
        time_range: TimeRange | None = None,
        frequency: Frequency.ValueType | None = None,
        include_unreported: bool = False,
    ) -> Sequence[FiscalPeriod]:
        """
        Get the fiscal calendar for a company.

        Args:
            company: The resource name of the company.
            time_range: The time range for fiscal periods. Returns all periods whose end date
                falls within this range. If not provided, returns all historical periods and,
                if include_unreported is True, future periods for the current fiscal year and
                two fiscal years into the future.
            frequency: The requested frequency. If not provided, uses the company's reporting
                frequency (quarterly or semi-annual).
            include_unreported: Whether to include unreported (future) fiscal periods.
                If False, only periods that have been reported are returned.

        Returns:
            A list of fiscal periods for the company, including labels, start/end dates,
            and whether each period has been reported.
        """
        request = GetCompanyCalendarRequest(
            company=company,
            time_range=time_range,
            frequency=frequency,
            include_unreported=include_unreported,
        )
        return self.client.get_company_calendar(request).periods

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
        self, company: str, frequency: Frequency.ValueType | None = None
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
