#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2022 German Aerospace Center <amiris@dlr.de>
#
# SPDX-License-Identifier: Apache-2.0

from setuptools import find_packages, setup

__author__ = [
    "Christoph Schimeczek",  # noqa
    "Felix Nitsch",  # noqa
]
__copyright__ = "Copyright 2022, German Aerospace Center (DLR)"

__license__ = "Apache License 2.0"
__maintainer__ = "Christoph Schimeczek"  # noqa
__email__ = "amiris@dlr.de"
__status__ = "Production"


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="amirispy",  # noqa
    version="1.3",
    description="Python tools for the electricity market model AMIRIS",
    long_description=readme(),
    long_description_content_type="text/markdown",
    keywords=["AMIRIS", "agent-based modelling"],
    url="https://gitlab.com/dlr-ve/esy/amiris/amiris-py",
    author=", ".join(__author__),
    author_email=__email__,
    license=__license__,
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    entry_points={
        "console_scripts": [
            "amiris=amirispy.scripts:amiris",  # noqa
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=["pandas", "wget", "fameio>=1.8.1,<1.9"],
    extras_require={"dev": ["pytest>=7.2"]},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8",
)
