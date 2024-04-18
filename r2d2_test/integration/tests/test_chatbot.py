import json
import time

from websockets.sync.client import connect


def test_ROUTE_chatbot_WITH_valid_messages_EXPECT_message_received(websocket_url: str) -> None:
    """
    Check whether with a valid WebSocket messages the chatbot returns a message.

    :param websocket_url: The URL of the WebSocket.

    :return: No return.
    """
    from r2d2_layer.util.websocket_response import WebsocketResponse

    with connect(websocket_url) as connection:
        # Start Chatbot session.
        data = json.dumps(
            {
                'action': 'chatbot_session_start'
            }
        )
        connection.send(data)
        response = json.loads(connection.recv())

        response_type = response.get('type')
        # Check if the response type indicates the session start.
        assert response_type == WebsocketResponse.SESSION_START.value, (
            f'Expected {WebsocketResponse.SESSION_START.value}, got {response_type}'
        )

        session_id = response.get('data', {}).get('session_id')
        # Check if the session ID is not None.
        assert session_id, 'Session ID is None.'

        # Send user message to a chatbot.
        data = json.dumps(
            {
                'action': 'chatbot_post_message',
                'session_id': session_id,
                'system_message': 'Your are really cool writer!',
                'user_message': 'Please write for me a story about a cat.'

            }
        )

        connection.send(data)

        message = None
        retry = 0
        while retry < 10:
            response = json.loads(connection.recv())
            response_type = response.get('type')

            # Check if response type exists in the message.
            assert response_type, 'Response type is None.'

            if response_type == WebsocketResponse.MESSAGE.value or response_type == WebsocketResponse.ERROR.value:
                message = response.get('data')
                break

            time.sleep(1)
            retry += 1

        # Check if the message is not None.
        assert message, 'Chatbot message is None.'

        # End Chatbot session.
        data = json.dumps(
            {
                'action': 'chatbot_session_end',
                'session_id': session_id
            }
        )
        connection.send(data)
        response = json.loads(connection.recv())

        response_type = response.get('type')
        # Check if the response type indicates the session start.
        assert response_type == WebsocketResponse.SESSION_END.value, (
            f'Expected {WebsocketResponse.SESSION_END.value}, got {response_type}'
        )
