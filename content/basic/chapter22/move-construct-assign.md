---
title: "移动构造函数和移动赋值函数"
date: 2024-08-23T14:54:42+08:00
---

在前面，讨论了std::auto_ptr，讨论了移动语义的需求，并分析了为复制语义设计的函数（拷贝构造函数和拷贝赋值运算符）重新定义以实现移动语义时出现的一些缺点。

在本课中，将更深入地了解C++11如何通过移动构造函数和移动赋值函数来解决这些问题。

***
## 回顾拷贝构造函数和拷贝赋值函数

首先，让我们花点时间回顾一下复制语义。

拷贝构造函数用于通过复制同一类的对象来初始化类。拷贝赋值函数用于将一个类对象复制到另一个现有的类对象。默认情况下，如果没有显式提供拷贝构造函数和拷贝赋值函数，C++将提供默认的。这些编译器提供的函数执行浅复制，这可能会导致分配动态内存的类出现问题。因此，处理动态内存的类应该覆盖这些函数来进行深拷贝。

回到本章第一课中的Auto_ptr智能指针类示例，让我们看看实现拷贝构造函数和拷贝赋值函数（执行深拷贝）的版本，以及使用它们的示例程序：

```C++
#include <iostream>

template<typename T>
class Auto_ptr3
{
	T* m_ptr {};
public:
	Auto_ptr3(T* ptr = nullptr)
		: m_ptr { ptr }
	{
	}

	~Auto_ptr3()
	{
		delete m_ptr;
	}

	// 拷贝构造函数
	// 从 a.m_ptr 到 m_ptr 的深拷贝
	Auto_ptr3(const Auto_ptr3& a)
	{
		m_ptr = new T;
		*m_ptr = *a.m_ptr;
	}

	// 拷贝赋值
	// 从 a.m_ptr 到 m_ptr 的深拷贝
	Auto_ptr3& operator=(const Auto_ptr3& a)
	{
		// 自我赋值检查
		if (&a == this)
			return *this;

		// 释放已经持有的资源
		delete m_ptr;

		// 拷贝资源
		m_ptr = new T;
		*m_ptr = *a.m_ptr;

		return *this;
	}

	T& operator*() const { return *m_ptr; }
	T* operator->() const { return m_ptr; }
	bool isNull() const { return m_ptr == nullptr; }
};

class Resource
{
public:
	Resource() { std::cout << "Resource acquired\n"; }
	~Resource() { std::cout << "Resource destroyed\n"; }
};

Auto_ptr3<Resource> generateResource()
{
	Auto_ptr3<Resource> res{new Resource};
	return res; // 这里会触发拷贝构造函数
}

int main()
{
	Auto_ptr3<Resource> mainres;
	mainres = generateResource(); // 这里会触发拷贝赋值函数

	return 0;
}
```

在这个程序中，我们使用一个名为generateResource（）的函数来创建一个智能指针封装的资源，然后将其传递回函数main（）。函数main（）然后将其分配给现有的Auto_ptr3对象。

运行此程序时，它将打印：

```C++
Resource acquired
Resource acquired
Resource destroyed
Resource acquired
Resource destroyed
Resource destroyed
```

（注意：如果编译器从函数generateResource（）中省略了返回值的构造，则只能获得4个输出）

对于这样一个简单的程序，这是大量的资源创建和销毁！这是怎么回事？

让我们仔细看看。此程序中发生了6个关键步骤（每个打印消息一个）：

1. 在generateResource()，局部变量res被动态创建，打印出第一个“Resource acquired”
2. res 按值返回给 main() 函数，因为res是局部变量，所以不能按地址或按引用返回，因为那样会导致悬空引用。所以res被拷贝给一个临时对象。因为这是一次深拷贝，一个新的Resource对象被分配了出来并调用了拷贝构造函数，因此打印出第二个“Resource acquired”
3. res超出了作用域，第一创建的Resource对象被销毁，打印出第一个“Resource destroyed”
4. 临时对象被赋值给mainres，发生了拷贝赋值。因为这是一次深拷贝，所以一个新的Resource对象被分配了出来，打印出了另一个“Resource acquired”
5. 赋值表达式结束，临时对象超出了作用域，被销毁，打印出第二个“Resource destroyed”
6. 在main()函数末尾，mainres超出作用域被销毁，打印出最后一个“Resource destroyed”

