---
title: "std::vector和栈行为"
date: 2024-07-08T11:10:28+08:00
---

考虑这样的情况，您正在编写一个程序，其中用户将输入一系列值（例如一组测试分数）。在这种情况下，它们将要输入的值的数量在编译时是未知的，并且每次运行程序时都可能变化。您将在std::vector中存储这些值，以供显示和/或处理。

根据我们到目前为止讨论的内容，您可以通过以下几种方式来实现这一点:

首先，您可以询问用户他们有多少个条目，创建一个具有该长度的vector，然后要求用户输入该数量的值。

这是一种不错的方法，但它要求用户提前准确地知道他们有多少条目，并且在计数时没有犯错误。手动计数10个或20个以上的项可能很乏味——当我们应该为它们计算值时，为什么要让用户计算输入的值的数量？

或者，我们可以假设用户不想输入超过一定数量的值（例如30），并创建（或调整）具有如此多元素的vector。然后，可以要求用户输入数据，直到完成（或直到达到30个输入值）。因为vector的长度意味着使用的元素的数量，所以我们可以将vector调整为用户实际输入的值的数量。

这种方法的缺点是用户只能输入30个值，我们不知道这是太多还是太少。如果用户想输入更多的值，那就太糟糕了。

我们可以通过添加一些逻辑来解决这个问题，每当用户达到最大值数量时，就将vector调整得更大。但这意味着我们现在必须将数组大小管理与程序逻辑混合，这将显著增加程序的复杂性（这将不可避免地导致错误）。

这里真正的问题是，我们试图猜测用户可以输入多少元素，因此我们可以适当地管理vector的大小。对于要输入的元素数量确实事先不知道的情况，有一种更好的方法。

但在此之前，我们先讨论下什么是栈。

***
## 什么是栈（stack）？

类比时间！考虑一下自助餐厅中的一堆盘子。由于某种未知的原因，这些盘子非常重，一次只能举起一个。由于盘子是跌在一起，因此只能通过以下两种方法之一操作:

1. 将一个新盘子放在最上面
2. 从最上面取出一个现有的盘子（假如存在的话）

不允许在栈的中间或底部添加或移除盘子，因为这需要一次操作多个盘子。

事物添加到栈和从栈中删除的顺序可以描述为后进先出（LIFO，last-in, first-out ）。添加到栈上的最后一个将是移除的第一个。

***
## 编程中的栈

在编程中，栈是一种容器数据类型，其中元素的插入和删除以后进先出的方式发生。这通常通过名为push和pop的两个操作来实现:

|  操作 |  行为  |  注 |
|  ----  | ----  | ----  |
| Push | 将新元素放入栈顶 |  |
| Pop | 移除栈顶元素 | 可能返回被移除元素，也可能返回void |

许多栈的实现也支持其他有用的操作:

|  操作 |  行为  |  注 |
|  ----  | ----  | ----  |
| Top | 获取栈顶元素 | 并不移除元素 |
| Empty | 查看栈是否是空的 | |
| Size | 获取栈中元素的个数 | |

栈在编程中很常见。在前面，讲到 使用集成调试器中的调用栈中，我们讨论了调用栈，它跟踪已调用的函数。调用栈是--栈！。调用函数时，会将包含该函数信息的条目添加到调用栈的顶部。当函数返回时，包含该函数信息的条目将从调用栈的顶部删除。通过这种方式，调用栈的顶部始终表示当前正在执行的函数，并且每个里面的条目表示以前执行到一半的函数。

例如，下面是一个简短的序列，展示了在栈上Push和Pop的行为:

```C++
       (Stack: empty)
Push 1 (Stack: 1)
Push 2 (Stack: 1 2)
Push 3 (Stack: 1 2 3)
Pop    (Stack: 1 2)
Push 4 (Stack: 1 2 4)
Pop    (Stack: 1 2)
Pop    (Stack: 1)
Pop    (Stack: empty)
```

***
## C++中的栈

在某些语言中，栈被实现为单独的容器。然而，这可能是功能非常有限的。考虑这样的情况，希望在不修改栈的情况下打印栈中的所有值。纯栈接口不提供执行此操作的直接方法。

在C++中，类似栈的操作被添加（作为成员函数）到现有的标准库容器类中，这些容器类支持在一端高效地插入和删除元素（std::vector、std:∶deque和std::list）。这允许除了其原本功能外，还将这些容器中的任何一个用作栈。

在本课的其余部分中，我们将讨论std::vector的栈接口是如何工作的，然后讨论它如何帮助我们解决本课顶部介绍的挑战。

***
## 使用std::vector的栈行为

std::vector中的栈行为通过以下成员函数实现:

