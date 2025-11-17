from exabel_data_sdk.client.api.api_client.calendar_api_client import CalendarApiClient
from exabel_data_sdk.client.api.api_client.exabel_api_group import ExabelApiGroup
from exabel_data_sdk.client.api.api_client.grpc.base_grpc_client import BaseGrpcClient
from exabel_data_sdk.client.client_config import ClientConfig
from exabel_data_sdk.stubs.exabel.api.data.v1.calendar_service_pb2 import (
    BatchCreateFiscalPeriodsRequest,
    BatchCreateFiscalPeriodsResponse,
    DeleteFiscalPeriodRequest,
    ListCompaniesWithFiscalPeriodsRequest,
    ListCompaniesWithFiscalPeriodsResponse,
    ListFiscalPeriodsRequest,
    ListFiscalPeriodsResponse,
)
from exabel_data_sdk.stubs.exabel.api.data.v1.calendar_service_pb2_grpc import CalendarServiceStub


class CalendarGrpcClient(CalendarApiClient, BaseGrpcClient):
    """
    Client which sends calendar requests to the Exabel Data API with gRPC.
    """

    def __init__(self, config: ClientConfig):
        super().__init__(config, ExabelApiGroup.DATA_API)
        self.stub = CalendarServiceStub(self.channel)

    def batch_create_fiscal_periods(
        self, request: BatchCreateFiscalPeriodsRequest
    ) -> BatchCreateFiscalPeriodsResponse:
        return self.stub.BatchCreateFiscalPeriods(
            request, metadata=self.metadata, timeout=self.config.timeout
        )

    def list_company_fiscal_periods(
        self, request: ListFiscalPeriodsRequest
    ) -> ListFiscalPeriodsResponse:
        return self.stub.ListFiscalPeriods(
            request, metadata=self.metadata, timeout=self.config.timeout
        )

    def delete_fiscal_periods(self, request: DeleteFiscalPeriodRequest) -> None:
        self.stub.DeleteFiscalPeriod(request, metadata=self.metadata, timeout=self.config.timeout)

    def list_companies_with_fiscal_periods(
        self, request: ListCompaniesWithFiscalPeriodsRequest
    ) -> ListCompaniesWithFiscalPeriodsResponse:
        return self.stub.ListCompaniesWithFiscalPeriods(
            request, metadata=self.metadata, timeout=self.config.timeout
        )
