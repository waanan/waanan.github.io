---
title: "类模板参数推导（CTAD）"
date: 2024-03-08T13:20:57+08:00
---

***
## 类模板参数推导（Class template argument deduction，CTAD）（C++17）

从C++17开始，当从类模板实例化对象时，编译器可以从对象的初始值的类型推断模板参数类型（这称为类模板参数推导或简称CTAD）。例如：

```C++
#include <utility> // for std::pair

int main()
{
    std::pair<int, int> p1{ 1, 2 }; // 显示声明 std::pair<int, int> (C++11)
    std::pair p2{ 1, 2 };           // CTAD，从初始值列表推导 std::pair<int, int> (C++17)

    return 0;
}
```

仅当不存在模板参数列表时才执行CTAD。因此，以下两项都是错误：

```C++
#include <utility> // for std::pair

int main()
{
    std::pair<> p1 { 1, 2 };    // error: 模版参数太少, 2个模版参数都缺少了
    std::pair<int> p2 { 3, 4 }; // error: 模版参数太少, 第二个模版参数缺少

    return 0;
}
```

由于CTAD是类型推导的一种形式，因此可以使用字面值后缀来更改推导的类型：

```C++
#include <utility> // for std::pair

int main()
{
    std::pair p1 { 3.4f, 5.6f }; // 推导为 pair<float, float>
    std::pair p2 { 1u, 2u };     // 推导为 pair<unsigned int, unsigned int>

    return 0;
}
```

{{< alert success >}}
**注**

本网站上的许多未来课程都使用CTAD。如果您使用C++14标准（或更早版本）编译这些示例，您将得到一个缺少模板参数的错误。需要将这些参数显式添加到示例中，以使其可编译。

{{< /alert >}}

***
## 模板参数推导指南（C++17）

在大多数情况下，CTAD是开箱即用的。然而，在某些情况下，编译器可能需要一些额外的帮助来理解如何正确推导模板参数。

您可能会惊讶地发现，以下程序（几乎与上面使用std::pair的示例相同）不能在C++17中编译：

```C++
// 自定义 Pair 类型
template <typename T, typename U>
struct Pair
{
    T first{};
    U second{};
};

int main()
{
    Pair<int, int> p1{ 1, 2 }; // ok: 显示指定模版参数
    Pair p2{ 1, 2 };           // C++17 中编译失败 (C++20 可以编译)

    return 0;
}
```

如果在C++17中编译它，可能会得到“类模板参数推导失败”或“无法推导模板参数”或“没有可行的构造函数或推导指引”的错误。这是因为在C++17中，CTAD不知道如何推导聚合类模板的模板参数。为了解决这个问题，需要为编译器提供一个演绎指引，告诉编译器如何推导给定类模板的模板参数。

下面是具体的样例：

```C++
template <typename T, typename U>
struct Pair
{
    T first{};
    U second{};
};

// 这是我们定义的 Pair 类型的推导指引 (只在 C++17 中必须)
// Pair 对象使用 T 和 U 参数初始化，类型推导为 Pair<T, U>
template <typename T, typename U>
Pair(T, U) -> Pair<T, U>;
    
int main()
{
    Pair<int, int> p1{ 1, 2 }; // 显示声明 std::pair<int, int> (C++11)
    Pair p2{ 1, 2 };           // CTAD，从初始值列表推导 std::pair<int, int> (C++17)

    return 0;
}
```

这个例子可以在C++17下编译。

Pair类的演绎指引非常简单，让我们仔细看看它是如何工作的。

```C++
// 这是我们定义的 Pair 类型的推导指引 (只在 C++17 中必须)
// Pair 对象使用 T 和 U 参数初始化，类型推导为 Pair<T, U>
template <typename T, typename U>
Pair(T, U) -> Pair<T, U>;
```

首先，使用与Pair类中相同的模板类型参数定义。因为如果我们的推导指南要告诉编译器如何推导Pair\<T，U\>的类型，必须定义T和U是什么（模板类型）。其次，在箭头的右侧，有一个类型，在帮助编译器推导它。在这种情况下，希望编译器能够为Pair\<T，U\>类型的对象推导模板参数。最后，在箭头的左侧，告诉编译器要查找哪种声明。在这种情况下，告诉它查找一个名为Pair的对象的声明，该对象具有两个参数（一个是T类型，另一个是U类型）。我们也可以将其写为Pair(T t, U t)（其中t和u是参数的名称，但由于不使用t和u，因此不需要为它们命名）。

