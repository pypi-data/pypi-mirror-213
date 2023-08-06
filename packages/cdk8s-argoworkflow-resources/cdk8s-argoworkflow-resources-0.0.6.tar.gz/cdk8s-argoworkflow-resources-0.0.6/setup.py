import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk8s-argoworkflow-resources",
    "version": "0.0.6",
    "description": "@opencdk8s/cdk8s-argoworkflow",
    "license": "Apache-2.0",
    "url": "https://github.com/opencdk8s/cdk8s-argoworkflow-resources.git",
    "long_description_content_type": "text/markdown",
    "author": "Gagan Singh<gaganpreet.singh@smallcase.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/opencdk8s/cdk8s-argoworkflow-resources.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk8s_argoworkflow_resources",
        "cdk8s_argoworkflow_resources._jsii",
        "cdk8s_argoworkflow_resources.k8s"
    ],
    "package_data": {
        "cdk8s_argoworkflow_resources._jsii": [
            "cdk8s-argoworkflow@0.0.6.jsii.tgz"
        ],
        "cdk8s_argoworkflow_resources": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "cdk8s>=2.2.74, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.61.0, <2.0.0",
        "publication>=0.0.3"
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
