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

"""Logger processors"""

import multiprocessing
from logging import Logger

from structlog.types import EventDict

__all__ = ["add_proc_name", "add_logger_name"]


def add_proc_name(_, __, event_dict):
    """Log processor current process name"""

    event_dict["proc_name"] = multiprocessing.current_process().name

    return event_dict


def add_logger_name(logger: Logger, _: str, event_dict: EventDict):
    """Add the logger name to the event dict"""

    record = event_dict.get("_record", None)
    if record is None:
        event_dict["logger"] = logger.name
    else:
        event_dict["logger"] = record.name

    return event_dict
