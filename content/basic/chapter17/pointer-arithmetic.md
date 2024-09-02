---
title: "指针运算和下标"
date: 2024-08-13T13:06:02+08:00
---

在前面，我们提到了数组按顺序存储在内存中。在本课中，我们将深入了解数组索引的工作原理。

尽管我们在以后的课程中不会使用下面介绍的访问方式，但本课程中涵盖的主题将让您深入了解基于范围的for循环实际上是如何工作的，并且在稍后讨论迭代器时将再次派上用场。

***
## 什么是指针运算？

指针运算是一种功能，允许我们将某些整数算术运算符（加法、减法，自增，自减）应用于指针，以产生新的内存地址。

给定某个指针ptr，ptr+1返回内存中下一个对象的地址（基于所指向的类型）。因此，如果ptr是int*，int是4个字节，ptr+1将返回ptr后4个字节的内存地址，ptr+2将返回ptr后8个字节的存储器地址。

```C++
#include <iostream>

int main()
{
    int x {};
    const int* ptr{ &x }; // 假设 int 是 4 字节

    std::cout << ptr << ' ' << (ptr + 1) << ' ' << (ptr + 2) << '\n';

    return 0;
}
```

在作者的机器上，打印:

```C++
00AFFD80 00AFFD84 00AFFD88
```

请注意，每个内存地址都比前一个地址大4个字节。

虽然不太常见，但指针运算也适用于减法。给定某个指针ptr，ptr-1返回内存中前一个对象的地址（基于所指向的类型）。

```C++
#include <iostream>

int main()
{
    int x {};
    const int* ptr{ &x }; // 假设 int 是 4 字节

    std::cout << ptr << ' ' << (ptr - 1) << ' ' << (ptr - 2) << '\n';

    return 0;
}
```

在作者的机器上，打印:

```C++
00AFFD80 00AFFD7C 00AFFD78
```

在这种情况下，每个存储器地址都比前一个少4个字节。

将自增（++）和之间（--）操作符应用于指针分别执行与指针加法和指针减法相同的操作，但实际上修改指针持有的地址。

给定某个int值x，++x是x=x+1的简写。类似地，给定一些指针ptr，++ptr是ptr=ptr+1的简写，它执行指针运算并将结果分配回ptr。

```C++
#include <iostream>

int main()
{
    int x {};
    const int* ptr{ &x }; // 假设 int 是 4 字节

    std::cout << ptr << '\n';

    ++ptr; // ptr = ptr + 1
    std::cout << ptr << '\n';

    --ptr; // ptr = ptr - 1
    std::cout << ptr << '\n';

    return 0;
}
```

在作者的机器上，打印:

```C++
00AFFD80 00AFFD84 00AFFD80
```

{{< alert success >}}
**关键点**

指针算法返回下一个/前一个对象的地址（基于所指向的类型），而不是下一个或前一个地址。

{{< /alert >}}

{{< alert success >}}
**警告**

从技术上讲，以上是未定义的行为。根据C++标准，指针运算仅在指针和结果位于同一数组（或超过末尾的数组）内时有效。然而，现代C++实现通常不强制执行这一点，并且通常不会禁止您在数组之外使用指针算法。

{{< /alert >}}

***
## 通过指针算法实现数组访问

在上一课中，我们注意到运算符[]可以应用于指针:

```C++
#include <iostream>

int main()
{
    const int arr[] { 9, 7, 5, 3, 1 };
    
    const int* ptr{ arr }; // 保存数组初始元素的地址
    std::cout << ptr[2];   // 访问第 2 个元素, 打印 5

    return 0;
}
```

让我们更深入地了解一下这里发生了什么。

事实证明，下标操作ptr\[n]\是一种简洁的语法，相当于更详细的表达式*（ ptr + n ）。您将注意到，这只是指针运算，带有一些额外的括号以确保事物以正确的顺序计算，以及一个隐式解引用以获取该地址处的对象。

首先，用arr初始化ptr。当arr用作初始值设定项时，它退化为一个指针，该指针保存索引为0的元素的地址。因此，ptr现在保存元素0的地址。

接下来，我们打印ptr\[2]\。ptr\[2\]等价于*（ ptr + 2 ）。ptr+2返回对象的地址，该对象是ptr之后的两个对象，这是索引为2的元素。然后将该地址处的对象返回给调用者。

让我们来看另一个例子:

