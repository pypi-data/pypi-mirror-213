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

import json
import yaml
import sys
import click
from typing import Any


class CtxpException(Exception):
    pass


def print_output(data: Any, output: str = "json", fields: str = None):
    if type(data) is str:
        text = data
    else:
        _filter_fields(data, fields)

        if output == "json":
            text = json.dumps(data, indent=4)
        elif output == "json-compact":
            text = json.dumps(data)
        elif output == "yaml":
            import vhcs.common.ctxp as ctxp

            text = yaml.dump(ctxp.jsondot.plain(data))
        elif output == "text":
            if isinstance(data, list):
                text = ""
                for i in data:
                    line = i if type(i) is str else json.dumps(i)
                    text += line + "\n"
            elif isinstance(data, dict):
                text = json.dumps(data, indent=4)
            else:
                text = json.dumps(data, indent=4)
        else:
            raise Exception(f"Unexpected output format: {output}")

    print(text, end="")


def _filter_fields(obj: Any, fields: str):
    if not fields:
        return obj
    parts = fields.split(",")

    def _filter_obj(o):
        if not isinstance(o, dict):
            return o
        for k in list(o.keys()):
            if k not in parts:
                del o[k]
        return o

    if isinstance(obj, list):
        return list(map(_filter_obj, obj))
    return _filter_obj(obj)


def panic(reason: Any = None, code: int = 1):
    print(reason, file=sys.stderr)
    sys.exit(code)


option_verbose = click.option(
    "-v",
    "--verbose",
    count=True,
    default=0,
    help="Print debug logs",
)

option_output = click.option(
    "-o",
    "--output",
    type=click.Choice(["json", "json-compact", "yaml", "text"]),
    default="json",
    help="Specify output format",
)

option_field = click.option(
    "-f",
    "--field",
    type=str,
    required=False,
    help="Specify fields to output",
)

option_id_only = click.option(
    "--id-only/--full-object",
    type=bool,
    default=False,
    required=False,
    help="Output only the object, instead of the full data object",
)
