---
title: "结构体初始化"
date: 2024-03-08T13:20:57+08:00
---

在上一课中，讨论了如何定义结构体、实例化结构体对象和访问其成员变量。在本课中，将讨论如何初始化结构体。

***
## 结构体默认情况下不初始化成员

与普通变量很相似，结构体默认情况下不会初始化数据成员。考虑以下：

```C++
#include <iostream>

struct Employee
{
    int id; // 注: 无初始化
    int age;
    double wage;
};

int main()
{
    Employee joe; // 注: 无初始化
    std::cout << joe.id << '\n';

    return 0;
}
```

因为没有提供任何初始化，所以当joe被实例化时，joe.id、joe.age和joe.wage都处于未被初始化状态。然后，当尝试打印joe.id的值时，将获得未定义的行为。

***
## 什么是聚合？

在一般编程中，聚合数据类型（也称为聚合）是可以包含多个数据成员的任何类型。某些类型的聚合允许成员具有不同的类型（例如结构体），而其他类型的聚合则要求所有成员都必须是单个类型（例如数组）。

在C++中，聚合的定义更窄，也更复杂。

此时需要理解的关键问题是，只包含数据成员的结构体是聚合数据类型。

{{< alert success >}}
**注**

在本教程系列中，当使用术语“聚合”（或“非聚合”）时，将指的是聚合的C++定义。

{{< /alert >}}

{{< alert success >}}
**对于高级读者**

为了简单起见，C++中的聚合要么是C样式数组，要么是具有以下特征的类类型（struct、class或union）：

1. 没有用户声明的构造函数
2. 没有私有或受保护的非静态数据成员
3. 无虚函数


流行的类型std::array也是一种聚合。