简而言之，因为调用一次拷贝构造函数将res复制到临时对象，并赋值一次将临时对象复制到mainres，所以我们总共分配和销毁了3个单独的对象。

效率低下，但至少不会崩溃！

然而，有了移动语义，我们可以做得更好。

***
## 移动构造函数和移动赋值

C++11定义了两个服务于移动语义的新函数：移动构造函数和移动赋值运算符。拷贝构造函数和拷贝赋值的目标是将一个对象复制到另一个对象，而移动构造函数和移动赋值的目标则是将资源的所有权从一个对象移动到另一对象（这通常比制作副本便宜得多）。

定义移动构造函数和移动赋值的工作方式类似于拷贝版本。然而，这些函数的拷贝版本采用常量左值引用参数（它将绑定到几乎任何东西），但这些函数的移动版本使用非常量右值引用参数（仅绑定到右值）。

这里是与上面相同的Auto_ptr3类，添加了移动构造函数和移动赋值运算符。为了进行比较，我们留下了深拷贝的拷贝构造函数和拷贝赋值函数。

```C++
#include <iostream>

template<typename T>
class Auto_ptr4
{
	T* m_ptr {};
public:
	Auto_ptr4(T* ptr = nullptr)
		: m_ptr { ptr }
	{
	}

	~Auto_ptr4()
	{
		delete m_ptr;
	}

	// 拷贝构造函数
	// 从 a.m_ptr 到 m_ptr 的深拷贝
	Auto_ptr4(const Auto_ptr4& a)
	{
		m_ptr = new T;
		*m_ptr = *a.m_ptr;
	}

	// 移动构造函数
	// a.m_ptr 的所有权转移至 m_ptr
	Auto_ptr4(Auto_ptr4&& a) noexcept
		: m_ptr(a.m_ptr)
	{
		a.m_ptr = nullptr; // 这一行后面会详细解释
	}

	// 拷贝赋值
	// 从 a.m_ptr 到 m_ptr 的深拷贝
	Auto_ptr4& operator=(const Auto_ptr4& a)
	{
		// 自我赋值检查
		if (&a == this)
			return *this;

		// 释放已经持有的资源
		delete m_ptr;

		// 拷贝资源
		m_ptr = new T;
		*m_ptr = *a.m_ptr;

		return *this;
	}

	// 移动赋值函数
	// a.m_ptr 的所有权转移至 m_ptr
	Auto_ptr4& operator=(Auto_ptr4&& a) noexcept
	{
		// 自我赋值检查
		if (&a == this)
			return *this;

		// 释放已经持有的资源
		delete m_ptr;

		// a.m_ptr 的所有权转移至 m_ptr
		m_ptr = a.m_ptr;
		a.m_ptr = nullptr; // 这一行后面会详细解释

		return *this;
	}

	T& operator*() const { return *m_ptr; }
	T* operator->() const { return m_ptr; }
	bool isNull() const { return m_ptr == nullptr; }
};

class Resource
{
public:
	Resource() { std::cout << "Resource acquired\n"; }
	~Resource() { std::cout << "Resource destroyed\n"; }
};

Auto_ptr4<Resource> generateResource()
{
	Auto_ptr4<Resource> res{new Resource};
	return res; // 这一行会触发移动构造函数
}

int main()
{
	Auto_ptr4<Resource> mainres;
	mainres = generateResource(); // 这一行会触发移动赋值函数

	return 0;
}
```

移动构造函数和移动赋值运算符很简单。我们不是将源对象（a）深度拷贝到隐式对象中，而是简单地移动（窃取）源对象的资源。这涉及将源指针浅拷贝到隐式对象中，然后将源指针设置为null。

运行时，此程序打印：

```C++
Resource acquired
Resource destroyed
```

那好多了！

main()中的流程与之前完全相同。然而，该程序不是调用拷贝构造函数和拷贝赋值函数，而是调用移动构造函数和移动赋值运算符。再深入一点：

