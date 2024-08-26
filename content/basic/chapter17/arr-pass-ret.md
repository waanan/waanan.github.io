---
title: "std::array作为函数参数或返回值"
date: 2024-08-13T13:06:02+08:00
---

类型为std::array的对象可以像任何其他对象一样传递给函数。这意味着，如果按值传递std::array，将生成一个昂贵的副本。因此，通常通过（const）引用传递std::array，以避免这种复制。

对于std::array，元素类型和数组长度都是对象类型信息的一部分。因此，当我们使用std::array作为函数参数时，必须显式指定元素类型和数组长度:

```C++
#include <array>
#include <iostream>

void passByRef(const std::array<int, 5>& arr) // 必须指定 <int, 5> 
{
    std::cout << arr[0] << '\n';
}

int main()
{
    std::array arr{ 9, 7, 5, 3, 1 }; // CTAD 推导类型为 std::array<int, 5>
    passByRef(arr);

    return 0;
}
```

CTAD（目前）不能与函数参数一起工作，因此不能在这里仅指定std::array，并让编译器推断函数参数类型。

***
## 使用函数模板传递不同元素类型或长度的std::array

要编写可以接受任何元素类型或任何长度的std::array的函数，我们可以创建一个函数模板，该模板同时参数化std::array的元素类型和长度，然后C++将使用该函数模板以实际类型和长度实例化实际函数。

由于std::array的定义如下:

```C++
template<typename T, std::size_t N> // N 是非类型模版参数
struct array;
```

可以创建使用相同模板参数声明的函数模板:

```C++
#include <array>
#include <iostream>

template <typename T, std::size_t N> // 注意这里模版参数声明与 std::array 一致
void passByRef(const std::array<T, N>& arr)
{
    static_assert(N != 0); // 如果 std::array 为空，则编译失败

    std::cout << arr[0] << '\n';
}

int main()
{
    std::array arr{ 9, 7, 5, 3, 1 }; // 使用 CTAD 推导类型为 std::array<int, 5>
    passByRef(arr);  // ok: 编译器会实例化 passByRef(const std::array<int, 5>& arr)

    std::array arr2{ 1, 2, 3, 4, 5, 6 }; // 使用 CTAD 推导类型为 std::array<int, 6>
    passByRef(arr2); // ok: 编译器会实例化 passByRef(const std::array<int, 6>& arr)

    std::array arr3{ 1.2, 3.4, 5.6, 7.8, 9.9 }; // 使用 CTAD 推导类型为 std::array<double, 5>
    passByRef(arr3); // ok: 编译器会实例化 passByRef(const std::array<double, 5>& arr)

    return 0;
}
```

在上面的示例中，创建了一个名为passByRef()的函数模板，该模板具有类型为std::array\<T，N\>的参数。T和N在上一行的模板参数声明中定义:template\<typename T，std::size_t N\>。T是一个标准的类型模板参数，允许调用方指定元素类型。N是类型为std::size_t的非类型模板参数，允许调用方指定数组长度。

因此，当从main()调用passByRef(arr)时（其中arr被定义为std::array\<int，5\>），编译器将实例化并调用void passByRef(const std::array\<int，5\>&arr)。arr2和arr3也会发生类似的过程。

我们创建了一个单独的函数模板，可以实例化函数来处理任何元素类型和长度的std::array参数！

如果需要，也可以仅模板化两个模板参数中的一个。在下面的示例中，仅参数化std::array的长度，但元素类型显式定义为int:

```C++
#include <array>
#include <iostream>

template <std::size_t N> // 注：这里只模板化了长度
void passByRef(const std::array<int, N>& arr) // 元素类型显式定义为int
{
    static_assert(N != 0); // 如果 std::array 为空，则编译失败

    std::cout << arr[0] << '\n';
}

int main()
{
    std::array arr{ 9, 7, 5, 3, 1 }; // 使用 CTAD 推导类型为 std::array<int, 5>
    passByRef(arr);  // ok: 编译器会实例化 passByRef(const std::array<int, 5>& arr)

    std::array arr2{ 1, 2, 3, 4, 5, 6 }; // 使用 CTAD 推导类型为 std::array<int, 6>
    passByRef(arr2); // ok: 编译器会实例化 passByRef(const std::array<int, 6>& arr)

    std::array arr3{ 1.2, 3.4, 5.6, 7.8, 9.9 }; // 使用 CTAD 推导类型为 std::array<double, 5>
    passByRef(arr3); // error: 编译器无法找到匹配的函数

    return 0;
}
```

