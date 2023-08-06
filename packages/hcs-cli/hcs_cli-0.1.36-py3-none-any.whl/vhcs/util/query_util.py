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

from urllib.parse import urlencode
from typing import Any, Callable


def _remove_none(obj: dict):
    keys = list(obj.keys())
    for k in keys:
        v = obj[k]
        if v == None:
            del obj[k]
    return obj


def with_query(url: str, **kwargs: Any) -> str:
    qs = urlencode(_remove_none(dict(kwargs)))
    if qs:
        url += "?" + qs
    return url


class PageRequest:
    def __init__(self, fn_get_page: Callable, limit: int, **kwargs):
        self.limit = limit
        self.fn_get_page = fn_get_page
        self.query = _remove_none(dict(kwargs))

    def get(self) -> list:
        ret = []
        page_index = 0

        while True:
            page_size = self.limit - len(ret)
            if page_size < 1:
                break
            if page_size > 200:
                page_size = 200
            self.query["size"] = page_size
            self.query["page"] = page_index
            query_string = urlencode(self.query)
            page = self.fn_get_page(query_string)
            if not page or not page.content:
                break
            ret += page.content
            page_index += 1

        return ret
