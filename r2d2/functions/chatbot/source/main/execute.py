import logging

from b_lambda_layer_common.exceptions.container.not_found_error import NotFoundError

from r2d2_layer.models.session.session_model import Session
from r2d2_layer.models.sqs_message.chatbot_sqs_message_model import ChatbotSqsMessage
from r2d2_layer.util.websocket_response import WebsocketResponse
from .utils.chat_completion import ChatCompletion, Message, MessageRole

logger = logging.getLogger(__name__)


class Execute:
    def __init__(self, chatbot_sqs_message: ChatbotSqsMessage) -> None:
        self._chatbot_sqs_message = chatbot_sqs_message

    def conversation(self) -> None:
        WebsocketResponse.PROCESSING_START.send(connection_id=self._chatbot_sqs_message.connection_id)

        if not (session := self._get_session()):
            return

        messages = []
        # Load the messages from the session.
        if session.messages:
            messages = [Message.from_dict(message) for message in session.messages]

        # Add the new user and system messages.
        messages.append(Message(role=MessageRole.USER, content=self._chatbot_sqs_message.user_message))
        if self._chatbot_sqs_message.system_message:
            messages.append(Message(role=MessageRole.SYSTEM, content=self._chatbot_sqs_message.system_message))

        chat_completion = ChatCompletion(gpt_model=self._chatbot_sqs_message.gpt_model or session.gpt_model)
        chat_completion.messages = messages

        response = chat_completion.chat()

        if not response:
            session.update_session(gpt_model=chat_completion.gpt_model)

            message = 'Unable to process the request. Please try again later.'
            logger.warning(message)
            WebsocketResponse.ERROR.send(
                connection_id=self._chatbot_sqs_message.connection_id,
                response_data=message
            )
            return

        session.update_session(gpt_model=chat_completion.gpt_model, messages=chat_completion.messages)
        WebsocketResponse.MESSAGE.send(
            connection_id=self._chatbot_sqs_message.connection_id,
            response_data=response
        )
        WebsocketResponse.PROCESSING_END.send(connection_id=self._chatbot_sqs_message.connection_id)

    def _get_session(self) -> Session | None:
        try:
            return Session.get_session(
                connection_id=self._chatbot_sqs_message.connection_id,
                session_id=self._chatbot_sqs_message.session_id,
                consistent_read=True
            )
        except NotFoundError as ex:
            logger.warning(repr(ex))
            WebsocketResponse.ERROR.send(
                connection_id=self._chatbot_sqs_message.connection_id,
                response_data=ex.message()
            )
            return
