---
title: "在多个文件中共享全局常量（使用内联变量）"
date: 2023-12-18T16:52:52+08:00
---

在某些应用程序中，可能需要在整个代码中使用某些符号常量（而不仅仅是在一个位置）。例如不改变的物理或数学常数（例如，pi或阿伏伽德罗数），或特定于应用的“系数”值（例如，摩擦系数或重力系数）。与其在每个需要它们的文件中重新定义这些常量），不如在中心位置声明它们一次，并在需要的地方使用它们。这样，如果需要更改它们，只需要在一个地方更改它们，并且这些更改可以传播出去。

***
## 作为内部变量的全局常数

在C++17之前，以下是最简单、最常见的解决方案：

1. 创建一个头文件来放置这些值
2. 在创建的头文件中定义一个命名空间
3. 使用constexpr来定义这些变量
4. 使用#include，将这个头文件包含在需要使用它的地方

例如：

constants.h：

```C++
#ifndef CONSTANTS_H
#define CONSTANTS_H

// 定义你自己的命名空间
namespace constants
{
    // 常量 默认内部链接
    constexpr double pi { 3.14159 };
    constexpr double avogadro { 6.0221413e23 };
    constexpr double myGravity { 9.2 }; // m/s^2 -- 重力在这个星球上稍微轻一点
    // ... 其它定义的常量
}
#endif
```

然后使用域解析操作符（::），左边是命名空间名称，右边是变量名称，来访问常量：

main.cpp：

```C++
#include "constants.h" // 本文件中，将包含每一个常量的定义

#include <iostream>

int main()
{
    std::cout << "Enter a radius: ";
    double radius{};
    std::cin >> radius;

    std::cout << "The circumference is: " << 2 * radius * constants::pi << '\n';

    return 0;
}
```

当该头文件被包含到.cpp文件中时，头文件中定义的每个变量都将被复制到代码文件中。因为这些变量位于函数外部，所以它们被视为包含的文件中的全局变量，然后可以在该文件中的任何位置使用它们。

因为const全局变量具有内部链接，所以每个.cpp文件都获得链接器看不到的全局变量的独立版本。在大多数情况下，由于这些是常量，编译器将简单的优化掉这些变量。

{{< alert success >}}
**作为旁白…**

术语“优化掉”是指编译器通过以不影响程序输出的方式，删除内容来优化程序性能的任何过程。例如，假设您有一个常量变量x，它被初始化为值4。只要代码引用变量x，编译器就可以将x替换为4（因为x是常量，我们知道它永远不会更改为不同的值），并避免完全创建和初始化变量。

{{< /alert >}}

***
## 作为外部链接属性的全局常量

上述方法有一些潜在的缺点。

虽然方法很简单（对于较小的程序来说也很好），但每次constants.h被包含在不同的代码文件中时，这些变量每个都会复制到对应的代码文件中。如果constants.h被包含在20个不同的代码文件中，则每个变量都重复20次。头文件保护不会阻止这种情况的发生，因为它们只会防止头文件被多次包含到单个文件中，而不是被一次包含到多个不同的代码文件中。这带来了两个挑战：

1. 改变一个常量，需要重编引用到对应头文件的所有代码文件，在大型项目中，会导致较长的重新编译时间。
2. 如果常量很大，不能被优化掉，那么会消耗大量的内存。

避免这些问题的一种方法是将这些常量转换为外部变量，因为可以有一个在所有文件中共享的单个变量（初始化一次）。在这种方法中，我们将在.cpp文件中定义常量（以确保定义仅存在于一个位置），并在头中进行声明（它将包含在其他文件中）。

constants.cpp：

```C++
#include "constants.h"

namespace constants
{
    // 实际的常量定义
    extern const double pi { 3.14159 };
    extern const double avogadro { 6.0221413e23 };
    extern const double myGravity { 9.2 }; // m/s^2 -- 重力在这个星球上稍微轻一点
}
```

constants.h：

```C++
#ifndef CONSTANTS_H
#define CONSTANTS_H

namespace constants
{
    // 因为定义是存在于命名空间中, 所以前向声明也在对应的命名空间
    extern const double pi;
    extern const double avogadro;
    extern const double myGravity;
}

#endif
```

在代码文件中的使用保持不变：

