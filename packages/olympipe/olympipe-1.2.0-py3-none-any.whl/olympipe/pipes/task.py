from typing import Any, Callable, TypeVar

from olympipe.shuttable_queue import ShuttableQueue

from .generic import GenericPipe

R = TypeVar("R")
S = TypeVar("S")


class TaskPipe(GenericPipe[R, S]):
    def __init__(
        self,
        source: "ShuttableQueue[R]",
        task: Callable[[R], S],
        target: "ShuttableQueue[S]",
        siblings_counter: Any,
        count: int,
    ):
        self._task = task
        super().__init__(source, target, siblings_counter, count)

    def _perform_task(self, data: R) -> S:
        return self._task(data)
