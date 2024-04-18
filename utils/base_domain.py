import os

import boto3
from aws_cdk import Environment
from aws_cdk import Stack


class BaseDomain:
    _MAIN_STACK_NAME = 'Main'

    def __init__(self, scope: Stack, prefix: str, domain_name: str) -> None:
        self._scope = scope
        self._prefix = prefix
        self._domain_name = domain_name

        self._main_stack = Stack(
            scope=self._scope,
            id=self.build_stack_name(self._MAIN_STACK_NAME),
            stack_name=self.build_stack_name(self._MAIN_STACK_NAME),
            env=Environment(
                account=boto3.client('sts').get_caller_identity()['Account'],
                region=os.environ.get('AWS_DEFAULT_REGION')
            )
        )

    @property
    def scope(self) -> Stack:
        return self._scope

    @property
    def prefix(self) -> str:
        return self._prefix

    @property
    def domain_name(self) -> str:
        return self._domain_name

    @property
    def main_stack(self) -> Stack:
        return self._main_stack

    def build_name(self, name: str) -> str:
        """
        Build domain-bound name string.

        E.g.: "MyName" -> "<prefix>MyName"


        :param name: Raw name string.

        :return: Formatted domain-bound name string.
        """
        return ''.join([self._prefix, name])

    def build_stack_name(self, name: str) -> str:
        """
        Build domain-bound stack name string.

        :param name: The name of the CloudFormation stack.

        :return: Formatted domain-bound stack name string.
        """
        return self.build_name(f'{self._domain_name}-{name}-Stack')
