from typing import Dict

from setuptools import find_packages, setup


def get_version() -> str:
    version: Dict[str, str] = {}
    with open("dagster_cloud/version.py") as fp:
        exec(fp.read(), version)  # pylint: disable=W0122

    return version["__version__"]


setup(
    name="dagster_cloud",
    version=get_version(),
    author_email="hello@elementl.com",
    packages=find_packages(exclude=["dagster_cloud_tests"]),
    include_package_data=True,
    install_requires=["dagster", "gql<3", "kubernetes"],
    extras_require={
        "tests": [
            "docker",
            "mypy==0.812",
            "pylint",
            "pytest",
            "black",
            "isort",
            "kubernetes",
            "dagster_k8s",
        ],
        "docker": ["docker"],
        "kubernetes": ["kubernetes", "dagster_k8s"],
    },
    author="Elementl",
    license="Apache-2.0",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "dagster-cloud = dagster_cloud.cli:main",
        ]
    },
)
