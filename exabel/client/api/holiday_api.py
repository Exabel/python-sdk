from collections.abc import Sequence

from exabel.client.api.api_client.grpc.holiday_grpc_client import HolidayGrpcClient
from exabel.client.client_config import ClientConfig
from exabel.stubs.exabel.api.data.v1.holiday_messages_pb2 import HolidaySpecification
from exabel.stubs.exabel.api.data.v1.holiday_service_pb2 import (
    CreateHolidaySpecificationRequest,
    DeleteHolidaySpecificationRequest,
    GetHolidaySpecificationRequest,
    ListHolidaySpecificationsRequest,
    UpdateHolidaySpecificationRequest,
)


class HolidayApi:
    """
    API class for CRUD operations on holiday specifications.

    Holiday specifications define sets of holidays with their properties (dates, windows, weights)
    that can be used when forecasting with the Prophet model.

    Example:
        from exabel import ExabelClient
        from exabel.stubs.exabel.api.data.v1.holiday_messages_pb2 import (
            Holiday, HolidaySpecification
        )
        from exabel.stubs.exabel.api.time.date_pb2 import Date

        client = ExabelClient(api_key="YOUR_API_KEY")

        # Create a holiday specification
        spec = HolidaySpecification(
            display_name="US Holidays",
            holidays=[
                Holiday(
                    label="Christmas",
                    dates=[Date(year=y, month=12, day=25) for y in range(2000, 2040)],
                    lower_window=-1,
                    upper_window=1,
                    prior_scale=10.0,
                ),
            ],
        )
        created = client.holiday_api.create_holiday_specification(spec)
        print(f"Created: {created.name}")

        # Use the holiday specification in a forecast signal:
        # signal.forecast('prophet', holidays=f'{created.name}')
    """

    def __init__(self, config: ClientConfig):
        self.client = HolidayGrpcClient(config)

    def list_holiday_specifications(self) -> Sequence[HolidaySpecification]:
        """
        List all holiday specifications.

        Returns:
            A sequence of all holiday specifications.
        """
        request = ListHolidaySpecificationsRequest()
        return self.client.list_holiday_specifications(request).holiday_specifications

    def get_holiday_specification(self, name: str) -> HolidaySpecification:
        """
        Get a holiday specification by name.

        Args:
            name: The resource name of the holiday specification,
                  e.g. "holidaySpecifications/123".

        Returns:
            The holiday specification.
        """
        request = GetHolidaySpecificationRequest(name=name)
        return self.client.get_holiday_specification(request)

    def create_holiday_specification(
        self, holiday_specification: HolidaySpecification
    ) -> HolidaySpecification:
        """
        Create a new holiday specification.

        Args:
            holiday_specification: The holiday specification to create.
                The name field should not be set.

        Returns:
            The created holiday specification with its assigned name.
        """
        request = CreateHolidaySpecificationRequest(holiday_specification=holiday_specification)
        return self.client.create_holiday_specification(request)

    def update_holiday_specification(
        self, holiday_specification: HolidaySpecification
    ) -> HolidaySpecification:
        """
        Update an existing holiday specification.

        Args:
            holiday_specification: The holiday specification to update.
                The name field must be set to identify which specification to update.

        Returns:
            The updated holiday specification.
        """
        request = UpdateHolidaySpecificationRequest(holiday_specification=holiday_specification)
        return self.client.update_holiday_specification(request)

    def delete_holiday_specification(self, name: str) -> None:
        """
        Delete a holiday specification.

        Note: Deleting a holiday specification that is referenced by KPI mapping groups
        will cause forecasting to fail for those groups until the reference is removed or updated.

        Args:
            name: The resource name of the holiday specification to delete,
                  e.g. "holidaySpecifications/123".
        """
        request = DeleteHolidaySpecificationRequest(name=name)
        self.client.delete_holiday_specification(request)
