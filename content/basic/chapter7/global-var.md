---
title: "全局变量"
date: 2023-12-18T16:52:52+08:00
---

在C++中，变量也可以在函数外部声明。这样的变量称为全局变量。

***
## 声明全局变量

按照惯例，全局变量在全局命名空间中的文件顶部、include的下方声明。下面是示例：

```C++
#include <iostream>

// 函数外的变量是全局变量
int g_x {}; // 全局变量 g_x

void doSomething()
{
    // 全局变量声明后，可以在文件内的任意位置看到和使用
    g_x = 3;
    std::cout << g_x << '\n';
}

int main()
{
    doSomething();
    std::cout << g_x << '\n';

    // 全局变量声明后，可以在文件内的任意位置看到和使用
    g_x = 5;
    std::cout << g_x << '\n';

    return 0;
}
// 文件结束，g_x离开作用域
```

上面的示例打印：

```C++
3
3
5
```

***
## 全局变量的作用域

在全局命名空间中声明的标识符具有全局命名空间作用域（通常称为全局作用域，有时非正式地称为文件作用域），这意味着它们从声明点到声明它们的文件末尾都是可见的。

一旦声明，全局变量就可以在文件中的任何位置使用！在上面的示例中，函数doSomething() 和main() 中都使用了全局变量 g_x。

全局变量也可以在用户定义的命名空间内定义。下面是与上面相同的示例，但g_x已从全局范围移动到用户定义的命名空间Foo：

```C++
#include <iostream>

namespace Foo // Foo 在全局命名空间中定义
{
    int g_x {}; // g_x 现在位于 Foo 命名空间中, 但仍是全局变量
}

void doSomething()
{
    // 全局变量声明后，可以在文件内的任意位置看到和使用
    Foo::g_x = 3;
    std::cout << Foo::g_x << '\n';
}

int main()
{
    doSomething();
    std::cout << Foo::g_x << '\n';

    // 全局变量声明后，可以在文件内的任意位置看到和使用
    Foo::g_x = 5;
    std::cout << Foo::g_x << '\n';

    return 0;
}
```

尽管标识符g_x现在被限制在命名空间Foo，但该名称仍然可以全局访问（通过Foo::g_x），g_x仍然是全局变量。

{{< alert success >}}
**关键点**

在命名空间内声明的变量也是全局变量。

{{< /alert >}}

***
## 全局变量具有静态存储期（static duration）

全局变量在程序启动时创建，在程序结束时销毁。这称为静态存储期。具有静态存储期的变量有时称为静态变量。

***
## 命名全局变量

按照惯例，一些开发人员在非常量的全局变量标识符前面加上“g”或“g_”，以表示它们是全局的。该前缀有几种用途：

1. 它有助于避免与全局命名空间中的其他标识符发生命名冲突。
2. 它有助于防止无意中的命名遮挡（name shadowing）（后续讨论）。
3. 它有助于指示变量存在于函数范围之外，因此，对它们所做的任何更改也将持续存在。


在用户定义的命名空间内定义的全局变量通常省略前缀（因为在这种情况下，上面列表中的前两点不是问题，并且当我们看到前缀的命名空间名称时，我们可以推断变量是全局的）。

{{< alert success >}}
**最佳实践**

在命名非常量的全局变量时，请考虑使用“g”或“g_”前缀，以帮助将它们与局部变量和函数参数区分开来。

{{< /alert >}}

***
## 全局变量初始化

与局部变量（默认情况下未初始化）不同，具有静态存储期的变量默认为被零初始化。

也可以选择初始化非常量的全局变量：

```C++
int g_x;       // 未显式初始化 (默认被初始化为0)
int g_y {};    // 值初始化 (被初始化为0)
int g_z { 1 }; // 使用特定的值，进行列表初始化
```

***
## 常量全局变量

就像局部变量一样，全局变量也可以是常量。与所有常量一样，必须初始化常量全局变量。

```C++
#include <iostream>

const int g_x;     // error: constant variables must be initialized
constexpr int g_w; // error: constexpr variables must be initialized

const int g_y { 1 };     // const global variable g_y, initialized with a value
constexpr int g_z { 2 }; // constexpr global variable g_z, initialized with a value

void doSomething()
{
    // global variables can be seen and used everywhere in the file
    std::cout << g_y << '\n';
    std::cout << g_z << '\n';
}

int main()
{
    doSomething();

    // global variables can be seen and used everywhere in the file
    std::cout << g_y << '\n';
    std::cout << g_z << '\n';

    return 0;
}
// g_y and g_z goes out of scope here
```

{{< alert success >}}
**相关内容**

我们在第7.9课中更详细地讨论了全局常量——在多个文件中共享全局常量（使用内联变量）。

{{< /alert >}}

***
## 关于（非常量）全局变量的一句话

新的程序员经常试图使用许多全局变量，因为可以使用它们，而不必将它们显式地传递给每个需要它们的函数。然而，通常应完全避免使用非常量全局变量！我们将在即将到来的第7.8课中讨论为什么——为什么（非常数）全局变量是邪恶的。

***
## 快速摘要

```C++
// Non-constant global variables
int g_x;                 // defines non-initialized global variable (zero initialized by default)
int g_x {};              // defines explicitly value-initialized global variable
int g_x { 1 };           // defines explicitly initialized global variable

// Const global variables
const int g_y;           // error: const variables must be initialized
const int g_y { 2 };     // defines initialized global const

// Constexpr global variables
constexpr int g_y;       // error: constexpr variables must be initialized
constexpr int g_y { 3 }; // defines initialized global constexpr
```