您可以在这里找到[C++聚合类型](https://en.cppreference.com/w/cpp/language/aggregate_initialization)的精确定义。

{{< /alert >}}

***
## 结构体的聚合初始化

由于普通变量只能保存单个值，因此只需要提供单个初始值设定项：

```C++
int x { 5 };
```

然而，结构体可以有多个成员：

```C++
struct Employee
{
    int id {};
    int age {};
    double wage {};
};
```

定义具有结构体类型的对象时，需要某种方法在初始化时初始化多个成员：

```C++
Employee joe; // 如何初始化 joe.id, joe.age, 和 joe.wage?
```

聚合初始化，允许我们直接初始化聚合类型的成员。为此，需要提供了一个初始化器列表，它只是一个逗号分隔值的大括号列表。

聚合初始化有两种主要形式：

```C++
struct Employee
{
    int id {};
    int age {};
    double wage {};
};

int main()
{
    Employee frank = { 1, 32, 60000.0 }; // 拷贝列表初始化
    Employee joe { 2, 28, 45000.0 };     // 列表初始化 (推荐)

    return 0;
}
```

这些初始化形式中的每一个都执行成员变量的初始化，这意味着结构体中的每个成员变量都是按声明的顺序初始化的。因此，Employee joe { 2, 28, 45000.0 }; 首先用值2初始化joe.id，然后用值28初始化joe.age，最后用值45000.0初始化joe.wage。

在C++20中，还可以使用带括号的值列表来初始化（某些）聚合：

```C++
    Employee robert ( 3, 45, 62500.0 );  // 直接初始化，使用圆括号 (C++20)
```

建议尽可能避免最后一种形式，因为它目前不适用于使用大括号省略的聚合（特别是std::array）。

{{< alert success >}}
**最佳实践**

初始化聚合类型时，首选列表初始化。

{{< /alert >}}

***
## 初始化器列表中缺少元素

如果初始化列表中，初始化值的数量小于成员变量的数量，则所有剩余的成员都将被值初始化。

```C++
struct Employee
{
    int id {};
    int age {};
    double wage {};
};

int main()
{
    Employee joe { 2, 28 }; // joe.wage 将会被值初始化为 0.0

    return 0;
}
```

在上面的示例中，joe.id将用值2初始化，joe.age将用值28初始化，并且由于joe.wage没有被赋予显式初始值设定项，因此它的值将初始化为0.0。

这意味着可以使用空的初始化列表来对结构体的所有成员变量进行值初始化：

```C++
Employee joe {}; // 使用默认值，初始化所有成员变量
```

***
## Const结构体

结构体类型的变量可以是const（或constexpr），就像所有const变量一样，它们必须被初始化。

```C++
struct Rectangle
{
    double length {};
    double width {};
};

int main()
{
    const Rectangle unit { 1.0, 1.0 };
    const Rectangle zero { }; // 值初始化所有的成员变量

    return 0;
}
```

***
## 指定成员初始值设定项(C++20)

从值列表初始化结构体时，初始值设定项按声明的顺序应用于成员。

```C++
struct Foo
{
    int a {};
    int c {};
};

int main()
{
    Foo f { 1, 3 }; // f.a = 1, f.c = 3

    return 0;
}
```

现在考虑一下，如果要更新此结构体定义，添加不是最后一个成员的新成员，会发生什么情况：

```C++
struct Foo
{
    int a {};
    int b {}; // 新添加的成员变量
    int c {};
};

int main()
{
    Foo f { 1, 3 }; // 现在, f.a = 1, f.b = 3, f.c = 0

    return 0;
}
```

现在，所有的初始化值都发生了偏移，更糟糕的是，编译器可能不会将其检测为错误（毕竟，语法仍然有效）。

为了帮助避免这种情况，C++20添加了一种新的方法来初始化结构成员，指定成员变量的初始值设定项。这允许您显式定义哪些初始化值映射到哪些成员变量。成员变量可以使用列表或复制初始化，并且必须以在结构中声明它们的相同顺序进行初始化，否则将导致警告或错误。未指定初始值设定项的成员将被初始化为默认值。

```C++
struct Foo
{
    int a{ };
    int b{ };
    int c{ };
};

int main()
{
    Foo f1{ .a{ 1 }, .c{ 3 } }; // ok: f1.a = 1, f1.b = 0 (值初始化), f1.c = 3
    Foo f2{ .a = 1, .c = 3 };   // ok: f2.a = 1, f2.b = 0 (值初始化), f2.c = 3
    Foo f3{ .b{ 2 }, .a{ 1 } }; // error: 初始化顺序与成员变量声明顺序不一致

    return 0;
}
```

这种初始化形式提供了某种程度的自我文档，并有助于确保不会无意中混淆初始化值的顺序。然而，这也会显著地扰乱初始值列表，因此不建议将其用作最佳实践。

{{< alert success >}}
**最佳实践**

将新成员添加到聚合时，最安全的做法是将其添加到定义列表的底部，以便其他成员的初始值设定项不会移动。

{{< /alert >}}

***
## 列表形式为结构体赋值

如前所示，可以单独为结构体的成员指定值：

```C++
struct Employee
{
    int id {};
    int age {};
    double wage {};
};

int main()
{
    Employee joe { 1, 32, 60000.0 };

    joe.age  = 33;      // Joe 大了一岁
    joe.wage = 66000.0; // 也加薪了

    return 0;
}
```

这对于单个成员变量来说很好，但想要更新所有成员变量时就不太好了。与使用列表初始化结构体类似，也可以使用列表将值分配给结构体（该列表执行成员级赋值）：

```C++
struct Employee
{
    int id {};
    int age {};
    double wage {};
};

int main()
{
    Employee joe { 1, 32, 60000.0 };
    joe = { joe.id, 33, 66000.0 }; // Joe 大了一岁 也加薪了

    return 0;
}
```

注意，因为我们不想更改joe.id，所以需要在列表中提供joe.id的当前值作为占位符，将其再赋值给joe.id。当然这看起来有点傻。

***
## 使用指定成员的列表进行赋值(C++20)

指定成员的初始值设定项也可以在列表赋值中使用：

```C++
struct Employee
{
    int id {};
    int age {};
    double wage {};
};

int main()
{
    Employee joe { 1, 32, 60000.0 };
    joe = { .id = joe.id, .age = 33, .wage = 66000.0 }; // Joe 大了一岁 也加薪了

    return 0;
}
```

任何未指定的成员，都会进行值初始化。例如，如果没有为joe.id指定指定的初始值设定项，那么joe.id将被赋值为0。

***
## 使用相同类型的另一个结构体进行初始化

也可以使用相同类型的另一个结构体来初始化：

```C++
#include <iostream>

struct Foo
{
    int a{};
    int b{};
    int c{};
};

int main()
{
    Foo foo { 1, 2, 3 };
    
    Foo x = foo; // 拷贝初始化
    Foo y(foo);  // 直接初始化
    Foo z {foo}; // 列表初始化
    
    std::cout << x.a << ' ' << y.b << ' ' << z.c << '\n';

    return 0;
}
```

以上打印内容：

```C++
1 2 3
```

请注意，这使用了我们熟悉的标准形式的初始化（拷贝、直接或列表初始化），而不是聚合初始化。

***

{{< prevnext prev="/basic/chapter13/struct-intro/" next="/basic/chapter13/struct-member-default-init/" >}}
13.4 结构体简介
<--->
13.6 成员变量的默认初始化
{{< /prevnext >}}
