---
title: "提前退出程序"
date: 2024-01-02T10:33:49+08:00
---

本节讨论的控制流语句是退出程序，这也是本章讨论的最后一类控制流语句。退出，代表程序终止执行。在C++中，这被实现为函数（而不是关键字），因此退出程序需要函数调用。

绕一个简短的弯路，回顾一下当程序正常退出时会发生什么。当main() 函数返回时（到达函数末尾或通过return语句返回），会发生许多事情。

首先，离开main函数，所以所有局部变量和函数参数都会被销毁（通常情况）。

接下来，调用一个名为std::exit()的特殊函数，并将main()函数的返回值作为参数传入。那么什么是std::exit()？

***
## std::exit()函数

exit()是一个导致程序正常终止的函数。正常终止意味着程序以预期的方式退出。请注意，术语正常终止并不意味着程序执行符合预期。例如，假设您正在编写一个程序，希望用户输入要处理的文件名。如果用户键入了无效的文件名，则程序可能会返回非零的状态码来指示故障状态，但它仍然是正常的终止。

exit()执行许多清理函数。首先，销毁具有静态存储期的对象。然后，如果使用了任何文件，则执行一些文件清理动作。最后，用传递给std::exit()的参数用作状态码，将控制返回给操作系统。

***
## 显式调用std::exit()

尽管在函数main()结束时隐式调用std::exit()，但也可以显式调用std::exit。当以这种方式调用std::exit()时，需要引用cstdlib头文件。

下面是显式使用std::exit()的示例:

```C++
#include <cstdlib> // 引入 std::exit()
#include <iostream>

void cleanup()
{
    // 这里来做一些清理工作
    std::cout << "cleanup!\n";
}

int main()
{
    std::cout << 1 << '\n';
    cleanup();

    std::exit(0); // 结束程序执行，并将0返回给操作系统

    // 下面的代码不会执行到
    std::cout << 2 << '\n';

    return 0;
}
```

该程序打印:

```C++
1
cleanup!
```

请注意，std::exit()后续的语句从不会执行到，因为程序已经终止。

在上面的程序中，从函数main()中调用std::exit()，但可以从任何函数中调用std::exit()来终止程序。

显式调用std::exit()，不会清理任何局部变量（当前函数中，以及在调用堆栈上的函数中）。因此，通常最好避免调用std::exit()。

{{< alert success >}}
**警告**

std::exit()函数不清理当前函数以及调用堆栈中的局部变量。

{{< /alert >}}

***
## std::atexit

由于std::exit()立即终止程序，因此您可能希望在终止之前手动进行一些清理。在这种情况下，清理意味着关闭数据库或网络连接、释放分配的任何内存、将信息写入日志文件等…

上面的示例调用了函数cleanup()来处理清理任务。然而，在每次调用exit()之前手动调用清理函数会给我们增加大量的负担。

为了帮助实现这一点，C++提供了std::atexit()函数，它允许您指定一个函数，该函数将在程序终止时通过std::exit()自动调用。

下面是一个示例:

```C++
#include <cstdlib> // 引入 std::exit()
#include <iostream>

void cleanup()
{
    // 这里来做一些清理工作
    std::cout << "cleanup!\n";
}

int main()
{
    // 注册 cleanup()，这样当调用到std::exit()时，cleanup函数会被自动调用
    std::atexit(cleanup); // 注: 这里是cleanup，而不是cleanup()，因为这里需要的是一个函数，而不是函数调用
    std::cout << 1 << '\n'

    std::exit(0); // 结束程序执行，并将0返回给操作系统

    // 下面的代码不会执行到
    std::cout << 2 << '\n';

    return 0;
}
```

该程序的输出与前面的示例相同:

```C++
1
cleanup!
```

为什么要这么做？这允许在一个地方（可能在main中）指定清理函数，然后不必担心在调用std::exit()之前，需要记住显式调用清理函数。

这里关于std::atexit()和清理函数的几点注意事项:首先，由于在main()终止时隐式调用std::exit()，因此如果程序以这种方式退出，也会调用std::atexit()注册的任何函数。其次，被注册的函数必须没有参数，并且没有返回值。最后，如果需要，可以使用std::atexit()注册多个清理函数，它们将按注册的相反顺序调用（最后注册的函数将首先调用）。

{{< alert success >}}
**对于高级读者**

在多线程程序中，调用std::exit()可能会导致程序崩溃（因为调用std::exit()的线程将清理可能仍然被其他线程访问的静态对象）。由于这个原因，C++引入了另一对函数，它们的工作方式类似于std::exit()和std::atexit()，称为std::quick_exit()和std:∶at_quick_exit()。std::quick_exit()会终止程序，但不会清理静态对象，并且不一定执行其他类型的清理。对于以std::quick_exit()终止的程序，std::at_quick_exit()扮演与std:∶atexit()相同的角色。

{{< /alert >}}

***
## std::abort和std::terminate

C++包含另外两个与退出程序相关的函数。

std::abort()导致程序异常终止。异常终止意味着程序出现某种异常运行时错误，程序无法继续运行。例如，尝试除以0将导致异常终止。std::abort()不执行任何清理。

```C++
#include <cstdlib> // 引入 std::abort()
#include <iostream>

int main()
{
    std::cout << 1 << '\n';
    std::abort();

    // 下面的代码不会执行到
    std::cout << 2 << '\n';

    return 0;
}
```

在本章后面的部分中，我们将看到隐式调用std::abort的情况（9.6--Assert和static_Assert）。

std::terminate()函数通常与异常一起使用（我们将在后面的一章中介绍异常）。尽管可以显式调用std::terminate，但在处理异常时（以及在其他一些与异常相关的情况下），它经常被隐式调用。默认情况下，std::terminate()会调用std::abort()。

***
## 什么时候需要手动退出程序？

简短的回答是“几乎从不”。销毁局部对象是C++的一个重要部分（特别是当使用class时），并且上面提到的函数都不能清理局部变量。

{{< alert success >}}
**最佳实践**

只有在没有安全的方法从main函数正常返回时才手动退出程序。

{{< /alert >}}

{{< alert success >}}
**提示**

尽管应该尽量减少手动的退出程序，但程序可以通过许多其他方式意外关闭。例如:

1. 应用程序可能由于错误而崩溃（在这种情况下，操作系统将关闭它）。
2. 用户可能会以各种方式终止应用程序。
3. 用户可能会关闭其计算机的电源。
4. 太阳可能会变成超新星，并在一个巨大的火球中吞噬地球。


一个设计良好的程序应该能够在任何时候被关闭，并且影响很小。

一个常见例子，现代游戏通常定期自动保存游戏状态和用户设置，以便如果游戏意外关闭而未保存，则用户可以稍后继续（使用先前的自动保存的设置），而不会损失太多进度。

{{< /alert >}}

***