---
title: "成员函数"
date: 2024-04-09T13:02:20+08:00
---

在前面，我们介绍了结构体是程序定义的类型，它可以包含成员变量。下面是用于保存日期的结构体的示例：

```C++
struct Date
{
    int year {};
    int month {};
    int day {};
};
```

现在，如果想将日期打印到屏幕上，需要编写一个函数来完成这项工作。下面是一个完整的程序：

```C++
#include <iostream>

struct Date
{
    // 这里是成员变量
    int year {};
    int month {};
    int day {};
};

void print(const Date& date)
{
    // 使用 (.) 来访问成员变量
    std::cout << date.year << '/' << date.month << '/' << date.day;
}

int main()
{
    Date today { 2020, 10, 14 }; // 聚合初始化结构体

    today.day = 16; // 使用 (.) 来访问成员变量
    print(today);   // 使用普通函数来访问结构体

    return 0;
}
```

该程序打印：

```C++
2020/10/16
```

***
## 属性和动作的分离

看看我们周围的一切——看到的每一个地方都是物体：书籍、建筑物、食物，甚至是我们自己。现实生活中的对象有两个主要组成部分：1）一些可观察的属性（例如重量、颜色、大小、坚固性、形状等……），以及2）它们可以执行的基于这些属性的一些操作（例如被打开、损坏其它）。这些属性和动作是不可分割的。

在编程中，用变量表示属性，用函数表示动作。

在上面的Date示例中，请注意，分别定义了属性（Date的成员变量）和使用这些属性执行的操作（函数print()）。只需根据print()的const Date&参数来推断Date和print()之间的连接。

虽然可以将Date和print()放在一个名称空间中（以便更清楚地知道这两个是要打包在一起的），但这会在程序中添加更多的名称和更多的名称空间前缀，从而使代码混乱。

如果有某种方法可以将属性和操作一起定义为一个整体，则可以解决这种分离问题。

***
## 成员函数

除了有成员变量之外，类类型（包括结构体、类和联合）也可以有自己的函数！属于类类型的函数称为成员函数。

不是成员函数的函数被称为非成员函数，以将它们与成员函数区分开来。上面的print()函数是一个非成员函数。

成员函数必须在类类型定义内部声明，可以在类类型内部或外部定义。提醒一下，定义也是声明，因此如果在类中定义成员函数，它将被视为声明。

{{< alert success >}}
**旁白**

在其他面向对象语言（如Java和C#）中，这些被称为方法。尽管术语“方法”在C++中没有使用，但首先学习其他语言之一的程序员仍然可以使用该术语。

{{< /alert >}}

{{< alert success >}}
**注**

在本课中，将使用结构体来显示成员函数的示例——但这里展示的所有内容都同样适用于类。后面对class进行更多讲解后将以类开始作为示例。

{{< /alert >}}

***
## 成员函数示例

让我们重写课程顶部的Date示例，将print()从非成员函数转换为成员函数：

```C++
// 成员函数版本
#include <iostream>

struct Date
{
    int year {};
    int month {};
    int day {};

    void print() // 定义了成员函数 print
    {
        std::cout << year << '/' << month << '/' << day;
    }
};

int main()
{
    Date today { 2020, 10, 14 }; // 结构体聚合初始化

    today.day = 16; // 使用 (.) 来访问成员变量
    today.print();  // 使用 (.) 来访问成员函数

    return 0;
}
```

该程序编译并产生与上面相同的结果：

```C++
2020/10/16
```

成员函数与非成员函数示例之间有三个关键区别：

1. 声明与定义 print() 函数的位置
2. 如何调用 print() 函数
3. 如果在 print() 函数中访问成员变量

让我们依次探索其中的每一个。

***
## 成员函数在类类型定义内声明

在非成员函数示例中，print() 非成员函数在Date结构体外部的全局命名空间中定义。默认情况下，它具有外部链接，因此可以从其他源文件调用它（使用适当的前向声明）。

