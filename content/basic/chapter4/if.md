---
title: "if语句简介"
date: 2023-10-09T20:06:10+08:00
---

考虑一个你要去市场的例子，你的室友告诉你，“如果他们有草莓打折，买一些”。这是一个条件语句，意味着只有当条件（“他们有出售的草莓”）为真时，您才会执行一些操作（“买一些”）。

这样的条件在编程中很常见，因为它允许我们在程序中实现条件行为。C++中最简单的条件语句类型称为if语句。只有在某些条件为真时，if语句才允许我们执行一行（或多行）代码。

最简单的if语句采用以下形式：

```C++
if (条件表达式) true_对应的语句;
```

为了可读性，这通常写为：

```C++
if (条件表达式)
    true_对应的语句;
```

条件（也称为条件表达式）是计算为布尔值的表达式。

如果if语句的条件计算为布尔值true，则执行 true_对应的语句。如果条件的计算结果为布尔值false，则跳过 true_对应的语句。

***
## 使用if语句的示例程序

给定以下程序：

```C++
#include <iostream>

int main()
{
    std::cout << "Enter an integer: ";
    int x {};
    std::cin >> x;

    if (x == 0)
        std::cout << "The value is zero\n";

    return 0;
}
```

下面是此程序一次运行的输出：

```C++
Enter an integer: 0
The value is zero
```

首先，用户输入一个整数。然后计算条件 x == 0。相等运算符（==）用于测试两个值是否相等。运算符== 如果操作数相等，则返回true；如果不相等，则为false。由于x的值为0，并且 0 == 0 为true，因此该表达式的计算结果为true。

由于条件的计算结果为true，因此执行后续语句，并打印“The value is zero”。

下面是此程序的另一个运行结果：

```C++
Enter an integer: 5
```

在这种情况下，x==0的计算结果为false。随后的语句被跳过，程序结束，并且不打印任何其他内容。

{{< alert success >}}
**警告**

If语句仅有条件地执行单个语句。我们在后续课程讨论如何有条件地执行多个语句——If语句和块。

{{< /alert >}}

***
## if-else

考虑上面的例子，如果我们想告诉用户他们输入的数字不是零，该怎么办？

我们可以这样写：

```C++
#include <iostream>

int main()
{
    std::cout << "Enter an integer: ";
    int x {};
    std::cin >> x;

    if (x == 0)
        std::cout << "The value is zero\n";
    if (x != 0)
        std::cout << "The value is non-zero\n";

    return 0;
}
```

或者这样：

```C++
#include <iostream>

int main()
{
    std::cout << "Enter an integer: ";
    int x {};
    std::cin >> x;

    bool zero { (x == 0) };
    if (zero)
        std::cout << "The value is zero\n";
    if (!zero)
        std::cout << "The value is non-zero\n";

    return 0;
}
```

这两个程序都比需要的复杂。我们可以使用另一种形式的if语句，叫做 if-else。为以下形式：

```C++
if (条件表达式)
    true_对应的语句;
else
    false_对应的语句;
```

如果条件的计算结果为布尔true，则执行 true_对应的语句。否则执行 false_对应的语句。

让我们修改上面的程序，使用if-else。

```C++
#include <iostream>

int main()
{
    std::cout << "Enter an integer: ";
    int x {};
    std::cin >> x;

    if (x == 0)
        std::cout << "The value is zero\n";
    else
        std::cout << "The value is non-zero\n";

    return 0;
}
```

现在，我们的程序将产生以下输出：

```C++
Enter an integer: 0
The value is zero
```

```C++
Enter an integer: 5
The value is non-zero
```

***
## 串联if语句

有时，我们想检查几个事情按顺序是真是假。我们可以通过将if语句（或if-else）链接到前面的if-else来实现，如下所示：

```C++
#include <iostream>

int main()
{
    std::cout << "Enter an integer: ";
    int x {};
    std::cin >> x;

    if (x > 0)
        std::cout << "The value is positive\n";
    else if (x < 0)
        std::cout << "The value is negative\n";
    else 
        std::cout << "The value is zero\n";

    return 0;
}
```

