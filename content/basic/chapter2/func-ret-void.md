---
title: "无返回值函数"
date: 2023-10-09T20:06:10+08:00
---

在之前的课程中，我们指出函数定义的语法如下所示：

```C++
返回值类型 函数名() // 函数头，告知编译器函数的存在
{
    // 函数体
}
```

在本课中，我们将探索返回类型为void的函数。

***
## 无返回值

函数不需要将值返回给调用方。要告诉编译器函数不需要返回值，使用返回类型void。例如：

```C++
#include <iostream>

// void 意味着函数不返回值给调用方
void printHi()
{
    std::cout << "Hi" << '\n';

    // 不返回数据，所以不需要return 语句
}

int main()
{
    printHi(); // 无需接收返回值

    return 0;
}
```

在上面的例子中，printHi函数有一个有用的行为（它打印“Hi”），但它不需要向调用者返回任何内容。因此，printHi被赋予void返回类型。

当main调用printHi时，执行printHi中的代码，并打印“Hi”。在printHi结束时，控制返回main，程序继续。

***
## Void函数不需要return语句

void函数将在函数结束时自动返回给调用方。不需要return语句。

可以在void函数中使用return语句（不带返回值）——这样的语句将导致函数在执行return语句的点返回给调用方。这与函数末尾发生的事情是相同的。将空返回语句放在void函数的末尾是多余的：

```C++
#include <iostream>

// void 意味着函数不返回值给调用方
void printHi()
{
    std::cout << "Hi" << '\n';

    return; // 告诉编译器返回 -- 该语句是多余的
}

int main()
{
    printHi();

    return 0;
}
```

{{< alert success >}}
**最佳实践**

不需要要将return语句放在返回void的函数的末尾。

{{< /alert >}}

***
## void函数不能在需要值的表达式中使用

某些类型的表达式需要值。例如：

```C++
#include <iostream>

int main()
{
    std::cout << 5;
    std::cout << ;  // 编译失败, 这里需要有一个能打印的值

    return 0;
}
```

在上述程序中，需要在std::cout<<的右侧提供要打印的值。如果没有提供值，编译器将产生语法错误。由于对std::cout的第二次调用没有提供要打印的值，因此这会导致错误。

现在考虑以下程序：

```C++
#include <iostream>

void printHi()
{
    std::cout << "Hi" << '\n';
}

int main()
{
    printHi();

    std::cout << printHi(); // 编译失败

    return 0;
}
```

对printHi() 的第一个调用是在不需要值的环境中调用的。由于函数不返回值，因此可以正常运行。

对函数printHi() 的第二个函数调用甚至无法编译。函数printHi具有void返回类型，这意味着它不返回值。然而，该语句试图将printHi的返回值发送到std::cout。std::cout不知道如何处理此问题（它将输出什么值？）。因此，编译器会将其标记为错误。您需要注释掉这一行代码，以便使代码能够编译。

{{< alert success >}}
**提示**

一些语句需要提供值，而其他语句则不需要。

当我们单独调用函数时（例如，上面示例中的第一个printHi() ），我们需要的是函数的行为，而不是其返回值。在这种情况下，我们可以返回void，也可以有返回值、但忽略返回值。

当我们在需要值的上下文中调用函数时（例如，std::cout），必须提供值。在这种上下文中，我们只能调用有返回值的函数。

```C++
#include <iostream>

// 无返回值
void returnNothing()
{
}

// 有返回值
int returnFive()
{
    return 5;
}

int main()
{
    // 在不需要返回值的上下文中调用函数
    returnNothing(); // 无返回值的函数
    returnFive();    // 有返回值的函数，返回值未使用

    // 在需要返回值的上下文中调用函数 (例如 std::cout)
    std::cout << returnFive();    // 使用函数返回值
    std::cout << returnNothing(); // 编译失败：无返回值

    return 0;
}
```

{{< /alert >}}

***
## 从void函数返回值导致编译错误

尝试从void函数中返回值将导致编译错误：

```C++
void printHi()
{
    std::cout << "In printHi()" << '\n';

    return 5; // 编译失败
}
```

***

{{< prevnext prev="/basic/chapter2/func-ret/" next="/basic/chapter2/func-arg/" >}}
2.1 函数返回值
<--->
2.3 函数参数简介
{{< /prevnext >}}
