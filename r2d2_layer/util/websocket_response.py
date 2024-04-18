import json
import logging
from enum import Enum
from typing import Any

import boto3
from b_lambda_layer_common.util.os_parameter import OSParameter
from botocore.exceptions import ClientError

CONNECTIONS_URL = OSParameter('CONNECTIONS_URL')
API_CLIENT = boto3.client(
    service_name='apigatewaymanagementapi',
    api_version='2018-11-29',
    endpoint_url=CONNECTIONS_URL.value,
)

logger = logging.getLogger(__name__)

__all__ = ['WebsocketResponse']


class WebsocketResponse(Enum):
    SESSION_START = 'session_start'
    SESSION_END = 'session_end'
    PROCESSING_START = 'processing_start'
    PROCESSING_END = 'processing_end'
    MESSAGE = 'message'
    ERROR = 'error'

    def send(self, connection_id: str, response_data: str | dict[str, Any] | None = None) -> None:
        """
        Send a message to the WebSocket connection.

        :param connection_id: WebSocket connection ID.
        :param response_data: Data to send.

        :return: No return.
        """
        message = json.dumps(
            {
                'type': self.value,
                'data': response_data,
            }
        ).encode('UTF-8')

        try:
            API_CLIENT.post_to_connection(
                Data=message,
                ConnectionId=connection_id,
            )
        except ClientError as ex:
            logger.error(f'Failed to send a message to the connection: {repr(ex)}.')
