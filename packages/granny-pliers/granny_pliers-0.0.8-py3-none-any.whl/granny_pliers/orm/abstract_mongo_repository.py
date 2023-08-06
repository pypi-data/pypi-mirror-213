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

"""Abstract MongoDB repository"""

import abc
import asyncio
from dataclasses import asdict, fields, field, dataclass
from datetime import datetime
from enum import Enum
from types import TracebackType
from typing import TypeVar, Optional, Any, Type

from bson import CodecOptions, ObjectId
from bson.codec_options import TypeRegistry
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from pymongo import DeleteOne, ReturnDocument, ReplaceOne, UpdateOne
from pymongo.errors import OperationFailure, DuplicateKeyError
from pymongo.results import (
    InsertOneResult,
    InsertManyResult,
    DeleteResult,
    BulkWriteResult,
    UpdateResult,
)

from granny_pliers.config import AbstractConfig
from granny_pliers.tools import setup_datetime
from .abstract_repository import AbstractRepository

__all__ = ["MongoConfig", "AbstractMongoRepository"]

ModelT = TypeVar("ModelT")


@dataclass()
class MongoConfig(AbstractConfig):
    """MongoConfig"""

    connection_uri: str = field(
        default=None,
        metadata={"env_var_name": "MONGODB_URI", "type": str},
    )
    connect: bool = field(
        default=False,
        metadata={"type": bool},
    )
    server_selection_timeout_ms: int = field(
        default=10000,
        metadata={"type": int},
    )


