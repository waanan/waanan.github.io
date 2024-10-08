---
title: "算法标准库简介"
date: 2024-08-19T20:14:59+08:00
---

新程序员通常花费大量时间编写定制的循环来执行相对简单的任务，例如排序或计数或搜索数组。这些循环可能是有问题的，有可能犯各种错误，或者在整体可维护性方面，因为循环可能很难理解。

由于搜索、计数和排序是如此常见的操作，C++标准库附带了一系列函数，可以在短短的几行代码中完成这些事情。此外，这些标准库函数经过预测试，效率高，可以在各种不同的容器类型上工作，并且许多支持并行化（将多个CPU线程分配给同一任务以更快地完成任务的能力）。

算法库中提供的功能通常分为三类:

1. 查看—用于查看（但不修改）容器中的数据。例如搜索和计数。
2. 修改——用于修改容器中的数据。例如排序和打乱数组。
3. 辅助——用于根据数据成员的值生成结果。包括针对元素乘以值的对象，或确定元素对应按何种顺序排序的对象。

这些算法位于algorithm库中。在本课中，我们将探索一些更常见的算法——但还有更多，我们鼓励您阅读对应的文档，以查看所有可用的算法！

***
## 使用std::find按值查找元素

std::find搜索容器中第一次出现的值。find接受3个参数:序列中开始元素的迭代器、序列中结束元素的迭代器和要搜索的值。它返回一个迭代器，指向元素（如果找到）或容器的末尾（如果找不到元素）。

例如:

```C++
#include <algorithm>
#include <array>
#include <iostream>

int main()
{
    std::array arr{ 13, 90, 99, 5, 40, 80 };

    std::cout << "Enter a value to search for and replace with: ";
    int search{};
    int replace{};
    std::cin >> search >> replace;

    // 这里忽略输入校验

    // std::find 返回指向元素的迭代器 (或者容器的end)
    // 将返回的迭代器存储在变量中
    // 这里使用auto，因为我们不关心具体的类型
    auto found{ std::find(arr.begin(), arr.end(), search) };

    // 如果没找到
    // 那么迭代器指向 end() 
    if (found == arr.end())
    {
        std::cout << "Could not find " << search << '\n';
    }
    else
    {
        // 覆盖找到的值
        *found = replace;
    }

    for (int i : arr)
    {
        std::cout << i << ' ';
    }

    std::cout << '\n';

    return 0;
}
```

找到元素时的运行样例

```C++
Enter a value to search for and replace with: 5 234
13 90 99 234 40 80
```

找不到元素时的运行样例

```C++
Enter a value to search for and replace with: 0 234
Could not find 0
13 90 99 5 40 80
```

***
## 使用std::find_if查找与某些条件匹配的元素

有时，我们希望查看容器中是否存在与某些条件匹配的值（例如，包含特定子字符串的字符串），而不是精确的值。在这种情况下，std::find_if是完美的。

std::find_if函数的工作方式类似于std::find，但不是传递要搜索的特定值，而是传递一个可调用对象，例如函数指针（或lambda，我们稍后将介绍）。对于迭代的每个元素，std::find_if将调用该函数（将元素作为参数传递给函数），如果找到匹配，函数返回true，否则返回false。

下面是一个示例，我们使用std::find_if检查是否有任何元素包含子字符串“nut”:

```C++
#include <algorithm>
#include <array>
#include <iostream>
#include <string_view>

// 如果匹配，返回true
bool containsNut(std::string_view str)
{
    // 如果没有找到，std::string_view::find 返回 std::string_view::npos
    // 否则返回对应子串在str中的位置
    return (str.find("nut") != std::string_view::npos);
}

int main()
{
    std::array<std::string_view, 4> arr{ "apple", "banana", "walnut", "lemon" };

    // 遍历数组，看是否任一字符串包含 "nut"
    auto found{ std::find_if(arr.begin(), arr.end(), containsNut) };

    if (found == arr.end())
    {
        std::cout << "No nuts\n";
    }
    else
    {
        std::cout << "Found " << *found << '\n';
    }

    return 0;
}
```

输出

```C++
Found walnut
```

如果要手工编写上面的示例，则至少需要三个循环（一个循环遍历数组，两个循环匹配子串）。标准库函数允许我们在几行代码中完成相同的事情！

***
## 使用std::count和std::count_if计算出现的次数

std::count和std::countif搜索满足条件的元素或元素的所有出现次数。

在下面的示例中，我们将计算有多少个元素包含子字符串“nut”:

```C++
#include <algorithm>
#include <array>
#include <iostream>
#include <string_view>

bool containsNut(std::string_view str)
{
	return (str.find("nut") != std::string_view::npos);
}

int main()
{
	std::array<std::string_view, 5> arr{ "apple", "banana", "walnut", "lemon", "peanut" };

	auto nuts{ std::count_if(arr.begin(), arr.end(), containsNut) };

	std::cout << "Counted " << nuts << " nut(s)\n";

	return 0;
}
```

输出

```C++
Counted 2 nut(s)
```

***
## 使用std::sort自定义排序

我们以前使用std::sort以升序对数组进行排序，但std::sort可以做更多的事情。有一个版本的std::sort，它将函数作为其第三个参数，允许我们根据自己的喜好进行排序。该函数接受两个参数进行比较，如果第一个参数应排在第二个参数之前，则返回true。默认情况下，std::sort按升序对元素进行排序。

让我们使用std::sort，使用名为greater的自定义比较函数以相反的顺序对数组进行排序:

```C++
#include <algorithm>
#include <array>
#include <iostream>

bool greater(int a, int b)
{
    // 如果a比b大，那么a应该排在b之前
    return (a > b);
}

int main()
{
    std::array arr{ 13, 90, 99, 5, 40, 80 };

    // 将 greater 传给 std::sort
    std::sort(arr.begin(), arr.end(), greater);

    for (int i : arr)
    {
        std::cout << i << ' ';
    }

    std::cout << '\n';

    return 0;
}
```

输出

```C++
99 90 80 40 13 5
```

再一次，我们可以在几行代码中对数组进行排序，而不是编写自定义循环函数！

我们的greater函数需要2个参数，但我们没有传递任何参数，那么它们从哪里来呢？当我们使用没有括号的greater函数时，它只是函数指针，而不是调用。您可能还记得，当我们试图打印没有括号的函数时，std::cout打印了“1”。sort使用该指针，并使用数组的2个元素调用实际的greater函数。在后面的一章中，我们将详细讨论函数指针。

由于降序排序非常常见，C++也为其提供了一个自定义类型（名为std::greater）（这是函数头的一部分）。在上面的示例中，我们可以替换:

```C++
  std::sort(arr.begin(), arr.end(), greater); // 调用自定义的 greater 函数
```

改为:

```C++
  std::sort(arr.begin(), arr.end(), std::greater{}); // 使用标准库的函数
  // 在 C++17 之前, 必须制定 std::greater 的模版参数
  std::sort(arr.begin(), arr.end(), std::greater<int>{}); // 使用标准库的函数
```

请注意，std::greater{}需要花括号，因为它不是可调用的函数。它是一种类型，为了使用它，我们需要实例化该类型的对象。花括号实例化该类型的匿名对象（然后将其作为参数传递给std::sort）。


***
## std::sort如何使用比较函数（高级读者）

为了进一步解释std::sort如何使用比较函数，我们必须返回到之前讲解的选择排序。

```C++
#include <iostream>
#include <iterator>
#include <utility>

void sort(int* begin, int* end)
{
    for (auto startElement{ begin }; startElement != end-1; ++startElement)
    {
        auto smallestElement{ startElement };

        // std::next 返回下一个需要迭代的元素, 类似于 (startElement + 1)
        for (auto currentElement{ std::next(startElement) }; currentElement != end; ++currentElement)
        {
            if (*currentElement < *smallestElement)
            {
                smallestElement = currentElement;
            }
        }

        std::swap(*startElement, *smallestElement);
    }
}

int main()
{
    int array[]{ 2, 1, 9, 4, 5 };

    sort(std::begin(array), std::end(array));

    for (auto i : array)
    {
        std::cout << i << ' ';
    }

    std::cout << '\n';

    return 0;
}
```

到目前为止，这并不是什么新鲜事，sort总是将元素从低到高排序。要添加比较函数，我们必须使用新类型std::function\<bool（int，int）\>来存储接受2个int参数并返回bool的函数。现在将这种类型视为魔术，我们将在后面解释它。

```C++
void sort(int* begin, int* end, std::function<bool(int, int)> compare)
```

我们现在可以将比较函数（如greater）传递给排序，但排序如何使用它？我们需要做的就是更换线路

```C++
if (*currentElement < *smallestElement)
```

改为

```C++
if (compare(*currentElement, *smallestElement))
```

现在，sort的调用者可以选择如何比较两个元素。

