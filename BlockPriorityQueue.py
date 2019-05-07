# encoding=utf-8
import threading
import heapq
import time


class BlockPriorityQueue:
    """
    __init__()    阻塞队列实例化
    @:parameter    maxsize    队列最大元素个数
    """

    def __init__(self, maxsize=20):
        self._queue = []
        self._queue_index = 0
        self._count = 0
        self._maxsize = maxsize
        # three condition constraint one lock
        self._lock = threading.Lock()
        self._not_full = threading.Condition(self._lock)
        self._not_empty = threading.Condition(self._lock)

    """
    put()    push item with priority
    @:parameter  item    element that want to join queue
    @:parameter  priority    element priority in queue, the greater one is faster get out of get()
    @:parameter  block    could set whether block
    @:parameter  time out    could set timeout length, if wait operation period is greater than timeout, then raise Exception
    """

    def put(self, item, priority=0, block=True, timeout=None):
        with self._not_full:
            if not block:
                if self._count >= self._maxsize:
                    raise Exception("the unblocked queue is full and you cannot call put()")
            else:
                if timeout is not None:
                    timeout = float(timeout)
                    if timeout < 0:
                        raise ValueError("parameter timeout should not be negative")
                    else:
                        start_time = time.time()
                        while self._count >= self._maxsize:
                            self._not_full.wait(timeout=timeout)
                        end_time = time.time()
                        if (end_time - start_time) >= timeout:
                            raise Exception("wait operation time is out of expectation")
                else:
                    while self._count >= self._maxsize:
                        self._not_full.wait()

            heapq.heappush(self._queue, (-priority, self._queue_index, item))
            self._queue_index += 1
            self._count += 1
            self._not_empty.notify()
    """
    get()    get the greatest priority item
    @:parameter    block    could set whether block
    @:parameter  timeout    could set timeout length, if wait operation period is greater than timeout, then raise Exception
    """
    def get(self, block=True, timeout=None):
        with self._not_empty:
            if not block:
                if self._count <= 0:
                    raise Exception("the unblocked queue is empty and you can't call get ()")
            else:
                if timeout is not None:
                    timeout = float(timeout)
                    if timeout < 0:
                        raise ValueError("parameter timeout should not be negative")
                    else:
                        start_time = time.time()
                        while self._count <= 0:
                            self._not_empty.wait(timeout=timeout)
                        end_time = time.time()
                        if end_time - start_time >= timeout:
                            raise Exception("wait operation time is out of expectation")
                else:
                    while self._count <= 0:
                        self._not_empty.wait()
            self._count -= 1
            item = heapq.heappop(self._queue)[-1]
            self._not_full.notify()
            return item

    def print_queue(self):
        for item in self._queue:
            print(item)

    def clear_queue(self):
        self._queue.clear()