| 函数名 |  栈操作  |  行为 |  注 |
|  ----  | ----  | ----  | ----  |
| push_back() | Push | 新元素放到栈顶 | 将新元素放到vector尾巴 |
| pop_back() | Pop | 移除栈顶元素 | 返回void，将vector最后一个元素移除 |
| back() | Top | 获取栈顶元素 | 不移除元素 |
| emplace_back() | Push | 更有效率的push_back | 将新元素放到vector尾巴 |

让我们看一个使用其中一些函数的示例:

```C++
#include <iostream>
#include <vector>

void printStack(const std::vector<int>& stack)
{
	if (stack.empty()) // if stack.size == 0
		std::cout << "Empty";

	for (auto element : stack)
		std::cout << element << ' ';

	// \t 是tab, 帮助对齐
	std::cout << "\tCapacity: " << stack.capacity() << "  Length " << stack.size() << "\n";
}

int main()
{
	std::vector<int> stack{}; // 空 stack

	printStack(stack);

	stack.push_back(1); // push_back() 就一个元素推入栈中
	printStack(stack);

	stack.push_back(2);
	printStack(stack);

	stack.push_back(3);
	printStack(stack);

	std::cout << "Top: " << stack.back() << '\n'; // back() 返回最后一个元素

	stack.pop_back(); // pop_back() 移除栈最后一个元素
	printStack(stack);

	stack.pop_back();
	printStack(stack);

	stack.pop_back();
	printStack(stack);

	return 0;
}
```

在GCC或Clang上，打印:

```C++
Empty   Capacity: 0  Length: 0
1       Capacity: 1  Length: 1
1 2     Capacity: 2  Length: 2
1 2 3   Capacity: 4  Length: 3
Top:3
1 2     Capacity: 4  Length: 2
1       Capacity: 4  Length: 1
Empty   Capacity: 4  Length: 0
```

记住，长度是vector中的元素数，在本例中，它是栈上的元素数。

与下标运算符[]或at()成员函数不同，push_back()（和emplace_back）将增加vector的长度，并在容量不足以插入值时导致重新分配。

在上面的示例中，vector被重新分配了3次（从0到1、从1到2和从2到4的容量）。

***
## push产生的额外容量

在上面的输出中，请注意，当三个重新分配中的最后一个发生时，容量从2跳到4（尽管我们只推了一个元素）。当推送触发重新分配时，std::vector通常会分配一些额外的容量，以允许添加其他元素，而不会在下次添加元素时触发另一个重新分配。

分配的额外容量取决于编译器对std::vector的实现，不同的编译器通常会执行不同的操作:

1. GCC和Clang使当前容量加倍。当触发最后一次调整大小时，容量将从2倍增加到4倍。
2. Visual Studio 2022将当前容量乘以1.5。触发最后一次调整大小时，容量从2更改为3。


因此，根据您使用的编译器，前面的程序可能会有稍微不同的输出。

***
## 调整vector大小不适用于栈行为

重新分配vector的计算开销很大（与vector的长度成比例），因此我们希望在合理的情况下避免重新分配。在上面的示例中，如果我们在程序开始时手动将vector大小调整为容量3，那么是不是可以避免重分配vector3次？

让我们看看如果将上例中的第18行更改为以下内容会发生什么:

```C++
std::vector<int> stack(3); // 初始容量设置为 3
```

现在，当我们再次运行程序时，我们得到以下输出:

```C++
0 0 0   Capacity: 3  Length: 3
0 0 0 1         Capacity: 4  Length: 4
0 0 0 1 2       Capacity: 6  Length: 5
0 0 0 1 2 3     Capacity: 6  Length: 6
Top: 3
0 0 0 1 2       Capacity: 6  Length: 5
0 0 0 1         Capacity: 6  Length: 4
0 0 0   Capacity: 6  Length: 3
```

这是不对的——不知何故，我们在栈的开头有一堆0值！这里的问题是括号初始化（设置vector的初始大小）和resize()函数设置容量和长度。我们的vector从容量3开始（这是我们想要的），但长度也被设置为3。因此，我们的vector从3个值为0的元素开始。我们稍后推送的元素被推送到这些初始元素之上。

当我们打算使用下标来访问元素时，resize()成员函数更改vector的长度是很好的（因为索引需要小于长度才能有效），但当我们将vector用作栈时，它会导致问题。

我们真正想要的是在不改变长度的情况下改变容量（避免将来的重新分配）。

***
## reserve()成员函数更改容量（但不更改长度）

reserve()成员函数可用于重新分配std::vector，而不更改当前长度。

下面是与前面相同的示例，但添加了对reserve（）的调用来设置容量:

