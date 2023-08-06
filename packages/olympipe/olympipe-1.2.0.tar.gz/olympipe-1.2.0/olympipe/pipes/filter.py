from multiprocessing import Value
from typing import Callable, TypeVar

from olympipe.shuttable_queue import ShuttableQueue

from .generic import GenericPipe

R = TypeVar("R")


class FilterPipe(GenericPipe[R, R]):
    def __init__(
        self,
        source: "ShuttableQueue[R]",
        task: Callable[[R], bool],
        target: "ShuttableQueue[R]",
    ):
        self._task = task
        sibling_counter = Value("i", 1)
        super().__init__(source, target, sibling_counter)

    def _perform_task(self, data: R) -> R:
        if self._task(data):
            super()._send_to_next(data)
        return data

    def _send_to_next(self, processed: R):
        pass
