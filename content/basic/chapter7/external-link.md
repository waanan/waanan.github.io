---
title: "外部链接和变量前向声明"
date: 2023-12-18T16:52:52+08:00
---

在上一课（7.6——内部链接）中，我们讨论了内部链接如何将标识符的使用限制为单个文件。在本课中，我们将探索外部链接的概念。

具有外部链接的标识符既可以从定义它的文件中看到，也可以从其他代码文件中使用（通过转发声明）。在这种意义上，具有外部链接的标识符是真正的“全局”标识符，因为它们可以在程序中的任何位置使用！

***
## 默认情况下，功能具有外部链接

在第2.8课——具有多个代码文件的程序中，您学习了可以从另一个文件调用在一个文件中定义的函数。这是因为函数在默认情况下具有外部链接。

为了调用在另一个文件中定义的函数，必须在希望使用该函数的任何其他文件中放置该函数的前向声明。forward声明将函数的存在告知编译器，链接器将函数调用连接到实际的函数定义。

下面是一个示例：

a.cpp：

```C++
#include <iostream>

void sayHi() // this function has external linkage, and can be seen by other files
{
    std::cout << "Hi!\n";
}
```

主.cpp：

```C++
void sayHi(); // forward declaration for function sayHi, makes sayHi accessible in this file

int main()
{
    sayHi(); // call to function defined in another file, linker will connect this call to the function definition

    return 0;
}
```

上述程序打印：

在上面的示例中，main.cpp中函数sayHi（）的前向声明允许main.cpp访问在.cpp.中定义的sayHi.（）函数。前向声明满足编译器的要求，并且链接器能够将函数调用链接到函数定义。

如果函数sayHi（）具有内部链接，则链接器将无法将函数调用连接到函数定义，并将导致链接器错误。

***
## 具有外部链接的全局变量

具有外部链接的全局变量有时称为外部变量。要将全局变量设置为外部变量（因此可由其他文件访问），可以使用extern关键字执行此操作：

```C++
int g_x { 2 }; // non-constant globals are external by default

extern const int g_y { 3 }; // const globals can be defined as extern, making them external
extern constexpr int g_z { 3 }; // constexpr globals can be defined as extern, making them external (but this is pretty useless, see the warning in the next section)

int main()
{
    return 0;
}
```

默认情况下，非常量全局变量是外部的（如果使用，将忽略extern关键字）。

***
## 通过extern关键字的变量前向声明

要实际使用在另一个文件中定义的外部全局变量，还必须在希望使用该变量的任何其他文件中放置全局变量的前向声明。对于变量，也可以通过extern关键字（没有初始化值）创建前向声明。

下面是使用变量转发声明的示例：

a.cpp：

```C++
// global variable definitions
int g_x { 2 }; // non-constant globals have external linkage by default
extern const int g_y { 3 }; // this extern gives g_y external linkage
```

主.cpp：

```C++
#include <iostream>

extern int g_x; // this extern is a forward declaration of a variable named g_x that is defined somewhere else
extern const int g_y; // this extern is a forward declaration of a const variable named g_y that is defined somewhere else

int main()
{
    std::cout << g_x << ' ' << g_y << '\n'; // prints 2 3

    return 0;
}
```

在上面的示例中，.cpp和main.cpp都引用了名为g_x的相同全局变量。因此，即使g_x是在.cpp中定义和初始化的，我们也可以通过g_x的前向声明在main.cpp内使用它的值。

请注意，extern关键字在不同的上下文中具有不同的含义。在某些上下文中，extern意味着“为该变量提供外部链接”。在其他上下文中，extern意味着“这是在其他地方定义的外部变量的前向声明”。是的，这很令人困惑，因此我们在第7.11课中总结了所有这些用法——范围、持续时间和链接摘要。

注意，函数前向声明不需要extern关键字——编译器能够根据是否提供函数体来判断您是在定义新函数还是在进行前向声明。变量向前声明确实需要extern关键字来帮助区分未初始化的变量定义和变量向前声明（它们在其他方面看起来相同）：

```C++
// non-constant 
int g_x; // variable definition (can have initializer if desired)
extern int g_x; // forward declaration (no initializer)

// constant
extern const int g_y { 1 }; // variable definition (const requires initializers)
extern const int g_y; // forward declaration (no initializer)
```

{{< alert success >}}
**警告**

如果要定义未初始化的非常量全局变量，请不要使用extern关键字，否则C++会认为您正在尝试对该变量进行前向声明。

{{< /alert >}}

{{< alert success >}}
**警告**

尽管可以通过extern关键字为constexpr变量提供外部链接，但它们不能向前声明为consterpr。这是因为编译器需要知道constexpr变量的值（在编译时）。如果该值在其他文件中定义，则编译器对该其他文件中所定义的值不可见。

然而，您可以将constexpr变量向前声明为const，编译器将其视为运行时常量。这并不是特别有用。

{{< /alert >}}

***
## 快速摘要

```C++
// External global variable definitions:
int g_x;                       // defines non-initialized external global variable (zero initialized by default)
extern const int g_x{ 1 };     // defines initialized const external global variable
extern constexpr int g_x{ 2 }; // defines initialized constexpr external global variable

// Forward declarations
extern int g_y;                // forward declaration for non-constant global variable
extern const int g_y;          // forward declaration for const global variable
extern constexpr int g_y;      // not allowed: constexpr variables can't be forward declared
```

我们在第7.11课中提供了一个全面的总结——范围、持续时间和链接总结。

***

{{< prevnext prev="/basic/chapter7/internal-link/" next="/" >}}
7.5 内部链接
<--->
主页
{{< /prevnext >}}
