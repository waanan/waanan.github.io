---
title: "异常、函数和堆栈展开"
date: 2025-02-12T14:07:59+08:00
---

在上一课中，我们解释了如何使用throw、try和catch来启用异常处理。在本课中，我们将讨论异常处理如何与函数交互。

***
## 被调函数抛出异常

在上一课中，我们注意到，“try块检测由try块内的语句抛出的任何异常”。在相应的示例中，我们的throw语句被放在try块中，并被关联的catch块捕获，所有这些都在同一函数中。在单个函数中同时抛出和捕获异常的价值有限。

更有趣的是，如果try块中的语句是函数调用，而被调用的函数抛出异常，会发生什么情况。try块是否会检测由从try块内调用的函数引发的异常？

幸运的是，答案是肯定的！

异常处理最有用的属性之一是throw语句不必直接放在try块中。相反，可以从被调函数中的任何位置引发异常，并且调用方（或调用方的调用方，等等…）的try块可以捕获这些异常。当以这种方式捕获异常时，代码的执行流从引发异常的点跳到处理异常的catch块。

{{< alert success >}}
**关键点**

Try块不仅捕获来自Try块中的语句的异常，还捕获来自在Try块内调用的函数的异常。

{{< /alert >}}

这允许我们以更模块化的方式使用异常处理。我们将通过重写上一课中的平方根程序来演示这一点。

```C++
#include <cmath> // for sqrt()
#include <iostream>

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
    double x {};
    std::cin >> x;

    try // try块中的异常，会由catch块进行捕获
    {
        double d = mySqrt(x);
        std::cout << "The sqrt of " << x << " is " << d << '\n';
    }
    catch (const char* exception) // 捕获类型为 const char* 的异常
    {
        std::cerr << "Error: " << exception << std::endl;
    }

    return 0;
}
```

在这个程序中，我们设计了检查异常并计算平方根的代码，并将其放在名为mySqrt()的函数中。然后，我们从try块内部调用了这个mySqrt()函数。让我们验证它是否仍按预期工作：

```C++
Enter a number: -4
Error: Can not take sqrt of negative number
```

是的！当在mySqrt()中引发异常时，mySqrt()中没有处理代码来处理该异常。然而，对mySqrt()的调用（在main()中）在具有关联的匹配异常处理的try catch。因此，执行流从mySqrt()中的throw语句跳到main()中catch块的顶部，然后继续。

上述程序最有趣的部分是，mySqrt()函数可以引发异常，但它本身不处理该异常！这本质上意味着mySqrt()愿意说，“嘿，有个问题！”，但不愿意自己处理问题。本质上，它是将处理异常的责任委托给其调用者（相当于使用返回码，将处理错误的责任传递回函数的调用者）。

此时，您可能想知道为什么将错误传递回调用方是一个好主意。为什么不让mySqrt()处理它自己的错误？问题是，不同的应用程序可能希望以不同的方式处理错误。控制台应用程序可能希望打印文本消息。windows应用程序可能希望弹出错误对话框。在一个应用程序中，出现的问题可能是一个致命错误，而在另一个应用程中，可能不是。通过将错误传出函数，每个应用程序都可以按最适合其上下文的方式处理来自mySqrt()的错误！最终，这将使mySqrt()尽可能保持模块化，并且错误处理可以放在代码中模块化程度较低的部分。


***
## 异常处理和堆栈展开

在这一节中，我们将了解当涉及多个函数时，异常处理实际上是如何工作的。

当抛出异常时，程序首先查看该异常是否可以立即在当前函数内处理（这意味着该异常是在当前函数的try块内抛出的，并且有一个相关联的对应catch块）。如果当前函数可以处理异常，则会这样做。

如果不是，程序接下来检查函数的调用方（调用堆栈上的上一个函数）是否可以处理异常。为了让函数的调用方处理异常，对当前函数的调用必须在try块内，并且必须关联匹配的catch块。如果没有找到匹配，则检查调用者的调用者（调用堆栈上的上两个函数）。类似地，为了调用方的调用方处理异常，对调用方的调用必须在try块内，并且必须关联匹配的catch块。

在调用堆栈上检查每个函数的过程将继续，直到找到处理程序，或者检查了调用堆栈上的所有函数，但找不到处理程序。

如果找到匹配的异常处理程序，则执行流将从引发异常的点跳到匹配的catch块的顶部。这需要根据需要多次展开堆栈（从调用堆栈中移除当前函数），以使处理异常的函数成为调用堆栈上的最下层的一个函数。

如果找不到匹配的异常处理程序，则堆栈可以展开，也可以不展开。我们将在下一课中详细讨论这种情况。

当从调用堆栈中删除当前函数时，所有局部变量都会像往常一样销毁，但不会返回任何值。

