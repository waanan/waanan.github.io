---
title: "std::move"
date: 2024-08-23T14:54:42+08:00
---

一旦您开始更经常地使用移动语义，您将开始发现希望调用移动语义，但必须处理的对象是左值，而不是右值的情况。以下面的交换函数为例：

```C++
#include <iostream>
#include <string>

template <typename T>
void mySwapCopy(T& a, T& b) 
{ 
	T tmp { a }; // 调用拷贝构造
	a = b; // 调用拷贝赋值
	b = tmp; // 调用拷贝赋值
}

int main()
{
	std::string x{ "abc" };
	std::string y{ "de" };

	std::cout << "x: " << x << '\n';
	std::cout << "y: " << y << '\n';

	mySwapCopy(x, y);

	std::cout << "x: " << x << '\n';
	std::cout << "y: " << y << '\n';

	return 0;
}
```

传入两个T类型的对象（在本例中为std::string），该函数通过制作三个副本来交换它们的值。因此，该程序打印：

```C++
x: abc
y: de
x: de
y: abc
```

正如我们上一课所示，复制可能效率低下。这个版本的交换制作3个副本。这导致了过度大量的字符串创建和销毁，这是缓慢的。

然而，这里不需要复制。我们真正想做的就是交换a和b的值，这也可以用3个移动来完成！因此，如果我们从复制语义切换到移动语义，可以使代码更具性能。

但如何做呢？这里的问题是参数a和b是左值引用，而不是右值引用，因此没有办法调用移动构造函数和移动赋值运算符。默认情况下，获得拷贝构造函数和拷贝赋值行为。该怎么办？

***
## std::move

在C++11中，std::move是一个标准库函数，它将其参数强制转换（使用static_cast）为右值引用，以便可以调用移动语义。因此，可以使用std::move将左值强制转换为更喜欢移动而不是复制的类型。std::move在utility头文件中定义。

下面是与上面相同的程序，但使用mySwapMove()函数，该函数使用std::move将左值转换为右值，以便我们可以调用移动语义：

```C++
#include <iostream>
#include <string>
#include <utility> // for std::move

template <typename T>
void mySwapMove(T& a, T& b) 
{ 
	T tmp { std::move(a) }; // 调用移动构造
	a = std::move(b); // 调用移动赋值
	b = std::move(tmp); // 调用移动赋值
}

int main()
{
	std::string x{ "abc" };
	std::string y{ "de" };

	std::cout << "x: " << x << '\n';
	std::cout << "y: " << y << '\n';

	mySwapMove(x, y);

	std::cout << "x: " << x << '\n';
	std::cout << "y: " << y << '\n';

	return 0;
}
```

这将打印与上面相同的结果：

```C++
x: abc
y: de
x: de
y: abc
```

在初始化tmp时，我们使用std::move将左值变量x转换为右值，而不是复制x。由于是右值，因此调用了移动语义，并将x移动到tmp中。

通过几个更多的交换，变量x的值被移到了y，而y的值被移动到了x。

***
## 另一个例子

当使用左值填充容器的元素（如std::vector）时，我们也可以使用std:∶move。

在下面的程序中，首先使用复制语义将元素添加到vector。然后，使用移动语义向vector添加元素。

```C++
#include <iostream>
#include <string>
#include <utility> // for std::move
#include <vector>

int main()
{
	std::vector<std::string> v;

	// 使用 std::string 因为它是可移动的 (std::string_view 不是)
	std::string str { "Knock" };

	std::cout << "Copying str\n";
	v.push_back(str); // 调用左值版本的 push_back, 拷贝 str到容器
	
	std::cout << "str: " << str << '\n';
	std::cout << "vector: " << v[0] << '\n';

	std::cout << "\nMoving str\n";

	v.push_back(std::move(str)); // 调用右值版本 push_back, 移动 str 到容器
	
	std::cout << "str: " << str << '\n'; // 这一行结果不确定，因为str的内容被move走了
	std::cout << "vector:" << v[0] << ' ' << v[1] << '\n';

	return 0;
}
```

在作者的机器上，该程序打印：

```C++
Copying str
str: Knock
vector: Knock

Moving str
str:
vector: Knock Knock
```

在第一种情况下，我们向push_back（）传递了一个左值，因此它使用复制语义向vector添加元素。由于这个原因，str中的值被保留。

在第二种情况下，我们向push_back（）传递了一个右值（实际上是通过std::move转换的左值），因此它使用移动语义将元素添加到vector。这更有效，因为可以窃取字符串的值，而不必复制它。

***
## 被移动的对象将处于有效但可能不确定的状态

当我们从临时对象中移动值时，被移动的对象剩余值并不重要，因为临时对象将立即被销毁。但我们在使用了std::move（）的左值对象呢？因为我们可以在移动这些对象的值后继续访问它们（例如，在上面的示例中，我们在移动str的值后打印它），所以访问它们剩余的值是有可能的。

这里有两个学派。一个学派认为，被移动的对象应该重置回某种默认/零状态，其中对象不再拥有资源。我们在上面看到了一个例子，其中str已被清除为空字符串。

另一个学派认为，我们应该做任何最方便的事情，如果不方便的话，不要把自己限制在必须清除被移动的物体上。

那么标准库在这种情况下做什么呢？关于这一点，C++标准说，“除非另有规定，否则对象（C++标准库中定义的类型）被移动后应处于有效但未指定的状态。”

在上面的示例中，当作者在调用std::move之后打印str的值时，它打印了一个空字符串。然而，这不是必需的，它可以打印任何有效的字符串，包括空字符串、原始字符串或任何其他有效字符串。因此，我们应该避免使用被移动对象的值，因为结果将特定于实现。

在某些情况下，我们希望重用其值已被移动的对象（而不是分配新对象）。例如，在上面的mySwapMove（）的实现中，我们首先将资源移出，然后将另一个资源移入。这很好，因为在移出资源的时间和给定新确定值的时间之间，我们从不使用a的值。

对于被移动对象，可以安全地调用不依赖于对象的当前值的任何函数。这意味着我们可以设置或重置被移动对象的值（使用 operator= 或任何类型的clear（）或reset（）成员函数）。我们还可以测试被移动对象的状态（例如，使用empty（）来查看对象是否有值）。然而，我们应该避免使用 operator[] 或front（）之类的函数（它返回容器中的第一个元素），因为这些函数依赖于具有元素的容器。

{{< alert success >}}
**关键点**

std::move（）向编译器提供一个提示，即程序员不再需要对象的值。对象被移动后，仍可对其重新赋值。但在被重新赋值之前，不要使用该对象。

{{< /alert >}}

***
## std::move还有何用处？

在对元素数组进行排序时，std::move也很有用。许多排序算法（如选择排序和冒泡排序）通过交换元素对来工作。在前面的课程中，我们不得不求助于复制语义来进行交换。现在我们可以使用移动语义，这更有效率。

如果我们想将由一个智能指针管理的内容移动到另一个指针指针，它也很有用。

{{< alert success >}}
**相关内容**

std::move（）的一个有用的变体称为std::move_if_noexcept（），如果对象具有noexcept 移动构造函数，则返回可移动的右值，否则返回可复制的左值。后面章节进行介绍。

{{< /alert >}}

***
## 结论

每当我们希望将左值视为右值时，可以使用std::move，以调用移动语义而不是复制语义。

***