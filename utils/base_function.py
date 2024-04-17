from abc import ABC, abstractmethod
from typing import Any, cast

from aws_cdk import Duration, Stack
from aws_cdk.aws_iam import PolicyStatement
from aws_cdk.aws_lambda import Function, Code, Runtime, LayerVersion
from aws_cdk.aws_logs import RetentionDays


class BaseFunction(Function, ABC):
    def __init__(self, scope: Stack, *args, **kwargs):
        self.__scope = scope

        super().__init__(
            scope=self.__scope,
            id=self.name(),
            function_name=self.name(),
            code=self.code(),
            handler=self.handler(),
            runtime=self.runtime(),
            environment={**self.environment()},
            layers=self.layers() or None,
            log_retention=RetentionDays.ONE_MONTH,
            memory_size=self.memory(),
            timeout=self.timeout(),
            *args,
            **kwargs
        )

        for statement in self.policy_statements():
            self.add_to_role_policy(statement)

        self.__public_endpoint: None = None

    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def code(self) -> Code:
        raise NotImplementedError()

    @staticmethod
    def handler() -> str:
        return 'main.index.handler'

    @staticmethod
    def layers() -> list[LayerVersion]:
        return []

    @staticmethod
    def memory() -> int:
        return 128

    @staticmethod
    def environment() -> dict[str, Any]:
        return {}

    @staticmethod
    def policy_statements() -> list[PolicyStatement]:
        return []

    def timeout(self) -> Duration:
        return Duration.seconds(25)

    def runtime(self) -> Runtime:
        return cast(Runtime, Runtime.PYTHON_3_12)

    @property
    def scope(self):
        return self.__scope
