"""
Copyright 2023-2023 VMware Inc.
SPDX-License-Identifier: Apache-2.0

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from setuptools import setup, find_packages

from setuptools_scm import get_version
import os

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

VERSION = "0.1.36"


def get_version():
    version = VERSION
    local_version = os.environ.get("SCM_REV")
    if local_version:
        version += "+" + local_version
    return version


setup(
    version=get_version(),
    packages=find_packages(),
    install_requires=requirements,
    package_data={
        "": ["*.yaml"],
    },
    include_package_data=True,
)
