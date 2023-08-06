import queue
import time
from multiprocessing import Value
from typing import List, Optional, TypeVar

from olympipe.shuttable_queue import ShuttableQueue

from .generic import GenericPipe

R = TypeVar("R")
S = TypeVar("S")
T = TypeVar("T")


class TimeBatchPipe(GenericPipe[R, List[R]]):
    def __init__(
        self,
        source: "ShuttableQueue[R]",
        target: "ShuttableQueue[List[R]]",
        interval: float,
    ):
        self._interval: float = interval
        self._timeout: float = interval
        self._datas: List[R] = []
        self._last_time = time.time()
        sibling_counter = Value("i", 1)
        super().__init__(source, target, sibling_counter)

    def _perform_task(self, data: R) -> Optional[List[R]]:  # type: ignore
        elapsed = time.time() - self._last_time
        self._timeout = self._last_time + self._interval - time.time()
        if elapsed >= self._interval:
            self.increment_timeout()
            packet = self._datas[:]
            self._datas.clear()
            self._datas.append(data)
            return packet
        self._datas.append(data)
        return None

    def increment_timeout(self):
        self._last_time += self._interval
        self._timeout += self._interval

    def _send_to_next(self, processed: List[R]):
        super()._send_to_next(processed)

    def run(self):
        while True:
            try:
                data = self._source_queue.get(timeout=self._timeout)
                processed = self._perform_task(data)
                if processed is not None:
                    self._send_to_next(processed)
            except queue.Empty:
                pass
            except TimeoutError:
                self._send_to_next(self._datas)
                self._datas = []
            except Exception:
                self.increment_timeout()
            if self._source_queue.shutted:
                self._send_to_next(self._datas)
                self._kill()
