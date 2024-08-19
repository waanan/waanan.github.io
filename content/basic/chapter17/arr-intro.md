---
title: "std::array简介"
date: 2024-08-13T13:06:02+08:00
---

容器和数组，概括的讲:

+ 容器提供对一组对象的存储管理能力
+ 数组会内部的对象在内存中连续存放，因此可以通过元素在数组中的位置快速访问
+ C++有三种不同的常用数组类型: std::vector，std::array，C样式的数组

数组又分为两类:

+ 固定大小的数组。在数组创建的时候，必须固定一个长度，长度之后也不能再修改，std::array和 C样式的数组属于这类
+ 动态数组，可以动态的调整长度，std::vector 输入这种


***
## 那么，为什么不对所有内容都使用动态数组呢？

动态数组功能强大且方便，但与生活中的一切一样，它们在提供的好处方面做出了一些权衡。

1. 与固定大小的数组相比，std::vector的性能稍差。在大多数情况下，您可能不会注意到差异（除非您正在编写导致大量无意重新分配的草率代码）。
2. std::vector仅在非常有限的上下文中支持constexpr。

在现代C++中，真正重要的是后一点。constexpr数组提供了编写更健壮的代码的能力，并且还可以由编译器进行更高的优化。每当可以使用constexpr数组时，都应该这样做——如果需要constexpr数组，std::array就是我们应该使用的容器类。

{{< alert success >}}
**最佳实践**

对constexpr数组使用std::array，对非常量表达式数组使用std::vector。

{{< /alert >}}

***
## 定义std::array

std::array在\<array\>头文件中定义。它的工作原理类似于std::vector，正如您将看到的，两者之间的相似之处多于差异。

一个区别是如何声明std::array:

```C++
#include <array>  // for std::array
#include <vector> // for std::vector

int main()
{
    std::array<int, 5> a {};  // 5个int的 std::array

    std::vector<int> b(5);    // 5个int的 std::vector

    return 0;
}
```

std::array声明有两个模板参数。第一个（int）是定义数组元素类型的类型模板参数。第二个（5）是定义数组长度的整型非类型模板参数。

***
## std::array的长度必须是常量表达式

与可以在运行时调整大小的std::vector不同，std::array的长度必须是常量表达式。通常，为长度提供的值将是整型字面值、constexpr变量或非限定作用域的枚举元素。

```C++
#include <array>

int main()
{
    std::array<int, 7> a {}; // 使用字面值常量

    constexpr int len { 8 };
    std::array<int, len> b {}; // 使用 constexpr 变量

    enum Colors
    {
         red,
         green,
         blue,
         max_colors
    };

    std::array<int, max_colors> c {}; // 使用枚举元素

#define DAYS_PER_WEEK 7
    std::array<int, DAYS_PER_WEEK> d {}; // 使用宏 (建议不要这样做, 应该使用 constexpr 变量)

    return 0;
}
```

请注意，非constexpr 变量和运行时常量不能用于长度:

```C++
#include <array>
#include <iostream>

void foo(const int length) // length 是运行时常量
{
    std::array<int, length> e {}; // error: length 不是常量表达式

int main()
{
    // 非 const 变量
    int numStudents{};
    std::cin >> numStudents; // numStudents 不是常量

    std::array<int, numStudents> {}; // error: numStudents 不是常量表达式

    foo(7);

    return 0;
}
```

也许令人惊讶的是，可以将std::array的长度定义为0:

```C++
#include <array>
#include <iostream>

int main()
{
    std::array<int, 0> arr {}; // 创建长度为0的 std::array
    std::cout << arr.empty();  // 可以看到长度确实为0

    return 0;
}
```

零长度std::array是一个没有数据的特例类。因此，调用访问零长度std::array的数据的任何成员函数（包括运算符[]）都将产生未定义的行为。

可以使用empty()成员函数测试std::array是否为零长度，如果数组长度为零，则返回true，否则返回false。


***
## std::array的聚合初始化

也许令人惊讶的是，std::array是一个聚合。这意味着它没有构造函数，而是使用聚合初始化进行初始化。快速回顾下，聚合初始化允许我们直接初始化聚合的成员。为此，提供了一个初始值设定项列表，这是一个用逗号分隔的初始化值的大括号括起来的列表。

```C++
#include <array>

int main()
{
    std::array<int, 6> fibonnaci = { 0, 1, 1, 2, 3, 5 }; // 使用大括号列表的拷贝初始化
    std::array<int, 5> prime { 2, 3, 5, 7, 11 };         // 使用大括号的列表初始化 (推荐使用)

    return 0;
}
```

每个初始化列表都按顺序初始化数组成员，从元素0开始。

如果在没有初始值设定项的情况下定义了std::array，则元素将被默认初始化。在大多数情况下，这将导致元素未初始化。

因为通常希望初始化元素，所以在没有初始化器的情况下定义std::array时，应该对其进行值初始化（使用空大括号）。

