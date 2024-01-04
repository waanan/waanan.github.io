---
title: "常见的if语句问题"
date: 2024-01-02T10:33:49+08:00
---

在本课将研究使用if语句时出现的一些常见问题。

***
## 嵌套的if语句和悬空的else问题

可以将if语句嵌套在其他if语句中：

```C++
#include <iostream>

int main()
{
    std::cout << "Enter a number: ";
    int x{};
    std::cin >> x;

    if (x >= 0) // 外层if条件
        // 这样的嵌套if代码样式，非常差
        if (x <= 20) // 内层if语句
            std::cout << x << " is between 0 and 20\n";

    return 0;
}
```

现在考虑以下程序：

```C++
#include <iostream>

int main()
{
    std::cout << "Enter a number: ";
    int x{};
    std::cin >> x;

    if (x >= 0) // 外层if条件
        // 这样的嵌套if代码样式，非常差
        if (x <= 20) // 内层if语句
            std::cout << x << " is between 0 and 20\n";

    // 这个else语句，属于哪个if条件呢？
    else
        std::cout << x << " is negative\n";

    return 0;
}
```

上面的程序引入了一个潜在的歧义源，称为悬空else问题。上面程序中的else语句与外部还是内部if语句匹配？

答案是，else语句与同一块中最后一个不匹配的if语句成对。因此，在上面的程序中，else与内部if语句匹配，就像程序是这样编写的：

```C++
#include <iostream>

int main()
{
    std::cout << "Enter a number: ";
    int x{};
    std::cin >> x;

    if (x >= 0) // 外层if条件
    {
        if (x <= 20) // 内层if语句
            std::cout << x << " is between 0 and 20\n";
        else // 内层if语句对应的else
            std::cout << x << " is negative\n";
    }

    return 0;
}
```

这导致上述程序产生不合预期的输出：

```C++
Enter a number: 21
21 is negative
```

为了在嵌套if语句时避免这种歧义，最好将内部if语句显式封装在代码块中。这允许我们在if语句中附加else，而不会产生歧义：

```C++
#include <iostream>

int main()
{
    std::cout << "Enter a number: ";
    int x{};
    std::cin >> x;

    if (x >= 0)
    {
        if (x <= 20)
            std::cout << x << " is between 0 and 20\n";
        else // 与内层if语句对应
            std::cout << x << " is greater than 20\n";
    }
    else // 与外层else语句对应
        std::cout << x << " is negative\n";

    return 0;
}
```

块内的else语句对应到内部if语句，块外的else语句对应到外部if语句。

***
## 展平嵌套if语句

嵌套的if语句通常可以通过重新构造逻辑展平。嵌套较少的代码不太容易出错。

例如，上述示例可以如下展平：

```C++
#include <iostream>

int main()
{
    std::cout << "Enter a number: ";
    int x{};
    std::cin >> x;

    if (x < 0)
        std::cout << x << " is negative\n";
    else if (x <= 20) //  x 大于等于0，小于等于20
        std::cout << x << " is between 0 and 20\n";
    else // x大于20
        std::cout << x << " is greater than 20\n";

    return 0;
}
```

下面是另一个使用逻辑运算符检查单个if语句中的多个条件的示例：

```C++
#include <iostream>

int main()
{
    std::cout << "Enter an integer: ";
    int x{};
    std::cin >> x;

    std::cout << "Enter another integer: ";
    int y{};
    std::cin >> y;

    if (x > 0 && y > 0) // 检查x与y同时大于0
        std::cout << "Both numbers are positive\n";
    else if (x > 0 || y > 0) // 检查x与y，只有一个大于0
        std::cout << "One of the numbers is positive\n";
    else
        std::cout << "Neither number is positive\n";

    return 0;
}
```

***
## 空语句（Null statements）

空语句是仅由分号组成的表达式语句：

```C++
if (x > 10)
    ; // 这是一个空语句
```

空语句不执行任何操作。它们通常在语言需要存在语句但程序员不需要时使用。为了可读性，空语句通常放在自己单独的行中。

在本章后面的内容中，当我们讨论循环时，我们将看到故意空语句的示例。空语句很少故意与if语句一起使用。然而，它们可能会无意中为新的（或粗心的）程序员带来问题。请考虑以下片段：

```C++
if (nuclearCodesActivated());
    blowUpTheWorld();
```

在上面的片段中，程序员不小心在if语句的末尾放了一个分号（这是一个常见的错误，因为许多语句以分号结尾）。这段代码编译良好，但执行时，等价于这样编写的：

```C++
if (nuclearCodesActivated())
    ; // 分号，这里是一个空语句
blowUpTheWorld(); // 这一行永远能执行到
```

{{< alert success >}}
**警告**

注意不要用分号“终止”if语句，否则true或false对应的语句将无条件执行（即使它们在块中）。

{{< /alert >}}

***
## 条件表达式中，运算符== 与 运算符=

在条件表达式中，在测试相等性时应该使用operator==，而不是operator=（这是赋值）。考虑以下程序：

```C++
#include <iostream>

int main()
{
    std::cout << "Enter 0 or 1: ";
    int x{};
    std::cin >> x;
    if (x = 0) // oops, 这里使用赋值，而不是相等性测试
        std::cout << "You entered 0\n";
    else
        std::cout << "You entered 1\n";

    return 0;
}
```

该程序将编译和运行，但在会产生错误的结果：

```C++
Enter 0 or 1: 0
You entered 1
```

事实上，该程序将始终产生结果1。这是因为x = 0首先将值0赋值给x，然后计算x的值，该值现在为0，这是布尔false。由于条件语句结果总是false，因此else语句总是执行。

***

{{< prevnext prev="/basic/chapter8/if-block/" next="/basic/chapter8/constexpr-if/" >}}
8.1 If语句与代码块
<--->
8.3 Constexpr if语句
{{< /prevnext >}}
