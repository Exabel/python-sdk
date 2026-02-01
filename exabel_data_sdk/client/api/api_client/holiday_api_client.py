from abc import ABC, abstractmethod

from exabel_data_sdk.stubs.exabel.api.data.v1.holiday_messages_pb2 import HolidaySpecification
from exabel_data_sdk.stubs.exabel.api.data.v1.holiday_service_pb2 import (
    CreateHolidaySpecificationRequest,
    DeleteHolidaySpecificationRequest,
    GetHolidaySpecificationRequest,
    ListHolidaySpecificationsRequest,
    ListHolidaySpecificationsResponse,
    UpdateHolidaySpecificationRequest,
)


class HolidayApiClient(ABC):
    """Superclass for clients that send holiday requests to the Exabel Data API."""

    @abstractmethod
    def list_holiday_specifications(
        self, request: ListHolidaySpecificationsRequest
    ) -> ListHolidaySpecificationsResponse:
        """List all holiday specifications."""

    @abstractmethod
    def get_holiday_specification(
        self, request: GetHolidaySpecificationRequest
    ) -> HolidaySpecification:
        """Get a holiday specification by name."""

    @abstractmethod
    def create_holiday_specification(
        self, request: CreateHolidaySpecificationRequest
    ) -> HolidaySpecification:
        """Create a new holiday specification."""

    @abstractmethod
    def update_holiday_specification(
        self, request: UpdateHolidaySpecificationRequest
    ) -> HolidaySpecification:
        """Update an existing holiday specification."""

    @abstractmethod
    def delete_holiday_specification(self, request: DeleteHolidaySpecificationRequest) -> None:
        """Delete a holiday specification."""
