---
title: "std::shared_ptr的循环依赖性问题和std::weak_ptr"
date: 2024-08-23T14:54:42+08:00
---

在上一课中，我们看到了std::shared_ptr允许多个智能指针共同拥有相同的资源。然而，在某些情况下，这可能会成为问题。考虑以下情况，其中两个单独对象中的std::shared_ptr都指向另一个对象：

```C++
#include <iostream>
#include <memory> // for std::shared_ptr
#include <string>

class Person
{
	std::string m_name;
	std::shared_ptr<Person> m_partner; // 初始化为空

public:
		
	Person(const std::string &name): m_name(name)
	{ 
		std::cout << m_name << " created\n";
	}
	~Person()
	{
		std::cout << m_name << " destroyed\n";
	}

	friend bool partnerUp(std::shared_ptr<Person> &p1, std::shared_ptr<Person> &p2)
	{
		if (!p1 || !p2)
			return false;

		p1->m_partner = p2;
		p2->m_partner = p1;

		std::cout << p1->m_name << " is now partnered with " << p2->m_name << '\n';

		return true;
	}
};

int main()
{
	auto lucy { std::make_shared<Person>("Lucy") }; // 创建 Person  "Lucy"
	auto ricky { std::make_shared<Person>("Ricky") }; // 创建 Person "Ricky"

	partnerUp(lucy, ricky); // 让 "Lucy" 指向 "Ricky" 同时 "Ricky" 指向 "Lucy" 

	return 0;
}
```

在上面的示例中，使用 make_shared() 动态分配两个Person，“Lucy”和“Ricky”（以期望Lucy和Ricky在main()末尾被销毁）。然后让他们互相指向。这会将“Lucy”中的std::shared_ptr设置为指向“Ricky”，并将“Ricky'”中的std::shared_ptr设置为“Lucy”。

然而，该程序没有按预期执行：

```C++
Lucy created
Ricky created
Lucy is now partnered with Ricky
```

哦哦。发生了什么事？

在调用partnerUp()后，有两个指向“Ricky”（ricky变量和lucy的m_partner）的shared_ptr，以及两个指向”Lucy”（lucy变量和ricky的m_partner）。

在main()的末尾，ricky首先超出作用域。当这种情况发生时，ricky检查是否有任何其他共享指针共同拥有Person “Ricky”。有（lucy的m_partner）。因此，它不会释放“Ricky”（如果释放了，则lucy的m_partner将最终成为悬空指针）。在这时，有一个指向“Ricky”（lucy的m_partner）的shared_ptr和两个指向“Lucy”（lucy变量和ricky的m_partner）的shared_ptr。

接下来，lucy超出作用域，并且发生了相同的事情。lucy检查是否存在共同拥有Person “lucy”的任何其它shared_ptr。有（ricky的m_partner），因此“Lucy”未被释放。在这时，有一个指向“Lucy”（ricky的m_partner）的shared_ptr和一个指向”Ricky“（lucy的m_partner）的shared_ptr。

然后程序结束——“Lucy”或“Ricky”都没有被释放！本质上，“Lucy”最终使“Ricky”不被摧毁，而“Ricky'”最终使”Lucy“不被摧毁。

事实证明，这种情况可以在形成循环引用的任何共享指针中发生。

***
## 循环引用

循环引用是一系列引用，其中每个对象引用下一个对象，最后一个对象引用回第一个对象，从而导致引用循环。

在shared_ptr的上下文中，引用的含义是shared_ptr。

这正是我们在上面的例子中看到的：“Lucy”指向“Ricky”，“Ricky”指向“Lucy”。有了三个指针，当A指向B，B指向C，C指向A时，你也会得到相同的结果。共享指针形成一个循环的实际效果是，每个对象最终都保持下一个对象的存活——最后一个对象保持第一个对象的存活。因此，序列中的任何对象都不能被释放，因为它们都认为其他对象仍然需要它！

***
## 另一个案例

事实证明，这种循环引用问题甚至可以在单个std::shared_ptr中发生——引用包含自身的std::shared_ptr是一个循环引用。尽管在实践中不太可能发生这种情况，但能给您更多的理解：

