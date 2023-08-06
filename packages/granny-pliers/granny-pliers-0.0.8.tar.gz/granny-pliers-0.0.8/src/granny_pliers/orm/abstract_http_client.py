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

"""AbstractHttpClient"""

import asyncio
from abc import abstractmethod
from types import TracebackType
from typing import Optional, Type, Any

import aiohttp
import jsonplus

from granny_pliers.logger import AbstractLogger

__all__ = ["AbstractHttpClient"]


class AbstractHttpClient(AbstractLogger):
    """AbstractHttpClient"""

    def __init__(self):
        super().__init__()
        self._session = None
        self._custom_headers = {}

    @property
    def timeout(self):
        """Default http connection time out is seconds"""
        return aiohttp.ClientTimeout(total=60)

    @property
    @abstractmethod
    def url(self):
        """Base http url""" ""

    @property
    def header_accept(self) -> dict[str, str]:
        """Custom accept header"""
        return {"Accept": "application/json"}

    @property
    def header_user_agent(self) -> dict[str, str]:
        """Custom user-agent header"""
        return {"User-Agent": "granny-pliers-http-client"}

    @property
    def headers_custom(self) -> dict[str, str]:
        """Custom other header"""
        return self._custom_headers

    @property
    def session(self) -> aiohttp.ClientSession:
        """Current session"""
        if self._session is None:
            if self.header_accept.get("Accept") == "application/json":
                self._session = aiohttp.ClientSession(
                    connector=aiohttp.TCPConnector(ttl_dns_cache=30000, ssl=False),
                    headers={**self.header_accept, **self.header_user_agent, **self.headers_custom},
                    json_serialize=jsonplus.dumps,
                    timeout=self.timeout,
                )
            else:
                self._session = aiohttp.ClientSession(
                    connector=aiohttp.TCPConnector(ttl_dns_cache=30000, ssl=False),
                    headers={**self.header_accept, **self.header_user_agent},
                    timeout=self.timeout,
                )
        return self._session

    async def close(self):
        """Close session"""
        if self._session is not None:
            self._session.close()

    async def __aenter__(self):
        """Async session context"""
        return self

    async def __aexit__(
        self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException], exc_tb: Optional[TracebackType]
    ) -> None:
        """Close Async session context"""
        if self._session is not None:
            await self._session.close()

    async def _get_request(self, url: str, params: dict) -> Optional[Any]:
        try:
            self.log.info("==>> GET %s", url, params=params)
            response = await self.session.get(url, params=params, ssl=False)
            self.log.info("<<== %d %s %s", response.status, response.reason, url)
            if response.status == 200:
                if self.header_accept.get("Accept") == "application/json":
                    return await response.json()
                return await response.text()
        except Exception as error:
            self.log.error("%s client error", self.__class__.__name__, error=error)
        return None

    async def _patch_request(self, url: str, params: dict) -> Optional[Any]:
        try:
            self.log.info("==>> PATCH %s", url, params=params)
            response = await self.session.patch(url, data=jsonplus.dumps(params), ssl=False)
            self.log.info("<<== %d : %s, %s", response.status, response.reason, url)
            if response.status == 200:
                if self.header_accept.get("Accept") == "application/json":
                    return await response.json()
                return await response.text()
        except Exception as error:
            self.log.error("%s client error", self.__class__.__name__, error=error)
        return None

    async def get(self, url: str, params: dict, retries: int = 10, delay: float = 5.0) -> Optional[dict]:
        """get"""
        while retries > 0:
            result = await self._get_request(url, params)
            if result is None:
                self.log.warning("Http result is empty, retry... (retries left: %d)", retries, url=url, params=params)
                await asyncio.sleep(delay)
                retries -= 1
                delay += 5
                continue
            return result
        return None

    async def patch(self, url: str, params: dict, retries: int = 10, delay: float = 5.0) -> Optional[dict]:
        """patch"""
        while retries > 0:
            result = await self._patch_request(url, params)
            if result is None:
                self.log.warning("Http result is empty, retry... (retries left: %d)", retries, url=url, params=params)
                await asyncio.sleep(delay)
                retries -= 1
                delay += 5
                continue
            return result
        return None
