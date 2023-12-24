---
title: "内部链接"
date: 2023-12-18T16:52:52+08:00
---

在局部变量一节中，我们说过，“标识符的链接属性决定了该名称的其他声明是否引用同一对象”，同时也得知--局部变量没有链接属性。

全局变量和函数标识符可以具有内部链接或外部链接属性。我们将在本课中介绍内部链接的情况，在下一节中介绍外部链接。

具有内部链接的标识符可以在单个翻译单元内看到并使用，但它不能从其他翻译单元访问（即，它不向链接器公开）。这意味着，如果两个源文件具有具有内部链接的同名标识符，则这些标识符将被视为独立的（并且不会因具有重复定义而导致ODR冲突）。

***
## 具有内部链接的全局变量

具有内部链接的全局变量有时称为内部变量。

为了使非常量全局变量成为内部变量，我们使用static关键字。

```C++
#include <iostream>

static int g_x{}; // non-constant globals have external linkage by default, but can be given internal linkage via the static keyword

const int g_y{ 1 }; // const globals have internal linkage by default
constexpr int g_z{ 2 }; // constexpr globals have internal linkage by default

int main()
{
    std::cout << g_x << ' ' << g_y << ' ' << g_z << '\n';
    return 0;
}
```

默认情况下，Const和constexpr全局变量具有内部链接（因此不需要static关键字——如果使用它，它将被忽略）。

下面是使用内部变量的多个文件的示例：

a.cpp：

```C++
[[maybe_unused]] constexpr int g_x { 2 }; // this internal g_x is only accessible within a.cpp
```

主.cpp：

```C++
#include <iostream>

static int g_x { 3 }; // this separate internal g_x is only accessible within main.cpp

int main()
{
    std::cout << g_x << '\n'; // uses main.cpp's g_x, prints 3

    return 0;
}
```

该程序打印：

因为g_x是每个文件的内部文件，所以main.cpp不知道.cpp也有一个名为g_x的变量（反之亦然）。

{{< alert success >}}
**对于高级读者**

上面静态关键字的使用是存储类说明符的一个示例，它设置名称的链接及其存储持续时间。最常用的存储类说明符是静态、外部和可变的。术语存储类说明符主要用于技术文档。

{{< /alert >}}

***
## 具有内部联动装置的功能

由于链接是标识符的属性（不是变量的属性），函数标识符具有与变量标识符相同的链接属性。函数默认为外部链接（我们将在下一课中介绍），但可以通过static关键字设置为内部链接：

添加.cpp：

```C++
// This function is declared as static, and can now be used only within this file
// Attempts to access it from another file via a function forward declaration will fail
[[maybe_unused]] static int add(int x, int y)
{
    return x + y;
}
```

主.cpp：

```C++
#include <iostream>

static int add(int x, int y); // forward declaration for function add

int main()
{
    std::cout << add(3, 4) << '\n';

    return 0;
}
```

此程序将不会链接，因为在add.cpp之外无法访问函数add。

***
## 一个定义规则和内部链接

在第2.7课——转发声明和定义中，我们注意到一个定义规则指出，对象或函数不能在文件或程序中具有多个定义。

然而，值得注意的是，在不同文件中定义的内部对象（和函数）被认为是独立的实体（即使它们的名称和类型相同），因此不会违反一个定义规则。每个内部对象只有一个定义。

***
## 静态命名空间与未命名命名空间

在现代C++中，使用static关键字为标识符提供内部链接越来越不受欢迎。未命名的名称空间可以为更广泛的标识符（例如，类型标识符）提供内部链接，并且它们更适合为许多标识符提供内部链接。

在第7.13课中，我们讨论了未命名的名称空间——未命名的和内联的名称空间。

***
## 为什么要费心为标识符提供内部链接？

给出标识符内部链接通常有两个原因：

1. 有一个标识符，我们要确保其他文件无法访问。这可能是一个我们不想弄乱的全局变量，或者是一个不想调用的辅助函数。
2. 迂腐地避免命名冲突。由于具有内部链接的标识符不会向链接器公开，因此它们只能与同一翻译单元中的名称发生冲突，而不能在整个程序中发生冲突。


许多现代开发指南建议提供不打算从另一个文件内部链接使用的每个变量和函数。如果你有纪律，这是一个很好的建议。

现在，我们至少推荐一种更轻量级的接触方法：为您有明确理由不允许从其他文件访问的任何标识符提供内部链接。

{{< alert success >}}
**最佳做法**

当您有明确的理由不允许从其他文件访问时，请提供标识符内部链接。

考虑为其他文件提供您不希望访问的所有标识符的内部链接（为此使用未命名的命名空间）。

{{< /alert >}}

***
## 快速摘要

```C++
// Internal global variables definitions:
static int g_x;          // defines non-initialized internal global variable (zero initialized by default)
static int g_x{ 1 };     // defines initialized internal global variable

const int g_y { 2 };     // defines initialized internal global const variable
constexpr int g_y { 3 }; // defines initialized internal global constexpr variable

// Internal function definitions:
static int foo() {};     // defines internal function
```

我们在第7.11课中提供了一个全面的总结——范围、持续时间和链接总结。

