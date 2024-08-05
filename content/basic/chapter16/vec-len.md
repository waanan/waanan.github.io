---
title: "vector与无符号长度和下标问题"
date: 2024-07-08T11:10:28+08:00
---

上一课介绍了运算符[]，它用于按数组下标访问元素。

在本课中，将研究访问数组元素的其他方法，以及获取容器类长度（容器类中当前元素的数量）的几种不同方法。

但在这样做之前，需要讨论C++设计者犯的一个错误，以及它如何影响C++标准库中的所有容器类。

***
## 容器长度问题

让我们从一个断言开始：获取数组长度的下标值的类型应该与用于存储数组长度的数据类型匹配。这是为了使尽可能长的数组中的所有元素都可以被索引。

正如Bjarne Stroustrup回忆的那样，当C++标准库中的容器类被设计时（大约1997年），设计者必须选择长度（和数组下标）是有符号的还是无符号的。当时的选择是无符号。

给出的原因是：标准库数组类型的下标不能为负，使用无符号类型，由于额外的一位，（在机器字长只有16位的日子里这是很重要的）而具有更大长度的数组，并且检查下标返回只需要一个条件检查，而不是两个条件检查（因为不需要检查来确保索引小于0）。

回顾过去，这通常被认为是错误的选择。我们现在理解，由于隐式转换规则，使用无符号值来尝试强制非负性不起作用（因为负有符号整数只会隐式转换为非常大的无符号整数，从而产生垃圾结果），在32位或64位系统上通常也不差额外的符号位（因为您可能不会创建包含20亿个以上元素的数组），并且常用的运算符[]也不进行范围检查。

在前面讨论无符号整数，以及为什么要避免它们，我们讨论了为什么要优先使用有符号值来保存量。还注意到，混合有符号值和无符号值会导致意外行为。因此，标准库容器类对长度（和索引）使用无符号值的事实是有问题的，因为这使得在使用这些类型时无法避免无符号值。

就目前而言，我们被这种选择和它造成的不必要的复杂性所困扰。

***
## 回顾：符号转换是窄化转换（constexpr除外）

在继续之前，快速回顾一下关于符号转换、列表初始化和constexpr初始值设定项，因为将在本章中大量讨论这些内容。

符号转换被认为是窄化转换，因为有符号或无符号类型不能保存对立类型范围中包含的所有值。当这样的转换将在运行时执行时，编译器将在不允许窄化转换的上下文中报出错误（例如在列表初始化中），并且在执行这种转换的其他上下文中可能发出警告。

例如：

```C++
#include <iostream>

void foo(unsigned int)
{
}

int main()
{
    int s { 5 };
    
    [[maybe_unused]] unsigned int u { s }; // 编译失败: 列表初始化不允许窄化转换
    foo(s);                                // 可能有 warning: 拷贝初始化允许窄化转换

    return 0;
}
```

在上面的示例中，变量u的初始化产生编译错误，因为在执行列表初始化时不允许窄化转换。对foo()的调用执行复制初始化，这确实允许窄化转换，并且根据编译器在生成符号转换警告方面的积极程度，这可能会生成警告，也可能不会生成警告。例如，在这种情况下，当使用编译器标志 -Wsign-conversion 时，GCC和Clang都将产生警告。

然而，如果要进行符号转换的值是constexpr，并且可以转换为相反类型中的等效值，则符号转换不被视为窄化转换。这是因为编译器可以保证转换是安全的。

```C++
#include <iostream>

void foo(unsigned int)
{
}

int main()
{
    constexpr int s { 5 };                 // 现在是 constexpr
    [[maybe_unused]] unsigned int u { s }; // ok: s 是 constexpr 并且可以安全转换, 不是窄化转换
    foo(s);                                // ok: s 是 constexpr 并且可以安全转换, 不是窄化转换

    return 0;
}
```

在这种情况下，由于s是constexpr，并且要转换的值（5）可以表示为无符号值，因此转换不被认为是窄化的，并且可以隐式执行而不会出现问题。

这种非窄化constexpr转换（从constexpr int到constexpr std::size_t）将是我们经常使用的。

***
## std::vector的长度和索引的类型为size_type

在Typedef和类型别名的学习中，我们提到类型定义和类型别名通常用于需要额外的类型名称的情况。例如，std::size_t是某些大型无符号整型的typedef，通常是unsigned long或unsigned long long。

每个标准库容器类都定义了一个名为size_type（有时写为T::size_type）的嵌套typedef成员，它是用于容器长度（和索引）的类型的别名。

