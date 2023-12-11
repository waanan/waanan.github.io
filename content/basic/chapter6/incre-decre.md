---
title: "自增/自减运算符和副作用"
date: 2023-12-07T13:09:17+08:00
---

***
## 自增和自减变量

变量的自增（加1）和自减（减1）都很常见，因此它们都有自己的运算符。

| 运算符 |  符号  |  使用形式 |  结果 |
|  ----  | ----  | ----  | ----  |
| 前缀自增 | ++ | ++x | x 加一，返回x |
| 前缀自减 | -- | --x | x 减一，返回x |
| 后缀自增 | ++ | x++ | 拷贝x，x加一，返回拷贝的值 |
| 后缀自减 | -- | x-- | 拷贝x，x减一，返回拷贝的值 |

请注意，每个运算符都有两个版本——前缀版本（运算符位于操作数之前）和后缀版本（运算符在操作数之后）。

***
## 前缀自增和自减

前缀增量/减量运算符非常简单。首先，操作数自增或自减，然后表达式计算为操作数的值。例如：

```C++
#include <iostream>

int main()
{
    int x { 5 };
    int y { ++x }; // x 增加到 6, 表达式的结果取x的值6,  6 被赋值给 y

    std::cout << x << ' ' << y << '\n';
    return 0;
}
```

这将打印：

```C++
6 6
```

***
## 后缀自增和自减

后缀自增/自减操作符更复杂。首先，复制操作数。然后自增或自减操作数（而不是副本）。最后，返回副本。例如：

```C++
#include <iostream>

int main()
{
    int x { 5 };
    int y { x++ }; // x 加到 6, x的原始拷贝值为 5, 5 被赋值给 y

    std::cout << x << ' ' << y << '\n';
    return 0;
}
```

这将打印：

```C++
6 5
```

让我们更详细地解释第6行是如何工作的。首先，创建x的临时副本，该副本从与x（5）相同的值开始。然后，x从5增加到6。然后返回x的副本（仍然具有值5），并将其分配给y。然后丢弃临时副本。

因此，y以值5结束，x以值6结束。

请注意，后缀版本需要更多的步骤，因此性能可能不如前缀版本。

***
## 更多示例

下面是另一个显示前缀和后缀版本之间差异的示例：

```C++
#include <iostream>

int main()
{
    int x { 5 };
    int y { 5 };
    std::cout << x << ' ' << y << '\n';
    std::cout << ++x << ' ' << --y << '\n'; // 前缀
    std::cout << x << ' ' << y << '\n';
    std::cout << x++ << ' ' << y-- << '\n'; // 后缀
    std::cout << x << ' ' << y << '\n';

    return 0;
}
```

这将产生输出：

```C++
5 5
6 4
6 4
6 4
7 3
```

在第8行，我们执行前缀自增和自减。在这一行中，x和y在其值发送到std::cout之前自增/自减，因此我们看到它们的更新值。

在第10行，我们进行后缀自增和自减。在这一行中，x和y的副本是发送到std::cout的内容，因此我们看不到这里反映的增量和减量。这些更改直到下一行才会显示。

***
## 何时使用前缀vs后缀

在许多情况下，前缀和后缀操作符产生相同的行为：

```C++
int main()
{
    int x { 0 };
    ++x; // x加一变成1
    x++; // x加一变成2

    return 0;
}
```

在编写可以同时使用前缀或后缀版本的情况下，最好使用前缀版本，因为它们通常更具性能，并且不太可能引起意外。

***
## 副作用

如果函数或表达式除了产生返回值之外还有一些可观察的效果，则称其具有副作用。

副作用的常见示例包括更改对象的值、执行输入或输出或更新图形用户界面（例如，启用或禁用按钮）。

大多数情况下，副作用是有用的：

```C++
x = 5; // 赋值操作的副作用是更改 x 的值
++x; // operator++ 的副作用是自增x的值
std::cout << x; // operator<< 的副作用是打印x
```

上例中的赋值运算符具有更改x值的副作用，operator++类似。operator<< 具有修改控制台状态的副作用，因为现在可以看到打印到控制台的x的值。

***
## 副作用与求值顺序问题

因为求值顺序问题，副作用可能产生未定义的行为。例如：

```C++
#include <iostream>

int add(int x, int y)
{
    return x + y;
}

int main()
{
    int x { 5 };
    int value{ add(x, ++x) }; // 未定义的行为: 是 5 + 6, 还是 6 + 6?
    // 这取决于编译器计算函数参数的顺序

    std::cout << value << '\n'; // 值可能是 11 或 12

    return 0;
}
```

C++标准没有定义函数参数的求值顺序。如果首先计算左参数，则这将变成对 add(5, 6) 的调用，它等于11。如果首先计算右的参数，这将成为对 add(6, 6) 的调用，等于12！

{{< alert success >}}
**旁白**

C++标准故意不定义求值顺序，以便编译器可以对给定的体系结构执行任何最自然（因此也是最具性能的）的操作。

{{< /alert >}}

在许多情况下，C++也没有指定何时必须应用运算符的副作用。在应用了副作用的对象在同一语句中多次使用的情况下，这可能导致未定义的行为。

例如，表达式 x + ++x是未指定的行为。当x初始化为1时，Visual Studio和GCC将其计算为2+2，Clang将其计算为由1+2！这是由于编译器应用自增x的副作用时的差异所致。

即使C++标准确实明确了应该如何求值，但从历史上看，这是一个存在许多编译器错误的领域。确保在给定语句中，使用应用了副作用的变量不超过一次，通常可以避免所有这些问题。

{{< alert success >}}
**警告**

C++不定义函数参数或运算符的操作数的求值顺序。

{{< /alert >}}

{{< alert success >}}
**警告**

不要在给定的语句中多次使用具有副作用的变量。如果这样做，则结果可能未定义。

一个例外是简单的赋值表达式语句，如 x = x + y；（也可以重写为 x += y）。

{{< /alert >}}

***

{{< prevnext prev="/basic/chapter6/remaind-exp/" next="/" >}}
6.2 余数和指数
<--->
主页
{{< /prevnext >}}