from BlockPriorityQueue import *


# BlockPriorityQueue 测试单元
def produce(q: BlockPriorityQueue):
    for i in range(100):
        q.put(item=int(i), priority=int(i), timeout=3)
        print('放入{}'.format(int(i)))


def consume(q: BlockPriorityQueue):
    for i in range(100):
        item = q.get(timeout=3)
        print('拿出{}'.format(item))


if __name__ == '__main__':
    q = BlockPriorityQueue(maxsize=10)
    print('运行开始时时间为 {}'.format(time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))))
    f1 = threading.Thread(target=produce, args=(q,))
    f2 = threading.Thread(target=produce, args=(q,))
    f3 = threading.Thread(target=consume, args=(q,))
    f4 = threading.Thread(target=consume, args=(q,))
    f1.start()
    f2.start()
    f3.start()
    f4.start()
    f1.join()
    f2.join()
    f3.join()
    f4.join()
    print('运行结束时时间为 {}'.format(time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))))
