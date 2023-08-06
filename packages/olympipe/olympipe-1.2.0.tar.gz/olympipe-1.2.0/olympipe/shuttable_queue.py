from multiprocessing import Value, get_context
from multiprocessing.queues import Queue
import time
from typing import Any, Generic, Optional, TypeVar

R = TypeVar("R")


class ShuttableQueue(Queue, Generic[R]):
    _max_queue_size = 1

    def __init__(self) -> None:
        ctx = get_context()
        super().__init__(ShuttableQueue._max_queue_size, ctx=ctx)
        self._shut = Value("b", False)

    def shutdown(self):
        time.sleep(0.05)
        with self._shut.get_lock():
            self._shut.value = True

    @property
    def shutted(self) -> bool:
        with self._shut.get_lock():
            return self._shut.value  # type: ignore

    def put(
        self, obj: Any, block: bool = True, timeout: Optional[float] = None
    ) -> None:
        if self.shutted:
            raise Exception("Dont you dare put this here")
        return super().put(obj, block, timeout)
