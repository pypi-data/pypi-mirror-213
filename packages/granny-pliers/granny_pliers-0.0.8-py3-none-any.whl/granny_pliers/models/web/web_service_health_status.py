#  Copyright 2022 Dmytro Stepanenko, Granny Pliers
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""WebServiceHealthStatus"""

import os
from dataclasses import dataclass, field
from datetime import datetime

from granny_pliers.orm import BaseModel
from granny_pliers.tools import setup_datetime

__all__ = ["WebServiceHealthStatus"]


@dataclass(repr=False, eq=False)
class WebServiceHealthStatus(BaseModel):
    """WebServiceHealthStatus"""

    created_at: datetime = None

    environment: str = None

    ci_commit_short_sha: str = None

    ci_commit_branch: str = None

    status: str = "Unknown"

    data: dict = field(default_factory=dict)

    system_name: str = None

    node_name: str = None

    os_release: str = None

    os_version: str = None

    hardware: str = None

    def __post_init__(self):
        super().__post_init__()
        uname = os.uname()
        self.system_name = uname.sysname
        self.node_name = uname.nodename
        self.os_release = uname.release
        self.os_version = uname.version
        self.hardware = uname.machine
        self.created_at = setup_datetime(self.created_at)
