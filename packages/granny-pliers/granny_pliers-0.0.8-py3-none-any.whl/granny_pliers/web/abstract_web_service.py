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

"""AbstractWebService"""

import abc
import asyncio
import datetime
import enum
from abc import ABC
from dataclasses import fields
from typing import Generic, TypeVar, Type, Optional

import dateparser
import jsonplus
import multidict
import pytz
import structlog
from aiohttp import web
from bson import ObjectId

from granny_pliers.auth import JwtToken
from granny_pliers.logger import AbstractLogger
from granny_pliers.orm import AbstractRepository

__all__ = ["AbstractWebService", "check_auth_permissions"]

ModelT = TypeVar("ModelT")


def check_auth_permissions(required_permissions: list[enum.IntEnum], roles: enum):
    """
    Decorator Validate allowed permissions

    :param required_permissions:
    :param roles
    :return:
    """

    def _decorator(function):
        """
        Decorator

        :param function:
        :return:
        """

        async def wrapper(*args, **kwargs):
            """
            Wrapper

            :param args:
            :param kwargs:
            :return:
            """
            try:
                request = args[1]
                auth_token: JwtToken = request.get("jwt_token_name", None)

                if auth_token is None:
                    return web.HTTPForbidden(text="Access forbidden")

                required = set(p.value for p in required_permissions)
                existing = set(roles[auth_token.payload.role].value)
                if not required.issubset(existing):
                    structlog.getLogger(args[0].__class__.__name__, api=args[0].path).warning(
                        "Unauthorized access, not enough permissions",
                        auth_token_payload=auth_token.payload,
                        remote=request.remote,
                    )
                    return web.HTTPForbidden(text="Access forbidden")
            except Exception as error:
                structlog.getLogger(args[0].__class__.__name__, api=args[0].path).error(
                    "Unauthorized access, auth bad format", error=error
                )
                return web.HTTPForbidden(text="Access forbidden")
            return await function(*args, **kwargs)

        return wrapper

    return _decorator


