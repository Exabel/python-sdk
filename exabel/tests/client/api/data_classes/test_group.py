from exabel.client.api.data_classes.group import Group
from exabel.client.api.data_classes.user import User


class TestDataSet:
    def test_proto_conversion(self):
        group = Group(
            name="groups/123",
            display_name="My Group",
            users=[User(name="users/123", email="example@example.com", blocked=False)],
        )
        assert group == Group.from_proto(group.to_proto())

    def test_equals(self):
        group_1 = Group(
            name="groups/123",
            display_name="My Group",
            users=[
                User(name="users/1", email="example@example.com", blocked=False),
                User(name="users/2", email="example@example.com", blocked=False),
            ],
        )
        group_2 = Group(
            name="groups/123",
            display_name="My Group",
            users=[],
        )

        group_3 = Group(
            name="groups/123",
            display_name="My Group",
            users=[
                User(name="users/2", email="example@example.com", blocked=False),
                User(name="users/1", email="example@example.com", blocked=False),
            ],
        )
        assert group_1 == group_3
        assert group_1 != group_2
