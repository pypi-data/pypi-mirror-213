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

"""Abstract HTTP repository"""

import abc
import asyncio
from types import TracebackType
from typing import TypeVar, Optional, Any, Type

from .abstract_repository import AbstractRepository
from .restful_http_client import RestfulHttpClient, RestfulHttpClientConfig

__all__ = ["AbstractHttpRepository"]

ModelT = TypeVar("ModelT")


class AbstractHttpRepository(AbstractRepository[ModelT], abc.ABC):
    """AbstractHttpRepository class"""

    def __init__(self, config: RestfulHttpClientConfig, model_class: Type[ModelT]):
        super().__init__(model_class)
        self._config = config
        self._client = None

    async def __aenter__(self) -> "AbstractHttpRepository":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        if self._client is not None:
            await self.client.session.close()

    async def close(self):
        """close"""
        if self._client is not None:
            await self.client.session.close()

    @property
    @abc.abstractmethod
    def collection_name(self) -> str:
        """Repository collection name"""

    @property
    def client(self) -> RestfulHttpClient[ModelT]:
        """client"""
        if self._client is None:
            self._client = RestfulHttpClient[self._model_class](self._config, self._model_class, self.collection_name)
        return self._client

    async def save(self, obj: ModelT) -> Optional[ModelT]:
        return await self.client.post(obj)

    async def save_many(self, objects: list[ModelT]) -> int:
        save_plan = list(map(self.client.post, objects))
        saves = await asyncio.gather(*save_plan)
        return sum(o is not None for o in saves)

    async def update(self, obj: ModelT) -> Optional[ModelT]:
        return await self.client.put(obj)

    async def update_many(self, objects: list[ModelT]) -> int:
        update_plan = list(map(self.client.put, objects))
        updates = await asyncio.gather(*update_plan)
        return sum(o is not None for o in updates)

    async def patch(self, obj: ModelT, resources: dict) -> Optional[ModelT]:
        """patch"""
        return await self.patch_by_id(obj.id, resources)

    async def patch_by_id(self, obj_id: Any, resources: dict) -> Optional[ModelT]:
        """patch_by_id"""
        return await self.client.patch(obj_id, resources)

    async def patch_self(self, resources: dict) -> Optional[ModelT]:
        """patch_self"""
        return await self.client.patch_self(resources)

    async def patch_many_by_id(self, obj_ids: list[Any], resources: dict) -> int:
        """patch_many_by_id"""
        patch_plan = list(map(lambda o: self.client.patch(o, resources), obj_ids))
        patches = await asyncio.gather(*patch_plan)
        return sum(o is not None for o in patches)

    async def patch_many(self, objects: list[ModelT], resources: dict) -> int:
        patch_plan = list(map(lambda o: self.client.patch(o.id, resources), objects))
        patches = await asyncio.gather(*patch_plan)
        return sum(o is not None for o in patches)

    async def delete(self, obj: ModelT, soft: bool = True) -> Optional[ModelT]:
        return await self.client.delete(obj.id)

    async def delete_many(self, objects: list[ModelT], soft: bool = True) -> int:
        delete_plan = list(map(lambda o: self.client.delete(o.id), objects))
        deletions = await asyncio.gather(*delete_plan)
        return sum(o is not None for o in deletions)

    async def delete_by_id(self, obj_id: Any, soft: bool = True) -> Optional[ModelT]:
        """delete_by_id"""
        return await self.client.delete(obj_id)

    async def delete_all(self, soft: bool = True) -> int:
        """delete_all"""
        self.log.error("Not implemented")
        return 0

    async def find(self, conditions: dict, verbose: bool = True) -> Optional[ModelT]:
        """find"""
        found_items = await self.find_many(conditions, 0, 1)
        if len(found_items) > 0:
            return found_items[0]
        return None

    async def find_by_id(self, obj_id: Any) -> Optional[ModelT]:
        """find_by_id"""
        return await self.client.get_one(obj_id)

    async def find_one_self(self) -> Optional[ModelT]:
        """find_one_self"""
        return await self.client.get_one_self()

    async def find_last(self, conditions: dict) -> Optional[ModelT]:
        """find_last"""
        self.log.error("Not implemented")
        return None

    async def count(self, conditions: dict = None) -> int:
        return await self.client.count(conditions)

    async def find_many(
        self,
        conditions: dict = None,
        page_number: int = 0,
        page_size: int = 0,
        sort: list[tuple] = None,
        verbose: bool = True,
    ) -> Optional[list[ModelT]]:
        if conditions is None:
            conditions = {}

        conditions["page_number"] = page_number
        conditions["page_size"] = page_size

        if sort is not None:
            for sort_item in sort:
                conditions["sort_by_field"] = sort_item[0]
                conditions["sort_direction"] = "asc" if sort_item[1] == 1 else "desc"

        page = await self.client.get(params=conditions)
        return page.items