```C++
#include <iostream>

int main()
{
    const int arr[] { 3, 2, 1 };

    // 首先，先获取每个元素的信息
    std::cout << &arr[0] << ' ' << &arr[1] << ' ' << &arr[2] << '\n';
    std::cout << arr[0] << ' ' << arr[1] << ' ' << arr[2] << '\n';

    // 来看下是否和指针运算的结果一致
    std::cout << arr << ' ' << (arr+ 1) << ' ' << (arr+ 2) << '\n';
    std::cout << *arr<< ' ' << *(arr+ 1) << ' ' << *(arr+ 2) << '\n';

    return 0;
}
```

在作者的机器上，打印:

```C++
00AFFD80 00AFFD84 00AFFD88
3 2 1
00AFFD80 00AFFD84 00AFFD88
3 2 1
```

您会注意到，arr保存的是地址00AFFD80，（arr+1）在4个字节的地址，而（arr+2）在8个字节之后的地址。可以通过这些地址获得对应的元素。

由于数组元素在内存中总是连续的，因此如果arr是数组元素0的指针，*（arr+n）将返回数组中的第n个元素。

这是数组起始位置基于0而不是基于1的主要原因。它使数学计算更快（因为编译器不必在计算下标时减去1）！

{{< alert success >}}
**旁白**

作为一个简单的细节，因为编译器计算指针下标时将ptr\[n\]转换为*（ ptr + n ），这意味着我们也可以写为n\[ptr\]！编译器将其转换为*（ n + ptr ），这在行为上与*（ ptr + n ）相同。但实际上不要这样做，因为这很令人困惑。

{{< /alert >}}

***
## 指针运算和下标是相对地址

当第一次学习数组下标时，很自然地假设索引表示数组中的固定元素:索引0总是第一个元素，索引1总是第二个元素，等等…

这是一种幻觉。数组索引实际上是相对位置。索引看起来是固定的，因为我们几乎总是从数组的开始（元素0）进行索引！

记住，给定一些指针ptr，\*（ptr+1）和ptr\[1\]都返回内存中的下一个对象（基于所指向的类型）。其次是相对项，而不是绝对项。因此，如果ptr指向元素0，则\*（ptr+1）和ptr\[1\]都将返回元素1。但如果ptr指向元素3，则\*（ptr+1）和ptr\[1\]都将返回元素4！

下面的示例演示了这一点:

```C++
#include <array>
#include <iostream>

int main()
{
    const int arr[] { 9, 8, 7, 6, 5 };
    const int *ptr { arr }; // 退化为指向第 0 个元素的指针

    // 验证 ptr 指向第 0 个元素
    std::cout << *ptr << ptr[0] << '\n'; // 打印 99
    // Prove that ptr[1] is element 1
    std::cout << *(ptr+1) << ptr[1] << '\n'; // 打印 88

    // ptr现在指向第 3 个元素
    ptr = &arr[3];

    // 验证 ptr 指向第 3 个元素
    std::cout << *ptr << ptr[0] << '\n'; // 打印 66
    // 验证 ptr[1] 是第 4 个元素!
    std::cout << *(ptr+1) << ptr[1] << '\n'; // 打印 55
 
    return 0;
}
```

当然，您也会注意到，如果我们不能假设ptr\[1\]总是索引为1的元素，那么程序会更加混乱。因此，建议仅在进行相对定位时使用指针算法。

***
## 负指针

在上一课中，我们提到（与标准库容器类不同）C样式数组的索引可以是无符号整数或有符号整数。这不仅仅是为了方便——实际上可以用负下标索引C样式的数组。这听起来很有趣，但很有道理。

我们刚刚讨论了*（ptr+1）返回内存中的下一个对象。ptr\[1\]只是一个方便的语法来做同样的事情。

在本课的顶部，我们注意到*（ptr-1）返回内存中的前一个对象。想猜猜下标等价物是什么吗？是的，ptr\[-1\]。

```C++
#include <array>
#include <iostream>

int main()
{
    const int arr[] { 9, 8, 7, 6, 5 };

    // ptr 指向第 3 个元素
    const int* ptr { &arr[3] };

    // 验证 ptr 指向第 3 个元素
    std::cout << *ptr << ptr[0] << '\n'; // 打印 66
    // 验证 ptr[-1] 是第 2 个元素!
    std::cout << *(ptr-1) << ptr[-1] << '\n'; // 打印 77
 
    return 0;
}
```

