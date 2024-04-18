import os

from b_aws_testing_framework.credentials import Credentials
from b_aws_testing_framework.tools.cdk_testing.cdk_tool_config import CdkToolConfig
from b_aws_testing_framework.tools.cdk_testing.testing_manager import TestingManager

GLOBAL_PREFIX = os.environ.get('DOMAIN_PREFIX')
CDK_PATH = os.path.dirname(os.path.abspath(__file__))

MANAGER = TestingManager(
    credentials=Credentials(),
    config=CdkToolConfig(cdk_app_path=CDK_PATH, destroy_before_preparing=False),
)

if GLOBAL_PREFIX:
    MANAGER.set_global_prefix(GLOBAL_PREFIX)
