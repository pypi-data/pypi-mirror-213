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

import os
from .jsondot import dotdict
from . import profile
from .fstore import fstore
from .util import CtxpException


_store_impl: fstore = None
_plain_profile: dict = None
_active_profile_name: str = None


def _store():
    global _store_impl, _active_profile_name, _plain_profile, _variables

    profile_name = profile.name()
    if not profile_name:
        raise CtxpException("Profile not specified")

    if profile_name != _active_profile_name:
        _active_profile_name = profile_name
        _store_impl = None

    if _store_impl == None:
        _store_impl = _context_store_from_profile_name(profile_name)
        _plain_profile = None
        _variables = None
    return _store_impl


def _context_store_from_profile_name(profile_name: str) -> fstore:
    profile_path = profile.path()
    if profile_path is None:
        return fstore(store_path=None)  # RAM only. No file persist

    profile_dir = os.path.dirname(profile.path())
    repo_dir = os.path.dirname(profile_dir)
    context_dir = os.path.join(repo_dir, "context", profile_name)
    return fstore(context_dir)


def list() -> list[str]:
    return _store().keys()


def get(name: str, reload: bool = False, default=None) -> dotdict:
    return _store().get(key=name, reload=reload, default=default)


def set(name: str, data: dict):
    return _store().save(name, data)


def delete(name: str):
    return _store().delete(name)


def clear():
    return _store().clear()


def destroy(profile_name: str):
    if profile.name() == profile_name:
        _store().destroy()
    else:
        store = _context_store_from_profile_name(profile_name)
        store.destroy()
