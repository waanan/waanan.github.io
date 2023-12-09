---
title: "逗号运算符"
date: 2023-12-07T13:09:17+08:00
---

逗号运算符（,）允许在允许单个表达式的地方可以编写多个表达式。逗号运算符计算左操作数，然后计算右操作数，最后返回右操作数的结果。

例如：

```C++
#include <iostream>

int main()
{
    int x{ 1 };
    int y{ 2 };

    std::cout << (++x, ++y) << '\n'; // increment x and y, evaluates to the right operand

    return 0;
}
```

首先计算逗号运算符的左操作数，将x从1递增到2。接下来，计算右操作数，将y从2递增到3。逗号运算符返回右操作数（3）的结果，随后将其打印到控制台。

请注意，逗号在所有运算符中的优先级最低，甚至低于赋值。因此，以下两行代码执行不同的操作：

```C++
z = (a, b); // evaluate (a, b) first to get result of b, then assign that value to variable z.
z = a, b; // evaluates as "(z = a), b", so z gets assigned the value of a, and b is evaluated and discarded.
```

这使得逗号运算符的使用有些危险。

在几乎所有情况下，使用逗号运算符编写的语句最好编写为单独的语句。例如，上述代码可以编写为：

```C++
#include <iostream>

int main()
{
    int x{ 1 };
    int y{ 2 };

    ++x;
    std::cout << ++y << '\n';

    return 0;
}
```

大多数程序员根本不使用逗号操作符，唯一的例外是inide for循环，在那里它的使用相当普遍。我们将在以后的第8.10课中讨论for循环——for语句。

{{< alert success >}}
**最佳做法**

避免使用逗号运算符，但在for循环中除外。

{{< /alert >}}

***
## 逗号作为分隔符

在C++中，逗号符号通常用作分隔符，这些用法不会调用逗号运算符。分隔符逗号的一些示例：

```C++
void foo(int x, int y) // Separator comma used to separate parameters in function definition
{
    add(x, y); // Separator comma used to separate arguments in function call
    constexpr int z{ 3 }, w{ 5 }; // Separator comma used to separate multiple variables being defined on the same line (don't do this)
}
```

没有必要避免分隔符逗号（除非在声明多个变量时，您不应该这样做）。

