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

您希望此程序打印什么？

```C++
#include <iostream> // for std::cout

int main()
{
    std::cout << "Hi!";
    std::cout << "My name is Alex.";
    return 0;
}
```

您可能会对结果感到惊讶：

单独的输出语句不会在控制台上产生单独的输出行。

如果我们想将单独的输出行打印到控制台，我们需要告诉控制台何时将光标移动到下一行。

一种方法是使用std:：endl。当使用std:：cout输出时，std::endl将新行字符打印到控制台（导致光标转到下一行的开头）。在这种情况下，endl代表“端线”。

例如：

```C++
#include <iostream> // for std::cout and std::endl

int main()
{
    std::cout << "Hi!" << std::endl; // std::endl will cause the cursor to move to the next line of the console
    std::cout << "My name is Alex." << std::endl;

    return 0;
}
```

这将打印：

{{< alert success >}}
**提示**

在上面的程序中，第二个std:：endl在技术上是不必要的，因为程序随后立即结束。然而，它有几个有用的目的。

首先，它有助于指示输出行是一个“完整的思想”（而不是在代码稍后的某个地方完成的部分输出）。在这个意义上，它的功能类似于在标准英语中使用句点。

其次，它将光标定位在下一行上，以便如果我们稍后添加额外的输出行（例如，让程序说“bye！”），这些行将出现在我们期望的位置（而不是附加到前一行输出）。

第三，从命令行运行可执行文件后，某些操作系统在再次显示命令提示符之前不会输出新行。如果我们的程序没有以光标在新行上结束，则命令提示符可能会追加到输出的前一行，而不是像用户预期的那样出现在新行的开头。

{{< /alert >}}

{{< alert success >}}
**最佳做法**

每当一行输出完成时，输出一个换行。

{{< /alert >}}

***
## std:：cout已缓冲

考虑在你最喜欢的游乐园坐过山车。乘客出现（以某种可变的速度）并排队。列车定期到达并登机（达到列车的最大容量）。当列车满载时，或当足够的时间过去时，列车与一批乘客一起出发，骑乘开始。任何不能登上当前列车的乘客都要等待下一班列车。

这种类比类似于在C++中通常如何处理发送到std:：cout的输出。程序中的语句请求将输出发送到控制台。然而，该输出通常不会立即发送到控制台。相反，请求的输出“进入队列”，并存储在为收集此类请求而预留的内存区域（称为缓冲区）中。定期刷新缓冲区，这意味着缓冲区中收集的所有数据都将传输到其目标（在本例中为控制台）。

这也意味着，如果程序在刷新缓冲区之前崩溃、中止或暂停（例如，出于调试目的），则不会显示仍在缓冲区中等待的任何输出。

{{< alert success >}}
**作者注释**

用另一个类比，冲洗缓冲区有点像冲洗马桶。您收集的所有“输出”都将传输到……下一个位置。伊夫。

{{< /alert >}}

{{< alert success >}}
**关键洞察力**

缓冲输出的反义词是无缓冲输出。对于无缓冲输出，每个单独的输出请求都直接发送到输出设备。

将数据写入缓冲区通常很快，而将一批数据传输到输出设备则相对较慢。当存在多个输出请求时，缓冲可以最大限度地减少需要执行的慢速传输的数量，从而显著提高性能。

{{< /alert >}}

***
## 标准：：endl vs“\n”

使用std:：endl可能有点低效，因为它实际上执行两项工作：将光标移动到控制台的下一行，并刷新缓冲区。当将文本写入控制台时，我们通常不需要刷新每行末尾的缓冲区。让系统定期刷新自己更有效（它被设计为高效地执行）。

因此，通常首选使用“\n”字符。“\n”字符将光标移动到控制台的下一行，但不请求刷新，因此它通常会执行得更好。“\n”字符也更简洁，因为它较短，并且可以嵌入到现有文本中。

下面是一个以两种不同方式使用“\n”的示例：

```C++
#include <iostream> // for std::cout

int main()
{
    int x{ 5 };
    std::cout << "x is equal to: " << x << '\n'; // Using '\n' standalone
    std::cout << "And that's all, folks!\n"; // Using '\n' embedded into a double-quoted piece of text (note: no single quotes when used this way)
    return 0;
}
```

