---
title: "常见的语义错误"
date: 2024-01-17T13:13:14+08:00
---

在前面我们介绍了语法错误，当您编写不符合C++语言语法的无效代码时会发生语法错误。编译器将通知您此类错误，因此它们很容易捕获，并且通常很容易修复。

我们还讨论了语义错误，这些错误发生在您编写的代码没有达到预期目的时。编译器通常不会捕获语义错误（尽管在某些情况下，智能编译器可能能够生成警告）。

语义错误会导致程序出现非预期的结果，例如导致程序产生错误的结果、导致不稳定的行为、损坏程序数据、导致程序崩溃——或者可能根本没有任何影响。

在编写程序时，几乎不可避免地会出现语义错误。在使用程序时，可能会有明显的问题：例如，如果您正在编写迷宫游戏，您的角色能够穿墙。测试程序也可以帮助发现语义错误。

但还有一件事可以帮助我们——那就是知道哪种类型的语义错误最常见，所以你可以花更多的时间来确保避免这类问题。

在本课中，将讨论C++中发生的一系列最常见类型的语义错误（其中大多数都与控制语句有关）。

***
## 条件逻辑错误

最常见的语义错误类型之一是条件逻辑错误。当程序员错误地编写条件语句或循环条件的逻辑时，会发生条件逻辑错误。下面是一个简单的示例：

```C++
#include <iostream>

int main()
{
    std::cout << "Enter an integer: ";
    int x{};
    std::cin >> x;

    if (x >= 5) // oops, 错误的使用 >= 而不是 >
        std::cout << x << " is greater than 5\n";

    return 0;
}
```

下面是条件逻辑错误的程序的运行：

```C++
Enter an integer: 5
5 is greater than 5
```

当用户输入5时，条件表达式x>=5的计算结果为true，因此执行关联的语句。

下面是另一个使用for循环的示例：

```C++
#include <iostream>

int main()
{
    std::cout << "Enter an integer: ";
    int x{};
    std::cin >> x;

    // oops, 使用了 > 而不是 <
    for (int count{ 1 }; count > x; ++count)
    {
        std::cout << count << ' ';
    }

    std::cout << '\n';

    return 0;
}
```

这个程序应该打印1和用户输入的数字之间的所有数字。但它实际上是这样做的：

```C++
Enter an integer: 5
```

它没有打印任何内容。发生这种情况是因为在for循环的入口，count > x 是false，因此循环内的代码根本不会执行。

***
## 死循环

如下这个示例：

```C++
#include <iostream>
 
int main()
{
    int count{ 1 };
    while (count <= 10) // 这个条件语句永远不会是 false
    {
        std::cout << count << ' '; // 这一行会一直重复执行
    }
 
    std::cout << '\n'; // 这一行不会执行到

    return 0; // 这一行不会执行到
}
```

在这种情况下，忘记了递增count变量，因此循环条件永远不会为false，循环将一直打印：

```C++
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
```

直到用户关闭程序。

这里有另一个例子。下面的代码有什么问题？

```C++
#include <iostream>

int main()
{
    for (unsigned int count{ 5 }; count >= 0; --count)
    {
        if (count == 0)
            std::cout << "blastoff! ";
        else
          std::cout << count << ' ';
    }

    std::cout << '\n';

    return 0;
}
```

这个程序应该打印5 4 3 2 1 blastoff!，确实如此，但它并没有就此止步。实际上，它打印：

```C++
5 4 3 2 1 blastoff! 4294967295 4294967294 4294967293 4294967292 4294967291
```

然后继续递减。程序永远不会终止，因为当count是无符号整数时，count>=0永远不能为false。

***
## 循环迭代次数错误

当循环执行多一次或少一次时会发生错误。例如：

```C++
#include <iostream>

int main()
{
    for (int count{ 1 }; count < 5; ++count)
    {
        std::cout << count << ' ';
    }

    std::cout << '\n';

    return 0;
}
```

