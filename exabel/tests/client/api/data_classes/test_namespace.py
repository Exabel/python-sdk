from exabel.client.api.data_classes.namespace import Namespace


class TestNamespace:
    def test_proto_conversion(self):
        namespace = Namespace(
            name="namespace/ns",
            writeable=True,
        )
        assert namespace == Namespace.from_proto(namespace.to_proto())
