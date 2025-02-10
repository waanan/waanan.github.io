---
title: "部分模板特化"
date: 2025-01-22T20:47:14+08:00
---

对于那些希望更深入了解C++模板的人来说，这一课和下一课可选阅读。部分模板特化并不经常使用（但在特定情况下可能有用）。

让我们再看一看我们在前面的一个示例中使用的Static Array类：

```C++
template <typename T, int size> // size 是一个非类型参数
class StaticArray
{
private:
    // size 控制数组的大小
    T m_array[size]{};
 
public:
    T* getArray() { return m_array; }
	
    const T& operator[](int index) const { return m_array[index]; }
    T& operator[](int index) { return m_array[index]; }
};
```

此模版类接受两个模板参数：一个类型参数和一个非类型参数。

现在，假设我们想编写一个函数来打印整个数组。尽管我们可以将其实现为成员函数，但这里将作为非成员函数来实现，因为它将使后续的示例更容易理解。

使用模板，我们可以这样编写：

```C++
template <typename T, int size>
void print(const StaticArray<T, size>& array)
{
    for (int count{ 0 }; count < size; ++count)
        std::cout << array[count] << ' ';
}
```

这将允许我们执行以下操作：

```C++
#include <iostream>

template <typename T, int size> // size 是一个非类型参数
class StaticArray
{
private:
	T m_array[size]{};

public:
	T* getArray() { return m_array; }

	const T& operator[](int index) const { return m_array[index]; }
	T& operator[](int index) { return m_array[index]; }
};

template <typename T, int size>
void print(const StaticArray<T, size>& array)
{
	for (int count{ 0 }; count < size; ++count)
		std::cout << array[count] << ' ';
}

int main()
{
	// 定义 int 数组
	StaticArray<int, 4> int4{};
	int4[0] = 0;
	int4[1] = 1;
	int4[2] = 2;
	int4[3] = 3;

	// 打印
	print(int4);

	return 0;
}
```

并得到以下结果：

```C++
0 1 2 3
```

尽管这是可行的，但它有一个设计缺陷。考虑以下内容：

```C++
#include <algorithm>
#include <iostream>
#include <string_view>

int main()
{
    // 定义 char 数组
    StaticArray<char, 14> char14{};

    // 拷贝一些数据到数组里
    constexpr std::string_view hello{ "Hello, world!" };
    std::copy_n(hello.begin(), hello.size(), char14.getArray());

    // 打印
    print(char14);

    return 0;
}
```

该程序可以通过编译、执行并产生以下值（或类似值）：

```C++
H e l l o ,   w o r l d !
```

对于非char类型，在每个数组元素之间放一个空格是有意义的，这样它们就不会一起展示。然而，对于char类型，将所有内容一起打印为C样式的字符串更有意义，而我们的print()函数不这样做。

那么我们如何解决这个问题呢？

***
## 模板部分特化？

可以首先考虑使用模板特化。完全模板特化的问题是必须显式定义所有模板参数。

考虑：

```C++
#include <algorithm>
#include <iostream>
#include <string_view>

template <typename T, int size> // size 是一个非类型参数
class StaticArray
{
private:
	// size 控制数组的大小
	T m_array[size]{};

public:
	T* getArray() { return m_array; }

	const T& operator[](int index) const { return m_array[index]; }
	T& operator[](int index) { return m_array[index]; }
};

template <typename T, int size>
void print(const StaticArray<T, size>& array)
{
	for (int count{ 0 }; count < size; ++count)
		std::cout << array[count] << ' ';
}

// 重写 print()，针对完全特化 StaticArray<char, 14>
template <>
void print(const StaticArray<char, 14>& array)
{
	for (int count{ 0 }; count < 14; ++count)
		std::cout << array[count];
}

int main()
{
    // 定义 char 数组
    StaticArray<char, 14> char14{};

    // 拷贝一些数据到数组里
    constexpr std::string_view hello{ "Hello, world!" };
    std::copy_n(hello.begin(), hello.size(), char14.getArray());

    // 打印
    print(char14);

    return 0;
}
```

如您所见，我们现在为完全特化的StaticArray\<char, 14\>提供了重载打印函数。事实上，它打印了：

```C++
Hello, world!
```

尽管这解决了StaticArray\<char, 14\>调用print()的问题，但它带来了另一个问题：使用完全模板特化意味着我们必须显式定义该函数将接受的数组的长度！考虑以下示例：

```C++
int main()
{
    //  定义 char 数组
    StaticArray<char, 12> char12{};

    // 拷贝一些数据到数组里
    constexpr std::string_view hello{ "Hello, mom!" };
    std::copy_n(hello.begin(), hello.size(), char12.getArray());

    // 打印
    print(char12);

    return 0;
}
```