{{< alert success >}}
**关键点**

展开堆栈会销毁被展开的函数中的局部变量（需要这样做，因为它可以确保它们的析构函数被执行）。

{{< /alert >}}

***
## 一个堆栈展开示例

为了说明上面的内容，让我们看一个更复杂的例子，使用一个更大的堆栈。尽管这个程序很长，但它非常简单：main()调用A()，A()调用B()，B()调用C()，C()调用D()，D()抛出异常。

```C++
#include <iostream>

void D() // 被 C() 调用
{
    std::cout << "Start D\n";
    std::cout << "D throwing int exception\n";

    throw - 1;

    std::cout << "End D\n"; // 这一行不会执行到
}

void C() // 被 B() 调用
{
    std::cout << "Start C\n";
    D();
    std::cout << "End C\n";
}

void B() // 被 A() 调用
{
    std::cout << "Start B\n";

    try
    {
        C();
    }
    catch (double) // 未捕获: exception 类型不匹配
    {
        std::cerr << "B caught double exception\n";
    }

    try
    {
    }
    catch (int) // 未捕获: try 中未抛出异常
    {
        std::cerr << "B caught int exception\n";
    }

    std::cout << "End B\n";
}

void A() // 被 main() 调用
{
    std::cout << "Start A\n";

    try
    {
        B();
    }
    catch (int) // exception 这里被捕并处理
    {
        std::cerr << "A caught int exception\n";
    }
    catch (double) // 不会被调用，因为前一个catch已经捕获成功
    {
        std::cerr << "A caught double exception\n";
    }

    // 异常处理结束，继续执行这里的代码
    std::cout << "End A\n";
}

int main()
{
    std::cout << "Start main\n";

    try
    {
        A();
    }
    catch (int) // 不会被调用，因为异常被 A 处理了
    {
        std::cerr << "main caught int exception\n";
    }
    std::cout << "End main\n";

    return 0;
}
```

更详细地看一看这个程序，看看您是否可以找出在运行时打印哪些内容，不打印哪些内容。答案如下：

```C++
Start main
Start A
Start B
Start C
Start D
D throwing int exception
A caught int exception
End A
End main
```

让我们来看看在这种情况下会发生什么。所有“Start”语句的打印都很简单，不需要进一步解释。函数D()打印“D throwing int exception”，然后引发int异常。这就是事情开始变得有趣的地方。

由于D()本身不处理异常，因此将检查其调用方（调用堆栈上的函数），以查看其中一个是否可以处理异常。函数C()不处理任何异常，因此在那里找不到匹配项。

函数B()有两个单独的try块。包含对C()的调用的try块具有用于类型double的异常的处理程序，但它与类型int的异常不匹配（并且异常不进行类型转换），因此未找到匹配项。下面的空的try块不抛出异常。

A()也有一个try块，对B()的调用在其中，因此程序会查看是否存在int异常的catch处理程序。有！因此，A()处理异常，并打印“A caught int exception”。

由于现在已经处理了异常，因此控制流在A()中的catch块之后正常继续。这意味着A()打印“End A”，然后正常终止。

控制流返回main()。尽管main()有一个int的异常处理程序，但我们的异常已经由A()处理，因此main()中的catch块不会被执行。main()简单地打印“End main”，然后正常终止。

该程序说明了许多有趣的原则：

首先，如果抛出异常的函数的直接调用方不想处理异常，则它不必处理该异常。在这种情况下，C()不处理D()抛出的异常。它将该职责委托给堆栈的上一个调用方。

其次，如果try块没有用于被抛出的异常类型的对应的catch处理程序，则会发生堆栈展开，就像根本没有try块一样。在这种情况下，B()也没有处理异常，因为它没有正确类型的catch块。

第三，如果函数具有匹配的catch块，但对当前函数的调用没有在关联的try块中发生，则不会使用该catch块。我们在B()中也看到了这一点。

最后，一旦执行匹配的catch块，控制流就照常进行，从最后一个catch块之后的第一条语句开始。这通过A()处理错误，然后继续“End A”，然后返回调用方来演示。当程序返回到main()时，异常已经被抛出并处理——main()完全不知道发生了异常！

正如您所看到的，堆栈展开为我们提供了一些非常有用的行为——如果函数不想处理异常，则不必处理。异常将向堆栈上传播，直到找到愿意处理的人！这允许我们决定调用堆栈中的什么位置是最合适处理错误的位置。

在下一课中，我们将看一看当您不捕获异常时会发生什么，以及防止这种情况发生的方法。

***

{{< prevnext prev="/basic/chapter27/exception-basic/" next="/" >}}
27.1 基本异常处理
<--->
主页
{{< /prevnext >}}
