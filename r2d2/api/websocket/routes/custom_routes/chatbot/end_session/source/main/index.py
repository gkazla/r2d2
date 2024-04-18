import json
import logging
from typing import Any

from b_lambda_layer_common.util.logging import LoggingManager

from r2d2_layer.util.chatbot_exception import ChatbotException
from .execute import Execute
from .input_model import InputModel

LoggingManager().setup_logging()
logger = logging.getLogger(__name__)


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    """
    Ends R2D2 chatbot session.

    :param event: Lambda event.
    :param context: Lambda context.

    :return: An api-gateway-formatted response.
    """
    logger.info(f'Received an event: {json.dumps(event)}')

    # ---------------------------------------------
    # Inputs.
    # ---------------------------------------------

    try:
        input_model = InputModel.parse_ws_event(event)
    except ChatbotException as ex:
        logger.error(repr(ex))
        return {'statusCode': 200}

    # ---------------------------------------------
    # Actions.
    # ---------------------------------------------

    Execute(input_model=input_model).end_session()

    # ---------------------------------------------
    # Outputs.
    # ---------------------------------------------

    return {'statusCode': 200}