{{< alert success >}}
**警告**

请注意，std::array的非类型模板参数的类型应该是std::size_t，而不是int！这是因为std::array被定义为template\<class T，std::size_t N\> struct array；。如果使用int作为非类型模板参数的类型，编译器将无法将类型为std::array\<T，std::size_T\>的参数与类型为std::arrary\<T，int\>的参数匹配（并且模板不会进行转换）。

{{< /alert >}}

***
## auto非类型模板参数（C++20）

必须记住（或查找）非类型模板参数的类型，以便可以在自己的函数模板的模板参数声明中使用它，这是一件痛苦的事情。

在C++20中，可以在模板参数声明中使用auto，让非类型模板参数从参数推断其类型:

```C++
#include <array>
#include <iostream>

template <typename T, auto N> // 使用 auto 去自动推导 N 的类型
void passByRef(const std::array<T, N>& arr)
{
    static_assert(N != 0); // 如果 std::array 为空，则编译失败

    std::cout << arr[0] << '\n';
}

int main()
{
    std::array arr{ 9, 7, 5, 3, 1 }; // 使用 CTAD 推导类型为 std::array<int, 5>
    passByRef(arr);  // ok: 编译器会实例化 passByRef(const std::array<int, 5>& arr)

    std::array arr2{ 1, 2, 3, 4, 5, 6 }; // 使用 CTAD 推导类型为 std::array<int, 6>
    passByRef(arr2); // ok: 编译器会实例化 passByRef(const std::array<int, 6>& arr)

    std::array arr3{ 1.2, 3.4, 5.6, 7.8, 9.9 }; // 使用 CTAD 推导类型为 std::array<double, 5>
    passByRef(arr3); // ok: 编译器会实例化 passByRef(const std::array<double, 5>& arr)

    return 0;
}
```

如果编译器支持C++20，则可以使用。

***
## 数组长度的静态断言

考虑以下模板函数，该函数类似于上面给出的函数:

```C++
#include <array>
#include <iostream>

template <typename T, std::size_t N>
void printElement3(const std::array<T, N>& arr)
{
    std::cout << arr[3] << '\n';
}

int main()
{
    std::array arr{ 9, 7, 5, 3, 1 };
    printElement3(arr);

    return 0;
}
```

虽然printElement3()在这种情况下工作良好，但在该程序中有一个潜在的错误等待粗心的程序员。看到了吗？

上面的程序打印索引为3的数组元素的值。只要数组具有索引为3的有效元素，这是可以的。然而，编译器允许让您传入索引3超出界限的数组。例如:

```C++
#include <array>
#include <iostream>

template <typename T, std::size_t N>
void printElement3(const std::array<T, N>& arr)
{
    std::cout << arr[3] << '\n'; // 无效索引
}

int main()
{
    std::array arr{ 9, 7 }; // 只有两个元素的 array (有效索引值为 0 和 1)
    printElement3(arr);

    return 0;
}
```

这会导致未定义的行为。理想情况下，当我们尝试这样做时，我们希望编译器警告我们！

模板参数比函数参数具有的一个优点是模板参数是编译时常量。这意味着我们可以利用常量表达式的能力。

因此，一种解决方案是使用std::get()（执行编译时边界检查），而不是操作符[]（不执行边界检查）:

```C++
#include <array>
#include <iostream>

template <typename T, std::size_t N>
void printElement3(const std::array<T, N>& arr)
{
    std::cout << std::get<3>(arr) << '\n'; // 编译时检查索引 3 是否有效
}

int main()
{
    std::array arr{ 9, 7, 5, 3, 1 };
    printElement3(arr); // okay

    std::array arr2{ 9, 7 };
    printElement3(arr2); // 编译失败

    return 0;
}
```

当编译器看到对printElement3(arr2)的调用时，它将实例化函数printElement3(const std::array\<int，2\>&)。在该函数体中看到std::get\<3\>(arr)。由于数组的长度为2，因此这是无效的访问，编译器将发出错误。

另一种解决方案是使用static_assert验证数组长度:

