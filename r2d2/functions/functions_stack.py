from aws_cdk import Stack

from r2d2 import GlobDomain
from r2d2.functions.chatbot.backend import ChatbotConversationFunction


class FunctionsStack(Stack):
    def __init__(self, scope: Stack) -> None:
        stack_name = GlobDomain.ins.build_stack_name('Functions')

        super().__init__(scope=scope, id=stack_name, stack_name=stack_name)

        # ------------------------------------------------------------
        # Functions.
        # ------------------------------------------------------------

        ChatbotConversationFunction(scope=self)
