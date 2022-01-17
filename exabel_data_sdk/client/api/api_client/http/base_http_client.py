import json
from typing import Optional, TypeVar, overload

import requests
from google.protobuf.json_format import MessageToJson, Parse
from google.protobuf.message import Message

from exabel_data_sdk.client.api.data_classes.request_error import RequestError
from exabel_data_sdk.client.api.error_handler import http_status_to_error_type
from exabel_data_sdk.client.client_config import ClientConfig

TMessage = TypeVar("TMessage", bound=Message)


class BaseHttpClient:
    """
    Base class for clients that access the Exabel Data API with JSON over HTTP.
    """

    def __init__(self, config: ClientConfig):
        self.config = config

    @overload
    def _request(
        self, method: str, url: str, response_proto: TMessage, body: Message = None
    ) -> TMessage:
        ...

    @overload
    def _request(self, method: str, url: str, response_proto: None, body: Message = None) -> None:
        ...

    def _request(
        self, method: str, url: str, response_proto: Optional[TMessage], body: Message = None
    ) -> Optional[TMessage]:
        response = requests.request(
            method,
            f"https://{self.config.host}/v1/{url}",
            data=MessageToJson(body) if body is not None else None,
            headers={
                "Accept": "application/json",
                "X-Api-Key": self.config.api_key,
            },
        )
        if response.status_code != 200:
            values = json.loads(response.content)
            raise RequestError(http_status_to_error_type(response.status_code), values["message"])
        if response_proto is None:
            return None
        return Parse(response.content, response_proto, ignore_unknown_fields=True)
