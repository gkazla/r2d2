from aws_cdk import Stack

from r2d2 import GlobDomain
from r2d2.api.websocket.routes.default_routes.default_routes_stack import DefaultWsRoutesStack


class WebsocketRoutesStack(Stack):
    def __init__(self, scope: Stack) -> None:
        stack_name = GlobDomain.ins.build_stack_name('WebsocketEndpoints')

        super().__init__(scope=scope, id=stack_name, stack_name=stack_name)

        # -----------------------------------------------
        # Stacks.
        # -----------------------------------------------

        self.default_routes_stack = DefaultWsRoutesStack(scope=self)
