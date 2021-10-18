from exabel_data_sdk import ExabelClient
from exabel_data_sdk.tests.client.api.mock_entity_api import MockEntityApi
from exabel_data_sdk.tests.client.api.mock_relationship_api import MockRelationshipApi


# pylint: disable=super-init-not-called
class ExabelMockClient(ExabelClient):
    """
    Mock of the ExabelClient that uses mock implementations of the API classes,
    which only store objects in memory.
    """

    def __init__(self):
        self.entity_api = MockEntityApi()
        self.relationship_api = MockRelationshipApi()
