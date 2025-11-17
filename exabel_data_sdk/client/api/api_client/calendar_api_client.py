from abc import ABC, abstractmethod

from exabel_data_sdk.stubs.exabel.api.data.v1.calendar_service_pb2 import (
    BatchCreateFiscalPeriodsRequest,
    BatchCreateFiscalPeriodsResponse,
    DeleteFiscalPeriodRequest,
    ListCompaniesWithFiscalPeriodsRequest,
    ListCompaniesWithFiscalPeriodsResponse,
    ListFiscalPeriodsRequest,
    ListFiscalPeriodsResponse,
)


class CalendarApiClient(ABC):
    """Superclass for clients that send calendar requests to the Exabel Data API."""

    @abstractmethod
    def batch_create_fiscal_periods(
        self, request: BatchCreateFiscalPeriodsRequest
    ) -> BatchCreateFiscalPeriodsResponse:
        """Add fiscal periods for a company."""

    @abstractmethod
    def list_company_fiscal_periods(
        self, request: ListFiscalPeriodsRequest
    ) -> ListFiscalPeriodsResponse:
        """List the fiscal periods for a company."""

    @abstractmethod
    def delete_fiscal_periods(self, request: DeleteFiscalPeriodRequest) -> None:
        """Delete fiscal periods for a company."""

    @abstractmethod
    def list_companies_with_fiscal_periods(
        self, request: ListCompaniesWithFiscalPeriodsRequest
    ) -> ListCompaniesWithFiscalPeriodsResponse:
        """List the companies for which there are uploaded fiscal periods."""
