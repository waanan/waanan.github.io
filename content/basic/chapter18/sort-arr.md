---
title: "对数组进行排序"
date: 2024-08-19T20:14:59+08:00
---

## 排序的案例

对数组排序是按特定顺序排列数组中所有元素的过程。在许多不同的情况下，对数组进行排序是有用的。例如，您的电子邮件程序通常按接收时间的顺序显示电子邮件，因为最近的电子邮件通常被认为更应该关注。当您进入联系人列表时，姓名通常按字母顺序排列，因为这样更容易找到您要查找的姓名。这两种例子都涉及在展示之前对数据进行排序。

对数组进行排序可以使搜索数组更有效，不仅对人类，对计算机也是如此。例如，考虑这样一种情况，即我们希望知道名称是否出现在名称列表中。为了查看名称是否在列表中，我们必须检查数组中的每个元素，以查看名称是否出现。对于具有多个元素的数组，搜索所有元素可能会非常昂贵。

然而，现在假设我们的名称数组是按字母顺序排序的。在这种情况下，如果从头遍历到某一个名称，该名称的字母顺序比我们要查找的名称大。此时，如果我们没有找到所需的名称，那么就能知道它不存在于数组的其余部分中，因为后续所有的名称都保证按字母顺序更大！

事实证明，还有更好的算法来搜索排序数组。使用一个简单的算法，我们只需20次比较就可以搜索包含1000000个元素的排序数组！当然，缺点是对数组进行排序相对昂贵，并且通常不值得为了快速搜索而对数组进行分类，除非您要多次搜索它。

在某些情况下，对数组进行排序可能会使搜索变得不必要。考虑另一个例子，我们希望找到最好的分数。如果数组未排序，我们必须遍历数组中的每个元素，以找到最大的分数。如果列表被排序，最好的分数将在第一个或最后一个位置（取决于我们是按升序还是降序排序），因此根本不需要搜索！

***
## 排序的工作原理

排序通常通过重复比较成对的数组元素来执行，并在它们满足某些预定义标准时交换它们。根据使用的排序算法，比较这些元素的顺序不同。同时也取决于列表的排序方式（例如，按升序或降序）。

要交换两个元素，可以使用C++标准库中的std::swap()函数，该函数在utility头文件中定义。

```C++
#include <iostream>
#include <utility>

int main()
{
    int x{ 2 };
    int y{ 4 };
    std::cout << "Before swap: x = " << x << ", y = " << y << '\n';
    std::swap(x, y); // 交换 x 和 y
    std::cout << "After swap:  x = " << x << ", y = " << y << '\n';

    return 0;
}
```

该程序打印:

```C++
Before swap: x = 2, y = 4
After swap:  x = 4, y = 2
```


请注意，在交换之后，x和y的值已经互换！

***
## 选择排序

有许多方法可以对数组进行排序。选择排序可能是最容易理解的排序，这使得它成为教学的好候选，尽管它是较慢的排序之一。

选择排序执行以下步骤，以从最小到最大对数组进行排序:

换句话说，我们将找到数组中最小的元素，并将其交换到第一个位置。然后我们要找到下一个最小的元素，并将其交换到第二个位置。将重复此过程，直到元素用完。

下面是该算法在5个元素上工作的示例。让我们从一个示例数组开始:

{30、50、20、10、40}

首先，我们找到最小的元素，从索引0开始:

{30、50、20、10、40}

然后将其与索引0处的元素交换:

{10、50、20、30、40}

现在第一个元素已经排序，我们可以忽略它。现在，我们找到最小的元素，从索引1开始:

{10、50、20、30、40}

并与索引1中的元素交换:

{10、20、50、30、40}

现在我们可以忽略前两个元素。从索引2开始查找最小元素:

{10、20、50、30、40}

并与索引2中的元素交换:

{10、20、30、50、40}

从索引3开始查找最小元素:

{10、20、30、50、40}

并与索引3中的元素交换:

{10、20、30、40、50}

最后，从索引4开始找到最小的元素:

{10、20、30、40、50}

并将其与索引4中的元素交换（该元素不执行任何操作）:

{10、20、30、40、50}

完成！

{10、20、30、40、50}

请注意，最后一次比较总是与自身进行比较（这是冗余的），因此我们实际上可以在数组最后一个元素之前停止比较。

***
## C++实现的选择排序

下面是该算法在C++中的实现方式:

```C++
#include <iostream>
#include <iterator>
#include <utility>

int main()
{
	int array[]{ 30, 50, 20, 10, 40 };
	constexpr int length{ static_cast<int>(std::size(array)) };

	// 从头遍历
	// 单不处理最后一个位置
	for (int startIndex{ 0 }; startIndex < length - 1; ++startIndex)
	{
		// smallestIndex 是遍历是遇到的最小元素的位置
		// 开头时肯定最小的一个就是起点位置
		int smallestIndex{ startIndex };

		// 然后遍历数组中后续的元素
		for (int currentIndex{ startIndex + 1 }; currentIndex < length; ++currentIndex)
		{
			// 如果发现一个元素比之前的要小
			if (array[currentIndex] < array[smallestIndex])
				// 更换记录的位置
				smallestIndex = currentIndex;
		}

		// smallestIndex 现在保存的就是最小元素的位置
        // 将其与开头的元素进行交换 (意味着将它放到了正确的位置)
		std::swap(array[startIndex], array[smallestIndex]);
	}

	// 现在数组都排序好了，打印验证一下
	for (int index{ 0 }; index < length; ++index)
		std::cout << array[index] << ' ';

	std::cout << '\n';

	return 0;
}
```

该算法最令人困惑的部分是循环（称为嵌套循环）中的循环。外部循环（startIndex）逐个迭代每个元素。对于外部循环的每个迭代，内部循环（currentIndex）用于查找剩余数组中的最小元素（从startIndex+1开始）。smallestIndex跟踪内部循环找到的最小元素的索引。然后smallestIndex与startIndex交换。最后，外部循环（startIndex）前进一个元素，并重复该过程。

提示:如果您在弄清楚上面的程序如何工作时遇到困难，那么在一张纸上完成一个示例案例会很有帮助。将起始（未排序）数组元素水平写在纸的顶部。绘制箭头，指示正在索引的元素startIndex、currentIndex和smallestIndex。手动跟踪程序，并在索引更改时重新绘制箭头。对于外部循环的每个迭代，开始一个新行，显示数组的当前状态。

排序名称使用相同的算法。只需将数组类型从int更改为std::string，并使用适当的值进行初始化。

***
## std::sort

由于排序数组非常常见，C++标准库包含一个名为std::sort的排序函数，该函数位于\<algorithm\>头文件中，并且可以在类似这样的数组上调用:

```C++
#include <algorithm> // for std::sort
#include <iostream>
#include <iterator> // for std::size

int main()
{
	int array[]{ 30, 50, 20, 10, 40 };

	std::sort(std::begin(array), std::end(array));

	for (int i{ 0 }; i < static_cast<int>(std::size(array)); ++i)
		std::cout << array[i] << ' ';

	std::cout << '\n';

	return 0;
}
```

默认情况下，std::sort使用操作符<以升序排序来比较元素对，并在必要时交换它们（与上面的选择排序示例非常相似）。

我们将在以后的一章中讨论更多关于std::sort的内容。

***

{{< prevnext prev="/basic/chapter17/summary/" next="/basic/chapter18/iter/" >}}
17.13 第17章总结
<--->
18.1 迭代器简介
{{< /prevnext >}}
