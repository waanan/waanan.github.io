---
title: "模板别名"
date: 2024-03-08T13:20:57+08:00
---

在前面，我们讨论了如何使用typedef或者using来定义现有类型的别名。

为类模板创建别名的方式类似：

```C++
#include <iostream>

template <typename T>
struct Pair
{
    T first{};
    T second{};
};

template <typename T>
void print(const Pair<T>& p)
{
    std::cout << p.first << ' ' << p.second << '\n';
}

int main()
{
    using Point = Pair<int>; // 创建类型别名
    Point p { 1, 2 };        // 编译器会把 Point 替换为 Pair<int>

    print(p);

    return 0;
}
```

这样的别名可以在局部作用域（例如在函数内部）或全局定义。

***
## 模板别名（Alias Template）

在其他情况下，可能需要直接为模板本身创建别名。为此，可以定义模板别名，这是一个可用于实例化类型的模板的另外名称。就像类型别名不定义不同类型一样，模板别名也不定义不同的模板。

下面是一个示例：

```C++
#include <iostream>

template <typename T>
struct Pair
{
    T first{};
    T second{};
};

// 这里是模板别名
// 模板别名必须定义在全局作用域里
template <typename T>
using Coord = Pair<T>; // Coord 是 Pair<T> 的别名

// print 函数里，需要知道 T 也是 Coord 的模板类型参数
template <typename T>
void print(const Coord<T>& c)
{
    std::cout << c.first << ' ' << c.second << '\n';
}

int main()
{
    Coord<int> p1 { 1, 2 }; // C++-20 之前: 必须显示指定模板类型参数
    Coord p2 { 1, 2 };      // 在 C++20, 可以使用CTAD进行自动推导

    std::cout << p1.first << ' ' << p1.second << '\n';
    print(p2);

    return 0;
}
```

在本例中，将Coord定义为Pair的别名。Coord\<T\>是Pair\<T\>的实例化类型的别名。定义完成后，可以在使用Pair的地方使用Coord，在使用Pair\<T\>的地方使用Coord\<T\>。

关于这个例子，有几点值得注意。

首先，与普通类型别名（可以在块内定义）不同，模板别名必须在全局作用域内定义（与所有模板一样）。

其次，在C++20之前，当使用别名模板实例化对象时，必须显式指定模板参数。从C++20开始，可以使用别名模板推导，别名类型将与CTAD一起生效，它将从初始值设定项中推断模板参数的类型。

第三，由于CTAD不适用于函数参数，因此当使用模板别名作为函数参数时，必须显式定义模板别名使用的模板参数。换句话说，这样做：

```C++
template <typename T>
void print(const Coord<T>& c)
{
    std::cout << c.first << ' ' << c.second << '\n';
}
```

而不是这样：

```C++
void print(const Coord& c) // 无法编译, 缺少模板参数
{
    std::cout << c.first << ' ' << c.second << '\n';
}
```

这与使用Pair\<T\>没有区别。

***