---
title: "死锁，以及如何避免"
date: 2025-03-13T16:40:41+08:00
---

先用一个简单的例子来感受下死锁（dead lock）。

假设有一个独木桥，一次只能通过一个人。如果两个人从两边同时上桥，都要到对岸去。如果他们两谁也不让着谁，那么他们两可以僵持到天荒地老。这种情况，就称为死锁。

产生死锁，有四个必要条件：

1. 互斥条件。这是死锁发生的前提，在多线程的场景下，一个资源，同一时间只能被一个线程占用。
2. 请求与保持。当线程占有一种资源后，又去请求其它的资源，但是其它的资源被别的线程占用。
3. 不可剥夺。线程在未完成既定的工作前，不会释放当前已经占有的资源，也不允许别的线程强行剥夺当前线程占有的资源。
4. 循环等待。线程间存在循环等待的情况。例如线程A等待B释放持有的资源，B等待C释放持有的资源，C又等待A释放持有的资源。这样互相等待，系统无法正常推进处理进度。

考虑如下示例：

```C++
#include <iostream>
#include <thread>
#include <mutex>

std::mutex mtx1;
std::mutex mtx2;

void thread1() {
    std::lock_guard<std::mutex> lg1(mtx1);  // 线程1先获取mtx1
    std::cout << "Thread 1 Get mtx1" << std::endl;

    // 给线程二足够的时间去获取mtx2
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));

    std::lock_guard<std::mutex> lg2(mtx2);  // 线程1再获取mtx2
    std::cout << "Thread 1 Get mtx2" << std::endl;

    // 线程一执行结束
    std::cout << "Thread 1 Finish" << std::endl;
}

void thread2() {
    std::lock_guard<std::mutex> lg1(mtx2);  // 线程2先获取mtx2
    std::cout << "Thread 2 Get mtx2" << std::endl;
    
    // 给线程一足够的时间去获取mtx1
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));

    std::lock_guard<std::mutex> lg2(mtx1);  // 线程二再获取mtx1
    std::cout << "Thread 2 Get mtx1" << std::endl;

    // 线程一执行结束
    std::cout << "Thread 2 Finish" << std::endl;
}

int main() {
    std::thread t1(thread1);
    std::thread t2(thread2);

    t1.join();
    t2.join();

    return 0;
}
```

这打印：

```C++
Thread 1 Get mtx1
Thread 2 Get mtx2

```

然后程序就一直无法结束运行。

让我们看看发生了什么。

程序启动后，线程t1和t2同时开始执行。然后t1获取了mtx1，t2获取了mtx2。然后t1和t2分别sleep了1秒。在这之后，t1尝试获取mtx2，t2尝试获取mtx1。显然无法成功，t1和t2会一直互相等待。main函数则一直在t1.join()的地方，等待t1执行完成。所以main函数也处于等待状态。整个程序中的三个线程都无法推进执行流。

***
## 按固定顺序为资源加锁

避免死锁，最简单的情况，就是按固定顺序为资源加锁。

可以按照顺序为资源编号，例如r1，r2，r3等等。获取资源时，从编号小的开始获取。例如A需要获取 r1 -> r2 -> r3。B需要获取 r2 -> r3。如果A获取到了r3，那么在此之前A一定获取了r2。那么B一定不会和A互相等待与抢占。

这里将上面的例子进行修改，t1和t2，都mtx1 -> mtx2的顺序进行资源获取:

```C++
#include <iostream>
#include <thread>
#include <mutex>

std::mutex mtx1;
std::mutex mtx2;

void thread1() {
    std::lock_guard<std::mutex> lg1(mtx1);  // 线程1先获取mtx1
    std::cout << "Thread 1 Get mtx1" << std::endl;

    // 线程一做一些逻辑
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));

    std::lock_guard<std::mutex> lg2(mtx2);  // 线程1再获取mtx2
    std::cout << "Thread 1 Get mtx2" << std::endl;

    // 线程一执行结束
    std::cout << "Thread 1 Finish" << std::endl;
}

void thread2() {
    std::lock_guard<std::mutex> lg1(mtx1);  // 线程2先获取mtx1
    std::cout << "Thread 2 Get mtx1" << std::endl;
    
    // 线程二做一些逻辑
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));

    std::lock_guard<std::mutex> lg2(mtx2);  // 线程二再获取mtx2
    std::cout << "Thread 2 Get mtx2" << std::endl;

    // 线程二执行结束
    std::cout << "Thread 2 Finish" << std::endl;
}

int main() {
    std::thread t1(thread1);
    std::thread t2(thread2);

    t1.join();
    t2.join();

    return 0;
}
```

这打印:

```C++
Thread 1 Get mtx1
Thread 1 Get mtx2
Thread 1 Finish
Thread 2 Get mtx1
Thread 2 Get mtx2
Thread 2 Finish
```

程序正常执行结束。

***

{{< prevnext prev="/lib/thread/interact-by-mutex/" next="/lib/thread/interact-by-queue/" >}}
0.2 多线程间交互-mutex
<--->
0.4 多线程间交互-消息队列(施工中)
{{< /prevnext >}}
