from __future__ import annotations

from json import JSONDecodeError
from typing import Any

from b_lambda_layer_common.api_gateway.body import Body
from pydantic import BaseModel, StrictStr, ValidationError

from r2d2_layer.util.chatbot_exception import ChatbotException
from r2d2_layer.util.websocket_response import WebsocketResponse


class InputModel(BaseModel):
    connection_id: StrictStr
    session_id: StrictStr

    @classmethod
    def parse_ws_event(cls, event: dict[str, Any]) -> InputModel:
        # Connection ID is required for the WebSocket response.
        connection_id = event['requestContext']['connectionId']
        try:
            data = Body(event).from_json()
            data['connection_id'] = connection_id

            return cls.parse_obj(data)
        except (ValidationError, JSONDecodeError) as ex:
            error_message = f'Unexpected error occurred. Reason: {repr(ex)}'

            WebsocketResponse.ERROR.send(
                connection_id=connection_id,
                response_data=error_message
            )

            raise ChatbotException(error_message)
