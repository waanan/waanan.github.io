---
title: "线程的生命周期"
date: 2025-03-15T11:09:41+08:00
---

线程是进程中完全独立的一条执行流。因此，类似于人生的三大终极问题，“我是谁，从哪里来，到哪里去？”。本节来研究下，std::thread是什么，如何创建，以及如何结束。

***
## std::thread

std::thread是C++11中引入的一个类，用于表示一个线程。它提供了一种简单而又贴切的方式来创建和管理线程，使得多线程的编程直观且容易。

要使用std::thread，需要引用头文件\<thread\>。

std::thread的构造函数，接受一个可调用的对象f（函数，lambda，函数对象等），以及该可调用对象需要的参数args。

当std::thread构造函数执行结束，立即启动实际的线程，以args作为参数，调用f。也就是说，在一条全新的执行流中，执行f(args)。

程序从main函数启动时，我们将这条执行流称为主线程。当主线程执行结束时，即使存在任何其它的后台线程，程序也会终止执行。

下面看一个例子：

```C++
#include <iostream>
#include <thread>

void f(int cnt)
{
	for (int i = 0; i < cnt; i++)
	{
		std::cout << "Thread 1 Run\n";
	}
}

class Foo
{
public:
	void bar(int cnt)
	{
		for (int i = 0; i < cnt; ++i)
		{
			std::cout << "Thread 2 Run\n";
		}
	}
};

int main()
{
	std::cout << "Start Two Thread!\n";
	std::thread t1(f, 2);   // 以普通函数启动线程
	Foo foo;
	std::thread t2(&Foo::bar, &foo, 3);  // 以class的成员函数来启动线程，需要额外多传一个对象指针，作为成员函数的this指针
	t1.join();  // 等待线程 t1 执行结束
	t2.join();  // 等待线程 t2 执行结束
	std::cout << "Two Thread Work Done\n";
	return 0;
}
```

在作者的机器上，这有如下的执行结果：

```C++
Start Two Thread!
Thread 1 Run
Thread 1 Run
Thread 2 Run
Thread 2 Run
Thread 2 Run
Two Thread Work Done
```

这里唯一要注意的是，当传递class的成员函数来启动线程时，除了该成员函数本身的参数要传递外，还要传递一个该class对象的指针，来作为这个成员函数的this指针。

当然，也可以不传入任何可调用对象，来创建std::thread，这样的std::thread实际不拥有线程资源，可以简单的将这种对象，想象为类似一个空指针。

```C++
#include <iostream>
#include <thread>

int main()
{
	std::thread t;  // 这里不会启动线程，因此t处于“空”的状态
	return 0;
}
```

***
## 以引用作为传入参数

不论线程启动时，使用的是哪种可调用对象。std::thread都不会收集它的返回值。为什么这样设计？

1. 新启动的线程是完全异步执行，与当前线程或许不会有任何交集，并且可能其生命周期，和整个程序一样长。没有任何必要有一个返回值。
2. C++标准库设计时，以灵活性和通用性为考量。如果需要返回值，那么std::thread对象就需要有一个存储返回值的内存空间。并且这个返回值的类型还是不确定的，这带来了设计上的复杂性。
3. 有大量的机制，可以轻易的在不同线程之间进行数据交互。没有必要为std::thread再额外设计机制。

例如，我们可以传递一个指针，让新启动的线程将结果传递出来：

```C++
#include <iostream>
#include <thread>

void compute(int* res)
{
	if (res != nullptr) {
		*res = 42;
	}
}

int main()
{
	int res = 0;
	std::thread t(compute, &res);   // 传入res，用来获取线程的计算结果
	t.join();   // 等待线程 t 执行结束
	std::cout << "Compute Res is " << res << std::endl;
	return 0;
}
```

这打印：

```C++
Compute Res is 42
```

当然，传入一个指针，还需要额外判断该指针是否有效，你可能会尝试按如下方式传入引用：

```C++
#include <iostream>
#include <thread>

void compute(int& res)
{
	res = 42;
}

int main()
{
	int res = 0;
	std::thread t(compute, res);   // 传入res，用来获取线程的计算结果
	t.join();   // 等待线程 t 执行结束
	std::cout << "Compute Res is " << res << std::endl;
	return 0;
}
```

在vs中，这会产生编译报错：

```C++
error C2672: “invoke”: 未找到匹配的重载函数
```

当然，即使在其它地方可以编译通过，执行的结果也会是：

```C++
Compute Res is 0
```