您通常会在文档和编译器警告/错误消息中看到size_type。例如，std::vector的 size() 成员函数的文档指出，size()返回类型为size_type的值。

size_type几乎总是std::size_t的别名，但可以覆盖（在极少数情况下）以使用不同的类型。

当访问容器类的size_type成员时，必须使用容器类的完全模板化名称来限定其范围。例如，std::vector\<int\>::size_type。

{{< alert success >}}
**关键点**

size_type是在标准库容器类中定义的嵌套typedef，用作容器类的长度（和索引）的类型。

size_type默认为std::size_t，并且由于这几乎从未更改，因此可以合理地假设size_type是std::size_t的别名。

{{< /alert >}}

{{< alert success >}}
**对于高级读者**

除了std::array之外的所有标准库容器都使用std::allocator来分配内存。对于这些容器，T::size_type派生自所使用的分配器的size_type。由于std::allocator最多可以分配std::size_t个字节的内存，因此std::allocator\<t\>::size_type定义为std::size_t。因此，T::size_type默认为std::size_t。

只有在自定义分配器的T::size_type被定义为std::size_t以外的内容的情况下，容器的T::size_type才会是std::size_t之外的内容。这很少见，并且是单个程序独立的行为，因此通常可以安全地假设T::size_type将是std::size_t。除非您的应用程序正在使用自定义分配器（您将知道情况是否如此）。

{{< /alert >}}

***
## 使用size()成员函数或std::size()获取std::vector的长度

可以使用size()成员函数（该函数将长度返回无符号 size_type）来查看容器类对象的长度：

```C++
#include <iostream>
#include <vector>

int main()
{
    std::vector prime { 2, 3, 5, 7, 11 };
    std::cout << "length: " << prime.size() << '\n'; // 返回的长度类型为 `size_type` (`std::size_t`的别名)
    return 0;
}
```

这将打印：

```C++
length: 5
```

与具有length()和size()成员函数（他们执行相同的操作）的std::string和std::string_view不同，std::vector（和C++中的大多数其他容器类型）仅具有size()。现在您明白了为什么容器的长度有时被模棱两可地称为其大小。

在C++17中，还可以使用std::size()非成员函数（对于容器类，该函数就是调用size()成员函数）。

```C++
#include <iostream>
#include <vector>

int main()
{
    std::vector prime { 2, 3, 5, 7, 11 };
    std::cout << "length: " << std::size(prime); // C++17, 返回的长度类型为 `size_type` (`std::size_t`的别名)

    return 0;
}
```

如果想使用上述任一方法将长度存储在有符号类型的变量中，可能会导致有符号/无符号转换编译警告或错误。这里最简单的操作是将结果static_cast转换为所需类型：

```C++
#include <iostream>
#include <vector>

int main()
{
    std::vector prime { 2, 3, 5, 7, 11 };
    int length { static_cast<int>(prime.size()) }; // static_cast 范围值为 int
    std::cout << "length: " << length ;

    return 0;
}
```

***
## 使用std::ssize() （C++20）获取std::vector的长度

C++20引入了std::ssize() 非成员函数，该函数将长度返回为大型有符号整数类型（通常为std::ptrdiff_t，这是通常用作std::size_t的有符号对应项的类型）：

```C++
#include <iostream>
#include <vector>

int main()
{
    std::vector prime{ 2, 3, 5, 7, 11 };
    std::cout << "length: " << std::ssize(prime); // C++20, 返回大型有符号整数作为长度

    return 0;
}
```

这是三个函数中唯一一个将长度返回为有符号类型的函数。

如果要使用此方法将长度存储在有符号类型的变量中，则有两个选项。

首先，由于int类型可能小于std::ssize()返回的有符号类型，如果要将长度分配给int变量，则应将结果static_cast为int（否则可能会收到窄化转换警告或错误）：

```C++
#include <iostream>
#include <vector>

int main()
{
    std::vector prime{ 2, 3, 5, 7, 11 };
    int length { static_cast<int>(std::ssize(prime)) }; // static_cast 结果转换为 int
    std::cout << "length: " << length;

    return 0;
}
```

或者，您可以使用auto让编译器推断要用于变量的正确签名类型：

```C++
#include <iostream>
#include <vector>

int main()
{
    std::vector prime{ 2, 3, 5, 7, 11 };
    auto length { std::ssize(prime) }; // 使用 auto 去自动推断 std::ssize() 返回的类型
    std::cout << "length: " << length;

    return 0;
}
```

