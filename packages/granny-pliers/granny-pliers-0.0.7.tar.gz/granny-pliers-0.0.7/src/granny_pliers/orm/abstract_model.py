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

from dataclasses import dataclass, fields

import jsonplus

__all__ = ["BaseModel", "base_model_encoder"]


@dataclass()
class BaseModel:
    """BaseModel"""

    def __post_init__(self):
        pass


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
        if cls_field.type is tuple:
            obj_dict[cls_field.name] = str(getattr(obj, cls_field.name))
        else:
            obj_dict[cls_field.name] = getattr(obj, cls_field.name)
    return obj_dict
