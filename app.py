import logging
import os

from aws_cdk import App

from r2d2.r2d2_domain import R2D2Domain

# Set up logging.
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

# Create AWS CDK application.
app = App(
    analytics_reporting=False,
    tree_metadata=False,
    stack_traces=False,
)

# Create a main stack with Amazon resources.
R2D2Domain(
    scope=app,
    prefix=os.environ['DOMAIN_PREFIX'],
)

app.synth()
