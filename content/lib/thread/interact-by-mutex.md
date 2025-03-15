---
title: "多线程间交互-mutex（施工中）"
date: 2025-03-15T16:25:41+08:00
---

进程中的所有线程，共享这个进程中的所有资源。这意味着，一个对象可能被所有的线程看见并进行操作。

参考如下的例子：

```C++
#include <iostream>
#include <thread>

int answer = 42;



```


***