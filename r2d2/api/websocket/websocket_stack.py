from aws_cdk import Stack
from b_cfn_api_v2.api import Api

from r2d2 import GlobApi, GlobDomain
from r2d2.api.websocket.routes.websocket_routes_stack import WebsocketRoutesStack


class WebSocketStack(Stack):
    def __init__(self, scope: Stack) -> None:
        stack_name = GlobDomain.ins.build_stack_name('WebSocket')

        super().__init__(scope=scope, id=stack_name, stack_name=stack_name)

        # -----------------------------------------------
        # Websocket API.
        # -----------------------------------------------

        ws_name = GlobDomain.ins.build_name('R2D2WebSocket')

        self.websocket_api = Api(
            scope=self,
            id=ws_name,
            name=ws_name,
            description='A backend websocket API for R2D2 chatbot.',
            protocol_type='WEBSOCKET',
            route_selection_expression='$request.body.action',
        )
        self.websocket_api.enable_default_stage(stage_name='dev')

        url = (
            f'{self.websocket_api.ref}.execute-api.{scope.region}.amazonaws.com/'
            f'{self.websocket_api.default_stage.ref}/'
        )
        self.websocket_url = f'wss://{url}'
        self.connection_url = f'https://{url}'

        GlobApi.websocket = self.websocket_api
        GlobApi.websocket_stage = self.websocket_api.default_stage
        GlobApi.websocket_connection_url = self.connection_url

        # -----------------------------------------------
        # Stacks.
        # -----------------------------------------------

        self.websocket_routes_stack = WebsocketRoutesStack(scope=self)
