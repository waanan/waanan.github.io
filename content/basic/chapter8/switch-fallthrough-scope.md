---
title: "switch fallthrough机制与作用域"
date: 2024-01-02T10:33:49+08:00
---

在上一课中，我们提到标签下的每一组语句都应该以break语句或return语句结尾。

在本课中，我们将探索原因，并讨论一些有时会绊倒新程序员的switch作用域问题。

***
## Fallthrough机制

当switch表达式与case标签或可选的默认标签匹配时，执行从匹配标签之后的第一条语句开始。然后继续按顺序执行，直到发生以下终止条件之一：

1. switch代码块结束
2. 另一个控制流语句（通常是break或return）导致退出代码块或函数。
3. 其它打断程序正常控制流的事情（操作系统杀死了对应的进程等其它原因）

请注意，另一个case标签的存在不是这些终止条件之一——因此，如果没有中断或返回，执行将溢出到后续的case情况中。

下面是一个显示此行为的程序：

```C++
#include <iostream>

int main()
{
    switch (2)
    {
    case 1: // 不匹配
        std::cout << 1 << '\n'; // 跳过
    case 2: // 匹配
        std::cout << 2 << '\n'; // 从这里开始执行
    case 3:
        std::cout << 3 << '\n'; // 这里也会执行
    case 4:
        std::cout << 4 << '\n'; // 这里也会执行
    default:
        std::cout << 5 << '\n'; // 这里也会执行
    }

    return 0;
}
```

该程序输出以下内容：

```C++
2
3
4
5
```

这可能不是我们想要的！当执行从标签下的语句流到后续标签下的语句时，这称为fallthrough。

由于很少需要有意进行fallthrough，因此许多编译器和代码分析工具将fallthrough标记为警告。

{{< alert success >}}
**警告**

一旦case或默认标签下的语句开始执行，它们将溢出（fallthrough）到后续的case中。Break或return语句通常用于防止这种情况。

{{< /alert >}}

***
## [[fallthrough]]属性

可以通过注释，来告诉其它开发人员，switch的fallthrough行为是有意设计的。虽然这对其他开发人员有效，但编译器和代码分析工具不知道如何解释注释，因此不会消除警告。

为了帮助解决这个问题，C++17添加了一个名为[[fallthrough]]的新属性。

属性是一种现代C++功能，它允许程序员向编译器提供有关代码的一些附加数据。要指定属性，请将属性名称放在双括号之间。属性不是语句——相反，它们几乎可以在上下文相关的任何地方使用。

下面的例子中，[[fallthrough]]属性修改null语句，以指示fallthrough是有意的（不应触发任何警告）：

```C++
#include <iostream>

int main()
{
    switch (2)
    {
    case 1:
        std::cout << 1 << '\n';
        break;
    case 2:
        std::cout << 2 << '\n'; // 这里开始执行
        [[fallthrough]]; // 有意的进行 fallthrough -- 注意这里的分号代表空语句
    case 3:
        std::cout << 3 << '\n'; // 这里也会执行到
        break;
    }

    return 0;
}
```

该程序打印：

```C++
2
3
```

并且它不应该生成任何关于fallthrough的警告。

{{< alert success >}}
**最佳实践**

使用[[fallthrough]]属性（以及null语句）来指示有意的fallthrough。

{{< /alert >}}

***
## 连续case标签

您可以使用逻辑OR运算符将多个测试组合到单个语句中：

```C++
bool isVowel(char c)
{
    return (c=='a' || c=='e' || c=='i' || c=='o' || c=='u' ||
        c=='A' || c=='E' || c=='I' || c=='O' || c=='U');
}
```

这里c被多次求值。

通过按顺序放置多个case标签，可以使用switch语句执行类似的操作：

```C++
bool isVowel(char c)
{
    switch (c)
    {
        case 'a': // if c is 'a'
        case 'e': // or if c is 'e'
        case 'i': // or if c is 'i'
        case 'o': // or if c is 'o'
        case 'u': // or if c is 'u'
        case 'A': // or if c is 'A'
        case 'E': // or if c is 'E'
        case 'I': // or if c is 'I'
        case 'O': // or if c is 'O'
        case 'U': // or if c is 'U'
            return true;
        default:
            return false;
    }
}
```

请记住，执行从匹配的case标签之后的第一条语句开始。case标签不是语句（它们是标签），因此它们不算数。

上面程序中所有case语句之后的第一个语句都返回true，因此如果任何case标签匹配，函数将返回true。

因此，我们可以“堆叠”case标签，以使所有这些case标签在之后共享相同的语句集。这不被认为是fallthrough行为，因此这里不需要使用注释或[[fallthrough]]。

***
## switch语句中case的作用域

使用if语句，在if条件之后只能有一条语句，并且该语句被认为隐式地位于代码块内：

```C++
if (x > 10)
    std::cout << x << " is greater than 10\n"; // 该语句被认为隐式地位于代码块内
```

然而，对于switch语句，标签后的语句都作用于switch块。不会创建隐式块。

```C++
switch (1)
{
    case 1: // 不会创建隐式块
        foo(); // 在switch的作用域内，而不是case 1内
        break; // 在switch的作用域内，而不是case 1内
    default:
        std::cout << "default case\n";
        break;
}
```

在上面的示例中，case 1 标签和default标签之间的2条语句的作用域是switch块的一部分，而不是case 1 隐含的代码块。

***
## case语句中的变量声明和初始化

您可以在case标签之前和之后声明或定义（但不能初始化）switch语句内的变量：

```C++
switch (1)
{
    int a; // okay: case标签之前可以声明变量
    int b{ 5 }; // 不合法: case 标签之前，不可以初始化变量

    case 1:
        int y; // okay 但不推荐
        y = 4; // okay: 赋值语句可以
        break;

    case 2:
        int z{ 4 }; // 不合法: 后面还有case标签，不允许初始化变量
        y = 5; // okay: y 在上面声明，所以这里可以赋值
        break;

    case 3:
        break;
}
```

在 case 1 中定义了变量y，在 case 2 中使用了它。switch内的所有语句都被视为同一作用域的一部分。因此，在 case 1 内声明或定义的变量可以在以后使用。

然而，变量的初始化，需要在运行时执行（因为需要将初始值设置给变量）。如果后续还有case标签，则不允许初始化变量（因为初始化可能被跳过，这将使变量未初始化）。在第一个case标签之前不允许初始化，因为这些语句永远不会执行，switch语句无法指定到它们。

如果case标签内需要定义和初始化新变量，最佳实践是在case语句下的显式块内进行定义和初始化：

```C++
switch (1)
{
    case 1:
    { // 这里有一个显示的代码块
        int x{ 4 }; // okay, 变量在一个新的代码块内初始化
        std::cout << x;
        break;
    }
    default:
        std::cout << "default case\n";
        break;
}
```

{{< alert success >}}
**最佳实践**

如果定义case语句中使用的变量，请在case内的显示代码块中定义。

{{< /alert >}}

***

{{< prevnext prev="/basic/chapter8/switch/" next="/basic/chapter8/goto/" >}}
8.4 Switch语句基础
<--->
8.6 goto语句
{{< /prevnext >}}
