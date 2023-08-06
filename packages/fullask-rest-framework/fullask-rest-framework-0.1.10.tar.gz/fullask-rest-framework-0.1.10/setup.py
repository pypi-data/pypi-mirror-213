#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

with open("README.md") as readme_file:
    readme = readme_file.read()

requirements = [
    "Flask",
    "flask-jwt-extended",
    "flask-sqlalchemy",
    "flask-marshmallow",
    "flask-migrate",
    "flask-smorest",
    "flask-cors",
    "python-dotenv",
    "dependency-injector",
    "marshmallow",
    "marshmallow-sqlalchemy",
]

test_requirements = []

setup(
    author="tgoddessana",
    author_email="twicegoddessana1229@gmail.com",
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    description="A fully-supported flask extension to build REST API.",
    entry_points={
        "console_scripts": ["fullask-manager=fullask_rest_framework.cli:main"],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    name="fullask-rest-framework",
    packages=find_packages(
        include=["fullask_rest_framework", "fullask_rest_framework.*"]
    ),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/tgoddessana/fullask-rest-framework",
    version="0.1.10",
    zip_safe=False,
)
