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

"""RestfulHttpClient"""

from dataclasses import dataclass, field
from types import TracebackType
from typing import Optional, Any, TypeVar, Generic, Type

import aiohttp
import jsonplus

from granny_pliers.auth import Jwt, AuthConfig
from granny_pliers.config import AbstractConfig
from granny_pliers.logger import AbstractLogger
from .abstract_model import ModelsPage

__all__ = ["RestfulHttpClientConfig", "RestfulHttpClient"]

ModelT = TypeVar("ModelT")


@dataclass()
class RestfulHttpClientConfig(AbstractConfig):
    """RestfulHttpClientConfig"""

    api_url: str = field(
        default=None,
        metadata={"env_var_name": "RESTFUL_HTTP_CLIENT_API_URL", "type": str},
    )
    """Api endpoint includes collection name, for example http://localhost:8080/documents/"""

    use_jwt_auth: bool = field(
        default=True,
        metadata={"env_var_name": "RESTFUL_HTTP_CLIENT_USE_JWT_AUTH", "type": bool},
    )

    login: str = field(
        default=None,
        metadata={"env_var_name": "RESTFUL_HTTP_CLIENT_USER", "type": str},
    )
    """JWT Auth user name"""

    secret: str = field(
        default=None,
        metadata={"env_var_name": "RESTFUL_HTTP_CLIENT_USER_SECRET", "type": str},
    )
    """JWT Auth user password"""

    auth_url: str = field(
        default=None,
        metadata={"env_var_name": "AUTH_URL", "type": str},
    )
    """Authentication service endpoint, for example http://localhost:8080/auth/"""

    auth: AuthConfig = None


