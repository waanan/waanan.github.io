---
title: "多线程间交互-mutex（施工中）"
date: 2025-03-15T16:25:41+08:00
---

## 竞态情况（race condition）

进程中的所有线程，共享这个进程中的所有资源。这意味着，一个对象可能被所有的线程看见并进行操作。

参考如下的例子：

```C++
#include <iostream>
#include <thread>

int i = 0;

void t1()
{
    // 线程一执行这个函数
    i++;
}

void t2()
{
    // 线程二执行这个函数
    i++;
}
```

假设线程一执行t1()，线程二执行t2()。线程一与线程二同时执行。当这两个线程都执行结束时，i的值会是多少？结果难道不是显而易见的“2”么。

这在单线程的场景下确实如此，但是在多线程的情况下，事情就会变得复杂起来。

“i++”实际在物理机器上执行时，会拆分为三段：

```C++
从 内存 加载 i 到 寄存器r
寄存器r 的值加一
将 寄存器r 的值 写回 i 对应的内存
```

对于线程t1和t2，可能会有多种执行情况：

```C++
// 情形1
t1：从 内存 加载 i 到 寄存器r1         // 寄存器r1 = 0
t2：从 内存 加载 i 到 寄存器r1         // 寄存器r2 = 0
t1：寄存器r1 的值加一                  // 寄存器r1 = 1
t2：寄存器r2 的值加一                  // 寄存器r2 = 1
t1：将 寄存器r1 的值 写回 i 对应的内存  // i = 1
t2：将 寄存器r2 的值 写回 i 对应的内存  // i = 1
```

又或者是这种执行情况：

```C++
// 情形2
t1：从 内存 加载 i 到 寄存器r1         // 寄存器r1 = 0
t1：寄存器r1 的值加一                  // 寄存器r1 = 1
t1：将 寄存器r1 的值 写回 i 对应的内存  // i = 1
t2：从 内存 加载 i 到 寄存器r1         // 寄存器r2 = 1
t2：寄存器r2 的值加一                  // 寄存器r2 = 2
t2：将 寄存器r2 的值 写回 i 对应的内存  // i = 2
```

或者可能是其它交错的执行情形。但是，当发生大概率执行的结果，不是预期的“2”。

当多线程同时访问同一资源，但又没有合理的进行同步，从而可能导致非预期的执行结果。我们说，这时处于「竞态情况」（race condition）。

***
## 临界区（Critical Section）

为了解决上面提到的问题，多线程对于共享资源操作的代码，必须同一时间，只能被一个线程进行执行。只有这样的特殊操作手段，以及合理的代码逻辑，才能完成多线程间的信息同步。

这块特殊的代码段，被称作「临界区」（Critical Section）。

因为所有的线程，都是在临界区串行执行。因此临界区的范围要尽可能的小，只覆盖必要的代码段，只同步必要的信息。否则，会削弱多线程并行处理的能力，无法发挥多线程的效果。

想象最极端的情况，线程中所有的代码都在临界区。那么实际最终的效果，就是多个线程一个挨着一个串行的执行。其实就等价于单线程来执行了。

此外，由上可知，即使「i++」这样简单的逻辑，在多线程的情况下都是不安全的，更不用说复杂的表达式了。所以对于共享的资源进行操作，一定要放在临界区中进行处理。

***
## 锁（mutex）

锁（mutex）是用来实现临界区的最常用的手段。位于\<mutex\>头文件中。

现在来举一个有味道的例子来进行说明。对于只有一个坑位的厕所，每次只能有一个人来使用。使用的时候，反锁门（lock）。使用完成后解锁（unlock），然后下个人才能进来使用。

如果有多个坑位，那么就是对应多把锁。每个坑位有自己的锁，每个锁保护独立的坑位，不同锁互不影响。

对于上面的例子：

```C++
#include <mutex>

// 锁对应的对象，加锁解锁在这个对象上进行操作
// 不同的锁对象，是互相独立的
std::mutex mtx;
mtx.lock();    // 针对mtx来加锁，临界区的起点
i++;
mtx.unlock();  // 针对mtx来加解锁，临界区的终点
```

实际使用下进行验证：

```C++
#include <iostream>
#include <thread>
#include <mutex>

// 锁对应的对象，加锁解锁在这个对象上进行操作
// 不同的锁对象，是互相独立的
std::mutex mtx;
int shared_data = 0;

void increment() {
    for (int i = 0; i < 1000; ++i) {
        mtx.lock();  // 针对mtx来加锁，临界区的起点
        shared_data++;
        mtx.unlock();  // 针对mtx来加解锁，临界区的终点
    }
}

int main() {
    std::thread t1(increment);
    std::thread t2(increment);

    t1.join();
    t2.join();

    std::cout << "Final value: " << shared_data << std::endl;
    return 0;
}
```

这打印：

```C++
Final value: 2000
```

***
## lock_guard

lock与unlock一定是成对出现的。如果lock了之后，因为各种原因，忘记了unlock，那么相当于一直占有锁。其它线程会一直等待直到锁被释放。

为了简化这种情况的处理。C++提供了RAII机制的包装类std::lock_guard。在lock_guard的构造函数中，会自动调用传入的mutex对象的lock()函数，在析构函数中，会自动调用传入的mutex对象的unlock()函数。

如下所示:

```C++
{
    std::mutex mtx;
    std::lock_guard<std::mutex> lg(mtx);  // 对象lg构造时，自动调用mtx.lock()
    // 这里所有的代码，都处于临界区中
}  // lg超出作用域，进行析构，析构时调用mtx.unlock()
```

同时，上面的例子可以改写为:

```C++
#include <iostream>
#include <thread>
#include <mutex>

// 锁对应的对象，加锁解锁在这个对象上进行操作
// 不同的锁对象，是互相独立的
std::mutex mtx;
int shared_data = 0;

void increment() {
    for (int i = 0; i < 1000; ++i) {
        std::lock_guard<std::mutex> lg(mtx);  // 对象lg构造时，自动调用mtx.lock()
        shared_data++;  // 这里所有的代码，都处于临界区中
    }  // lg超出作用域，进行析构，析构时调用mtx.unlock()
}

int main() {
    std::thread t1(increment);
    std::thread t2(increment);

    t1.join();
    t2.join();

    std::cout << "Final value: " << shared_data << std::endl;
    return 0;
}
```

***

{{< prevnext prev="/lib/thread/thread-life/" next="/lib/thread/dead-lock/" >}}
0.1 线程的生命周期
<--->
0.3 死锁，以及如何避免
{{< /prevnext >}}
