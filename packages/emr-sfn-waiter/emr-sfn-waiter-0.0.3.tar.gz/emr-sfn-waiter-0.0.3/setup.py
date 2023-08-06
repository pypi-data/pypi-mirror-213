import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "emr-sfn-waiter",
    "version": "0.0.3",
    "description": "CDK library for an SFN workflow that polls for EMR Serverless job completion",
    "license": "MIT",
    "url": "https://github.com/alexgelman/emr-sfn-waiter",
    "long_description_content_type": "text/markdown",
    "author": "Alex Gelman<6887237+alexgelman@users.noreply.github.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/alexgelman/emr-sfn-waiter"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "emr_sfn_waiter._jsii"
    ],
    "package_data": {
        "emr_sfn_waiter._jsii": [
            "emr-sfn-waiter@0.0.3.jsii.tgz"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib==2.83.1",
        "constructs>=10.2.50, <11.0.0",
        "jsii>=1.83.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
