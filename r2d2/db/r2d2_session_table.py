from aws_cdk import Stack
from aws_cdk.aws_dynamodb import Attribute, AttributeType

from r2d2 import GlobDomain
from utils.base_table import BaseTable


class R2D2SessionTable(BaseTable):
    def __init__(self, scope: Stack) -> None:
        super().__init__(
            scope=scope,
            table_name=GlobDomain.ins.build_name('R2D2SessionTable'),
            # PK is used to store WebSocket connection ID.
            partition_key=Attribute(name='pk', type=AttributeType.STRING),
            # SK is used to store R2D2 chatbot session ID.
            sort_key=Attribute(name='sk', type=AttributeType.STRING),
        )
