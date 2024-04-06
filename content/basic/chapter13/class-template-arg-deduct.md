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

如果您在C++17中编译它，您可能会得到关于“类模板参数演绎失败”或“无法演绎模板参数”或“没有可行的构造函数或演绎指南”的错误。这是因为在C++17中，CTAD不知道如何推导聚合类模板的模板参数。为了解决这个问题，我们可以为编译器提供一个演绎指南，该指南告诉编译器如何推导给定类模板的模板参数。

下面是具有扣除指南的相同计划：

```C++
template <typename T, typename U>
struct Pair
{
    T first{};
    U second{};
};

// Here's a deduction guide for our Pair (needed in C++17 only)
// Pair objects initialized with arguments of type T and U should deduce to Pair<T, U>
template <typename T, typename U>
Pair(T, U) -> Pair<T, U>;
    
int main()
{
    Pair<int, int> p1{ 1, 2 }; // explicitly specify class template Pair<int, int> (C++11 onward)
    Pair p2{ 1, 2 };           // CTAD used to deduce Pair<int, int> from the initializers (C++17)

    return 0;
}
```

这个例子应该在C++17下编译。

Pair类的演绎指南非常简单，但让我们仔细看看它是如何工作的。

```C++
// Here's a deduction guide for our Pair (needed in C++17 only)
// Pair objects initialized with arguments of type T and U should deduce to Pair<T, U>
template <typename T, typename U>
Pair(T, U) -> Pair<T, U>;
```

首先，我们使用与Pair类中相同的模板类型定义。这是有意义的，因为如果我们的演绎指南要告诉编译器如何演绎Pair<T，U>的类型，我们必须定义T和U是什么（模板类型）。其次，在箭头的右侧，我们有一个类型，我们正在帮助编译器推导它。在这种情况下，我们希望编译器能够为Pair<T，U>类型的对象推导模板参数，因此这正是我们在这里放置的。最后，在箭头的左侧，我们告诉编译器要查找哪种声明。在这种情况下，我们告诉它查找一个名为Pair的对象的声明，该对象具有两个参数（一个是T类型，另一个是U类型）。我们也可以将其写为Pair（T T，U U）（其中T和U是参数的名称，但由于我们不使用T和U，因此不需要为它们命名）。

将它们放在一起，我们告诉编译器，如果它看到一个具有两个参数的Pair的声明（分别为T和U类型），它应该将类型推断为Pair<T，U>。

因此，当编译器看到定义对p2{1，2}时；在我们的程序中，它会说，“哦，这是Pair的声明，并且有两个int和int类型的参数，因此使用演绎指南，我应该将其演绎为Pair<int，int>”。

下面是采用单个模板类型的Pair的类似示例：

```C++
template <typename T>
struct Pair
{
    T first{};
    T second{};
};

// Here's a deduction guide for our Pair (needed in C++17 only)
// Pair objects initialized with arguments of type T and T should deduce to Pair<T>
template <typename T>
Pair(T, T) -> Pair<T>;

int main()
{
    Pair<int> p1{ 1, 2 }; // explicitly specify class template Pair<int> (C++11 onward)
    Pair p2{ 1, 2 };      // CTAD used to deduce Pair<int> from the initializers (C++17)

    return 0;
}
```

在这种情况下，我们的演绎指南将Pair（T，T）（具有两个类型T的参数的Pair）映射到Pair<T>。

{{< alert success >}}
**提示**

C++20增加了编译器自动为聚合生成演绎指南的功能，因此只需要为C++17兼容性提供演绎指南。

因此，没有演绎指南的Pair版本应该在C++20中编译。

std:：pair（和其他标准库模板类型）附带预定义的演绎指南，这就是为什么我们上面使用std:∶pair的示例在C++17中编译得很好，而不需要我们自己提供演绎指南。

{{< /alert >}}

{{< alert success >}}
**对于高级读者**

在C++17中，非聚合不需要演绎指南，因为构造函数的存在具有相同的用途。

{{< /alert >}}

***
## 使用默认值键入模板参数

就像函数参数可以有默认参数一样，模板参数也可以给定默认值。当模板参数未显式指定且无法推导时，将使用这些参数。

下面是对上面的Pair<T，U>类模板程序的修改，类型模板参数T和U默认为类型int：

```C++
template <typename T=int, typename U=int> // default T and U to type int
struct Pair
{
    T first{};
    U second{};
};

template <typename T, typename U>
Pair(T, U) -> Pair<T, U>;

int main()
{
    Pair<int, int> p1{ 1, 2 }; // explicitly specify class template Pair<int, int> (C++11 onward)
    Pair p2{ 1, 2 };           // CTAD used to deduce Pair<int, int> from the initializers (C++17)

    Pair p3;                   // uses default Pair<int, int>

    return 0;
}
```

我们对p3的定义没有显式地指定类型模板参数的类型，也没有用于推导这些类型的初始值设定项。因此，编译器将使用默认值中指定的类型，这意味着p3的类型为Pair<int，int>。

***
## CTAD不适用于非静态成员初始化

使用非静态成员初始化初始化类类型的成员时，CTAD在此上下文中不起作用。必须显式指定所有模板参数：

```C++
#include <utility> // for std::pair

struct Foo
{
    std::pair<int, int> p1{ 1, 2 }; // ok, template arguments explicitly specified
    std::pair p2{ 1, 2 };           // compile error, CTAD can't be used in this context
};

int main()
{
    std::pair p3{ 1, 2 };           // ok, CTAD can be used here
    return 0;
}
```

***
## CTAD不与功能参数一起工作

CTAD代表类模板参数演绎，而不是类模板参数推导，因此它将仅演绎模板参数的类型，而不是模板参数。

因此，CTAD不能用于功能参数。

```C++
#include <iostream>
#include <utility>

void print(std::pair p) // compile error, CTAD can't be used here
{
    std::cout << p.first << ' ' << p.second << '\n';
}

int main()
{
    std::pair p { 1, 2 }; // p deduced to std::pair<int, int>
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
    std::pair p { 1, 2 }; // p deduced to std::pair<int, int>
    print(p);

    return 0;
}
```

