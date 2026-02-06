import copy

from exabel.client.api.data_classes.user import User


class TestUser:
    def test_proto_conversion(self):
        user = User(name="users/123", email="example@example.com", blocked=False)
        assert user == User.from_proto(user.to_proto())

    def test_equals(self):
        user_1 = User(name="users/1", email="example@example.com", blocked=False)
        user_2 = User(name="users/2", email="example@example.com", blocked=False)
        assert user_1 == copy.copy(user_1)
        assert user_1 != user_2