***
## 使用运算符[]访问数组元素不进行边界检查

在上一课中，介绍了下标运算符（运算符[]）：

```C++
#include <iostream>
#include <vector>

int main()
{
    std::vector prime{ 2, 3, 5, 7, 11 };

    std::cout << prime[3];  // 打印下标为3的位置中存储的值 (7)
    std::cout << prime[9]; // 非法下标 (未定义的行为)

    return 0;
}
```

运算符[]不执行边界检查。将在后面的部分中进一步讨论这一点。

***
## 使用at()成员函数访问数组元素执行运行时边界检查

数组容器类支持另一种访问方法。at() 成员函数会进行运行时边界检查：

```C++
#include <iostream>
#include <vector>

int main()
{
    std::vector prime{ 2, 3, 5, 7, 11 };

    std::cout << prime.at(3); // 打印下标为3的位置中存储的值 (7)
    std::cout << prime.at(9); // 无效索引 (抛出异常)

    return 0;
}
```

在上面的例子中，对prime.at(3)的调用会检查确保索引3有效，并且由于它有效，它返回对数组元素3的引用。然后，可以打印该值。然而，对prime.at(9)的调用失败（在运行时），因为9不是该数组的有效索引。函数不会返回引用，而是生成一个错误来终止程序。

因为它对每个调用都进行运行时边界检查，所以at()比运算符[]慢（但更安全）。尽管不太安全，但通常使用操作符[]而不是at()，因为我们会现检查索引在数组长度内，然后再访问，不会首先尝试使用无效的索引。

{{< alert success >}}
**对于高级读者**

当at()成员函数遇到越界索引时，它实际上抛出类型为std::out_of_range的异常。如果不处理异常，程序将被终止。

{{< /alert >}}

***
## 使用constexpr有符号int索引访问std::vector

当使用constexpr（带符号）int索引std::vector时，可以让编译器隐式地将其转换为std::size_t，而不会进行窄化转换：

```C++
#include <iostream>
#include <vector>

int main()
{
    std::vector prime{ 2, 3, 5, 7, 11 };

    std::cout << prime[3] << '\n';     // okay: 3 从 int 转换为 std::size_t, 不是窄化转化
 
    constexpr int index { 3 };         // constexpr
    std::cout << prime[index] << '\n'; // okay: constexpr 索引 隐式转换为 std::size_t, 不是窄化转化
   
    return 0;
}
```

***
## 使用非constexpr值索引std::vector

用于索引数组的下标可以是非常数：

```C++
#include <iostream>
#include <vector>

int main()
{
    std::vector prime{ 2, 3, 5, 7, 11 };

    std::size_t index { 3 };           // non-constexpr
    std::cout << prime[index] << '\n'; // operator[] 参数是 std::size_t, 无需转换
   
    return 0;
}
```

然而，根据最佳实践，通常希望避免使用无符号类型来保存数量。

当下标是非constexpr有符号值时，会遇到问题：

```C++
#include <iostream>
#include <vector>

int main()
{
    std::vector prime{ 2, 3, 5, 7, 11 };

    int index { 3 };                   // non-constexpr
    std::cout << prime[index] << '\n'; // 可能会有 warning: index 隐式转换为 std::size_t, 窄化转换
   
    return 0;
}
```

在本例中，索引是一个非constexpr有符号的int。std::vector的运算符[]的下标的类型为size_type（std::size_t的别名）。因此，当调用prime[index]时，有符号int必须转换为std::size_t。

这样的转换不应该是危险的（因为std::vector的索引应该是非负的，并且非负有符号值将安全地转换为无符号值）。但当在运行时执行时，这被认为是一个窄化转换，编译器可能生成一个警告，说明这是一个不安全的转换。

由于数组下标是常见的，并且每个这样的转换都将生成一个警告，因此这很容易使编译日志中出现虚假的警告。或者，如果启用了“将警告视为错误”，将编译失败。

有许多可能的方法可以避免此问题（例如，每次索引数组时，static_cast将int转换为std::size_t），但没有一种方法是方便的——它们都不可避免地以某种方式使代码变得混乱或复杂。

在这种情况下，要做的最简单的事情是使用类型为std::size_t的变量作为索引，并且除了索引之外，不要将该变量用于其他任何事情。

***

{{< prevnext prev="/basic/chapter16/intro-vector-list-init/" next="/basic/chapter16/vec-pass/" >}}
16.1 std::vector和列表构造函数简介
<--->
16.3 传递std::vector
{{< /prevnext >}}
