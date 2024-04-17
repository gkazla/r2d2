from aws_cdk import Stack
from aws_cdk.aws_apigatewayv2 import CfnDeployment

from r2d2 import GlobDomain, GlobApi


class CustomWsRoutesStack(Stack):
    def __init__(self, scope: Stack) -> None:
        stack_name = GlobDomain.ins.build_stack_name('CustomWsRoutes')

        super().__init__(scope=scope, id=stack_name, stack_name=stack_name)

        # -----------------------------------------------
        # Mi Assistant Endpoints Stack.
        # -----------------------------------------------

        # -----------------------------------------------
        # Routes.
        # -----------------------------------------------

        self.routes = []

        # -----------------------------------------------
        # Deployment.
        # -----------------------------------------------

        self.deployment = CfnDeployment(
            scope=self,
            id=GlobDomain.ins.build_name('R2D2CustomWsRoutesDeployment'),
            api_id=GlobApi.websocket.ref,
        )

        for route in self.routes:
            self.deployment.node.add_dependency(route)
