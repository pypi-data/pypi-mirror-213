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

"""AbstractHealthStatusWebService"""

from abc import ABC, abstractmethod

import jsonplus
from aiohttp import web

from granny_pliers.config import AutoWiredConfig
from granny_pliers.logger import AbstractLogger
from granny_pliers.models.web import WebServiceHealthStatus

__all__ = ["AbstractHealthStatusWebService"]


class AbstractHealthStatusWebService(AbstractLogger, ABC):
    """AbstractHealthStatusWebService"""

    def __init__(self, base_path: str):
        super().__init__()
        self.base_path = base_path
        self.autowired_config = AutoWiredConfig()
        self.log.info("Initialized %s", self.path)

    @property
    @abstractmethod
    def name(self) -> str:
        """service name"""

    @property
    def path(self) -> str:
        """base_path/service_name"""
        return f"{self.base_path}/{self.name}"

    @property
    def routes(self):
        """routes"""
        return [web.get(self.path, self.get)]

    async def generate_status(self) -> WebServiceHealthStatus:
        """generate_status"""
        return WebServiceHealthStatus(
            environment=self.autowired_config.environment,
            ci_commit_branch=self.autowired_config.commit_branch,
            ci_commit_short_sha=self.autowired_config.commit_short_sha,
            status="ok",
        )

    async def get(self, _) -> web.Response:
        """Get SS Service status

        :return: JSON - SSServiceHealthStatus
        """
        return web.json_response(await self.generate_status(), dumps=jsonplus.dumps)
