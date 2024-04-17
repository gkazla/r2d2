from aws_cdk import Stack

from r2d2 import GlobDomain, GlobQueues
from r2d2.queue.sqs_fifo_queue import SqsFifoQueue


class QueueStack(Stack):
    def __init__(self, scope: Stack) -> None:
        """
        SQS Queue stack.

        :param scope: Stack in which resources should be created.
        """
        stack_name = GlobDomain.ins.build_stack_name('SqsQueue')

        super().__init__(scope=scope, id=stack_name, stack_name=stack_name)

        GlobQueues.mi_assistant_sqs_fifo_queue = SqsFifoQueue(
            scope=self,
            queue_name=GlobDomain.ins.build_name('R2D2ChatbotMessageQueue'),
            content_based_deduplication=True
        )
