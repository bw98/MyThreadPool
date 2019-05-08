from MyThreadPool import *
import random
import time


# MyThreadPool 测试单元
def do_work(data):
    time.sleep(random.choice([1, 2, 3, 4, 5]))
    res = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time())) + '    ' + str(data)
    return res


def do_result(res):
    res = res + '     蔡徐坤打篮球'
    return res


if __name__ == '__main__':
    thread_pool = MyThreadPool(req_que_size=5, worker_num=3, timeout=10)  # 初始化线程池实例
    all_requests = []
    print('-' * 30 + '开始创建请求' + '-' * 30)
    for i in range(10):
        request = WorkRequest(func=do_work, args=[i], do_res_callback=do_result)  # 初始化请求
        print('创建id为{}的请求'.format(request.work_request_id))
        all_requests.append(request)
        thread_pool.submit_request(request)
    print('-' * 30 + '所有请求都已创建并提交' + '-' * 30)

    thread_pool.create_worker(number=1)  # 添加新的工作线程

    for request in all_requests:
        print('id为{}的请求得到的结果为：{}'.format(request.work_request_id, thread_pool.get_result(work_request=request)))

    thread_pool.stop(block=False)
