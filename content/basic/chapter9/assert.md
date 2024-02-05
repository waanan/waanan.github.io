---
title: "断言"
date: 2024-01-17T13:13:14+08:00
---

在接受参数的函数中，调用方可以传入语法上有效但语义上无意义的参数。例如，在上一课中的示例函数:

```C++
void printDivision(int x, int y)
{
    if (y != 0)
        std::cout << static_cast<double>(x) / y;
    else
        std::cerr << "Error: Could not divide by zero\n";
}
```

该函数执行显式检查，以查看y是否为0，因为除以零是语义错误，并且如果执行，将导致程序崩溃。

在上一课中，我们讨论了两种处理此类问题的方法，分为停止程序或跳过有问题的语句。

然而，这两种选择都有问题。

如果程序由于错误而跳过语句，则它本质上是在默默地失败。特别是当我们编写和调试程序时，静默故障是不好的，因为它们掩盖了真实的问题。即使我们打印错误消息，该错误消息也可能会在其他程序输出中丢失。并且在哪里生成错误消息，或者触发错误消息的条件是如何发生的，这可能是不明显的。一些函数可能被调用几十次或几百次，如果这些调用里只有一个产生了问题，则很难知道是哪一个。

如果程序终止（通过std::exit），那么我们将丢失调用堆栈和任何可能帮助隔离问题的调试信息。对于这种情况，std::abort是更好的选择，因为通常开发人员可以选择在程序中止的点开始调试。

***
## 前置条件、不变量和后置条件

在编程中，前置条件是在执行某些代码段（通常是函数体）之前必须为true的条件。在上例中，检查y != 0，是确保在除以y之前具有非零值的前提条件。

函数的前提条件最好放在函数的顶部，如果不满足前提条件，则使用提前返回来返回调用方。例如:

```C++
void printDivision(int x, int y)
{
    if (y == 0) // 校验前置条件 
    {
        std::cerr << "Error: Could not divide by zero\n";
        return; // 返回给调用方
    }

    // 这里一定 y != 0
    std::cout << static_cast<double>(x) / y;
}
```

不变量是在执行代码的某些部分时必须为true的条件。这通常用于循环，其中循环体仅在不变量为true时执行。

类似地，后置条件是在执行代码的某些部分后必须为true的东西。上面示例的函数没有任何后置条件。

***
## 断言

使用条件语句检测无效参数（或验证某种其他类型的假设），以及打印错误消息并终止程序，是检测问题的常见方法，C++为此提供了一种快捷方法。

断言是一个表达式。如果表达式的计算结果为true，则断言语句不执行任何操作。如果条件表达式的计算结果为false，则显示错误消息并终止程序（通过std::abort）。该错误消息通常包含表达式的文本，以及代码文件的名称和断言的行号。这不仅使得可以很容易地知道问题是什么，还可以知道问题发生在代码中的什么地方。这可以极大地帮助调试工作。

在C++中，运行时断言是通过断言预处理器宏实现的，该宏位于<cassert>头中。

```C++
#include <cassert> // for assert()
#include <cmath> // for std::sqrt
#include <iostream>

double calculateTimeUntilObjectHitsGround(double initialHeight, double gravity)
{
  assert(gravity > 0.0); // 重力一定为正
 
  if (initialHeight <= 0.0)
  {
    // 东西已经落在地上了
    return 0.0;
  }
 
  return std::sqrt((2.0 * initialHeight) / gravity);
}

int main()
{
  std::cout << "Took " << calculateTimeUntilObjectHitsGround(100.0, -9.8) << " second(s)\n";

  return 0;
}
```

当程序调用 calculateTimeUntilObjectHitsGround(100.0, -9.8) 时，assert(gravity > 0.0) 的计算结果将为false，这将触发断言。将打印类似于以下内容的消息:

```C++
dropsimulator: src/main.cpp:6: double calculateTimeUntilObjectHitsGround(double, double): Assertion 'gravity > 0.0' failed.
```

实际消息因使用的编译器而异。

尽管断言最常用于验证函数参数，但它们可以用于您希望验证某些内容是否正确的任何地方。

尽管我们以前告诉过您不要使用预处理器宏，但断言是为数不多的被认为可以使用的预处理器宏之一。我们鼓励您在代码中自由地使用断言语句。

{{< alert success >}}
**关键点**

当断言的计算结果为false时，程序将立即停止。这使您有机会使用调试工具来检查程序的状态，并确定断言失败的原因。然后您可以找到并解决问题。

如果发生了错误，但没有设置断言检查，这样的错误可能会导致您的程序稍后发生故障。在这种情况下，很难确定哪里出了问题，或者问题的根本原因是什么。

{{< /alert >}}

***
## 使断言语句更具描述性

有时断言表达式不是非常描述性的。考虑以下语句:

