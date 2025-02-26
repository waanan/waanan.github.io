---
title: "函数模板特化"
date: 2025-01-22T20:47:14+08:00
---

当为给定类型实例化函数模板时，编译器模板化出函数的副本，并用变量声明中使用的实际类型替换模板类型参数。这意味着特定的函数将对每个实例化类型具有相同的实现细节（只是使用不同的类型）。虽然大多数时候这正是您想要的，但有时对于特定的数据类型，以稍微不同的方式实现模板化函数是有用的。

***
## 使用非模板函数

考虑以下示例：

```C++
#include <iostream>

template <typename T>
void print(const T& t)
{
    std::cout << t << '\n';
}

int main()
{
    print(5);
    print(6.7);
    
    return 0;
}
```

这将打印：

```C++
5
6.7
```

现在，假设我们希望以科学记数法输出double值（并且只对double值生效该逻辑）。

为给定类型获取不同行为的一种方法是定义非模板函数：

```C++
#include <iostream>

template <typename T>
void print(const T& t)
{
    std::cout << t << '\n';
}

void print(double d)
{
    std::cout << std::scientific << d << '\n';
}

int main()
{
    print(5);
    print(6.7);
    
    return 0;
}
```

当编译器解析print(6.7)时，它将看到我们已经定义了print(double)，并使用它来代替从print(const T&)实例化版本。

这将产生以下结果：

```C++
5
6.700000e+000
```

以这种方式定义函数的一个好处是，非模板函数不需要与函数模板具有相同的签名。请注意，print(const T&)传递常量引用，而print(double)传递值。

通常，如果非模板函数可用，则优先定义该类函数。

***
## 函数模板特化

实现类似结果的另一种方法是使用显式模板特化。显式模板特化是一种功能，允许我们为特定类型或值显式定义模板的不同实现。当所有模板参数都被特化时，它被称为完全特化。当只有一些模板参数被特化时，它被称为部分特化。

当T是double时，让我们创建打印的特化函数：

```C++
#include <iostream>

// 这是原始的模版 (必须写在前面)
template <typename T>
void print(const T& t)
{
    std::cout << t << '\n';
}

// template print<T> 对于 double 的一个完全特化版本
// 完全特化不是隐式 inline, 所以将它放到头文件时，需要添加 inline 标记
template<>                          // 模版参数声明里，没有任何声明的参数
void print<double>(const double& d) // 针对 double 类型特化
{
    std::cout << std::scientific << d << '\n'; 
}

int main()
{
    print(5);
    print(6.7);
    
    return 0;
}
```

为了特化模板，编译器首先必须看到原始的模板声明。上例中的原始模板是print\<T\>(const T&)。

现在，让我们仔细看看我们的函数模板特化：

```C++
template<>                          // 模版参数声明里，没有任何声明的参数
void print<double>(const double& d) // 针对 double 类型特化
```

首先，我们需要一个模板参数声明，以便编译器知道我们正在做与模板相关的事情。然而，在这种情况下，我们实际上不需要任何模板参数，因此我们使用一对空的尖括号。由于在特化中没有模板参数，因此这是一个完全特化。

在下一行，print\<double\>告诉编译器，我们正在特化类型double的print原始模板函数。特化必须具有与原始模板有相同的函数签名（除了特化在原始模板使用T的任何地方替换double）。由于原始模板具有 「const T&」 类型的参数，因此特化必须具有「const double&」类型的形参。当原始模板传递引用时，特化不能传递值（反之亦然）。

此示例打印与上面相同的结果。

请注意，如果匹配的非模板函数和匹配的模板函数特化都存在，则非模板函数将优先被使用。此外，完全特化不是隐式内联的，因此如果在头文件中定义一个，请确保内联它，以避免ODR冲突。

与普通函数一样，如果希望解析为特化的任何函数调用产生编译错误，则可以删除函数模板特化（使用=delete）。

通常，您应该尽可能避免函数模板特化，而使用非模板函数。

{{< alert success >}}
**警告**

完全特化不是隐式内联的（部分特化是隐式内联的）。如果在头文件中放置完全特化，则应将其标记为内联，以便在它被包含到多个翻译单元中时不会导致ODR冲突。

{{< /alert >}}

***
## 成员函数的模板特化？

现在考虑以下类模板：

```C++
#include <iostream>

template <typename T>
class Storage
{
private:
    T m_value {};
public:
    Storage(T value)
      : m_value { value }
    {
    }

    void print()
    {
        std::cout << m_value << '\n';
    }
};

int main()
{
    // 定义一些Storage
    Storage i { 5 };
    Storage d { 6.7 };

    // 打印
    i.print();
    d.print();
}
```

这将打印：

```C++
5
6.7
```

假设我们再次希望创建一个版本的print()函数，该函数以科学记数法打印double。然而，这次print()是成员函数，因此不能定义非成员函数。那么我们该怎么做呢？

尽管看起来我们需要在这里使用函数模板特化，但这是错误的工具。请注意，i.print()调用Storage\<int\>::print()，d.print()调用Storage\<double\>::print()。因此，如果我们想在T是double时更改此函数的行为，我们需要特化Storage\<double\>::print()，这是一个类模板特化，而不是函数模板特化！

那么该怎么做呢？我们将在下一课中讨论类模板特化。

***

{{< prevnext prev="/basic/chapter26/no-type-template-param/" next="/basic/chapter26/class-template-specialization/" >}}
26.1 模板非类型参数
<--->
26.3 类模板特化
{{< /prevnext >}}
