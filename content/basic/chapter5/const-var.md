---
title: "常量（命名常量）"
date: 2023-11-28T13:19:42+08:00
---

## 常数简介

在编程中，常数是在程序执行期间不能更改的值。

C++支持两种不同类型的常量：

1. 命名常量（Named constants）是与标识符关联的常量值。这些有时也被称为符号常量（symbolic constants），或者只称为常量（constants）。
2. 字面值常量（Literal constants）是与标识符无关的常量值。


本节先来介绍命名常量。

***
## 命名常量的类型

在C++中定义命名常量有三种方法：

1. 将变量设置为不可更改，即为常变量（Constant variables）（在本课中介绍）。
2. 具有替换文本的类对象宏（在-预处理器简介 中介绍，在本课中有额外的介绍）。
3. 枚举常数（在后续-枚举值中介绍）。


常变量（Constant variables）是最常见的命名常量类型，因此我们将从这里开始。

***
## 常变量（Constant variables）

到目前为止，我们看到的所有变量的值可以随时更改（通常通过分配新值）。例如：

```C++
int main()
{
    int x { 4 }; // x 不是一个常变量
    x = 5; // 通过赋值操作将 x 设置为 5 

    return 0;
}
```

然而，在许多情况下，定义具有无法更改的值的变量是有用的。例如，考虑地球的重力（表面附近）：9.8米/秒^2。这不太可能很快改变（如果改变了，你可能会遇到比学习C++更大的问题）。将该值定义为常量有助于确保该值不会意外更改。常数还有其他好处，我们将在后面的课程中探讨。

尽管它是一个众所周知的矛盾叫法，但值不能改变的变量称为常变量。

***
## 声明常变量

要声明常变量，我们将const关键字（称为“const限定符”）放在对象类型的旁边：

```C++
const double gravity { 9.8 };  // 更推荐将 const 放在类型前
int const sidesInSquare { 4 }; // const放在类型后，可以但不推荐
```

尽管const限定符可以放在类型之前或之后，但在类型之前使用const更常见，因为它更好地遵循标准的英语语言约定，即修饰符在被修改的对象之前（例如，“绿球”，而不是“球绿”）。

{{< alert success >}}
**旁白**

由于编译器解析复杂声明的方式，一些开发人员更喜欢将const放在类型之后（因为它稍微更一致）。这种风格被称为“east const”。虽然这种风格有一些支持者（和一些合理的观点），但它并没有得到显著的流行。

{{< /alert >}}

{{< alert success >}}
**最佳实践**

将const放在类型之前（因为这样做更传统）。

{{< /alert >}}

***
## 必须初始化常变量

定义常变量时必须对其进行初始化，之后不能通过赋值更改该值：

```C++
int main()
{
    const double gravity; // error: const variables 必须初始化
    gravity = 9.9;        // error: const variables 的值不能改变

    return 0;
}
```

注意，常变量可以从其他变量（包括非常变量）初始化：

```C++
#include <iostream>

int main()
{ 
    std::cout << "Enter your age: ";
    int age{};
    std::cin >> age;

    const int constAge { age }; // 使用非常量的值初始化常变量

    age = 5;      // ok: age 不是const, 所以可以改变值
    constAge = 6; // error: constAge 是 const, 不能改变值

    return 0;
}
```

在上面的示例中，我们使用非常变量age初始化常变量constAge。因为age仍然是非const的，我们可以改变它的值。然而，由于constAge是const，因此无法在初始化后更改它的值。

***
## 命名约定

常量变量有许多不同的命名约定。

从C转换过来的程序员通常更喜欢常变量的带下划线的大写名称（例如，EARTH_GRAVITY）。在C++中更常见的是使用带“k”前缀的插入名称（例如，kEarthGravity）。

然而，由于常变量的行为类似于普通变量（除了它们不能被赋值），因此它们没有理由需要特殊的命名约定。因此，我们更喜欢使用与用于普通变量（例如earthGravity）相同的命名约定。

***
## const函数参数

函数参数可以通过const关键字设置为常量：

```C++
#include <iostream>

void printInt(const int x)
{
    std::cout << x << '\n';
}

int main()
{
    printInt(5); // 5 被用来初始化 x
    printInt(6); // 6 被用来初始化 x

    return 0;
}
```

注意，我们没有为常量参数x提供显式初始值——函数调用中的参数值将用作x的初始值。

使函数参数成为常量需要编译器的帮助，以确保参数的值不会在函数内部更改。然而，在现代C++中，向函数传递值时一般不将参数设置为常量，因为我们通常不关心函数是否更改参数的值（因为它只是一个副本，无论如何都会在函数结束时被销毁）。const关键字还为函数原型添加了少量不必要的混乱。

