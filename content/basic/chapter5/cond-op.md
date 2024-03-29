---
title: "条件运算符"
date: 2023-11-28T13:19:42+08:00
---

|  符号 | 形式 |  含义  |
|  ---- | ----  | ----  |
| ? : | c ? x : y | 表达式c的结果为true，计算x，否则计算y |

条件运算符（? :）（有时也称为算术if运算符）是三元运算符（接受3个操作数的运算符）。因为它在历史上是C++唯一的三元运算符，所以有时也被称为“三元运算符”。

条件运算符操作符为执行特定类型的if-else语句提供了一种速记方法。

概括地说，if-else语句采用以下形式：

```C++
if (条件表达式)
    true_对应的语句;
else
    false_对应的语句;
```

如果 条件表达式 的计算结果为true，则执行 true_对应的语句，否则执行 false_对应的语句。else和 false_对应的语句 是可选的。

条件运算符运算符采用以下形式：

```C++
条件表达式 ? true_对应的语句 : false_对应的语句;
```

如果 条件表达式 的计算结果为true，则执行 true_对应的语句，否则执行 false_对应的语句。: 和 false_对应的语句 是必选的。

考虑如下所示的if-else语句：

```C++
if (x > y)
    greater = x;
else
    greater = y;
```

这可以重写为：

```C++
greater = ((x > y) ? x : y);
```

在这种情况下，条件运算符可以帮助压缩代码，而不会丢失可读性。

***
## 条件运算符是表达式

由于条件运算符是表达式而不是语句，因此条件运算符可以用于需要表达式的位置。

例如，初始化变量时：

```C++
#include <iostream>

int main()
{
    constexpr bool inBigClassroom { false };
    constexpr int classSize { inBigClassroom ? 30 : 20 };
    std::cout << "The class size is: " << classSize << '\n';

    return 0;
}
```

如果用if-else替代。您可能会尝试这样的操作：

```C++
#include <iostream>

int main()
{
    constexpr bool inBigClassroom { false };

    if (inBigClassroom)
        constexpr int classSize { 30 };
    else
        constexpr int classSize { 20 };

    std::cout << "The class size is: " << classSize;

    return 0;
}
```

然而，这无法编译，并且将得到一条错误消息，即classSize未定义。就像函数中定义的变量在函数的末尾失效一样，在if语句或else语句内定义的变量也会在if或else的末尾失效。因此，在我们尝试打印classSize时，它已经被破坏了。

如果要使用If-else，则必须执行以下操作：

```C++
#include <iostream>

int getClassSize(bool inBigClassroom)
{
    if (inBigClassroom)
        return 30;
    else
        return 20;
}

int main()
{
    const int classSize { getClassSize(false) };
    std::cout << "The class size is: " << classSize;

    return 0;
}
```

这一个可以工作，因为getClassSize(false) 是一个表达式，而if-else逻辑位于函数内部（可以在其中使用语句）。但这是许多额外的代码。

***
## 带圆括号的条件运算符

由于C++大多数操作符的求值优先于条件操作符的计算，因此条件操作符容易与您的预期执行顺序不同。

例如：

```C++
#include <iostream>

int main()
{
    int x { 2 };
    int y { 1 };
    int z { 10 - x > y ? x : y };
    std::cout << z;
    
    return 0;
}
```

您可能期望它的计算结果为10 - (x > y ? x : y )（这将计算为8），但它实际上的计算结果是(10 - x) > y ? x : y（计算为2）。

由于这个原因，条件运算符应该用括号括起来：

1. 如果条件运算符作为子表达式，用圆括号括住整个条件运算符。
2. 为了可读性，条件运算符如果条件表达式中包含任何运算符（函数调用运算符除外），请用括号括起来。

条件运算符的操作数不需要括号。

让我们看一下包含条件运算符的一些语句，以及如何将它们括起来：

```C++
return isStunned ? 0 : movesLeft;           // 不作为子表达式, 条件表达式中无操作符
int z { (x > y) ? x : y };                  // 不作为子表达式, 条件表达式中有操作符
std::cout << (isAfternoon() ? "PM" : "AM"); // 作为子表达式, 条件表达式中无操作符 (函数调用运算符除外)
std::cout << ((x > y) ? x : y);             // 作为子表达式, 条件表达式中有操作符
```

{{< alert success >}}
**相关内容**

在未来的——运算符优先级和结合性——中，我们讨论了C++对运算符求值进行优先级排序的方法。

{{< /alert >}}

{{< alert success >}}
**最佳实践**

在复合表达式中使用时，用圆括号括住整个条件运算符。

为了可读性，如果条件表达式中包含任何运算符（函数调用运算符除外），请用括号括起来。

{{< /alert >}}

***
## 表达式的类型必须匹配或可转换

要符合C++的类型检查规则，必须满足以下条件之一：

1. 第二个和第三个操作数的类型必须匹配。
2. 编译器必须能够找到将第二个和第三个操作数中的一个或两个转换为匹配类型的方法。编译器使用的转换规则相当复杂，在某些情况下可能会产生令人惊讶的结果。


例如：

```C++
#include <iostream>

int main()
{
    std::cout << (true ? 1 : 2) << '\n';    // okay: 两个操作数的类型都是int

    std::cout << (false ? 1 : 2.2) << '\n'; // okay: int  1 被转换为 double

    std::cout << (true ? -1 : 2u) << '\n';  // 令人惊讶: -1 被转换为 unsigned int, 发生溢出

    return 0;
}
```

以上打印内容：

```C++
1
2.2
4294967295
```

通常，可以将操作数中的基本类型混用（不包括混合有符号和无符号值）。如果其中一个操作数不是基本类型，通常最好自己显式地将它转换为匹配类型，以便确切地知道将得到什么。

如果编译器无法找到将第二个和第三个操作数转换为匹配类型的方法，则将导致编译错误：

```C++
#include <iostream>

int main()
{
    constexpr int x{ 5 };
    std::cout << (x != 5 ? x : "x is 5"); // compile error: constexpr int 与 C-style 字符串 类型无法匹配

    return 0;
}
```

在上面的示例中，一个表达式是整数，另一个是C样式的字符串文字。编译器将无法找到匹配的类型，因此将导致编译错误。

在这种情况下，可以执行显式转换，也可以使用if-else语句：

```C++
#include <iostream>
#include <string>

int main()
{
    constexpr int x{ 5 };

    // 可以现实的做类型转换
    std::cout << (x != 5 ? std::to_string(x) : std::string{"x is 5"}) << '\n';

    // 或者使用 if-else
    if (x != 5)
        std::cout << x << '\n';
    else
        std::cout << "x is 5" << '\n';
    
    return 0;
}
```

***
## 那么什么时候应该使用条件运算符？

当执行以下操作之一时，条件运算符有限使用：

1. 使用两个值之一初始化对象。
2. 将两个值之一指定给对象。
3. 将两个值之一传递给函数。
4. 从函数中返回两个值之一。
5. 打印两个值之一。

复杂的表达式通常应避免使用条件运算符，因为它们往往容易出错，并且难以阅读。

{{< alert success >}}
**最佳实践**

在复杂的表达式中，最好避免使用条件运算符。

{{< /alert >}}

***

{{< prevnext prev="/basic/chapter5/num-sys/" next="/basic/chapter5/inline/" >}}
5.4 数字系统（十进制、二进制、十六进制和八进制）
<--->
5.6 内联函数和变量
{{< /prevnext >}}
