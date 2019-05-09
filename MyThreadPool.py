from BlockPriorityQueue import BlockPriorityQueue
import threading
import time

"""
使用步骤:
    1. 初始化线程池实例
    2. 将要执行的任务初始化为 WorkRequest 实例，若需要处理返回结果，则需要设计处理结果函数 do_res_callback
    3. 通过线程池实例的 submit_request 方法将 WorkRequest 实例提交到线程池
    4. 通过线程池的 get_result 方法得到 WorkRequest 实例相对应的执行结果
"""


# 请求接口类
class WorkRequest:
    """
    __init__()    请求对象实例化
    @:parameter    func    需要被执行的目标函数
    @:parameter    args    列表参数
    @:parameter    kwargs    字典参数
    @:parameter    work_request_id    请求对象的id
    @:parameter    res_callback    负责处理结果的回调函数
    """

    def __init__(self, func=None, args=None, kwargs=None, work_request_id=None, do_res_callback=None):
        if func is None:
            raise Exception("func should not be None")
        else:
            self.func = func

        if work_request_id is None:
            self.work_request_id = hash(id(self))
        else:
            self.work_request_id = hash(work_request_id)

        if args is None:
            self.args = []  # 会获得变量的值而不是变量名
        else:
            self.args = args

        if kwargs is None:
            self.kwargs = {}
        else:
            self.kwargs = kwargs

        self.do_res_callback = do_res_callback

    def __str__(self):
        return 'work_request_id={0} args={1} kwargs={2}'.format(self.work_request_id, self.args, self.kwargs)


# 线程管理器类
class MyThreadPool:
    """
    __init__()    线程池对象实例化
    @:parameter    req_que_size    请求队列的最大容量
    @:parameter    timeout         一个请求的最大等待时间
    @:parameter    worker_num      工作线程数量
    """

    def __init__(self, worker_num=10, req_que_size=100, timeout=3.0):
        self.request_queue = BlockPriorityQueue(maxsize=req_que_size)  # 请求队列
        self.result_dict = {}  # 结果字典
        self.timeout = timeout
        self.workers = []
        self.closed_workers = []
        self.worker_num = worker_num
        self.create_worker(worker_num)

    """
    submit_request()    提交请求给请求队列
    @:parameter    work_request    WorkRequest对象(请求对象)
    @:parameter    priority    请求的优先级，任务忙时优先级越大越先执行，默认为最低级0
    """

    def submit_request(self, work_request, priority=0):
        if not isinstance(work_request, WorkRequest):
            raise TypeError("work_request must be WorkRequest Type")
        self.request_queue.put(item=work_request, priority=priority, timeout=self.timeout)

    """
    create_worker()    创建work_num个工作线程
    """

    def create_worker(self, number: int):
        for i in range(number):
            work = WorkThread(request_queue=self.request_queue, result_dict=self.result_dict, timeout=self.timeout)
            self.workers.append(work)
            work.start()

    """
    get_workers_len()    得到当前未被关闭的工作线程的总个数
    """

    def get_workers_len(self):
        return len(self.workers)

    """
    get_closed_workers_len()    得到当前被关闭的工作线程的总个数
    """

    def get_closed_workers_len(self):
        return len(self.closed_workers)

    """
    close_worker()    关闭number个数的工作线程
    :parameter    number    要关闭的工作线程的个数
    :parameter    block    是否要等待对应工作线程工作完毕后再关闭
    """

    def close_worker(self, number: int, block=False):
        closed_workers = []
        for i in range(number):
            work = self.workers.pop()
            work.close()
            closed_workers.append(work)

        if block:
            for work in closed_workers:
                work.join()
            self.closed_workers.extend(closed_workers)
        else:
            self.closed_workers.extend(closed_workers)

    """
    get_result()    得到对应请求的处理结果
    @:parameter    work_request    工作请求实例
    """

    def get_result(self, work_request: WorkRequest, poll_timeout=None):
        if poll_timeout is None:
            timeout = self.timeout
        else:
            timeout = float(poll_timeout)
        start_time = time.time()
        while True:
            if work_request.work_request_id not in self.result_dict:
                if (time.time() - start_time) >= timeout:
                    print("id为 {} 的请求结果并不在结果字典中".format(work_request.work_request_id))
                    break
                else:
                    continue
            else:
                try:
                    if work_request.work_request_id not in self.result_dict:
                        raise Exception('id为 {} 的请求结果并不在结果字典中'.format(work_request.work_request_id))
                    elif work_request.do_res_callback is not None:
                        res = self.result_dict.pop(work_request.work_request_id)
                        res = work_request.do_res_callback(res)
                        return res
                    else:
                        res = self.result_dict.pop(work_request.work_request_id)
                        return res
                except Exception as e:
                    print("从结果队列中获取请求并调用结果处理函数失败，报错如下: {}".format(e))
                    break

    """
    stop()    停止线程池工作，block=True时保证所有工作线程的工作都已完成
    @:parameter    block    是否等待任务都完成后再关闭
    """

    def stop(self, block=True):
        self.close_worker(number=self.get_workers_len(), block=block)


# 工作线程类
class WorkThread(threading.Thread):
    """
    __init__()    工作线程实例化
    @:parameter    request_queue    请求队列
    @:parameter    request_queue    结果队列
    @:parameter    timeout          队列中可接受的阻塞时长
    @:parameter    **kwargs    传递给threading.Thread的参数字典
    """

    def __init__(self, request_queue: BlockPriorityQueue, result_dict: dict, timeout, **kwargs):
        threading.Thread.__init__(self, **kwargs)
        self.request_queue = request_queue
        self.setDaemon(daemonic=True)
        self.result_dict = result_dict
        self.timeout = timeout
        self.closed = False

    """
    close()     设置该工作线程的closed标志为True
    """

    def close(self):
        self.closed = True

    """
    run()       工作线程主方法，工作线程是一个守护线程，需要从请求队列中获取请求并执行，执行完成后将结果添加到结果队列
    """

    def run(self):
        while True:
            if self.closed:
                break

            try:
                work_request = self.request_queue.get(timeout=self.timeout)
            except Exception as e:
                print("线程{}从请求队列中获取请求失败，报错如下:{}".format(self.getName(), e))
                continue

            try:
                if callable(work_request.func):  # 请求对象的目标函数是否可调用
                    result = work_request.func(*work_request.args, **work_request.kwargs)
                    if work_request.work_request_id not in self.result_dict:
                        self.result_dict[work_request.work_request_id] = result
                else:
                    raise Exception('得到的请求对象中的目标函数不可调用')
            except Exception as e:
                self.result_dict[work_request.work_request_id] = e
                continue
