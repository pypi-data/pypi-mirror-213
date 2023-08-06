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

"""Abstract Repository"""

import abc
from types import TracebackType
from typing import TypeVar, Generic, Optional, Any, Type

from granny_pliers.logger import AbstractLogger

__all__ = ["AbstractRepository"]
ModelT = TypeVar("ModelT")


class AbstractRepository(Generic[ModelT], AbstractLogger):
    """AbstractRepository"""

    def __init__(self, model_class: Type[ModelT]):
        super().__init__()
        self._model_class = model_class

    async def __aenter__(self):
        """__aenter__"""
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        """__aexit__"""

    @property
    def model_class_name(self) -> str:
        """Repository model class name"""
        return self._model_class.__name__

    @property
    def model_class(self) -> ModelT:
        """Repository model class name"""
        return self._model_class

    @abc.abstractmethod
    async def save(self, obj: ModelT) -> Optional[ModelT]:
        """
        Save single object

        :param obj: object to be saved
        :return: saved object or None if error
        """

    @abc.abstractmethod
    async def save_many(self, objects: list[ModelT]) -> int:
        """
        Save multiple objects

        :param objects: list of objects to be saved
        :return: number saved objects or 0 if error
        """

    @abc.abstractmethod
    async def update(self, obj: ModelT) -> Optional[ModelT]:
        """
        Update single object. The object will be replaced.

        :param obj: object to be updated
        :return: updated object or None if error
        """

    @abc.abstractmethod
    async def update_many(self, objects: list[ModelT]) -> int:
        """
        Update multiple objects. Objects will be replaced.

        :param objects: list of objects to be updated
        :return: number of updated objects or 0 if error
        """

    @abc.abstractmethod
    async def patch(self, obj: ModelT, resources: dict) -> Optional[ModelT]:
        """
        Patch single object. Partial update single object.

        :param obj: object to be updated
        :param resources: dict of new key/values to be updated
        :return: updated object or None if error
        """

    @abc.abstractmethod
    async def patch_many(self, objects: list[ModelT], resources: dict) -> int:
        """
        Patch multiple objects. Partial update multiple objects.

        :param objects: list of the objects to be updated
        :param resources: dict of new key/values to be updated
        :return: number of updated objects or 0 if error
        """

    @abc.abstractmethod
    async def patch_many_by_id(self, obj_ids: list[Any], resources: dict) -> int:
        """
        Patch multiple objects. Partial update multiple objects.

        :param obj_ids: list of unique id's of the objects to be updated
        :param resources: dict of new key/values to be updated
        :return: number of updated objects or 0 if error
        """

    @abc.abstractmethod
    async def patch_by_id(self, obj_id: Any, resources: dict) -> Optional[ModelT]:
        """
        Patch single object. Partial update single object.

        :param obj_id: unique object id object to be updated
        :param resources: dict of new key/values to be updated
        :return: updated object or None if error
        """

    @abc.abstractmethod
    async def delete(self, obj: ModelT, soft: bool = True) -> Optional[ModelT]:
        """
        Delete single object

        :param obj: object to be deleted
        :param soft: indicates that will be applied soft delete, record will be marked as deleted,
        but actually not
        :return: True if object has been successful deleted or False if error
        """

    @abc.abstractmethod
    async def delete_many(self, objects: list[ModelT], soft: bool = True) -> int:
        """
        Delete multiple objects

        :param objects: list of object to be deleted
        :param soft: indicates that will be applied soft delete, record will be marked as deleted,
        but actually not
        :return: number of deleted objects or 0 if error
        """

    @abc.abstractmethod
    async def delete_by_id(self, obj_id: Any, soft: bool = True) -> Optional[ModelT]:
        """
        Delete single object by id

        :param obj_id: unique object id
        :param soft: indicates that will be applied soft delete, record will be marked as deleted,
        but actually not
        :return: deleted object or None if error
        """

    @abc.abstractmethod
    async def delete_all(self, soft: bool = True) -> int:
        """
        Delete all objects

        :param soft: indicates that will be applied soft delete, record will be marked as deleted,
        but actually not
        :return: Number deleted objects
        """

    @abc.abstractmethod
    async def find(self, conditions: dict, verbose: bool = True) -> Optional[ModelT]:
        """
        Find single object
        :param conditions: dict of conditions
        :param verbose print log
        :return: Found object or None if it does not exist or error
        """

    @abc.abstractmethod
    async def find_by_id(self, obj_id: Any) -> Optional[ModelT]:
        """
        Find single object by unique id
        :param obj_id: object unique id
        :return: Found object or None if it does not exist or error
        """

    @abc.abstractmethod
    async def find_many(
        self,
        conditions: dict = None,
        page_number: int = 0,
        page_size: int = 0,
        sort: list[tuple] = None,
        verbose: bool = True,
    ) -> Optional[list[ModelT]]:
        """
        Find multiple documents

        :param conditions: dict of conditions
        :param page_number: uses for pagination, default value 0 means all pages
        :param page_size: uses for pagination, default value 0 means all objects,
                    unlimited page size
        :param sort: tuple of sort parameters.
                    [(sort_by_field_name, sort_direction)]. sort_direction:
                    ASCENDING = 1, DESCENDING = -1
        :param verbose:
        :return: list of found objects or None if error
        """

    @abc.abstractmethod
    async def find_last(self, conditions: dict) -> Optional[ModelT]:
        """
        Find last documents
        :return: found object or None if error
        """

    @abc.abstractmethod
    async def count(self, conditions: dict = None) -> int:
        """
        Calculate number of objects

        :param conditions: dict of conditions
        :return: number of documents
        """

    async def create_indexes(self) -> list[Any]:
        """
        Check and if necessary create/update indexes
        :return: list of indexes
        """
