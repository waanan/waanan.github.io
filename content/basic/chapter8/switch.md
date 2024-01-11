---
title: "Switch语句基础"
date: 2024-01-02T10:33:49+08:00
---

尽管可以将许多if-else语句链接在一起，但这既难以阅读，又效率低下。考虑以下程序：

```C++
#include <iostream>

void printDigitName(int x)
{
    if (x == 1)
        std::cout << "One";
    else if (x == 2)
        std::cout << "Two";
    else if (x == 3)
        std::cout << "Three";
    else
        std::cout << "Unknown";
}

int main()
{
    printDigitName(2);
    std::cout << '\n';

    return 0;
}
```

根据传入的值，printDigitName() 中的变量x最多将求值三次，这是低效的。

根据一组不同的值测试变量或表达式很常见的，因此C++提供了另一种称为switch语句的条件语句，该语句专门用于此目的。下面是与上面相同的程序：

```C++
#include <iostream>

void printDigitName(int x)
{
    switch (x)
    {
        case 1:
            std::cout << "One";
            return;
        case 2:
            std::cout << "Two";
            return;
        case 3:
            std::cout << "Three";
            return;
        default:
            std::cout << "Unknown";
            return;
    }
}

int main()
{
    printDigitName(2);
    std::cout << '\n';

    return 0;
}
```

switch语句背后的思想很简单：计算表达式（有时称为条件）以产生值。如果表达式的值等于任何case标签之后的值，则执行匹配的case标签后面的语句。如果找不到匹配的值并且存在默认标签，则改为执行默认标签之后的语句。

与原始的if语句相比，switch语句的优点是只对表达式求值一次（使其更有效率），switch语句还使读者更清楚地看到，在每个情况下，都有哪些对应的处理语句。

让我们更详细地研究一下这些概念。

{{< alert success >}}
**最佳实践**

做多个选择比较时，首选switch语句而不是多个if-else。

{{< /alert >}}

***
## 使用switch语句

我们通过使用switch关键字来启动switch语句，后跟括号，其中包含要在其中求值的条件表达式。表达式通常只是单个变量，但它可以是任何有效的表达式。

一个限制是，条件必须求值为整数类型（请参见基本数据类型的介绍）或枚举类型（在未来的--无范围枚举中介绍），或者可以转换为一个整数或枚举值。此处不能使用计算为浮点类型、字符串和大多数其他非整型的表达式。

在条件表达式之后，声明了一个代码块。在块内部，我们使用标签来定义要测试相等性的所有值。有两种标签。

{{< alert success >}}
**对于高级读者**

为什么switch语句只允许整数（或枚举）类型？答案是因为switch语句被设计为高度优化。从历史上看，编译器实现switch语句的最常见方法是通过跳转表——跳转表只能处理整数值。

对于那些已经熟悉数组的人来说，跳转表的工作方式与数组非常相似，使用整数值作为数组索引来直接“跳转”到结果。这比进行一系列顺序比较要有效得多。

当然，编译器不必使用跳转表实现switch语句，有时它们也不需要。从技术上讲，C++没有理由不放松限制，以便也可以使用其他类型，只是还没有这样做（截至C++23）。

{{< /alert >}}

***
## case标签

第一种标签是case标签，它使用case关键字声明，后跟常量表达式。常量表达式必须与条件表达式的类型匹配，或者必须可转换为该类型。

如果条件表达式的值等于case标签后的表达式，则从该case标签之后的第一条语句开始执行，然后按顺序继续。

下面是示例：

```C++
#include <iostream>

void printDigitName(int x)
{
    switch (x) // x 为 2
    {
        case 1:
            std::cout << "One";
            return;
        case 2: // 与这个标签匹配
            std::cout << "Two"; // 从这里开始执行
            return; // 然后函数返回
        case 3:
            std::cout << "Three";
            return;
        default:
            std::cout << "Unknown";
            return;
    }
}

int main()
{
    printDigitName(2);
    std::cout << '\n';

    return 0;
}
```

