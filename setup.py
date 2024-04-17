from setuptools import find_packages, setup


with open('README.md') as file:
    README = file.read()

setup(
    name='r2d2',
    version='1.0.0',
    packages=find_packages(exclude=[
        'venv',
        'venv.*'
    ]),
    description='Domain for R2D2 chatbot.',
    long_description=README,
    long_description_content_type='text/markdown',
    include_package_data=True,
    install_requires=[
        'b-cfn-api-v2>=5.0.0,<6.0.0',
        'b-cfn-lambda-layer>=3.0.0,<4.0.0',
        'b-lambda-layer-common>=4.0.0,<5.0.0',
        'b-dynamodb-common>=0.4.1,<1.0.0',
        'pydantic==1.10.0a1',
        'pynamodb==5.5.1',
        'openai==1.20.0',
        'boto3>=1.15.0,<2.0.0',
        'setuptools',

        # --------------------------------------
        # AWS CDK dependencies.
        # --------------------------------------

        'aws-cdk-lib==2.123.0',
        'aws-cdk-constructs==2.25.0',
    ]
)
