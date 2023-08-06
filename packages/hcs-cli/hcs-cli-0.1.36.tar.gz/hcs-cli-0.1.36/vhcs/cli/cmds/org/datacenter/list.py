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

import click
from vhcs.service import org_service
from vhcs.common.sglib.util import option_org_id, get_org_id


@click.command("list")
@option_org_id
def list_datacenters(org: str):
    """List all datacenters"""

    if org == "" or org == "all":
        ret = org_service.datacenter.list()
    else:
        org_id = get_org_id(org)
        return org_service.datacenter.find_by_org(org_id)

    return ret
