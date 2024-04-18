from b_aws_testing_framework.tools.cdk_testing.testing_stack import TestingStack
from constructs import Construct

from r2d2.r2d2_domain import R2D2Domain


class R2d2Infrastructure(TestingStack):
    R2D2_WEBSOCKET_URL = 'R2D2WebSocketUrl'
    R2D2_CONNECTION_URL = 'R2D2ConnectionUrl'
    R2D2_SESSION_TABLE_NAME = 'R2D2SessionTableName'
    R2D2_SESSION_TABLE_REGION = 'R2D2SessionTableRegion'

    def __init__(self, scope: Construct) -> None:
        super().__init__(scope)

        self.r2d2_domain = R2D2Domain(
            scope=self,
            prefix=self.global_prefix()
        )

        self.add_output(
            key=self.R2D2_WEBSOCKET_URL,
            value=self.r2d2_domain.api_stack.websocket_stack.websocket_url
        )
        self.add_output(
            key=self.R2D2_CONNECTION_URL,
            value=self.r2d2_domain.api_stack.websocket_stack.connection_url
        )
        self.add_output(
            key=self.R2D2_SESSION_TABLE_NAME,
            value=self.r2d2_domain.database_stack.r2d2_session_table.table_name
        )
        self.add_output(
            key=self.R2D2_SESSION_TABLE_REGION,
            value=self.r2d2_domain.database_stack.r2d2_session_table.region
        )

    @staticmethod
    def name() -> str:
        return f'{TestingStack.global_prefix()}R2D2TestingStack'
