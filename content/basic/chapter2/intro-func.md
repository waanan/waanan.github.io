---
title: "函数简介"
date: 2023-10-09T20:06:10+08:00
---

上一章中，函数为按顺序执行的语句集合。虽然是正确的，但该定义没有提供太多函数为什么有用的见解。更新一下函数的定义：函数是一个可重用的语句序列，旨在完成特定工作。

可执行程序都必须有一个名为main的函数（程序运行时开始执行的位置）。然而，随着程序变得越来越长，所有代码放在主函数中变得难以管理。函数提供了一种方法，将程序划分为较小模块，这些模块更易于组织、测试和使用。C++标准库附带了许多已编写好的函数供使用——然而，编写自己的函数也是常见的。编写的函数称为用户定义函数。

考虑一个现实生活中的场景：正在读书时，需要打电话。在书中放一个书签，打了电话，通话后，回到书签位置，继续读书。

C++程序以相同的方式工作。函数内顺序执行语句。函数调用是一个表达式，告诉CPU中断当前函数并执行另一个函数。CPU在当前执行点“放置书签”，然后调用（执行）函数。被调用的函数结束时，CPU返回到它标记的点，继续执行。

发起函数调用的函数是调用者，而被调用的函数是被调用者或被调用函数。

***
## 用户定义函数的示例

首先，从定义函数的基本语法开始。接下来几节课中，所有用户定义函数将采用以下形式：

```C++
返回值类型 函数名() // 函数头，告知编译器函数的存在
{
    // 函数体
}
```

第一行称为函数头，告诉编译器函数的存在、函数的名称及将在以后课程中介绍的一些其他信息（如返回类型和参数类型）。

1. 本课中，使用int（对于函数main（））或void的返回值类型。下一课中，将更多讨论返回类型和返回值。现在，可以忽略这些。
2. 就如变量有名称，用户定义函数也有名称。「函数名」是用户定义函数的名称（标识符）。
3. 标识符后面的括号告诉编译器在定义函数。

中间的花括号和语句称为函数体。决定函数执行操作的语句。

下面示例程序，展示如何定义和调用新函数：

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

程序在函数main开始执行，执行第一行打印Starting main()。

main中的第二行对函数doPrint函数调用。在函数名后附加一对括号来调用函数doPrint，如：doPrint()。注意，如果忘记括号，程序无法编译。

由于进行了函数调用，所以main中语句的执行被挂起，且执行跳转到被调用函数doPrint的顶部。doPrint中的第一行（也是唯一一行）在doPrint() 中打印。当doPrint终止时，执行返回给调用方（main函数），并从停止的点恢复。因此，在main中执行的下一条语句打印Ending main()。

{{< alert success >}}
**警告**

当进行函数调用时，不要忘记在函数名后包含括号()。

{{< /alert >}}

***
## 多次调用函数

函数的一个好处是可被多次调用。演示如下：

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

该程序输出：
```C++
Starting main()
In doPrint()
In doPrint()
Ending main()
```

由于main调用doPrint两次，doPrint执行两次，In doPrint() 打印两次（每次调用一次）。

***
## 被调用的函数,再调用函数

函数main可调用另一个函数（例如上面例子中的函数doPrint）。任何函数都可以调用任何其他函数。如下程序，函数main调用函数doA，doA调用函数doB：

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

与一些编程语言不同，C++中，函数不能在其他函数中定义。以下程序不合法：

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

正确方法是：

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

“foo”是一个无意义的词，当名称不重要时，“foo”用作函数或变量的占位符名称。这样的词被称为元语法变量（在通用语言中，通常被称为“占位符名称”，因为没有人能记住术语“元语法变量”）。C++中其他常见的元语法变量包括“bar”、“baz”和以“oo”结尾的3个字母的单词，如“goo”、“moo”和“boo”）。

{{< /alert >}}

***

{{< prevnext prev="/basic/chapter1/summary/" next="/basic/chapter2/func-ret/" >}}
1.11 第1章总结
<--->
2.1 函数返回值
{{< /prevnext >}}