```C++
#include <iostream>
#include <vector>

void printStack(const std::vector<int>& stack)
{
	if (stack.empty()) // if stack.size == 0
		std::cout << "Empty";

	for (auto element : stack)
		std::cout << element << ' ';

	// \t 是tab, 帮助对齐
	std::cout << "\tCapacity: " << stack.capacity() << "  Length " << stack.size() << "\n";
}

int main()
{
	std::vector<int> stack{};

	printStack(stack);

	stack.reserve(6); // 预设容量为6，但长度为0
	printStack(stack);

	stack.push_back(1);
	printStack(stack);

	stack.push_back(2);
	printStack(stack);

	stack.push_back(3);
	printStack(stack);

	std::cout << "Top: " << stack.back() << '\n';

	stack.pop_back();
	printStack(stack);

	stack.pop_back();
	printStack(stack);

	stack.pop_back();
	printStack(stack);

	return 0;
}
```

在作者的机器上，此命令打印:

```C++
Empty   Capacity: 0  Length: 0
Empty   Capacity: 6  Length: 0
1       Capacity: 6  Length: 1
1 2     Capacity: 6  Length: 2
1 2 3   Capacity: 6  Length: 3
Top: 3
1 2     Capacity: 6  Length: 2
1       Capacity: 6  Length: 1
Empty   Capacity: 6  Length: 0
```

您可以看到，调用reserve(6)将容量更改为6，但不影响长度。由于std::vector足够大，可以容纳push的所有元素，因此不会发生更多的重新分配。

{{< alert success >}}
**关键点**

resize()成员函数更改vector的长度和容量。reserve()成员函数仅更改容量

{{< /alert >}}

***
## push_back vs emplace_back

push_back()和emplace_back()都将元素推送到栈上。如果要推送的对象已经存在，则push_back()和emplace_back()是等效的，应首选push_back()。

然而，在创建临时对象（与vector的元素类型相同）以将其推送到vector上的情况下，emplace_back()可能更有效:

```C++
#include <iostream>
#include <string>
#include <string_view>
#include <vector>

class Foo
{
private:
    std::string m_a{};
    int m_b{};

public:
    Foo(std::string_view a, int b)
        : m_a { a }, m_b { b }
        {}

    explicit Foo(int b)
        : m_a {}, m_b { b }
        {};
};

int main()
{
	std::vector<Foo> stack{};

	// 已经有一个对象是, push_back 和 emplace_back 类似等效
	Foo f{ "a", 2 };
	stack.push_back(f);    // 优先使用这个
	stack.emplace_back(f);

	// 当需要push一个临时对象, emplace_back 更高效
	stack.push_back({ "a", 2 }); // 创建临时对象, 然后拷贝到vector中
	stack.emplace_back("a", 2);  // 传递参数，让对象直接在vector中创建（省略了对象拷贝）

	// push_back 不能使用显示构造函数, emplace_back 可以
	stack.push_back({ 2 }); // 编译失败: Foo(int) is explicit
	stack.emplace_back(2);  // ok
    
	return 0;
}
```

在上面的例子中，我们有一个Foo对象的vector。使用push_back({“a”，2})，我们创建并初始化一个临时Foo对象，然后将其复制到vector中。对于成本高昂的复制类型（如std::string），此复制可能会导致性能降低。

使用emplace_back()，我们不需要创建要传递的临时对象。相反，我们传递将用于创建临时对象的参数，并将它们转发（使用称为完美转发的功能）到vector，在vector中，它们用于创建和初始化vector内的对象。这避免了本应制作的副本。

需要注意的是，push_back()不会使用显式构造函数，而emplace_back()会。这使得emplace_back更加危险，因为很容易意外地调用显式构造函数来执行一些没有意义的转换。

在C++20之前，emplace_back()不适用于聚合初始化。

{{< alert success >}}
**最佳实践**

在创建要添加到容器的新临时对象时，或者在需要访问显式构造函数时，首选emplace_back()。

否则，首选push_back()。

{{< /alert >}}

***
## 使用栈操作解决我们的挑战

现在应该很明显，我们应该如何应对在课程顶部介绍的挑战。如果我们事先不知道将有多少元素添加到std::vector中，则使用栈函数插入这些元素是一种方法。

下面是一个示例:

```C++
#include <iostream>
#include <limits>
#include <vector>

int main()
{
	std::vector<int> scoreList{};

	while (true)
	{
		std::cout << "Enter a score (or -1 to finish): ";
		int x{};
		std::cin >> x;

		if (!std::cin) // 处理异常输入
		{
			std::cin.clear();
			std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
			continue;
		}

		// 如果完成，跳出循环
		if (x == -1)
			break;

		// 输入有效值, 将其放入vector中
		scoreList.push_back(x);
	}

	std::cout << "Your list of scores: \n";

	for (const auto& score : scoreList)
		std::cout << score << ' ';

	return 0;
}
```

该程序允许用户输入测试分数，将每个分数添加到vector。用户完成输入后，将打印vector中的所有值。

请注意，在这个程序中，我们根本不需要进行任何计数、索引或处理数组长度！可以只关注我们希望程序做什么的逻辑，并让vector处理所有的存储问题！

***
