from __future__ import annotations

import json
from json import JSONDecodeError
from typing import Any

from b_lambda_layer_common.api_gateway.body import Body
from pydantic import BaseModel, StrictStr, ValidationError

from r2d2_layer.util.chatbot_exception import ChatbotException
from r2d2_layer.util.websocket_response import WebsocketResponse


class ChatbotSqsMessage(BaseModel):
    connection_id: StrictStr
    session_id: StrictStr
    message_id: StrictStr
    user_message: StrictStr
    system_message: StrictStr = None
    gpt_model: StrictStr = None

    @property
    def group_id(self) -> str:
        """
        Group ID is used to group messages in the SQS FIFO queue.
        Messages with the same group ID are processed in order.

        :return: String representation of the message group ID.
        """
        return f'{self.connection_id}::{self.session_id}'

    @classmethod
    def parse_sqs_message(cls, message: dict[str, Any]) -> ChatbotSqsMessage:
        """
        Parse the SQS message to a message model.

        :param message: SQS message.

        :return: Message model instance.

        :raises ChatbotException: If the message is not valid.
        """
        record = message['Records'][0]
        message_body = json.loads(record['body'])
        connection_id = message_body['connection_id']
        try:
            return cls.parse_obj(message_body)
        except ValidationError as ex:
            error_message = f'Unexpected error occurred. Reason: {repr(ex)}'

            WebsocketResponse.ERROR.send(
                connection_id=connection_id,
                response_data=error_message
            )

            raise ChatbotException(error_message)

    @classmethod
    def parse_ws_event(cls, event: dict[str, Any]) -> ChatbotSqsMessage:
        """
        Parse the WebSocket event to a message model.

        :param event: WebSocket event.

        :return: Message model instance.

        :raises ChatbotException: If the message is not valid.
        """
        # Connection ID is required for the WebSocket response.
        connection_id = event['requestContext']['connectionId']
        # Message ID is required to make the request message unique in the SQS FIFO queue.
        # It is used to prevent the message duplication in the queue.
        # Message ID comes from the WebSocket event request context.
        # A unique server-side ID for a message and is generated by AWS API Gateway.
        message_id = event['requestContext']['messageId']
        try:
            data = Body(event).from_json()
            data['connection_id'] = connection_id
            data['message_id'] = message_id

            return cls.parse_obj(data)
        except (ValidationError, JSONDecodeError) as ex:
            error_message = f'Unexpected error occurred. Reason: {repr(ex)}'

            WebsocketResponse.ERROR.send(
                connection_id=connection_id,
                response_data=error_message
            )

            raise ChatbotException(error_message)