将它们放在一起，告诉编译器，如果它看到一个具有两个参数的Pair的声明（分别为T和U类型），它应该将类型推断为Pair\<T，U\>。

因此，当编译器看到 p2{1，2}；，它会说，“哦，这是Pair的声明，并且有两个int和int类型的参数，因此使用推导指南，应该将其推导为Pair\<int，int\>”。

下面是采用单个模板类型参数的Pair的类似示例：

```C++
template <typename T>
struct Pair
{
    T first{};
    T second{};
};

// 这是我们定义的 Pair 类型的推导指引 (只在 C++17 中必须)
// Pair 对象使用 T 和 T 参数初始化，类型推导为 Pair<T>
template <typename T>
Pair(T, T) -> Pair<T>;

int main()
{
    Pair<int> p1{ 1, 2 }; // 显示声明 std::pair<int> (C++11)
    Pair p2{ 1, 2 };      // CTAD，从初始值列表推导 std::pair<int> (C++17)

    return 0;
}
```

在这种情况下，我们的推导指南将Pair(T, T)（具有两个类型T作为参数的Pair）映射到Pair\<T\>。

{{< alert success >}}
**提示**

C++20增加了编译器自动为聚合生成推导指南的功能，因此只需要为C++17提供推导指南。

std::pair（和其它标准库模板类型）附带预定义的推导指南，这就是为什么上面使用std::pair的示例在C++17中编译得很好。

{{< /alert >}}

{{< alert success >}}
**对于高级读者**

在C++17中，非聚合不需要推导指南，因为构造函数的存在具有相同的用途。

{{< /alert >}}

***
## 模板参数默认值

就像函数参数可以有默认参数一样，模板参数也可以给定默认值。当模板参数未显式指定且无法推导时，将使用这些参数。

下面是对上面的Pair\<T，U\>类模板程序的修改，模板类型参数T和U默认为类型int：

```C++
template <typename T=int, typename U=int> // T 和 U 默认为 int
struct Pair
{
    T first{};
    U second{};
};

template <typename T, typename U>
Pair(T, U) -> Pair<T, U>;

int main()
{
    Pair<int, int> p1{ 1, 2 }; // 显示声明 std::pair<int, int> (C++11)
    Pair p2{ 1, 2 };           // CTAD，从初始值列表推导 std::pair<int, int> (C++17)

    Pair p3;                   // 使用默认类型 Pair<int, int>

    return 0;
}
```

p3的定义没有显式地指定模板参数，也没有用于推导这些类型的初始值。因此，编译器将使用默认值中指定的类型，这意味着p3的类型为Pair\<int，int\>。

***
## CTAD不适用于非静态成员初始化

为非静态成员设置默认值时，CTAD在此上下文中不起作用。必须显式指定所有模板参数：

```C++
#include <utility> // for std::pair

struct Foo
{
    std::pair<int, int> p1{ 1, 2 }; // ok, 模板参数显示指定
    std::pair p2{ 1, 2 };           // 编译失败, CTAD 在这里不会生效
};

int main()
{
    std::pair p3{ 1, 2 };           // ok, CTAD 可以在这里生效
    return 0;
}
```

***
## CTAD不在函数参数的类型上生效

CTAD代表类模板参数推导，它将只推导给定实际参数的值的情况。

因此，CTAD不能用于函数参数。

```C++
#include <iostream>
#include <utility>

void print(std::pair p) // 编译失败, CTAD 在这里不会生效
{
    std::cout << p.first << ' ' << p.second << '\n';
}

int main()
{
    std::pair p { 1, 2 }; // p 推导 std::pair<int, int>
    print(p);

    return 0;
}
```

在这种情况下，应改用模板：

```C++
#include <iostream>
#include <utility>

template <typename T, typename U>
void print(std::pair<T, U> p)
{
    std::cout << p.first << ' ' << p.second << '\n';
}

int main()
{
    std::pair p { 1, 2 }; // p 推导 std::pair<int, int>
    print(p);

    return 0;
}
```

***

{{< prevnext prev="/basic/chapter13/class-template/" next="/" >}}
13.10 类模板
<--->
主页
{{< /prevnext >}}