class RestfulHttpClient(Generic[ModelT], AbstractLogger):
    """RestfulHttpClient"""

    def __init__(self, config: RestfulHttpClientConfig, model_class: Type[ModelT], collection_name: str):
        super().__init__()
        self._config = config
        self._model_class = model_class
        self._session = None
        self._jwt_token = None
        self.__jwt = None
        self.collection_name = collection_name
        self.headers = {}

    async def __aenter__(self) -> "RestfulHttpClient":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        if self._session is not None:
            await self._session.close()

    @property
    def jwt(self) -> Optional[Jwt]:
        """jwt"""
        if self.__jwt is None:
            self.__jwt = Jwt(self._config.auth)
        return self.__jwt

    async def authenticate(self) -> bool:
        """authenticate"""
        if not self._config.use_jwt_auth:
            return True

        if self._jwt_token is not None and self.jwt.verify_token(self._jwt_token.token) is not None:
            return True

        self.log.info("Authenticating...")

        # reset previous session
        if self._session is not None:
            await self._session.close()
            self._session = None
        # reset previous headers
        self.headers = {"Accept": "application/json", "User-Agent": "oma-http-client"}

        try:
            async with aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(ttl_dns_cache=30000, ssl=False),
                headers=self.headers,
                json_serialize=jsonplus.dumps,
                timeout=aiohttp.ClientTimeout(total=60),
            ) as auth_session:
                self.log.info(">> %s, login: %s", self._config.auth_url, self._config.login)

                response = await auth_session.post(
                    self._config.auth_url,
                    json=dict(login=self._config.login, secret=self._config.secret),
                    ssl=False,
                )

                self.log.info("<< %d : %s, %s", response.status, response.reason, self._config.auth_url)

                if response.status != 200:
                    self.log.error(
                        "Authentication error url: %s, status: %d, reason: %s",
                        self._config.auth_url,
                        response.status,
                        response.reason,
                    )
                    return False

                response_with_auth_token = await response.json()
                self._jwt_token = self.jwt.verify_token(response_with_auth_token.get("auth_token", None))

                if self._jwt_token is None:
                    self.log.warning("Authentication failed, Invalid token")
                    return False

                self.headers["Authorization"] = "Bearer " + str(self._jwt_token.token)
                return True

        except Exception as error:
            self.log.error("Authentication error", error=error)
            return False

    @property
    def session(self) -> aiohttp.ClientSession:
        """session"""
        if self._session is None:
            self._session = aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(ttl_dns_cache=30000, ssl=False),
                headers=self.headers,
                json_serialize=jsonplus.dumps,
                timeout=aiohttp.ClientTimeout(total=60),
            )
        return self._session

    async def get(self, params: dict) -> ModelsPage[ModelT]:
        """get"""
        if not await self.authenticate():
            return ModelsPage[self._model_class]()
        try:
            url = f"{self._config.api_url}{self.collection_name}"
            self.log.info(">> GET %s", url)
            response = await self.session.get(url=url, params=params, ssl=False)
            self.log.info("<< GET %s %d, %s", response.url, response.status, response.reason)

            if response.status != 200:
                self.log.error(
                    "Get error url: %s, status: %d, reason: %s",
                    response.url,
                    response.status,
                    response.reason,
                )
                return ModelsPage[self._model_class]()

            result = await response.json()

            models_page = ModelsPage[self._model_class](
                total=result.get("total"),
                items=list(map(lambda i: self._model_class(**i), result.get("items", []))),
            )
            return models_page
        except Exception as error:
            self.log.error("Can not get", error=error)
        return ModelsPage[self._model_class]()

    async def post(self, obj: ModelT) -> Optional[ModelT]:
        """post"""
        if not await self.authenticate():
            return None

        try:
            url = f"{self._config.api_url}{ self.collection_name}"
            self.log.info(">> POST %s", url)
            response = await self.session.post(url=url, json=obj, ssl=False)
            self.log.info("<< POST %s %d, %s", response.url, response.status, response.reason)

            if response.status != 201:
                self.log.error(
                    "Post error url: %s, status: %d, reason: %s",
                    response.url,
                    response.status,
                    response.reason,
                )
                return None

            result = await response.json()

            return self._model_class(**result)
        except Exception as error:
            self.log.error("Can not post", error=error)
        return None

    async def put(self, obj: ModelT) -> Optional[ModelT]:
        """put"""
        if not await self.authenticate():
            return None

        try:
            url = f"{self._config.api_url}{self.collection_name}/{str(obj.id)}"
            self.log.info(">> PUT %s", url)
            response = await self.session.put(url=url, json=obj, ssl=False)
            self.log.info("<< PUT %s %d, %s", response.url, response.status, response.reason)

            if response.status != 200:
                self.log.error(
                    "Put error url: %s, status: %d, reason: %s",
                    response.url,
                    response.status,
                    response.reason,
                )
                return None

            result = await response.json()

            return self._model_class(**result)
        except Exception as error:
            self.log.error("Can not put", error=error)
        return None

    async def get_one(self, obj_id: Any) -> Optional[ModelT]:
        """get_one"""
        if not await self.authenticate():
            return None
        try:
            url = f"{self._config.api_url}{self.collection_name}/{str(obj_id)}"
            self.log.info(">> GET %s", url)
            response = await self.session.get(url=url, ssl=False)
            self.log.info("<< GET %s %d, %s", response.url, response.status, response.reason)

            if response.status != 200:
                self.log.error(
                    "Get error url: %s, status: %d, reason: %s",
                    response.url,
                    response.status,
                    response.reason,
                )
                return None

            result = await response.json()

            return self._model_class(**result)
        except Exception as error:
            self.log.error("Can not get_one", error=error)
        return None

    async def get_one_self(self) -> Optional[ModelT]:
        """get_one_self"""
        if not await self.authenticate():
            return None
        try:
            url = f"{self._config.api_url}{self.collection_name}/self"
            self.log.info(">> GET %s", url)
            response = await self.session.get(url=url, ssl=False)
            self.log.info("<< GET %s %d, %s", response.url, response.status, response.reason)

            if response.status != 200:
                self.log.error(
                    "Get error url: %s, status: %d, reason: %s",
                    response.url,
                    response.status,
                    response.reason,
                )
                return None

            result = await response.json()

            return self._model_class(**result)
        except Exception as error:
            self.log.error("Can not get_one", error=error)
        return None

    async def patch(self, obj_id: Any, resource: dict) -> Optional[ModelT]:
        """patch"""
        if not await self.authenticate():
            return None
        try:
            url = f"{self._config.api_url}{self.collection_name}/{ str(obj_id)}"
            self.log.info(">> PATCH %s", url)
            response = await self.session.patch(url=url, json=resource, ssl=False)
            self.log.info("<< PATCH %s %d, %s", response.url, response.status, response.reason)

            if response.status != 200:
                self.log.error(
                    "Patch error url: %s, status: %d, reason: %s",
                    response.url,
                    response.status,
                    response.reason,
                )
                return None

            result = await response.json()

            return self._model_class(**result)
        except Exception as error:
            self.log.error("Can not patch", error=error)
        return None

    async def patch_self(self, resource: dict) -> Optional[ModelT]:
        """patch_self"""
        if not await self.authenticate():
            return None
        try:
            url = f"{self._config.api_url}{self.collection_name}/self"
            self.log.info(">> PATCH %s", url)
            response = await self.session.patch(url=url, json=resource, ssl=False)
            self.log.info("<< PATCH %s %d, %s", response.url, response.status, response.reason)

            if response.status != 200:
                self.log.error(
                    "Patch error url: %s, status: %d, reason: %s",
                    response.url,
                    response.status,
                    response.reason,
                )
                return None

            result = await response.json()

            return self._model_class(**result)
        except Exception as error:
            self.log.error("Can not patch", error=error)
        return None

    async def delete(self, obj_id: Any) -> Optional[ModelT]:
        """delete"""
        if not await self.authenticate():
            return None
        try:
            url = f"{self._config.api_url}{ self.collection_name}/{str(obj_id)}"
            self.log.info(">> DELETE %s", url)
            response = await self.session.delete(url=url, ssl=False)
            self.log.info("<< DELETE %s %d, %s", response.url, response.status, response.reason)

            if response.status != 200:
                self.log.error(
                    "Delete error url: %s, status: %d, reason: %s",
                    response.url,
                    response.status,
                    response.reason,
                )
                return None

            result = await response.json()

            return self._model_class(**result)
        except Exception as error:
            self.log.error("Can not delete", error=error)
        return None

    async def count(self, conditions: dict = None) -> int:
        """count"""
        if not await self.authenticate():
            return 0
        try:
            url = f"{self._config.api_url}{self.collection_name}/count"
            self.log.info(">> GET %s", url)
            response = await self.session.get(url=url, params=conditions, ssl=False)
            self.log.info("<< GET %s %d, %s", response.url, response.status, response.reason)

            if response.status != 200:
                self.log.error(
                    "Count error url: %s, status: %d, reason: %s",
                    response.url,
                    response.status,
                    response.reason,
                )
                return 0

            count = await response.json()

            return count.get("count", 0)
        except Exception as error:
            self.log.error("Can not count", error=error)
        return 0
