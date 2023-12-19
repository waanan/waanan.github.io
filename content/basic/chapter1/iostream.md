---
title: "iostream:cout、cin和endl简介"
date: 2023-10-09T20:06:10+08:00
---

本课中，将讨论在Hello world程序中使用的std::cout。使用它输出文本Hello world！到控制台。此外，讲解如何使用std::cin，如何从用户获得输入，使程序更具交互性。

***
## 输入/输出库

输入/输出库（io库）是C++标准库中处理基本输入和输出的一部分。使用该库中的功能从键盘获取输入，并将数据输出到控制台。iostream的io部分表示输入（input）/输出（output）。

使用iostream库中定义的功能，需在代码文件顶部引入对应的头文件。

```C++
#include <iostream>

// 后续的代码可以使用iostream的函数
```

***
## std::cout

iostream库包含一些预定义的变量。最有用的是std::cout，将数据发送到控制台，打印文本。cout代表“字符输出”(character output)。

下面是之前的Hello world程序：

```C++
#include <iostream> // 之后可以使用 std::cout

int main()
{
    std::cout << "Hello world!"; // 打印 Hello world! 到控制台

    return 0;
}
```

包含了iostream，以便访问std::cout。主函数中，使用std::cout和插入操作符（<<）来发送文本Hello world！到打印的控制台。

std::cout不仅打印文本，还可打印数字：

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

还可用于打印变量的值：

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

要在同一行上打印多个内容，可在单个语句中多次使用插入运算符（<<）来连接多个输出。例如：

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

另一个例子，在同一语句中打印文本和变量和值：

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

结果可能令你惊讶：

```C++
Hi!My name is Alex.
```

单独的输出语句不会在控制台上产生单独的输出行。

如果想将单独的输出行打印到控制台，需要告诉控制台将光标移动到下一行。

一种方法是使用std::endl。当使用std::cout输出时，std::endl将换行字符打印到控制台（光标会转到下一行的开头）。在这种情况下，endl代表“一行结束，换行”。

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

想象在游乐园坐过山车的场景。乘客出现（以可变速度）排队。列车定期到达并登机（达到列车最大容量）。当列车满载，或时间推移时，列车与一批乘客一起出发，骑乘开始。不能登上当前列车的乘客要等待下一班列车。

这类似于C++中如何处理发送到std::cout的输出。程序中的语句请求将输出发送到控制台。该输出不会立即发送到控制台。而是，请求的输出“进入队列”，并存储在预留的内存区域（称为缓冲区）中。定期刷新缓冲区的数据输出到控制台。

意味着，如果程序在刷新缓冲区之前崩溃、中止或暂停（例如，出于调试目的），缓冲区内到数据不会输出到外部。


{{< alert success >}}
**关键点**

缓冲输出的反义词是无缓冲输出。对于无缓冲输出，每个单独的输出请求直接发送到输出设备。

将数据写入缓冲区通常很快，而将数据传输到输出设备则相对较慢。当存在多个输出请求时，缓冲可以最大限度地减少需要执行的慢速传输的数量，显著提高性能。

{{< /alert >}}

***
## std::endl vs "\n"

相比于输出"\n"换行,用std::endl有点低效。因为它实际上执行两项工作：将光标移动到控制台的下一行，并刷新缓冲区。当文本写入控制台时，通常不会刷新每行末尾的缓冲区。系统定期刷新更有效。

因此，首选用"\n"字符。"\n"字符将光标移动到控制台下一行，但不刷新缓冲区。

下面是以两种不同方式使用"\n"的示例：

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

打印：

```C++
x is equal to: 5
And that's all, folks!
```

当嵌入双引号的文本时，不需额外引号。

后续字符的课程，将详细讨论“\n”是什么。

***
## std::cin

std::cin是iostream库中另一预定义变量。std::cout使用插入操作符（<<）将数据打印到控制台，std:∶cin（代表字符输入, character input）使用提取操作符（>>）从键盘读取输入。输入存储在变量中。

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

编译此程序并运行它。程序运行时，第5行将打印"Enter a number: "。到第8行时，等待输入。输入一个数字（并按enter），输入的数字赋值给变量x。第10行，程序打印"You entered "，和刚才输入的数字。

例如（输入了4）：

```C++
Enter a number: 4
You entered 4
```

这是一种从用户获得键盘输入的简单方法，后面许多示例也会使用。

正如可在单行中输出多个文本位一样，也可在单行中输入多个值：

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

以后课程中会讨论std::cin如何处理无效输入。现在，只需知道std::cin尽可能多提取，且无法提取的输入字符将在后续提取。

***
## 总结

新手通常会混淆std::cin、std::cout、插入操作符（<<）和提取操作符（>>）。一种简单的记忆方法：

1. std::cin和std::cout始终位于语句的左侧。
2. std::cout用于输出值（cout=字符输出）
3. std::cin用于获取输入值（cin=字符输入）
4. <<与std::cout一起使用，并显示数据移动的方向（如果std:∶cout表示控制台，则输出数据从变量移动到控制台）。std::cout<<4将值4移动到控制台
5. >>与std::cin一起使用，并显示数据移动的方向（如果std:∶cin表示键盘，则输入数据从键盘移动到变量）。std::cin>>x将用户输入值从键盘移动到x中

***

{{< prevnext prev="/basic/chapter1/variable-init-assign/" next="/basic/chapter1/uninit-variable/" >}}
1.3 变量初始化和赋值
<--->
1.5 未初始化的变量及未定义的行为
{{< /prevnext >}}
