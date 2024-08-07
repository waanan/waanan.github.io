---
title: "std::vector和列表构造函数简介"
date: 2024-07-08T11:10:28+08:00
---

在上一课中，我们介绍了容器和数组。在本课中，将介绍在本章剩余部分中重点关注的数组类型：std::vector。还将解决上一课介绍的一部分的可扩展性挑战。

***
## std::vector简介

vector是C++标准容器库中实现数组的容器类之一。std::vector在\<vector\>头文件中定义为类模板，其模版参数为其中存放元素的类型。因此，std::vector\<int\>声明了一个std::vector，其元素的类型为int。

实例化std::vector对象很简单：

```C++
#include <vector>

int main()
{
	// 值初始化 (使用默认构造函数)
	std::vector<int> empty{}; // 含有 0 个 int 的vector

	return 0;
}
```

变量empty被定义为一个std::vector，其元素的类型为int。因为我们在这里使用了值初始化，所以我们的vector将以空开始（即，没有元素）。

没有元素的vector现在可能不太有用，但将在以后的课程中再次遇到这种情况。

***
## 使用值列表初始化std::vector

由于容器的目标是管理一组相关的值，因此通常希望用这些值初始化容器。可以使用具有所需的特定初始化值的列表初始化来实现这一点。例如：

```C++
#include <vector>

int main()
{
	// 列表初始化
	std::vector<int> primes{ 2, 3, 5, 7 };          // vector 包含 4 个 int，分别为 2, 3, 5, 7
	std::vector vowels { 'a', 'e', 'i', 'o', 'u' }; // vector 包含 5 个 char， 'a', 'e', 'i', 'o', 'u'.  使用 CTAD (C++17) 来自动推导元素的类型为char.

	return 0;
}
```

对于primes，显式地指定需要一个std::vector，其元素具有int类型。因为提供了4个初始化值，所以primes将包含4个元素，其值为2、3、5和7。

对于vowels，没有显式地指定元素类型。相反，使用C++17的CTAD（类模板参数推导）让编译器从初始值设定项推断元素类型。因为提供了5个初始化值，vowels将包含5个元素，其值为“a”、“e”、“i”、“o”和“u”。

***
## 列表构造函数

让我们更详细地讨论一下上面的工作原理。

在前面聚合初始化中，我们将初始值设定项列表定义为逗号分隔值的大括号列表（例如{1，2，3}）。

容器通常具有一个名为列表构造函数的特殊构造函数，该构造函数允许我们使用初始值设定项列表构造容器的实例。列表构造函数做三件事：

1. 确保容器具有足够的存储空间来保存所有初始化值（如果需要）。
2. 将容器的长度设置为初始值设定项列表中的元素数（如果需要）。
3. 将元素初始化为初始值设定项列表中的值（按顺序）。


因此，当为容器提供初始值设定项列表时，将调用列表构造函数，并使用该值列表构造容器！

{{< alert success >}}
**相关内容**

在后面，会讨论了将列表构造函数添加到自己的程序定义类中——std::initializer_list。

{{< /alert >}}

***
## 使用下标运算符（operator[]）访问数组元素

现在我们已经创建了一个元素数组，如何访问它们？

让我们用一个类比。考虑一组相同的邮箱，并排放置。为了更容易识别邮箱，每个邮箱的前面都漆有一个数字。第一个邮箱有0号，第二个邮箱有1号，等等……所以如果你被告知在0号邮箱中放东西，你就会知道这意味着第一个邮箱。

在C++中，访问数组元素的最常见方法是使用数组的名称和下标运算符（operator[]）。为了选择特定的元素，在下标运算符的方括号内，提供一个整数值，用于标识要选择的元素。该整数值称为下标（非正式地称为索引）。与邮箱非常相似，第一个元素是使用索引0访问的，第二个是使用索引1访问的，等等…

例如，primes[0]将从primes数组返回索引为0的元素（第一个元素）。下标运算符返回对实际元素的引用，而不是副本。一旦访问了数组元素，就可以像普通对象一样使用它（例如，为其赋值、输出它等等…）

因为索引从0开始，而不是1，所以我们说C++中的数组是从零开始的。这可能会令人困惑，因为通常习惯于从1开始计算对象。这也可能导致一些歧义，因为当我们谈论数组元素1时，可能不清楚谈论的是第一个数组元素（索引为0）还是第二个数组元素（索引为1）。

下面是一个示例：

```C++
#include <iostream>
#include <vector>

int main()
{
    std::vector primes { 2, 3, 5, 7, 11 }; // 有五个 5 素数

    std::cout << "The first prime number is: " << primes[0] << '\n';
    std::cout << "The second prime number is: " << primes[1] << '\n';
    std::cout << "The sum of the first 5 primes is: " << primes[0] + primes[1] + primes[2] + primes[3] + primes[4] << '\n';

    return 0;
}
```

