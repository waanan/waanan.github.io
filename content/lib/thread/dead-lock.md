---
title: "死锁，以及如何避免"
date: 2025-03-13T16:40:41+08:00
---

当多个线程，循环等待同一个资源的时候，就会发生死锁（dead lock）。

考虑如下示例：

```C++
```

***

{{< prevnext prev="/lib/thread/interact-by-mutex/" next="/lib/thread/interact-by-queue/" >}}
0.2 多线程间交互-mutex（施工中）
<--->
0.4 多线程间交互-消息队列
{{< /prevnext >}}