```C++
#include <iostream>
#include <memory> // for std::shared_ptr

class Resource
{
public:
	std::shared_ptr<Resource> m_ptr {}; // 初始化为空
	
	Resource() { std::cout << "Resource acquired\n"; }
	~Resource() { std::cout << "Resource destroyed\n"; }
};

int main()
{
	auto ptr1 { std::make_shared<Resource>() };

	ptr1->m_ptr = ptr1; // m_ptr 现在指向被管理的对象自身

	return 0;
}
```

在上面的示例中，当ptr1超出作用域时，不会释放资源，因为m_ptr正在共享资源。此时，释放资源的唯一方法是将m_ptr设置为其他值（因此不再共享资源）。但已不能访问m_ptr，因为ptr1超出作用域，所以不再有办法这样做。资源已造成内存泄漏。

因此，程序打印：

```C++
Resource acquired
```

***
## 那么，std::weak_ptr到底是什么？

std::weak_ptr旨在解决上面描述的“循环引用”问题。std::weak_ptr是一个观察者——它可以观察和访问与std:∶shared_ptr（或其他std::weak_ptrs）所指向的对象，但它不被视为所有者。记住，当std:∶shared_ptr超出作用域时，它只考虑其他std:∶shared_ptr是否共同拥有该对象。std::weak_ptr不被考虑！

让我们使用std::weak_ptr解决上面的问题：

```C++
#include <iostream>
#include <memory> // for std::shared_ptr and std::weak_ptr
#include <string>

class Person
{
	std::string m_name;
	std::weak_ptr<Person> m_partner; // 注: 这里现在是 std::weak_ptr

public:
		
	Person(const std::string &name): m_name(name)
	{ 
		std::cout << m_name << " created\n";
	}
	~Person()
	{
		std::cout << m_name << " destroyed\n";
	}

	friend bool partnerUp(std::shared_ptr<Person> &p1, std::shared_ptr<Person> &p2)
	{
		if (!p1 || !p2)
			return false;

		p1->m_partner = p2;
		p2->m_partner = p1;

		std::cout << p1->m_name << " is now partnered with " << p2->m_name << '\n';

		return true;
	}
};

int main()
{
	auto lucy { std::make_shared<Person>("Lucy") };
	auto ricky { std::make_shared<Person>("Ricky") };

	partnerUp(lucy, ricky);

	return 0;
}
```

此代码行为正常：

```C++
Lucy created
Ricky created
Lucy is now partnered with Ricky
Ricky destroyed
Lucy destroyed
```

在代码上，它与有问题的示例几乎相同。然而，现在当ricky超出作用域时，它看到没有其他指向“Ricky”的std::shared_ptr（“Lucy”中的std::weak_ptr不计算）。因此，它将释放“Ricky”。lucy也是如此。

***
## 使用std::weak_ptr

std::weak_ptr的一个缺点是，std::weak_ptr不能直接使用（它们没有 operator->）。要使用std::weak_ptr，必须首先将其转换为std::shared_ptr。然后可以使用std::shared_ptr。要将std::weak_ptr转换为std::shared_ptr，可以使用lock()成员函数。下面是上面的示例，以展示这一点：

```C++
#include <iostream>
#include <memory> // for std::shared_ptr and std::weak_ptr
#include <string>

class Person
{
	std::string m_name;
	std::weak_ptr<Person> m_partner; // 注：这里现在是 std::weak_ptr

public:

	Person(const std::string &name) : m_name(name)
	{
		std::cout << m_name << " created\n";
	}
	~Person()
	{
		std::cout << m_name << " destroyed\n";
	}

	friend bool partnerUp(std::shared_ptr<Person> &p1, std::shared_ptr<Person> &p2)
	{
		if (!p1 || !p2)
			return false;

		p1->m_partner = p2;
		p2->m_partner = p1;

		std::cout << p1->m_name << " is now partnered with " << p2->m_name << '\n';

		return true;
	}

	std::shared_ptr<Person> getPartner() const { return m_partner.lock(); } // 使用 lock() 将 weak_ptr 转换成 shared_ptr
	const std::string& getName() const { return m_name; }
};

int main()
{
	auto lucy { std::make_shared<Person>("Lucy") };
	auto ricky { std::make_shared<Person>("Ricky") };

	partnerUp(lucy, ricky);

	auto partner = ricky->getPartner(); // 获取 Ricky 的 partner 的 shared_ptr
	std::cout << ricky->getName() << " partner is: " << partner->getName() << '\n';

	return 0;
}
```

