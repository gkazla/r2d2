from abc import ABC
from typing import Any, cast

from aws_cdk.aws_iam import PolicyStatement
from aws_cdk.aws_lambda import Runtime

from r2d2 import GlobLayers, GlobTables
from utils.base_function import BaseFunction


class BaseR2D2Function(BaseFunction, ABC):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        GlobLayers.r2d2.add_to_function(self)

    @staticmethod
    def environment() -> dict[str, Any]:
        return {
            'R2D2_SESSION_TABLE_NAME': GlobTables.r2d2_session_table.table_name,
            'R2D2_SESSION_TABLE_REGION': GlobTables.r2d2_session_table.region,
        }

    def runtime(self) -> Runtime:
        return cast(Runtime, Runtime.PYTHON_3_12)

    @staticmethod
    def policy_statements() -> list[PolicyStatement]:
        return [
            PolicyStatement(
                actions=[
                    'dynamodb:GetItem',
                ],
                resources=[
                    GlobTables.r2d2_session_table.table_arn,
                ],
            )
        ]
