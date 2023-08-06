import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-static-wordpress",
    "version": "0.1.9",
    "description": "Generate a static site from Wordpress (via WP2Static) using AWS CDK",
    "license": "Apache-2.0",
    "url": "https://github.com/blimmer/cdk-static-wordpress.git",
    "long_description_content_type": "text/markdown",
    "author": "Ben Limmer<hello@benlimmer.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/blimmer/cdk-static-wordpress.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_static_wordpress",
        "cdk_static_wordpress._jsii"
    ],
    "package_data": {
        "cdk_static_wordpress._jsii": [
            "cdk-static-wordpress@0.1.9.jsii.tgz"
        ],
        "cdk_static_wordpress": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.59.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.81.0, <2.0.0",
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
