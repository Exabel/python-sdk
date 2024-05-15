import logging
import threading
from concurrent.futures import Future, ThreadPoolExecutor
from typing import Any, Callable

logger = logging.getLogger(__name__)


class LoggingThreadPoolExecutor(ThreadPoolExecutor):
    """
    A thread pool executor logs the number of active threads
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.running_threads = 0
        self.lock = threading.Lock()
        super().__init__(*args, **kwargs)

    def active_threads_counter(self, func: Callable) -> Callable:
        """Decorator to count the number of active threads."""

        def wrapped(*args, **kwargs):  # type: ignore
            with self.lock:
                self.running_threads += 1
                logger.debug("Thread started. Active threads: %d", self.running_threads)
            try:
                result = func(*args, **kwargs)
            finally:
                with self.lock:
                    self.running_threads -= 1
                logger.debug("Thread finished. Active threads: %d", self.running_threads)

            return result

        return wrapped

    def submit(  # type: ignore[override]  # pylint: disable=arguments-differ
        self, function: Callable[..., Any], *args: Any, **kwargs: Any
    ) -> Future:
        return super().submit(self.active_threads_counter(function), *args, **kwargs)
