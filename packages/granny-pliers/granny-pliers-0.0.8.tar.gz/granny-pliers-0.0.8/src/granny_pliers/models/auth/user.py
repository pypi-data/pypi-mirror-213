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

"""User"""

import hashlib
from dataclasses import dataclass
from typing import Type, TypeVar

from granny_pliers.orm import AbstractModel, AbstractMongoRepository, MongoConfig, BaseModel

__all__ = ["User", "Users", "UserActivationRequest", "UserResetPasswordRequest", "UserSetPasswordRequest"]
TModel = TypeVar("TModel")


@dataclass(repr=False, eq=False)
class User(AbstractModel):
    """User"""

    login: str = None
    secret: str = None
    role: str = None

    @staticmethod
    def generate_secret_hash(secret: str) -> str:
        """generate_secret_hash"""
        return hashlib.sha256(secret.encode("utf-8")).hexdigest()


@dataclass(repr=False, eq=False)
class UserActivationRequest(BaseModel):
    """UserActivationRequest"""

    token: str = None


@dataclass(repr=False, eq=False)
class UserResetPasswordRequest(BaseModel):
    """UserResetPasswordRequest"""

    login: str = None


@dataclass(repr=False, eq=False)
class UserSetPasswordRequest(BaseModel):
    """UserSetPasswordRequest"""

    secret: str = None
    token: str = None


class Users(AbstractMongoRepository[User]):
    """Users"""

    def __init__(self, config: MongoConfig, model_class: Type[TModel] = None):
        super().__init__(config, User if model_class is None else model_class)

    @property
    def collection_name(self) -> str:
        return "_users"

    @property
    def indexes(self) -> dict:
        return {"login": 1, "secret": 1, "role": 1}
