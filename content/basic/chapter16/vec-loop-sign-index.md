---
title: "数组、循环和有符号下标"
date: 2024-07-08T11:10:28+08:00
---

我们通常喜欢使用有符号值来保存值，因为无符号值有时行为令人惊讶。然而，std:∶vector（和其他容器类）使用无符号整数类型std::size_t作为长度和索引。

这可能会导致如下问题：

```C++
#include <iostream>
#include <vector>

template <typename T>
void printReverse(const std::vector<T>& arr)
{
    for (std::size_t index{ arr.size() - 1 }; index >= 0; --index) // index 是无符号整数
    {
        std::cout << arr[index] << ' ';
    }

    std::cout << '\n';
}

int main()
{
    std::vector arr{ 4, 6, 7, 3, 8, 2, 1, 9 };

    printReverse(arr);

    return 0;
}
```

此代码从反向打印数组开始：

```C++
9 1 2 8 3 7 6 4
```

然后表现出未定义的行为。它可能会打印垃圾值，或使应用程序崩溃。

这里有两个问题。首先，只要index>=0（或者换句话说，只要index为正），循环就会执行，当index为无符号时，这总是正确的。因此，循环永远不会终止。

第二，当index的值为0时，递减index时，它将回绕到一个大的正值，然后在下一次迭代中使用该值来索引数组。这是一个越界索引，将导致未定义的行为。如果vector为空，也会遇到相同的问题。

虽然有许多方法可以解决这些特定问题，但这类问题是吸引错误的磁石。

对循环变量使用有符号类型更容易避免此类问题，但也有自己的挑战。下面是使用有符号索引的上述问题的一个版本：

```C++
#include <iostream>
#include <vector>

template <typename T>
void printReverse(const std::vector<T>& arr)
{
    for (int index{ static_cast<int>(arr.size()) - 1}; index >= 0; --index) // index 是有符号整数
    {
        std::cout << arr[static_cast<std::size_t>(index)] << ' ';
    }

    std::cout << '\n';
}

int main()
{
    std::vector arr{ 4, 6, 7, 3, 8, 2, 1, 9 };

    printReverse(arr);

    return 0;
}
```

虽然该版本按预期工作，但由于添加了两个静态强制转换，代码也很混乱。代码特别难以读懂。在这种情况下，以显著的可读性代价提高了安全性。

下面是使用有符号索引的另一个示例：

```C++
#include <iostream>
#include <vector>

// 使用函数模版计算 std::vector 中数字的平均值
template <typename T>
T calculateAverage(const std::vector<T>& arr)
{
    int length{ static_cast<int>(arr.size()) };

    T average{ 0 };
    for (int index{ 0 }; index < length; ++index)
        average += arr[static_cast<std::size_t>(index)];
    average /= length;

    return average;
}

int main()
{
    std::vector testScore1 { 84, 92, 76, 81, 56 };
    std::cout << "The class 1 average is: " << calculateAverage(testScore1) << '\n';

    return 0;
}
```

代码的静态强制转换的杂乱是相当可怕的。

那该怎么办呢？这是一个没有理想解决方案的领域。

这里有许多可行的选择，我们将按从最坏到最好的顺序介绍。您可能会在其他人编写的代码中遇到所有这些问题。

{{< alert success >}}
**注**

尽管我们将在std::vector的上下文中讨论这一点，但所有标准库容器（例如，std::array）的工作方式都类似，并且具有相同的挑战。下面的讨论适用于其中任何一个。

{{< /alert >}}

***
## 关闭有符号/无符号转换警告

如果您想知道为什么有符号/无符号转换警告通常在默认情况下被禁用，那么本主题是关键原因之一。每次使用有符号数字作为标准库容器下标时，都会生成符号转换警告。这将很快用虚假警告填充编译日志，淹没实际上可能合法的警告。

因此，避免处理大量有符号/无符号转换警告的一种方法是关闭这些警告。