使用char12调用print()将调用采用StaticArray\<T, size\>的print()版本，因为char12的类型为StaticArray\<char, 12\>。

尽管我们可以制作一个处理StaticArray\<char, 12\>的print()的副本，但当我们想调用数组大小为5或22的print()时会发生什么？我们必须为每个不同的数组大小复制函数。那是多余的。

显然，完全模板特化在这里是一种限制性太强的解决方案。我们正在寻找的解决方案是部分模板特化。

***
## 部分模板特化

部分模板特化允许我们特化类（但不是单个函数！），其中一些模板参数（但不是所有）被显式定义。对于上面的挑战，理想的解决方案是让重载的print函数与char类型的StaticArray一起工作，但保留长度表达式参数的模板化，以便它可以根据需要变化。部分模板特化允许我们这样做！

下面是一个重载print函数的示例，该函数采用部分特化的StaticArray：

```C++
// 重载 print() 函数，部分特化 StaticArray<char, size>
template <int size> // size 仍然是非类型模版参数
void print(const StaticArray<char, size>& array) // 这里显示指定第一个参数是char
{
	for (int count{ 0 }; count < size; ++count)
		std::cout << array[count];
}
```

正如您在这里看到的，我们已经明确声明，该函数仅适用于char类型的StaticArray，但size仍然是模板化的表达式参数，因此它适用于任何大小的char数组！

下面是一个使用此的完整程序：

```C++
#include <algorithm>
#include <iostream>
#include <string_view>

template <typename T, int size> // size 是一个非类型参数
class StaticArray
{
private:
	// size 控制数组的大小
	T m_array[size]{};

public:
	T* getArray() { return m_array; }

	const T& operator[](int index) const { return m_array[index]; }
	T& operator[](int index) { return m_array[index]; }
};

template <typename T, int size>
void print(const StaticArray<T, size>& array)
{
	for (int count{ 0 }; count < size; ++count)
		std::cout << array[count] << ' ';
}

// 重载 print() 函数，部分特化 StaticArray<char, size>
template <int size>
void print(const StaticArray<char, size>& array)
{
	for (int count{ 0 }; count < size; ++count)
		std::cout << array[count];
}

int main()
{
	// 定义长度为 14 的 char 数组
	StaticArray<char, 14> char14{};

	// 拷贝一些数据到数组里
	constexpr std::string_view hello14{ "Hello, world!" };
	std::copy_n(hello14.begin(), hello14.size(), char14.getArray());

	// 打印
	print(char14);

	std::cout << ' ';

	// 定义长度为 12 的 char 数组
	StaticArray<char, 12> char12{};

	// 拷贝一些数据到数组里
	constexpr std::string_view hello12{ "Hello, mom!" };
	std::copy_n(hello12.begin(), hello12.size(), char12.getArray());

	// 打印
	print(char12);

	return 0;
}
```

这将打印：

```C++
Hello, world! Hello, mom!
```

正如我们所料。

部分模板特化只能与类一起使用，而不能与模板函数一起使用（函数必须完全特化）。我们的void print(StaticArray\<char, size\>\& array)示例可以工作，因为print函数不是部分特化的（它只是一个重载的模板函数，碰巧有一个部分特化的类参数）。

***
## 成员函数的部分模板特化

在处理成员函数时，对函数的部分特化的限制可能会导致一些挑战。例如，如果我们这样定义了StaticArray，会怎么样？

```C++
template <typename T, int size>
class StaticArray
{
private:
    T m_array[size]{};
 
public:
    T* getArray() { return m_array; }
	
    const T& operator[](int index) const { return m_array[index]; }
    T& operator[](int index) { return m_array[index]; }

    void print() const;
};

template <typename T, int size> 
void StaticArray<T, size>::print() const
{
    for (int i{ 0 }; i < size; ++i)
        std::cout << m_array[i] << ' ';
    std::cout << '\n';
}
```

print()现在是类StaticArray\<T, int\>的成员函数。那么，当我们希望部分特化print()时，会发生什么情况，以便它以不同的方式工作？您可以尝试以下操作：

```C++
// 无法编译, 不能部分特化函数
template <int size>
void StaticArray<double, size>::print() const
{
	for (int i{ 0 }; i < size; ++i)
		std::cout << std::scientific << m_array[i] << ' ';
	std::cout << '\n';
}
```

不幸的是，这不起作用，因为我们正在尝试部分特化函数，这是不允许的。

那么我们该怎么解决这个问题呢？一种明显的方法是部分特化整个类：

