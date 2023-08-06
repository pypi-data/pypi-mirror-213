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

from vhcs.common.ctxp import profile, panic
from vhcs.common.sglib import hcs_client


def hdc_service_client(service_name: str):
    url = profile.current().hcs.url
    if not url.endswith("/"):
        url += "/"
    url += service_name
    return hcs_client(url)


def _get_region_url(region_name: str):
    regions = profile.current().hcs.regions
    if not region_name:
        return regions[0].url
    for r in regions:
        if r.name.lower() == region_name.lower():
            return r.url
    names = []
    for r in regions:
        names.append(r.name)
    panic(f"Region not found: {region_name}. Available regions: {names}")


def regional_service_client(region_name: str, service_name: str):
    #'https://dev1b-westus2-cp103a.azcp.horizon.vmware.com/vmhub'
    url = _get_region_url(region_name)
    if not url:
        panic("Missing profile property: hcs.regions")
    if not url.endswith("/"):
        url += "/"
    url += service_name
    return hcs_client(url)