这是最简单的解决方案，但我们不建议这样做，因为这也将抑制生成合法的符号转换警告，可能会导致错误。

***
## 使用无符号循环变量

许多开发人员认为，由于标准库数组类型被设计为使用无符号索引，因此我们应该使用无符号数字！这是一个完全合理的立场。只需要格外小心，以免在执行此操作时遇到有符号/无符号不匹配。如果可能，请避免将索引循环变量用于索引之外的任何操作。

如果我们决定使用这种方法，应该实际使用哪个无符号类型？

我们注意到标准库容器类定义了嵌套的typedef size_type，这是用于数组长度和索引的无符号整数类型。size()成员函数返回size_type，操作符[]使用size_type作为索引，因此从技术上讲，使用size_type作为索引的类型是最一致和最安全的无符号类型（因为它在所有情况下都可以工作）。例如：

```C++
#include <iostream>
#include <vector>

int main()
{
	std::vector arr { 1, 2, 3, 4, 5 };

	for (std::vector<int>::size_type index { 0 }; index < arr.size(); ++index)
		std::cout << arr[index] << ' ';

	return 0;
}
```

然而，使用size_type有一个主要的缺点：因为它是嵌套类型，所以要使用它，必须用容器的完全模板化名称显式地为名称加前缀（这意味着我们必须键入std::vector\<int\>::size_type，而不是仅键入std::size_type）。这需要大量的类型名称，很难阅读，并且根据容器和元素类型的不同而不同。

当在函数模板内使用时，可以使用T作为模板参数。但还需要使用typename关键字为类型添加前缀：

```C++
#include <iostream>
#include <vector>

template <typename T>
void printArray(const std::vector<T>& arr)
{
	// 依赖类型，需要添加 typename 关键字
	for (typename std::vector<T>::size_type index { 0 }; index < arr.size(); ++index)
		std::cout << arr[index] << ' ';
}

int main()
{
	std::vector arr { 9, 7, 5, 3, 1 };

	printArray(arr);

	return 0;
}
```

如果忘记typename关键字，编译器可能会提醒您添加它。

{{< alert success >}}
**对于高级读者**

依赖于包含模板参数的类型的任何名称都称为依赖名称(dependent name)。依赖名称必须以关键字typename为前缀，才能用作类型。

在上面的示例中，std::vector\<T\>是一个具有模板参数的类型，因此嵌套类型std::vector\<T\>::size_type是依赖名称，并且必须以typename作为前缀才能用作类型。

{{< /alert >}}

您有时可能会看到数组类型的别名，以使循环更易于读取：

```C++
    using arrayi = std::vector<int>;
    for (arrayi::size_type index { 0 }; index < arr.size(); ++index)
```

一个更通用的解决方案是让编译器为我们获取数组类型对象的类型，这样我们就不必显式地指定容器类型或模板参数。为此，可以使用decltype关键字，它返回其参数的类型。

```C++
    // arr 是非引用类型
    for (decltype(arr)::size_type index { 0 }; index < arr.size(); ++index) // decltype(arr) resolves to std::vector<int>
```

然而，如果arr是引用类型（例如，通过引用传递的数组），则上述方法不起作用。需要首先从arr中删除引用：

```C++
template <typename T>
void printArray(const std::vector<T>& arr)
{
	// arr 可以是引用或者非引用类型
	for (typename std::remove_reference_t<decltype(arr)>::size_type index { 0 }; index < arr.size(); ++index)
		std::cout << arr[index] << ' ';
}
```

不幸的是，这不再是简洁或容易记住。

由于size_type几乎总是size_t的typedef，因此许多程序员只是完全跳过使用size_type，而使用更容易记住的std::size_t:

```C++
    for (std::size_t index { 0 }; index < arr.size(); ++index)
```

除非您正在使用自定义分配器，否则我们认为这是一种合理的方法。


***
## 使用有符号循环变量

