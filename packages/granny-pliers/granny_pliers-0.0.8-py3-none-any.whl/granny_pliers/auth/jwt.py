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

"""JWT"""

import datetime
from base64 import urlsafe_b64encode, urlsafe_b64decode
from dataclasses import dataclass, asdict, field
from typing import Optional

import jsonplus

from granny_pliers.logger import AbstractLogger
from .auth_config import AuthConfig
from .rsa_codec import RSACodec

__all__ = ["JwtHeader", "JwtPayload", "JwtToken", "Jwt"]


@dataclass(frozen=True, repr=False, eq=False)
class JwtHeader:
    """JwtHeader"""

    alg: str = "RS256"
    typ = "JWT"


@dataclass(frozen=True, repr=False, eq=False)
class JwtPayload:
    """Jwt payload"""

    user_id: str
    expired_at: int
    role: str


@dataclass(frozen=True, repr=False, eq=False)
class JwtToken:
    """JwtToken"""

    payload: JwtPayload
    token: str
    header: JwtHeader = field(default=JwtHeader())


class Jwt(AbstractLogger):
    """Jwt class"""

    @property
    def private_key(self) -> Optional[bytes]:
        """private_key"""
        private_key_base64 = self.config.jwt_private_key
        if private_key_base64 is not None:
            key = urlsafe_b64decode(private_key_base64)
            return key
        return None

    @property
    def public_key(self) -> Optional[bytes]:
        """public_key"""
        public_key_base64 = self.config.jwt_public_key
        if public_key_base64 is not None:
            key = urlsafe_b64decode(public_key_base64)
            return key
        return None

    def __init__(self, config: AuthConfig):
        super().__init__()
        self.config = config
        self.rsa = RSACodec(
            key_password=self.config.jwt_private_key_secret,
            private_key_pem=self.private_key,
            private_key_filename=self.config.jwt_private_key_file,
            public_key_pem=self.public_key,
            public_key_file_name=self.config.jwt_public_key_file,
        )

    def generate_token(self, user_id: str, role: str, custom_jwt_token_life_time_ms: int = None) -> JwtToken:
        """
        Generated JWT token

        :param user_id:
        :param role:
        :param custom_jwt_token_life_time_ms
        :return:
        """

        self.log.info("Generating jwt token...", user_id=user_id)

        expired_at = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
        if custom_jwt_token_life_time_ms is None:
            expired_at += datetime.timedelta(milliseconds=self.config.jwt_token_life_time_ms)
        else:
            expired_at += datetime.timedelta(milliseconds=custom_jwt_token_life_time_ms)

        header = JwtHeader()

        payload = JwtPayload(
            user_id=user_id,
            expired_at=round(expired_at.timestamp() * 1000),
            role=role,
        )

        base64_header = urlsafe_b64encode(jsonplus.dumps(asdict(header)).encode()).decode()
        base64_payload = urlsafe_b64encode(jsonplus.dumps(asdict(payload)).encode()).decode()
        signature = urlsafe_b64encode(self.rsa.sign(f"{base64_header}.{base64_payload}".encode())).decode()

        token = f"{base64_header}.{base64_payload}.{signature}"
        self.log.info("Jwt token has been generated", user_id=user_id, expired_at=payload.expired_at)
        return JwtToken(payload, token)

    def verify_token(self, token: str) -> Optional[JwtToken]:
        """
        Verify token

        :param token:
        :return: Parsed valid JwtToken or None if not valid
        """
        if token is None:
            self.log.warning("Jwt token verification failed, token is empty")
            return None

        try:
            # self.log.info("Verifying jwt token...")
            header, payload, signature = token.split(".")

            if not self.rsa.verify(f"{header}.{payload}".encode(), urlsafe_b64decode(signature)):
                self.log.warning("Jwt token verification failed, invalid signature")
                return None

            payload = JwtPayload(**jsonplus.loads(urlsafe_b64decode(payload)))

            current_time = round(datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).timestamp() * 1000)
            if payload.expired_at < current_time:
                self.log.warning(
                    "Jwt token verification failed, token is expired",
                    user_id=payload.user_id,
                    expired_at=payload.expired_at,
                    current_time=current_time,
                )
                return None

            self.log.info("Jwt token has been verified", user_id=payload.user_id)
            return JwtToken(payload, token)

        except (ValueError, TypeError, AttributeError) as error:
            self.log.error("Jwt token verification failed, unexpected error", error=error)
        return None

    def refresh_token(self, jwt_token: JwtToken) -> Optional[JwtToken]:
        """
        Refresh token

        :param jwt_token:
        :return: New refreshed valid JwtToken or None if not valid
        """
        try:
            self.log.info("Refreshing jwt token...", user_id=jwt_token.payload.user_id)
            new_token = self.generate_token(
                jwt_token.payload.user_id,
                jwt_token.payload.role,
            )
            self.log.info(
                "Jwt token has been refreshed",
                user_id=new_token.payload.user_id,
                expired_at=new_token.payload.expired_at,
            )
            return new_token
        except (ValueError, TypeError, AttributeError) as error:
            self.log.error("Jwt token refresh failed, unexpected error", error=error)
        return None
