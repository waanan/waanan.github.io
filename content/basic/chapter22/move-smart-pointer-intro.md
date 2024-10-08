---
title: "智能指针和移动语义简介"
date: 2024-08-23T14:54:42+08:00
---

考虑一个动态分配值的函数:

```C++
void someFunction()
{
    Resource* ptr = new Resource(); // Resource 是结构体或类

    // 这里对ptr做一些操作

    delete ptr;
}
```

尽管上面的代码看起来相当简单，但很容易忘记释放ptr。即使您确实记得在函数末尾删除ptr，但如果函数提前退出，您可能忘记在中间退出时删除ptr。例如:

```C++
#include <iostream>

void someFunction()
{
    Resource* ptr = new Resource();

    int x;
    std::cout << "Enter an integer: ";
    std::cin >> x;

    if (x == 0)
        return; // 函数提前退出, ptr没有被删除!

    // 这里对ptr做一些操作

    delete ptr;
}
```

或者抛出异常导致提前退出:

```C++
#include <iostream>

void someFunction()
{
    Resource* ptr = new Resource();

    int x;
    std::cout << "Enter an integer: ";
    std::cin >> x;

    if (x == 0)
        throw 0; // 函数提前退出, ptr没有被删除!

    // 这里对ptr做一些操作

    delete ptr;
}
```

在上述两个程序中，提前使用return或throw语句，导致函数终止，而不能删除变量ptr。因此，分配给变量ptr的内存现在泄漏了（并且每次调用该函数并提早返回时都会再次泄漏）。

从本质上讲，之所以会出现这种问题，是因为指针变量没有内在的机制来清理它们自己。

***
## 智能指针类

类的最好之处之一是它们包含析构函数，当类的对象超出作用域时，析构函数会自动执行。因此，如果在构造函数中分配（或获取）内存，则可以在析构函数中释放它，并确保在类对象被销毁时释放内存（无论它是否超出作用域、是否显式删除，等等…）。这是RAII编程范例的核心。

因此，我们可以使用类来帮助我们管理和清理指针吗？当然可以！

考虑一个类，该类的唯一任务是保存并“拥有”传递给它的指针，然后在类对象超出作用域时释放该指针。只要该类的对象仅被创建为局部变量，我们就可以保证该类超出作用域时（无论函数何时或如何终止），拥有的指针将被销毁。

这是想法的初稿:

```C++
#include <iostream>

template <typename T>
class Auto_ptr1
{
	T* m_ptr {};
public:
	// 通过构造函数，“拥有”传递进来的指针
	Auto_ptr1(T* ptr=nullptr)
		:m_ptr(ptr)
	{
	}
	
	// 析构函数，确保拥有的指针被释放
	~Auto_ptr1()
	{
		delete m_ptr;
	}

	// 重载 解引用 和 operator-> ，以便 Auto_ptr1 用起来和 m_ptr 姿势一样.
	T& operator*() const { return *m_ptr; }
	T* operator->() const { return m_ptr; }
};

// 样例class，用来证明上述的方案有效
class Resource
{
public:
    Resource() { std::cout << "Resource acquired\n"; }
    ~Resource() { std::cout << "Resource destroyed\n"; }
};

int main()
{
	Auto_ptr1<Resource> res(new Resource()); // 注意这里动态分配了内存

        // ... 但没有显式delete释放

	// 注意这里使用 <Resource>, 而不是 <Resource*>
        // 这是因为 m_ptr 的类型时 T* (而不是 T)

	return 0;
} // res 这里超出作用域, 并且释放了 Resource 申请的内存
```

该程序打印:

```C++
Resource acquired
Resource destroyed
```

考虑下这个程序和类是如何工作的。首先，我们动态创建一个Resource，并将其作为参数传递给模板化的Auto_ptr1类。从这开始，我们的Auto_ptr1变量res拥有该Resource对象。因为res被声明为局部变量，并且具有块作用域，所以当块结束时，它将超出作用域，并被销毁（不用担心忘记释放它）。因为它是一个类，所以当它被销毁时，将调用Auto_ptr1析构函数。该析构函数将确保它所持有的资源指针被删除！

只要Auto_ptr1定义为局部变量（具有自动存储期，这是类名中的“Auto”部分），就可以保证资源在声明它的块的末尾被销毁，无论函数如何终止（即使它提前终止）。

这样的类称为智能指针。智能指针是一个组合类，旨在管理动态分配的内存，并确保当智能指针对象超出作用域时删除内存。（相关地，内置指针有时被称为“哑指针”，因为它们不能在指针变量失效之后进行清理）。

现在，让我们回到上面的someFunction()示例，并展示智能指针类如何解决我们的挑战:

```C++
#include <iostream>

template <typename T>
class Auto_ptr1
{
	T* m_ptr {};
public:
	// 通过构造函数，“拥有”传递进来的指针
	Auto_ptr1(T* ptr=nullptr)
		:m_ptr(ptr)
	{
	}
	
	// 析构函数，确保拥有的指针被释放
	~Auto_ptr1()
	{
		delete m_ptr;
	}

	// 重载 解引用 和 operator-> ，以便 Auto_ptr1 用起来和 m_ptr 姿势一样.
	T& operator*() const { return *m_ptr; }
	T* operator->() const { return m_ptr; }
};

// 样例class，用来证明上述的方案有效
class Resource
{
public:
    Resource() { std::cout << "Resource acquired\n"; }
    ~Resource() { std::cout << "Resource destroyed\n"; }
    void sayHi() { std::cout << "Hi!\n"; }
};

void someFunction()
{
    Auto_ptr1<Resource> ptr(new Resource()); // ptr 现在拥有 Resource
 
    int x;
    std::cout << "Enter an integer: ";
    std::cin >> x;
 
    if (x == 0)
        return; // 这里提前返回
 
    // 对 ptr 做一些操作
    ptr->sayHi();
}

int main()
{
    someFunction();

    return 0;
}
```

如果用户输入非零整数，则上述程序将打印:

```C++
Resource acquired
Hi!
Resource destroyed
```

如果用户输入零，上述程序将提前终止，打印:

```C++
Resource acquired
Resource destroyed
```

请注意，即使在用户输入零并且函数提前终止的情况下，资源仍然被正确地释放。

由于变量ptr是局部变量，因此当函数终止时，ptr将被销毁（无论它如何终止）。由于Auto_ptr1析构函数将清理资源，因此我们可以确保资源将被正确清理。

***
## 一个关键的缺陷

Auto_ptr1类在某些自动生成的代码背后潜伏着一个严重缺陷。在进一步阅读之前，请思考您是否可以识别它是什么？

（提示:考虑如果不提供类的哪些部分将自动生成）

（危险的音乐）

好了，时间到了。

考虑以下程序:

```C++
#include <iostream>

// 和上面一样
template <typename T>
class Auto_ptr1
{
	T* m_ptr {};
public:
	Auto_ptr1(T* ptr=nullptr)
		:m_ptr(ptr)
	{
	}
	
	~Auto_ptr1()
	{
		delete m_ptr;
	}

	T& operator*() const { return *m_ptr; }
	T* operator->() const { return m_ptr; }
};

class Resource
{
public:
	Resource() { std::cout << "Resource acquired\n"; }
	~Resource() { std::cout << "Resource destroyed\n"; }
};

int main()
{
	Auto_ptr1<Resource> res1(new Resource());
	Auto_ptr1<Resource> res2(res1);

	return 0;
}
```

该程序打印:

```C++
Resource acquired
Resource destroyed
Resource destroyed
```

此时，您的程序很可能（但不一定）崩溃。现在看到问题了吗？由于没有提供拷贝构造函数或赋值运算符，C++为我们提供了默认的实现。它提供的函数进行浅拷贝。因此，当用res1初始化res2时，两个Auto_ptr1变量都指向同一个资源。当res2超出作用域时，它删除资源，使res1具有悬空指针。当res1删除其（已删除）资源时，将导致未定义的行为（可能是崩溃）！

对于这样的函数，您会遇到类似的问题:

```C++
void passByValue(Auto_ptr1<Resource> res)
{
}

int main()
{
	Auto_ptr1<Resource> res1(new Resource());
	passByValue(res1);

	return 0;
}
```

在该程序中，res1将按值复制到参数res中，因此res1.m_ptr和res.m_ptr将保持相同的地址。

当在函数末尾销毁res时，res1.m_ptr处于悬空状态。稍后删除res1.m_ptr时，将产生未定义的行为。

很明显，这并不好。我们如何解决这个问题？

嗯，我们可以做的一件事是显式删除拷贝构造函数和赋值运算符，从而防止进行任何复制。这将防止按值传递情况（这很好，我们可能无论如何都不应该按值传递这些）。

但是，我们如何将函数中的Auto_ptr1返回给调用者呢？

```C++
??? generateResource()
{
     Resource* r{ new Resource() };
     return Auto_ptr1(r);
}
```

我们不能通过引用返回Auto_ptr1，因为局部的Auto_ptrl将在函数结束时被销毁，调用方将保留一个悬空引用。或者直接返回Resource*，但稍后可能会忘记删除这个指针。但这样就完全没有使用到智能指针的各种好处。按值返回Auto_ptr1是我们需要的能力——但最终会出现浅拷贝、重复指针和崩溃。

另一种选择是重载拷贝构造函数和赋值运算符以进行深拷贝。这样，至少可以避免重复指向同一对象的指针。但复制可能代价高昂（并且可能不理想，甚至不可能），并且我们不想仅仅为了从函数返回Auto_ptr1而为对象进行不必要的复制。再加上分配或初始化原始的指针不会复制所指向的对象，那么为什么我们希望智能指针的行为不同呢？

我们该怎么办？

***
## 移动语义（Move semantics）