尽管这使得使用标准库容器类型变得有点困难，但使用有符号循环变量与我们代码其余部分中采用的最佳实践是一致的。而且，越能坚持应用我们的最佳实践，总体错误就会越少。

如果要使用有符号循环变量，则需要解决三个问题：

1. 应该使用什么类型？
2. 获取数组的长度作为有符号值
3. 将有符号循环变量转换为无符号索引

***
## 应该使用什么类型？

这里有三种（有时是四种）好的选择。

1. 除非数组非常大，那么 int 就是足够了（通常有4个字节）。如果不关心任何细节，int是默认的有符号整数。没有什么理由不用int。
2. 如果数组非常大，建议使用 std::ptrdiff_t，它通常作为 std::size_t 的有符号版本。
3. std::ptrdiff_t 是一个比较奇怪的名称，通常建议使用它的别名。

```C++
using Index = std::ptrdiff_t;

// 使用Index的简单示例
for (Index index{ 0 }; index < static_cast<Index>(arr.size()); ++index)
```

在下一节中，将展示这方面的完整示例。

定义自己的类型别名也有一个潜在的未来好处：如果C++标准库发布了一个设计为用作有符号索引的类型，则可以很容易地将index修改为该类型的别名，或者用该类型的名称来查找/替换Index。

```C++
    for (auto index{ static_cast<std::ptrdiff_t>(arr.size())-1 }; index >= 0; --index)
```

在C++23中，Z后缀可以用来定义std::size_t的对应的有符号类型（大概率是std::ptrdiff_t）的字面值：

```C++
    for (auto index{ 0Z }; index < static_cast<std::ptrdiff_t>(arr.size()); ++index)
```

***
## 获取数组的长度作为有符号值

在C++20之前，最好的办法是将返回的长度转换为有符号整数:

```C++
#include <iostream>
#include <vector>

using Index = std::ptrdiff_t;

int main()
{
    std::vector arr{ 9, 7, 5, 3, 1 };

    for (auto index{ static_cast<Index>(arr.size())-1 }; index >= 0; --index)
        std::cout << arr[static_cast<std::size_t>(index)] << ' ';

    return 0;
}
```

这样，arr.size()返回的无符号值将被转换为有符号类型，因此比较运算符将比较两个有符号操作数。由于有符号索引在变为负时不会溢出，因此不存在使用无符号索引时遇到的环绕问题。

这种方法的缺点是它使循环变得混乱，使其更难阅读。可以通过将长度移出循环来解决这一问题：

```C++
#include <iostream>
#include <vector>

using Index = std::ptrdiff_t;

int main()
{
    std::vector arr{ 9, 7, 5, 3, 1 };

    auto length{ static_cast<Index>(arr.size()) }; 
    for (auto index{ length-1 }; index >= 0; --index)
        std::cout << arr[static_cast<std::size_t>(index)] << ' ';

    return 0;
}
```

在C++20之后，请使用std::ssize()。

C++20中引入std::ssize()，这证明C++的设计者现在认为有符号索引是可行的。此函数将数组类型的大小作为有符号类型返回（可能是ptrdiff_t）。

```C++
#include <iostream>
#include <vector>

int main()
{
    std::vector arr{ 9, 7, 5, 3, 1 };

    for (auto index{ std::ssize(arr)-1 }; index >= 0; --index) // std::ssize 在 C++20 中引入
        std::cout << arr[static_cast<std::size_t>(index)] << ' ';

    return 0;
}
```

***
## 将有符号循环变量转换为无符号索引

一旦有了有符号循环变量，每当我们试图将该有符号循环变量用作索引时，就会遇到隐式符号转换警告。因此，需要某种方法将有符号循环变量转换为无符号值，只要打算将其用作索引。

