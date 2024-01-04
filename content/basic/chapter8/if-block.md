---
title: "If语句与代码块"
date: 2024-01-02T10:33:49+08:00
---

我们将要讨论的第一类控制流语句是条件语句。条件语句是指定，根据一个判定条件，来确定是否应执行某些关联语句的语句。

C++支持两种基本类型的条件句：if语句（之前有过简单介绍）和switch语句（本章讨论）。

***
## if语句快速回顾

C++中最基本的条件语句类型是if语句。if语句的格式为：

```C++
if (条件表达式) true_对应的语句;
```

或使用可选的else语句：

```C++
if (条件表达式)
    true_对应的语句;
else
    false_对应的语句;
```

如果条件的计算结果为true，则执行true对应的语句。如果条件的计算结果为false，并且可选的else语句存在，则执行false对应的语句。

下面是一个简单的程序，它将if语句与可选的else语句一起使用：

```C++
#include <iostream>

int main()
{
    std::cout << "Enter a number: ";
    int x{};
    std::cin >> x;

    if (x > 10)
        std::cout << x << " is greater than 10\n";
    else
        std::cout << x << " is not greater than 10\n";

    return 0;
}
```

程序运行结果与预期的一致：

```C++
Enter a number: 15
15 is greater than 10
```

```C++
Enter a number: 4
4 is not greater than 10
```

***
## 根据if或else的结果，来执行多条语句

新手程序员通常会这样尝试：

```C++
#include <iostream>

namespace constants
{
    constexpr int minRideHeightCM { 140 };
}

int main()
{
    std::cout << "Enter your height (in cm): ";
    int x{};
    std::cin >> x;

    if (x >= constants::minRideHeightCM)
        std::cout << "You are tall enough to ride.\n";
    else
        std::cout << "You are not tall enough to ride.\n";
        std::cout << "Too bad!\n"; // 预期检查失败，才执行这一行

    return 0;
}
```

然而，考虑以下程序运行效果：

```C++
Enter your height (in cm): 180
You are tall enough to ride.
Too bad!
```

该程序不能按预期工作，因为结果为true对应的语句，和结果为flase对应的语句，只能是单条语句。缩进在这里欺骗了我们——上面的程序执行起来就像它是按如下方式编写的：

```C++
#include <iostream>

namespace constants
{
    constexpr int minRideHeightCM { 140 };
}

int main()
{
    std::cout << "Enter your height (in cm): ";
    int x{};
    std::cin >> x;

    if (x >= constants::minRideHeightCM)
        std::cout << "You are tall enough to ride.\n";
    else
        std::cout << "You are not tall enough to ride.\n";

    std::cout << "Too bad!\n"; // 预期检查失败，才执行这一行

    return 0;
}
```

可以清楚的看到，“Too bad!”这一行会永远执行到。

然而，通常希望基于某种条件执行多个语句。为此，我们可以使用复合语句（代码块）：

```C++
#include <iostream>

namespace constants
{
    constexpr int minRideHeightCM { 140 };
}

int main()
{
    std::cout << "Enter your height (in cm): ";
    int x{};
    std::cin >> x;

    if (x >= constants::minRideHeightCM)
        std::cout << "You are tall enough to ride.\n";
    else
    { // 这里使用代码块
        std::cout << "You are not tall enough to ride.\n";
        std::cout << "Too bad!\n";
    }

    return 0;
}
```

请记住，代码块被视为单个语句，因此现在可以按预期工作：

```C++
Enter your height (in cm): 180
You are tall enough to ride.
```

```C++
Enter your height (in cm): 130
You are not tall enough to ride.
Too bad!
```

***
## 条件结果的单条语句，是否应该放在代码块中？

对于if或else后面的单个语句是否应显式封装在代码块中，程序员社区中存在争议。

通常有两个理由，需要放在代码块中。

首先，考虑以下片段：

```C++
if (age >= minDrinkingAge)
    purchaseBeer();
```

现在，假设匆忙的修改此程序以添加另一个能力：

```C++
if (age >= minDrinkingAge)
    purchaseBeer();
    driverCar(); // 这一行会永远执行
```

哎呀，未到一定年龄是无法开车的。这样的修改，很容易使一条语句在任何条件下都能执行到。

其次，它会使程序更难调试。假设我们有以下片段：

```C++
if (age >= minDrinkingAge)
    addBeerToCart();

checkout();
```

假设我们怀疑addBeerToCart()函数有问题，因此将其注释掉：

```C++
if (age >= minDrinkingAge)
//    addBeerToCart();

checkout();
```

现在我们已经将checkout()设为满足条件后要执行的语句，这肯定不是我们想要的。

如果总是在if或else语句之后使用代码块，则不会出现这些问题。

不在单个语句周围使用块的最佳理由是，通过垂直间隔添加块，一次会看到较少的代码，这会降低代码的可读性，并可能导致其他更严重的错误。

社区似乎更喜欢总是使用代码块，而不是不使用代码块。

中间的替代方法是将单个语句放在与if语句相同的一行上：

```C++
if (age >= minDrinkingAge) purchaseBeer();
```

这避免了上面提到的两个缺点，对可读性的影响很小。

{{< alert success >}}
**最佳实践**

考虑将与if或else相关的单个语句放在块中（特别是在学习时）。

{{< /alert >}}

***
## 隐式块

如果没有在if else语句里使用代码块，编译器将隐式声明块。因此：

```C++
if (条件表达式)
    true_对应的语句;
else
    false_对应的语句;
```

实际上相当于：

```C++
if (条件表达式)
{
    true_对应的语句;
}
else
{
    false_对应的语句;
}
```

大多数时候，这并不重要。然而，新手程序员有时会尝试这样做：

```C++
#include <iostream>

int main()
{
    if (true)
        int x{ 5 };
    else
        int x{ 6 };

    std::cout << x << '\n';

    return 0;
}
```

这无法编译通过，因为编译器会提示，一个未定义标识符x的错误。这是因为上面的示例等效于：

```C++
#include <iostream>

int main()
{
    if (true)
    {
        int x{ 5 };
    } // x 这里销毁
    else
    {
        int x{ 6 };
    } // x 这里销毁

    std::cout << x << '\n'; // x 不在作用域里

    return 0;
}
```

这样能更清楚的看到，变量x具有代码块作用域，并在块的末尾被销毁。当执行到std::cout行时，x已不存在。

在下一课中，我们将继续探索if语句。

***

{{< prevnext prev="/basic/chapter8/control-flow-intro/" next="/basic/chapter8/if-problem/" >}}
8.0 控制流简介
<--->
8.2 常见的if语句问题
{{< /prevnext >}}
