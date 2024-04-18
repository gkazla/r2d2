from typing import Any

from aws_cdk.aws_iam import PolicyStatement, Effect
from aws_cdk.aws_lambda import Code

from r2d2 import GlobDomain, GlobQueues, GlobTables
from r2d2.api.websocket.routes.custom_routes.chatbot.base_chatbot_backend import BaseChatbotBackend


class ChatbotPostMessageWsFunction(BaseChatbotBackend):
    def route_key(self) -> str:
        return 'chatbot_post_message'

    def name(self) -> str:
        return GlobDomain.ins.build_name('R2D2ChatbotPostMessageWsFunction')

    def policy_statements(self) -> list[PolicyStatement]:
        return [
            *super().policy_statements(),
            PolicyStatement(
                effect=Effect.ALLOW,
                actions=['sqs:SendMessage'],
                resources=[GlobQueues.chatbot_sqs_fifo_queue.queue_arn]
            ),
            PolicyStatement(
                effect=Effect.ALLOW,
                actions=['dynamodb:UpdateItem'],
                resources=[GlobTables.r2d2_session_table.table_arn]
            )
        ]

    def environment(self) -> dict[str, Any]:
        return {
            **super().environment(),
            'CHATBOT_SQS_FIFO_QUEUE_URL': GlobQueues.chatbot_sqs_fifo_queue.queue_url,
        }

    def code(self) -> Code:
        from .source import root

        return Code.from_asset(root)