这将打印：

```C++
The first prime number is: 2
The second prime number is: 3
The sum of the first 5 primes is: 28
```

通过使用数组，不再需要定义5个不同命名的变量来保存5个质数值。相反，可以定义一个具有5个元素的数组（质数），只需更改索引的值以访问不同的元素！

***
## 下标越界

访问数组时，提供的索引必须选择数组的有效元素。也就是说，对于长度为N的数组，下标必须是介于0和N-1（包含）之间的值。

运算符[]不执行任何类型的边界检查，这意味着它不检查索引是否在0到N-1（包括0和N-1）的边界内。将无效索引传递给运算符[]将以未定义的行为返回。

不要使用负下标是相当容易的。但不太容易记住没有索引为N的元素！数组的最后一个元素索引为N-1，因此使用索引N将导致编译器尝试访问数组末尾后一个的元素。

{{< alert success >}}
**提示**

在具有N个元素的数组中，第一个元素具有索引0，第二个元素索引为1，最后一个元素索引为N-1。没有索引为N的元素！

使用N作为下标将导致未定义的行为（因为这实际上是试图访问N+1个元素，它不是数组的一部分）。

{{< /alert >}}

{{< alert success >}}
**提示**

某些编译器（如Visual Studio）提供了索引有效的运行时断言。在这种情况下，如果在调试模式下访问无效索引，则程序将报错。在发布模式下，则不编译这种assert，因此没有性能损失。

{{< /alert >}}

***
## 数组在内存中是连续的

数组的定义特征之一是元素总是在内存中连续分配，这意味着元素在内存中都是相邻的（它们之间没有间隙）。

作为一个例子：

```C++
#include <iostream>
#include <vector>

int main()
{
    std::vector primes { 2, 3, 5, 7, 11 }; // 有五个 5 素数

    std::cout << "An int is " << sizeof(int) << " bytes\n";
    std::cout << &(primes[0]) << '\n';
    std::cout << &(primes[1]) << '\n';
    std::cout << &(primes[2]) << '\n';

    return 0;
}
```

在作者的机器上，上述程序的一次运行产生了以下结果：

```C++
An int is 4 bytes
00DBF720
00DBF724
00DBF728
```

您将注意到，这些int元素的内存地址间隔为4个字节，与作者机器上的int大小相同。

这意味着数组没有任何针对单个元素的额外开销。它还允许编译器快速计算数组中任何元素的地址。

数组是少数允许随机访问的容器类型之一，这意味着容器中的任何元素都可以直接访问（与顺序访问相反，顺序访问中的元素必须按特定顺序访问）。对数组元素的随机访问通常是有效的，并且使数组非常易于使用。这是数组通常比其他容器更受欢迎的主要原因。

***
## 构造特定长度的std::vector

考虑这样一种情况，我们希望用户输入10个值，这些值将存储在std::vector中。在这种情况下，在将任何值放入std::vector之前，需要一个长度为10的std::vector。如何解决这个问题？

我们可以创建一个std::vector，并使用具有10个占位符值的初始值设定项列表对其进行初始化：

```C++
	std::vector<int> data { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }; // vector 初始包含10个int
```

但由于许多原因，这是不好的。它需要大量的打字。要知道有多少个初始值设定项并不容易。如果决定以后需要不同数量的值，更新并不容易。

幸运的是，std::vector有一个显式构造函数（显式 std::vector\<T\>(int) ），该构造函数采用单个int值来定义要构造的std::vector的长度：

```C++
	std::vector<int> data( 10 ); // vector 含有 10 个 int, 值初始化为 0
```

每个创建的元素都是值初始化的，对于int，它执行零初始化（对于类类型，调用默认构造函数）。

然而，使用这个构造函数有一件不明显的事情：必须使用直接初始化来调用它。

***
## 列表构造函数优先于其他构造函数

要理解为什么必须使用直接初始化调用上一个构造函数，请考虑以下定义：

```C++
	std::vector<int> data{ 10 }; // 这会产生什么行为呢?
```

有两个不同的构造函数与此初始化匹配：

1. {10}可以解释为初始值设定项列表，并与列表构造函数匹配以构造长度为1、值为10的vector。
2. {10}可以解释为单个初始化值，并与std::vector\<T\>(int) 构造函数匹配，以构造长度为10的vector，其中元素值初始化为0。


通常，当类类型定义与多个构造函数匹配时，匹配被认为是不明确的，并导致编译错误。然而，C++对于这种情况有一个特殊的规则：匹配的列表构造函数将被选择，而不是其他匹配的构造函数。如果没有此规则，列表构造函数将导致与采用单个类型参数的任何构造函数的不明确匹配。

由于{10}可以解释为初始值设定项列表，并且std::vector具有列表构造函数，因此在这种情况下，列表构造函数优先。

