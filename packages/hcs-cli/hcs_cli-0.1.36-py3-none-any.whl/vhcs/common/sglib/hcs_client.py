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

from vhcs.common.ctxp import context, profile
from .ez_client import EzClient
from . import auth as auth


def _get_auth(client: EzClient, force: bool):
    auth_data = auth.login()
    return "authorization", f"Bearer {auth_data.token}"


def hcs_client(url: str, login: bool = False) -> EzClient:
    if not url:
        url = profile.current().hcs.url
    if url.endswith("/"):
        url = url[:-1]
    _client = EzClient(url, _get_auth)
    if login:
        _client.login()
        context.set("orgId", auth.data().org.id)
    return _client
