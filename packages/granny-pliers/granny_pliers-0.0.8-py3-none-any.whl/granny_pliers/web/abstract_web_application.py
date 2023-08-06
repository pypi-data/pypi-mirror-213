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

"""AbstractWebApplication"""

from abc import ABC, abstractmethod

from aiohttp import web

from granny_pliers.auth import Jwt
from granny_pliers.logger import AbstractLogger
from .web_application_config import WebApplicationConfig

__all__ = ["AbstractWebApplication"]


class AbstractWebApplication(AbstractLogger, ABC):
    """Abstract WebApplication class"""

    def __init__(self, config: WebApplicationConfig):
        super().__init__()
        self.__my_server = None
        self.web_app = None
        self.__jwt = None
        self.config = config

    @property
    def jwt(self) -> Jwt:
        """JWT"""
        if self.__jwt is None:
            self.__jwt = Jwt(self.config.auth)
        return self.__jwt

    async def start(self):
        """
        Since web application will be started as worker, it requires method start and stop.
        Initializes all required for web application objects.
        """
        self.log.info("Launching Web server...")

        self.__jwt = Jwt(self.config.auth)

        self.web_app = web.Application(client_max_size=self.config.client_max_size)
        self.init_middleware()
        self.init_routes()

        web_app_runner = web.AppRunner(self.web_app)

        await web_app_runner.setup()

        self.__my_server = web.TCPSite(web_app_runner, self.config.host, self.config.port)

        self.log.debug("Web Server started %s", f"http://{self.config.host}:{self.config.port}")

        return await self.__my_server.start()

    async def stop(self):
        """Stops running worker, uses for graceful shutdown"""
        await self.__my_server.stop()

    def init_middleware(self):
        """init_middleware"""
        self.web_app.middlewares.append(self.error_handler)
        self.web_app.middlewares.append(self.auth_handler)

    @abstractmethod
    def init_routes(self):
        """Add here all web app routes"""

    @web.middleware
    async def error_handler(self, request: web.Request, handler):
        """Wrap http errors to JSON"""
        try:
            response: web.Response = await handler(request)
            if 400 <= response.status <= 599:
                self.log.error("Response error", response=response, request=request)
                return web.json_response({"error": response.text}, status=response.status)

            return response
        except web.HTTPException as ex:
            self.log.error("Response error", error=ex, request=request, headers=request.headers)
            return web.json_response({"error": ex.text}, status=ex.status)

    @web.middleware
    async def auth_handler(self, request: web.Request, handler):
        """
        Middleware that extracts and validate AuthToken

        :param request:
        :param handler:
        :return:
        """
        request["jwt"] = self.jwt
        request["jwt_token_name"] = None

        auth_header = request.headers.getone("Authorization", None)
        if auth_header is not None:
            try:
                _, token = auth_header.split(" ")
                auth_token = self.jwt.verify_token(token)

                if auth_token is not None:
                    request["jwt_token_name"] = auth_token
                else:
                    self.log.warning("Unauthorized access", remote=request.remote)
                    return web.HTTPForbidden(text="Access forbidden")
            except (ValueError, TypeError) as error:
                self.log.error("Can not parse Auth token", error=error)
                return web.HTTPForbidden(text="Access forbidden")

        response = await handler(request)
        return response
