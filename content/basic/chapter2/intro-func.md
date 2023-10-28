---
title: "函数简介"
date: 2023-10-09T20:06:10+08:00
---

在上一章中，我们将函数定义为按顺序执行的语句的集合。虽然这肯定是正确的，但该定义并没有提供太多关于函数为什么有用的见解。让我们更新一下我们的定义：函数是一个可重用的语句序列，旨在完成特定的工作。

每个可执行程序都必须有一个名为main的函数（这是程序在运行时开始执行的位置）。然而，随着程序开始变得越来越长，将所有代码放在主函数中变得越来越难以管理。函数为我们提供了一种方法，可以将程序划分为较小的模块，这些模块更易于组织、测试和使用。C++标准库附带了许多已经编写好的函数供您使用——然而，编写自己的函数也是常见的。您自己编写的函数称为用户定义函数。

考虑一个现实生活中的场景：正在读书时，需要打电话。在书中放了一个书签，打了电话，当完成电话通话后，回到书签的地方，继续读书。

C++程序以相同的方式工作。当程序遇到函数调用时，它将在一个函数内顺序执行语句。函数调用是一个表达式，它告诉CPU中断当前函数并执行另一个函数。CPU在当前执行点“放置书签”，然后调用（执行）函数。当被调用的函数结束时，CPU返回到它标记的点，并继续执行。

发起函数调用的函数是调用者，而被调用的函数则是被调用者或被调用函数。

***
## 用户定义函数的示例

首先，让我们从定义函数的最基本语法开始。在接下来的几节课中，所有用户定义函数都将采用以下形式：

```C++
返回值类型 函数名() // 函数头，告知编译器函数的存在
{
    // 函数体
}
```

第一行非正式地称为函数头，它告诉编译器函数的存在、函数的名称以及我们将在以后的课程中介绍的一些其他信息（如返回类型和参数类型）。

1. 在本课中，我们将使用int（对于函数main（））或void的返回值类型。在下一课中，我们将更多地讨论返回类型和返回值。现在，您可以忽略这些。
2. 就像变量有名称一样，用户定义函数也有名称。「函数名」是用户定义函数的名称（标识符）。
3. 标识符后面的括号告诉编译器我们正在定义函数。

中间的花括号和语句称为函数体。这里是决定函数执行什么操作的语句。

下面是一个示例程序，展示了如何定义和调用新函数：

```C++
#include <iostream>

// 用户自定义函数 doPrint()
void doPrint() // doPrint() 是被调函数
{
    std::cout << "In doPrint()\n";
}

// 定义函数 main()
int main()
{
    std::cout << "Starting main()\n";
    doPrint(); // 去执行函数 doPrint().  main() 是调用者.
    std::cout << "Ending main()\n"; // doPrint() 执行结束后，返回这里继续执行

    return 0;
}
```

该程序产生以下输出：
```C++
Starting main()
In doPrint()
Ending main()
```

该程序在函数main开始执行，要执行的第一行打印Starting main()。

main中的第二行是对函数doPrint的函数调用。我们通过在函数名后面附加一对括号来调用函数doPrint，如：doPrint()。请注意，如果忘记括号，则程序可能无法编译。

因为进行了函数调用，所以main中语句的执行被挂起，并且执行跳转到被调用函数doPrint的顶部。doPrint中的第一行（也是唯一一行）在doPrint() 中打印。当doPrint终止时，执行返回给调用方（main函数），并从停止的点恢复。因此，在main中执行的下一条语句打印Ending main()。

{{< alert success >}}
**警告**

当进行函数调用时，不要忘记在函数名后面包含括号()。

{{< /alert >}}

***
## 多次调用函数

函数的一个有用之处是它们可以被多次调用。下面的程序演示了这一点：

```C++
#include <iostream>
void doPrint()
{
    std::cout << "In doPrint()\n";
}

int main()
{
    std::cout << "Starting main()\n";
    doPrint(); // doPrint() 第一次调用
    doPrint(); // doPrint() 第二次调用
    std::cout << "Ending main()\n";

    return 0;
}
```

该程序产生以下输出：
```C++
Starting main()
In doPrint()
In doPrint()
Ending main()
```

由于main调用doPrint两次，doPrint执行两次，In doPrint() 打印两次（每次调用一次）。

***
## 被调用的函数,再调用函数

您已经看到函数main可以调用另一个函数（例如上面例子中的函数doPrint）。任何函数都可以调用任何其他函数。在下面的程序中，函数main调用函数doA，该函数调用函数doB：

```C++
#include <iostream>

void doB()
{
    std::cout << "In doB()\n";
}


void doA()
{
    std::cout << "Starting doA()\n";

    doB();

    std::cout << "Ending doA()\n";
}

// Definition of function main()
int main()
{
    std::cout << "Starting main()\n";

    doA();

    std::cout << "Ending main()\n";

    return 0;
}
```

该程序产生以下输出：
```C++
Starting main()
Starting doA()
In doB()
Ending doA()
Ending main()
```


***
## 不支持嵌套函数定义

与其他一些编程语言不同，在C++中，函数不能在其他函数中定义。以下程序不合法：

```C++
#include <iostream>

int main()
{
    void foo() // 不合法，不允许再函数中定义函数
    {
        std::cout << "foo!\n";
    }

    foo();
    return 0;
}
```

编写上述程序的正确方法是：

```C++
#include <iostream>

void foo()
{
    std::cout << "foo!\n";
}

int main()
{
    foo();
    return 0;
}
```

{{< alert success >}}
**注**

“foo”是一个无意义的词，当名称对某个概念的演示不重要时，它通常用作函数或变量的占位符名称。这样的词被称为元语法变量（尽管在通用语言中，它们通常被称为“占位符名称”，因为没有人能记住术语“元语法变量”）。C++中其他常见的元语法变量包括“bar”、“baz”和以“oo”结尾的3个字母的单词，如“goo”、“moo”和“boo”）。

{{< /alert >}}

***
{{< prevnext prev="/basic/chapter1/summary/" next="/basic/chapter2/func-ret/" >}}
第1章总结
<--->
函数返回值
{{< /prevnext >}}