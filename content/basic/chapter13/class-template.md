---
title: "类模板"
date: 2024-03-08T13:20:57+08:00
---

在前面函数模板中，介绍了一个挑战，即必须为不同的参数类型创建单独的（重载）函数：

```C++
#include <iostream>

// 计算两个int值中最大值的函数
int max(int x, int y)
{
    return (x < y) ? y : x;
}

// 与上面的函数几乎相同
// 只是输入类型不同
double max(double x, double y)
{
    return (x < y) ? y : x;
}

int main()
{
    std::cout << max(5, 6);     // 调用 max(int, int)
    std::cout << '\n';
    std::cout << max(1.2, 3.4); // 调用 max(double, double)

    return 0;
}
```

解决方案是创建一个函数模板，编译器可以使用该模板为需要的任何类型集实例化普通函数：

```C++
#include <iostream>

// max 函数模版
template <typename T>
T max(T x, T y)
{
    return (x < y) ? y : x;
}

int main()
{
    std::cout << max(5, 6);     // 实例化并调用 max<int>(int, int)
    std::cout << '\n';
    std::cout << max(1.2, 3.4); // 实例化并调用 max<double>(double, double)

    return 0;
}
```

***
## 聚合类型具有类似的挑战

在聚合类型（结构体/类/联合和数组）方面，会遇到类似的挑战。

例如，假设正在编写一个程序，需要处理成对的int值，并需要确定两个数字中哪个更大。可以编写这样的程序：

```C++
#include <iostream>

struct Pair
{
    int first{};
    int second{};
};

constexpr int max(Pair p) // 直接传递Pair，因为它很小
{
    return (p.first < p.second ? p.second : p.first);
}

int main()
{
    Pair p1{ 5, 6 };
    std::cout << max(p1) << " is larger\n";

    return 0;
}
```

后来，我们发现还需要成对的double。因此，将程序更新为：

```C++
#include <iostream>

struct Pair
{
    int first{};
    int second{};
};

struct Pair // 编译失败: 重复定义Pair
{
    double first{};
    double second{};
};

constexpr int max(Pair p)
{
    return (p.first < p.second ? p.second : p.first);
}

constexpr double max(Pair p) // 编译失败: 重载函数，但是只有返回类型不同
{
    return (p.first < p.second ? p.second : p.first);
}

int main()
{
    Pair p1{ 5, 6 };
    std::cout << max(p1) << " is larger\n";

    Pair p2{ 1.2, 3.4 };
    std::cout << max(p2) << " is larger\n";

    return 0;
}
```

不幸的是，这个程序无法编译，并且有许多问题需要解决。

首先，与函数不同，类型定义不能重载。编译器将把Pair的第二个定义视为Pair的第一个定义的错误重新声明。其次，尽管函数可以重载，但max(Pair)函数仅在返回类型上有所不同，重载函数不能仅根据返回类型来区分。第三，这里有许多冗余。每个Pair结构体都相同（除了数据类型），并且max(Pair)函数相同（除了返回类型）。

可以通过为Pair结构赋予不同的名称（例如，PairInt和PairDouble）来解决前两个问题。但是，必须记住它们的命名方案，并且为每个类型拷贝一组代码，这有严重的冗余问题。

幸运的是，可以做得更好。

{{< alert success >}}
**注**

在继续之前，如果您对函数模板、模板类型或函数模板实例化的工作方式不清楚，请复习之前相关内容。

{{< /alert >}}

***
## 类模板

就像函数模板是用于实例化函数的模板定义一样，类模板是用于实例化类类型的模板定义。

下面这是int Pair的定义：

```C++
struct Pair
{
    int first{};
    int second{};
};
```

让我们将Pair类重写为类模板：

```C++
#include <iostream>

template <typename T>
struct Pair
{
    T first{};
    T second{};
};

int main()
{
    Pair<int> p1{ 5, 6 };        // 实例化 Pair<int> 并创建对象 p1
    std::cout << p1.first << ' ' << p1.second << '\n';

    Pair<double> p2{ 1.2, 3.4 }; // 实例化 Pair<double> 并创建对象 p2
    std::cout << p2.first << ' ' << p2.second << '\n';

    Pair<double> p3{ 7.8, 9.0 }; // 创建 p3，使用已经实例化了的 Pair<double>
    std::cout << p3.first << ' ' << p3.second << '\n';

    return 0;
}
```

就像函数模板一样，使用template来启动类模板定义。从template关键字开始。接下来，在尖括号（<>）内指定使用的所有模板类型。对于需要的每个模板类型，使用关键字typename（推荐）或class（不推荐），后跟模板类型的名称（例如T）。在这种情况下，由于两个成员变量是相同的类型，因此只需要一个模板类型。

接下来，像往常一样定义结构体，可以在任何需要模板化类型的地方使用模板类型（T），该类型稍后将被替换为真实类型。就是这样！我们完成了类模板定义。

在main中，可以使用所需的任何类型实例化Pair对象。首先，实例化一个类型为Pair\<int\>的对象。由于Pair\<int\>的类型定义尚不存在，编译器使用类模板实例化名为Pair\<int\>的结构体类型定义，其中模板类型T的所有出现都被类型int替换。