main.cpp：

```C++
#include "constants.h" // 引入所有的前向声明

#include <iostream>

int main()
{
    std::cout << "Enter a radius: ";
    double radius{};
    std::cin >> radius;

    std::cout << "The circumference is: " << 2 * radius * constants::pi << '\n';

    return 0;
}
```

由于全局符号常量具有名称空间（以避免与全局名称空间中的其他标识符发生命名冲突），因此不需要使用“g_”命名前缀。

现在，符号常量将仅实例化一次（在constants.cpp中），而不是在包含constants.h的每个代码文件中实例化，并且这些常量的所有使用都将链接到constants.cpp，对constants.cpp所做的任何更改都将只需要重新编译constants.cpp。

然而，这种方法有几个缺点。首先，这些常量现在仅在它们实际定义的文件（constants.cpp）中被视为编译时常量。在其他文件中，编译器将只看到前向声明，该声明不定义常量值（并且必须由链接器解析）。这意味着在其他文件中，它们被视为运行时常量值，而不是编译时常量。因此，在constants.cpp之外，不能在需要编译时常量的任何地方使用这些变量。其次，由于编译时常量通常可以比运行时常量更容易优化，编译器可能无法对这些常量进行足够的优化。

由于编译器单独编译每个源文件，因此它只能看到出现在正在编译的源文件中的变量定义（包括任何包含的头文件）。例如，当编译器编译main.cpp时，constants.cpp中的变量定义不可见。因此，constexpr变量不能分为头文件和源文件，它们必须在头文件中定义。

鉴于上述缺点，最好在头文件中定义常量。如果您发现常量的值经常变动（例如，因为您正在调整程序），导致编译时间过长，则可以根据需要将有问题的常量移到.cpp文件中。

{{< alert success >}}
**注**

在该方法中，我们使用const而不是constexpr，因为constexper变量不能被前向声明，即使它们具有外部链接。这是因为编译器需要在编译时知道变量的值，而前向声明不提供此信息。

{{< /alert >}}

{{< alert success >}}
**关键点**

为了使变量在编译时上下文中可用，例如数组大小，编译器必须查看变量的定义（不仅仅是向前声明）。

{{< /alert >}}

***
## 全局常量作为内联变量 C++17

在前面内联函数和变量的学习中，我们介绍了内联变量，这些变量可以有多个定义，只要这些定义相同。通过使constexpr变量内联，我们可以在头文件中定义它们，然后将它们包含到需要它们的任何.cpp文件中。这避免了单定义规则冲突和重复变量的缺点。

constants.h：

```C++
#ifndef CONSTANTS_H
#define CONSTANTS_H

// 定义你自己的命名空间
namespace constants
{
    inline constexpr double pi { 3.14159 }; // 注: 内联 的 constexpr
    inline constexpr double avogadro { 6.0221413e23 };
    inline constexpr double myGravity { 9.2 }; // m/s^2 -- 重力在这个星球上稍微轻一点
    // ... 其它定义的常量
}
#endif
```

main.cpp：

```C++
#include "constants.h"

#include <iostream>

int main()
{
    std::cout << "Enter a radius: ";
    double radius{};
    std::cin >> radius;

    std::cout << "The circumference is: " << 2 * radius * constants::pi << '\n';

    return 0;
}
```

我们可以将 constants.h 包含到任意多的代码文件中，但这些变量将仅实例化一次，并在所有代码文件中共享。

该方法的缺点是，如果更改任何常量值，则需要重新编译包含常量头文件的每个文件。

{{< alert success >}}
**一个提醒**

Constexpr函数是隐式内联的，但Constexpr变量不是隐式内嵌的。

{{< /alert >}}

{{< alert success >}}
**最佳实践**

如果需要全局常量，并且编译器支持C++17，则最好在头文件中定义内联constexpr全局变量。

{{< /alert >}}

{{< alert success >}}
**一个提醒**

对constexpr字符串使用std::string_view。

{{< /alert >}}

***

{{< prevnext prev="/basic/chapter7/why-non-const-global-var-evil/" next="/basic/chapter7/static-local-var/" >}}
7.7 为什么（非常量）全局变量是邪恶的
<--->
7.9 静态局部变量
{{< /prevnext >}}