1. 在generateResource()，局部变量res被动态创建，打印出第一个“Resource acquired”
2. res 按值返回给main()函数，res被移动构造到一个临时对象中，动态创建的Resource所有权被转移到了临时对象，在下面小节会详细分析为什么会发生这样的行为
3. res超出作用域，但因为它不再管理任何指针，所以无事发生
4. 临时对象被移动赋值到mainres，动态创建的Resource所有权被转移到mainres
5. 赋值语句结束，临时对象被销毁，但因为临时对象不再管理任何指针，所以无事发生
6. main()函数末尾，mainres超出作用域被销毁，打印出最后一个“Resource destroyed”

因此，我们不是复制资源两次，而是转移它两次。这更有效，因为Resource只构造和销毁一次，而不是三次。

{{< alert success >}}
**相关内容**

移动构造函数和移动赋值应标记为noexcept。这告诉编译器这些函数不会引发异常。

我们在后面介绍noexcept。

{{< /alert >}}

***
## 何时调用移动构造函数和移动赋值函数？

当定义了这些函数，并且构造或赋值的参数是右值，调用移动构造函数和移动赋值函数。最典型的情况是，值将是字面值或临时值。

否则使用拷贝构造函数和拷贝赋值（当参数是左值时，或者当参数是右值并且未定义移动构造函数或移动赋值函数时）。

***
## 隐式移动构造函数和移动赋值运算符

如果满足以下所有条件，编译器将创建隐式移动构造函数和移动赋值运算符：

1. 没有用户声明的拷贝构造函数或拷贝赋值函数。
2. 没有用户声明的移动构造函数或移动赋值运算符。
3. 没有用户声明的析构函数。

这两个默认的函数都执行成员级移动，规则如下：

1. 如果成员变量有移动构造或者移动赋值函数，则会调用对应的函数
2. 否则，进行拷贝

这意味着，如果成员变量是指针，则默认进行浅拷贝。

***
## 移动语义背后的关键点

现在您有了足够的上下文来理解移动语义背后的关键点。

如果我们构造一个对象或进行赋值，其中参数是左值，那么唯一可以合理地做的事情就是复制左值。我们不能假设更改左值是安全的，因为它可能会在以后的程序中再次使用。如果我们有一个表达式“a=b”（其中b是左值），不应该期望b以任何方式改变。

然而，如果我们构造一个对象或进行赋值，其中参数是右值，则我们知道右值只是某种临时对象。可以简单地将其资源（代价很低）转移到我们正在构造或赋值的对象，而不是复制它（这可能很昂贵）。这样做是安全的，因为临时变量无论如何都将在表达式末尾被销毁，所以我们知道它将永远不会被再次使用！

C++11通过右值引用，使我们能够在参数为右值和左值时提供不同的行为，使我们可以按对象的行为方式做出更聪明、更有效的决策。

{{< alert success >}}
**关键点**

移动语义是一个优化机会。

{{< /alert >}}

***
## 移动函数应始终使两个对象都处于有效状态

在上面的示例中，移动构造函数和移动赋值函数都将a.m_ptr设置为nullptr。这似乎是无需做的的——毕竟，如果a是一个临时的右值，那么如果a无论如何都要被销毁，为什么还要费心进行“清理”呢？

答案很简单：当a超出作用域时，将调用a的析构函数，并删除a.m_ptr。如果在这时，a.m_ptr仍然指向与m_ptr相同的对象，则m_ptr将变为悬空指针。当包含m_ptr的对象最终被使用（或销毁）时，将得到未定义的行为。

在实现移动语义时，重要的是确保资源移出的对象处于有效状态，以便它将正确地销毁（而不会导致未定义的行为）。

***
## 函数按值返回可以触发移动而不是拷贝

在上面的Auto_ptr4示例的generateResource（）函数中，当变量res按值返回时，它将被移动而不是复制，即使res是左值。C++规范有一个特殊的规则，即使是左值，也可以移动按值从函数返回的对象。这是有意义的，因为res无论如何都会在函数的末尾被销毁！不妨窃取它的资源，而不是制作昂贵和不必要的副本。

尽管编译器可以移动左值返回值，但在某些情况下，它甚至可以通过完全避免创建返回值来做得更好（这避免了制作副本而且根本不做移动）。在这种情况下，既不会调用拷贝构造函数，也不会调用移动构造函数。

***
## 禁用复制

