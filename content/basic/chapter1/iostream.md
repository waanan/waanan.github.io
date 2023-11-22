---
title: "iostream:cout、cin和endl简介"
date: 2023-10-09T20:06:10+08:00
---

在本课中，将更多地讨论在Hello world程序中使用的std::cout。我们使用它输出文本Hello world！到控制台。此外还将讲解如何使用std::cin如何从用户那里获得输入，这将使程序更具交互性。

***
## 输入/输出库

输入/输出库（io库）是C++标准库中处理基本输入和输出的一部分。我们将使用该库中的功能从键盘获取输入，并将数据输出到控制台。iostream的io部分表示输入（input）/输出（output）。

要使用iostream库中定义的功能，需要在代码文件的顶部包含对应的头文件。

```C++
#include <iostream>

// 后续的代码可以使用iostream的函数
```

***
## std::cout

iostream库包含一些预定义的变量供我们使用。最有用的一个是std::cout，它允许我们将数据发送到控制台，以打印为文本。cout代表“字符输出”(character output)。

下面是之前的Hello world程序：

```C++
#include <iostream> // 之后可以使用 std::cout

int main()
{
    std::cout << "Hello world!"; // 打印 Hello world! 到控制台

    return 0;
}
```

在这个程序中包含了iostream，以便可以访问std::cout。在主函数中，使用std::cout和插入操作符（<<）来发送文本Hello world！到要打印的控制台。

std::cout不仅可以打印文本，还可以打印数字：

```C++
#include <iostream>

int main()
{
    std::cout << 4; // 打印 4 到控制台

    return 0;
}
```

该程序打印：

```C++
4
```

它还可以用于打印变量的值：

```C++
#include <iostream>

int main()
{
    int x = 5; // 定义一个初始值为5的变量x
    std::cout << x; // 打印变量x的值5到控制台
    return 0;
}
```

该程序打印：

```C++
5
```

要在同一行上打印多个内容，可以在单个语句中多次使用插入运算符（<<）来连接多个输出。例如：

```C++
#include <iostream>

int main()
{
    std::cout << "Hello" << " world!";
    return 0;
}
```

该程序打印：

```C++
Hello world!
```

下面是另一个例子，在同一语句中打印文本和变量和值：

```C++
#include <iostream>

int main()
{
    int x = 5;
    std::cout << "x is equal to: " << x;
    return 0;
}
```

该程序打印：

```C++
x is equal to: 5
```

***
## std::endl

下面的程序打印什么？

```C++
#include <iostream>

int main()
{
    std::cout << "Hi!";
    std::cout << "My name is Alex.";
    return 0;
}
```

您可能会对结果感到惊讶：

```C++
Hi!My name is Alex.
```

单独的输出语句不会在控制台上产生单独的输出行。

如果我们想将单独的输出行打印到控制台，我们需要告诉控制台何时将光标移动到下一行。

一种方法是使用std::endl。当使用std::cout输出时，std::endl将换行字符打印到控制台（光标因此会转到下一行的开头）。在这种情况下，endl代表“一行结束，换行”。

例如：

```C++
#include <iostream>

int main()
{
    std::cout << "Hi!" << std::endl; // std::endl会让之后的输出在下一行中
    std::cout << "My name is Alex." << std::endl;

    return 0;
}
```

这将打印：

```C++
Hi!
My name is Alex.
```

***
## std::cout缓冲

考虑在游乐园坐过山车的场景。乘客出现（以某种可变的速度）并排队。列车定期到达并登机（达到列车的最大容量）。当列车满载，或当足够的时间过去时，列车与一批乘客一起出发，骑乘开始。任何不能登上当前列车的乘客都要等待下一班列车。

这类似于在C++中如何处理发送到std::cout的输出。程序中的语句请求将输出发送到控制台。然而，该输出通常不会立即发送到控制台。相反，请求的输出“进入队列”，并存储在预留的内存区域（称为缓冲区）中。定期刷新缓冲区的数据输出到控制台。

这也意味着，如果程序在刷新缓冲区之前崩溃、中止或暂停（例如，出于调试目的），缓冲区内到数据并不会输出到外部。


