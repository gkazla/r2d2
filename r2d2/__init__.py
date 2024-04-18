from aws_cdk.aws_apigatewayv2 import CfnStage
from aws_cdk.aws_sqs import IQueue
from b_cfn_api_v2.api import Api

from utils.base_domain import BaseDomain


class GlobDomain:
    ins: BaseDomain | None = None


class GlobLayers:
    from r2d2_layer.r2d2_layer import R2D2Layer

    r2d2: R2D2Layer | None = None


class GlobTables:
    from r2d2.db.r2d2_session_table import R2D2SessionTable

    r2d2_session_table: R2D2SessionTable | None = None


class GlobQueues:
    chatbot_sqs_fifo_queue: IQueue | None = None


class GlobApi:
    websocket: Api | None = None
    websocket_stage: CfnStage | None = None