在成员函数示例中，print() 成员函数在Date结构体定义中声明。因此 print() 被声明为Date的一部分，所以这告诉编译器print() 是一个成员函数。

在类类型定义内定义的成员函数是隐式内联的，因此如果类类型定义被包含在多个代码文件中，它们不会导致违反单定义规则。

***
## 调用成员函数（以及隐式对象）

在非成员函数示例中，调用print(today)，其中today（显式）作为参数传递。

在成员函数示例中，调用today.print() 。此语法使用成员选择运算符（.）选择要调用的成员函数，与访问成员变量的方式一致（例如，today.day=16; ）。

必须使用对应类型的对象调用（非静态）成员函数。在这种情况下，today 是调用 print() 的对象。

注意，在成员函数的情况下，不需要 today 作为参数传递。调用成员函数的对象隐式传递给成员函数。由于这个原因，调用成员函数的对象通常称为隐式对象。

换句话说，当调用 today.print() 时，today是隐式对象，它隐式传递给print() 成员函数。

{{< alert success >}}
**相关内容**

后续课程会讨论将相关对象实际传递给成员函数的机制 —— 隐藏的“this”指针。

{{< /alert >}}

***
## 成员函数内访问成员变量使用隐式对象

下面是print()的非成员函数版本：

```C++
// 非成员函数版本 print
void print(const Date& date)
{
    // 使用 (.) 来访问 date 的成员变量
    std::cout << date.year << '/' << date.month << '/' << date.day;
}
```

此版本的print()有引用参数 const Date& date 。在函数中，通过此引用参数访问date的成员变量，如date.year、date.month和date.day。调用print(today)时，date引用参数绑定到today，date.year、date.month和date.day的计算结果分别为today.year，today.month，和today.day。

print()成员函数的定义：

```C++
    void print() // 成员函数版本 print
    {
        std::cout << year << '/' << month << '/' << day;
    }
```

在成员函数内部，未以（.）为前缀的成员变量都与隐式对象相关联。

换句话说，当调用today.print()时，today是隐式对象，year、month和day（没有前缀）的值分别为today.year、today.month和today.day。

{{< alert success >}}
**关键点**

对于非成员函数，必须显式地将对象传递给要使用的函数，并且成员是通过该对象显式访问的。

对于成员函数，隐式地将对象传递给要使用的函数，并且通过该对象隐式地访问成员。

{{< /alert >}}

***
## 另一个成员函数示例

下面是一个稍微复杂一些的成员函数的示例：

```C++
#include <iostream>
#include <string>

struct Person
{
    std::string name{};
    int age{};

    void kisses(const Person& person)
    {
        std::cout << name << " kisses " << person.name << '\n';
    }
};

int main()
{
    Person joe{ "Joe", 29 };
    Person kate{ "Kate", 27 };

    joe.kisses(kate);

    return 0;
}
```

这将产生输出：

```C++
Joe kisses Kate
```


来看看这是如何工作的。首先，定义了两个Person变量，joe和kate。接下来，调用 joe.kisses(kate);  。joe是这里的隐式对象，kate作为显式参数传递。

当 kisses() 成员函数执行时，name 不使用成员选择操作符（.），因此它引用隐式对象，即joe，所以解析为joe.name。person.name 使用成员选择操作符，因此它不引用隐式对象。由于person是kate的引用，因此解析为kate.name。

{{< alert success >}}
**关键点**

如果没有成员函数功能，就会写kisses(joe, kate)。使用成员函数，可以编写joe.kisses(kate) 。请注意后者的可读性好的多，可以明确哪个对象正在启动操作，哪个对象是输入数据。

{{< /alert >}}

***
## 成员变量和函数可以按任何顺序定义

C++编译器通常从上到下编译代码。对于遇到的每个名称，编译器会检查它是否已经看到该名称的声明，以便它可以进行适当的类型检查。

这意味着在非成员函数内部，不能使用未在之前声明的变量或函数：