小于运算符（<）用于测试一个值是否小于另一个值。类似地，大于运算符（>）用于测试一个值是否大于另一个值。这些运算符都返回布尔值。

下面是该程序的几次运行的输出：

```C++
Enter an integer: 4
The value is positive
```

```C++
Enter an integer: -3
The value is negative
```

```C++
Enter an integer: 0
The value is zero
```

请注意，可以根据需要计算的条件多次链接if语句。

***
## 布尔返回值和if语句

在上一课中，我们使用返回布尔值的函数编写了此程序：

```C++
#include <iostream>

// x与y相等返回true, 不然返回false
bool isEqual(int x, int y)
{
    return (x == y); // 操作符== ， x 等于y，返回true，否则返回false
}

int main()
{
    std::cout << "Enter an integer: ";
    int x{};
    std::cin >> x;

    std::cout << "Enter another integer: ";
    int y{};
    std::cin >> y;

    std::cout << std::boolalpha; // 以  true ， false 格式打印bool
    
    std::cout << x << " and " << y << " are equal? ";
    std::cout << isEqual(x, y) << '\n'; // isEqual返回true或false

    return 0;
}
```

让我们使用if语句来改进此程序：

```C++
#include <iostream>
 
// x与y相等返回true, 不然返回false
bool isEqual(int x, int y)
{
    return (x == y); // 操作符== ， x 等于y，返回true，否则返回false
}
 
int main()
{
    std::cout << "Enter an integer: ";
    int x {};
    std::cin >> x;
 
    std::cout << "Enter another integer: ";
    int y {};
    std::cin >> y;
    
    if (isEqual(x, y))
        std::cout << x << " and " << y << " are equal\n";
    else
        std::cout << x << " and " << y << " are not equal\n";

    return 0;
}
```

该程序的两次运行情况：

```C++
Enter an integer: 5
Enter another integer: 5
5 and 5 are equal
```

```C++
Enter an integer: 6
Enter another integer: 4
6 and 4 are not equal
```

在这种情况下，我们的条件表达式是对函数isEqual的函数调用，获取返回的布尔值。

***
## 非布尔条件

在上面的所有示例中，我们的条件要么是布尔值（true或false）、布尔变量，要么是返回布尔值的函数。如果条件是不计算为布尔值的表达式，会发生什么情况？

在这种情况下，条件表达式被转换为布尔值：非零值被转换为 true，零值被转化为 false。

因此，如果我们这样做：

```C++
#include <iostream>

int main()
{
    if (4) // 无任何意义，用来作为示例...
        std::cout << "hi\n";
    else
        std::cout << "bye\n";

    return 0;
}
```

这将打印“hi”，因为4是一个非零值，它被转换为布尔true。

***
## If语句和提前返回

不是函数中最后一个语句的返回语句会导致函数提前返回。这样的语句将导致函数在执行return语句时返回给调用方（在函数以其他方式返回到调用方之前，因此是“提前”）。

无条件的提前返回没有用处：

```C++
void print()
{
    std::cout << "A";

    return; // 函数在这里返回

    std::cout << "B"; // 这行不会执行到
}
```

std::cout << "B"; 将永远不会被执行，我们可以将其删除，然后我们的return语句就是函数的最后一条语句了。

然而，当与if语句组合时，提前返回提供了一种条件化函数返回的方法。

```C++
#include <iostream>

// 返回函数 x的绝对值
int abs(int x) 
{
    if (x < 0)
        return -x; // 提前返回 (当 x < 0)

    return x;
}

int main()
{
    std::cout << abs(4) << '\n'; // 打印 4
    std::cout << abs(-3) << '\n'; // 打印 3

    return 0;
}
```

当调用 abs(4) 时，x的值为4。if (x < 0) 为false，不执行提前返回语句。该函数在函数末尾将x（值4）返回给调用者。

当调用 abs(-3) 时，x的值为-3。if (x < 0) 为true，执行提前返回语句。此时，函数将-x（值3）返回给调用方。

***