这将打印：

当“\n”单独用于将光标移动到控制台的下一行时，它应该是单引号。当嵌入到已经双引号的文本中时，不需要额外的引号。

当我们进入关于字符的课程（4.11--字符）时，我们将更详细地讨论“\n”是什么。

{{< alert success >}}
**最佳做法**

将文本输出到控制台时，首选“\n”而不是std:：endl。

{{< /alert >}}

{{< alert success >}}
**警告**

“\n”使用反斜杠（就像C++中的所有特殊字符一样），而不是正斜杠。相反，使用正斜杠（例如“/n”）可能会导致意外的行为。

{{< /alert >}}

***
## 标准：：cin

std:：cin是在iostream库中定义的另一个预定义变量。虽然std:：cout使用插入操作符（<<）将数据打印到控制台，但std:∶cin（代表“字符输入”）使用提取操作符（>>）从键盘读取输入。输入必须存储在要使用的变量中。

```C++
#include <iostream>  // for std::cout and std::cin

int main()
{
    std::cout << "Enter a number: "; // ask user for a number

    int x{ }; // define variable x to hold user input (and zero-initialize it)
    std::cin >> x; // get number from keyboard and store it in variable x

    std::cout << "You entered " << x << '\n';
    return 0;
}
```

尝试编译此程序并自己运行它。运行程序时，第5行将打印“输入数字：”。当代码到达第8行时，程序将等待您输入。一旦输入一个数字（并按enter），您输入的数字将被分配给变量x。最后，在第10行，程序将打印“you entered”，后跟您刚才输入的数字。

例如（我输入了4）：

这是一种从用户那里获得键盘输入的简单方法，我们将在后面的许多示例中使用它。请注意，在接受输入时不需要使用“\n”，因为用户需要按enter键接受他们的输入，这将把光标移动到控制台的下一行。

如果在输入数字后屏幕立即关闭，请参阅第0.8课——解决方案的几个常见C++问题。

正如可以在单行中输出多个文本位一样，也可以在单行中输入多个值：

```C++
#include <iostream>  // for std::cout and std::cin

int main()
{
    std::cout << "Enter two numbers separated by a space: ";

    int x{ }; // define variable x to hold user input (and zero-initialize it)
    int y{ }; // define variable y to hold user input (and zero-initialize it)
    std::cin >> x >> y; // get two numbers and store in variable x and y respectively

    std::cout << "You entered " << x << " and " << y << '\n';

    return 0;
}
```

这将产生输出：

我们将在以后的课程中讨论std:：cin如何处理无效输入（8.17--std:∶cin和处理无效输入）。现在，只需知道std:：cin将尽可能多地提取，并且任何无法提取的输入字符都将留给以后的提取尝试。

{{< alert success >}}
**最佳做法**

对于是否有必要在通过另一个源（例如，std:：cin）为变量提供用户提供的值之前立即初始化变量，存在一些争议，因为用户提供的数值只会覆盖初始化值。根据我们之前的建议，即变量应始终初始化，最佳实践是首先初始化变量。

{{< /alert >}}

{{< alert success >}}
**对于高级读者**

C++I/O库不提供一种在用户不必按enter键的情况下接受键盘输入的方法。如果这是您想要的，则必须使用第三方库。对于控制台应用程序，我们建议使用pdcurses、FXTUI、cpp terminal或notcurses。许多图形用户界面库都有自己的函数来完成这类事情。

{{< /alert >}}

***
## 总结

新程序员通常会混淆std:：cin、std:∶cout、插入操作符（<<）和提取操作符（>>）。下面是一种简单的记忆方法：

1. std:：cin和std:：cout始终位于语句的左侧。
2. std:：cout用于输出值（cout=字符输出）
3. std:：cin用于获取输入值（cin=字符输入）
4. <<与std:：cout一起使用，并显示数据移动的方向（如果std:∶cout表示控制台，则输出数据从变量移动到控制台）。std:：cout<<4将值4移动到控制台
5. >>与std:：cin一起使用，并显示数据移动的方向（如果std:∶cin表示键盘，则输入数据从键盘移动到变量）。std:：cin>>x将用户输入的值从键盘移动到x中


我们将在第1.9课——文字和操作符简介中更多地讨论操作符。

***
## 测验时间