class AbstractWebService(Generic[ModelT], AbstractLogger, ABC):
    """Abstract WebService"""

    def __init__(self, cls: Type[ModelT], repository: AbstractRepository[ModelT], base_path: str = "/"):
        super().__init__()
        self.cls = cls
        self.base_path = base_path
        self.repository: Type[repository] = repository
        self.log.info("Initialized %s", self.path)

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Service name"""

    @property
    def path(self) -> str:
        """path"""
        return f"{self.base_path}/{self.name}"

    @property
    def routes(self):
        """Defines default API endpoints"""
        return [
            web.get(self.path, self.get),
            web.post(self.path, self.post),
            web.get(self.path + "/count", self.count),
            web.put(self.path + r"/{id:[0-9a-f]{24}+}", self.put),
            web.get(self.path + r"/{id:[0-9a-f]{24}+}", self.get_one),
            web.patch(self.path + r"/{id:[0-9a-f]{24}+}", self.patch),
            web.delete(self.path + r"/{id:[0-9a-f]{24}+}", self.delete),
        ]

    @staticmethod
    def get_authenticated_user_id(request: web.Request) -> Optional[ObjectId]:
        """get_authenticated_user_id"""
        jwt_token: JwtToken = request.get("jwt_token_name", None)
        if jwt_token is None:
            return None
        return ObjectId(jwt_token.payload.user_id)

    @staticmethod
    def get_authenticated_user_id_filter(request: web.Request) -> dict:
        """get_authenticated_user_id_filter"""
        return dict(user_id=AbstractWebService.get_authenticated_user_id(request))

    @staticmethod
    def _get_page_number(query: multidict.MultiDict[str]) -> int:
        """Parse page_number parameter"""
        page_number = query.get("page_number")
        return int(page_number) if page_number else 0

    @staticmethod
    def _get_page_size(query: multidict.MultiDict[str]) -> int:
        """Parse page_size parameter"""
        page_size = query.get("page_size")
        return int(page_size) if page_size else 0

    @staticmethod
    def _get_sort_by_field(query: multidict.MultiDict[str]) -> Optional[str]:
        """Parse sort_by_field parameter"""
        return query.get("sort_by_field")

    @staticmethod
    def _get_sort_direction(query: multidict.MultiDict[str]) -> Optional[int]:
        """Parse sort_direction parameter"""
        return 1 if query.get("sort_direction") == "asc" else -1

    def _get_condition(self, query: multidict.MultiDict[str], _: web.Request) -> dict:
        """Parse data filter parameters"""
        condition = {}
        for cls_field in fields(self.cls):
            if cls_field.name not in query.keys():
                continue

            if cls_field.type is bool:
                condition[cls_field.name] = query.get(cls_field.name).lower() == "true"
                continue

            if cls_field.type is int:
                condition[cls_field.name] = int(query.get(cls_field.name))
                continue

            if cls_field.type is float:
                condition[cls_field.name] = float(query.get(cls_field.name))
                continue

            if cls_field.type is ObjectId:
                condition[cls_field.name] = ObjectId(query.get(cls_field.name))
                continue

            if cls_field.type is datetime.date or cls_field.type is datetime.datetime:
                condition[cls_field.name] = dateparser.parse(query.get(cls_field.name)).replace(
                    microsecond=0, tzinfo=pytz.utc
                )
                continue

            if issubclass(cls_field.type, enum.IntEnum):
                condition[cls_field.name] = int(query.get(cls_field.name))
                continue

            if cls_field.type is str:
                # rgx = re.compile(query.get(cls_field.name), re.IGNORECASE)
                condition[cls_field.name] = query.get(cls_field.name)
                # {"$regex": rgx}
                continue

        return condition

    async def get(self, request: web.Request):
        """Method GET, reads multiple records

        :param request:
        :return: JSON SSPage{items: [], total: int}
        """
        try:
            page_number = self._get_page_number(request.rel_url.query)
            page_size = self._get_page_size(request.rel_url.query)
            sort_by_field = self._get_sort_by_field(request.rel_url.query)
            sort_direction = self._get_sort_direction(request.rel_url.query)
            if sort_by_field is None:
                sort = None
            else:
                sort = [(sort_by_field, sort_direction)]
            condition = self._get_condition(request.rel_url.query, request)

            items, total = await asyncio.gather(
                self.repository.find_many(condition, page_number, page_size, sort),
                self.repository.count(condition),
            )

            result = dict(items=items, total=total)
            return web.json_response(result, dumps=jsonplus.dumps)
        except Exception as error:
            self.log.error(request.url, error=error)
            return web.HTTPBadRequest(text="Bad filter")

    async def get_one(self, request: web.Request):
        """Method GET, reads single record

        :param request:
        :return: single JSON document type T
        """
        try:
            result = await self.repository.find_by_id(request.match_info["id"])

            if result is None:
                return web.HTTPNotFound(text="Not found")

            return web.json_response(result, dumps=jsonplus.dumps)
        except Exception as error:
            self.log.error(request.url, error=error)
            return web.HTTPBadRequest(text="Bad request")

    async def post(self, request: web.Request):
        """Method POST, creates new records

        :param request:
        :return: single JSON - created record
        """
        try:
            body = await request.text()
            resource = self.cls(**jsonplus.loads(body))

            result = await self.repository.save(resource)

            if result is None:
                return web.HTTPInsufficientStorage(text="Can not store resource into database")

            return web.json_response(result, status=201, dumps=jsonplus.dumps)
        except Exception as error:
            self.log.error(request.url, error=error)
            return web.HTTPBadRequest(text="Can not parse resource")

    async def put(self, request: web.Request):
        """METHOD PUT, updates whole record

        :param request:
        :return: single JSON - updated record
        """
        try:
            body = await request.text()

            resource = self.cls(**jsonplus.loads(body))

            result = await self.repository.update(resource)

            if result is None:
                return web.HTTPInsufficientStorage(text="Can not store resource into database")

            return web.json_response(result, dumps=jsonplus.dumps)
        except Exception as error:
            self.log.error(request.url, error=error)
            return web.HTTPBadRequest(text="Can not parse resource")

    async def patch(self, request: web.Request):
        """METHOD PATCH, partial record update

        :param request:
        :return: single JSON - patched record
        """
        try:
            body = await request.text()

            resource = jsonplus.loads(body)

            result = await self.repository.patch_by_id(request.match_info["id"], resource)

            if result is None:
                return web.HTTPNotFound(text="Not found")

            return web.json_response(result, dumps=jsonplus.dumps)
        except Exception as error:
            self.log.error(request.url, error=error)
            return web.HTTPBadRequest(text="Can not parse resource")

    async def delete(self, request: web.Request):
        """Method DELETE, deletes one record

        :param request:
        :return: single JSON - deleted records
        """
        try:
            result = await self.repository.delete_by_id(request.match_info["id"], soft=False)

            if result is None:
                return web.HTTPNotFound(text="Not found")

            return web.json_response(result, status=200, dumps=jsonplus.dumps)

        except Exception as error:
            self.log.error(request.url, error=error)
            return web.HTTPBadRequest(text="Can not parse resource")

    async def count(self, request: web.Request):
        """Method GET, calculates count

        :param request:
        :return: single JSON - deleted records
        """
        try:
            condition = self._get_condition(request.rel_url.query, request)

            count = await self.repository.count(condition)
            return web.json_response(dict(count=count), dumps=jsonplus.dumps)
        except Exception as error:
            self.log.error(request.url, error=error)
            return web.HTTPBadRequest(text="Bad filter")
