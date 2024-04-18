import json
import logging
from typing import Any

import boto3
from b_lambda_layer_common.util.logging import LoggingManager
from b_lambda_layer_common.util.os_parameter import OSParameter

from r2d2_layer.models.sqs_message.chatbot_sqs_message_model import ChatbotSqsMessage
from r2d2_layer.util.chatbot_exception import ChatbotException

CHATBOT_SQS_FIFO_QUEUE_URL = OSParameter('CHATBOT_SQS_FIFO_QUEUE_URL')
SQS_CLIENT = boto3.client('sqs')

LoggingManager().setup_logging()
logger = logging.getLogger(__name__)


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    """
    R2D2 Chatbot Post Message Lambda function.

    Sends the message to the Chatbot SQS FIFO queue for further processing.

    :param event: Lambda event.
    :param context: Lambda context.

    :return: An api-gateway-formatted response.
    """
    logger.info(f'Received an event: {json.dumps(event)}')

    # ---------------------------------------------
    # Inputs.
    # ---------------------------------------------

    try:
        chatbot_sqs_message = ChatbotSqsMessage.parse_ws_event(event)
    except ChatbotException as ex:
        logger.error(repr(ex))
        return {'statusCode': 200}

    # ---------------------------------------------
    # Actions.
    # ---------------------------------------------

    SQS_CLIENT.send_message(
        QueueUrl=CHATBOT_SQS_FIFO_QUEUE_URL.value,
        MessageBody=chatbot_sqs_message.json(),
        MessageGroupId=chatbot_sqs_message.group_id
    )

    # ---------------------------------------------
    # Outputs.
    # ---------------------------------------------

    return {'statusCode': 200}