如果我们不是让拷贝构造函数和赋值操作符复制指针（“复制语义”），而是将指针的所有权从源对象转移/移动到目标对象，该怎么样？这是移动语义背后的核心思想。移动语义意味着类将转移对象的所有权，而不是制作副本。

让我们更新Auto_ptr1类，以显示如何完成此操作:

```C++
#include <iostream>

template <typename T>
class Auto_ptr2
{
	T* m_ptr {};
public:
	Auto_ptr2(T* ptr=nullptr)
		:m_ptr(ptr)
	{
	}
	
	~Auto_ptr2()
	{
		delete m_ptr;
	}

	// 实现移动语义的拷贝构造函数
	Auto_ptr2(Auto_ptr2& a) // 注: 非 const
	{
		// 不需要删除 m_ptr.  构造函数只有在对象创建时调用，m_ptr不可能被赋值过
		m_ptr = a.m_ptr; // 将内部指针的所有权转移到当前对象
		a.m_ptr = nullptr; // 确保源对象，不再拥有指针
	}
	
	// 实现移动语义的赋值运算符
	Auto_ptr2& operator=(Auto_ptr2& a) // 注: 非 const
	{
		if (&a == this)
			return *this;

		delete m_ptr; // 释放之前已经持有的指针
		m_ptr = a.m_ptr; // 将内部指针的所有权转移到当前对象
		a.m_ptr = nullptr; // 确保源对象，不再拥有指针
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

int main()
{
	Auto_ptr2<Resource> res1(new Resource());
	Auto_ptr2<Resource> res2; // 以 nullptr 初始化

	std::cout << "res1 is " << (res1.isNull() ? "null\n" : "not null\n");
	std::cout << "res2 is " << (res2.isNull() ? "null\n" : "not null\n");

	res2 = res1; // res2 获得所有权, res1 被设置为 null

	std::cout << "Ownership transferred\n";

	std::cout << "res1 is " << (res1.isNull() ? "null\n" : "not null\n");
	std::cout << "res2 is " << (res2.isNull() ? "null\n" : "not null\n");

	return 0;
}
```

该程序打印:

```C++
Resource acquired
res1 is not null
res2 is null
Ownership transferred
res1 is null
res2 is not null
Resource destroyed
```

注意，我们的重载 “operator=” 将m_ptr的所有权从res1赋予res2！因此，我们不会造成指针的重复副本，并且一切都会被整洁地清理干净。

***
## std::auto_ptr，以及为什么这是一个坏方案

现在是讨论std::auto_ptr的适当时机。在C++98中引入并在C++17中删除的std::auto_ptr是C++对标准化智能指针的首次尝试。std::auto_ptr选择像auto_ptr2类那样实现移动语义。

然而，std::auto_ptr（和我们的auto_ptr2类）有许多问题，使得使用它变得危险。

首先，由于std::auto_ptr通过拷贝构造函数和赋值操作符实现移动语义，因此通过值将std::auto_ptr传递给函数将导致资源移动到函数参数（并在函数参数超出作用域时在函数末尾被销毁）。然后，当您从调用方访问auto_ptr变量时（没有意识到它已被移动和删除），您突然开始解引用空指针！

其次，std::auto_ptr总是使用非数组删除来删除其内容。这意味着auto_ptr不能正确地处理动态分配的数组，因为它使用了错误的释放方式。更糟糕的是，它不会阻止您向它传递数组，然后它会错误地管理该数组，从而导致内存泄漏。

最后，auto_ptr不能很好地处理标准库中的许多其他类，包括大多数容器和算法。发生这种情况是因为这些标准库类假设在复制项时，实际上是进行复制，而不是移动。

由于上述缺点，在C++11中不推荐使用std::auto_ptr，在C++17中删除了它。

***
## 再进一步

std::auto_ptr设计的核心问题是，在C++11之前，C++语言根本没有区分“复制语义”和“移动语义”的机制。覆盖复制语义来实现移动语义会导致奇怪的边缘情况和意外的错误。例如，您可以编写 res1 = res2 ，但不知道res2是否将被更改！

正因为如此，在C++11中，“移动”的概念被正式定义，并在语言中添加了“移动语义”，以正确区分复制和移动。既然我们已经知道移动语义为何是有用的，那么我们将在本章的其余部分探索移动语义的主题。我们还将使用移动语义修复Auto_ptr2类。

在C++11中，std::auto_ptr已被一系列其他类型的“移动感知”智能指针取代: std::unique_ptr、std::weak_ptr和std:∶shared_ptr。我们还将研究其中最流行的两个: unique_ptr（它是auto_ptr的直接替代品）和shared_ptr。

{{< alert success >}}
**一个提醒**

delete nullptr是可以的，因为它什么也不做。

{{< /alert >}}

***

{{< prevnext prev="/basic/chapter21/summary/" next="/basic/chapter22/r-value-ref/" >}}
21.14 第21章总结
<--->
22.1 右值引用
{{< /prevnext >}}
