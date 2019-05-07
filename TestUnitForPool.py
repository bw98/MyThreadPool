from MyThreadPool import *
import random
import time


# MyThreadPool 测试单元
def do_work(data):
    #time.sleep(random.choice([1, 2, 3, 4, 5]))
    res = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time())) + '    ' + str(data)
    return res


def do_result(res):
    print("处理完结果，得到：" + str(res))


if __name__ == '__main__':
    thread_pool = MyThreadPool(req_que_size=20, timeout=10)
    all_requests = []
    for i in range(40):
        request = WorkRequest(func=do_work, args=[i], do_res_callback=do_result)
        all_requests.append(request)
        thread_pool.submit_request(request)
    print('-' * 30 + '所有请求都已创建并提交' + '-' * 30)

    # 添加新的工作线程
    thread_pool.create_worker(number=3)

    for request in all_requests:
        print(thread_pool.get_result(work_request=request))

    thread_pool.stop(block=True)
