from r2d2_layer.models.session.session_model import Session
from r2d2_layer.util.websocket_response import WebsocketResponse
from .input_model import InputModel


class Execute:
    def __init__(self, input_model: InputModel) -> None:
        self.__input_model = input_model

    def start_session(self) -> None:
        """
        Start a new R2D2 Chatbot session.

        :return: No return
        """
        session = Session.create_session(
            connection_id=self.__input_model.connection_id,
            gpt_model=self.__input_model.gpt_model
        )

        WebsocketResponse.SESSION_START.send(
            connection_id=self.__input_model.connection_id,
            response_data={
                'session_id': session.session_id
            }
        )