```C++
#include <array>
#include <vector>

int main()
{
    std::array<int, 5> a;   // 默认初始化 (int 元素未被初始化)
    std::array<int, 5> b{}; // 值初始化 (int 元素被设置为0) (推荐使用)

    std::vector<int> v(5);  // 值初始化 (int 元素被设置为0) (作为对比)

    return 0;
}
```

如果初始化列表中提供的初始化值多于定义的数组长度，编译器将报错。如果初始化器列表中提供的初始化值少于定义的数组长度，则没有初始化值的其余元素将被值初始化:

```C++
#include <array>

int main()
{
    std::array<int, 4> a { 1, 2, 3, 4, 5 }; // 编译失败: 太多初始化值
    std::array<int, 4> b { 1, 2 };          // b[2] 与 b[3] 被值初始化

    return 0;
}
```

***
## Const和constexpr std::array

std::array可以是常量:

```C++
#include <array>

int main()
{
    const std::array<int, 5> prime { 2, 3, 5, 7, 11 };

    return 0;
}
```

即使const std::array的元素没有显式标记为const，它们仍然被视为const（因为整个数组是const）。

std::array还完全支持constexpr:

```C++
#include <array>

int main()
{
    constexpr std::array<int, 5> prime { 2, 3, 5, 7, 11 };

    return 0;
}
```

对constexpr的这种支持是使用std::array的关键原因。

{{< alert success >}}
**最佳实践**

尽可能将std::array定义为constexpr。如果您的std::array不是constexpr，请考虑改用std::vector。

{{< /alert >}}

***
## std::array C++17的类模板参数推导（CTAD）

在C++17中使用CTAD（类模板参数推导），可以让编译器从初始值设定项列表中推导std::array的元素类型和数组长度:

```C++
#include <array>
#include <iostream>

int main()
{
    constexpr std::array a1 { 9, 7, 5, 3, 1 }; // 类型被推导为 std::array<int, 5>
    constexpr std::array a2 { 9.7, 7.31 };     // 类型被推导为 std::array<double, 2>

    return 0;
}
```

只要可行，优先使用这种语法。如果编译器不支持C++17，则需要显式提供类型和长度模板参数。

CTAD不支持部分省略模板参数，因此无法仅省略std::array的长度或类型:

```C++
#include <iostream>

int main()
{
    constexpr std::array<int> a2 { 9, 7, 5, 3, 1 };     // error: 模版参数太少 (缺少长度)
    constexpr std::array<5> a2 { 9, 7, 5, 3, 1 };       // error: 模版参数太少 (缺少类型)

    return 0;
}
```

{{< alert success >}}
**最佳实践**

使用类模板参数推导（CTAD）让编译器从其初始值设定项推断std::array的类型和长度。

{{< /alert >}}

***
## 使用std::to_array（C++20）省略数组长度

然而，TAD（模板参数推导，用于函数模板解析）支持部分省略模板参数。从C++20以后，可以通过使用std::to_array helper函数来省略std::array的数组长度:

```C++
#include <array>
#include <iostream>

int main()
{
    constexpr auto myArray1 { std::to_array<int, 5>({ 9, 7, 5, 3, 1 }) }; // 声明类型和大小
    constexpr auto myArray2 { std::to_array<int>({ 9, 7, 5, 3, 1 }) };    // 声明类型，省略大小
    constexpr auto myArray3 { std::to_array({ 9, 7, 5, 3, 1 }) };         // 省略类型和大小

    return 0;
}
```

不幸的是，使用std::to_array比直接创建std::数组代价更高，因为它涉及创建一个临时std::array，然后该数组用于复制和初始化所需的std:∶array。由于这个原因，std::to_array应该仅在无法从初始值设定项有效确定类型的情况下使用，并且应该在多次创建数组时（例如在循环中）避免使用。

例如，由于无法指定short类型的字面值，因此可以使用以下命令创建short的std::array（而不必显式指定std::array的长度）:

```C++
#include <array>
#include <iostream>

int main()
{
    constexpr auto shortArray { std::to_array<short>({ 9, 7, 5, 3, 1 }) };
    std::cout << sizeof(shortArray[0]) << '\n';

    return 0;
}
```

***
## 使用运算符[]访问数组元素

就像std::vector一样，访问std:array元素的最常见方法是使用下标操作符（操作符[]）:

```C++
#include <array> // for std::array
#include <iostream>

int main()
{
    constexpr std::array<int, 5> prime{ 2, 3, 5, 7, 11 };

    std::cout << prime[3]; // 打印下标为 3 的元素的值 (7)
    std::cout << prime[9]; // 无效索引 (未定义的行为)

    return 0;
}
```

运算符[]不执行边界检查。如果提供了无效的索引，将导致未定义的行为。

在下一课中，将讨论其他几种索引std::array的方法。

***

{{< prevnext prev="/basic/chapter16/summary/" next="/" >}}
16.12 第16章总结
<--->
主页
{{< /prevnext >}}
