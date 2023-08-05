"""
Type annotations for personalize-events service client.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_personalize_events/client.html)

Usage::

    ```python
    import boto3
    from mypy_boto3_personalize_events import PersonalizeEventsClient

    client: PersonalizeEventsClient = boto3.client("personalize-events")
    ```
"""
from typing import Any, Dict, List, Type

from botocore.client import ClientMeta

from .type_defs import EventTypeDef, ItemTypeDef, UserTypeDef

__all__ = ("PersonalizeEventsClient",)

class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str
    def __init__(self, error_response: Dict[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    InvalidInputException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]

class PersonalizeEventsClient:
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/personalize-events.html#PersonalizeEvents.Client)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_personalize_events/client.html)
    """

    meta: ClientMeta
    exceptions: Exceptions
    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/personalize-events.html#PersonalizeEvents.Client.can_paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_personalize_events/client.html#can_paginate)
        """
    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/personalize-events.html#PersonalizeEvents.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_personalize_events/client.html#generate_presigned_url)
        """
    def put_events(
        self, *, trackingId: str, sessionId: str, eventList: List[EventTypeDef], userId: str = None
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/personalize-events.html#PersonalizeEvents.Client.put_events)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_personalize_events/client.html#put_events)
        """
    def put_items(self, *, datasetArn: str, items: List[ItemTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/personalize-events.html#PersonalizeEvents.Client.put_items)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_personalize_events/client.html#put_items)
        """
    def put_users(self, *, datasetArn: str, users: List[UserTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/personalize-events.html#PersonalizeEvents.Client.put_users)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_personalize_events/client.html#put_users)
        """