在上面的Auto_ptr4类中，为了进行比较，我们保留了拷贝构造函数和赋值运算符。但在支持移动的类中，有时需要删除拷贝构造函数和拷贝赋值函数，以确保不进行复制。在Auto_ptr类的情况下，我们不想复制模板化的对象T—— 一个原因是因为它可能很昂贵，而且类T可能也不支持复制！

下面是支持移动语义但不支持复制语义的Auto_ptr版本：

```C++
#include <iostream>

template<typename T>
class Auto_ptr5
{
	T* m_ptr {};
public:
	Auto_ptr5(T* ptr = nullptr)
		: m_ptr { ptr }
	{
	}

	~Auto_ptr5()
	{
		delete m_ptr;
	}

	// 拷贝构造 -- 不允许拷贝!
	Auto_ptr5(const Auto_ptr5& a) = delete;

	// 移动构造函数
	// a.m_ptr 的所有权转移至 m_ptr
	Auto_ptr5(Auto_ptr5&& a) noexcept
		: m_ptr(a.m_ptr)
	{
		a.m_ptr = nullptr;
	}

	// 拷贝赋值 -- 不允许拷贝!
	Auto_ptr5& operator=(const Auto_ptr5& a) = delete;

	// 移动赋值函数
	// a.m_ptr 的所有权转移至 m_ptr
	Auto_ptr5& operator=(Auto_ptr5&& a) noexcept
	{
		// 自我赋值检查
		if (&a == this)
			return *this;

		// 释放已经持有的资源
		delete m_ptr;

		// a.m_ptr 的所有权转移至 m_ptr
		m_ptr = a.m_ptr;
		a.m_ptr = nullptr;

		return *this;
	}

	T& operator*() const { return *m_ptr; }
	T* operator->() const { return m_ptr; }
	bool isNull() const { return m_ptr == nullptr; }
};
```

如果试图按值将Auto_ptr5 左值传递给函数，编译器将报错，提示初始化函数参数所需的拷贝构造函数已被删除。这很好，因为无论如何，大概率应该通过常量左值引用传递Auto_ptr5！

Auto_ptr5是一个很好的智能指针类。而且，事实上，标准库包含一个与此非常相似的类（您应该使用它），名为std::unique_ptr。我们将在本章后面讨论更多关于std::unique_ptr的内容。

***
## 另一个例子

让我们看一看另一个使用动态内存的类：一个简单的动态模板化数组。此类包含深拷贝构造函数和拷贝赋值函数。

```C++
#include <algorithm> // for std::copy_n
#include <iostream>

template <typename T>
class DynamicArray
{
private:
	T* m_array {};
	int m_length {};

public:
	DynamicArray(int length)
		: m_array { new T[length] }, m_length { length }
	{
	}

	~DynamicArray()
	{
		delete[] m_array;
	}

	// 拷贝构造
	DynamicArray(const DynamicArray &arr)
		: m_length { arr.m_length }
	{
		m_array = new T[m_length];
		std::copy_n(arr.m_array, m_length, m_array); // 复制 m_length 个元素，从 arr 到 m_array
	}

	// 拷贝赋值
	DynamicArray& operator=(const DynamicArray &arr)
	{
		if (&arr == this)
			return *this;

		delete[] m_array;
		
		m_length = arr.m_length;
		m_array = new T[m_length];

		std::copy_n(arr.m_array, m_length, m_array); // 复制 m_length 个元素，从 arr 到 m_array

		return *this;
	}

	int getLength() const { return m_length; }
	T& operator[](int index) { return m_array[index]; }
	const T& operator[](int index) const { return m_array[index]; }

};
```

现在让我们在程序中使用这个类。现在向您展示当我们在堆上分配一百万个整数时，这个类是如何执行的，我们将利用之前开发的Timer类为代码计时。将使用Timer类来计时代码的运行速度，并向您展示复制和移动之间的性能差异。