这将打印：

```C++
Lucy created
Ricky created
Lucy is now partnered with Ricky
Ricky partner is: Lucy
Ricky destroyed
Lucy destroyed
```

不必担心std::shared_ptr变量partner的循环依赖，因为它只是函数内部的局部变量。它最终将在函数结束时超出作用域，引用计数将减少为0。

***
## 使用std::weak_ptr避免悬空指针

考虑这样的情况，一个普通的原始指针保存着某个对象的地址，然后该对象被销毁。这样的指针是悬空的，解指针的引用将导致未定义的行为。不幸的是，没有办法确定持有非空地址的指针是否悬空。这是原始指针危险的很大一部分原因。

由于std::weak_ptr不会使所拥有的资源保持存活，因此std::weak_ptr也有类似的可能，它仍然指向已由std::shared_ptr释放的资源。然而，std::weak_ptr有一个巧妙的技巧——因为它可以访问对象的引用计数，所以它可以确定它是否指向有效的对象！如果引用计数不为零，则资源仍然有效。如果引用计数为零，则资源已被销毁。

测试std::weak_ptr是否有效的最简单方法是使用expired()成员函数，如果std::weak_ptr指向无效对象，则返回true，否则返回false。

下面是一个简单的例子，展示了这种行为差异：

```C++
#include <iostream>
#include <memory>

class Resource
{
public:
	Resource() { std::cerr << "Resource acquired\n"; }
	~Resource() { std::cerr << "Resource destroyed\n"; }
};

// 返回无效对象的 std::weak_ptr
std::weak_ptr<Resource> getWeakPtr()
{
	auto ptr{ std::make_shared<Resource>() };
	return std::weak_ptr<Resource>{ ptr };
} // ptr 超出作用域, 资源销毁

// 返回无效对象的原始指针
Resource* getDumbPtr()
{
	auto ptr{ std::make_unique<Resource>() };
	return ptr.get();
} // ptr 超出作用域, 资源销毁

int main()
{
	auto dumb{ getDumbPtr() };
	std::cout << "Our dumb ptr is: " << ((dumb == nullptr) ? "nullptr\n" : "non-null\n");

	auto weak{ getWeakPtr() };
	std::cout << "Our weak ptr is: " << ((weak.expired()) ? "expired\n" : "valid\n");

	return 0;
}
```

这将打印：

```C++
Resource acquired
Resource destroyed
Our dumb ptr is: non-null
Resource acquired
Resource destroyed
Our weak ptr is: expired
```

当getDumbPtr()返回Resource*时，它返回一个悬空指针（因为std::unique_ptr在函数末尾销毁了Resource）。当getWeakPtr()返回std::weak_ptr时，该std::weak_ptr类似地指向无效对象（因为std:∶shared_ptr在函数末尾销毁了资源）。

在main()中，我们首先测试返回的原始指针是否为nullptr。由于原始指针仍然保存已释放资源的地址，因此该测试失败。main() 无法判断该指针是否悬空。在这种情况下，因为它是一个悬空指针，所以如果解引用该指针，将导致未定义的行为。

接下来，测试weak.expired()是否为真。由于weak指向的对象的引用计数为0（因为所指向的对象已被销毁），因此结果为true。因此，main()中的代码可以判断weak_ptr指向的是无效对象，并且我们可以根据需要对代码进行条件处理！

请注意，如果std::weak_ptr失效，则不应对其调用lock()，因为所指向的对象已经被销毁，因此没有要共享的对象。如果对失效的std::weak_ptr调用lock()，它将返回指向nullptr的std::shared_ptr。

***
## 结论

当您需要多个可以共同拥有资源的智能指针时，可以使用std::sharedptr。当最后一个std::shared_ptr超出作用域时，将释放资源。当您希望智能指针可以查看和使用共享资源，但不参与该资源的所有权时，可以使用std::weakptr。

***
