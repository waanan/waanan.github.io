---
title: "前向声明"
date: 2023-10-09T20:06:10+08:00
---

看看这个看似没有问题的示例程序：

```C++
#include <iostream>

int main()
{
    std::cout << "The sum of 3 and 4 is: " << add(3, 4) << '\n';
    return 0;
}

int add(int x, int y)
{
    return x + y;
}
```

您希望该程序产生以下结果：

```C++
The sum of 3 and 4 is: 7
```

但事实上，它根本无法编译通过！Visual Studio生成以下编译错误：

```C++
add.cpp(5) : error C3861: 'add': identifier not found
```

该程序编译失败的原因是编译器按顺序编译代码文件的内容。因为我们直到第9行才定义add，当编译器在main的第5行到达add的函数调用时，它不知道add是什么。

有两种常见的方法来解决这个问题。

***
## 选项1：重新排序函数定义

解决该问题的一种方法是重新排序函数定义，以便在main之前定义add：

```C++
#include <iostream>

int add(int x, int y)
{
    return x + y;
}

int main()
{
    std::cout << "The sum of 3 and 4 is: " << add(3, 4) << '\n';
    return 0;
}
```

这样，到main调用add时，编译器将已经知道什么是add。因为这是一个如此简单的程序，所以这种更改相对容易做。然而，在较大的程序中，试图弄清楚哪些函数调用哪些其他函数（以及以什么顺序），以便可以按顺序声明它们，可能会很繁琐。

此外，这种方法并不总是可行的。假设我们正在编写一个有两个函数A和B的程序。如果函数A调用函数B，函数B调用函数A，那么就没有办法对函数进行排序。如果首先定义A，编译器将告警它不知道B是什么。如果首先定义B，编译器将告警它不知道A是什么。

***
## 选项2：使用前向声明

我们还可以通过使用前向声明来修复此问题。

前向声明允许我们在实际定义标识符之前告诉编译器标识符的存在。

对于函数，这允许我们在定义函数体之前告诉编译器函数的存在。这样，当编译器遇到对函数的调用时，它将理解我们正在进行函数调用，并可以检查以确保我们正确调用了函数，即使它还不知道如何或在何处定义函数。

为了编写函数的前向声明，我们使用函数声明语句（也称为函数原型）。函数声明由函数的返回类型、名称和参数类型组成，以分号结尾。可以选择包括参数的名称。声明中不包括函数体。

下面是add函数的函数声明：

```C++
int add(int x, int y); // function declaration includes return type, name, parameters, and semicolon.  No function body!
```

下面是我们的原始程序，它没有编译，使用函数声明作为函数add的前向声明：

```C++
#include <iostream>

int add(int x, int y); // forward declaration of add() (using a function declaration)

int main()
{
    std::cout << "The sum of 3 and 4 is: " << add(3, 4) << '\n'; // this works because we forward declared add() above
    return 0;
}

int add(int x, int y) // even though the body of add() isn't defined until here
{
    return x + y;
}
```

现在，当编译器到达main中对add的调用时，它将知道add是什么样子的（接受两个整数参数并返回一个整数的函数），并且它不会抱怨。

值得注意的是，函数声明不需要指定参数的名称（因为它们不被视为函数声明的一部分）。在上面的代码中，您还可以如下转发声明函数：

```C++
int add(int, int); // valid function declaration
```

然而，我们更喜欢命名参数（使用与实际函数相同的名称），因为它允许您通过查看声明来理解函数参数是什么。否则，您必须找到函数定义。

{{< alert success >}}
**最佳做法**

在函数声明中保留参数名。

{{< /alert >}}

{{< alert success >}}
**提示**

通过复制/粘贴函数的标头并添加分号，可以轻松创建函数声明。

{{< /alert >}}

***
## 为什么要转发声明？

您可能想知道，如果我们可以重新排序函数以使程序工作，为什么要使用前向声明。

大多数情况下，前向声明用于告诉编译器存在在不同代码文件中定义的某个函数。在这种情况下，无法重新排序，因为调用者和被调用者位于完全不同的文件中！我们将在下一课（2.8——具有多个代码文件的程序）中更详细地讨论这一点。

前向声明也可以用于以不确定顺序的方式定义函数。这允许我们以最大化组织（例如，通过将相关功能聚集在一起）或读者理解的任何顺序来定义功能。

