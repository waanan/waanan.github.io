---
title: "重载赋值运算符"
date: 2024-08-20T12:01:51+08:00
---

拷贝赋值操作符（operator=）用于将值从一个对象复制到另一个已存在的对象。

{{< alert success >}}
**相关内容**

从C++11开始，C++还支持“移动赋值”。我们在后续进行讨论。

{{< /alert >}}

***
## 拷贝赋值与拷贝构造函数

拷贝构造函数和拷贝赋值操作符的用途几乎相同——都将一个对象复制到另一个对象。然而，拷贝构造函数初始化新对象，而赋值运算符替换现有对象的内容。

拷贝构造函数和拷贝赋值操作符之间的差异给新程序员带来了许多困惑，但它实际上并不那么困难。总结：

1. 如果在复制之前必须创建新对象，则使用拷贝构造函数（注意：这包括按值传递或返回对象）。
2. 如果在复制之前不必创建新对象，则使用赋值运算符。

***
## 重载赋值运算符

重载拷贝赋值操作符（operator=）相当简单，但有一个特定的警告需要注意。拷贝赋值运算符必须作为成员函数重载。

```C++
#include <cassert>
#include <iostream>

class Fraction
{
private:
	int m_numerator { 0 };
	int m_denominator { 1 };

public:
	// 默认构造函数
	Fraction(int numerator = 0, int denominator = 1 )
		: m_numerator { numerator }, m_denominator { denominator }
	{
		assert(denominator != 0);
	}

	// 拷贝构造函数
	Fraction(const Fraction& copy)
		: m_numerator { copy.m_numerator }, m_denominator { copy.m_denominator }
	{
		// 不需要判断denominator为0，因为被复制的对象，不可能无效
		std::cout << "Copy constructor called\n"; // 这里打印，为了证明函数有效
	}

	// 重载赋值操作符
	Fraction& operator= (const Fraction& fraction);

	friend std::ostream& operator<<(std::ostream& out, const Fraction& f1);
        
};

std::ostream& operator<<(std::ostream& out, const Fraction& f1)
{
	out << f1.m_numerator << '/' << f1.m_denominator;
	return out;
}

// operator= 的最简单的实现
Fraction& Fraction::operator= (const Fraction& fraction)
{
    // do the copy
    m_numerator = fraction.m_numerator;
    m_denominator = fraction.m_denominator;

    // 返回当前对象，以便可以链式操作
    return *this;
}

int main()
{
    Fraction fiveThirds { 5, 3 };
    Fraction f;
    f = fiveThirds; // 调用重载的拷贝复制操作符
    std::cout << f;

    return 0;
}
```

这将打印：

```C++
5/3
```

到目前为止，这应该是非常简单的。我们的 “operator=” 返回*this，因此我们可以将多个赋值链接在一起：

```C++
int main()
{
    Fraction f1 { 5, 3 };
    Fraction f2 { 7, 2 };
    Fraction f3 { 9, 5 };

    f1 = f2 = f3; // 链式赋值

    return 0;
}
```

***
## 自我赋值导致的问题

这里是事情开始变得更有趣的地方。C++允许自我赋值：

```C++
int main()
{
    Fraction f1 { 5, 3 };
    f1 = f1; // 自我赋值

    return 0;
}
```

这将调用f1.operator=(f1)，并且在上面的简单实现下，所有成员都将被分配给自己。在这个特定的示例中，自我分配导致每个成员被分配给自己，这除了浪费时间之外，没有任何其它作用。在大多数情况下，自我赋值根本不需要做任何事情！

然而，在赋值运算符需要动态分配内存的情况下，自我赋值实际上可能是危险的：

```C++
#include <algorithm> // for std::max and std::copy_n
#include <iostream>

class MyString
{
private:
	char* m_data {};
	int m_length {};

public:
	MyString(const char* data = nullptr, int length = 0 )
		: m_length { std::max(length, 0) }
	{
		if (length)
		{
			m_data = new char[static_cast<std::size_t>(length)];
			std::copy_n(data, length, m_data); // 拷贝 length 长度的数据到 m_data
		}
	}
	~MyString()
	{
		delete[] m_data;
	}

	MyString(const MyString&) = default; // 一些编译器 (gcc) 会告警，如果成员变量有指针，但没有实现拷贝构造函数

	// 重载赋值操作符
	MyString& operator= (const MyString& str);

	friend std::ostream& operator<<(std::ostream& out, const MyString& s);
};

std::ostream& operator<<(std::ostream& out, const MyString& s)
{
	out << s.m_data;
	return out;
}

// operator= 的简单的有问题的实现 (不要使用)
MyString& MyString::operator= (const MyString& str)
{
	// 如果原来数据存在，进行删除
	if (m_data) delete[] m_data;

	m_length = str.m_length;
	m_data = nullptr;

	// 分配新的合适的长度的内存
	if (m_length)
		m_data = new char[static_cast<std::size_t>(str.m_length)];

	std::copy_n(str.m_data, m_length, m_data); // 将 m_length 长度的数据从 str.m_data 复制到 m_data

	// 返回当前对象，以便可以链式操作
	return *this;
}

int main()
{
	MyString alex("Alex", 5); // 遇到 Alex
	MyString employee;
	employee = alex; // Alex 现在是 employee
	std::cout << employee; // 打印 employee

	return 0;
}
```

