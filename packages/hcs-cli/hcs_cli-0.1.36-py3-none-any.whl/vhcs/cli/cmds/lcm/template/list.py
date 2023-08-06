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
from vhcs.service import lcm
from vhcs.common.sglib.util import option_org_id, get_org_id
from vhcs.common.ctxp.util import option_id_only


@click.command("list")
@click.option(
    "--limit", "-l", type=int, required=False, default=20, help="Optionally, specify the number of records to return."
)
@option_org_id
@option_id_only
@click.option("--type", "-t", type=str, required=False, help="Optionally, specify cloud provider type.")
@click.option("--name", "-n", type=str, required=False, help="Optionally, specify name pattern to find.")
def list_templates(limit: int, org: str, id_only: bool, type: str, name: str):
    """List templates"""
    if org == "all":
        ret = lcm.template.list(limit, name=name, type=type)
    else:
        ret = lcm.template.list(limit, org_id=get_org_id(org), name=name, type=type)

    if id_only:

        def _get_id_only(t):
            return t.get("id")

        return list(map(_get_id_only, ret))

    return ret
