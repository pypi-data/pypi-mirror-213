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

"""AuthError"""

from dataclasses import dataclass, asdict

import jsonplus

__all__ = ["AuthError"]


@dataclass(repr=False, eq=False)
class AuthError:
    """AuthError"""
    error: str


@jsonplus.encoder("AuthError", predicate=lambda obj: isinstance(obj, AuthError), exact=False, priority=100)
def auth_error_encoder(obj):
    """auth_error_encoder"""
    return asdict(obj)