```C++
#include <iostream>
#include <type_traits> // for std::is_integral and std::is_enum
#include <vector>

using Index = std::ptrdiff_t;

template <typename T>
constexpr std::size_t toUZ(T value)
{
    // 确保 T 是整数类型
    static_assert(std::is_integral<T>() || std::is_enum<T>());
    
    return static_cast<std::size_t>(value);
}

int main()
{
    std::vector arr{ 9, 7, 5, 3, 1 };

    auto length { static_cast<Index>(arr.size()) };  // in C++20, 推荐 std::ssize()
    for (auto index{ length-1 }; index >= 0; --index)
        std::cout << arr[toUZ(index)] << ' '; // 使用 toUZ() 来避免符号转换告警

    return 0;
}
```

在上面的示例中，创建了一个名为toUZ()的函数，该函数旨在将整数值转换为std::size_t类型的值。"arr[ toUZ(index) ]"的可读性较好。

在前面的课程中，讨论了std::string拥有字符串，而std::string_view是存在于其他地方的字符串的视图。关于std::string_view的一个妙处是它可以查看不同类型的字符串（C样式的字符串字面值、std::string和其他std::string_view），但保持一致的接口供我们使用。

虽然我们不能修改标准库容器来接受带符号的整数索引，但我们可以创建自己的自定义视图类来“查看”标准库容器类。在这样做的过程中，可以定义自己的接口，以按我们希望的方式工作。

在下面的示例中，定义了一个自定义视图类，该类可以查看支持索引的任何标准库容器。我们的接口将做两件事：

1. 允许我们使用带符号整数类型的运算符[]访问元素。
2. 以有符号整数类型获取容器的长度（因为std::ssize（）仅在C++20上可用）。

这使用操作符重载，这是尚未讨论的主题，以便实现操作符[]。您不需要知道SignedArrayView是如何实现的，就可以使用它。

SignedArrayView.h:

```C++
#ifndef SIGNED_ARRAY_VIEW_H
#define SIGNED_ARRAY_VIEW_H

#include <cstddef> // for std::size_t and std::ptrdiff_t

// SignedArrayView 提供了支持索引的容器类的一个视图
// 来允许我们使用有符号整形
template <typename T>
class SignedArrayView // C++17
{
private:
    T& m_array;

public:
    using Index = std::ptrdiff_t;

    SignedArrayView(T& array)
        : m_array{ array } {}

    // 重载 operator[] 以使用有符号整形
    constexpr auto& operator[](Index index) { return m_array[static_cast<typename T::size_type>(index)]; }
    constexpr const auto& operator[](Index index) const { return m_array[static_cast<typename T::size_type>(index)]; }
    constexpr auto ssize() const { return static_cast<Index>(m_array.size()); }
};

#endif
```

main.cpp：

```C++
#include <iostream>
#include <vector>
#include "SignedArrayView.h"

int main()
{
    std::vector arr{ 9, 7, 5, 3, 1 };
    SignedArrayView sarr{ arr }; // 创建 std::vector 的一个视图

    for (auto index{ sarr.ssize() - 1 }; index >= 0; --index)
        std::cout << sarr[index] << ' '; // 使用有符号整数作为索引

    return 0;
}
```

***
## 唯一明智的选择：完全避免索引！

上面介绍的所有选项都有自己的缺点，因此很难推荐一种方法而不是另一种。然而，有一种选择比其他选择明智得多：完全避免使用整数值进行索引。

C++提供了其他几种方法来遍历数组,根本不使用索引。如果不使用索引，那么就不会遇到所有这些有符号/无符号转换问题。

用于无索引数组遍历的两种常见方法包括range for和迭代器。

{{< alert success >}}
**相关内容**

在下一课中，将讨论 range for。迭代器则在后续专门的一章介绍。

{{< /alert >}}

{{< alert success >}}
**最佳实践**

尽可能避免使用整数值进行数组索引。

{{< /alert >}}

***

{{< prevnext prev="/basic/chapter16/vec-loop/" next="/basic/chapter16/range-for/" >}}
16.5 数组和循环
<--->
16.7 基于范围的for循环（range for / for each）
{{< /prevnext >}}