这是因为，std::thread构造函数在将参数传递给compute时，采用的是值传递。当然修复办法也很简单，采用之前学习过的std::ref即可。

```C++
#include <iostream>
#include <thread>

void compute(int& res)
{
	res = 42;
}

int main()
{
	int res = 0;
	std::thread t(compute, std::ref(res));   // 传入res，用来获取线程的计算结果
	t.join();   // 等待线程 t 执行结束
	std::cout << "Compute Res is " << res << std::endl;
	return 0;
}
```

***
## join

当调用std::join函数的时候，意味着在当前执行流中，等待对应的线程执行结束。

```C++
t.join();  // 在当前线程，等待线程 t 执行结束
```

std::thread实际映射管理了物理线程，因此当有效的std::thread对象析构时，它会判断是否调用过join函数。如果未调用过，则会直接调用std::terminate()终止程序。

考虑以下函数：

```C++
void compute()
{
	// 进行一些计算
}

void foo()
{
	std::thread t(compute);
	// 这里可能有一些复杂的逻辑
	// 因此忘记调用了t.join()
	return;
}
```

如果不这么设计，会发生什么？在foo中，因为各种原因漏了调用t.join()。那么每次调用foo()，都会创建一个线程出来。线程是一种相对比较宝贵的资源，线程有自己独立的调用栈以及一些独占的内存。相信很快程序就会因为奇怪的报错，无法正常执行而退出。

强制这么设计，可以大大避免出问题的可能。

***
## jthread（C++20）

当然，每次手写join()，在复杂的场景下，非常容易出错。因此合理的方式，是利用RAII机制进行包装。C++20引入了std::jthread。

“j”代表，jthread析构时，会自动先调用join。除此之外，它的行为与std::thread一致。

```C++
void compute()
{
	// 进行一些计算
}

void foo()
{
	std::jthread t(compute);
	// 这里可能有一些复杂的逻辑
	// 因此忘记调用了t.join()
	return;
}  // 但是无需担心，当这里t超出作用域进行析构时，会自动先调用t.join()
```

***
## detach

有一些任务，我们想放到后台执行，并且也不关心它们的生命周期。这些后台线程按自己的逻辑进行执行即可。那么，我们必须调用join函数就显的有些奇怪了。

这时候，我们可以调用std::thread的detach()函数。

```C++
#include <iostream>
#include <thread>

void back_task()
{
	// 做一些后台处理的任务
	std::cout << "Back Task \n";
}

int main()
{
	int res = 0;
	std::thread t(back_task);   // 启动后台任务
	t.detach();
	std::cout << "Front Task!\n";
	return 0;
}
```

在主线程中，启动了后台线程来执行back_task。因为back_task的逻辑，与主线程完全无任何关联，主线程也不关心back_task的任何执行情况，因此调用t.detach()，这代表对象t完全不再管理对应的实际线程，所以t析构时，也可以正常析构。

***
## std::thread可移动，不可拷贝

在多线程的程序中，不同线程在并行执行时，可能会有大量的交互，这涉及到非常精妙的状态维护。如果对一个线程进行拷贝，复制出来相同的一条执行流，这条新的执行流从复制的点位开始执行。谁知道它是从哪里开始执行的？它大概率无法与其它线程正常交互，这会带来恐怖的状态管理成本。因此，C++不允许对线程进行复制，所以std::thread设计为不可拷贝。要想启动线程，必须从一个可调用对象，从头开始清爽的执行。

但是，允许对std::thread进行移动，这是合理的。只要可以安全的进行资源转移，就会简化很多代码编写成本。例如，很多场景下，我们需要创建一组线程来执行任务。与其每个线程使用单独的变量，或者搞出来一个指针数组。相对而言，将一组新创建的std::thread，转移到std::vector中进行统一管理，更为简洁明了。

```C++
std::thread t1([] { std::cout << "Thread 1\n"; });
std::thread t2 = std::move(t1); // t1 的线程资源被转移给 t2

t2.join(); // t2 现在是线程的所有者
// t1 不再拥有线程资源，不能调用 join() 或 detach()
```

如上，调用过std::move之后，t1不再拥有线程资源，也不应该调用join() 或 detach()方法。线程资源转到到t2来进行管理。

std::thread的这种资源管理和所有权语义，与std::unique_ptr有一定的相似之处。

***

{{< prevnext prev="/lib/thread/intro/" next="/lib/thread/interact-by-mutex/" >}}
0.0 多线程简介
<--->
0.2 多线程间交互-mutex（施工中）
{{< /prevnext >}}
