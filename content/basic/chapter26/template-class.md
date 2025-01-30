---
title: "模板类"
date: 2025-01-22T20:47:14+08:00
---

在之前，我们介绍了函数模板，它允许我们泛化函数以处理许多不同的数据类型。虽然这是泛型编程道路上的一个伟大开端，但它并不能解决我们所有的问题。让我们来看一个这样的例子，看看模板可以为我们做些什么。

***
## 模板和容器类

容器类使用组合来包含其他类的多个实例。IntArray类是这样的一个例子。下面是该类的一个简化示例：

```C++
#ifndef INTARRAY_H
#define INTARRAY_H

#include <cassert>

class IntArray
{
private:
    int m_length{};
    int* m_data{};

public:

    IntArray(int length)
    {
        assert(length > 0);
        m_data = new int[length]{};
        m_length = length;
    }

    // 不允许 IntArray 被拷贝
    IntArray(const IntArray&) = delete;
    IntArray& operator=(const IntArray&) = delete;

    ~IntArray()
    {
        delete[] m_data;
    }

    void erase()
    {
        delete[] m_data;
        // 确保 m_data 为nullptr
        // 否则 它将指向被释放的空间
        m_data = nullptr;
        m_length = 0;
    }

    int& operator[](int index)
    {
        assert(index >= 0 && index < m_length);
        return m_data[index];
    }

    int getLength() const { return m_length; }
};

#endif
```

虽然这个类提供了一种创建整数数组的简单方法，但如果我们想创建一个double数组，该怎么办？使用传统的编程方法，我们必须创建一个全新的类！这里是DoubleArray的一个例子，这是一个用于保存双精度数的数组类

```C++
#ifndef DOUBLEARRAY_H
#define DOUBLEARRAY_H

#include <cassert>

class DoubleArray
{
private:
    int m_length{};
    double* m_data{};

public:

    DoubleArray(int length)
    {
        assert(length > 0);
        m_data = new double[length]{};
        m_length = length;
    }

    DoubleArray(const DoubleArray&) = delete;
    DoubleArray& operator=(const DoubleArray&) = delete;

    ~DoubleArray()
    {
        delete[] m_data;
    }

    void erase()
    {
        delete[] m_data;
        // 确保 m_data 为nullptr
        // 否则 它将指向被释放的空间
        m_data = nullptr;
        m_length = 0;
    }

    double& operator[](int index)
    {
        assert(index >= 0 && index < m_length);
        return m_data[index];
    }

    int getLength() const { return m_length; }
};

#endif
```

尽管代码清单很长，但您会注意到这两个类几乎是相同的！事实上，唯一的实质性区别是所包含的数据类型（int与double）。正如您可能已经猜到的，这是另一个可以很好地使用模板的领域，使我们不必创建一个绑定到特定数据类型的类。

创建模板类的方式与创建模版函数的方式几乎相同，所以我们将通过示例继续。

这是我们的数组类，模板化版本：

Array.h:

```C++
#ifndef ARRAY_H
#define ARRAY_H

#include <cassert>

template <typename T> // 新增
class Array
{
private:
    int m_length{};
    T* m_data{}; // 修改类型为 T

public:

    Array(int length)
    {
        assert(length > 0);
        m_data = new T[length]{}; // 分配存放类型为 T 的对象的数组
        m_length = length;
    }

    Array(const Array&) = delete;
    Array& operator=(const Array&) = delete;

    ~Array()
    {
        delete[] m_data;
    }

    void erase()
    {
        delete[] m_data;
        // 确保 m_data 为nullptr
        // 否则 它将指向被释放的空间
        m_data = nullptr;
        m_length = 0;
    }

    // operator[] 函数，在下面定义
    T& operator[](int index); // 现在返回 T&

    int getLength() const { return m_length; }
};

// 在类外定义的成员函数，因此需要带上模版声明
template <typename T>
T& Array<T>::operator[](int index) // 现在返回 T&
{
    assert(index >= 0 && index < m_length);
    return m_data[index];
}

#endif
```

如您所见，该版本几乎与IntArray版本相同，只是我们添加了模板声明，并将包含的数据类型从int更改为T。

请注意，我们还在类声明外部定义了operator[]函数。这不是必要的，但由于语法的原因，新程序员在第一次尝试这样做时通常会出错，因此一个例子很有启发性。在类声明外部定义的每个模板成员函数都需要自己的模板声明。此外，请注意模板数组类的名称是Array\<T\>，而不是Array。在类内部使用Array，在类外部使用Array\<T\>。例如，拷贝构造函数和赋值运算符使用Array，而不是Array\<T\>。

下面是一个使用上述模板数组类的简短示例：

```C++
#include <iostream>
#include "Array.h"

int main()
{
	const int length { 12 };
	Array<int> intArray { length };
	Array<double> doubleArray { length };

	for (int count{ 0 }; count < length; ++count)
	{
		intArray[count] = count;
		doubleArray[count] = count + 0.5;
	}

	for (int count{ length - 1 }; count >= 0; --count)
		std::cout << intArray[count] << '\t' << doubleArray[count] << '\n';

	return 0;
}
```

此示例打印以下内容：

```C++
11     11.5
10     10.5
9       9.5
8       8.5
7       7.5
6       6.5
5       5.5
4       4.5
3       3.5
2       2.5
1       1.5
0       0.5
```

模板类的实例化方式与模板函数相同--编译器根据需要模版输出副本，按用户需要的实际数据类型替换模板参数，然后编译副本。如果不使用模板类，编译器甚至不会编译它。

