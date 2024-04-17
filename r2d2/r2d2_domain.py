from aws_cdk import App, Stack

from r2d2 import GlobDomain, GlobLayers
from r2d2.db.database_stack import DatabaseStack
from r2d2_layer.r2d2_layer import R2D2Layer
from utils.base_domain import BaseDomain


class R2D2Domain(BaseDomain):
    def __init__(self, scope: App | Stack, prefix: str) -> None:
        super().__init__(scope=scope, prefix=prefix, domain_name='R2D2')

        # -----------------------------------------------
        # Global access.
        # -----------------------------------------------

        if GlobDomain.ins is not None:
            raise ValueError('Domain already initialized.')

        GlobDomain.ins = self

        GlobLayers.r2d2 = R2D2Layer(
            scope=self.main_stack,
            name=GlobDomain.ins.build_name('R2D2Layer')
        )

        # -----------------------------------------------
        # Resources.
        # -----------------------------------------------

        self.database_stack = DatabaseStack(scope=self.main_stack)
