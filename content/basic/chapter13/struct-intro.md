---
title: "结构体简介"
date: 2024-03-08T13:20:57+08:00
---

在许多情况下，需要多个变量来表示我们感兴趣的东西。正如分数有一个分子和分母，它们共同组成数学中的一个完整概念。

又或者，假设编写一个程序，在其中存储有关公司员工的信息。需要记录员工的姓名、职务、年龄、员工id、经理id、工资、生日、雇佣日期等属性…

如果使用变量来跟踪所有这些信息，可能会如下所示：

```C++
std::string name;
std::string title;
int age;
int id;
int managerId;
double wage;
int birthdayYear;
int birthdayMonth;
int birthdayDay;
int hireYear;
int hireMonth;
int hireDay;
```

然而，这种方法存在许多问题。首先，还不能立即清楚这些变量是否实际相关（必须阅读注释，或者查看它们在代码中的使用方式）。其次，现在有12个变量需要管理。如果想将这个员工信息传递给函数，必须传递12个参数（并且以正确的顺序），这将把函数定义和函数调用搞得一团糟。如果函数只能返回单个值，那么函数如何返回员工信息呢？

如果想要一个以上的员工，需要为每个额外的员工定义12个以上的变量（每个变量都需要一个唯一的名称）！这显然根本无法扩展。真正需要的是某种方法来将所有这些相关的数据片段组织在一起，使它们更易于管理。

幸运的是，C++附带了两种旨在解决此类挑战的复合类型：结构体（struct，现在将介绍）和类（class，将很快探索）。结构体是程序定义的数据类型，它允许将多个变量绑定到一个类型中。这使得相关变量集的管理简单得多！

***
## 定义结构体

由于结构体是程序定义的类型，因此在开始使用之前，必须首先告诉编译器结构体类型的定义。下面是简化后的员工的结构体定义示例：

```C++
struct Employee
{
    int id {};
    int age {};
    double wage {};
};
```

struct关键字用于告诉编译器正在定义一个结构体，我们将其命名为Employee（因为程序定义的类型通常以大写字母开头）。

然后，在一对花括号内，定义每个Employee对象将包含的变量。在这个例子中，Employee有3个变量：int id、int age和double wage。作为结构体一部分的变量称为数据成员（或成员变量）。

就像使用一组空的花括号来初始化普通变量一样，每个成员变量后面的空花括号确保在创建Employee时，Employee中的成员变量被初始化。后续会详细介绍这一点。

最后，用分号结束类型定义。

提醒一下，Employee只是一个类型定义——此时实际上没有创建任何对象。

{{< alert success >}}
**提示**

在日常语言中，成员是属于一个群体的个人。例如，您可能是篮球队的成员，而您的妹妹可能是合唱团的成员。

在C++中，成员是属于结构体（或类）的变量、函数或类型。所有成员都必须在结构体（或类）定义中声明。

在以后的课程中，将经常使用“成员”一词，因此请确保您记住它的含义。

{{< /alert >}}

***
## 定义结构体对象

可以简单地定义Employme类型的变量：

```C++
Employee joe {}; // Employee 是类型, joe 是变量名
```

这定义了一个名为joe的Employee类型的变量。执行代码时，将实例化包含3个成员变量的Employee对象。空大括号确保对象是值初始化的。

与任何其他类型一样，可以定义相同结构体类型的多个变量：

```C++
Employee joe {}; // 创建一个类型为 Employee 结构体的变量 Joe
Employee frank {}; // 创建一个类型为 Employee 结构体的变量 Frank
```

***
## 访问成员变量

考虑以下示例：

```C++
struct Employee
{
    int id {};
    int age {};
    double wage {};
};

int main()
{
    Employee joe {};

    return 0;
}
```

在上面的示例中，名称joe指的是整个结构体对象（其中包含成员变量）。为了访问特定的成员变量，在结构体变量名和成员变量名之间使用成员选择操作符（operator.）。例如，要访问joe的age成员，使用joe.age。

结构体成员变量就像普通变量一样，因此可以对它们进行普通操作，包括赋值、算术、比较等…

```C++
#include <iostream>

struct Employee
{
    int id {};
    int age {};
    double wage {};
};

int main()
{
    Employee joe {};

    joe.age = 32;  // 使用成员选择操作符 (.) 去选择 joe 的成员变量 age

    std::cout << joe.age << '\n'; // 打印 joe 的 age

    return 0;
}
```

这将打印：

```C++
32
```

结构体的最大优势之一是，只需要为每个结构体对象创建一个名称（成员变量名称作为结构体类型定义的一部分是固定的）。在下面的示例中，实例化了两个Employee对象：joe和frank。

```C++
#include <iostream>

struct Employee
{
    int id {};
    int age {};
    double wage {};
};

int main()
{
    Employee joe {};
    joe.id = 14;
    joe.age = 32;
    joe.wage = 60000.0;

    Employee frank {};
    frank.id = 15;
    frank.age = 28;
    frank.wage = 45000.0;

    int totalAge { joe.age + frank.age };

    if (joe.wage > frank.wage)
        std::cout << "Joe makes more than Frank\n";
    else if (joe.wage < frank.wage)
        std::cout << "Joe makes less than Frank\n";
    else
        std::cout << "Joe and Frank make the same amount\n";

    // Frank 升职加薪了
    frank.wage += 5000.0;

    // 今天是joe的生日
    ++joe.age; // Joe 的年龄加一

    return 0;
}
```

在上面的示例中，很容易区分哪些成员变量属于Joe，哪些属于Frank。这提供了比单个变量更高级别的组织。此外，由于Joe和Frank的成员变量具有相同的名称，这提供了一致性。

在下一课中，将继续探索结构体，研究如何初始化它们。

***