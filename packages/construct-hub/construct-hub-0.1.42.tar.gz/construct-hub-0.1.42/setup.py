import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "construct-hub",
    "version": "0.1.42",
    "description": "A construct library that model Construct Hub instances.",
    "license": "Apache-2.0",
    "url": "https://github.com/cdklabs",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services, Inc.<construct-ecosystem-team@amazon.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdklabs/construct-hub.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "construct_hub",
        "construct_hub._jsii"
    ],
    "package_data": {
        "construct_hub._jsii": [
            "construct-hub@0.1.42.jsii.tgz"
        ],
        "construct_hub": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-certificatemanager==1.108.1",
        "aws-cdk.aws-cloudfront-origins==1.108.1",
        "aws-cdk.aws-cloudfront==1.108.1",
        "aws-cdk.aws-cloudwatch-actions==1.108.1",
        "aws-cdk.aws-cloudwatch==1.108.1",
        "aws-cdk.aws-events-targets==1.108.1",
        "aws-cdk.aws-events==1.108.1",
        "aws-cdk.aws-iam==1.108.1",
        "aws-cdk.aws-lambda-event-sources==1.108.1",
        "aws-cdk.aws-lambda==1.108.1",
        "aws-cdk.aws-logs==1.108.1",
        "aws-cdk.aws-route53-targets==1.108.1",
        "aws-cdk.aws-route53==1.108.1",
        "aws-cdk.aws-s3-deployment==1.108.1",
        "aws-cdk.aws-s3==1.108.1",
        "aws-cdk.aws-sns==1.108.1",
        "aws-cdk.aws-sqs==1.108.1",
        "aws-cdk.core==1.108.1",
        "aws-cdk.cx-api==1.108.1",
        "cdk-watchful==0.5.154",
        "constructs>=3.3.69, <4.0.0",
        "jsii>=1.30.0, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Typing :: Typed",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