接下来，实例化一个类型为Pair\<double\>的对象，其中T被double替换。对于p3，Pair<double>已经被实例化，因此编译器将使用先前的类型定义。

下面是与上面相同的示例，显示了在完成所有模板实例化后编译器实际编译的内容：

```C++
#include <iostream>

// Pair 类模版定义
// (模版实例化后这个定义不再被需要了)
template <typename T>
struct Pair;

// 显示定义 Pair<int>
template <> // 告诉编译器这是一个没有类型参数的模版
struct Pair<int>
{
    int first{};
    int second{};
};

// 显示定义 Pair<double>
template <> // 告诉编译器这是一个没有类型参数的模版
struct Pair<double>
{
    double first{};
    double second{};
};

int main()
{
    Pair<int> p1{ 5, 6 };        // 实例化 Pair<int> 并创建对象 p1
    std::cout << p1.first << ' ' << p1.second << '\n';

    Pair<double> p2{ 1.2, 3.4 }; // 实例化 Pair<double> 并创建对象 p2
    std::cout << p2.first << ' ' << p2.second << '\n';

    Pair<double> p3{ 7.8, 9.0 }; // 创建 p3，使用已经实例化了的 Pair<double>
    std::cout << p3.first << ' ' << p3.second << '\n';

    return 0;
}
```

您可以直接编译这个示例，并看到它按预期工作！

{{< alert success >}}
**提醒**

“类类型”是结构体、类或联合类型。为了简单起见，这里在结构体上演示“类模板”，但这里的一切都同样适用于类。

{{< /alert >}}

{{< alert success >}}
**对于高级读者**

上面的示例使用了一个名为类模板特化的功能（后面介绍）。此时不需要了解此功能的工作原理。

{{< /alert >}}

***
## 在函数中使用类模板

现在，让我们看看如何让max函数与类模版一起使用。由于编译器将Pair\<int\>和Pair\<double\>视为单独的类型，因此可以使用按参数类型区分重载函数：

```C++
constexpr int max(Pair<int> p)
{
    return (p.first < p.second ? p.second : p.first);
}

constexpr double max(Pair<double> p) // okay: Pair<int> 和 Pair<double> 是不同的类型，因此可以重载
{
    return (p.first < p.second ? p.second : p.first);
}
```

但这不能解决冗余问题。我们真正想要的是一个可以接受任何类型Pair的函数。换句话说，需要一个接受Pair\<T\>类型参数的函数，其中T是模板类型参数。这意味着需要一个函数模板来完成这项工作！

下面是一个完整的示例，max()被实现为函数模板：

```C++
#include <iostream>

template <typename T>
struct Pair
{
    T first{};
    T second{};
};

template <typename T>
constexpr T max(Pair<T> p)
{
    return (p.first < p.second ? p.second : p.first);
}

int main()
{
    Pair<int> p1{ 5, 6 };
    std::cout << max<int>(p1) << " is larger\n"; // 显示调用 max<int>

    Pair<double> p2{ 1.2, 3.4 };
    std::cout << max(p2) << " is larger\n"; // 使用参数类型推导调用 max<double> (推荐)

    return 0;
}
```

max()函数模板非常简单。因为我们想传入Pair\<T\>，所以需要编译器理解T是什么。因此，需要一个模版类型参数 T 。然后，可以将T既用作返回类型，也用作Pair\<T\>的模板类型。

当使用Pair\<int\>调用max()函数时，编译器将从函数模板中实例化函数int max\<int\>（Pair\<int\>），其中模板类型T被替换为int。下面的片段显示了在这种情况下编译器实际实例化的内容：

```C++
template <>
constexpr int max(Pair<int> p)
{
    return (p.first < p.second ? p.second : p.first);
}
```

与对函数模板的所有调用一样，可以明确指定模板类型参数（例如 max\<int\>(p1) ），也可以隐式调用（例如 max(p2) ），并让编译器使用模板参数推导来确定模板类型参数应该是什么。

***
## 具有模板类型和普通类型的类模板

类模板可以某些成员使用模版类型，其它成员使用普通类型。例如：

```C++
template <typename T>
struct Foo
{
    T first{};    // first 类型为 T，实例化时会被替换
    int second{}; // second 类型为 int, 与 T 无关
};
```

这与期望的完全一样：first 是模版类型 T ，second 总是int。

***
## 具有多个模板类型的类模板

类模板也可以有多个模板类型。例如，如果希望Pair类的两个成员能够具有不同的类型，则可以使用两个模板类型定义Pair类模板：

```C++
#include <iostream>

template <typename T, typename U>
struct Pair
{
    T first{};
    U second{};
};

template <typename T, typename U>
void print(Pair<T, U> p)
{
    std::cout << '[' << p.first << ", " << p.second << ']';
}

int main()
{
    Pair<int, double> p1{ 1, 2.3 }; // p1 保存 int 和 double
    Pair<double, int> p2{ 4.5, 6 }; // p2 保存 double 和 int
    Pair<int, int> p3{ 7, 8 };      // p3 保存两个 int

    print(p2);

    return 0;
}
```

