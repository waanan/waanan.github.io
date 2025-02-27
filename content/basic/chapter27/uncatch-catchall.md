---
title: "未捕获的异常和捕获所有异常"
date: 2025-02-12T14:07:59+08:00
---

现在，您应该已经对异常的工作方式有了合理的了解。在本课中，我们将介绍几个更有趣的异常情况。

***
## 未捕获的异常

当函数抛出它不处理自己的异常时，它假设调用栈中的某个函数将处理该异常。在下面的示例中，mySqrt()假设有人将处理它抛出的异常——但如果没有人真正处理，会发生什么情况？

这是我们的sqrt程序，移除main()中的try块：

```C++
#include <iostream>
#include <cmath> // for sqrt()

// 独立的平方根函数
double mySqrt(double x)
{
    // 如果输入小于0，那么肯定是异常情况
    if (x < 0.0)
        throw "Can not take sqrt of negative number"; // 抛出类型为 const char* 的异常

    return std::sqrt(x);
}

int main()
{
    std::cout << "Enter a number: ";
    double x;
    std::cin >> x;

    // 这里，不再处理异常
    std::cout << "The sqrt of " << x << " is " << mySqrt(x) << '\n';

    return 0;
}
```

现在，假设用户输入-4，mySqrt(-4)引发异常。函数mySqrt()不处理异常，因此程序会查看调用栈中的某个函数是否会处理该异常。main()也没有用于此异常的处理，因此找不到任何处理代码。

当找不到函数的异常处理程序时，会调用std::terminate（），并终止应用程序。在这种情况下，调用栈可以展开，也可以不展开！如果调用栈未展开，则不会销毁局部变量，在销毁变量时预期的任何清理都不会发生！

当异常未处理时，操作系统通常会通知您发生了未处理的异常错误。它如何做到这一点取决于操作系统，但可能包括打印错误消息、弹出错误对话框或只是崩溃。一些操作系统不如其他操作系统优雅。通常，这是您要避免的事情！

{{< alert success >}}
**警告**

如果未处理异常，则调用栈可能会展开，也可能不会展开。

如果调用栈未展开，则不会销毁局部变量，如果这些变量具有非平凡的析构函数，则可能会导致问题。

{{< /alert >}}

{{< alert success >}}
**旁白**

尽管在这种情况下不展开调用栈似乎很奇怪，但有一个很好的理由不这样做。未处理的异常通常是您希望不惜一切代价避免的。如果调用栈被展开，那么异常的调用栈状态的所有调试信息都将丢失！通过不展开调用栈，我们保留了该信息，从而更容易确定什么引发了未处理的异常，并修复它。

{{< /alert >}}

***
## 捕获所有异常

现在我们发现自己陷入了一个难题：

1. 函数可能会引发任何数据类型（包括用户定义的数据类型）的异常，这意味着要捕获的可能异常类型数量是无限的。
2. 如果未捕获异常，则程序将立即终止（并且调用栈可能不会展开，因此您的程序甚至可能不会在自身正确清理后结束）。
3. 为每个可能的类型添加显式catch处理程序是冗长的！

幸运的是，C++还为我们提供了一种捕获所有类型异常的机制。这被称为捕获所有异常的处理程序（catch all）。它的工作方式与普通的catch块类似，只是它没有使用特定的类型来捕获，而是使用「...」作为要捕获的类型。由于这个原因，catch all处理程序有时也被称为“省略号捕获处理程序”

当用作函数参数时，省略号以前用于将任何类型的参数传递给函数。在catch的上下文中，它们表示任何数据类型的异常。下面是一个简单的例子：

```C++
#include <iostream>

int main()
{
	try
	{
		throw 5; // 抛出异常
	}
	catch (double x)
	{
		std::cout << "We caught an exception of type double: " << x << '\n';
	}
	catch (...) // catch-all 处理
	{
		std::cout << "We caught an exception of an undetermined type\n";
	}
}
```

