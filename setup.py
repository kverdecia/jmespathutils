#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

test_requirements: list[str] = []

setup(
    extras_require={
        "dev": [
            "mypy",
            "black",
            "vistir==0.6.1",
            "pipenv-setup[black]",
            "pre-commit",
            "types-jmespath",
            "tox",
            "invoke",
            "twine",
            "wheel",
            "zest.releaser",
            "flake8",
            "pytest",
        ]
    },
    author="Karel Antonio Verdecia Ortiz",
    author_email="kverdecia@gmail.com",
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    description="Functions for jmespath",
    install_requires=["jmespath", "xmltodict", "cuid"],
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="jmespathutils",
    name="jmespathutils",
    packages=find_packages(include=["jmespathutils", "jmespathutils.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/kverdecia/jmespathutils",
    version="0.1.3",
    zip_safe=False,
)
