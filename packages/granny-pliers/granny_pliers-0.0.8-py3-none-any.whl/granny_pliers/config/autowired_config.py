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

"""AutoWiredConfig"""

from dataclasses import dataclass, field

from .abstract_config import AbstractConfig
from .project_environment import ProjectEnvironment

__all__ = ["AutoWiredConfig"]


@dataclass()
class AutoWiredConfig(AbstractConfig):
    """AutoWiredConfig"""

    environment: str = field(
        default=ProjectEnvironment.LOCAL.value,
        metadata={"env_var_name": "PROJECT_ENV", "type": str},
    )

    commit_short_sha: str = field(
        default=None,
        metadata={"env_var_name": "COMMIT_SHORT_SHA", "type": str},
    )

    commit_branch: str = field(
        default=None,
        metadata={"env_var_name": "COMMIT_BRANCH", "type": str},
    )

    def __post_init__(self):
        super().__post_init__()
        self.environment = self.environment.lower()
        if self.commit_short_sha is not None:
            self.commit_short_sha = self.commit_short_sha.lower()
        if self.commit_branch is not None:
            self.commit_branch = self.commit_branch.lower()
