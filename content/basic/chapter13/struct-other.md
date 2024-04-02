---
title: "结构体杂项"
date: 2024-03-08T13:20:57+08:00
---

## 结构体嵌套

在C++中，结构体（和类）可以具有其它程序定义类型的成员。有两种方法可以做到这一点。

首先，可以定义一个程序定义的类型（在全局范围内），然后将其用作另一个程序自定义类型的成员：

```C++
#include <iostream>

struct Employee
{
    int id {};
    int age {};
    double wage {};
};

struct Company
{
    int numberOfEmployees {};
    Employee CEO {}; // Employee 是 Company 的成员
};

int main()
{
    Company myCompany{ 7, { 1, 32, 55000.0 } }; // 嵌套列表，用来初始化 Company
    std::cout << myCompany.CEO.wage << '\n'; // 打印 CEO 的 wage

    return 0;
}
```

在上面的例子中，定义了一个Employee结构体，然后将其用作Company结构体中的成员。初始化myCompany时，还可以使用嵌套的初始化列表。如果想知道CEO的工资是多少，只需使用两次成员选择操作符：myCompany.CEO.wage；

其次，类型也可以嵌套在其他类型中，因此如果Employee仅作为Company的一部分存在，则Employme类型可以嵌套在Company结构体中：

```C++
#include <iostream>

struct Company
{
    struct Employee // 可以通过 Company::Employee 来访问
    {
        int id{};
        int age{};
        double wage{};
    };

    int numberOfEmployees{};
    Employee CEO{}; // Employee定义 位于 Company 中
};

int main()
{
    Company myCompany{ 7, { 1, 32, 55000.0 } }; // 嵌套列表，用来初始化 Company
    std::cout << myCompany.CEO.wage << '\n'; // 打印 CEO 的 wage

    return 0;
}
```

***
## 大多数情况下，结构体应该作为数据的所有者

在前面，我们介绍了所有者和查看器的概念。所有者管理自己的数据，并控制数据何时被销毁。查看者查看其他人的数据，并且不控制数据何时被更改或销毁。

在大多数情况下，我们希望结构（体和类）是数据的所有者。这提供了一些有用的好处：

1. 只要结构体（或类）存在，数据成员就有效。
2. 这些数据成员的值不会意外更改。


使结构体（或类）成为所有者的最简单方法，是为每个成员提供一个表示数据所有者的类型（例如，不是查看器、指针或引用）。如果结构体或类的所有数据成员都是所有者，则该结构体或类本身自动成为所有者。

如果结构体（或类）具有作为查看器的数据成员，则该成员正在查看的对象可能在该结构体之前被销毁。如果发生这种情况，该结构体将保留一个悬空成员，并且访问该成员将导致未定义的行为。

这就是为什么字符串数据作为成员几乎总是具有类型std::string（它是所有者），而不是std::string_view（它是查看器）。下面的示例说明了这种情况：

```C++
#include <iostream>
#include <string>
#include <string_view>

struct Owner
{
    std::string name{}; // std::string 是所有者
};

struct Viewer
{
    std::string_view name {}; // std::string_view 是查看器
};

// getName() 将用户输入的字符串作为 std::string 临时变量返回
// 该临时变量在对应的表达式末尾会被销毁
std::string getName()
{
    std::cout << "Enter a name: ";
    std::string name{};
    std::cin >> name;
    return name;
}

int main()
{
    Owner o { getName() };  // getName() 的返回值 name，刚被初始化，就会被销毁
    std::cout << "The owners name is " << o.name << '\n';  // ok

    Viewer v { getName() }; // getName() 的返回值 name，刚被初始化，就会被销毁
    std::cout << "The viewers name is " << v.name << '\n'; // 未定义的行为

    return 0;
}
```

getName() 函数返回临时std::string变量name。该临时返回值在所处的完整表达式的末尾被销毁。

在o的情况下，该临时std::string用于初始化o.name。由于o.name是一个std::string，o.name会复制临时std::string。临时std::string随后销毁，但o.name不会受到影响，因为它是一个副本。在随后的语句中打印o.name时，它按预期工作。

在v的情况下，此临时std::string用于初始化v.name。由于v.name是一个std::string_view，因此v.name只是临时std::string的观察器，而不是副本。std::string_view随后失效，使v.name悬而未决。在随后的语句中打印v.name时，得到了未定义的行为。

{{< alert success >}}
**最佳实践**

在大多数情况下，我们希望结构体（和类）是数据所有者。启用此功能的最简单方法是确保每个数据成员都是数据所有者（例如，不是查看器、指针或引用）。

{{< /alert >}}

***
## 结构体大小和数据对齐

通常，结构的大小是其所有成员的大小之和。但并不总是这样！

考虑以下程序：

```C++
#include <iostream>

struct Foo
{
    short a {};
    int b {};
    double c {};
};

int main()
{
    std::cout << "The size of short is " << sizeof(short) << " bytes\n";
    std::cout << "The size of int is " << sizeof(int) << " bytes\n";
    std::cout << "The size of double is " << sizeof(double) << " bytes\n";

    std::cout << "The size of Foo is " << sizeof(Foo) << " bytes\n";

    return 0;
}
```

在作者的机器上，打印了：

```C++
The size of short is 2 bytes
The size of int is 4 bytes
The size of double is 8 bytes
The size of Foo is 16 bytes
```

注意，short+int+double的大小是14个字节，但Foo的大小是16个字节！

因此只能说结构体的大小至少与它包含的所有变量的大小一样大。但它可以更大！出于性能原因，编译器有时会在结构中添加间隙（这称为填充）。

在上面的Foo结构中，编译器在成员a之后无形地添加了2个字节的填充，使结构的大小由14个字节变为16个字节。

这实际上会对结构的大小产生相当大的影响，如下程序所示：

```C++
#include <iostream>

struct Foo1
{
    short a{}; // 在 a 之后有两个字节的填充
    int b{};
    short c{}; // 在 c 之后有两个字节的填充
};

struct Foo2
{
    int b{};
    short a{};
    short c{};
};

int main()
{
    std::cout << sizeof(Foo1) << '\n'; // 打印 12
    std::cout << sizeof(Foo2) << '\n'; // 打印 8

    return 0;
}
```

该程序打印：

```C++
12
8
```

请注意，Foo1和Foo2具有相同的成员，唯一的区别是声明顺序。然而，由于添加了填充，Foo1大小增加了50%。

{{< alert success >}}
**对于高级读者**

编译器可能会添加填充的原因超出了本教程的范围，但希望了解更多信息的读者可以阅读百科上的结构体对齐。这是可选阅读，不影响理解结构体或C++！

{{< /alert >}}

{{< alert success >}}
**提示**

通过按大小的递减顺序定义成员，可以最小化填充。

C++编译器不允许对成员重新排序，因此必须手动完成。

{{< /alert >}}

***

{{< prevnext prev="/basic/chapter13/struct-arg-ret/" next="/" >}}
13.7 结构体作为函数的输入与输出
<--->
主页
{{< /prevnext >}}
