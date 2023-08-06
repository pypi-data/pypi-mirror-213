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

"""Workers"""

import asyncio
import multiprocessing
import platform
import signal
from abc import abstractmethod, ABC
from typing import Type, TypeVar

from granny_pliers.logger import AbstractLogger

__all__ = [
    "AbstractWorker",
    "AbstractWorkerProcess",
    "AbstractConsumerProcess",
    "AbstractPublisherProcess",
    "AbstractProcessPool",
    "ProcessPoolPublishers",
    "ProcessPoolConsumers",
]


class AbstractWorker(AbstractLogger, ABC):
    """AbstractWorker"""

    def __init__(self):
        super().__init__()
        self._loop = None

    @property
    def loop(self):
        """event loop"""
        if self._loop is None:
            self._loop = asyncio.get_event_loop()
        return self._loop

    @abstractmethod
    async def _process(self):
        """Process body"""

    def run(self) -> None:
        """main run loop"""
        name = multiprocessing.current_process().name

        if platform.system() == "Windows":
            signal.signal(signal.SIGINT, self.windows_graceful_shutdown)
            signal.signal(signal.SIGTERM, self.windows_graceful_shutdown)
        else:
            for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGHUP]:
                self.loop.add_signal_handler(sig, self.loop.stop)

        try:
            self.log.info("Initializing process %s...", name)
            self.loop.create_task(self._process())
            self.log.info("Process %s is started", name)

            self.loop.run_forever()
        finally:
            self.shutdown()
            self.log.info("Process %s is finished", name)
            self.loop.close()

    def shutdown(self):
        """Graceful process shutdown"""
        name = multiprocessing.current_process().name
        self.log.info("Shutting down %s ...", name)
        tasks = [task for task in asyncio.all_tasks(self.loop) if task is not asyncio.current_task(self.loop)]
        for task in tasks:
            task.cancel()

        self.loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
        self.log.info("Process %s is shutdown", name)

    def windows_graceful_shutdown(self, _):
        """Graceful shutdown for Windows"""
        self.loop.stop()


class AbstractWorkerProcess(AbstractWorker, multiprocessing.Process, ABC):
    """AbstractWorkerProcess"""


class AbstractConsumerProcess(AbstractWorkerProcess, ABC):
    """AbstractConsumerProcess"""

    def __init__(self, queue: multiprocessing.JoinableQueue, config):
        super().__init__()
        self.queue = queue
        self.config = config

    @abstractmethod
    async def _process_task(self, task: dict):
        """Process body"""

    async def _process(self):
        while 1:
            task = self.queue.get()

            if task is None:
                self.queue.task_done()
                self.loop.stop()
                break

            await self._process_task(task)

            self.queue.task_done()


class AbstractPublisherProcess(AbstractWorkerProcess, ABC):
    """AbstractPublisherProcess"""

    def __init__(self, queue: multiprocessing.JoinableQueue, config):
        super().__init__()
        self.queue = queue
        self.config = config


AbstractQueueProcess = TypeVar(
    "AbstractQueueProcess",
    AbstractConsumerProcess,
    AbstractPublisherProcess,
)


class AbstractProcessPool(AbstractLogger, ABC):
    """AbstractProcessPool"""

    def __init__(
        self,
        cls: Type[AbstractQueueProcess],
        queue: multiprocessing.JoinableQueue,
        config,
        size: int = 1,
    ):
        super().__init__()
        self._cls = cls
        self._size = size
        self._queue = queue
        self._pool: list[AbstractQueueProcess] = [cls(queue, config) for _ in range(size)]
        self.config = config

    def start(self):
        """Start the process"""
        for process in self._pool:
            process.start()

    @abstractmethod
    def stop(self):
        """Stop the process"""


class ProcessPoolPublishers(AbstractProcessPool):
    """ProcessPoolPublishers"""

    def stop(self):
        for process in self._pool:
            if process.is_alive():
                process.join()


class ProcessPoolConsumers(AbstractProcessPool):
    """ProcessPoolConsumers"""

    def stop(self):
        for _ in self._pool:
            self._queue.put(None)

        self._queue.join()

        for process in self._pool:
            if process.is_alive():
                process.join()
