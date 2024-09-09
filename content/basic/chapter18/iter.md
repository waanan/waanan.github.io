---
title: "迭代器简介"
date: 2024-08-19T20:14:59+08:00
---

在编程中，迭代数据的数组（或其他结构）是非常常见的事情。到目前为止，我们已经介绍了许多不同的方法:使用循环和索引（对于for循环和while循环），使用指针和指针算术，以及使用基于范围的循环:

```C++
#include <array>
#include <cstddef>
#include <iostream>

int main()
{
    // 在 C++17, data 类型被推导为 std::array<int, 7>
    // 如果你编译失败，请看下面的警告
    std::array data{ 0, 1, 2, 3, 4, 5, 6 };
    std::size_t length{ std::size(data) };

    // 使用显式索引的while循环
    std::size_t index{ 0 };
    while (index < length)
    {
        std::cout << data[index] << ' ';
        ++index;
    }
    std::cout << '\n';

    // 使用显式索引的for循环
    for (index = 0; index < length; ++index)
    {
        std::cout << data[index] << ' ';
    }
    std::cout << '\n';

    // 使用指针的for循环 (注: ptr 不能时 const, 因为需要进行累加)
    for (auto ptr{ &data[0] }; ptr != (&data[0] + length); ++ptr)
    {
        std::cout << *ptr << ' ';
    }
    std::cout << '\n';

    // 基于范围的for循环
    for (int i : data)
    {
        std::cout << i << ' ';
    }
    std::cout << '\n';

    return 0;
}
```

可以使用索引来访问元素，但它也仅在容器（例如数组）提供对元素的直接访问时有效（数组提供这种访问，但其他类型的容器（如列表）不提供这种访问）。

使用指针和指针算术进行循环是冗长的，并且可能会使不知道指针算术规则的读者感到困惑。指针算法也仅在元素在内存中连续时有效（这对于数组是正确的，但对于其他类型的容器（如列表、树和map）不是正确的）。

基于范围的for循环更有趣一些，因为在容器中迭代的机制是隐藏的——然而，它们仍然适用于各种不同的结构（数组、列表、树、映射等）。这些是如何工作的？它们使用迭代器。

{{< alert success >}}
**警告**

本课中的示例使用名为类模板参数推导的C++17功能，从模板变量的初始值设定项中推导模板变量的模板参数。在上面的示例中，当编译器看到"std::array data{0，1，2，3，4，5，6};"，它将推断我们需要"std::array\<int，7\> data{0, 1, 2, 3, 4, 5, 6};"。

如果编译器未启用C++17，则会出现类似于“在“data”之前缺少模板参数”的错误。在这种情况下，最好的办法是启用C++17。或者，可以将使用类模板参数推导的行替换为具有显式模板参数的行（例如，将"std::array data{0，1，2，3，4，5，6};"替换为"std::array\<int，7\> data{0, 1, 2, 3, 4, 5, 6};"

{{< /alert >}}

{{< alert success >}}
**对于高级读者**

指针也可以用于迭代某些非顺序结构。在链接列表中，每个元素通过指针连接到前一个元素。可以通过跟踪指针链来迭代列表。

{{< /alert >}}

***
## 迭代器

迭代器是设计用于遍历容器（例如，数组中的值或字符串中的字符）的对象，提供对沿途每个元素的访问。

容器可以提供不同类型的迭代器。例如，数组容器可以提供按正向顺序遍历数组的正向迭代器，以及按反向顺序遍历的反向迭代器。

一旦创建了适当类型的迭代器，程序员就可以使用迭代器提供的接口来遍历和访问元素，而不必担心正在进行的是哪种遍历，或者数据是如何存储在容器中的。由于C++迭代器通常使用相同的接口进行遍历（操作符++移动到下一个元素）和访问（操作符*访问当前元素），因此我们可以使用一致的方法迭代各种不同的容器类型。

***
## 指针作为迭代器

最简单的迭代器类型是指针，它（使用指针算术）用于顺序存储在内存中的数据。让我们使用指针和指针算法重新访问一个简单的数组遍历:

```C++
#include <array>
#include <iostream>

int main()
{
    std::array data{ 0, 1, 2, 3, 4, 5, 6 };

    auto begin{ &data[0] };
    // 注意end时结束后的下一个元素
    auto end{ begin + std::size(data) };

    // 使用指针的 for 循环
    for (auto ptr{ begin }; ptr != end; ++ptr) // ++ 移动ptr指向下一个元素
    {
        std::cout << *ptr << ' '; // 间接获取当前遍历的元素
    }
    std::cout << '\n';

    return 0;
}
```

输出:

```C++
0 1 2 3 4 5 6
```

在上面，我们定义了两个变量:begin（指向容器的开始）和end（标记终结点）。对于数组，结束标记通常是内存中结束后的下一个元素所在的位置。

然后指针在begin和end之间迭代，可以通过解指针的引用来访问当前元素。

{{< alert success >}}
**警告**

您可能想通过数组和取地址语法来获取end，如下所示:

```C++
int* end{ &data[std::size(data)] };
```

但这会导致未定义的行为，因为data\[std::size(data)\]隐式解引用数组末尾以外的元素。

相反，请使用:

```C++
int* end{ data.data() + std::size(data) }; // data() 返回第一个元素的地址
```

{{< /alert >}}

***
## 标准库迭代器

迭代是如此常见的操作，以至于所有标准库容器都为迭代提供直接支持。我们可以通过方便地命名为begin()和end()的成员函数简单地向容器请求起点和终点，而不是计算自己的起点和终点:

```C++
#include <array>
#include <iostream>

int main()
{
    std::array array{ 1, 2, 3 };

    // 通过begin和end成员函数，获取数组的起点和终点
    auto begin{ array.begin() };
    auto end{ array.end() };

    for (auto p{ begin }; p != end; ++p) // ++ 移动p指向下一个元素
    {
        std::cout << *p << ' '; // 解引用获取当前遍历的元素
    }
    std::cout << '\n';

    return 0;
}
```

这将打印:

```C++
1 2 3
```

迭代器头文件还包含两个可以使用的泛型函数（std::begin和std:∶end）。

```C++
#include <array>    // includes <iterator>
#include <iostream>

int main()
{
    std::array array{ 1, 2, 3 };

    // 使用 std::begin 和 std::end 取获取开始和结束.
    auto begin{ std::begin(array) };
    auto end{ std::end(array) };

    for (auto p{ begin }; p != end; ++p) // ++ 移动p指向下一个元素
    {
        std::cout << *p << ' '; // 解引用获取当前遍历的元素
    }
    std::cout << '\n';

    return 0;
}
```

这也会打印:

```C++
1 2 3
```

现在不要担心迭代器的类型，我们将在后面的一章中重新研究迭代器。重要的是迭代器负责遍历容器的概念。我们只需要四件事:开始点、结束点、将迭代器移动到下一个元素（或结束）的操作符++，以及获取当前元素的值的操作符*。

{{< alert success >}}
**提示**

C样式数组的std::begin和std::end在\<iterator\>头中定义。

支持迭代器的容器的std::begin和std::end在这些容器的头文件中定义（例如\<array\>、\<vector\>）。

{{< /alert >}}

***
## 运算符< 对比 运算符=!

在之前的循环示例中，我们注意到使用运算符<比运算符=！更好:

```C++
    for (index = 0; index < length; ++index)
```

对于迭代器，通常使用运算符=！来测试迭代器是否已到达end元素，请执行以下操作:

```C++
    for (auto p{ begin }; p != end; ++p)
```

这是因为某些迭代器类型在关系上不可比较。运算符=！适用于所有迭代器类型。

***
## 返回到基于范围的循环

所有同时具有begin()和end()成员函数的类型，或者可以使用std::begin与std::end的类型，都可以使用基于范围的for循环。

```C++
#include <array>
#include <iostream>

int main()
{
    std::array array{ 1, 2, 3 };

    // 这与前面的遍历示例其实一致
    for (int i : array)
    {
        std::cout << i << ' ';
    }
    std::cout << '\n';

    return 0;
}
```

在幕后，基于范围的for循环调用要迭代的类型的begin()和end()。array具有begin和end成员函数，因此我们可以在基于范围的循环中使用它。C风格的固定数组可以与std::begin和std:∶end函数一起使用，因此我们也可以使用基于范围的循环来循环它们。然而，动态C样式数组（或退化的C样式数组）无法工作，因为它们没有std::end函数（因为类型信息不包含数组的长度）。

稍后，您将学习如何将这些函数添加到类型中，以便它们也可以与基于范围的for循环一起使用。

基于范围的for循环并不是唯一使用迭代器的东西。迭代器也用于std::sort和其他算法。现在您知道了它们是什么，您会注意到它们在标准库中使用得相当多。

***
## 迭代器无效（悬空迭代器）

与指针和引用很相似，如果被迭代的元素更改地址或被销毁，迭代器会保持“悬空”状态。当这种情况发生时，我们说迭代器已经失效。访问无效迭代器会产生未定义的行为。

一些修改容器的操作（例如将元素添加到std::vector）可能会产生副作用，导致容器中的元素更改地址。当这种情况发生时，这些元素的现有迭代器将无效。好的C++参考文档应该标注哪些容器操作可以或将使迭代器无效。例如，请参阅cppreference上std::vector的“迭代器无效”部分。

由于基于范围的for循环在幕后使用迭代器，因此我们必须小心，不要做任何使我们正在主动遍历的容器的迭代器无效的事情:

```C++
#include <vector>

int main()
{
    std::vector v { 0, 1, 2, 3 };

    for (auto num : v) // 隐式的在 v 上使用迭代器
    {
        if (num % 2 == 0)
            v.push_back(num + 1); // 会影响 v 的迭代器, 导致未定义的行为
    }

    return 0;
}
```

下面是迭代器无效的另一个例子:

```C++
#include <iostream>
#include <vector>

int main()
{
	std::vector v{ 1, 2, 3, 4, 5, 6, 7 };

	auto it{ v.begin() };

	++it; // 移动到第二个元素
	std::cout << *it << '\n'; // ok: 打印 2

	v.erase(it); // 删除正在遍历的元素

	// erase() 使迭代器失效
	// 所以 "it" 现在时无效状态

	++it; // 未定义的行为
	std::cout << *it << '\n'; // 未定义的行为

	return 0;
}
```

通过为无效迭代器分配有效迭代器（例如，begin()、end()或返回迭代器的其他函数），可以重新使迭代器有效。

erase函数的作用是:返回被删除元素的下一个元素的迭代器（如果最后一个元素被删除，则返回end()）。因此，我们可以如下修复上述代码:

```C++
#include <iostream>
#include <vector>

int main()
{
	std::vector v{ 1, 2, 3, 4, 5, 6, 7 };

	auto it{ v.begin() };

	++it; // 移动到第二个元素
	std::cout << *it << '\n';

	it = v.erase(it); // 删除当前元素, 将 `it` 指向下一个元素

	std::cout << *it << '\n'; // 现在 ok, 打印 3

	return 0;
}
```

***

{{< prevnext prev="/basic/chapter18/sort-arr/" next="/" >}}
18.0 对数组进行排序
<--->
主页
{{< /prevnext >}}
