import os
from importlib.metadata import version

from aws_cdk import Stack
from aws_cdk.aws_lambda import Runtime
from b_cfn_lambda_layer.lambda_layer import LambdaLayer
from b_cfn_lambda_layer.package_version import PackageVersion


class R2D2Layer(LambdaLayer):
    SOURCE_PATH = os.path.dirname(__file__)

    COMPATIBLE_RUNTIMES: list[Runtime] = [
        Runtime.PYTHON_3_8,
        Runtime.PYTHON_3_9,
        Runtime.PYTHON_3_10,
        Runtime.PYTHON_3_11,
        Runtime.PYTHON_3_12,
    ]

    DEPENDENCIES = [
        'b-lambda-layer-common',
        'b-dynamodb-common',
        'openai',
        'pydantic',
        'pynamodb',
    ]

    def __init__(self, scope: Stack, name: str) -> None:
        super().__init__(
            scope=scope,
            name=name,
            source_path=self.SOURCE_PATH,
            code_runtimes=self.COMPATIBLE_RUNTIMES,
            include_source_path_directory=True,
            dependencies={
                dependency_name: PackageVersion.from_string_version(version(dependency_name))
                for dependency_name in self.DEPENDENCIES
            },
        )
