---
title: "预处理器简介"
date: 2023-10-09T20:06:10+08:00
---

在编译项目时，您可能希望编译器完全按照您编写的代码文件编译每个代码文件。事实并非如此。

相反，在编译之前，每个代码（.cpp）文件都要经过预处理阶段。在这个阶段，一个名为预处理器的程序对代码文件的文本进行各种更改。预处理器实际上不会修改原始代码文件，预处理器所做的所有更改都是临时发生在内存中或使用临时文件。

预处理器所做的大多数工作都相当乏味。例如，它去除注释，并确保每个代码文件以换行结束。然而，预处理器确实有一个非常重要的作用：它会处理#include指令。

预处理器完成对代码文件的处理，处理的结果称为翻译单元。翻译单元是编译器随后编译的基本单元。

{{< alert success >}}
**旁白**

在历史上，预处理器是一个独立于编译器的程序，但在现代编译器中，预处理器可以直接构建到编译器本身中。

{{< /alert >}}

{{< alert success >}}
**相关内容**

预处理、编译和链接的整个过程称为翻译。

如果你好奇，这里有一个[翻译阶段](https://en.cppreference.com/w/cpp/language/translation_phases)的列表。在编写时，预处理包括阶段1到4，编译是阶段5到7。

{{< /alert >}}

***
## 预处理指令

当预处理器运行时，它扫描代码文件（从上到下），查找预处理器指令。预处理器指令是以#符号开头、以换行符（不是分号）结尾的指令。这些指令告诉预处理器执行某些文本操作任务。注意，预处理器不理解C++语法——相反，它有自己的语法（在某些情况下类似于C++语法，在其他情况下则不太类似）。

在本课中，我们将学习一些最常见的预处理器指令。

{{< alert success >}}
**作为旁白…**

使用指令（在第2.9课中介绍——命名冲突和名称空间介绍）不是预处理器指令（因此不由预处理器处理）。因此，虽然术语指令通常意味着预处理器指令，但情况并不总是如此。

{{< /alert >}}

***
## #包括

您已经看到了#include指令的作用（通常是#incluse<iostream>）。当您#include文件时，预处理器将#include指令替换为所包含文件的内容。然后对包含的内容进行预处理（这可能导致递归地预处理额外的#includes），然后预处理文件的其余部分。

考虑以下程序：

```C++
#include <iostream>

int main()
{
    std::cout << "Hello, world!\n";
    return 0;
}
```

当预处理器在此程序上运行时，预处理器将用名为“iostream”的文件的内容替换#include<iostream>，然后预处理包含的内容和文件的其余部分。

一旦预处理器完成了对代码文件和所有#包含内容的处理，结果就称为翻译单元。翻译单元是发送给编译器进行编译的单元。

由于#include几乎专用于包括头文件，因此我们将在下一课（讨论头文件时）中更详细地讨论#incl包括。

{{< alert success >}}
**关键洞察力**

翻译单元既包含来自代码文件的已处理代码，也包含来自所有#included文件的处理代码。

{{< /alert >}}

***
## 宏定义

#define指令可用于创建宏。在C++中，宏是一条规则，定义如何将输入文本转换为替换输出文本。

宏有两种基本类型：类对象宏和类函数宏。

类函数宏的行为类似于函数，并具有类似的用途。它们的使用通常被认为是不安全的，它们可以做的任何事情都可以由正常功能完成。

类对象宏可以用两种方法之一定义：

顶部定义没有替换文本，而底部定义有。由于这些是预处理器指令（不是语句），请注意，两种形式都没有以分号结尾。

宏的标识符使用与普通标识符相同的命名规则：它们可以使用字母、数字和下划线，不能以数字开头，并且不应以下划线开头。按照惯例，宏名称通常都是大写的，由下划线分隔。

***
## 具有替换文本的类对象宏

当预处理器遇到该指令时，标识符的任何进一步出现都将替换为substitution_text。标识符传统上是用所有大写字母键入的，使用下划线表示空格。

考虑以下程序：

```C++
#include <iostream>

#define MY_NAME "Alex"

int main()
{
    std::cout << "My name is: " << MY_NAME << '\n';

    return 0;
}
```

预处理器将上述内容转换为以下内容：

```C++
// The contents of iostream are inserted here

int main()
{
    std::cout << "My name is: " << "Alex" << '\n';

    return 0;
}
```

它在运行时打印输出。我的名字是：亚历克斯。

具有替换文本的类对象宏（在C中）用作将名称分配给文本的方法。这不再是必要的，因为C++中提供了更好的方法。具有替换文本的类对象宏现在通常只能在旧代码中看到。

我们建议完全避免这些类型的宏，因为有更好的方法来做这类事情。我们在第4.13课中对此进行了更多的讨论——常量变量和符号常量。

***
## 无替换文本的类对象宏

类对象宏也可以在没有替换文本的情况下定义。

例如：

```C++
#define USE_YEN
```

这种形式的宏的工作方式与您可能期望的一样：标识符的任何进一步出现都将被删除，并且不替换任何内容！

这可能看起来非常无用，并且对于进行文本替换也是无用的。然而，这并不是这种形式的指令通常用于的目的。我们稍后将讨论此形式的用法。

与具有替换文本的类对象宏不同，这种形式的宏通常被认为可以使用。

***
## 条件编译

条件编译预处理器指令允许您指定在什么条件下某些东西将编译或不编译。有许多不同的条件编译指令，但我们将只介绍到目前为止使用最多的三个：#ifdef、#ifndef和#endif。

#ifdef预处理器指令允许预处理器检查以前是否#定义了标识符。如果是，则编译#ifdef和匹配的#endif之间的代码。如果不是，则忽略代码。

考虑以下程序：

```C++
#include <iostream>

#define PRINT_JOE

int main()
{
#ifdef PRINT_JOE
    std::cout << "Joe\n"; // will be compiled since PRINT_JOE is defined
#endif

#ifdef PRINT_BOB
    std::cout << "Bob\n"; // will be excluded since PRINT_BOB is not defined
#endif

    return 0;
}
```

由于PRINT_JOE已定义#，因此将编译行std:：cout<<“JOE\n”。由于尚未#定义PRINT_BOB，因此将忽略行std:：cout<<“BOB\n”。

#ifndef与ifdef相反，它允许您检查标识符是否尚未定义。

```C++
#include <iostream>

int main()
{
#ifndef PRINT_BOB
    std::cout << "Bob\n";
#endif

    return 0;
}
```

该程序打印“Bob”，因为PRINT_Bob从未#定义。

代替#ifdef PRINT_BOB和#ifndef PRINT_TBOB，您还将看到#if defined（PRINT_BOB）和#if！定义（PRINT_BOB）。它们的作用是相同的，但使用了稍微更具C++风格的语法。

***
## #如果为0

条件编译的另一个常见用法是使用#if 0排除正在编译的代码块（就像它在注释块内一样）：

```C++
#include <iostream>

int main()
{
    std::cout << "Joe\n";

#if 0 // Don't compile anything starting here
    std::cout << "Bob\n";
    std::cout << "Steve\n";
#endif // until this point

    return 0;
}
```

上面的代码只打印“Joe”，因为#if0预处理器指令将“Bob”和“Steve”排除在编译之外。

这提供了一种方便的方法来“注释掉”包含多行注释的代码（由于多行注释不可嵌套，因此不能使用另一个多行注释注释掉）：

```C++
#include <iostream>

int main()
{
    std::cout << "Joe\n";

#if 0 // Don't compile anything starting here
    std::cout << "Bob\n";
    /* Some
     * multi-line
     * comment here
     */
    std::cout << "Steve\n";
#endif // until this point

    return 0;
}
```

要临时重新启用包装在#if 0中的代码，可以将#if 0:

```C++
#include <iostream>

int main()
{
    std::cout << "Joe\n";

#if 1 // always true, so the following code will be compiled
    std::cout << "Bob\n";
    /* Some
     * multi-line
     * comment here
     */
    std::cout << "Steve\n";
#endif

    return 0;
}
```

***
## 类对象宏不影响其他预处理器指令

现在您可能会想：

```C++
#define PRINT_JOE

#ifdef PRINT_JOE
// ...
```

既然我们将PRINT_JOE定义为空，为什么预处理器没有用空来替换#ifdef PRINT_JOE中的PRINT_JOE？

宏仅导致普通代码的文本替换。忽略其他预处理器命令。因此，#ifdef PRINT_JOE中的PRINT_JOE将被保留。

例如：

```C++
#define FOO 9 // Here's a macro substitution

#ifdef FOO // This FOO does not get replaced because it’s part of another preprocessor directive
    std::cout << FOO << '\n'; // This FOO gets replaced with 9 because it's part of the normal code
#endif
```

然而，预处理器的最终输出根本不包含指令——它们都是在编译之前解析/剥离的，因为编译器不知道如何处理它们。

***
## #的范围定义了

指令在编译之前解析，以逐个文件为基础，从上到下。

考虑以下程序：

```C++
#include <iostream>

void foo()
{
#define MY_NAME "Alex"
}

int main()
{
	std::cout << "My name is: " << MY_NAME << '\n';

	return 0;
}
```

尽管#define MY_NAME“Alex”似乎是在函数foo中定义的，但预处理器不会注意到，因为它不理解C++概念（如函数）。因此，该程序的行为与#define MY_NAME“Alex”在函数foo之前或之后定义的程序相同。为了可读性，通常需要在函数外部#define标识符。

一旦预处理器完成，该文件中定义的所有标识符都将被丢弃。这意味着指令仅从定义点到定义它们的文件末尾有效。在一个代码文件中定义的指令不会影响同一项目中的其他代码文件。

考虑以下示例：

功能.cpp：

```C++
#include <iostream>

void doSomething()
{
#ifdef PRINT
    std::cout << "Printing!\n";
#endif
#ifndef PRINT
    std::cout << "Not printing!\n";
#endif
}
```

主.cpp：

```C++
void doSomething(); // forward declaration for function doSomething()

#define PRINT

int main()
{
    doSomething();

    return 0;
}
```

上述程序将打印：

尽管PRINT是在main.cpp中定义的，但这对function.cpp的任何代码都没有任何影响（PRINT只是从定义点到main.cpp末尾定义的#）。这在我们在以后的课程中讨论页眉保护时将是非常重要的。

***

{{< prevnext prev="/basic/chapter2/namespace/" next="/" >}}
2.8 命名冲突和名称空间简介
<--->
主页
{{< /prevnext >}}
