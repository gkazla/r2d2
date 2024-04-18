from aws_cdk.aws_iam import PolicyStatement, Effect
from aws_cdk.aws_lambda import Code

from r2d2 import GlobDomain, GlobTables
from r2d2.api.websocket.routes.custom_routes.chatbot.base_chatbot_backend import BaseChatbotBackend


class ChatbotStartSessionWsFunction(BaseChatbotBackend):
    def route_key(self) -> str:
        return 'chatbot_session_start'

    def name(self) -> str:
        return GlobDomain.ins.build_name('R2D2ChatbotStartSessionWsFunction')

    def policy_statements(self) -> list[PolicyStatement]:
        return [
            *super().policy_statements(),
            PolicyStatement(
                effect=Effect.ALLOW,
                actions=['dynamodb:PutItem'],
                resources=[GlobTables.r2d2_session_table.table_arn],
            ),
        ]

    def code(self) -> Code:
        from .source import root

        return Code.from_asset(root)
