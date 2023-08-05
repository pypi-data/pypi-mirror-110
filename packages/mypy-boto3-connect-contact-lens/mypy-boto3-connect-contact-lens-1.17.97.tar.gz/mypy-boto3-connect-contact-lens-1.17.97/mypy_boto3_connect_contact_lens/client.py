"""
Type annotations for connect-contact-lens service client.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_connect_contact_lens/client.html)

Usage::

    ```python
    import boto3
    from mypy_boto3_connect_contact_lens import ConnectContactLensClient

    client: ConnectContactLensClient = boto3.client("connect-contact-lens")
    ```
"""
from typing import Any, Dict, Type

from botocore.client import ClientMeta

from .type_defs import ListRealtimeContactAnalysisSegmentsResponseTypeDef

__all__ = ("ConnectContactLensClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Dict[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalServiceException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]


class ConnectContactLensClient:
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/connect-contact-lens.html#ConnectContactLens.Client)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_connect_contact_lens/client.html)
    """

    meta: ClientMeta
    exceptions: Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/connect-contact-lens.html#ConnectContactLens.Client.can_paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_connect_contact_lens/client.html#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/connect-contact-lens.html#ConnectContactLens.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_connect_contact_lens/client.html#generate_presigned_url)
        """

    def list_realtime_contact_analysis_segments(
        self, *, InstanceId: str, ContactId: str, MaxResults: int = None, NextToken: str = None
    ) -> ListRealtimeContactAnalysisSegmentsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/connect-contact-lens.html#ConnectContactLens.Client.list_realtime_contact_analysis_segments)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_connect_contact_lens/client.html#list_realtime_contact_analysis_segments)
        """