为了定义多个模板类型，在模板参数声明中，用逗号分隔每个所需的模板类型。在上面的示例中，定义了两个不同的模板类型，一个名为T，一个称为U。T和U的实际模板类型参数可以不同（如上面的p1和p2），也可以相同（如p3）。

***
## 使函数模板与多个模版类型的模版类一起工作

考虑上面示例中的 print() 函数模板：

```C++
template <typename T, typename U>
void print(Pair<T, U> p)
{
    std::cout << '[' << p.first << ", " << p.second << ']';
}
```

因为已经将函数参数显式定义为Pair\<T，U\>，所以只有类型为Pair\<T，U\>(或那些可以转换为 Pair\<T，U\> )的输入才会匹配。

在某些情况下，可以编写与任何类型一起使用的函数模板。为此，只需要将模版类型参数，直接作为函数参数的类型。

例如：

```C++
#include <iostream>

template <typename T, typename U>
struct Pair
{
    T first{};
    U second{};
};

struct Point
{
    int first{};
    int second{};
};

template <typename T>
void print(T p) // 类型参数 T 将会匹配任何类型
{
    std::cout << '[' << p.first << ", " << p.second << ']'; // 只有 T 类型，有 first 和 second 成员，才能编译通过
}

int main()
{
    Pair<double, int> p1{ 4.5, 6 };
    print(p1); // 匹配 print(Pair<double, int>)

    std::cout << '\n';

    Point p2 { 7, 8 };
    print(p2); // 匹配 print(Point)

    std::cout << '\n';
    
    return 0;
}
```

在上面的示例中，重写了print()，使其只有一个模板类型参数（T），它将匹配任何类型。T只要具有 first 和 second 成员，print就能成功编译。使用类型为Pair\<double，int\>的对象调用print()，然后再次使用类型为Point的对象来调用，演示这一点。

有一种情况可能会产生误导。考虑以下版本的print()：

```C++
template <typename T, typename U>
struct Pair // 定义了一个类型 Pair
{
    T first{};
    U second{};
};

template <typename Pair> // 定义了一个模版类型参数 Pair (遮挡住了 struct Pair 的定义)
void print(Pair p)       // 这里指向模版类型参数 Pair, 而不是 struct Pair
{
    std::cout << '[' << p.first << ", " << p.second << ']';
}
```

您可能期望该函数仅在使用struct Pair调用时匹配。但此版本的print()在功能上与模板类型参数名为T的先前版本相同，并且将与任何类型匹配。这里的问题是，当将Pair定义为模板类型参数时，它遮挡了名称Pair在全局范围内的其他用法。因此，在函数模板中，Pair指的是模板类型参数Pair，而不是类类型Pair。由于模板类型参数将匹配任何类型，因此该Pair匹配任何类型，而不仅仅是类类型Pair！

这是坚持使用简单的模板参数名称（如T、U、N）的一个很好的理由，因为它们不太可能隐藏类类型名称。

***
## std::pair

由于使用数据对很常见的，C++标准库包含一个名为std::pair的类模板（在\<utility\>头文件中），该模板与我们自己定义的一样。事实上，上述代码可以替换使用std::pair：

```C++
#include <iostream>
#include <utility>

template <typename T, typename U>
void print(std::pair<T, U> p)
{
    std::cout << '[' << p.first << ", " << p.second << ']';
}

int main()
{
    std::pair<int, double> p1{ 1, 2.3 }; // p1 保存 int 和 double
    std::pair<double, int> p2{ 4.5, 6 }; // p2 保存 double 和 int
    std::pair<int, int> p3{ 7, 8 };      // p3 保存两个 int

    print(p2);

    return 0;
}
```

在本课中，我们开发了自己的Pair类来演示如何工作，但在实际代码中，更应该使用std::pair，而不是自己编写。

***
## 在多个文件中使用类模板

就像函数模板一样，类模板通常在头文件中定义，因此它们可以包含在任何需要它们的代码文件中。模板定义和类型定义都不受单定义规则的约束，因此这不会导致问题：

pair.h：

```C++
#ifndef PAIR_H
#define PAIR_H

template <typename T>
struct Pair
{
    T first{};
    T second{};
};

template <typename T>
constexpr T max(Pair<T> p)
{
    return (p.first < p.second ? p.second : p.first);
}

#endif
```

foo.cpp：

```C++
#include "pair.h"
#include <iostream>

void foo()
{
    Pair<int> p1{ 1, 2 };
    std::cout << max(p1) << " is larger\n";
}
```

main.cpp：

```C++
#include "pair.h"
#include <iostream>

void foo(); // 前向声明函数 foo()

int main()
{
    Pair<double> p2 { 3.4, 5.6 };
    std::cout << max(p2) << " is larger\n";

    foo();

    return 0;
}
```

***

{{< prevnext prev="/basic/chapter13/struct-member-select/" next="/basic/chapter13/class-template-arg-deduct/" >}}
13.9 结构体指针和引用的成员选择操作
<--->
13.11 类模板参数推导（CTAD）
{{< /prevnext >}}
