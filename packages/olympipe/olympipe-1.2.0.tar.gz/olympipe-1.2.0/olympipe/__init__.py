__version__ = "1.2.0"

from multiprocessing import TimeoutError, Value
from queue import Empty, Full
from threading import Timer
import time
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Iterable,
    List,
    Optional,
    TypeVar,
)
from olympipe.shuttable_queue import ShuttableQueue

from olympipe.pipes.batch import BatchPipe
from olympipe.pipes.explode import ExplodePipe
from olympipe.pipes.filter import FilterPipe
from olympipe.pipes.instance import ClassInstancePipe
from olympipe.pipes.reduce import ReducePipe
from olympipe.pipes.task import TaskPipe
from olympipe.pipes.timebatch import TimeBatchPipe

R = TypeVar("R")
S = TypeVar("S")
T = TypeVar("T")


class Pipeline(Generic[T]):
    def __init__(
        self,
        datas: Optional[Iterable[T]] = None,
        source: Optional["ShuttableQueue[Any]"] = None,
        output_queue: Optional["ShuttableQueue[T]"] = None,
    ):
        self._source_queue = source
        self._output_queue: "ShuttableQueue[T]" = (
            Pipeline.get_new_queue() if output_queue is None else output_queue
        )
        self._datas = datas
        self._contains = Value("i", 0)
        Timer(0, self.start).start()

    @staticmethod
    def get_new_queue() -> "ShuttableQueue[Any]":
        queue: "ShuttableQueue[Any]" = ShuttableQueue()
        return queue

    def start(self):
        if self._datas is not None:
            for data in self._datas:
                while True:
                    try:
                        self._output_queue.put(data, timeout=0.1)
                        break
                    except Exception:
                        pass
            while not self._output_queue.empty():
                time.sleep(0.1)
            while self._source_queue is not None and not self._source_queue.empty():
                time.sleep(0.1)
            if self._source_queue is not None:
                self._source_queue.shutdown()
                time.sleep(0.1)
            self._output_queue.shutdown()

    def task(self, task: Callable[[T], S], count: int = 1) -> "Pipeline[S]":
        assert count >= 1

        output_task_queue: "ShuttableQueue[S]" = Pipeline.get_new_queue()

        sibling_counter = Value("i", count)
        for _ in range(count):
            _ = TaskPipe(
                self._output_queue, task, output_task_queue, sibling_counter, count
            )

        return Pipeline(
            source=self._output_queue,
            output_queue=output_task_queue,
        )

    def class_task(
        self,
        class_constructor: Any,
        class_method: Callable[[Any, T], S],
        class_args: List[Any] = [],
        close_method: Optional[Callable[[Any], Any]] = None,
        class_kwargs: Dict[str, Any] = {},
        count: int = 1,
    ) -> "Pipeline[S]":
        assert count >= 1
        output_task_queue: "ShuttableQueue[S]" = Pipeline.get_new_queue()

        sibling_counter = Value("i", count)
        for _ in range(count):
            _ = ClassInstancePipe(
                self._output_queue,
                class_constructor,
                class_method,
                output_task_queue,
                sibling_counter,
                count,
                close_method,
                class_args,
                class_kwargs,
            )
        return Pipeline(
            source=self._output_queue,
            output_queue=output_task_queue,
        )

    def explode(self, explode_function: Callable[[T], Iterable[S]]) -> "Pipeline[S]":
        output_task_queue: "ShuttableQueue[S]" = Pipeline.get_new_queue()

        _ = ExplodePipe(self._output_queue, explode_function, output_task_queue)

        return Pipeline(
            source=self._output_queue,
            output_queue=output_task_queue,
        )

    def batch(
        self, count: int = 2, keep_incomplete_batch: bool = True
    ) -> "Pipeline[List[T]]":
        output_task_queue: "ShuttableQueue[List[T]]" = Pipeline.get_new_queue()
        _ = BatchPipe(
            self._output_queue, output_task_queue, count, keep_incomplete_batch
        )
        return Pipeline(source=self._output_queue, output_queue=output_task_queue)

    def temporal_batch(self, time_interval: float) -> "Pipeline[List[T]]":
        output_task_queue: "ShuttableQueue[List[T]]" = Pipeline.get_new_queue()
        _ = TimeBatchPipe(self._output_queue, output_task_queue, time_interval)

        return Pipeline(source=self._output_queue, output_queue=output_task_queue)

    def filter(self, filter_function: Callable[[T], bool]) -> "Pipeline[T]":
        output_task_queue: "ShuttableQueue[T]" = Pipeline.get_new_queue()

        _ = FilterPipe(self._output_queue, filter_function, output_task_queue)

        return Pipeline(source=self._output_queue, output_queue=output_task_queue)

    @staticmethod
    def print_return(data: S) -> S:
        print(f"debug_pipe {data}")
        return data

    def debug(self) -> "Pipeline[T]":
        return self.task(Pipeline.print_return)

    def reduce(self, accumulator: R, reducer: Callable[[T, R], R]) -> "Pipeline[R]":
        task_output_queue: "ShuttableQueue[R]" = Pipeline.get_new_queue()

        _ = ReducePipe(self._output_queue, task_output_queue, accumulator, reducer)
        return Pipeline(source=self._output_queue, output_queue=task_output_queue)

    def wait_and_reduce(
        self,
        accumulator: R,
        reducer: Callable[[T, R], R],
    ) -> "R":
        output_pipeline = self.reduce(accumulator, reducer)
        [[res]] = Pipeline._wait_for_all_results([output_pipeline])
        return res

    @staticmethod
    def _wait_for_all_completions(pipes: List["Pipeline[Any]"]) -> None:
        final_queues: List[Optional[ShuttableQueue[Any]]] = [
            p._output_queue for p in pipes
        ]

        while any(final_queues):
            for i, final_queue in enumerate(final_queues):
                if final_queue is None:
                    continue
                try:
                    _ = final_queue.get(timeout=0.1)
                except:
                    pass
                if final_queue.shutted:
                    final_queues[i] = None

    @staticmethod
    def _wait_for_all_results(pipes: List["Pipeline[Any]"]) -> List[List[Any]]:
        final_queues: List[Optional[ShuttableQueue[Any]]] = [
            p._output_queue for p in pipes
        ]

        outputs: List[List[Any]] = [[] for _ in pipes]

        while any(final_queues) > 0:
            for i, final_queue in enumerate(final_queues):
                if final_queue is None:
                    continue
                try:
                    packet = final_queue.get(timeout=0.1)
                    outputs[i].append(packet)
                except TimeoutError:
                    pass
                except Full:
                    pass
                except Empty:
                    pass
                except Exception as e:
                    print("Error waiting:", e)
                    final_queues[i] = None

                if final_queue.shutted and final_queue.empty():
                    final_queues[i] = None

        return outputs

    def wait_for_completion(self, other_pipes: List["Pipeline[Any]"] = []) -> None:
        """_summary_

        Args:
            other_pipes (List[&quot;Pipeline[Any]&quot;], optional): _description_. Defaults to [].

        Returns:
            _type_: _description_
        """
        return Pipeline._wait_for_all_completions([self, *other_pipes])

    def wait_for_results(
        self, other_pipes: List["Pipeline[Any]"] = []
    ) -> List[List[T]]:
        """_summary_

        Args:
            other_pipes (List[&quot;Pipeline[Any]&quot;], optional): _description_. Defaults to [].

        Returns:
            List[List[R]]: _description_
        """
        return Pipeline._wait_for_all_results([self, *other_pipes])

    def wait_for_result(self) -> List[T]:
        """
        Args:

        Returns:
            Iterable[R]: _description_
        """
        res: List[List[T]] = Pipeline._wait_for_all_results([self])
        return res[0]
