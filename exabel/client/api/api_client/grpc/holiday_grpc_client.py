from exabel.client.api.api_client.exabel_api_group import ExabelApiGroup
from exabel.client.api.api_client.grpc.base_grpc_client import BaseGrpcClient
from exabel.client.api.api_client.holiday_api_client import HolidayApiClient
from exabel.client.api.error_handler import handle_grpc_error
from exabel.client.client_config import ClientConfig
from exabel.stubs.exabel.api.data.v1.holiday_messages_pb2 import HolidaySpecification
from exabel.stubs.exabel.api.data.v1.holiday_service_pb2 import (
    CreateHolidaySpecificationRequest,
    DeleteHolidaySpecificationRequest,
    GetHolidaySpecificationRequest,
    ListHolidaySpecificationsRequest,
    ListHolidaySpecificationsResponse,
    UpdateHolidaySpecificationRequest,
)
from exabel.stubs.exabel.api.data.v1.holiday_service_pb2_grpc import HolidayServiceStub


class HolidayGrpcClient(HolidayApiClient, BaseGrpcClient):
    """
    Client which sends holiday requests to the Exabel Data API with gRPC.
    """

    def __init__(self, config: ClientConfig):
        super().__init__(config, ExabelApiGroup.DATA_API)
        self.stub = HolidayServiceStub(self.channel)

    @handle_grpc_error
    def list_holiday_specifications(
        self, request: ListHolidaySpecificationsRequest
    ) -> ListHolidaySpecificationsResponse:
        return self.stub.ListHolidaySpecifications(
            request, metadata=self.metadata, timeout=self.config.timeout
        )

    @handle_grpc_error
    def get_holiday_specification(
        self, request: GetHolidaySpecificationRequest
    ) -> HolidaySpecification:
        return self.stub.GetHolidaySpecification(
            request, metadata=self.metadata, timeout=self.config.timeout
        )

    @handle_grpc_error
    def create_holiday_specification(
        self, request: CreateHolidaySpecificationRequest
    ) -> HolidaySpecification:
        return self.stub.CreateHolidaySpecification(
            request, metadata=self.metadata, timeout=self.config.timeout
        )

    @handle_grpc_error
    def update_holiday_specification(
        self, request: UpdateHolidaySpecificationRequest
    ) -> HolidaySpecification:
        return self.stub.UpdateHolidaySpecification(
            request, metadata=self.metadata, timeout=self.config.timeout
        )

    @handle_grpc_error
    def delete_holiday_specification(self, request: DeleteHolidaySpecificationRequest) -> None:
        self.stub.DeleteHolidaySpecification(
            request, metadata=self.metadata, timeout=self.config.timeout
        )
