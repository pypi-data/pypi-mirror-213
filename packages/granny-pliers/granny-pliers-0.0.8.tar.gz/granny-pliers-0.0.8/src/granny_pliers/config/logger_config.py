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

"""LoggerConfig"""

import logging.config
import sys
from dataclasses import dataclass, field

import structlog

from granny_pliers.logger import add_proc_name, add_logger_name
from .abstract_config import AbstractConfig
from .autowired_config import AutoWiredConfig
from .project_environment import ProjectEnvironment

__all__ = ["LoggerConfig"]


@dataclass()
class LoggerConfig(AbstractConfig):
    """LoggerConfig"""

    log_level: int = field(
        default=None,
        metadata={"env_var_name": "LOG_LEVEL", "type": str},
    )
    log_output_format: int = field(
        default="plain",
        metadata={"env_var_name": "LOG_OUTPUT_FORMAT", "type": str},
    )

    auto_wired: AutoWiredConfig = None

    def get_log_level_from_env(self) -> int:
        """get_log_level_from_env"""
        return {
            ProjectEnvironment.LOCAL: logging.DEBUG,
            ProjectEnvironment.DEV: logging.DEBUG,
            ProjectEnvironment.STAGE: logging.DEBUG,
            ProjectEnvironment.TEST: logging.DEBUG,
            ProjectEnvironment.PROD: logging.INFO,
        }.get(self.auto_wired.environment, logging.INFO)

    def __post_init__(self):
        super().__post_init__()

        if self.log_level is None:
            self.log_level = self.get_log_level_from_env()
        elif isinstance(self.log_level, str):
            self.log_level = logging.getLevelNamesMapping()[self.log_level]

    def setup(self):
        """Initialize and setup logger"""
        logging.config.dictConfig(
            {
                "version": 1,
                "disable_existing_loggers": False,
                "loggers": {
                    "": {
                        "level": self.log_level,
                        "handlers": [self.auto_wired.environment],
                        "propagate": 1,
                    }
                },
                "handlers": {
                    ProjectEnvironment.LOCAL.value: {
                        "class": "logging.StreamHandler",
                        "formatter": ProjectEnvironment.LOCAL.value,
                        "stream": sys.stdout,
                    },
                    ProjectEnvironment.DEV.value: {
                        "class": "logging.StreamHandler",
                        "formatter": ProjectEnvironment.DEV.value,
                        "stream": sys.stdout,
                    },
                    ProjectEnvironment.STAGE.value: {
                        "class": "logging.StreamHandler",
                        "formatter": ProjectEnvironment.STAGE.value,
                        "stream": sys.stdout,
                    },
                    ProjectEnvironment.PROD.value: {
                        "class": "logging.StreamHandler",
                        "formatter": ProjectEnvironment.PROD.value,
                        "stream": sys.stdout,
                    },
                    ProjectEnvironment.TEST.value: {
                        "class": "logging.StreamHandler",
                        "formatter": ProjectEnvironment.TEST.value,
                        "stream": sys.stdout,
                    },
                },
                "formatters": {
                    ProjectEnvironment.LOCAL.value: {
                        "()": structlog.stdlib.ProcessorFormatter,
                        "processor": structlog.dev.ConsoleRenderer(pad_event=100, colors=True),
                    },
                    ProjectEnvironment.DEV.value: {
                        "()": structlog.stdlib.ProcessorFormatter,
                        "processor": structlog.dev.ConsoleRenderer(colors=False),
                    },
                    ProjectEnvironment.PROD.value: {
                        "()": structlog.stdlib.ProcessorFormatter,
                        "processor": structlog.dev.ConsoleRenderer(colors=False),
                    },
                    ProjectEnvironment.STAGE.value: {
                        "()": structlog.stdlib.ProcessorFormatter,
                        "processor": structlog.dev.ConsoleRenderer(colors=False),
                    },
                    ProjectEnvironment.TEST.value: {
                        "()": structlog.stdlib.ProcessorFormatter,
                        "processor": structlog.dev.ConsoleRenderer(colors=False),
                    },
                },
            }
        )

        log_processors = [
            structlog.processors.TimeStamper(fmt="iso"),
            add_proc_name,
            add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
        ]
        if self.log_output_format == "json":
            log_processors += [
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                structlog.processors.JSONRenderer(),
            ]
        else:
            log_processors += [
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
            ]
        structlog.configure(
            processors=log_processors,
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )
