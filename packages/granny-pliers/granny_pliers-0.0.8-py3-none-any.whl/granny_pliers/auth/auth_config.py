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

"""AuthConfig"""

from dataclasses import dataclass, field

from granny_pliers.config import AbstractConfig

__all__ = ["AuthConfig"]


@dataclass()
class AuthConfig(AbstractConfig):
    """Auth configs"""

    jwt_public_key: str = field(
        default=None,
        metadata={"env_var_name": "AUTH_JWT_PUBLIC_KEY", "type": str},
    )

    jwt_public_key_file: str = field(
        default=None,
        metadata={"env_var_name": "AUTH_JWT_PUBLIC_KEY_FILE", "type": str},
    )

    jwt_private_key: str = field(
        default=None,
        metadata={"env_var_name": "AUTH_JWT_PRIVATE_KEY", "type": str},
    )

    jwt_private_key_file: str = field(
        default=None,
        metadata={"env_var_name": "AUTH_JWT_PRIVATE_KEY_FILE", "type": str},
    )

    jwt_private_key_secret: str = field(
        default=None,
        metadata={"env_var_name": "AUTH_JWT_SECRET", "type": str},
    )

    jwt_token_life_time_ms: int = field(
        default=1000 * 60 * 60 * 24 * 1,  # 1 day
        metadata={"env_var_name": "AUTH_JWT_TOKEN_LIFE_TIME_MS", "type": int},
    )
