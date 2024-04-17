import json
import logging
from typing import Any

from b_lambda_layer_common.util.logging import LoggingManager

LoggingManager().setup_logging()
logger = logging.getLogger(__name__)


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    """
    Logs a Websocket connect event.

    :param event: Lambda event.
    :param context: Lambda context.

    :return: An api-gateway-formatted response.
    """
    logger.info(f'Received an event: {json.dumps(event)}')

    # ---------------------------------------------
    # Inputs.
    # ---------------------------------------------

    try:
        connection_id = event['requestContext']['connectionId']
    except KeyError as ex:
        logger.error(f'Unexpected error while parsing request: {repr(ex)}.')
        raise

    # ---------------------------------------------
    # Actions.
    # ---------------------------------------------

    # ---------------------------------------------
    # Outputs.
    # ---------------------------------------------

    logger.info(f'Websocket connection was closed. Connection id: {connection_id}')

    return {'statusCode': 200}
