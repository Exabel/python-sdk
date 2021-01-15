import pandas as pd
from dateutil import tz

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.entity import Entity
from exabel_data_sdk.client.api.data_classes.relationship import Relationship
from exabel_data_sdk.client.api.data_classes.relationship_type import RelationshipType
from exabel_data_sdk.client.api.data_classes.signal import Signal


def create_time_series() -> None:
    """
    Example showing how to create an entity, a relationship type, a relationship,
    a signal and a time series.

    Everything is removed again before returning.

    The environment variable EXABEL_API_KEY must be set and the namespace ("test") used in this
    example must be one of the namespaces of the customer that the api key belongs to.
    """
    customer_namespace = "test"

    client = ExabelClient()

    # Create new "brand" entity.
    brand_entity = client.entity_api.create_entity(
        Entity(
            name=f"entityTypes/brand/entities/{customer_namespace}.brand1",
            display_name="Brand 1",
            description="This is the description",
            properties={"a": True},
        ),
        entity_type="entityTypes/brand",
    )
    print(f"Created entity: {brand_entity}")

    # Create a new relationship type.
    relationship_type = client.relationship_api.create_relationship_type(
        RelationshipType(
            name=f"relationshipTypes/{customer_namespace}.BRAND_OWNED_BY",
            description="The owner of a brand, usually a company",
            properties={},
        )
    )
    print(f"Created relationship type: {relationship_type}")

    # Add a relationship between a company entity and the brand entity.
    company_entity = client.entity_api.get_entity("entityTypes/company/entities/F_000Q07-E")
    relationship = client.relationship_api.create_relationship(
        Relationship(
            description="Relationship between a company and a brand.",
            relationship_type=relationship_type.name,
            from_entity=brand_entity.name,
            to_entity=company_entity.name,
            properties={},
        )
    )
    print(f"Created relationship: {relationship}")

    # Add a signal.
    signal = client.signal_api.create_signal(
        Signal(
            name=f"signals/{customer_namespace}.signal1",
            display_name="Signal 1",
            description="description",
            entity_type="entityTypes/brand",
        )
    )
    print(f"Created signal: {signal}")

    # Create a time series.
    time_series_name = f"{brand_entity.name}/{signal.name}"
    client.time_series_api.create_time_series(
        time_series_name,
        pd.Series(
            [1, 2, 3, 4],
            index=pd.DatetimeIndex(
                ["2019-01-01", "2019-02-01", "2019-03-01", "2019-04-01"], tz=tz.tzutc()
            ),
        ),
    )

    # Retrieve time series.
    series = client.time_series_api.get_time_series(time_series_name)
    print(f"Created time series:\n{series}")

    # Delete entity, signal and relationship type
    # (relationship and time series will be implicitly deleted).
    client.entity_api.delete_entity(brand_entity.name)
    print(f"Deleted entity: {brand_entity.name}")
    client.signal_api.delete_signal(signal.name)
    print(f"Deleted signal: {signal.name}")
    client.relationship_api.delete_relationship_type(relationship_type.name)
    print(f"Deleted relationship type: {relationship_type.name}")


if __name__ == "__main__":
    create_time_series()
