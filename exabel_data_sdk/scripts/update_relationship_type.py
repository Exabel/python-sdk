import argparse
import sys
from typing import Sequence

from google.protobuf.field_mask_pb2 import FieldMask

from exabel_data_sdk import ExabelClient
from exabel_data_sdk.client.api.data_classes.relationship_type import RelationshipType
from exabel_data_sdk.scripts.base_script import BaseScript


class UpdateRelationshipType(BaseScript):
    """
    Updates a relationship type.
    """

    def __init__(self, argv: Sequence[str], description: str):
        super().__init__(argv, description)
        self.parser.add_argument(
            "--name",
            required=True,
            type=str,
            help="The resource name of the relationship type, "
            "for example 'relationshipTypes/ns.relationshipTypeIdentifier'",
        )
        self.parser.add_argument(
            "--description",
            required=False,
            type=str,
            help="One or more paragraphs of text description",
        )
        self.parser.add_argument(
            "--allow-missing",
            required=False,
            action="store_true",
            help="If set to true, and the resource is not found, a new resource will be created",
        )
        is_ownership_group = self.parser.add_mutually_exclusive_group()
        is_ownership_group.add_argument(
            "--is-ownership",
            default=None,
            required=False,
            action="store_true",
            help="Whether this relationship type is a data set ownership",
        )
        is_ownership_group.add_argument(
            "--no-is-ownership",
            dest="is_ownership",
            default=None,
            required=False,
            action="store_false",
            help="Whether this relationship type is not a data set ownership",
        )

    def run_script(self, client: ExabelClient, args: argparse.Namespace) -> None:
        update_mask = []
        if args.description is not None:
            update_mask.append("description")

        if args.is_ownership is not None:
            update_mask.append("is_ownership")

        relationship_type = client.relationship_api.update_relationship_type(
            RelationshipType(
                name=args.name,
                description=args.description,
                is_ownership=args.is_ownership,
            ),
            update_mask=FieldMask(paths=update_mask),
            allow_missing=args.allow_missing,
        )
        print("Successfully updated relationship type:")
        print(relationship_type)


if __name__ == "__main__":
    UpdateRelationshipType(sys.argv, "Update a relationship type.").run()
