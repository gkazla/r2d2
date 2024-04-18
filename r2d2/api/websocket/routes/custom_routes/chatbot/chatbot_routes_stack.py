from aws_cdk import Stack

from r2d2 import GlobDomain
from r2d2.api.websocket.routes.custom_routes.chatbot.end_session.backend import ChatbotEndSessionWsFunction
from r2d2.api.websocket.routes.custom_routes.chatbot.post_message.backend import ChatbotPostMessageWsFunction
from r2d2.api.websocket.routes.custom_routes.chatbot.start_session.backend import ChatbotStartSessionWsFunction


class ChatbotRoutesStack(Stack):
    def __init__(self, scope: Stack) -> None:
        stack_name = GlobDomain.ins.build_stack_name('ChatbotRoutes')

        super().__init__(scope=scope, id=stack_name, stack_name=stack_name)

        # -----------------------------------------------
        # Functions.
        # -----------------------------------------------

        chatbot_start_session_function = ChatbotStartSessionWsFunction(scope=self)
        chatbot_end_session_function = ChatbotEndSessionWsFunction(scope=self)
        chatbot_post_message_function = ChatbotPostMessageWsFunction(scope=self)

        # -----------------------------------------------
        # Routes.
        # -----------------------------------------------

        self.routes = [
            chatbot_start_session_function.route,
            chatbot_end_session_function.route,
            chatbot_post_message_function.route,
        ]
