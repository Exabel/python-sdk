from concurrent.futures import ThreadPoolExecutor

import grpc

from exabel.client.api.api_client.exabel_api_group import ExabelApiGroup
from exabel.client.api.api_client.grpc.base_grpc_client import BaseGrpcClient
from exabel.client.client_config import ClientConfig


def test_mixed_case_extra_headers_reach_grpc_server():
    received_metadata = []

    def receive(request, context):
        received_metadata.extend(context.invocation_metadata())
        return request

    with ThreadPoolExecutor(max_workers=2) as executor:
        server = grpc.server(executor)
        server.add_generic_rpc_handlers(
            [
                grpc.method_handlers_generic_handler(
                    "test.Metadata", {"Echo": grpc.unary_unary_rpc_method_handler(receive)}
                )
            ]
        )
        port = server.add_insecure_port("127.0.0.1:0")
        server.start()
        config = ClientConfig(
            api_key="NO_KEY",
            analytics_api_host="127.0.0.1",
            analytics_api_port=port,
            extra_headers=[("X-Tag", "a"), ("x-tag", "b")],
        )
        try:
            client = BaseGrpcClient(config, ExabelApiGroup.ANALYTICS_API)
            with client.channel:
                assert (
                    client.channel.unary_unary("/test.Metadata/Echo")(
                        b"payload", metadata=client.metadata, timeout=2
                    )
                    == b"payload"
                )
            assert [value for name, value in received_metadata if name == "x-tag"] == ["a", "b"]
            assert ("x-client-name", config.client_name) in received_metadata
            assert config.extra_headers == [("X-Tag", "a"), ("x-tag", "b")]
        finally:
            server.stop(None).wait()