不太常见的是，有时我们有两个函数相互调用。在这种情况下，也不可能重新排序，因为没有办法重新排序函数，使每个函数都在另一个之前。前向声明为我们提供了一种解决这种循环依赖性的方法。

***
## 忘记函数体

新程序员经常想知道，如果他们前向声明一个函数，但不定义它会发生什么。

答案是：视情况而定。如果进行了前向声明，但从未调用函数，则程序将编译并正常运行。然而，如果进行了前向声明并调用了函数，但程序从未定义函数，则程序将编译正常，但链接器将抱怨它无法解析函数调用。

考虑以下程序：

```C++
#include <iostream>

int add(int x, int y); // forward declaration of add()

int main()
{
    std::cout << "The sum of 3 and 4 is: " << add(3, 4) << '\n';
    return 0;
}

// note: No definition for function add
```

在这个程序中，我们向前声明add，并调用add，但我们从未在任何地方定义add。尝试编译此程序时，Visual Studio会生成以下消息：

正如您所看到的，程序编译良好，但它在链接阶段失败，因为从未定义intadd（int，int）。

***
## 其他类型的远期申报

前向声明最常用于函数。然而，前向声明也可以与C++中的其他标识符一起使用，例如变量和类型。变量和类型具有不同的前向声明语法，因此我们将在以后的课程中介绍这些。

***
## 声明与定义

在C++中，您会经常听到使用“声明”和“定义”两个词，并且通常可以互换。它们是什么意思？你现在有了足够的基础知识来理解两者之间的区别。

声明告诉编译器标识符的存在及其关联的类型信息。下面是一些声明示例：

```C++
int add(int x, int y); // tells the compiler about a function named "add" that takes two int parameters and returns an int.  No body!
int x;                 // tells the compiler about an integer variable named x
```

定义是一个声明，它实际实现（对于函数和类型）或实例化（对于变量）标识符。

下面是一些定义示例：

```C++
int add(int x, int y) // implements function add()
{
    int z{ x + y };   // instantiates variable z

    return z;
}

int x;                // instantiates variable x
```

在C++中，所有定义都是声明。因此为int x；既是定义又是声明。

相反，并不是所有的声明都是定义。不是定义的声明称为纯声明。纯声明的类型包括函数、变量和类型的前向声明。

当编译器遇到标识符时，它将进行检查以确保该标识符的使用有效（例如，该标识符在范围内，以语法有效的方式使用，等等）。

在大多数情况下，声明足以允许编译器确保正确使用标识符。例如，当编译器遇到函数调用add（5，6）时，如果它已经看到add（int，int）的声明，那么它可以验证add实际上是一个接受两个int参数的函数。它不需要实际看到函数add的定义（可能存在于其他文件中）。

然而，在一些情况下，编译器必须能够看到完整的定义才能使用标识符（例如，对于模板定义和类型定义，我们将在以后的课程中讨论这两种定义）。

下面是一个摘要表：

{{< alert success >}}
**作者注释**

在通用语言中，术语“声明”通常用于表示“纯声明”，“定义”用于表示“也用作声明的定义”。因此，我们通常称为intx；定义，即使它既是定义又是声明。

{{< /alert >}}

***
## 一个定义规则（ODR）

单定义规则（简称ODR）是C++中众所周知的规则。ODR由三部分组成：

违反ODR的第1部分将导致编译器发出重新定义错误。违反ODR第2部分将导致链接器发出重新定义错误或导致未定义的行为。违反ODR第3部分将导致未定义的行为。

下面是违反第1部分的示例：

```C++
int add(int x, int y)
{
     return x + y;
}

int add(int x, int y) // violation of ODR, we've already defined function add
{
     return x + y;
}

int main()
{
    int x;
    int x; // violation of ODR, we've already defined x
}
```

由于上述程序违反ODR第1部分，这导致Visual Studio编译器发出以下编译错误：

ODR不适用于纯声明（它是一个定义规则，而不是一个声明规则），因此可以根据需要为标识符提供任意多的纯声明（尽管有多个纯声明是多余的）。

{{< alert success >}}
**对于高级读者**

共享标识符但具有不同参数的函数被认为是不同的函数。我们将在第10.10课中进一步讨论这一点——函数重载简介

{{< /alert >}}

***

{{< prevnext prev="/basic/chapter2/why-func/" next="/" >}}
2.5 为什么需要函数
<--->
主页
{{< /prevnext >}}