为了帮助进一步阐明在各种初始化情况下会发生什么，让我们看一下使用复制、直接和列表初始化的类似情况：

```C++
	// Copy init
	std::vector<int> v1 = 10;     // 10 不是初始值列表, 拷贝构造函数也没有能匹配的项: 编译失败

	// Direct init
	std::vector<int> v2(10);      // 10 不是初始值列表, 匹配显式的单参数的构造函数

	// List init
	std::vector<int> v3{ 10 };    // { 10 } 是初始值列表, 匹配列表构造函数

	// Copy list init
	std::vector<int> v4 = { 10 }; // { 10 } 是初始值列表, 匹配列表构造函数
	std::vector<int> v5({ 10 });  // { 10 } 是初始值列表, 匹配列表构造函数
```

在v1的情况下，10的初始化值不是初始值设定项列表，因此列表构造函数不匹配。单参数构造函数显式std::vector\<T\>(int) 也不匹配，因为复制初始化将不匹配显式构造函数。由于没有匹配的构造函数，这是一个编译错误。

在v2的情况下，10的初始化值不是初始值设定项列表，因此列表构造函数不匹配。单参数构造函数显式std::vector\<T\>(int) 匹配，因此选择单参数构造函数。

在v3（列表初始化）的情况下，{10}可以与列表构造函数或显式std::vector\<T\>(int) 匹配。列表构造函数优先于其他匹配构造函数，并被选中。

在v4（复制列表初始化）的情况下，{10}可以与列表构造函数匹配（这是一个非显式构造函数，因此可以与复制初始化一起使用）。已选择列表构造函数。

令人惊讶的是，情况v5是复制列表初始化（不是直接初始化）的替代语法，并且与v4相同。

这是C++初始化的缺点之一：{10}将匹配列表构造函数（如果存在），或者匹配单参数构造函数（如果列表构造函数不存在）。这意味着您获得的行为取决于列表构造函数是否存在！通常可以假设容器具有列表构造函数。

总之，列表初始值设定项通常被设计为允许我们使用元素值列表来初始化容器，并且应该用于该目的。无论如何，这是我们大多数时候想要的。因此，如果10是元素值，则{10}是适当的。如果10是容器的非列表构造函数的参数，请使用直接初始化。

{{< alert success >}}
**关键点**

在构造类类型对象时，匹配列表构造函数被选中，而不是其他匹配构造函数。

{{< /alert >}}

{{< alert success >}}
**最佳实践**

使用不是元素值的初始值设定项构造容器（或具有列表构造函数的任何类型）时，请使用直接初始化。

{{< /alert >}}

{{< alert success >}}
**提示**

当std:：vector是类类型的成员时，不能使用直接初始化：

```C++
#include <vector>

struct Foo
{
    std::vector<int> v1(8); // 编译失败: 直接初始化不能用在类类型的成员初始化上
};
```

为类类型的成员提供默认初始值设定项时：

1. 必须使用复制初始化或列表初始化。
2. 不允许CTAD（因此必须显式指定元素类型）。


答案如下：

```C++
struct Foo
{
    std::vector<int> v{ std::vector<int>(8) }; // ok 
};
```

这将创建一个容量为8的std::vector，然后将其用作v的初始值设定项。

{{< /alert >}}

***
## const和constexpr std::vector

可以将std::vector类型的对象设置为const:

```C++
#include <vector>

int main()
{
    const std::vector<int> prime { 2, 3, 5, 7, 11 }; // prime 和其中的元素不允许被修改

    return 0;
}
```

必须初始化const std::vector，然后不能修改。这样一个vector中的元素被视为常量。

非常量std::vector的元素必须是非常量。因此，不允许出现以下情况：

```C++
#include <vector>

int main()
{
    std::vector<const int> prime { 2, 3, 5, 7, 11 };
}
```

std::vector的最大缺点之一是它不能成为constexpr。如果需要constexpr数组，请使用std::array。

***
## 为什么它被称为vector？

当人们在谈话中使用术语“vector”时，他们通常指的是几何向量，即具有大小和方向的对象。那么，当std::vector不是几何向量时，它是如何获得名称的呢？

Alexander Stepanov在《从数学到泛型编程》（From Mathematics to Generic Programming）一书中写道，“STL中的名称向量取自早期的编程语言Scheme和Common Lisp。不幸的是，这与数学中这个词的更古老的含义不一致……这种数据结构应该被称为数组。遗憾的是，如果你犯了错误并违反了这些原则，结果可能会保留很长时间。”

因此，基本上，std::vector的名称是错误的，但现在更改它太晚了。

***

{{< prevnext prev="/basic/chapter16/intro-container-array/" next="/basic/chapter16/vec-len/" >}}
16.0 容器和数组简介
<--->
16.2 vector与无符号长度和下标问题
{{< /prevnext >}}
