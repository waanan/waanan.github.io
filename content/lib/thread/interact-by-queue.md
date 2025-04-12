---
title: "多线程间交互-消息队列(施工中)"
date: 2025-03-15T16:25:41+08:00
---
 
在更多的场景下，多个线程并不是完全对称的，也就是说，它们并不是完全执行相同的处理逻辑。

与之相反的是，少部分线程负责与外部进行通信，收发任务，然后将任务分配给其余的线程，其余的线程来负责实际的计算任务。

因此需要一个中间的介质，来做消息的传递。

***
## std::queue

一般情况下，我们都是希望先到达的消息先处理（先入先出）。描述这种性质的数据结构叫队列（queue）。在标准库中提供了该功能，位于queue头文件。

这里我们暂时只需要关注四个函数：

1. push 往队列尾部插入一条数据
2. front 查看队列头部的元素
3. pop 移除队列头部的元素
4. empty 判断队列是否为空

下面是一个简单的使用示例：

```C++
#include <iostream>
#include <queue>

int main() {
    std::queue<int> q;
    q.push(1);  // q = 1
    q.push(2);  // q = 1, 2
    q.push(3);  // q = 1, 2, 3
    std::cout << "front: " << q.front() << std::endl;
    q.pop();  // q = 2, 3
    std::cout << "front: " << q.front() << std::endl;
    q.pop();  // q = 3
    q.push(4);  // q = 3, 4
    q.push(5);  // q = 3, 4, 5
    std::cout << "Remain:" << std::endl;
    // 打印并pop剩下的所有元素
    while (!q.empty())
    {
        std::cout << q.front() << std::endl;
        q.pop();
    }
    return 0;
}
```

输出：

```C++
front: 1
front: 2
Remain:
3
4
5
```

这里按顺序插入了1到5到队列的尾部。同时front()与pop()交替进行，查看并删除队列头部的元素。

因为队列是先入先出，所以打印的顺序，与插入的顺序一致。

此外，需要额外注意的是，调用front()与pop()函数之前，一定要确保队列中存在数据。

如下：

```C++
#include <iostream>
#include <queue>

int main() {
    std::queue<int> q;
    q.pop();  // 这里程序会直接崩溃
    return 0;
}
```

执行到pop()函数时，程序会直接崩溃，毕竟谁也无法从“空”中变出任何玩意。如果无法明确保障队列中存在数据，使用empty()或者size()函数进行判断。

***
## 线程安全的队列

如果要实现线程安全的队列，你可能会想。这很简单，包装一个类，然后将上述的四个函数，使用锁保护起来就可以了。

因此可能会写出下面的代码：

```C++
#include <mutex>
#include <queue>

template <typename T>
class ThreadSafeQueue {
public:
    void Push(T v) {
        std::lock_guard<std::mutex> lg(mtx_); // 加锁
        queue.push(v); // 将元素添加到队列中
    }

    T Pop() {
        std::lock_guard<std::mutex> lg(mtx_); // 加锁
        return q_.pop();
    }

private:
    std::mutex mtx_;
    std::queue<T> q_;
}
```

***

{{< prevnext prev="/lib/thread/dead-lock/" next="/lib/thread/interact-by-notify/" >}}
0.3 死锁，以及如何避免
<--->
0.5 多线程间交互-wait与notify
{{< /prevnext >}}
