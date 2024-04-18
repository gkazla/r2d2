import os
from typing import Any

from aws_cdk import Stack, Duration
from aws_cdk.aws_iam import PolicyStatement, Effect
from aws_cdk.aws_lambda import Code
from aws_cdk.aws_lambda_event_sources import SqsEventSource

from r2d2 import GlobDomain, GlobQueues, GlobTables, GlobApi
from r2d2.base_r2d2_function import BaseR2D2Function


class ChatbotConversationFunction(BaseR2D2Function):
    def __init__(self, scope: Stack, *args, **kwargs) -> None:
        super().__init__(scope, *args, **kwargs)

        self.add_event_source(
            SqsEventSource(
                queue=GlobQueues.chatbot_sqs_fifo_queue,
                # Limiting chatbot process to a single message at a time.
                # Message group ID consist of WebSocket connection ID and chatbot session ID.
                # Messages of the different sessions will be processed in parallel.
                batch_size=1
            )
        )

    def name(self) -> str:
        return GlobDomain.ins.build_name('R2D2ChatbotConversationFunction')

    def code(self) -> Code:
        from .source import root
        return Code.from_asset(root)

    def memory(self) -> int:
        return 3009

    def timeout(self) -> Duration:
        # Function timout must match the visibility timeout of the queue.
        return Duration.seconds(60)

    def environment(self) -> dict[str, Any]:
        return {
            **super().environment(),
            'OPENAI_API_KEY': os.environ['OPENAI_API_KEY'],
            'CONNECTIONS_URL': (
                f'https://{GlobApi.websocket.ref}.execute-api.{self.scope.region}.amazonaws.com/'
                f'{GlobApi.websocket_stage.ref}'
            ),
        }

    def policy_statements(self) -> list[PolicyStatement]:
        return [
            *super().policy_statements(),
            PolicyStatement(
                effect=Effect.ALLOW,
                actions=['execute-api:ManageConnections'],
                resources=[
                    f'arn:aws:execute-api:{self.scope.region}:{self.scope.account}:{GlobApi.websocket.ref}/*'
                ],
            ),
            PolicyStatement(
                effect=Effect.ALLOW,
                actions=['dynamodb:UpdateItem'],
                resources=[GlobTables.r2d2_session_table.table_arn],
            )
        ]
