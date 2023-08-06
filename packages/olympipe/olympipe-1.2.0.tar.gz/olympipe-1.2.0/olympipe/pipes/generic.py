from multiprocessing import Process
from queue import Empty, Full
import time
from typing import Any, Generic, Optional, Tuple, TypeVar, cast

from olympipe.shuttable_queue import ShuttableQueue

R = TypeVar("R")
S = TypeVar("S")


class GenericPipe(Process, Generic[R, S]):
    DEBUG = False

    def __init__(
        self,
        source: "ShuttableQueue[R]",
        target: "ShuttableQueue[S]",
        siblings_counter: "Any",
        count: int = 1,
    ):
        self.siblings_counter = siblings_counter
        self._timeout: Optional[float] = 0.1
        self._source_queue = source
        self._target_queue = target
        self._siblings_count = count
        super().__init__()
        self.daemon = True
        self.start()

    def get_ends(self) -> "Tuple[ShuttableQueue[R], Process, ShuttableQueue[S]]":
        return (self._source_queue, self, self._target_queue)

    def _kill(self):
        finish_queue = False
        with self.siblings_counter.get_lock():
            if self.DEBUG:
                print(self, self.siblings_counter.value)
            self.siblings_counter.value -= 1
            if self.siblings_counter.value == 0:
                finish_queue = True

        if finish_queue:
            if self.DEBUG:
                print(self, "Killing...")
            self._close_output_queue()

        try:
            self.kill()
        except:
            pass

    def _close_output_queue(self):
        try:
            # This should already be closed
            self._source_queue.shutdown()
        except:
            pass
        try:
            time.sleep(0.1)
            while not self._target_queue.empty():
                time.sleep(0.1)
            if self.DEBUG:
                print("Close output queue")
            self._target_queue.shutdown()
        except Exception as e:
            print("Failed: Could not close", e)

        try:
            self.kill()
        except:
            pass

    def _perform_task(self, data: R) -> S:
        return cast(S, data)

    def _send_to_next(self, processed: S):
        while True:
            try:
                self._target_queue.put(processed, timeout=self._timeout)
                break
            except TimeoutError:
                pass
            except Full:
                pass
            except Empty:
                pass
            except Exception as e:
                print("Error sending:", e)

    def run(self):
        while True:
            try:
                data = self._source_queue.get(timeout=self._timeout)
                processed = self._perform_task(data)
                self._send_to_next(processed)
            except Empty:
                pass
            except Exception as e:
                print(f"Error_{e.__class__.__name__}_{e.args}")
                self._source_queue.shutdown()
                self._kill()
            if self._source_queue.shutted and self._source_queue.empty():
                self._kill()
