from aws_cdk import Stack

from r2d2 import GlobDomain, GlobTables
from r2d2.db.r2d2_session_table import R2D2SessionTable


class DatabaseStack(Stack):
    def __init__(self, scope: Stack) -> None:
        """
        CloudFormation stack for database resources.

        :param scope: Stack in which resources should be created.

        :return: No return.
        """
        stack_name = GlobDomain.ins.build_stack_name('Database')

        super().__init__(scope=scope, id=stack_name, stack_name=stack_name)

        self.r2d2_session_table = R2D2SessionTable(scope=self)

        GlobTables.r2d2_session_table = self.r2d2_session_table