在本系列教程的后面，我们将讨论向函数传递参数的两种其他方法：通过引用传递和通过地址传递。当使用这些方法中的任何一种时，正确使用const非常重要。

{{< alert success >}}
**最佳实践**

通过值传递时不要使用const。

{{< /alert >}}

***
## 常量返回值

函数的返回值也可以设置为常量：

```C++
#include <iostream>

const int getValue()
{
    return 5;
}

int main()
{
    std::cout << getValue() << '\n';

    return 0;
}
```

对于基本类型，返回类型上的const限定符被简单地忽略（编译器可能会生成警告）。

对于其他类型（稍后将介绍），按值返回常量对象通常没有什么意义，因为它们是临时副本，无论如何都会被销毁。返回常量值也会阻碍某些类型的编译器优化（涉及移动语义），可能会导致较低的性能。

{{< alert success >}}
**最佳实践**

按值返回时不要使用const。

{{< /alert >}}

***
## 替换文本的类对象宏

在 预处理器简介 中，我们讨论了替换文本的类对象宏。例如：

```C++
#include <iostream>

#define MY_NAME "Fly"

int main()
{
    std::cout << "My name is: " << MY_NAME << '\n';

    return 0;
}
```

当预处理器处理包含该代码的文件时，它将用“Fly”替换MY_NAME（第7行）。请注意，MY_NAME是一个名称，替换文本是一个常量值，因此替换文本的类对象宏也被命名为常量。

***
## 与预处理器宏相比，更推荐常变量

使用命名常量时，为什么不推荐使用预处理器宏呢？（至少）有三个主要原因。

最大的问题是宏不遵循正常的C++作用域规则。定义宏后，将替换当前文件中宏名称的所有后续引用。如果在其他地方使用该名称，则会在不需要的地方进行宏替换。这很可能会导致奇怪的编译错误。例如：

```C++
#include <iostream>

void someFcn()
{
// 尽管 gravity 在这个函数中定义
// 但预处理器会替换剩余文件中所有出现的gravity
#define gravity 9.8
}

void printGravity(double gravity) // 当替换到这里时, 会导致编译错误
{
    std::cout << "gravity: " << gravity << '\n';
}

int main()
{
    printGravity(3.71);

    return 0;
}
```

编译时，GCC产生了这个令人困惑的错误：

```C++
prog.cc:5:17: error: expected ',' or '...' before numeric constant
    5 | #define gravity 9.8
      |                 ^~~
prog.cc:9:26: note: in expansion of macro 'gravity'
```

其次，调试宏定义相关代码通常比较困难。尽管源代码中有宏的名称，但编译器和调试器从未看到该宏，因为在此之前已被替换。许多调试器无法检查宏的值，并且对宏的支持通常有限。

第三，宏替换的行为与C++中的其他所有操作行为都不同。因此，很容易发生无意的错误。

常变量没有这些问题：它们遵循正常的作用域规则，可以被编译器和调试器看到，并且行为一致。

{{< alert success >}}
**最佳实践**

定义常量时，不推荐使用类对象宏。

{{< /alert >}}

***
## 在多文件程序中使用常变量

在许多应用程序中，需要在整个代码中使用给定的命名常量（而不仅仅是在一个文件中）。例如不改变的物理或数学常数（例如，pi或阿伏伽德罗数），或特定于应用的“调谐”值（例如，摩擦系数或重力系数）。与其每次需要它们时都重新定义它们，不如在特定位置声明它们一次，并在需要的地方使用它们。这样，如果你需要改变它们，你只需要在一个地方改变它们。

在C++中有多种方法来完成这一点——我们在后续章节中详细介绍了这个主题——在多个文件中共享全局常量（使用内联变量）。

***
## 类型限定符

类型限定符（有时简称为限定符）是应用于修改类型行为方式的关键字。用于声明常变量的const称为常量类型限定符（简称为常量限定符）。

截至C++23，C++只有两个类型限定符：const和volatile。

{{< alert success >}}
**可选阅读**

volatile限定符用于告诉编译器对象的值可以随时更改。这个很少使用的限定符禁用某些类型的优化。

在技术文档中，const和volatile限定符通常被称为cv限定符。C++标准中也使用了以下术语：

1. 非cv限定类型（cv-unqualified）是没有类型限定符的类型（例如int）。
2. cv限定类型（cv-qualified）是应用了一个或多个类型限定符的类型（例如，const int）。
3. 可能cv限定类型（possibly cv-qualified）是可以是cv不限定或cv限定的类型。

这些术语在技术文档之外很少使用，因此这里列出它们是为了参考，而不是需要记住的东西。

{{< /alert >}}

***

{{< prevnext prev="/basic/chapter4/summary/" next="/basic/chapter5/const-exp/" >}}
4.12 第4章总结
<--->
5.1 常量表达式、编译时常量和运行时常量
{{< /prevnext >}}
