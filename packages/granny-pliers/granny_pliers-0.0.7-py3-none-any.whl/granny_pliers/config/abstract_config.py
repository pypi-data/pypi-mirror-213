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

"""AbstractConfig"""
import inspect
import os
import pathlib
from abc import ABC
from dataclasses import dataclass, fields

import structlog
import yaml

__all__ = ["AbstractConfig", "ConfigError"]


class ConfigError(Exception):
    """ConfigError"""


@dataclass()
class AbstractConfig(ABC):
    """AbstractConfig"""

    def __post_init__(self):
        for field in fields(self):
            if issubclass(field.type, AbstractConfig):
                if (class_config := getattr(self, field.name, None)) is None:
                    continue
                parameters = inspect.signature(field.type).parameters
                filtered_config_dic = {k: v for k, v in class_config.items() if k in parameters}
                setattr(self, field.name, field.type(**filtered_config_dic))
                continue

            if (field_meta_type := field.metadata.get("type", None)) is None:
                msg = f"Field: {field.name} has unknown filed type"
                raise ConfigError(msg)

            if (env_var_name := field.metadata.get("env_var_name", None)) is None:
                continue

            if (value := os.getenv(env_var_name, None)) is None:
                continue

            setattr(self, field.name, field_meta_type(value))

    @classmethod
    def load(cls, config_file: pathlib.Path) -> "AbstractConfig":
        """Load config"""
        log = structlog.get_logger(cls.__name__)
        log.info("Loading config from: %s", config_file)
        if not config_file.exists():
            msg = f"Can not load config from {str(config_file)}, file not found"
            log.error(msg)
            raise ConfigError(msg)

        try:
            with config_file.open(mode="rt", encoding="UTF-8") as file:
                config_dict = yaml.full_load(file)

            if (class_config := config_dict.get(cls.__name__, None)) is None:
                msg = f"Can not load config from {str(config_file)}, root section: {cls.__name__} not found"
                log.error(msg)
                raise ConfigError(msg)

            parameters = inspect.signature(cls).parameters
            filtered_config_dic = {k: v for k, v in class_config.items() if k in parameters}
            config = cls(**filtered_config_dic)
            log.info("Configuration loaded [OK]")
            return config
        except ConfigError as error:
            raise error
        except Exception as error:
            msg = f"Can not load config from {str(config_file)}"
            log.error(msg, error=error)
            raise ConfigError(msg) from error
