---
title: "class简介"
date: 2024-04-09T13:02:20+08:00
---

在前一章中，我们介绍了结构体。它可以将多个成员变量绑定到单个对象（可以作为一个单元进行初始化和传递）。换句话说，结构体提供了一个方便的封装形式，来存储和移动相关的数据值。

考虑以下结构：

```C++
#include <iostream>

struct Date
{
    int day{};
    int month{};
    int year{};
};

void printDate(const Date& date)
{
    std::cout << date.day << '/' << date.month << '/' << date.year; // 设置 DMY 的格式
}

int main()
{
    Date date{ 4, 10, 21 }; // 使用聚合初始化
    printDate(date);        // 讲对象传递给函数

    return 0;
}
```

在上面的示例中，创建了一个Date对象，然后将其传递给打印日期的函数。该程序打印：

```C++
4/10/21
```

尽管结构体很有用，但有许多缺陷，在试图构建大型复杂程序（特别是由多个开发人员处理的程序）时，这些缺陷可能会带来挑战。

{{< alert success >}}
**提醒**

在本教程中，所有的结构体都是聚合类型。

{{< /alert >}}

***
## 数据状态有效性问题

结构体最大的问题，是没有办法确保结构体内的数据一定是有效的。在前面，我们学习过不变量的定义，即“在某个组件执行时必须为真的条件”。

在类类型（包括结构体、类和联合）的情况下，类不变量是一个条件，必须在对象的整个生存期内为真，以便对象保持有效状态。违反的类不变量的对象被称为处于无效状态，使用该对象可能会导致意外或未定义的行为。

首先，考虑以下结构体：

```C++
struct Pair
{
    int first {};
    int second {};
};
```

第一个和第二个成员可以独立设置为任何值，因此Pair结构没有不变量。

现在考虑以下表示分数的几乎相同的结构体：

```C++
struct Fraction
{
    int numerator { 0 };
    int denominator { 1 };
};
```

分母为0的分数在数学上是无效的（因为分数的值是其分子除以分母——除以0在数学上没有定义）。因此，需要确保Fraction对象的denominator成员不会设置为0。

例如：

```C++
#include <iostream>

struct Fraction
{
    int numerator { 0 };
    int denominator { 1 }; // 默认初始化: 初始化为有效值
};

void printFractionValue(const Fraction& f)
{
     std::cout << f.numerator / f.denominator << '\n';
}

int main()
{
    Fraction f { 5, 0 };   // 创建一个分母为0的分数
    printFractionValue(f); // 会导致除0错误

    return 0;
}
```

在上面的例子中，使用注释来记录Fraction的不变量。还提供了一个默认的成员初始值，以确保在用户不提供初始化值的情况下将分母设置为1。这确保了当用户决定对Fraction对象进行值初始化时，Fraction object将有效。这是一个好的开始。

但没有什么可以阻止显式地违反这个类不变量：当创建分数f时，可以使用聚合初始化来显式地将分母初始化为0。虽然这不会立即导致问题，但对象现在处于无效状态，进一步使用该对象可能会导致意外或未定义的行为。

当调用printFractionValue(f)时：程序由于除零错误而终止。

考虑到Fraction示例的相对简单性，简单地避免创建无效的Fraction对象应该不会太困难。然而，在使用许多结构体、具有许多成员的结构体或其成员具有复杂关系的更复杂的代码库中，理解哪些值组合可能违反某些类不变量可能不是那么明显。

{{< alert success >}}
**旁白**

一个小的改进是在printFractionValue函数的头部使用断言 assert(f.denominator != 0); 。然而，从行为上来说，这并没有真正改变任何事情。我们应该做到的是避免出错。

{{< /alert >}}

***
## 更复杂的类不变量

Fraction的类不变量是简单的——分母成员不能为0。这在概念上很容易理解，也不太难避免。

当结构体的成员必须具有相关值时，这变得更具挑战性。

```C++
#include <string>

struct Employee
{
    std::string name { };
    char firstInitial { }; // 应当永远是 `name` 的第一个字母 (or `0`)
};
```

在上面的（设计不佳）结构体中，存储在成员firstInitial中的字符值应始终与name的第一个字符匹配。

初始化Employee对象时，用户负责确保维护类不变量。如果name被分配了一个新值，还必须确保firstInitial也被更新。对于使用Employee对象的开发人员来说，这种相关性可能并不明显，也可能忘记维护这种关系。

即使我们编写函数来帮助我们创建和更新Employee对象（确保始终从name的第一个字符设置firstInitial），仍然依赖于用户了解和使用这些函数。

简而言之，依赖开发人员手动维护类不变量可能会导致有问题的代码。

理想情况下，希望有一种机制，对象要么不能被置于无效状态，要么可以立即发出异常信号（而不是让未定义的行为在未来的某个随机点发生）。

结构体（聚合样式）没有解决这种问题的优雅机制。

***
## class简介

在开发C++时，Bjarne Stroustrup希望引入一些功能，允许开发人员创建可以更直观地使用的程序定义类型。他还对为困扰大型复杂程序的一些常见缺陷和维护挑战（如前面提到的类不变量问题）寻找优雅的解决方案感兴趣。

根据他在其他编程语言（特别是Simula，第一个面向对象的编程语言）方面的经验，Bjarne确信，开发一种程序定义的类型是可能的，它是通用的，功能强大，足以用于几乎任何事情。在向Simula学习时，他将这种类型称为类（class）。

就像结构体一样，类是程序定义的复合类型，可以有许多具有不同类型的成员变量。

{{< alert success >}}
**关键点**

从技术角度来看，结构体和类几乎是相同的——因此，使用结构体实现的任何示例都可以使用类实现，反之亦然。然而，从实践的角度来看，我们使用结构体和类的方式不同。

我们在后面讨论具体技术和实践差异

{{< /alert >}}

***
## 定义类

由于类是程序定义的数据类型，因此必须在使用之前定义它。类的定义类似于结构体，只是我们使用class关键字而不是struct。例如，下面是Employee类的定义：

```C++
class Employee
{
    int m_id {};
    int m_age {};
    double m_wage {};
};
```

为了演示相似的类和结构体可以有多相似，下面的程序等效于在课程顶部介绍的程序，但Date现在是一个类，而不是结构：

```C++
#include <iostream>

class Date       // 将 struct 替换为 class
{
public:          // 这里行，是一个访问说明符
    int m_day{}; // 为成员变量，添加 "m_" 前缀
    int m_month{};
    int m_year{};
};

void printDate(const Date& date)
{
    std::cout << date.m_day << '/' << date.m_month << '/' << date.m_year;
}

int main()
{
    Date date{ 4, 10, 21 };
    printDate(date);

    return 0;
}
```

这将打印：

```C++
4/10/21
```

{{< alert success >}}
**相关内容**

在后面，会解释为什么类的成员变量通常以“m_”为前缀，同时会介绍访问说明符是什么

{{< /alert >}}

***
## 大多数C++标准库都是类

您已经在使用过类对象。std::string和std::string_view都被定义为类。事实上，标准库中的大多数非别名类型都定义为类！

类确实是C++的核心和灵魂——它们是如此基础，以至于C++最初被命名为“带类的C”！一旦您熟悉了类，您在C++中的大部分时间都将用于编写、测试和使用它们。

***

{{< prevnext prev="/basic/chapter14/intro-oop/" next="/basic/chapter14/member_func/" >}}
14.0 面向对象编程简介
<--->
14.2 成员函数
{{< /prevnext >}}
