---
title: "C样式数组简介"
date: 2024-08-13T13:06:02+08:00
---

现在，我们将介绍最后一个数组类型:C样式数组。

风格的数组继承自C语言，并内置于C++的核心语言中（与其他数组类型不同，后者是标准库容器类）。这意味着我们不需要引用头文件来使用它们。

{{< alert success >}}
**旁白**

由于它是该语言直接支持的唯一数组类型，因此标准库数组容器类型（例如，std::array和std::vector）通常使用C样式数组来实现。

{{< /alert >}}

***
## 声明C样式数组

由于C样式数组是核心语言的一部分，因此它们有自己的特殊声明语法。在C样式数组声明中，使用方括号（[]）来告诉编译器声明的对象是C样式数组。在方括号内，我们可以选择提供数组的长度，这是类型为std::size_t的整数值，它告诉编译器数组中有多少个元素。

以下定义创建了一个名为testScore的C样式数组变量，该变量包含30个int类型的元素:

```C++
int main()
{
    int testScore[30] {};      // 定义名为 testScore 的C样式数组，包含 30个值初始化的int元素（无需inlcude头文件）

//  std::array<int, 30> arr{}; // 作为比较, 这是包含 30个值初始化元素的 std::array (需要 #including <array>)

    return 0;
}
```

C样式数组的长度必须至少为1。如果数组长度为零、负值或非整数值，编译器将出错。

{{< alert success >}}
**对于高级读者**

堆上动态分配的C样式数组允许长度为0。

{{< /alert >}}

***
## c样式数组的数组长度必须是常量表达式

与std::array一样，在声明C样式数组时，数组的长度必须是常量表达式（类型为std::size_t，但这通常并不重要）。

{{< alert success >}}
**提示**

一些编译器可能允许创建具有非constexpr长度的数组，以与名为可变长度数组（VLA）的C99功能兼容。

可变长度数组不是有效的C++语法，不应在C++程序中使用。如果编译器允许这些数组，您可能忘记了禁用编译器扩展。

{{< /alert >}}

***
## 访问C样式数组

就像使用std::array一样，可以使用下标操作符（操作符[]）索引C样式的数组:

```C++
#include <iostream>

int main()
{
    int arr[5]; // 定义有5个元素的数组

    arr[1] = 7; // 使用[] 访问索引为 1 的元素
    std::cout << arr[1]; // 打印 7

    return 0;
}
```

与标准库容器类（仅使用类型为std::size_t的无符号索引）不同，C样式数组的索引可以是任何整数类型（有符号或无符号）的值，也可以是非范围枚举。这意味着C样式数组不会受到标准库容器类所具有的所有符号转换问题的影响！

```C++
#include <iostream>

int main()
{
    const int arr[] { 9, 8, 7, 6, 5 };

    int s { 2 };
    std::cout << arr[s] << '\n'; // 可以使用有符号索引

    unsigned int u { 2 };
    std::cout << arr[u] << '\n'; // 也可以使用无符号索引

    return 0;
}   
```

运算符[]不执行任何边界检查，传入越界索引将导致未定义的行为。

{{< alert success >}}
**旁白**

声明数组（例如，int arr\[5\]）时，[]的使用是声明语法的一部分，而不是对下标运算符[]的调用。

{{< /alert >}}

***
## C样式数组的聚合初始化

与std::array一样，C样式数组也是聚合，这意味着可以使用聚合初始化来初始化它们。

作为快速回顾，聚合初始化允许我们直接初始化聚合的成员。为此，我们提供了一个初始值设定项列表，这是一个用逗号分隔的初始化值的大括号括起来的列表。

```C++
int main()
{
    int fibonnaci[6] = { 0, 1, 1, 2, 3, 5 }; // 拷贝列表初始化
    int prime[5] { 2, 3, 5, 7, 11 };         // 列表初始化 (更推荐)

    return 0;
}
```

每个初始化列表都按顺序初始化数组成员，从元素0开始。

如果不为C样式数组提供初始值设定项，则元素将默认初始化。在大多数情况下，这将导致元素未初始化。因为我们通常希望初始化元素，所以在没有初始化器的情况下定义C样式数组时，应该对其进行值初始化（使用空大括号）。

```C++
int main()
{
    int arr1[5];    // 默认初始化，会导致所有成员的值未初始化
    int arr2[5] {}; // 成员值初始化 (int值默认初始化为0) (更推荐)

    return 0;
}
```

如果初始化列表中提供的初始化元素多于定义的数组长度，编译器将出错。如果初始化器列表中提供的初始化元素少于定义的数组长度，则没有初始化元素的其余元素将被值初始化:

```C++
int main()
{
    int a[4] { 1, 2, 3, 4, 5 }; // 编译失败: 太多的初始值
    int b[4] { 1, 2 };          // arr[2] 和 arr[3] 被值初始化

    return 0;
}
```

使用C样式数组的一个缺点是必须显式指定元素的类型。CTAD无法工作，因为C样式数组不是类模板。并且使用auto尝试从初始值设定项列表中推断数组的元素类型也不起作用:

```C++
int main()
{
    auto squares[5] { 1, 4, 9, 16, 25 }; // 编译失败: C样式数组无法使用类型自动推导

    return 0;
}
```

***
## 省略的长度

在下面的数组定义中存在细微的冗余。看到了吗？

```C++
int main()
{
    const int prime[5] { 2, 3, 5, 7, 11 }; // prime 长度为 5

    return 0;
}
```

我们显式地告诉编译器数组的长度为5，然后也用5个元素初始化它。当用初始值设定项列表初始化C样式数组时，可以省略长度（在数组定义中），并让编译器从初始值设定项数中推断数组的长度。

