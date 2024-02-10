---
title: "函数的类型推导"
date: 2024-01-31T13:21:38+08:00
---

考虑以下程序：

```C++
int add(int x, int y)
{
    return x + y;
}
```

编译此函数时，编译器将确定x+y的计算结果为int，然后确保返回值的类型与函数的声明返回类型匹配（或者返回值类型可以转换为声明的返回类型）。

由于编译器必须从return语句中推断返回类型，因此在C++14中，auto关键字被扩展为，可以推导函数返回类型。通过使用auto关键字代替函数的返回类型来实现。

例如：

```C++
auto add(int x, int y)
{
    return x + y;
}
```

由于return语句返回一个int值，编译器将推断该函数的返回类型为int。

使用auto返回类型时，函数中的所有返回语句都必须返回相同类型的值，否则将导致错误。例如：

```C++
auto someFcn(bool b)
{
    if (b)
        return 5; // return 类型 int
    else
        return 6.7; // return 类型 double
}
```

在上面的函数中，两个return语句返回不同类型的值，因此编译器将报错。

如果出于某种原因需要这种情况，则可以显式指定函数的返回类型（在这种情况下，编译器将尝试将任何不匹配的返回表达式隐式转换为显式返回的类型），或者可以显式将所有返回语句转换为同一类型。在上面的示例中，可以通过将5更改为5.0来修改程序编译通过。

使用自动返回类型的函数的一个主要缺点是，在使用这些函数之前，必须完全定义它们（向前声明是不够的）。例如：

```C++
#include <iostream>

auto foo();

int main()
{
    std::cout << foo() << '\n'; // 编译器这里只能看到前向声明

    return 0;
}

auto foo()
{
    return 5;
}
```

在作者的机器上，这会产生以下编译错误：

```C++
error C3779: 'foo': a function that returns 'auto' cannot be used before it is defined.
```

这是有意义的：前向声明没有足够的信息供编译器推断函数的返回类型。这意味着返回auto的普通函数通常只在从定义它们的文件中调用。

与对象的类型推导不同，在函数返回类型推导的最佳实践方面没有太多共识。当在对象上使用类型推导时，初始值设定项总是作为同一语句的一部分出现，因此确定将要推导的类型通常不会过于繁琐。对于函数，情况并非如此——当查看函数的原型时，没有上下文来帮助指示函数返回的类型。一个好的编程IDE应该可以判断出函数的导出类型是什么。但在没有可用工具的情况下，用户实际上必须挖掘函数体本身，以确定函数返回的类型。犯错误的几率更高。并且这种函数不能被前向声明，限制了它们在多文件程序中的有用性。

{{< alert success >}}
**最佳实践**

对于普通函数，使用显式返回类型，而不是函数返回类型推导。

{{< /alert >}}

***
## 尾部返回类型语法

auto关键字还可以用于使用尾部返回语法声明函数，其中返回类型在函数原型的其余部分之后指定。

考虑以下函数：

```C++
int add(int x, int y)
{
  return (x + y);
}
```

使用尾部返回语法，这可以等效地写为：

```C++
auto add(int x, int y) -> int
{
  return (x + y);
}
```

在这种情况下，auto不执行类型推导 —— 它是使用尾部返回类型的语法的一部分。

为什么要使用此功能？

一个好的方面是它使所有函数名对齐：

```C++
auto add(int x, int y) -> int;
auto divide(double x, double y) -> double;
auto printSomething() -> void;
auto generateSubstring(const std::string &s, int start, int len) -> std::string;
```

C++的一些高级功能也需要尾部返回语法，例如lambda函数（在后续介绍）。

目前，我们建议继续使用传统的函数返回语法，除非在需要尾部返回语法的情况下。

***
## 类型推导不能用于函数参数的类型

许多了解类型推导的新程序员尝试这样做：

```C++
#include <iostream>

void addAndPrint(auto x, auto y)
{
    std::cout << x + y << '\n';
}

int main()
{
    addAndPrint(2, 3); // case 1: 使用int参数调用
    addAndPrint(4.5, 6.7); // case 2: 使用double参数调用

    return 0;
}
```

不幸的是，类型推导不适用于函数参数，在C++20之前，上述程序将无法编译（您将得到一个关于函数参数不能自动类型推导的错误）。

在C++20中，对auto关键字进行了扩展，以便上面的程序能够正确编译和运行——然而，在这种情况下，auto并没有调用类型推导。相反，它触发了一个称为函数模板的功能，该功能旨在实际处理此类情况。

{{< alert success >}}
**相关内容**

这里的auto关键字在函数模版章节进行讲解。

{{< /alert >}}

***

{{< prevnext prev="/basic/chapter10/auto-type-object/" next="/basic/chapter10/summary/" >}}
10.7 使用auto关键字的对象类型自动推导
<--->
10.9 第10章总结
{{< /prevnext >}}
