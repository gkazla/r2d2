import logging

from b_lambda_layer_common.exceptions.container.not_found_error import NotFoundError

from r2d2_layer.models.session.session_model import Session, SessionStatus
from r2d2_layer.util.websocket_response import WebsocketResponse
from .input_model import InputModel

logger = logging.getLogger(__name__)


class Execute:
    def __init__(self, input_model: InputModel) -> None:
        self.__input_model = input_model

    def end_session(self) -> None:
        """
        Ends R2D2 chatbot session.

        :return: No return.
        """
        try:
            session = Session.get_session(
                session_id=self.__input_model.session_id,
                connection_id=self.__input_model.connection_id,
                consistent_read=True
            )
        except NotFoundError as ex:
            logger.error(ex.message())
            WebsocketResponse.ERROR.send(
                connection_id=self.__input_model.connection_id,
                response_data=ex.message()
            )
            return

        session.update_session(session_status=SessionStatus.CLOSED)
        WebsocketResponse.SESSION_END.send(
            connection_id=self.__input_model.connection_id
        )