{{< alert success >}}
**关键点**

缓冲输出的反义词是无缓冲输出。对于无缓冲输出，每个单独的输出请求都直接发送到输出设备。

将数据写入缓冲区通常很快，而将数据传输到输出设备则相对较慢。当存在多个输出请求时，缓冲可以最大限度地减少需要执行的慢速传输的数量，从而显著提高性能。

{{< /alert >}}

***
## std::endl vs "\n"

相比于输出"\n"来进行换行,使用std::endl可能有点低效。因为它实际上执行两项工作：将光标移动到控制台的下一行，并刷新缓冲区。当将文本写入控制台时，我们通常不需要刷新每行末尾的缓冲区。让系统定期刷新自己更有效。

因此，通常首选使用"\n"字符。"\n"字符将光标移动到控制台的下一行，但不刷新缓冲区。

下面是一个以两种不同方式使用"\n"的示例：

```C++
#include <iostream>

int main()
{
    int x{ 5 };
    std::cout << "x is equal to: " << x << "\n"; // 单独使用"\n"
    std::cout << "And that's all, folks!\n";     // 将"\n"放置在要输出到字符串尾巴上
    return 0;
}
```

这将打印：

```C++
x is equal to: 5
And that's all, folks!
```

当嵌入到已经双引号的文本中时，不需要额外的引号。

当我们进入关于字符的课程时，将更详细地讨论“\n”是什么。

***
## std::cin

std::cin是在iostream库中定义的另一个预定义变量。std::cout使用插入操作符（<<）将数据打印到控制台，但std:∶cin（代表字符输入, character input）使用提取操作符（>>）从键盘读取输入。输入必须存储在要使用的变量中。

```C++
#include <iostream>

int main()
{
    std::cout << "Enter a number: ";

    int x{ };
    std::cin >> x; // 从键盘中读取一个数字，并保存到变量x中

    std::cout << "You entered " << x << std::endl;
    return 0;
}
```

尝试编译此程序并自己运行它。运行程序时，第5行将打印"Enter a number: "。当代码到达第8行时，程序将等待您输入。一旦输入一个数字（并按enter），您输入的数字将被赋值给变量x。最后，在第10行，程序将打印"You entered "，后跟您刚才输入的数字。

例如（输入了4）：

```C++
Enter a number: 4
You entered 4
```

这是一种从用户获得键盘输入的简单方法，后面的许多示例中也会使用。

正如可以在单行中输出多个文本位一样，也可以在单行中输入多个值：

```C++
#include <iostream>

int main()
{
    std::cout << "Enter two numbers separated by a space: ";

    int x{ };
    int y{ };
    std::cin >> x >> y; // 读入两个数字并且按顺序在变量x和y中

    std::cout << "You entered " << x << " and " << y << std::endl;

    return 0;
}
```

输出：

```C++
Enter two numbers separated by a space: 5 6
You entered 5 and 6
```

我们将在以后的课程中讨论std::cin如何处理无效输入。现在，只需知道std::cin将尽可能多地提取，并且任何无法提取的输入字符都将留给以后来提取。

***
## 总结

新程序员通常会混淆std::cin、std::cout、插入操作符（<<）和提取操作符（>>）。下面是一种简单的记忆方法：

1. std::cin和std::cout始终位于语句的左侧。
2. std::cout用于输出值（cout=字符输出）
3. std::cin用于获取输入值（cin=字符输入）
4. <<与std::cout一起使用，并显示数据移动的方向（如果std:∶cout表示控制台，则输出数据从变量移动到控制台）。std::cout<<4将值4移动到控制台
5. >>与std::cin一起使用，并显示数据移动的方向（如果std:∶cin表示键盘，则输入数据从键盘移动到变量）。std::cin>>x将用户输入的值从键盘移动到x中

***

{{< prevnext prev="/basic/chapter1/variable-init-assign/" next="/basic/chapter1/uninit-variable/" >}}
1.3 变量初始化和赋值
<--->
1.5 未初始化的变量及未定义的行为
{{< /prevnext >}}
