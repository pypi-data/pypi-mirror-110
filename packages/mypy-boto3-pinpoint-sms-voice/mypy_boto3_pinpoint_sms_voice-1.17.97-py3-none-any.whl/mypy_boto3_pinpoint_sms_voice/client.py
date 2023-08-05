"""
Type annotations for pinpoint-sms-voice service client.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice/client.html)

Usage::

    ```python
    import boto3
    from mypy_boto3_pinpoint_sms_voice import PinpointSMSVoiceClient

    client: PinpointSMSVoiceClient = boto3.client("pinpoint-sms-voice")
    ```
"""
from typing import Any, Dict, Type

from botocore.client import ClientMeta

from .type_defs import (
    EventDestinationDefinitionTypeDef,
    GetConfigurationSetEventDestinationsResponseTypeDef,
    SendVoiceMessageResponseTypeDef,
    VoiceMessageContentTypeDef,
)

__all__ = ("PinpointSMSVoiceClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Dict[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AlreadyExistsException: Type[BotocoreClientError]
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalServiceErrorException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]


class PinpointSMSVoiceClient:
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/pinpoint-sms-voice.html#PinpointSMSVoice.Client)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice/client.html)
    """

    meta: ClientMeta
    exceptions: Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/pinpoint-sms-voice.html#PinpointSMSVoice.Client.can_paginate)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice/client.html#can_paginate)
        """

    def create_configuration_set(self, *, ConfigurationSetName: str = None) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/pinpoint-sms-voice.html#PinpointSMSVoice.Client.create_configuration_set)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice/client.html#create_configuration_set)
        """

    def create_configuration_set_event_destination(
        self,
        *,
        ConfigurationSetName: str,
        EventDestination: EventDestinationDefinitionTypeDef = None,
        EventDestinationName: str = None
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/pinpoint-sms-voice.html#PinpointSMSVoice.Client.create_configuration_set_event_destination)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice/client.html#create_configuration_set_event_destination)
        """

    def delete_configuration_set(self, *, ConfigurationSetName: str) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/pinpoint-sms-voice.html#PinpointSMSVoice.Client.delete_configuration_set)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice/client.html#delete_configuration_set)
        """

    def delete_configuration_set_event_destination(
        self, *, ConfigurationSetName: str, EventDestinationName: str
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/pinpoint-sms-voice.html#PinpointSMSVoice.Client.delete_configuration_set_event_destination)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice/client.html#delete_configuration_set_event_destination)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/pinpoint-sms-voice.html#PinpointSMSVoice.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice/client.html#generate_presigned_url)
        """

    def get_configuration_set_event_destinations(
        self, *, ConfigurationSetName: str
    ) -> GetConfigurationSetEventDestinationsResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/pinpoint-sms-voice.html#PinpointSMSVoice.Client.get_configuration_set_event_destinations)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice/client.html#get_configuration_set_event_destinations)
        """

    def send_voice_message(
        self,
        *,
        CallerId: str = None,
        ConfigurationSetName: str = None,
        Content: VoiceMessageContentTypeDef = None,
        DestinationPhoneNumber: str = None,
        OriginationPhoneNumber: str = None
    ) -> SendVoiceMessageResponseTypeDef:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/pinpoint-sms-voice.html#PinpointSMSVoice.Client.send_voice_message)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice/client.html#send_voice_message)
        """

    def update_configuration_set_event_destination(
        self,
        *,
        ConfigurationSetName: str,
        EventDestinationName: str,
        EventDestination: EventDestinationDefinitionTypeDef = None
    ) -> Dict[str, Any]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.17.97/reference/services/pinpoint-sms-voice.html#PinpointSMSVoice.Client.update_configuration_set_event_destination)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_pinpoint_sms_voice/client.html#update_configuration_set_event_destination)
        """
