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

"""Configs"""

from .abstract_config import *
from .autowired_config import *
from .logger_config import *
from .project_environment import *

__all__ = (
    abstract_config.__all__  # pylint: disable=E0602
    + autowired_config.__all__  # pylint: disable=E0602
    + logger_config.__all__  # pylint: disable=E0602
    + project_environment.__all__  # pylint: disable=E0602
)
