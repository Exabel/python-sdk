import threading

from exabel.util.logging_thread_pool_executor import LoggingThreadPoolExecutor


class TestLoggingThreadPoolExecutor:
    def test_thread_count_with_multiple_tasks(self):
        """Test that the running thread count is correctly managed."""
        executor = LoggingThreadPoolExecutor(max_workers=2)

        start_semaphore = threading.Semaphore(0)
        start_barrier = threading.Barrier(2 + 1)  # For 2 worker threads + 1 main test thread

        def task():
            start_semaphore.release()  # Signal that the task has started
            start_barrier.wait()  # Wait for all other threads to reach this point
            return "result"

        futures = [executor.submit(task) for _ in range(2)]

        for _ in range(2):
            start_semaphore.acquire()
        assert executor.running_threads == 2

        start_barrier.wait()

        result = [future.result() for future in futures]
        assert executor.running_threads == 0
        assert result == ["result"] * 2
