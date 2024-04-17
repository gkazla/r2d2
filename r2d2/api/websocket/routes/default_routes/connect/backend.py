from aws_cdk.aws_lambda import Code

from r2d2 import GlobDomain
from r2d2.api.websocket.base_r2d2_ws_backend import BaseR2D2WsBackend


class DefaultWsConnectFunction(BaseR2D2WsBackend):
    def route_key(self) -> str:
        return '$connect'

    def name(self) -> str:
        return GlobDomain.ins.build_name('R2D2DefaultWsConnectFunction')

    def code(self) -> Code:
        from .source import root

        return Code.from_asset(root)
