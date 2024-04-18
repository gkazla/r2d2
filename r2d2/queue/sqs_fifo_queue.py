from aws_cdk import Stack, Duration
from aws_cdk.aws_sqs import Queue


class SqsFifoQueue(Queue):
    def __init__(
            self,
            scope: Stack,
            queue_name: str,
            content_based_deduplication: bool = True,
            receive_message_wait_time: Duration = Duration.seconds(20),
            message_visibility_timeout: Duration = Duration.seconds(60),
            message_retention_period: Duration = Duration.minutes(1)
    ) -> None:
        """
        SQS FIFO queue resource.

        :param scope: Main domain stack.
        :param queue_name: Name of the queue.
        :param content_based_deduplication: Specifies whether to enable content-based deduplication.
            During the deduplication interval (5 minutes), Amazon SQS treats messages that are sent with
            identical content (excluding attributes) as duplicates and delivers only one copy of the message.
            Default: true
        :param receive_message_wait_time: Wait time for ReceiveMessage calls. Default is max value
            of 20 seconds for long polling of the messages.
        :param message_visibility_timeout: Timeout of processing a single message. Default: Duration.seconds(60) if not set.
        :param message_retention_period: The time that Amazon SQS retains a message in the queue.
            Default: Duration.minutes(1) if not set.

        :return: No return.
        """
        super().__init__(
            scope=scope,
            id=queue_name,
            queue_name=f'{queue_name}.fifo',
            content_based_deduplication=content_based_deduplication,
            fifo=True,
            # Wait time for ReceiveMessage calls. Setting max value of 20 seconds.
            # For more information, see Amazon SQS Long Poll.
            # https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-short-and-long-polling.html
            receive_message_wait_time=receive_message_wait_time,
            # Setting SQS message visibility timeout equal to runtime of the lambda.
            # https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html
            visibility_timeout=message_visibility_timeout,
            # Setting up message retention period. Once the message retention quota is reached,
            # messages are automatically deleted.
            retention_period=message_retention_period
        )