首先，按原样运行程序。您将看到程序按原样打印“Alex”。

现在运行以下程序：

```C++
int main()
{
    MyString alex { "Alex", 5 }; // 遇到 Alex
    alex = alex; // Alex 是它自己
    std::cout << alex; // 打印 Alex

    return 0;
}
```

您可能会得到垃圾输出。发生了什么事？

考虑当隐式对象和传入参数（str）都是变量alex时，重载“operator=”中发生了什么。在这种情况下，m_data与str.m_data相同。发生的第一件事是函数检查隐式对象是否已经有字符串。如果是，需要删除它，这样就不会导致内存泄漏。在这种情况下，之前已经有m_data，因此函数删除m_data。但由于str与*this相同，因此想要复制的字符串已被删除，m_data（和str.m_data）悬空。

稍后，我们将新内存分配给m_data（和str.m_data）。因此，当随后将数据从str.m_data复制到m_data时，正在复制垃圾，因为str.m_data未初始化。

***
## 检测和处理自我赋值

幸运的是，我们可以检测到自我赋值何时发生。下面是MyString类的重载“operator=”的合理实现：

```C++
MyString& MyString::operator= (const MyString& str)
{
	// 自我赋值检查
	if (this == &str)
		return *this;

	// 如果原来数据存在，进行删除
	if (m_data) delete[] m_data;

	m_length = str.m_length;
	m_data = nullptr;

	// 分配新的合适的长度的内存
	if (m_length)
		m_data = new char[static_cast<std::size_t>(str.m_length)];

	std::copy_n(str.m_data, m_length, m_data); // 将 m_length 长度的数据从 str.m_data 复制到 m_data

	// 返回当前对象，以便可以链式操作
	return *this;
}
```

通过检查隐式对象的地址是否与作为参数传入的对象的地址相同，我们可以让赋值运算符立即返回，而不做任何其他工作。

因为这只是一个指针比较，所以它很快，并且不需要重载“operator==”。

***
## 何时不处理自我复制

对于拷贝构造函数，通常跳过自我赋值检查。由于正在拷贝构造的对象是新创建的，因此新创建的对象可以等于正在复制的对象的唯一情况是尝试用其自身初始化自身：

```C++
someClass c { c };
```

在这种情况下，编译器应该警告您c是未初始化的变量。

其次，在可以自然处理自我赋值的类中，可以省略自我赋值检查。考虑具有自我赋值保护的Fraction类赋值运算符：

```C++
// operator= 的更好的实现
Fraction& Fraction::operator= (const Fraction& fraction)
{
    // 自我赋值保护
    if (this == &fraction)
        return *this;

    // 做复制
    m_numerator = fraction.m_numerator; // 发生自我赋值也无影响
    m_denominator = fraction.m_denominator; // 发生自我赋值也无影响

    // 返回当前对象，以便可以链式操作
    return *this;
}
```

如果自我赋值保护不存在，则该函数在自我赋值期间仍将正确运行（因为该函数执行的所有操作都可以正确处理自我赋值）。

由于自我赋值是一种罕见的事件，一些著名的C++专家建议即使在可以从中受益的类中也省略自我赋值保护。我们不建议这样做，因为我们认为，更好的做法是进行防御性编码，然后在以后有选择地优化。

***
## 隐式拷贝赋值运算符

与其他操作符不同，如果不提供用户定义的pulic拷贝赋值运算符，编译器将为类提供隐式的实现。该赋值操作符执行成员级赋值（本质上与默认拷贝构造函数所做的成员级初始化相同）。

与其他构造函数和运算符一样，您可以通过将拷贝赋值运算符设置为private或使用delete关键字来防止进行赋值：

```C++
#include <cassert>
#include <iostream>

class Fraction
{
private:
	int m_numerator { 0 };
	int m_denominator { 1 };

public:
    // 默认构造函数
    Fraction(int numerator = 0, int denominator = 1)
        : m_numerator { numerator }, m_denominator { denominator }
    {
        assert(denominator != 0);
    }

	// 拷贝构造函数
	Fraction(const Fraction &copy) = delete;

	// 重载赋值运算符
	Fraction& operator= (const Fraction& fraction) = delete; // 不允许进行赋值!

	friend std::ostream& operator<<(std::ostream& out, const Fraction& f1);
        
};

std::ostream& operator<<(std::ostream& out, const Fraction& f1)
{
	out << f1.m_numerator << '/' << f1.m_denominator;
	return out;
}

int main()
{
    Fraction fiveThirds { 5, 3 };
    Fraction f;
    f = fiveThirds; // 编译失败, operator= 被 deleted
    std::cout << f;

    return 0;
}
```

请注意，如果类具有常量成员，编译器会自动将“operator=”定义为删除。这是因为不能为常量成员赋值，所以编译器将假定您的类不应该是可赋值的。

如果希望具有常量成员的类是可赋值的（对于非常量成员进行赋值），则需要显式重载“operator=”，并手动赋值每个非常量成员。

*** 