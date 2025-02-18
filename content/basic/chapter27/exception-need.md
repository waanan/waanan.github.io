---
title: "为什么需要异常机制"
date: 2025-02-12T14:07:59+08:00
---

在很多实际项目中，禁止使用异常机制。如果您参与的项目未使用异常机制，可以跳过本章的学习。

关于错误处理，我们讨论了使用assert()、std::cerr和exit()。然而，我们推迟了要讨论的一个主题：异常（exception）处理。

***
## 函数返回码的不足

在编写可重用代码时，错误处理是必要的。处理潜在错误的最常见方法之一是通过返回码。例如：

```C++
#include <string_view>

int findFirstChar(std::string_view string, char ch)
{
    // 遍历 string 中每一个字符
    for (std::size_t index{ 0 }; index < string.length(); ++index)
        // 如果string中的字符匹配 ch, 返回对应的 index
        if (string[index] == ch)
            return index;

    // 如果没找到，返回 -1
    return -1;
}
```

此函数返回字符串中与ch匹配的第一个字符的位置。如果找不到匹配的字符，则函数返回-1，作为找不到字符的指示。

这种方法的主要优点是它非常简单。然而，使用返回码有许多缺点，当在稍微复杂的场景下使用时，这些缺点会很快变得明显：

首先，返回值可能是神秘的——如果函数返回-1，它是试图指示错误，还是这实际上是一个有效的返回值？如果不深入阅读函数或参考文档，通常很难判断。

其次，函数只能返回一个值，因此当您需要同时返回函数结果和可能的错误码时会发生什么？考虑以下函数：

```C++
double divide(int x, int y)
{
    return static_cast<double>(x)/y;
}
```

该函数迫切需要一些错误处理，因为如果用户为参数y传入0，它将崩溃。然而，它还需要返回x/y的结果。它如何既做又做？最常见的答案是，结果或错误处理必须作为引用参数传回，这使得代码难看而且不太方便使用。例如：

```C++
#include <iostream>

double divide(int x, int y, bool& outSuccess)
{
    if (y == 0)
    {
        outSuccess = false;
        return 0.0;
    }

    outSuccess = true;
    return static_cast<double>(x)/y;
}

int main()
{
    bool success {}; // 必须传递一个 bool 来看是否计算成功
    double result { divide(5, 3, success) };

    if (!success) // 使用结果前必须检查下
        std::cerr << "An error occurred" << std::endl;
    else
        std::cout << "The answer is " << result << '\n';
}
```

第三，在许多事情可能出错的代码序列中，必须不断检查错误代码。考虑以下代码片段，该代码片段涉及解析文本文件中应该存在的值：

```C++
    std::ifstream setupIni { "setup.ini" }; // 打开 setup.ini
    // 如果文件无法打开 (例如， 可能文件不存在) 返回一个错误码
    if (!setupIni)
        return ERROR_OPENING_FILE;

    // 现在，从文件中读取一些值
    if (!readIntegerFromFile(setupIni, m_firstParameter)) // 尝试读一个 int
        return ERROR_READING_VALUE; // 如果读失败，返回一个错误码

    if (!readDoubleFromFile(setupIni, m_secondParameter)) // 尝试读一个 double
        return ERROR_READING_VALUE;

    if (!readFloatFromFile(setupIni, m_thirdParameter)) // 尝试读一个 float
        return ERROR_READING_VALUE;
```

我们还没有介绍文件访问，因此如果您不理解上面的工作原理，请不要担心——只需注意，每个调用都需要进行错误检查并返回给调用者。现在想象一下，如果有20个不同类型的参数，您实际上是在检查错误并返回20次ERROR_READING_VALUE！所有这些错误检查和返回值，使得确定函数试图做什么变得更加困难。

第四，返回码不能与构造函数很好地混合。如果您正在创建一个对象，而构造函数中的某些内容发生灾难性错误，会发生什么情况？构造函数没有返回类型来传回状态，并且通过引用参数传回信号是混乱的，必须显式检查。此外，即使发生了错误，对象仍将被创建，然后必须处理。

最后，当错误代码被返回给调用者时，调用者可能并不总是能够处理该错误。如果调用方不想处理错误，它要么必须忽略它（在这种情况下，它将永远丢失），要么将错误向上返回到调用它的函数。这可能会很混乱，并导致上面提到的许多相同的问题。

总之，返回码的主要问题是错误处理代码最终与正常控制流错综复杂地链接在一起。这反过来又限制了代码的布局，以及如何合理地处理错误。

***
## 异常机制

异常处理提供了一种机制，可以将错误或其他异常情况的处理与代码的正常控制流解耦。这允许更自由地处理错误，减轻了返回码造成的大多数混乱。

在下一课中，我们将了解异常在C++中的工作方式。

***

{{< prevnext prev="/basic/chapter26/summary/" next="/basic/chapter27/exception-basic/" >}}
26.6 第26章总结
<--->
27.1 基本异常处理
{{< /prevnext >}}
