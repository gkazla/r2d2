import json
import logging
from typing import Any

from b_lambda_layer_common.util.logging import LoggingManager

from r2d2_layer.models.sqs_message.chatbot_sqs_message_model import ChatbotSqsMessage
from r2d2_layer.util.chatbot_exception import ChatbotException
from .execute import Execute

LoggingManager().setup_logging()
logger = logging.getLogger(__name__)


def handler(event: dict[Any, Any], context: Any) -> None:
    """
    Function handling Chatbot conversation.

    :param event: Lambda event.
    :param context: Lambda context.

    :return: No return value.
    """
    logger.info(f'Received an event: {json.dumps(event)}')

    # ----------------------------------------------------
    # Inputs.
    # ----------------------------------------------------

    try:
        chatbot_sqs_message = ChatbotSqsMessage.parse_sqs_message(event)
    except ChatbotException as ex:
        logger.error(repr(ex))
        return

    # ----------------------------------------------------
    # Actions.
    # ----------------------------------------------------

    Execute(chatbot_sqs_message=chatbot_sqs_message).conversation()

    # ----------------------------------------------------
    # Outputs.
    # ----------------------------------------------------

    return