```C++
void x()
{
    y(); // error: y 没有声明, 编译器无法得知y是什么
}
 
int y()
{
    return 5;
}
```

然而，在类类型内部，对于成员函数和成员变量，这个限制不适用，可以按自己喜欢的顺序定义成员。例如：

```C++
struct Foo
{
    int m_x{ y() };   // 这里可以调用 y()，即使 y 在这里仍未被定义

    void x() { y(); } // 这里可以调用 y()，即使 y 在这里仍未被定义
    int y()  { return 5; }
};
```

{{< alert success >}}
**对于高级读者**

对于非成员函数，可以前向声明变量或函数，以便在编译器看到完整定义之前使用它们。

类类型的成员变量和成员函数不能显式前向声明（因为编译器总是需要查看完整的类类型定义才能正常工作）。在正常的编译规则下，这意味着不能在定义成员之前使用它们，并且将被迫按使用顺序定义它们。那将是一种痛苦！

因此，编译器有一个巧妙的技巧：类内的实际定义有隐式的向前声明。

这样，在编译器编译成员变量初始值设定项和成员函数定义，它已经看到了类的所有成员的隐式声明！

{{< /alert >}}

***
## 成员函数可以重载

就像非成员函数一样，成员函数也可以重载，只要每个成员函数之间可以区分。

例如下面的示例：

```C++
#include <iostream>
#include <string_view>

struct Date
{
    int year {};
    int month {};
    int day {};

    void print()
    {
        std::cout << year << '/' << month << '/' << day;
    }

    void print(std::string_view prefix)
    {
        std::cout << prefix << year << '/' << month << '/' << day;
    }
};

int main()
{
    Date today { 2020, 10, 14 };

    today.print(); // 调用 Date::print()
    std::cout << '\n';

    today.print("The date is: "); // 调用 Date::print(std::string_view)
    std::cout << '\n';

    return 0;
}
```

这将打印：

```C++
2020/10/14
The date is: 2020/10/14
```

***
## 结构体和成员函数

在C中，结构体只能有成员变量，没有成员函数。

在C++中，在设计class时，Bjarne Stroustrup花费了一些时间考虑是否应授予结构体（从C继承）具有成员函数的能力。经过考虑，决定应该这样做。

在现代C++中，结构体具有成员函数。

{{< alert success >}}
**旁白**

这一决定引发了一系列其他问题，即结构体应该有哪些其他新的C++功能。Bjarne担心，让结构体访问有限的功能子集最终会增加语言的复杂性和边缘情况。为了简单起见，他最终决定结构体和类将具有统一的规则集（这意味着结构体可以做类可以做的一切，反之亦然）。

{{< /alert >}}

{{< alert success >}}
**最佳实践**

成员函数可以与结构体和类一起使用。

然而，结构体应该避免定义构造函数，因为这样做会使它们成为非聚合函数。

{{< /alert >}}

***
## 没有数据变量的类类型

可以创建没有数据成员的类类型（例如，仅具有成员函数）。也可以实例化此类类型的对象：

```C++
#include <iostream>

struct Foo
{
    void printHi() { std::cout << "Hi!\n"; }
};

int main()
{
    Foo f{};
    f.printHi(); // requires object to call

    return 0;
}
```

然而，如果类类型没有任何数据成员，那么使用类类型可能是多余的。在这种情况下，请考虑改用名称空间。可以更清楚地看到，没有管理的数据（并且不需要实例化对象来调用函数）。

```C++
#include <iostream>

namespace Foo
{
    void printHi() { std::cout << "Hi!\n"; }
};

int main()
{
    Foo::printHi(); // 不需要实际的对象

    return 0;
}
```

{{< alert success >}}
**最佳实践**

如果类类型没有数据成员，则首选使用命名空间。

{{< /alert >}}

***

{{< prevnext prev="/basic/chapter14/intro-class/" next="/" >}}
14.1 面向对象编程简介
<--->
主页
{{< /prevnext >}}