```C++
assert(found);
```

如果触发此断言，则断言将显示:

```C++
Assertion failed: found, file C:\\VCProjects\\Test.cpp, line 34
```

这意味着什么？明显found的值是false（因为断言被触发），但为什么？您必须查看代码才能确定这一点。

幸运的是，有一个小技巧可以使断言语句更具描述性。只需添加由逻辑AND连接的字符串文本:

```C++
assert(found && "Car could not be found in database");
```

这样做的原因: 字符串文本总是计算为布尔true。因此，如果found为假，则false&&true为假。如果found为true，则true&&true为true。因此，对字符串文本进行逻辑“与”运算不会影响断言的计算。

当断言触发时，字符串文本将包含在断言消息中:

```C++
Assertion failed: found && "Car could not be found in database", file C:\\VCProjects\\Test.cpp, line 34
```

这为您提供了一些关于出错原因的额外背景。

***
## 断言与错误处理

断言和错误处理非常相似，因此它们的目的可能会混淆，因此让我们澄清一下:

断言的目标是记录不应该发生的事情来捕获编程错误。如果那件事真的发生了，那么程序员在某处犯了错误，并且该错误可以被识别和修复。断言不允许从错误中恢复（毕竟，如果某些事情永远不会发生，则不需要从中恢复），并且程序不会产生友好的错误消息。

另一方面，错误处理旨在优雅地处理可能发生问题的情况（尽管很少）。这些可以恢复，也可以不恢复，但应该始终假设程序的用户可能会遇到它们。

断言有时也用于记录未实现功能的情况，因为编写代码时还不需要实现它们:

```C++
assert(moved && "Need to handle case where student was just moved to another classroom");
```

这样，如果代码的未来用户确实遇到需要这种情况的情况，代码将失败，并显示有用的错误消息，然后程序员可以确定如何实现这种情况。

{{< alert success >}}
**最佳实践**

使用断言来记录逻辑上不可能的情况。

{{< /alert >}}

***
## NDEBUG

每次检查断言条件时，断言宏都会产生较小的性能开销。此外，（理想情况下）在生产代码中永远不会遇到断言（因为您的代码应该已经过彻底测试）。因此，许多开发人员更喜欢仅在调试构建时使用断言。C++提供了一种在生产代码中关闭断言的方法。如果定义了宏NDEBUG，则断言宏将被禁用。

一些IDE默认将NDEBUG设置为发布配置的项目设置的一部分。例如，在VisualStudio中，在项目配置默认设置以下预处理器定义: WIN32;NDEBUG;_CONSOLE 。如果您正在使用VisualStudio，并且希望在发布版本中触发断言，则需要从该设置中删除NDEBUG。

如果您使用的IDE或构建系统没有在发布配置中自动定义NDEBUG，则需要将其手动添加到项目或编译设置中。

***
## 一些断言限制和警告

断言有一些缺陷和限制。首先，断言语句本身可能不正确地编写。如果发生这种情况，断言要么报告不存在的错误，要么不报告存在的错误。

其次，您的断言应该没有副作用——也就是说，程序应该在有断言和没有断言的情况下运行相同。否则，您在调试配置中测试的内容将与发布配置中的内容不同。

还要注意，abort()函数立即终止程序，没有机会进行任何进一步的清理（例如，关闭文件或数据库）。因此，断言应该仅在程序意外终止，且不太可能发生损坏的情况下使用。

***
## static_assert

C++还有另一种类型的断言，称为static_assert。static_assert是在编译时而不是在运行时检查的断言，失败的static_assert会导致编译错误。与在<cassert>头文件中声明的assert不同，static_assert是一个关键字，因此不需要包含任何头文件来使用它。

static_assert采用以下形式:

```C++
static_assert(条件表达式, 诊断信息)
```

如果条件不为真，则打印诊断消息。下面是使用static_assert确保类型具有特定大小的示例:

```C++
static_assert(sizeof(long) == 8, "long must be 8 bytes");
static_assert(sizeof(int) >= 4, "int must be at least 4 bytes");

int main()
{
	return 0;
} 
```

在作者的机器上，编译时，编译器错误:

```C++
1>c:\consoleapplication1\main.cpp(19): error C2338: long must be 8 bytes
```

关于static_assert的一些有用点:

1. 由于static_assert在编译期计算，因此条件表达式必须是常量表达式。
2. static_assert可以放在代码文件中的任何位置（甚至在全局命名空间中）。
3. 在发布版本中不编译static_assert。


在C++17之前，必须将诊断消息作为第二个参数提供。在C++17及之后，提供诊断消息是可选的。

***

{{< prevnext prev="/basic/chapter9/cin-error-handle/" next="/basic/chapter9/summary/" >}}
9.4 std::cin和处理无效输入
<--->
9.6 第9章总结
{{< /prevnext >}}
