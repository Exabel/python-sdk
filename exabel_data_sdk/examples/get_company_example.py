from exabel_data_sdk import ExabelClient


def get_company() -> None:
    """
    Example showing how to retrieve a single company and related information from the Data API.

    The environment variable EXABEL_API_KEY must be set.
    """

    client = ExabelClient()

    # Fetch the company.
    microsoft = client.entity_api.get_entity("entityTypes/company/entities/F_000Q07-E")

    # Retrieve location of company.
    located_in_relationships = client.relationship_api.get_relationships_from_entity(
        relationship_type="relationshipTypes/LOCATED_IN", from_entity=microsoft.name
    )
    country = client.entity_api.get_entity(located_in_relationships.results[0].to_entity)

    # Retrieve web domains of the company.
    web_domain_relationships = client.relationship_api.get_relationships_to_entity(
        relationship_type="relationshipTypes/WEB_DOMAIN_OWNED_BY", to_entity=microsoft.name
    )
    web_domains = [
        client.entity_api.get_entity(e.from_entity) for e in web_domain_relationships.results
    ]

    # Retrieve primary security of company.
    primary_security_relationships = client.relationship_api.get_relationships_from_entity(
        relationship_type="relationshipTypes/HAS_PRIMARY_SECURITY", from_entity=microsoft.name
    )
    primary_security = client.entity_api.get_entity(
        primary_security_relationships.results[0].to_entity
    )

    # Retrieve primary regional for company.
    primary_regional_relationships = client.relationship_api.get_relationships_from_entity(
        relationship_type="relationshipTypes/HAS_PRIMARY_REGIONAL",
        from_entity=primary_security.name,
    )
    primary_regional = client.entity_api.get_entity(
        primary_regional_relationships.results[0].to_entity
    )

    # Retrieve primary listing for company.
    primary_listing_relationships = client.relationship_api.get_relationships_from_entity(
        relationship_type="relationshipTypes/HAS_PRIMARY_LISTING", from_entity=primary_regional.name
    )
    primary_listing = client.entity_api.get_entity(
        primary_listing_relationships.results[0].to_entity
    )

    # Retrieve all securities.
    security_relationships = client.relationship_api.get_relationships_from_entity(
        relationship_type="relationshipTypes/HAS_SECURITY", from_entity=microsoft.name
    )
    securities = [client.entity_api.get_entity(e.to_entity) for e in security_relationships.results]

    # Retrieve all regionals.
    regionals = []
    for security in securities:
        regional_relationships = client.relationship_api.get_relationships_from_entity(
            relationship_type="relationshipTypes/HAS_REGIONAL", from_entity=security.name
        )
        regionals.extend(
            [client.entity_api.get_entity(e.to_entity) for e in regional_relationships.results]
        )

    # Retrieve all listings.
    listings = []
    for regional in regionals:
        listing_relationships = client.relationship_api.get_relationships_from_entity(
            relationship_type="relationshipTypes/HAS_LISTING", from_entity=regional.name
        )
        listings.extend(
            [client.entity_api.get_entity(e.to_entity) for e in listing_relationships.results]
        )

    # Get time series for the company.
    time_series = client.time_series_api.get_entity_time_series(microsoft.name).results

    # Print results:
    print(f"Company: {microsoft}")
    print(f"Located in: {country}")
    print(f"Web domains: {web_domains}")
    print(f"Primary security: {primary_security}")
    print(f"Primary regional: {primary_regional}")
    print(f"Primary listing: {primary_listing}")
    print(f"Securities: {securities}")
    print(f"Regionals: {regionals}")
    print(f"Listings: {listings}")
    print(f"Time series: {time_series}")


if __name__ == "__main__":
    get_company()
