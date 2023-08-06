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

"""BaseModel"""

from dataclasses import dataclass, fields, field
from datetime import datetime
from typing import TypeVar, Generic

import jsonplus

__all__ = ["BaseModel", "base_model_encoder", "AbstractModel", "ModelsPage", "ModelsCount"]

from bson import ObjectId

from granny_pliers.tools import setup_datetime


@dataclass()
class BaseModel:
    """BaseModel"""

    def __post_init__(self):
        pass


@dataclass(repr=False, eq=False, order=False)
class AbstractModel(BaseModel):
    """Basic Abstract model"""

    _id: ObjectId = None
    _created_at: datetime = None
    is_deleted: bool = False

    @property
    def id(self) -> ObjectId:  # pylint: disable=C0103
        """ObjectID"""
        return self._id

    @id.setter
    def id(self, value: None | str | ObjectId):  # pylint: disable=C0103
        """id"""
        match value:
            case ObjectId():
                self._id = value
            case None:
                self._id = ObjectId()
            case str():
                self._id = ObjectId() if value == "" else ObjectId(value)

    @property
    def created_at(self) -> datetime:
        """ObjectID"""
        return self._created_at

    @created_at.setter
    def created_at(self, value: None | datetime | str | int):
        self._created_at = setup_datetime(value)

    def __post_init__(self):
        super().__post_init__()
        self.id = self._id  # pylint: disable=C0103
        self.created_at = self._created_at


ModelT = TypeVar("ModelT")


@dataclass(repr=False, eq=False)
class ModelsPage(Generic[ModelT]):
    """ModelsPage"""

    items: list[ModelT] = field(default_factory=list)
    total: int = 0


@dataclass(repr=False, eq=False)
class ModelsCount:
    """ModelsCount"""

    count: int = 0


@jsonplus.encoder(
    "BaseModel",
    predicate=lambda obj: isinstance(obj, BaseModel),
    exact=False,
    priority=100,
)
def base_model_encoder(obj):
    """
    Json Encoder for BaseModel

    :param obj:
    :return: dict
    """
    obj_dict = {}
    for cls_field in fields(obj):
        if cls_field.type is ObjectId:
            obj_dict[cls_field.name] = str(getattr(obj, cls_field.name))
        elif cls_field.type is tuple:
            obj_dict[cls_field.name] = str(getattr(obj, cls_field.name))
        else:
            obj_dict[cls_field.name] = getattr(obj, cls_field.name)
    return obj_dict
