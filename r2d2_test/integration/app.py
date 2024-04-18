from aws_cdk import App

from r2d2_test.integration.infrastructure import R2d2Infrastructure

app = App()
infrastructure_stack = R2d2Infrastructure(app)
app.synth()
