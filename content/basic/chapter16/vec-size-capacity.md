---
title: "std::vector大小调整和容量"
date: 2024-07-08T11:10:28+08:00
---

在本章前面的课程中，我们介绍了容器、数组和std::vector。我们还讨论了一些主题，如何访问数组元素、获取数组的长度以及如何遍历数组。虽然我们在示例中使用了std::vector，但讨论的概念通常适用于所有数组类型。

在本章的其余课程中，将重点关注使std::vector与大多数其他数组类型显著不同的一件事：实例化后调整自身大小的能力。

***
## 固定大小数组与动态大小数组

大多数数组类型都有一个显著的限制：数组的长度必须在实例化时已知，然后不能更改。这种称为固定大小数组或固定长度数组。array和C样式数组都是固定大小的数组类型。将在下一章进一步讨论这些问题。

另一方面，std::vector是一个动态数组。动态数组（也称为可调整大小的数组）其大小可以在实例化后更改。这种调整大小的能力使std::vector变得特别。

***
## 在运行时调整std::vector的大小

通过调用所需长度的resize()成员函数，可以在实例化后调整std::vector的大小：

```C++
#include <iostream>
#include <vector>

int main()
{
    std::vector v{ 0, 1, 2 }; // 有 3 个元素
    std::cout << "The length is: " << v.size() << '\n';

    v.resize(5);              // resize 到 5 个元素
    std::cout << "The length is: " << v.size() << '\n';

    for (auto i : v)
        std::cout << i << ' ';

    std::cout << '\n';

    return 0;
}
```

这将打印：

```C++
The length is: 3
The length is: 5
0 1 2 0 0
```

这里有两件事需要注意。首先，当调整vector的大小时，现有的元素值被保留！其次，新元素是值初始化的（它对类类型执行默认初始化，对其他类型执行零初始化）。因此，int类型的两个新元素被零初始化为值0。

vector也可以调整为更小：

```C++
#include <iostream>
#include <vector>

void printLength(const std::vector<int>& v)
{
	std::cout << "The length is: "	<< v.size() << '\n';
}

int main()
{
    std::vector v{ 0, 1, 2, 3, 4 }; // 初始长度 5
    printLength(v);

    v.resize(3);                    // resize 为 3
    printLength(v);

    for (int i : v)
        std::cout << i << ' ';

    std::cout << '\n';

    return 0;
}
```

这将打印：

```C++
The length is: 5
The length is: 3
0 1 2
```

***
## 长度与容量

考虑一排12栋房子。我们会说房子的数量（或一排房子的长度）是12。如果我们想知道这些房子中的哪些正在被占用……我们必须以其他方式确定这一点（例如，按门铃，看看是否有人回答）。当我们只有长度时，我们只知道存在多少东西。

现在考虑一盒鸡蛋，其中目前有5个鸡蛋。我们会说，鸡蛋的个数是5。但在这种情况下，还有一个我们关心的维度：如果纸箱满了，它可以装多少鸡蛋。我们可以说一箱鸡蛋的容量是12个。纸箱有容纳12个鸡蛋的空间，并且只有5个正在使用——因此，我们可以再添加7个鸡蛋，而不会溢出纸箱。当我们既有长度又有容量时，我们可以区分当前存在多少东西，也可以区分空间有多少东西。

到目前为止，我们只讨论了std::vector的长度。但std::vector也有容量。在std::vector的上下文中，容量是std:∶vector为多少个元素分配了存储空尽，长度是当前正在使用的元素数。

容量为5的std::vector为5个元素分配了空间。如果包含2个正在使用的元素，则vector的长度（大小）为2。剩余的3个元素为它们分配了内存，但它们不被视为处于活动使用状态。它们可以在以后使用，而不会溢出。

{{< alert success >}}
**关键点**

vector的长度是“正在使用”的元素数。vector的容量是内存中分配了多少个元素的空间。

{{< /alert >}}

***
## 获取std::vector的容量

可以通过capacity()成员函数查看std::vector的容量。

例如：

```C++
#include <iostream>
#include <vector>

void printCapLen(const std::vector<int>& v)
{
	std::cout << "Capacity: " << v.capacity() << " Length:"	<< v.size() << '\n';
}

int main()
{
    std::vector v{ 0, 1, 2 }; // 长度为 3

    printCapLen(v);

    for (auto i : v)
        std::cout << i << ' ';
    std::cout << '\n';

    v.resize(5); // resize 为 5 

    printCapLen(v);

    for (auto i : v)
        std::cout << i << ' ';
    std::cout << '\n';

    return 0;
}
```

在作者的机器上，这将打印以下内容：

```C++
Capacity: 3  Length: 3
0 1 2
Capacity: 5  Length: 5
0 1 2 0 0
```

首先，我们用3个元素初始化vector。这导致vector为3个元素分配存储（容量为3），并且所有3个元素都被认为处于活动使用状态（长度=3）。

然后我们调用resize(5)，这意味着我们现在需要一个长度为5的vector。由于vector只有3个元素的存储空间，但它需要5个，因此vector需要获得更多的存储空间来容纳额外的元素。

在对resize()的调用完成后，我们可以看到vector现在有5个元素的空间（容量为5），并且所有5个元素现在都被认为正在使用（长度为5）。

在大多数情况下，您不需要使用capacity()函数，但我们将在下面的示例中大量使用它，以便可以看到vector的存储发生了什么。