***
## 指针算法可用于遍历数组

指针算法最常见的用途之一是在没有显式索引的情况下迭代C样式的数组。下面的示例说明了如何完成此操作:

```C++
#include <iostream>

int main()
{
	constexpr int arr[]{ 9, 7, 5, 3, 1 };

	const int* begin{ arr };                // 从开头
	const int* end{ arr + std::size(arr) }; // 到结束

	for (; begin != end; ++begin)           // 进行遍历（排除end）
	{
		std::cout << *begin << ' ';     // 打印每个元素
	}

	return 0;
}
```

在上面的例子中，我们在begin所指向的元素（在本例中是数组的元素0）处开始遍历。begin != end 时，循环体执行。在循环中，通过*begin访问当前元素，这只是一个指针解引用。在循环体之后，我们执行++begin，它使用指针算法来让begin以指向下一个元素。begin != end 时，循环体再次执行。这一直持续到 begin != end 为false。

因此，上面打印了:

```C++
9 7 5 3 1
```

请注意，end被设置为数组末尾之后的一个位置。让end保持这个地址是可以的（只要我们不去引用end，因为在那个地址上并没有有效的元素）。这样做是因为它使begin与end的比较尽可能简单（不需要在任何地方加减1）。

在上一课，我们提到数组退化使重构函数变得困难，因为某些东西可以与非退化数组一起工作，但不能与退化数组（如std::size）一起工作。以这种方式遍历数组的一个好处是，我们可以将上面示例的循环部分重构为的单独函数，并且它仍然可以工作:

```C++
#include <iostream>

void printArray(const int* begin, const int* end)
{
	for (; begin != end; ++begin)   // 从begin 遍历到 end （排除 end）
	{
		std::cout << *begin << ' '; // 打印每个遍历的元素
	}
    
	std::cout << '\n';
}

int main()
{
	constexpr int arr[]{ 9, 7, 5, 3, 1 };

	const int* begin{ arr };                // begin 指向开头的元素
	const int* end{ arr + std::size(arr) }; // end 指向结尾的后一个元素

	printArray(begin, end);

	return 0;
}
```

请注意，即使我们从未显式地将数组传递给函数，该程序也会编译并生成正确的结果！因为我们没有传递arr，所以不必在printArray()中处理退化的arr。相反，begin和end包含遍历数组所需的所有信息。

在以后的课程中（当我们介绍迭代器和算法时），我们将看到标准库中充满了函数，这些函数使用begin和end对来定义函数应该在容器的哪些元素上操作。

{{< alert success >}}
**提示**

对于指向C样式数组元素的指针，只要生成的地址是有效数组元素的地址，或者是最后一个元素之后的地址，指针算法就有效。如果指针运算导致地址超出这些界限，则这是未定义的行为（即使结果未解引用）。

{{< /alert >}}

***
## 使用指针算法实现C样式数组上的基本范围的for循环

考虑以下基于循环的范围:

```C++
#include <iostream>

int main()
{
	constexpr int arr[]{ 9, 7, 5, 3, 1 };

	for (auto e : arr)         // 从 `begin` 遍历到 `end` （排除 end）
	{
		std::cout << e << ' '; // 打印每个元素
	}

	return 0;
}
```

如果您查看基于范围的for循环的文档，您将看到它们通常是这样实现的:

```C++
{
    auto __begin = begin-expr;
    auto __end = end-expr;

    for ( ; __begin != __end; ++__begin)
    {
        range-declaration = *__begin;
        loop-statement;
    }
}
```

让我们将上例中基于范围的for循环替换为以下实现:

```C++
#include <iostream>

int main()
{
	constexpr int arr[]{ 9, 7, 5, 3, 1 };

	auto __begin = arr;                // arr 是 begin-expr
	auto __end = arr + std::size(arr); // arr + std::size(arr) 是 end-expr

	for ( ; __begin != __end; ++__begin)
	{
		auto e = *__begin;         // e 是 range-declaration
		std::cout << e << ' ';     // 这里是 loop-statement
	}

	return 0;
}
```

请注意，这与我们在上一节中编写的示例非常相似！唯一的区别是我们将\*__begin分配给e并使用e，而不是直接使用\*__begin！

***

{{< prevnext prev="/basic/chapter17/c-arr-decay/" next="/basic/chapter17/c-str/" >}}
17.7 C样式数组退化
<--->
17.9 C样式字符串
{{< /prevnext >}}
