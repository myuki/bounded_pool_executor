import multiprocessing
import concurrent.futures
import threading

name = 'bounded_pool_executor'


class _BoundedPoolExecutor:

    semaphore = None

    def acquire(self):
        self.semaphore.acquire()

    def release(self, fn):
        self.semaphore.release()

    def submit(self, fn, *args, **kwargs):
        self.acquire()
        future = super().submit(fn, *args, **kwargs)
        future.add_done_callback(self.release)

        return future


class BoundedProcessPoolExecutor(_BoundedPoolExecutor, concurrent.futures.ProcessPoolExecutor):

    def __init__(self, max_workers=None, cache_size=0, **kwargs):
        super().__init__(max_workers, **kwargs)
        self.semaphore = multiprocessing.BoundedSemaphore(self._max_workers + cache_size)


class BoundedThreadPoolExecutor(_BoundedPoolExecutor, concurrent.futures.ThreadPoolExecutor):

    def __init__(self, max_workers=None, cache_size=0, **kwargs):
        super().__init__(max_workers, **kwargs)
        self.semaphore = threading.BoundedSemaphore(self._max_workers + cache_size)

