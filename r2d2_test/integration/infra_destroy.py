import os

from b_aws_cdk_parallel.deployment_executor import DeploymentExecutor
from b_aws_cdk_parallel.deployment_type import DeploymentType
from b_aws_testing_framework.tools.cdk_testing.cdk_tool_config import CdkToolConfig

from r2d2_test.integration.manager import MANAGER

DESTROY_TEST_INFRASTRUCTURE = bool(int(os.getenv('DESTROY_TEST_INFRASTRUCTURE', True)))


def inf_destroy(max_parallel_deployments: int = None):
    if not DESTROY_TEST_INFRASTRUCTURE:
        return

    def wrapper(cdk_config: CdkToolConfig):
        DeploymentExecutor(
            type=DeploymentType.DESTROY,
            path=cdk_config.cdk_app_path,
            env=cdk_config.deployment_process_environment,
            max_parallel_deployments=max_parallel_deployments,
        ).run()

    MANAGER.destroy_infrastructure(wrapper)


if __name__ == '__main__':
    inf_destroy()