程序员打算打印1 2 3 4 5。然而，使用了错误的关系运算符（<而不是<=），因此循环的执行次数比预期的少一次，打印1 2 3 4。

***
## 运算符优先级不正确

以下程序会犯运算符优先级错误：

```C++
#include <iostream>

int main()
{
    int x{ 5 };
    int y{ 7 };

    if (!x > y) // oops: 运算符优先级问题
        std::cout << x << " is not greater than " << y << '\n';
    else
        std::cout << x << " is greater than " << y << '\n';

    return 0;
}
```

由于逻辑NOT的优先级高于运算符>，因此条件的求值方式就像它是（!x）> y 一样，这不是我们想要的。

因此，该程序打印：

```C++
5 is greater than 7
```

在同一表达式中混合逻辑OR和逻辑AND时也可能发生这种情况（逻辑AND优先于逻辑OR）。使用显式括号来避免这类错误。

***
## 浮点类型的精度问题

以下浮点变量的精度不足，无法存储整个数字：

```C++
#include <iostream>

int main()
{
    float f{ 0.123456789f };
    std::cout << f << '\n';

    return 0;
}
```

由于缺乏精度，数字稍微四舍五入：

```C++
0.123457
```

在前面，我们讨论了，运算符==和运算符!=，由于舍入错误（以及如何处理它），比较浮点数可能会有问题。下面是一个示例：

```C++
#include <iostream>

int main()
{
    double d{ 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 }; // should sum to 1.0

    if (d == 1.0)
        std::cout << "equal\n";
    else
        std::cout << "not equal\n";

    return 0;
}
```

该程序打印：

```C++
not equal
```

对浮点数进行的算术运算越多，它积累的小舍入错误就越多。

***
## 整数除法

在下面的示例中，打算进行浮点除法，但由于两个操作数都是整数，因此最终只能进行整数除法：

```C++
#include <iostream>

int main()
{
    int x{ 5 };
    int y{ 3 };

    std::cout << x << " divided by " << y << " is: " << x / y << '\n'; // 整数除法

    return 0;
}
```

这将打印：

```C++
5 divided by 3 is: 1
```

在前面，我们展示了可以使用static_cast将一个整数操作数转换为浮点值，以便进行浮点除法。

***
## 意外的空语句

在if语句学习中，讨论了空语句，它们是不做任何事情的语句。

在下面的程序中，我们只想在获得用户许可的情况下炸毁世界：

```C++
#include <iostream>

void blowUpWorld()
{
    std::cout << "Kaboom!\n";
} 

int main()
{
    std::cout << "Should we blow up the world again? (y/n): ";
    char c{};
    std::cin >> c;

    if (c=='y'); // 意外的空语句
        blowUpWorld(); // 所以这一行会执行到，因为它不是if语句的一部分
 
    return 0;
}
```

然而，由于意外的空语句，始终会执行对blowUpWorld()的函数调用，因此不管怎样，都会执行到 Kaboom! ：

```C++
Should we blow up the world again? (y/n): n
Kaboom!
```

***
## 需要复合语句时不使用复合语句

上述程序的另一个变体也总是会炸毁世界：

```C++
#include <iostream>

void blowUpWorld()
{
    std::cout << "Kaboom!\n";
} 

int main()
{
    std::cout << "Should we blow up the world again? (y/n): ";
    char c{};
    std::cin >> c;

    if (c=='y')
        std::cout << "Okay, here we go...\n";
        blowUpWorld(); // oops, 这一行也会永远执行到
 
    return 0;
}
```

该程序打印：

```C++
Should we blow up the world again? (y/n): n
Kaboom!
```

悬空的else也属于这一类问题。

***
## 还有什么？

上面是新C++程序员倾向于犯的最常见的一些语义错误，但还有更多。读者们，如果您有任何其他认为是常见陷阱的问题，请在评论留言。

***
