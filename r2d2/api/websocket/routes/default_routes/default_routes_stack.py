from aws_cdk import Stack
from aws_cdk.aws_apigatewayv2 import CfnDeployment

from r2d2 import GlobDomain, GlobApi
from r2d2.api.websocket.routes.default_routes.connect.backend import DefaultWsConnectFunction
from r2d2.api.websocket.routes.default_routes.default.backend import DefaultWsFunction
from r2d2.api.websocket.routes.default_routes.disconnect.backend import DefaultWsDisconnectFunction


class DefaultWsRoutesStack(Stack):
    def __init__(self, scope: Stack) -> None:
        stack_name = GlobDomain.ins.build_stack_name('DefaultWsRoutes')

        super().__init__(scope=scope, id=stack_name, stack_name=stack_name)

        # -----------------------------------------------
        # Functions.
        # -----------------------------------------------

        self.connect_function = DefaultWsConnectFunction(scope=self)
        self.disconnect_function = DefaultWsDisconnectFunction(scope=self)
        self.default_function = DefaultWsFunction(scope=self)

        # -----------------------------------------------
        # Routes.
        # -----------------------------------------------

        self.routes = [
            self.connect_function.route,
            self.disconnect_function.route,
            self.default_function.route,
        ]

        # -----------------------------------------------
        # Deployment.
        # -----------------------------------------------

        self.deployment = CfnDeployment(
            scope=self,
            id=GlobDomain.ins.build_name('R2D2DefaultWsRoutesDeployment'),
            api_id=GlobApi.websocket.ref,
        )

        for route in self.routes:
            self.deployment.node.add_dependency(route)
