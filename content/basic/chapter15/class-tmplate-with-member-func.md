---
title: "具有成员函数的类模板"
date: 2024-06-24T18:56:16+08:00
---

在前面，我们学习了函数模版：

```C++
template <typename T> // 模版参数声明
T max(T x, T y) // 函数模版 max<T> 定义
{
    return (x < y) ? y : x;
}
```

使用函数模板，可以定义类型模板参数（例如，类型名T），然后将它们用作函数参数 (T x, T y) 的类型。

同时我们也介绍了类模板，它允许为类类型（结构体、类和联合）的数据成员的类型使用类型模板参数：

```C++
#include <iostream>

template <typename T>
struct Pair
{
    T first{};
    T second{};
};

// 这里是我们自定义的 Pair 的推导 (需要在 C++17 以上版本使用)
// Pair 以两个参数 T 和 T初始化，会被推导为 Pair<T>
template <typename T>
Pair(T, T) -> Pair<T>;

int main()
{
    Pair<int> p1{ 5, 6 };        // 实例化 Pair<int> 并创建对象 p1
    std::cout << p1.first << ' ' << p1.second << '\n';

    Pair<double> p2{ 1.2, 3.4 }; // 实例化 Pair<double> 并创建对象 p2
    std::cout << p2.first << ' ' << p2.second << '\n';

    Pair<double> p3{ 7.8, 9.0 }; // 创建对象 p3，使用之前实例化的 Pair<double>
    std::cout << p3.first << ' ' << p3.second << '\n';

    return 0;
}
```

在本课中，将结合函数模板和类模板的元素，以便更仔细地查看具有成员函数的类模板。

***
## 在成员函数中键入模板参数

模版参数，既可以作为成员变量的类型，也可以作为成员函数参数的类型。

在下面的示例中，重写了上面的Pair类模板，将其从结构体转换为类：

```C++
#include <ios>       // for std::boolalpha
#include <iostream>

template <typename T>
class Pair
{
private:
    T m_first{};
    T m_second{};

public:
    // 在类中定义成员函数
    // 模版参数是类声明时的模版参数
    Pair(const T& first, const T& second)
        : m_first{ first }
        , m_second{ second }
    {
    }

    bool isEqual(const Pair<T>& pair);
};

// 在类外部定义成员函数
// 需要重新提供模版参数声明
template <typename T>
bool Pair<T>::isEqual(const Pair<T>& pair)
{
    return m_first == pair.m_first && m_second == pair.m_second;
}

int main()
{
    Pair p1{ 5, 6 }; // 使用 CTAD 来推导 Pair<int>
    std::cout << std::boolalpha << "isEqual(5, 6): " << p1.isEqual( Pair{5, 6} ) << '\n';
    std::cout << std::boolalpha << "isEqual(5, 7): " << p1.isEqual( Pair{5, 7} ) << '\n';

    return 0;
}
```

上面的内容应该非常简单，但有几点值得注意。

首先，因为类具有私有成员，所以它不是聚合，因此不能使用聚合初始化。相反，必须使用构造函数初始化类对象。

由于类数据成员的类型为T，因此将构造函数类型的参数设置为const T&，因此用户可以提供相同类型的初始化值。由于T的复制成本可能很高，因此通过常量引用传递比通过值传递更安全。

注意，当在类模板定义中定义成员函数时，不需要为成员函数提供模板参数声明。这样的成员函数隐式使用类模板参数声明。

其次，可以使用CTAD，提供初始值匹配构造函数，让编译器来自动推断模板参数所需的信息。

让我们更仔细地看一下在类模板定义之外为类模板定义成员函数的情况：

```C++
template <typename T>
bool Pair<T>::isEqual(const Pair<T>& pair)
{
    return m_first == pair.m_first && m_second == pair.m_second;
}
```

由于该成员函数定义与类模板定义是分开的，因此需要重新提供模板参数声明（template \<typename T\>），以便编译器知道T是什么。

此外，当在类之外定义成员函数时，需要用类模板的完全模板化名称（Pair\<T\>::isEqual，而不是Pair::isEqual）来限定成员函数名称。

***
## 如何在类模板外部定义成员函数

对于类模板的成员函数，编译器需要查看类定义（以确保将成员函数模板声明为类的一部分）和模板成员函数定义（了解如何实例化模板）。因此，通常希望在同一位置定义类及其成员函数模板。

当在类内部中定义成员函数模板时，模板成员函数定义是类定义的一部分，因此，只要可以看到类定义，就可以看到模板成员函数的定义。这使得事情变得容易（以类定义比较乱为代价）。

当成员函数模板在类之外定义时，通常应在类定义的正下方定义它。这样，在任何可以看到类定义的地方，也将看到类定义下面的成员函数模板定义。

在类在头文件中定义的典型情况下，这意味着在类之外定义的任何成员函数模板也应该在类定义下面的相同头文件中进行定义。

{{< alert success >}}
**关键点**

在前面，我们知道从模板隐式实例化的函数是隐式内联的。这包括非成员和成员函数模板。因此，将头文件中定义的成员函数模板包含到多个代码文件中没有问题，因为从这些模板实例化的函数将隐式内联（并且链接器将消除它们的重复）。

{{< /alert >}}

{{< alert success >}}
**最佳实践**

在类定义之外定义的任何成员函数模板都应该在类定义的正下方定义（在同一文件中）。

{{< /alert >}}

***

{{< prevnext prev="/basic/chapter15/destruct-intro/" next="/basic/chapter15/static-member-var/" >}}
15.3 析构函数简介
<--->
15.5 静态成员变量
{{< /prevnext >}}