class AbstractMongoRepository(AbstractRepository[ModelT]):
    """AMongoRepository class"""

    def __init__(self, config: MongoConfig, model_class: Type[ModelT], client: AsyncIOMotorClient = None):
        super().__init__(model_class)
        self.config = config
        self.__client = client
        self.__collection = None
        self._defaults: list[ModelT] = []
        self.__codec_options = CodecOptions(type_registry=TypeRegistry(fallback_encoder=self._fallback_encoder))

    @property
    @abc.abstractmethod
    def collection_name(self) -> str:
        """Repository collection name"""

    @property
    @abc.abstractmethod
    def indexes(self) -> dict:
        """Collection indexes"""

    async def __aenter__(self) -> "AbstractMongoRepository":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.close()

    @property
    def defaults(self) -> list[ModelT]:
        """defaults"""
        return self._defaults

    async def seed_defaults(self):
        """Seeding defaults/patches etc..."""
        for obj in self.defaults:
            if await self.find_by_id(obj.id) is None:
                await self.save(obj)
            else:
                await self.update(obj)

    @property
    def client(self) -> AsyncIOMotorClient:
        """MongoDB client"""
        if self.__client is None:
            self.__client = AsyncIOMotorClient(
                host=self.config.connection_uri,
                connect=self.config.connect,
                serverSelectionTimeoutMS=self.config.server_selection_timeout_ms,
            )
        return self.__client

    @property
    def collection(self) -> AsyncIOMotorCollection:
        """Current active collection instance"""
        if self.__collection is None:
            database = self.client.get_database(codec_options=self.__codec_options)
            self.__collection = database.get_collection(self.collection_name)
        return self.__collection

    def __enter__(self):
        """Uses for WITH statement"""
        return self

    def __exit__(self, obj_type, value, traceback):
        self.close()

    def close(self):
        """close"""
        if self.__client is not None:
            self.__client.close()
            self.__client = None

    def _fallback_encoder(self, value):
        try:
            if isinstance(value, Enum):
                return asdict(value.value)
            else:
                # Python datetime to BSON DateTime encoder
                return setup_datetime(value)
        except TypeError as error:
            self.log.error("_fallback_encoder", error=error)

    @staticmethod
    def parse_object_id(obj_id: Any):
        """parse ObjectId from any type"""
        if obj_id is None:
            return ObjectId()

        if isinstance(obj_id, str):
            return ObjectId(obj_id)

        return obj_id

    async def create_indexes(self) -> list[str]:
        cursor = self.collection.list_indexes()
        existing = list(map(lambda i: i.to_dict()["name"], await cursor.to_list(None)))
        create = [
            self.collection.create_index([(k, v)], background=True, name=k, unique=(k == "uuid"))
            for k, v in self.indexes.items()
            if k not in existing
        ]
        if len(create) > 0:
            created = await asyncio.gather(*create)
            self.log.info("Created indexes %s", created)
        else:
            created = []
        return created

    async def save(self, obj: ModelT, verbose: bool = True) -> Optional[ModelT]:
        try:
            insert_result: InsertOneResult = await self.collection.insert_one(document=asdict(obj))

            if insert_result.acknowledged is None:
                self.log.error("Can not save %s", self.model_class_name)
                return None

            resource = await self.collection.find_one(filter=insert_result.inserted_id)

            if resource is None:
                self.log.error("Saved %s not found", self.model_class_name)
                return None
            if verbose:
                self.log.info("Saved %s: %s", self.model_class_name, resource.get("_id"))
            return self.model_class(**resource)

        except (DuplicateKeyError, OperationFailure, TypeError) as error:
            self.log.error("Can not save %s", self.model_class_name, error=error)
            return None

    async def save_if_not_exists(self, obj: ModelT, conditions: dict = None) -> Optional[ModelT]:
        """save_if_not_exists"""
        try:
            if conditions is None:
                conditions = dict(_id=obj.id)

            result = await self.collection.find_one(filter=conditions)

            if result is None:
                return await self.save(obj)

            return None
        except (DuplicateKeyError, OperationFailure, TypeError) as error:
            self.log.error("Can not save_if_not_exists %s", self.model_class_name, error=error)
            return None

    async def save_many(self, objects: list[ModelT]) -> int:
        if len(objects) == 0:
            self.log.info("Saved 0 %ss", self.model_class_name)
            return 0
        try:
            insert_result: InsertManyResult = await self.collection.insert_many(map(asdict, objects))

            if not insert_result.acknowledged:
                self.log.error("Can not save many %s", self.model_class_name)
                return 0
            self.log.info("Saved %d %ss", len(insert_result.inserted_ids), self.model_class_name)
            return len(insert_result.inserted_ids)

        except (DuplicateKeyError, OperationFailure, TypeError) as error:
            self.log.error("Can not save %s", self.model_class_name, error=error)
            return 0

    async def update(self, obj: ModelT) -> Optional[ModelT]:
        try:
            result = await self.collection.find_one_and_replace(
                filter=dict(_id=obj.id),
                replacement=asdict(obj),
                upsert=False,
                return_document=ReturnDocument.AFTER,
            )

            if result is None:
                self.log.error("Can not update %s: %s", self.model_class_name, obj.id)
                return None
            self.log.info("Updated %s: %s", self.model_class_name, obj.id)
            return self.model_class(**result)
        except (OperationFailure, TypeError) as error:
            self.log.error("Can not update %s: %s", self.model_class_name, obj.id, error=error)
            return None

    async def update_many(self, objects: list[ModelT]) -> int:
        if len(objects) == 0:
            self.log.info("Updated 0 %ss", self.model_class_name)
            return 0
        try:
            result: BulkWriteResult = await self.collection.bulk_write(
                list(map(lambda o: ReplaceOne(dict(_id=o.id), asdict(o)), objects))
            )
            if result.modified_count != len(objects):
                self.log.error(
                    "Update_many error, expected updated %d %ss actual updated %d %ss",
                    len(objects),
                    self.model_class_name,
                    result.modified_count,
                    self.model_class_name,
                )
            self.log.info("Updated %d %ss", result.modified_count, self.model_class_name)
            return result.modified_count
        except (OperationFailure, TypeError) as error:
            self.log.error("Can not update objects", self.model_class_name, error=error)
            return 0

    async def patch(self, obj: ModelT, resources: dict) -> Optional[ModelT]:
        return await self.patch_by_id(obj.id, resources)

    async def patch_by_id(self, obj_id: Any, resources: dict) -> Optional[ModelT]:
        mongo_obj_id = self.parse_object_id(obj_id)

        allowed_fields = list(map(lambda f: f.name, fields(self.model_class)))
        for key in resources.keys():
            if key not in allowed_fields:
                self.log.error(
                    "Can not patch %s, bad field",
                    self.model_class_name,
                    obj_id=str(mongo_obj_id),
                    field=key,
                )
                return None
        try:
            result = await self.collection.find_one_and_update(
                filter=dict(_id=mongo_obj_id),
                update={"$set": resources},
                upsert=False,
                return_document=ReturnDocument.AFTER,
            )

            if result is None:
                self.log.error("Can not patch %s: %s", self.model_class_name, obj_id)
                return None
            self.log.info("Patched %s: %s", self.model_class_name, obj_id)
            return self.model_class(**result)
        except (OperationFailure, TypeError) as error:
            self.log.error("Can not patch %s", self.model_class_name, obj_id=obj_id, error=error)
            return None

    async def patch_many_by_id(self, obj_ids: list[Any], resources: dict) -> int:
        if len(obj_ids) == 0:
            self.log.info("Patched 0 %ss", self.model_class_name)
            return 0
        try:
            mongo_obj_ids = list(map(self.parse_object_id, obj_ids))
            result: BulkWriteResult = await self.collection.bulk_write(
                list(
                    map(
                        lambda o_id: UpdateOne(dict(_id=o_id), {"$set": resources}),
                        mongo_obj_ids,
                    )
                )
            )
            if result.matched_count != len(mongo_obj_ids):
                self.log.error(
                    "patch_many_by_id error, expected updated %d %ss actual updated %d %ss",
                    len(mongo_obj_ids),
                    self.model_class_name,
                    result.matched_count,
                    self.model_class_name,
                )
            self.log.info("Patched %d %ss", result.matched_count, self.model_class_name)
            return result.matched_count
        except (OperationFailure, TypeError) as error:
            self.log.error("Can not patch objects", self.model_class_name, error=error)
            return 0

    async def patch_many(self, objects: list[ModelT], resources: dict) -> int:
        obj_ids = [o.id for o in objects]
        return await self.patch_many_by_id(obj_ids, resources)

    async def delete(self, obj: ModelT, soft: bool = True) -> Optional[ModelT]:
        return await self.delete_by_id(obj.id, soft)

    async def delete_many(self, objects: list[ModelT], soft: bool = True) -> int:
        if len(objects) == 0:
            self.log.info("Deleted 0 %ss", self.model_class_name)
            return 0

        try:
            if soft:
                result = await self.patch_many(objects, dict(is_deleted=True))
                self.log.info("Soft Deleted %d %ss", result, self.model_class_name)
                return result
            else:
                result = await self.collection.bulk_write(list(map(lambda o: DeleteOne(dict(_id=o.id)), objects)))
                self.log.info("Hard Deleted %d %ss", result.deleted_count, self.model_class_name)
                return result.deleted_count
        except (OperationFailure, TypeError) as error:
            self.log.error("Can not delete objects", self.model_class_name, error=error)
            return 0

    async def delete_by_id(self, obj_id: Any, soft: bool = True) -> Optional[ModelT]:
        try:
            mongo_obj_id = self.parse_object_id(obj_id)
            if soft:
                result = await self.patch_by_id(obj_id, dict(is_deleted=True))
                self.log.info("Soft deleted %s: %s", self.model_class_name, mongo_obj_id)
            else:
                result = await self.collection.find_one_and_delete(dict(_id=mongo_obj_id))
                self.log.info("Hard deleted %s: %s", self.model_class_name, mongo_obj_id)

            if result is None:
                self.log.error("Can not delete %s", self.model_class_name, obj_id=mongo_obj_id)
                return None

            return result if isinstance(result, self._model_class) else self.model_class(**result)
        except (OperationFailure, TypeError) as error:
            self.log.error("Can not delete %s", self.model_class_name, obj_id=obj_id, error=error)
            return None

    async def delete_all(self, soft: bool = True) -> int:
        try:
            if soft:
                result: UpdateResult = await self.collection.update_many(
                    {},
                    {"$set": {"is_deleted": True}},
                    upsert=False,
                )

                if not result.acknowledged:
                    self.log.error("Cant soft delete %s", self.model_class_name)
                    return 0

                self.log.info("Soft Deleted %d %ss", result.modified_count, self.model_class_name)
                return result.modified_count
            else:
                result: DeleteResult = await self.collection.delete_many({})

                if not result.acknowledged:
                    self.log.error("Cant delete %s", self.model_class_name)
                    return 0
                self.log.info("Hard Deleted %d %ss", result.deleted_count, self.model_class_name)

                return result.deleted_count
        except (OperationFailure, TypeError) as error:
            self.log.error("Can not delete many %s", self.model_class_name, error=error)
            return 0

    async def find(self, conditions: dict, verbose: bool = True) -> Optional[ModelT]:
        try:
            result = await self.collection.find_one(filter=conditions)

            if result is None:
                return None

            if verbose:
                self.log.info("Found %s: %s", self.model_class_name, result.get("_id"))

            return self.model_class(**result)
        except (OperationFailure, TypeError) as error:
            self.log.error(
                "Can not execute find for %s",
                self.model_class_name,
                conditions=conditions,
                error=error,
            )
            return None

    async def find_by_id(self, obj_id: Any) -> Optional[ModelT]:
        try:
            mongo_obj_id = self.parse_object_id(obj_id)

            result = await self.collection.find_one(filter=mongo_obj_id)
            if result is None:
                self.log.info("Not found %s: %s", self.model_class_name, mongo_obj_id)
                return None

            self.log.info("Found %s: %s", self.model_class_name, result.get("_id"))
            return self.model_class(**result)
        except (OperationFailure, TypeError) as error:
            self.log.error(
                "Can not execute find_by_id %s",
                self.model_class_name,
                obj_id=obj_id,
                error=error,
            )
            return None

    async def find_last(self, conditions: dict) -> Optional[ModelT]:
        try:
            result = await self.collection.find_one(filter=conditions, limit=1, sort=[("_id", -1)])

            if result is None:
                self.log.info("Last not found %s, collection is empty", self.model_class_name)
                return None

            self.log.info("Found %s: %s", self.model_class_name, result.get("_id"))
            return self.model_class(**result)
        except (OperationFailure, TypeError) as error:
            self.log.error("Can not find %s", self.model_class_name, error=error)
            return None

    async def count(self, conditions: dict = None) -> int:
        """
        Calculate number of objects

        :param conditions: dict
        :return: number of documents
        """
        if conditions is None:
            conditions = {}
        return await self.collection.count_documents(conditions)

    async def find_many(
        self,
        conditions: dict = None,
        page_number: int = 0,
        page_size: int = 0,
        sort: list[tuple] = None,
        verbose: bool = True,
        projection: dict = None,
    ) -> Optional[list[ModelT]]:
        if conditions is None:
            conditions = {}

        if page_number is None:
            page_number = 0

        if page_size is None:
            page_size = 0

        skip = page_number * page_size
        limit = page_size
        try:
            cursor = self.collection.find(filter=conditions, skip=skip, limit=limit, sort=sort, projection=projection)

            result = await cursor.to_list(None)
            if verbose:
                self.log.info("Found %d %ss", len(result), self.model_class_name)
            return list(map(lambda t: self.model_class(**t), result))
        except (OperationFailure, TypeError, Exception) as error:
            self.log.error("Can not find %s", self.model_class_name, error=error)
            return []

    @staticmethod
    def helper_symbol_date_condition(symbol: str, date: datetime) -> dict:
        """helper_symbol_date_condition"""
        return {
            "symbol": symbol,
            "$expr": {
                "$and": [
                    {"$eq": [{"$year": "$created_at"}, date.year]},
                    {"$eq": [{"$month": "$created_at"}, date.month]},
                    {"$eq": [{"$dayOfMonth": "$created_at"}, date.day]},
                ]
            },
        }

    @staticmethod
    def helper_date_condition(date: datetime) -> dict:
        """helper_date_condition"""
        return {
            "$expr": {
                "$and": [
                    {"$eq": [{"$year": "$created_at"}, date.year]},
                    {"$eq": [{"$month": "$created_at"}, date.month]},
                    {"$eq": [{"$dayOfMonth": "$created_at"}, date.day]},
                ]
            },
        }
