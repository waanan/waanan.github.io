---
title: "预处理器简介"
date: 2023-10-09T20:06:10+08:00
---

编译项目时，希望编译器按照编写代码文件编译每个文件。事实并非如此。

相反，在编译之前，每个代码（.cpp）文件要经过预处理阶段。在这个阶段，预处理器对代码文件进行更改。预处理器不会修改原始代码文件，所做的更改都是临时发生在内存中或使用临时文件。

预处理器所做的大多数工作都很乏味。例如，去除注释，将每个代码文件以换行结束。然而，预处理器确实有一个非常重要的作用：它会处理#include指令。

预处理器完成对代码文件的处理，处理结果称为翻译单元。翻译单元是编译器随后编译的基本单元。

{{< alert success >}}
**旁白**

在历史上，预处理器是一个独立于编译器的程序，但在现代编译器中，预处理器可直接构建到编译器本身中。

{{< /alert >}}

{{< alert success >}}
**相关内容**

预处理、编译和链接的整个过程称为翻译。

如果你好奇，这里有一个[翻译阶段](https://en.cppreference.com/w/cpp/language/translation_phases)的列表。在编写时，预处理包括阶段1到4，编译是阶段5到7。

{{< /alert >}}

***
## 预处理指令

预处理器运行时，扫描代码文件（从上到下），查找预处理指令。预处理指令是以#符号开头、以换行符（不是分号）结尾的指令。这些指令告诉预处理器执行某些文本操作任务。注意，预处理器不理解C++语法——相反，它有自己的语法（在某些情况下类似于C++语法，在其他情况下则不太类似）。

本课中，将学习一些常见的预处理指令。

{{< alert success >}}
**作为旁白…**

using namespace（在命名冲突和名称空间简介一节）不是预处理指令（不由预处理器处理）。

{{< /alert >}}

***
## include

了解了#include指令作用（一个常见的例子是#include \<iostream\>）。当#include文件时，预处理器将#include指令替换为所包含文件的内容。然后对包含内容进行预处理（可能导致递归地预处理其他的#include文件），然后处理文件的其余部分。

如下程序：

```C++
#include <iostream>

int main()
{
    std::cout << "Hello, world!\n";
    return 0;
}
```

预处理器运行此程序时，预处理器将用名为“iostream”的文件内容替换#include<iostream>，然后处理引入的内容和文件其余部分。

预处理器对代码文件和所有#包含内容的处理结果称为翻译单元。翻译单元是编译器编译的单元。

由于#include专用于处理头文件，下一课（讨论头文件时）中会更详细地讨论#include。

{{< alert success >}}
**关键点**

翻译单元既包含来自代码文件的代码，也包含所有#included文件的处理代码。

{{< /alert >}}

***
## 宏定义

#define指令用于创建宏。C++中，宏是一条规则，定义如何将输入文本转换为替换输出文本。

宏有两种基本类型：类对象宏和类函数宏。

类函数宏的行为类似于函数，并有类似的用途。使用它们通常是不安全的，它所做的事情都可由正常功能完成。

类对象宏可以用两种方法定义：

```C++
#define 标识符
#define 标识符 替换文本
```

第一个定义没有替换文本，第二个有。这些是预处理指令（不是语句），请注意，两种形式都没有以分号结尾。

宏的标识符与普通标识符使用相同的命名规则：可以使用字母、数字和下划线，不能以数字开头，且不以下划线开头。按照惯例，宏名称通常都是大写的，由下划线分隔。

***
## 具有替换文本的类对象宏

当预处理器遇到该指令时，后续标识符的每次出现都将替换为substitution_text。标识符传统上是用所有大写字母键入的，使用下划线表示空格。

考虑以下程序：

```C++
#include <iostream>

#define MY_NAME "Fly"

int main()
{
    std::cout << "My name is: " << MY_NAME << '\n';

    return 0;
}
```

预处理器将上述转换为以下内容：

```C++
// iostream 中的内容将会被替换到这里

int main()
{
    std::cout << "My name is: " << "Fly" << '\n';

    return 0;
}
```

运行时打印输出。"My name is: Fly"。

具有替换文本的类对象宏（在C中）用作将名称分配给文本。但C++中提供了更好的方法。具有替换文本的类对象宏只能在旧代码中看到。

建议避免这种类型的宏，因为有更好的方法实现。后续章节会讨论——常量变量和符号常量。

***
## 无替换文本的类对象宏

类对象宏也可以在没有替换文本的情况下定义。

例如：

```C++
#define USE_YEN
```

这种形式的宏的工作方式可能与期望一样：标识符任何进一步出现都将被删除，并且不替换任何内容！

这可能看起来无用，并且对于进行文本替换也是无用的。但这并不是此指令的使用场景。

与具有替换文本的类对象宏不同，这种形式的宏通常被认可使用。

***
## 条件编译

条件编译预处理器指令允许在指定条件下编译或不编译。有许多条件编译指令，只介绍目前使用最多的三个：#ifdef、#ifndef和#endif。

#ifdef预处理器指令允许预处理器检查以前是否#定义了标识符。如果是，则编译#ifdef和匹配的#endif之间的代码。如果不是，则忽略代码。

考虑以下程序：

```C++
#include <iostream>

#define PRINT_JOE

int main()
{
#ifdef PRINT_JOE
    std::cout << "Joe\n"; // PRINT_JOE被定义，这一行会被编译
#endif

#ifdef PRINT_BOB
    std::cout << "Bob\n"; // PRINT_BOB未被定义，这一行不会被编译
#endif

    return 0;
}
```

由于PRINT_JOE已定义，因此将编译行std::cout<<“JOE\n”。由于未定义PRINT_BOB，将忽略行std::cout << “BOB\n”。

#ifndef与ifdef相反，允许检查标识符是否未定义。

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

该程序打印“Bob”，因为PRINT_BOB未定义。

代替#ifdef PRINT_BOB 和#ifndef PRINT_BOB，还将看到#if defined(PRINT_BOB)和#if !defined(PRINT_BOB)。作用相同，只使用了更具C++风格的语法。

***
## #if 0

条件编译另一常见用法是使用#if 0排除不需编译的代码块（和使用注释块一样）：

```C++
#include <iostream>

int main()
{
    std::cout << "Joe\n";

#if 0 // 从这里开始的不编译
    std::cout << "Bob\n";
    std::cout << "Steve\n";
#endif // 到这里结束

    return 0;
}
```

上面的代码只打印“Joe”，因为#if 0预处理指令将“Bob”和“Steve”排除在编译之外。

这提供了一种方便的方法来“注释掉”包含多行注释的代码（由于多行注释不可嵌套，因此不能使用另一个多行注释来注释）：

```C++
#include <iostream>

int main()
{
    std::cout << "Joe\n";

#if 0 // 从这里开始的不编译
    std::cout << "Bob\n";
    /* 一些
     * 多行
     * 注释
     */
    std::cout << "Steve\n";
#endif // 到这里结束

    return 0;
}
```

要临时重新启用包装在#if 0中的代码，可以将#if 0改成 #if 1。

```C++
#include <iostream>

int main()
{
    std::cout << "Joe\n";

#if 1 // 永远为true, 所以下面的代码会被编译
    std::cout << "Bob\n";
    /* 一些
     * 多行
     * 注释
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

既然将PRINT_JOE定义为空，为什么预处理器没有用空来替换#ifdef PRINT_JOE中的PRINT_JOE？

宏仅导致普通代码的文本替换。忽略其他预处理器命令。因此，#ifdef PRINT_JOE中的PRINT_JOE将被保留。

例如：

```C++
#define FOO 9 // 宏定义

#ifdef FOO // 这里的预处理指令不会受影响
    std::cout << FOO << '\n'; // FOO 被替换为 9，因为这里是普通代码 
#endif
```

预处理器的最终输出不包含预处理指令——会在编译之前解析，因为编译器不知道如何处理。

***
## #define的作用范围

#define 在编译之前解析，从文件中，从上到下，逐个文件进行处理。

考虑以下程序：

```C++
#include <iostream>

void foo()
{
#define MY_NAME "Fly"
}

int main()
{
	std::cout << "My name is: " << MY_NAME << '\n';

	return 0;
}
```

尽管#define MY_NAME "Fly" 是在函数foo中定义的，但预处理器不理解C++概念（如函数）。因此，该程序的行为与#define MY_NAME "Fly" 在函数foo之前或之后定义的程序相同。为了可读性，通常需要在函数外部设置 #define。

一旦预处理器处理完成，该文件中定义的所有#define定义的标识符将被丢弃。意味着指令仅从定义点到定义它们的文件末尾有效。在一个代码文件中定义的指令不会影响同一项目中的其他代码文件。

考虑以下示例：

function.cpp：

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

main.cpp：

```C++
void doSomething(); // 前向声明 doSomething()

#define PRINT

int main()
{
    doSomething();

    return 0;
}
```

上述程序将打印：

```C++
Not printing!
```

PRINT是在main.cpp中定义的，对function.cpp的代码没有任何影响（PRINT只是从定义点到main.cpp末尾定义有效）。

***

{{< prevnext prev="/basic/chapter2/namespace/" next="/basic/chapter2/header-file/" >}}
2.8 命名冲突和名称空间简介
<--->
2.10 头文件
{{< /prevnext >}}