***
## 存储的重新分配，以及它为什么昂贵

当std::vector更改其管理的存储量时，此过程称为重新分配。非正式地，重新分配过程如下所示：

1. vector获取所需数量的元素容量的新内存。这些元素是值初始化的。
2. 将旧内存中的元素复制（或移动，如果可能）到新内存中。然后将旧内存返回给系统。
3. 将std::vector的容量和长度设置为新值。


从外部看，std::vector似乎已调整大小。但在内部，内存（和所有元素）实际上已经被替换！

由于重新分配通常需要复制数组中的每个元素，因此重新分配是一个昂贵的过程。因此，我们希望尽可能避免重新分配。

{{< alert success >}}
**关键点**

重新分配通常很昂贵。避免不必要的重新分配。

{{< /alert >}}

***
## 为什么区分长度和容量？

如果需要，std::vector将重新分配其存储，但一般不希望这样做，因为重新分配存储的计算开销很大。

如果std::vector仅保存其长度，则每个resize()请求都会导致对新长度的昂贵重新分配。区分长度和容量使std::vector能够更聪明地处理何时需要重新分配的问题。

下面的示例对此进行了说明：

```C++
#include <iostream>
#include <vector>

void printCapLen(const std::vector<int>& v)
{
	std::cout << "Capacity: " << v.capacity() << " Length:"	<< v.size() << '\n';
}

int main()
{
    // 初始长度为 5
    std::vector v{ 0, 1, 2, 3, 4 };
    v = { 0, 1, 2, 3, 4 }; // okay, array length = 5
    printCapLen(v);

    for (auto i : v)
        std::cout << i << ' ';
    std::cout << '\n';

    // Resize 为 3 个元素
    v.resize(3);
    printCapLen(v);

    for (auto i : v)
        std::cout << i << ' ';
    std::cout << '\n';

    // 再 Resize 回 5 个元素
    v.resize(5);
    printCapLen(v);

    for (auto i : v)
        std::cout << i << ' ';
    std::cout << '\n';

    return 0;
}
```

这会产生以下结果：

```C++
Capacity: 5  Length: 5
0 1 2 3 4 
Capacity: 5  Length: 3
0 1 2 
Capacity: 5  Length: 5
0 1 2 0 0
```

当我们用5个元素初始化vector时，容量被设置为5，这表示我们的vector最初为5个元素分配了空间。长度也设置为5，表示所有这些元素都在使用中。

在调用v.resize(3) 之后，长度被更改为3，以满足我们对较小数组的请求。然而，请注意容量仍然是5，这意味着vector没有进行重新分配！

最后，v.resize(5)。因为vector已经具有5的容量，所以它不需要重新分配。它只是将长度改回5，并对最后两个元素进行了值初始化。

通过分离长度和容量，在本例中，避免了可能会发生的2次重新分配。在下一课中，我们将看到将元素逐个添加到vector的示例。在这种情况下，不在每次长度更改时重新分配的能力更为重要。

{{< alert success >}}
**关键点**

长度与容量分开的能力允许std::vector在长度更改时避免一些重新分配。

{{< /alert >}}

***
## vector索引基于长度，而不是容量

您可能会惊讶地发现，下标操作符（操作符[]）和at()成员函数的有效索引基于vector的长度，而不是容量。

在上例中，当v具有容量5和长度3时，只有0到2的索引有效。即使vector为3到4之间的元素分配了存储，但它们的索引被认为是越界的。

{{< alert success >}}
**警告**

下标仅在0和vector的长度（而不是其容量）之间有效！

{{< /alert >}}

***
## 收缩std::vector

将vector调整为更大的大小将增加vector的长度，并在需要时增加其容量。然而，将vector大小调整为更小只会减少其长度，而不会减少其容量。

大量减少vector中的元素，而不回收内存是一个糟糕的选择。在我们有一个包含大量不再需要的元素的vector的情况下，内存浪费可能是实质性的。

为了帮助解决这种情况，std::vector有一个名为shrink_to_fit()的成员函数，该函数请求vector收缩其容量以匹配其长度。此请求是非强制的，这意味着具体编译器实现可以自由地忽略它。根据实现认为最好的方式，实现可以决定满足请求，可以部分满足请求（例如，减少容量，但不是全部满足），或者可以完全忽略请求。

下面是一个示例：

```C++
#include <iostream>
#include <vector>

void printCapLen(const std::vector<int>& v)
{
	std::cout << "Capacity: " << v.capacity() << " Length:"	<< v.size() << '\n';
}

int main()
{

	std::vector<int> v(1000); // 分配 1000 个元素
	printCapLen(v);

	v.resize(0); // resize 为 0
	printCapLen(v);

	v.shrink_to_fit();
	printCapLen(v);

	return 0;
}
```

在作者的机器上，这会产生以下结果：

```C++
Capacity: 1000  Length: 1000
Capacity: 1000  Length: 0
Capacity: 0  Length: 0
```

可以看到，当调用v.shrink_to_fit()时，vector将其容量重新分配为0，从而为1000个元素释放内存。

***

{{< prevnext prev="/basic/chapter16/enum-as-index/" next="/basic/chapter16/vec-stack/" >}}
16.8 使用枚举值来作为数组索引
<--->
16.10 std::vector和栈行为
{{< /prevnext >}}