以下数组定义的行为相同:

```C++
int main()
{
    const int prime1[5] { 2, 3, 5, 7, 11 }; // prime1 显式声明长度为 5
    const int prime2[] { 2, 3, 5, 7, 11 };  // prime2 被编译推导长度为 5

    return 0;
}
```

这仅在为所有数组成员显式提供初始值设定项时有效。

```C++
int main()
{
    int bad[] {}; // error: 编译器认为数组长度为0，这不被允许！

    return 0;
}
```

当使用初始值设定项列表来初始化C样式数组的所有元素时，最好省略长度，并让编译器计算数组的长度。这样，如果添加或删除初始值设定项，数组的长度将自动调整，并且我们不会面临定义的数组长度和提供的初始值设定项数之间不匹配的风险。

***
## Const和constexpr C样式数组

就像std::array一样，C样式数组可以是const或constexpr。就像其他常量变量一样，必须初始化常量数组，并且随后不能更改元素的值。

```C++
#include <iostream>

namespace ProgramData
{
    constexpr int squares[5] { 1, 4, 9, 16, 25 }; // constexpr int 数组
}

int main()
{
    const int prime[5] { 2, 3, 5, 7, 11 }; // const int 数组
    prime[0] = 17; // 编译失败: 不能修改 const int

    return 0;
}
```

***
## C样式数组的大小

在前面的课程中，我们使用sizeof()操作符来获取对象或类型的大小（以字节为单位）。应用于C样式数组时，sizeof()返回整个数组使用的字节数:

```C++
#include <iostream>

int main()
{
    const int prime[] { 2, 3, 5, 7, 11 }; // 编译器推导数组长度为 5
    
    std::cout << sizeof(prime); // 打印 20 (假设int长度为 4 byte)

    return 0;
}
```

假设整数是4个字节，上面的程序打印20。prime数组包含5个int元素，每个元素4个字节，因此5*4=20个字节。

请注意，这里没有额外开销。C样式数组对象仅包含其元素。

***
## 获取C样式数组的长度

在C++17中，我们可以使用std::size()（在\<iterator\>中定义），它将数组长度返回为无符号整数值（类型为std::size_t）。在C++20中，我们还可以使用std::ssize()，它以有符号整数值的形式返回数组长度（对于大型有符号整数类型，可能是std::ptrdiff_t）。

```C++
#include <iostream>
#include <iterator> // for std::size and std::ssize

int main()
{
    const int prime[] { 2, 3, 5, 7, 11 };   // 编译器推导数组长度为 5

    std::cout << std::size(prime) << '\n';  // C++17, 返回无符号整数 5
    std::cout << std::ssize(prime) << '\n'; // C++20, 返回有符号整数 5

    return 0;
}
```

***
## 获取C样式数组的长度（C++14或更早版本）

在C++17之前，没有标准的库函数来获取C样式数组的长度。

如果使用的是C++11或C++14，则可以改用此函数:

```C++
#include <cstddef> // for std::size_t
#include <iostream>

template <typename T, std::size_t N>
constexpr std::size_t length(const T(&)[N]) noexcept
{
	return N;
}

int main() {

	int array[]{ 1, 1, 2, 3, 5, 8, 13, 21 };
	std::cout << "The array has: " << length(array) << " elements\n";

	return 0;
}
```

这使用一个函数模板，该函数模板通过引用获取C样式数组，然后返回表示数组长度的非类型模板参数。

在更旧的代码基中，您可能会看到C样式数组的长度是通过将整个数组的大小除以数组元素的大小来确定的:

```C++
#include <iostream>

int main()
{
    int array[8] {};
    std::cout << "The array has: " << sizeof(array) / sizeof(array[0]) << " elements\n";

    return 0;
}
```

这将打印:

```C++
The array has: 8 elements
```

这是如何工作的？首先，请注意，整个数组的大小等于数组的长度乘以元素的大小。更紧凑地说:数组大小=长度*元素大小。

可以重新排列这个方程:长度=数组大小/元素大小。常使用sizeof（array\[0\]）作为元素大小。因此，长度=sizeof（array）/ sizeof（array\[0\]）。您有时也可能会看到它被写为sizeof(array) / sizeof（*array），这也做了同样的事情。

然而，正如我们将在下一课中向您展示的那样，该公式很容易失败（当传递到退化的数组时），使程序意外中断。在这种情况下，C++17的std::size()和上面显示的length()函数模板都会导致编译错误，因此它们是安全的。

{{< alert success >}}
**相关内容**

我们将在下一课讨论数组退化

{{< /alert >}}

***
## C样式数组不支持赋值

也许令人惊讶的是，C++数组不支持赋值:

```C++
int main()
{
    int arr[] { 1, 2, 3 }; // okay: 初始化ok
    arr[0] = 4;            // 为每个元素赋值也ok
    arr = { 5, 6, 7 };     // 编译失败: 无法为数组直接赋值

    return 0;
}
```

从技术上讲，这不起作用，因为赋值要求左操作数是可修改的左值，C样式的数组不被视为可修改的左值。

如果需要将新的值列表分配给C样式数组，则最好使用std::vector。或者，可以逐个元素将新值分配给C样式数组，或者使用std::copy复制现有的C样式数组:

```C++
#include <algorithm> // for std::copy

int main()
{
    int arr[] { 1, 2, 3 };
    int src[] { 5, 6, 7 };

    // 复制 src 到 arr
    std::copy(std::begin(src), std::end(src), std::begin(arr));

    return 0;
}
```

***

