from multiprocessing import Value
from typing import Callable, Iterable, TypeVar

from olympipe.pipes.task import TaskPipe
from olympipe.shuttable_queue import ShuttableQueue

R = TypeVar("R")
S = TypeVar("S")


class ExplodePipe(TaskPipe[R, S]):
    def __init__(
        self,
        source: "ShuttableQueue[R]",
        task: Callable[[R], Iterable[S]],
        target: "ShuttableQueue[S]",
    ):
        sibling_counter = Value("i", 1)
        super().__init__(source, task, target, sibling_counter, 1)  # type: ignore

    def _send_to_next(self, processed: Iterable[S]):  # type: ignore
        for p in processed:
            super()._send_to_next(p)