```C++
#include <functional> // std::function
#include <iostream>
#include <iterator>
#include <utility>

// sort 接收比较函数
void sort(int* begin, int* end, std::function<bool(int, int)> compare)
{
    for (auto startElement{ begin }; startElement != end-1; ++startElement)
    {
        auto smallestElement{ startElement };

        for (auto currentElement{ std::next(startElement) }; currentElement != end; ++currentElement)
        {
            // 比较函数用来比较元素该如何排序
            if (compare(*currentElement, *smallestElement))
            {
                smallestElement = currentElement;
            }
        }

        std::swap(*startElement, *smallestElement);
    }
}

int main()
{
    int array[]{ 2, 1, 9, 4, 5 };

    // 使用 std::greater 来按降序排序
    // (这里sort前加了::，指定全局命名空间，来避免和其它定义冲突)
    ::sort(std::begin(array), std::end(array), std::greater{});

    for (auto i : array)
    {
        std::cout << i << ' ';
    }

    std::cout << '\n';

    return 0;
}
```

***
## 使用std::for_each对容器的所有元素执行某些操作

for_each接受列表作为输入，并将自定义函数应用于每个元素。当我们希望对列表中的每个元素执行相同的操作时，这非常有用。

下面是一个使用std::for_each将数组中的所有数字加倍的示例:

```C++
#include <algorithm>
#include <array>
#include <iostream>

void doubleNumber(int& i)
{
    i *= 2;
}

int main()
{
    std::array arr{ 1, 2, 3, 4 };

    std::for_each(arr.begin(), arr.end(), doubleNumber);

    for (int i : arr)
    {
        std::cout << i << ' ';
    }

    std::cout << '\n';

    return 0;
}
```

输出:

```C++
2 4 6 8
```


对于新开发人员来说，这似乎是最不必要的算法，因为具有基于范围的for循环的等效代码更短、更容易。但std::for_each有一些好处。让我们将std::for_each与基于范围的for循环进行比较。

```C++
std::ranges::for_each(arr, doubleNumber); // 从 C++20, 不再需要指定 begin() 和 end().
// std::for_each(arr.begin(), arr.end(), doubleNumber); // 在 C++20 之前

for (auto& i : arr)
{
    doubleNumber(i);
}
```

使用std::for_each，我们的意图是明确的。用arr的每个元素调用doubleNumber。在基于范围的for循环中，我们必须添加一个新的变量，i。这会导致程序员在疲劳或不注意时可能会犯几个错误。首先，如果我们不使用auto，可能会存在隐式转换。我们可以忘记“&”号，而doubleNumber不会影响数组。我们可能会意外地将除i之外的变量传递给doubleNumber。这些错误不会在std::for_each中发生。

此外，std::for_each可以跳过容器开头或结尾的元素，例如，要跳过arr的第一个元素，可以使用std::next将begin前进到下一个元素。

```C++
std::for_each(std::next(arr.begin()), arr.end(), doubleNumber);
// 现在 arr 是 [1, 4, 6, 8]. 第一个元素被跳过
```

对于基于范围的for循环，这是不可能的。

与许多算法一样，std::for_each可以并行化以实现更快的处理，这使得它比基于范围的for循环更适合大型项目和大数据。

***
## 性能以及执行顺序

算法库中的许多算法对它们的执行方式做出了某种保证。通常，这些要么是性能保证，要么是关于它们的执行顺序的保证。例如，std::for_each保证每个元素只访问一次，并且元素将按向前顺序访问。

虽然大多数算法提供某种性能保证，但具有执行顺序保证的算法较少。对于这种算法，我们需要小心，不要假设元素将被访问或处理的顺序。

例如，如果我们使用标准库算法将第一个值乘以1，将第二个值乘以2，将第三个值乘以3，等等……我们希望避免使用任何不保证向前顺序执行的算法！

以下算法保证顺序执行:std::for_each、std::copy、std::copy_backward、std::move和std::move_backway。由于迭代器前向的要求，许多其他算法（特别是使用前向迭代器的算法）是隐式顺序的。

{{< alert success >}}
**最佳实践**

在使用特定算法之前，请确保性能和执行顺序保证适用于您的特定用例。

{{< /alert >}}

***
## C++20中的Range

必须显式地将arr.begin()和arr.end()传递给每个算法，这有点烦人。但不要担心——C++20增加了Range功能，允许我们简单地只传递arr。这将使我们的代码更短，更可读。

***
## 结论

算法库有大量有用的功能，可以使代码更简单、更健壮。在本课中，我们只讨论了一小部分，但由于大多数函数的工作原理都非常相似，因此一旦您知道其中一些函数是如何工作的，您就可以利用它们中的大多数。

{{< alert success >}}
**最佳实践**

优先使用算法库中的函数，而不是编写自己的函数来执行相同的操作。

{{< /alert >}}

***

{{< prevnext prev="/basic/chapter18/iter/" next="/basic/chapter18/time-code/" >}}
18.1 迭代器简介
<--->
18.3 为代码计时
{{< /prevnext >}}
