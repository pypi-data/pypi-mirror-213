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

"""datetime helper"""

from datetime import datetime, date, timezone
from typing import TypeVar

import dateparser

__all__ = ["setup_datetime"]
SomeDateTime = TypeVar("SomeDateTime", datetime, date, str, int)


def setup_datetime(value: SomeDateTime = None) -> datetime:
    """Aligns datetime to OMA standard datetime.

    :param value: None, str, date or datetime
    :return: aligned datetime with timezone UTC if successful, else raises TypeError exception
    """

    if value is None:
        return datetime.now(timezone.utc).replace(microsecond=0)

    value_type = type(value)

    if value_type is datetime:
        return value.replace(microsecond=0, tzinfo=timezone.utc)

    if value_type is str:
        try:
            # Mostly using mogodb iso date time, let try to read it
            result = datetime.fromisoformat(value.replace("Z", "+00:00"))
            return result.replace(microsecond=0, tzinfo=timezone.utc)
        except (TypeError, ValueError):
            pass

        result = dateparser.parse(value)
        if result is None:
            raise TypeError(f"Can not convert {value_type.__name__}: {value} into datetime")
        return result.replace(microsecond=0, tzinfo=timezone.utc)

    if value_type is date:
        return datetime(
            year=value.year,
            month=value.month,
            day=value.day,
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
            tzinfo=timezone.utc,
        )

    if value_type is int:
        return datetime.fromtimestamp(value)

    raise TypeError(f"Can not convert {value_type.__name__}: {value} into datetime")
