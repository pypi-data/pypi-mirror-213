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

"""WebApplicationConfig"""

from dataclasses import dataclass, field

from granny_pliers.auth import AuthConfig
from granny_pliers.config import AbstractConfig

__all__ = ["WebApplicationConfig"]


@dataclass()
class WebApplicationConfig(AbstractConfig):
    """WebApplicationConfig"""

    auth: AuthConfig = None

    host: str = field(
        default="localhost",
        metadata={"env_var_name": "WEB_HOST", "type": str},
    )
    port: int = field(
        default=8080,
        metadata={"env_var_name": "WEB_PORT", "type": int},
    )

    client_max_size: int = field(
        default=1024 * 1024,
        metadata={"env_var_name": "WEB_CLIENT_MAX_SIZE", "type": int},
    )
    """Max post body size server can accept, default value 1MB in bytes"""

    base_http_path: str = field(
        default="/",
        metadata={"env_var_name": "WEB_BASE_HTTP_PATH", "type": str},
    )