```C++
#include <iostream>

template <typename T, int size>
class StaticArray
{
private:
	T m_array[size]{};

public:
	T* getArray() { return m_array; }

	const T& operator[](int index) const { return m_array[index]; }
	T& operator[](int index) { return m_array[index]; }

	void print() const;
};

template <typename T, int size> 
void StaticArray<T, size>::print() const
{
	for (int i{ 0 }; i < size; ++i)
		std::cout << m_array[i] << ' ';
	std::cout << '\n';
}

// 部分特化类
template <int size>
class StaticArray<double, size>
{
private:
	double m_array[size]{};

public:
	double* getArray() { return m_array; }

	const double& operator[](int index) const { return m_array[index]; }
	double& operator[](int index) { return m_array[index]; }

	void print() const;
};

// 部分特化类的成员函数
template <int size>
void StaticArray<double, size>::print() const
{
	for (int i{ 0 }; i < size; ++i)
		std::cout << std::scientific << m_array[i] << ' ';
	std::cout << '\n';
}

int main()
{
	// 定义有 6 个int的数组
	StaticArray<int, 6> intArray{};

	// Fill it up in order, then print it
	for (int count{ 0 }; count < 6; ++count)
		intArray[count] = count;

	intArray.print();

	// 定义有 4 个double的数组
	StaticArray<double, 4> doubleArray{};

	for (int count{ 0 }; count < 4; ++count)
		doubleArray[count] = (4.0 + 0.1 * count);

	doubleArray.print();

	return 0;
}
```

这将打印：

```C++
0 1 2 3 4 5
4.000000e+00 4.100000e+00 4.200000e+00 4.300000e+00
```

这是因为StaticArray\<double, size\>::print()不再是部分特化的函数——它是部分特化类StaticArray\<double, size\>的非特化成员函数。

然而，这不是一个很好的解决方案，因为我们必须将大量代码从StaticArray\<T, size\>复制到StaticArray\<double, size\>。

如果有某种方法可以重用StaticArray\<T, size\>中的代码就好了。听起来像是继承的工作！

您可以从尝试这样编写代码开始：

```C++
template <int size> // size 是非类型模版参数
class StaticArray<double, size>: public StaticArray<T, size>
```

但这不起作用，因为我们使用T时没有定义它。没有语法允许我们以这种方式继承。

{{< alert success >}}
**旁白**

即使我们能够将T定义为类型模板参数，当StaticArray\<double, size\>被实例化时，编译器也需要用实际类型替换StaticArray\<T, size\>。它将使用什么实际类型？唯一有意义的类型是T = double，但这将使StaticArray\<double, size\>从自身继承！

{{< /alert >}}

幸运的是，通过使用public继承基类，有一个解决方法：

```C++
#include <iostream>

template <typename T, int size>
class StaticArray_Base
{
protected:
	T m_array[size]{};

public:
	T* getArray() { return m_array; }

	const T& operator[](int index) const { return m_array[index]; }
	T& operator[](int index) { return m_array[index]; }

	void print() const
	{
		for (int i{ 0 }; i < size; ++i)
			std::cout << m_array[i] << ' ';
		std::cout << '\n';
	}

	// 如果要使用虚函数，不要忘记析构函数声明为虚函数
};

template <typename T, int size>
class StaticArray: public StaticArray_Base<T, size>
{
};

template <int size>
class StaticArray<double, size>: public StaticArray_Base<double, size>
{
public:

	void print() const
	{
		for (int i{ 0 }; i < size; ++i)
			std::cout << std::scientific << this->m_array[i] << ' ';
// 注: this-> 前缀这里是必须的
// 细节请看 https://stackoverflow.com/a/6592617 或 https://isocpp.org/wiki/faq/templates#nondependent-name-lookup-members
		std::cout << '\n';
	}
};

int main()
{
	// 定义6个int的数组
	StaticArray<int, 6> intArray{};

	// 按顺序填充并打印
	for (int count{ 0 }; count < 6; ++count)
		intArray[count] = count;

	intArray.print();

	// 定义有6个double的数组
	StaticArray<double, 4> doubleArray{};

	for (int count{ 0 }; count < 4; ++count)
		doubleArray[count] = (4.0 + 0.1 * count);

	doubleArray.print();

	return 0;
}
```

这与上面的打印相同的结果，但重复代码少得多。

***

{{< prevnext prev="/basic/chapter26/class-template-specialization/" next="/basic/chapter26/pointer-part-template-special/" >}}
26.3 类模板特化
<--->
26.5 指针的部分模板特化
{{< /prevnext >}}