```C++
#include <array>
#include <iostream>

template <typename T, std::size_t N>
void printElement3(const std::array<T, N>& arr)
{
    // 前置检查: 数组长度一定要比3大
    static_assert (N > 3);

    // 这里可以确定，数组的长度一定为4或以上

    std::cout << arr[3] << '\n';
}

int main()
{
    std::array arr{ 9, 7, 5, 3, 1 };
    printElement3(arr); // okay

    std::array arr2{ 9, 7 };
    printElement3(arr2); // 便是以失败

    return 0;
}
```

当编译器看到对printElement3(arr2)的调用时，它将实例化函数printElement3(const std::array\<int，2\>&)。该函数体内部的 static_assert(N > 3)。由于非类型模板参数N的值为2，并且2>3为false，因此编译器将发出错误。

{{< alert success >}}
**关键点**

在上面的例子中，您可能想知道为什么我们使用static_assert(N > 3)；而不是static_assert(std::size(arr) > 3)。由于上一课中提到的语言缺陷，后者不能在C++23之前编译。

{{< /alert >}}

***
## 返回std::array

抛开语法不谈，将std::array传递给函数在概念上很简单——通过（const）引用传递它。但如果有一个需要返回std::array的函数，该怎么办？事情有点复杂。与std::vector不同，std::array不支持移动，因此按值返回std::array将制作array的副本。如果array中的元素支持移动，则将移动它们，否则将复制它们。

这里有两个常规选项，您应该根据情况选择。

***
## 按值返回std::array

当以下所有条件都为true时，可以按值返回std:array:

1. 数组不是很大。
2. 元素类型的复制（或移动）成本很低。
3. 代码未在性能敏感的上下文中使用。


在这种情况下，将制作std::array的副本，但如果以上所有都为真，性能损失将很小，坚持使用最传统的方法将数据返回给调用者可能是最佳选择。

```C++
#include <array>
#include <iostream>
#include <limits>

// 按值返回
template <typename T, std::size_t N>
std::array<T, N> inputArray()
{
	std::array<T, N> arr{};
	std::size_t index { 0 };
	while (index < N)
	{
		std::cout << "Enter value #" << index << ": ";
		std::cin >> arr[index];

		if (!std::cin) // 处理异常输入
		{
			std::cin.clear();
			std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
			continue;
		}
		++index;
	}

	return arr;
}

int main()
{
	std::array<int, 5> arr { inputArray<int, 5>() };

	std::cout << "The value of element 2 is " << arr[2] << '\n';

	return 0;
}
```

这种方法有几个优点:

1. 它使用最传统的方式将数据返回给调用者。
2. 很明显，函数正在返回一个值。

还有一些缺点:

1. 该函数返回数组及其所有元素的副本，这非常没有效率。
2. 当调用函数时，必须显式地提供模板参数，因为没有参数来推导它们。

***
## 通过出参返回std::array

在按值返回太昂贵的情况下，可以改用出参。在这种情况下，调用方负责通过非常量引用（或地址）传入std::array，然后函数可以修改该数组。

```C++
#include <array>
#include <limits>
#include <iostream>

template <typename T, std::size_t N>
void inputArray(std::array<T, N>& arr) // non-const 引用作为参数
{
	std::size_t index { 0 };
	while (index < N)
	{
		std::cout << "Enter value #" << index << ": ";
		std::cin >> arr[index];

		if (!std::cin) // 处理异常输入
		{
			std::cin.clear();
			std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
			continue;
		}
		++index;
	}

}

int main()
{
	std::array<int, 5> arr {};
	inputArray(arr);

	std::cout << "The value of element 2 is " << arr[2] << '\n';

	return 0;
}
```

这种方法的主要优点是从未制作array的副本，因此这是有效的。

还有一些缺点:

1. 这种返回数据的方法是非常规的，并且不容易看出函数正在修改参数。
2. 只能使用此方法将值分配给数组，而不是初始化一个新的。
3. 这样的函数不能用于生成临时对象。

***
## 或者考虑返回std::vector

vector支持移动，并且可以按值返回，而无需制作昂贵的副本。如果按值返回std::array，则您的std::array可能不是constexpr，您应该考虑改用（并返回）std::vector。

***

{{< prevnext prev="/basic/chapter17/arr-len-index/" next="/basic/chapter17/arr-of-class/" >}}
17.1 std::array长度和索引
<--->
17.3 std::array与类类型元素
{{< /prevnext >}}
