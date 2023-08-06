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

"""AbstractTestCase"""

import os
from abc import abstractmethod, ABC
from unittest import TestCase

import jsonplus

from granny_pliers.logger import AbstractLogger

__all__ = ["AbstractTestCase", "AbstractTest"]


class AbstractTest(AbstractLogger, ABC):
    """AbstractTest"""

    @property
    @abstractmethod
    def working_dir(self) -> str:
        """Set test case working directory"""

    @property
    def debug_dir(self) -> str:
        """Set test case debug directory"""
        debug_directory = os.path.join(self.working_dir, "debug")
        if not os.path.exists(debug_directory):
            os.makedirs(debug_directory)
        return debug_directory

    @property
    def data_dir(self) -> str:
        """Set test case data directory"""
        data_directory = os.path.join(self.working_dir, "data")
        if not os.path.exists(data_directory):
            os.makedirs(data_directory)
        return data_directory

    def load_test_json_data(self, data_file) -> dict:
        """
        Loads test data from file. File should be placed in data dir near the current py file
        :param data_file:
        :return:
        """
        with open(f"{self.data_dir}/{data_file}", "rt", encoding="UTF-8") as file:
            data = jsonplus.loads(file.read())

        return data


class AbstractTestCase(TestCase, AbstractTest, ABC):
    """AbstractTestCase"""
