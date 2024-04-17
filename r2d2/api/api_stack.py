from aws_cdk import Stack

from r2d2 import GlobDomain
from r2d2.api.websocket.websocket_stack import WebSocketStack


class ApiStack(Stack):
    def __init__(self, scope: Stack) -> None:
        """
        API Gateway stack.

        :param scope: Main R2D2 domain stack.

        :return: No return.
        """
        stack_name = GlobDomain.ins.build_stack_name('Api')

        super().__init__(scope=scope, id=stack_name, stack_name=stack_name)

        # -----------------------------------------------
        # Stacks.
        # -----------------------------------------------

        self.websocket_stack = WebSocketStack(scope=self)
