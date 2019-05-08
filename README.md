# MyThreadPool
## 简介
##### 利用python语言实现一个线程池，能够提供和 concurrent.futures 中提供的线程池类差不多的功能，比如初始化任务请求，初始化工作线程个数，获得特定请求对应的执行结果。
<br></br>
## 基本结构
##### 1、线程池管理器（ThreadPool），用于启动、停用、管理线程池
##### 2、请求（WorkRequest），用于创建请求对象，以供工作线程调度并执行任务
##### 3、工作线程（WorkThread），用于执行目标函数的工作线程
##### 4、请求队列（RequestQueue）,它是线程安全优先级阻塞队列，用于存放和获取请求
##### 5、结果字典（resultDict）,它是字典，用于存储请求执行后返回的结果
<br></br>
## 模型示例图
[![EcAG6K.md.png](https://s2.ax1x.com/2019/05/08/EcAG6K.md.png)](https://imgchr.com/i/EcAG6K)
<br></br>
## 各代码介绍
##### BlockPriorityQueue.py：构建线程安全的优先级阻塞队列
##### TestUnitForBPQueue.py：优先级阻塞队列的测试文件，写了一个基本生产者消费者示例用于测试队列的鲁棒性
##### MyThreadPool.py：构建线程池
##### TestUnitForPool.py：线程池测试文件，写了一个简单的示例用于测试我的线程池，do_work() 是要执行的目标函数，do_result() 是用于处理结果的函数（可以为空）
<br></br>
## 线程池测试结果
![E6XbiF.png](https://s2.ax1x.com/2019/05/08/E6XbiF.png)
<br></br>