模板类是实现容器类的理想选择，因为容器在各种数据类型上工作是非常理想的，模板允许您在不复制代码的情况下这样做。尽管语法很难看，错误消息也可能很神秘，但模板类确实是C++最好、最有用的功能之一。

***
## 拆分模板类

模板不是类或函数——它是用于创建类或函数的模具。因此，它的工作方式与普通函数或类的工作方式不完全相同。在大多数情况下，这不是什么大问题。然而，有一个领域通常会给开发人员带来问题。

对于非模板类，常见的过程是将类定义放在头文件中，将成员函数定义放在相同名称的代码文件中。这样，成员函数定义被编译为单独的项目文件。然而，对于模板，这不起作用。

请考虑以下内容：

Array.h:

```C++
#ifndef ARRAY_H
#define ARRAY_H

#include <cassert>

template <typename T> // 新增
class Array
{
private:
    int m_length{};
    T* m_data{}; // 修改类型为 T

public:

    Array(int length)
    {
        assert(length > 0);
        m_data = new T[length]{}; // 分配存放类型为 T 的对象的数组
        m_length = length;
    }

    Array(const Array&) = delete;
    Array& operator=(const Array&) = delete;

    ~Array()
    {
        delete[] m_data;
    }

    void erase()
    {
        delete[] m_data;
        // 确保 m_data 为nullptr
        // 否则 它将指向被释放的空间
        m_data = nullptr;
        m_length = 0;
    }

    // operator[] 函数，在对应的cpp文件定义
    T& operator[](int index); // 现在返回 T&

    int getLength() const { return m_length; }
};

// Array<T>::operator[] 定义移动到 Array.cpp

#endif
```

Array.cpp:

```C++
#include "Array.h"

// 在类外定义的成员函数，因此需要带上模版声明
template <typename T>
T& Array<T>::operator[](int index) // 现在返回 T&
{
    assert(index >= 0 && index < m_length);
    return m_data[index];
}
```

main.cpp:

```C++
#include <iostream>
#include "Array.h"

int main()
{
	const int length { 12 };
	Array<int> intArray { length };
	Array<double> doubleArray { length };

	for (int count{ 0 }; count < length; ++count)
	{
		intArray[count] = count;
		doubleArray[count] = count + 0.5;
	}

	for (int count{ length - 1 }; count >= 0; --count)
		std::cout << intArray[count] << '\t' << doubleArray[count] << '\n';

	return 0;
}
```

上述程序会导致链接错误：

```C++
undefined reference to `Array<int>::operator[](int)'
```

就像函数模板一样，如果在翻译单元中使用类模板（例如，作为intArray等对象的类型），编译器将仅实例化类模板。为了执行实例化，编译器必须同时看到完整的类模板定义（不仅仅是声明）和所需的特定模板类型。

还要记住，C++单独编译文件。编译main.cpp时，Array.h头文件的内容（包括模板类定义）被复制到main.cpp中。当编译器发现我们需要两个模板实例Array\<int\>和Array\<double\>时，它将实例化这些实例，并将它们编译为main.cpp翻译单元的一部分。由于 operator[] 成员函数具有声明，编译器将接受对它的调用，假设它将在其他地方定义。

单独编译Array.cpp时，Array.h头文件的内容被复制到Array.cpp中，但编译器在Array.cpp中找不到任何需要实例化Array类模板或Array\<int\>::operator[]函数模板的代码——因此它不会实例化任何内容。

因此，当程序被链接时，我们将得到一个链接器错误，因为main.cpp调用了Array\<int\>::operator[]，但该模板函数从未实例化！

有许多方法可以解决这个问题。

最简单的方法是将所有模板类代码放在头文件中（在本例中，将Array.cpp的内容放在类下面的Array.h中）。这样，当您引用头文件时，所有模板代码都将位于一个位置。这种解决方案的好处是它很简单。这里的缺点是，如果模板类在许多文件中使用，您将得到模板类的许多本地实例，这可能会增加编译和链接时间（链接器应该删除重复的定义，因此它不会膨胀您的可执行文件）。这是我们的首选解决方案，除非编译或链接时间开始成为问题。

如果您认为将Array.cpp代码放入Array.h头文件会使头文件过长/混乱，则另一种方法是将Array.cpp的内容移动到名为Array.inl（.inl表示内联）的新文件中，然后在Array.h头文件的底部（头文件保护内）引用Array.inl。这产生了与将所有代码放在头中相同的结果，但有助于使事情更有条理。

其他解决方案涉及 include .cpp文件，但我们不建议使用这种方式，因为include cpp的使用方式是非标准的。

另一种替代方法是使用三文件方法。模板类定义在头文件中。模板类成员函数放在代码文件中。然后添加第三个文件，其中包含您需要的所有实例化类：

templates.cpp:

```C++
// 确保可以看到完整的Array模板定义
#include "Array.h"
#include "Array.cpp" // 我们在这里打破了最佳实践，但仅在这一处

// 此处include所需的其他.h和.cpp模板定义

template class Array<int>; // 显式实例化模板 Array<int>
template class Array<double>; // 显式实例化模板 Array<double>

// 在此处实例化其他模板
```

“template class”使编译器显式实例化模板类。在上述情况下，编译器将在templates.cpp内实例化模板Array\<int\>和Array\<double\>的定义。想要使用这些类型的其他代码文件可以引用Array.h（以满足编译器要求），链接器将从template.cpp链接这些显式类型定义。

这种方法可能更有效（取决于编译器和链接器处理模板和重复定义的方式），但需要为每个程序维护templates.cpp文件。

***
