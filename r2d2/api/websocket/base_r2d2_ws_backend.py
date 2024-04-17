from abc import ABC, abstractmethod

from aws_cdk.aws_apigatewayv2 import CfnIntegration, CfnRoute
from aws_cdk.aws_iam import PolicyStatement, Effect
from aws_cdk.aws_lambda import CfnPermission

from r2d2 import GlobApi
from r2d2.base_r2d2_function import BaseR2D2Function


class BaseR2D2WsBackend(BaseR2D2Function, ABC):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.route = self.build_ws_endpoint()

    @abstractmethod
    def route_key(self) -> str:
        raise NotImplementedError()

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
        ]

    def build_ws_endpoint(self) -> CfnRoute:
        integration = CfnIntegration(
            scope=self.scope,
            id=f'{self.name()}Integration-{self.route_key()}',
            api_id=GlobApi.websocket.ref,
            integration_type='AWS_PROXY',
            integration_uri=(
                f'arn:aws:apigateway:{self.scope.region}:lambda:path/2015-03-31/functions/{self.function_arn}/invocations'
            ),
        )

        route = CfnRoute(
            scope=self.scope,
            id=f'{self.name()}Route-{self.route_key()}',
            route_key=self.route_key(),
            api_id=GlobApi.websocket.ref,
            authorization_type='NONE',
            target='integrations/' + integration.ref,
        )

        permission = CfnPermission(
            scope=self.scope,
            id=f'{self.name()}Permission-{self.route_key()}',
            action='lambda:InvokeFunction',
            principal='apigateway.amazonaws.com',
            function_name=self.function_name,
            source_arn=f'arn:aws:execute-api:{self.scope.region}:{self.scope.account}:{GlobApi.websocket.ref}/*/{self.route_key()}',
        )
        permission.node.add_dependency(self)

        return route