此代码打印：

```C++
Two
```

在上面的程序中，计算x产生值2。由于存在值为2的case标签，因此执行将跳转到该匹配case标签下的语句。程序打印Two，然后执行return语句，函数返回给调用者。

对于可以具有的case标签的数量没有实际限制，但switch中的所有case标签都必须是唯一的。也就是说，您不能这样做：

```C++
switch (x)
{
    case 54:
    case 54:  // error: 54已经存在
    case '6': // error: '6' 会转换为整数 54, 也已经存在
}
```

如果条件表达式与任何case标签都不匹配，则不会执行任何case语句。

***
## default标签

第二种标签是default标签（通常称为默认情况），它是使用default关键字声明的。如果条件表达式与任何case标签都不匹配，并且存在default标签，则从default标签之后的第一条语句开始执行。

下面是与default标签匹配的示例：

```C++
#include <iostream>

void printDigitName(int x)
{
    switch (x) // x 是 5
    {
        case 1:
            std::cout << "One";
            return;
        case 2:
            std::cout << "Two";
            return;
        case 3:
            std::cout << "Three";
            return;
        default: // 5与任何case标签都不匹配
            std::cout << "Unknown"; // 所以从这里开始执行
            return; // 然后返回给调用者
    }
}

int main()
{
    printDigitName(5);
    std::cout << '\n';

    return 0;
}
```

打印：

```C++
Unknown
```

default标签是可选的，每个switch语句只能有一个default标签。按照惯例，default情况放在switch块中的最后一个。

{{< alert success >}}
**最佳实践**

将default标签放在switch块的最后一个。

{{< /alert >}}

***
## 没有匹配的case标签，也没有default标签

如果条件表达式的值与任何case标签都不匹配，并且没有default标签，则不会执行switch内的任何语句。

```C++
#include <iostream>

void printDigitName(int x)
{
    switch (x) // x 是 5
    {
    case 1:
        std::cout << "One";
        return;
    case 2:
        std::cout << "Two";
        return;
    case 3:
        std::cout << "Three";
        return;
    // 没有匹配的case标签，也没有defaule标签
    }

    // 所以从这里继续执行
    std::cout << "Hello";
}

int main()
{
    printDigitName(5);
    std::cout << '\n';

    return 0;
}
```

在上面的示例中，x求值为5，但没有与5匹配的case标签，也没有default标签。因此，不会执行任何switch内的语句。从switch后继续执行，打印Hello。

***
## 使用break关键字

在上面的例子中，我们使用return语句来停止标签后面的语句的执行。然而，这也会退出整个函数。

break语句（使用break关键字声明）告诉编译器，我们已经完成了在switch中执行语句的操作，需要执行switch后的下一条语句。这允许我们在不退出整个函数的情况下退出switch语句。

下面是一个稍微修改的示例，使用break而不是return重写：

```C++
#include <iostream>

void printDigitName(int x)
{
    switch (x) // x 是 3
    {
        case 1:
            std::cout << "One";
            break;
        case 2:
            std::cout << "Two";
            break;
        case 3:
            std::cout << "Three"; // 从这里开始执行
            break; // 跳出switch代码块
        default:
            std::cout << "Unknown";
            break;
    }

    // 从这里继续执行
    std::cout << " Ah-Ah-Ah!";
}

int main()
{
    printDigitName(3);
    std::cout << '\n';

    return 0;
}
```

上面的示例打印：

```C++
Three Ah-Ah-Ah!
```

那么，如果不以break或return结束标签下的一组语句，会发生什么呢？在下一课中，我们将探索该主题。

{{< alert success >}}
**最佳实践**

switch语句中标签下的每一组语句都应该以break语句或return语句结尾。

{{< /alert >}}

***

{{< prevnext prev="/basic/chapter8/constexpr-if/" next="/basic/chapter8/switch-fallthrough-scope/" >}}
8.3 Constexpr if语句
<--->
8.5 switch fallthrough机制与作用域
{{< /prevnext >}}