```C++
#include <algorithm> // for std::copy_n
#include <chrono> // for std::chrono functions
#include <iostream>

// 使用上面的 DynamicArray 类

class Timer
{
private:
	// 类型别名，简化代码
	using Clock = std::chrono::high_resolution_clock;
	using Second = std::chrono::duration<double, std::ratio<1> >;
	
	std::chrono::time_point<Clock> m_beg { Clock::now() };

public:
	void reset()
	{
		m_beg = Clock::now();
	}
	
	double elapsed() const
	{
		return std::chrono::duration_cast<Second>(Clock::now() - m_beg).count();
	}
};

// 返回一个所有元素都是输入双倍的数组
DynamicArray<int> cloneArrayAndDouble(const DynamicArray<int> &arr)
{
	DynamicArray<int> dbl(arr.getLength());
	for (int i = 0; i < arr.getLength(); ++i)
		dbl[i] = arr[i] * 2;

	return dbl;
}

int main()
{
	Timer t;

	DynamicArray<int> arr(1000000);

	for (int i = 0; i < arr.getLength(); i++)
		arr[i] = i;

	arr = cloneArrayAndDouble(arr);

	std::cout << t.elapsed();
}
```

在作者的一台机器上，在发布模式下，该程序在0.00825559秒内执行。

现在，让我们再次运行相同的程序，将拷贝构造函数和拷贝赋值替换为移动构造函数和移动赋值。

```C++
template <typename T>
class DynamicArray
{
private:
	T* m_array {};
	int m_length {};

public:
	DynamicArray(int length)
		: m_array(new T[length]), m_length(length)
	{
	}

	~DynamicArray()
	{
		delete[] m_array;
	}

	// 拷贝构造
	DynamicArray(const DynamicArray &arr) = delete;

	// 拷贝赋值
	DynamicArray& operator=(const DynamicArray &arr) = delete;

	// 移动构造
	DynamicArray(DynamicArray &&arr) noexcept
		:  m_array(arr.m_array), m_length(arr.m_length)
	{
		arr.m_length = 0;
		arr.m_array = nullptr;
	}

	// 移动赋值
	DynamicArray& operator=(DynamicArray &&arr) noexcept
	{
		if (&arr == this)
			return *this;

		delete[] m_array;

		m_length = arr.m_length;
		m_array = arr.m_array;
		arr.m_length = 0;
		arr.m_array = nullptr;

		return *this;
	}

	int getLength() const { return m_length; }
	T& operator[](int index) { return m_array[index]; }
	const T& operator[](int index) const { return m_array[index]; }

};

#include <iostream>
#include <chrono> // for std::chrono functions

class Timer
{
private:
	// 类型别名，简化代码
	using Clock = std::chrono::high_resolution_clock;
	using Second = std::chrono::duration<double, std::ratio<1> >;
	
	std::chrono::time_point<Clock> m_beg { Clock::now() };

public:
	void reset()
	{
		m_beg = Clock::now();
	}
	
	double elapsed() const
	{
		return std::chrono::duration_cast<Second>(Clock::now() - m_beg).count();
	}
};

// 返回一个所有元素都是输入双倍的数组
DynamicArray<int> cloneArrayAndDouble(const DynamicArray<int> &arr)
{
	DynamicArray<int> dbl(arr.getLength());
	for (int i = 0; i < arr.getLength(); ++i)
		dbl[i] = arr[i] * 2;

	return dbl;
}

int main()
{
	Timer t;

	DynamicArray<int> arr(1000000);

	for (int i = 0; i < arr.getLength(); i++)
		arr[i] = i;

	arr = cloneArrayAndDouble(arr);

	std::cout << t.elapsed();
}
```

在同一台机器上，该程序在0.0056秒内执行。

比较两个程序的运行时间，（0.00825559-0.0056）/ 0.00825559 * 100=32.1%，性能提升 32.1% ！

***
## 删除移动构造函数和移动赋值函数

可以使用=delete语法删除移动构造函数和移动赋值，就像删除拷贝构造函数和拷贝赋值一样。

```C++
#include <iostream>
#include <string>
#include <string_view>

class Name
{
private:
    std::string m_name {};

public:
    Name(std::string_view name) : m_name{ name }
    {
    }

    Name(const Name& name) = delete;
    Name& operator=(const Name& name) = delete;
    Name(Name&& name) = delete;
    Name& operator=(Name&& name) = delete;

    const std::string& get() const { return m_name; }
};

int main()
{
    Name n1{ "Alex" };
    n1 = Name{ "Joe" }; // 错误: 移动赋值被删除

    std::cout << n1.get() << '\n';

    return 0;
}
```

如果删除拷贝构造函数，编译器将不会生成隐式移动构造函数（使对象既不可复制也不可移动）。因此，在删除拷贝构造函数时，明确需要移动构造函数的行为是有用的。要么设置它们为delete（明确这是所需的行为），要么设置它们为default（仅使类移动）。