因为类型int没有特定的异常处理程序，所以catch all处理程序捕获此异常。此示例产生以下结果：

```C++
We caught an exception of an undetermined type
```

catch all处理程序必须放在catch链中的最后一个。这是为了确保为特定数据类型定制的异常处理程序可以捕获异常。

通常，catch all处理程序块为空：

```C++
catch(...) {} // 忽略任何非预期的异常
```

这将捕获任何未预料到的异常，确保在此之前发生调用栈展开，并防止程序终止，但不进行特定的错误处理。

***
## 使用catch all处理程序包装main

catch all处理程序的一个用途是包装main()函数：

```C++
#include <iostream>

struct GameSession
{
    // Game session 数据
};

void runGame(GameSession&)
{
    throw 1;
}

void saveGame(GameSession&)
{
    // 保存用户的游戏信息
}

int main()
{
    GameSession session{};

    try
    {
        runGame(session);
    }
    catch(...)
    {
        std::cerr << "Abnormal termination\n";
    }

    saveGame(session); // 即使发生了异常，也要保存用户游戏信息

    return 0;
}
```

在这种情况下，如果runGame()或它调用的任何函数抛出未处理的异常，则它将被该catch all处理程序捕获。调用栈将以有序的方式展开（确保销毁局部变量）。这也将防止程序立即终止，使我们有机会打印我们选择的错误，并在退出之前保存用户的状态。

{{< alert success >}}
**提示**

若您的程序使用异常，请考虑在main中使用catch all处理程序，以在发生未处理的异常时帮助确保有序的行为。

如果catch all程序捕获到异常，则应该假设程序现在处于某种不确定状态，需要立即执行清理，然后终止。

{{< /alert >}}

***
## 调试未处理的异常

未处理的异常表示发生了意外情况，我们可能希望首先诊断引发未处理异常的原因。许多调试器将（或可以配置为）中断未处理的异常，允许我们在引发未处理异常的点处查看调用栈。然而，如果我们有一个catch-all处理程序，那么所有异常都会被处理，并且（因为调用栈被展开）我们会丢失有用的诊断信息。

因此，在调试构建中，禁用catch all处理程序可能很有用。我们可以通过条件编译指令来实现这一点。

这里有一种方法：

```C++
#include <iostream>

struct GameSession
{
    // Game session 数据
};

void runGame(GameSession&)
{
    throw 1;
}

void saveGame(GameSession&)
{
    // 保存用户的游戏信息
}

class DummyException // 不能被初始化的类
{
    DummyException() = delete;
}; 

int main()
{
    GameSession session {}; 

    try
    {
        runGame(session);
    }
#ifdef NDEBUG // 发布给外部用的版本
    catch(...) // 编译 catch-all 
    {
        std::cerr << "Abnormal termination\n";
    }
#else // debug 版本, 编译一个永远不会走到的catch处理（为了兼容必须有catch关键字的语法）
    catch(DummyException)
    {
    }
#endif

    saveGame(session); // 即使发生了异常，也要保存用户游戏信息

    return 0;
}
```

在语法上，try块需要至少一个关联的catch块。因此，如果catch all处理程序是有条件编译出来的，我们要么需要有条件的编译出try块，要么需要有条件的编译另外一个catch块。后者更干净。

为此，我们创建了类DummyException，该类不能被实例化，因为它有一个已删除的默认构造函数，而没有其他构造函数。当未定义NDEBUG时，我们在catch处理程序中编译捕获DummyException类型的异常。因为我们不能创建DummyException，所以这个catch处理程序永远不会捕获任何东西。因此，任何达到这一点的异常都不会被处理。

***

{{< prevnext prev="/basic/chapter27/exception-func-stack-unwind/" next="/basic/chapter27/exception-and-class/" >}}
27.2 异常、函数和堆栈展开
<--->
27.4 异常、类和继承
{{< /prevnext >}}
