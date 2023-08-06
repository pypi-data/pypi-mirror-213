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

from . import jsondot
from typing import Any
import os


class state_file:
    def __init__(self, file_path: str):
        self._path = file_path
        self._cache = None

    def _data(self, reload: bool = False):
        if self._cache is None or reload:
            self._cache = jsondot.load(self._path, {})
        return self._cache

    def get(self, key: str, default: Any, reload: bool = False):
        return self._data(reload).get(key, default)

    def set(self, key: str, value: Any):
        self._data()[key] = value
        jsondot.save(self._cache, self._path)


_file: state_file = None


def _init(store_path: str, name: str):
    global _file
    _file = state_file(os.path.join(store_path, name))


def get(key: str, default: Any, reload: bool = False):
    return _file.get(key=key, default=default, reload=reload)


def set(key: str, value: Any):
    _file.set(key, value)
