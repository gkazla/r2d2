from aws_cdk.aws_iam import PolicyStatement
from aws_cdk.aws_lambda import Code

from r2d2 import GlobDomain, GlobTables
from r2d2.api.websocket.base_r2d2_ws_backend import BaseR2D2WsBackend


class DefaultWsDisconnectFunction(BaseR2D2WsBackend):
    def route_key(self) -> str:
        return '$disconnect'

    def name(self) -> str:
        return GlobDomain.ins.build_name('R2D2DefaultWsDisconnectFunction')

    def code(self) -> Code:
        from .source import root

        return Code.from_asset(root)

    def policy_statements(self) -> list[PolicyStatement]:
        return [
            *super().policy_statements(),
            PolicyStatement(
                actions=[
                    'dynamodb:Query',
                    'dynamodb:UpdateItem',
                ],
                resources=[GlobTables.r2d2_session_table.table_arn],
            )
        ]