如果您想要可复制但不可移动的对象，那么仅删除移动构造函数和移动赋值似乎是一个好主意，但这会导致在复制省略不生效的情况下，类不能按值返回。发生这种情况是因为虽然声明删除了移动构造函数，但仍可进行进行重载解析。并且函数按值返回将优先匹配已删除的移动构造函数，而不是未删除的拷贝构造函数。下面的程序对此进行了说明：

```C++
#include <iostream>
#include <string>
#include <string_view>

class Name
{
private:
    std::string m_name {};

public:
    Name(std::string_view name) : m_name{ name }
    {
    }

    Name(const Name& name) = default;
    Name& operator=(const Name& name) = default;

    Name(Name&& name) = delete;
    Name& operator=(Name&& name) = delete;

    const std::string& get() const { return m_name; }
};

Name getJoe()
{
    Name joe{ "Joe" };
    return joe; // 错误: 移动构造函数被删除
}

int main()
{
    Name n{ getJoe() };

    std::cout << n.get() << '\n';

    return 0;
}
```

{{< alert success >}}
**关键洞察力**

如果定义或删除了拷贝构造函数、拷贝赋值、移动构造函数、移动赋值或析构函数，那么应该定义或删除其中的每个函数。

{{< /alert >}}

***
## 移动语义和std::swap的问题(进阶)

交换也适用于移动语义，这意味着我们可以通过将资源与将被销毁的对象交换来实现移动构造函数和移动赋值。

这有两个好处：

1. 持久化对象现在控制以前属于濒死对象所有权的资源（这是我们的主要目标）。
2. 垂死对象现在控制以前属于持久对象所有权的资源。当对象实际死亡时，它可以对这些资源进行清理。


当您考虑交换时，首先想到的通常是std::swap（）。然而，使用std::swap（）实现移动构造函数和移动赋值是有问题的，因为std::swap将导致无限递归问题。

您可以在以下示例中看到这种情况：

```C++
#include <iostream>
#include <string>
#include <string_view>

class Name
{
private:
    std::string m_name {}; // std::string 是可移动的

public:
    Name(std::string_view name) : m_name{ name }
    {
    }

    Name(const Name& name) = delete;
    Name& operator=(const Name& name) = delete;

    Name(Name&& name) noexcept
    {
        std::cout << "Move ctor\n";

        std::swap(*this, name); // 有问题!
    }

    Name& operator=(Name&& name) noexcept
    {
        std::cout << "Move assign\n";

        std::swap(*this, name); // 有问题!

        return *this;
    }

    const std::string& get() const { return m_name; }
};

int main()
{
    Name n1{ "Alex" };   
    n1 = Name{"Joe"}; // 触发移动赋值

    std::cout << n1.get() << '\n';
    
    return 0;
}
```

这将打印：

```C++
Move assign
Move ctor
Move ctor
Move ctor
Move ctor
```

无线打印……直到堆栈溢出。

而通过交换成员，就可以简单的实现移动语义，下面是一个示例：

```C++
#include <iostream>
#include <string>
#include <string_view>

class Name
{
private:
    std::string m_name {};

public:
    Name(std::string_view name) : m_name{ name }
    {
    }

    Name(const Name& name) = delete;
    Name& operator=(const Name& name) = delete;
    
    // 交换函数，交换Name的成员
    friend void swap(Name& a, Name& b) noexcept
    {
        // 通过 std::swap 交换成员, 而不是整个对象,
        // 避免无限循环
        std::swap(a.m_name, b.m_name);
    }

    Name(Name&& name) noexcept
    {
        std::cout << "Move ctor\n";

        swap(*this, name); // 调用我们自己的 swap, 而不是 std::swap
    }

    Name& operator=(Name&& name) noexcept
    {
        std::cout << "Move assign\n";

        swap(*this, name); // 调用我们自己的 swap, 而不是 std::swap

        return *this;
    }

    const std::string& get() const { return m_name; }
};

int main()
{
    Name n1{ "Alex" };   
    n1 = Name{"Joe"}; // 触发移动赋值

    std::cout << n1.get() << '\n';

    return 0;
}
```

这按预期工作，并打印：

```C++
Move assign
Joe
```

***