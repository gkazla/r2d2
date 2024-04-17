from abc import ABC

from aws_cdk import Stack, RemovalPolicy
from aws_cdk.aws_dynamodb import Attribute, Table, BillingMode, StreamViewType


class BaseTable(Table, ABC):
    def __init__(
            self,
            scope: Stack,
            table_name: str,
            partition_key: Attribute,
            sort_key: Attribute | None = None,
            stream: StreamViewType | None = None,
            time_to_live_attribute: str | None = None,
            removal_policy: RemovalPolicy = RemovalPolicy.DESTROY,
            billing_mode: BillingMode = BillingMode.PAY_PER_REQUEST,
    ) -> None:
        self.__scope = scope
        self.__table_name = table_name

        super().__init__(
            scope=scope,
            id=self.__table_name,
            table_name=self.__table_name,
            partition_key=partition_key,
            removal_policy=removal_policy,
            point_in_time_recovery=True,
            billing_mode=billing_mode,
            sort_key=sort_key,
            stream=stream,
            time_to_live_attribute=time_to_live_attribute
        )

    @property
    def table_name(self) -> str:
        """
        Table name property.

        Overrides original parent method. Calling this method will not create a dependency to this resource.

        :return: Table name.
        """
        return self.__table_name

    @property
    def table_arn(self) -> str:
        """
        Table ARN property.

        Overrides original parent method. Calling this method will not create a dependency to this resource.

        :return: Table ARN.
        """
        return f'arn:aws:dynamodb:{self.__scope.region}:{self.__scope.account}:table/{self.__table_name}'

    @property
    def region(self) -> str:
        return self.__scope.region
