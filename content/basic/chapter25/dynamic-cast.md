---
title: "dynamic_cast"
date: 2024-11-04T13:14:53+08:00
---

在前面显式类型转换中，我们研究了如何使用static_cast将变量从一种类型转换为另一种类型。

在本课程中，我们将继续研究另一种类型的强制转换：dynamic_cast。

***
## 为什么需要dynamic_cast

在处理多态性时，您经常会遇到这样的情况，即您有一个指向基类的指针，但您希望访问仅存在于派生类中的一些信息。

考虑下面的（稍微有点做作的）程序：

```C++
#include <iostream>
#include <string>
#include <string_view>

class Base
{
protected:
	int m_value{};

public:
	Base(int value)
		: m_value{value}
	{
	}

	virtual ~Base() = default;
};

class Derived : public Base
{
protected:
	std::string m_name{};

public:
	Derived(int value, std::string_view name)
		: Base{value}, m_name{name}
	{
	}

	const std::string& getName() const { return m_name; }
};

Base* getObject(bool returnDerived)
{
	if (returnDerived)
		return new Derived{1, "Apple"};
	else
		return new Base{2};
}

int main()
{
	Base* b{ getObject(true) };

	// 只有Base指针，如何获得Derived 对象的 m_name？

	delete b;

	return 0;
}
```

在该程序中，函数getObject()始终返回Base指针，但该指针可以指向Base或Derived对象。在Base指针实际指向Derived对象的情况下，如何调用Derived::getName()？

一种方法是将一个名为getName()的虚函数添加到Base中（因此我们可以使用Base指针/引用调用它，并将其动态解析为Derived::getName()）。但如果使用实际指向Base对象的Base指针/引用调用它，该函数将返回什么？没有任何真正有意义的结果。而且，仅由派生类关注的东西污染了我们的基类。

我们知道C++隐式地允许您将Derived指针转换为Base指针（实际上，getObject()就是这样做的）。该过程有时称为类型向上转换。如果有一种方法可以将Base指针转换回Derived指针，我们就可以使用该指针直接调用Derived::getName()，而根本不必使用虚函数解析。

***
## dynamic_cast

C++提供了一个名为dynamic_cast的转换操作符，可以用于此目的。尽管dynamic_cast具有一些不同的功能，但到目前为止，最常见的用途是将基类指针转换为派生类指针。这个过程被称为向下转换。

使用dynamic_cast就像static_cast一样。下面是对应上面的示例

```C++
int main()
{
	Base* b{ getObject(true) };

	Derived* d{ dynamic_cast<Derived*>(b) }; // 使用 dynamic cast 将 Base 指针转换为 Derived 指针

	std::cout << "The name of the Derived is: " << d->getName() << '\n';

	delete b;

	return 0;
}
```

这会打印：

```C++
The name of the Derived is: Apple
```

***
## dynamic_cast失败的情况

上面的示例之所以有效，是因为b实际上指向Derived对象，因此将b转换为Derived指针是可以的。然而，我们做了一个相当危险的假设：b一定指向Derived对象。如果b没有指向Derived对象怎么办？通过将参数从true更改为false可以来轻松测试到。在这种情况下，getObject()将返回指向Base对象的指针。当我们试图将其dynamic_cast为Derived时，它将失败，因为无法进行转换。

如果dynamic_cast失败，转换的结果将是空指针。

如果我们没有检查返回空指针的结果，直接访问d->getName()，它将尝试解引用空指针，导致未定义的行为（可能是崩溃）。

为了使该程序安全，我们需要确保dynamic_cast的结果实际成功：

```C++
int main()
{
	Base* b{ getObject(true) };

	Derived* d{ dynamic_cast<Derived*>(b) }; // 使用 dynamic cast 将 Base 指针转换为 Derived 指针

	if (d) // 确保 d 不是空指针
		std::cout << "The name of the Derived is: " << d->getName() << '\n';

	delete b;

	return 0;
}
```

{{< alert success >}}
**提示**

通过检查空指针结果，来确保dynamic_cast实际成功。

{{< /alert >}}

请注意，由于dynamic_cast在运行时执行一些一致性检查（以确保可以进行转换），因此使用dynamic_cast会导致一些性能损失。

还要注意，在一些情况下，使用dynamic_cast进行向下转换将不起作用：

1. 使用protected 或者 private 继承。
2. 对于不声明或继承任何虚拟函数（因此没有虚函数表）的类。
3. 在涉及虚拟基类的某些情况下（请参阅本页以获取其中一些情况的示例，以及如何解决它们）。

***
## 使用static_cast进行向下转换

向下转换也可以使用static_cast完成。主要区别是static_cast不进行运行时类型检查。这使得使用static_cast更快，但更危险。它将Base\*强制转换为Derived\*，即使Base指针未指向Derived对象，它也将“成功”。当您尝试访问生成的Derived指针（它实际上指向Base对象）时，这将导致未定义的行为。

如果您绝对确信正在向下转换的指针将成功转换，那么使用static_cast是可以接受的。知道所指向的对象类型的一种方法是使用虚函数，这里有一种（不是很好的）方法：

```C++
#include <iostream>
#include <string>
#include <string_view>

// 类型定义
enum class ClassID
{
	base,
	derived
	// 其它以后会添加的类
};

class Base
{
protected:
	int m_value{};

public:
	Base(int value)
		: m_value{value}
	{
	}

	virtual ~Base() = default;
	virtual ClassID getClassID() const { return ClassID::base; }
};

class Derived : public Base
{
protected:
	std::string m_name{};

public:
	Derived(int value, std::string_view name)
		: Base{value}, m_name{name}
	{
	}

	const std::string& getName() const { return m_name; }
	ClassID getClassID() const override { return ClassID::derived; }

};

Base* getObject(bool bReturnDerived)
{
	if (bReturnDerived)
		return new Derived{1, "Apple"};
	else
		return new Base{2};
}

int main()
{
	Base* b{ getObject(true) };

	if (b->getClassID() == ClassID::derived)
	{
		// 我们确信 b 指向 Derived 对象, 所以下面的转换是一定会成功的
		Derived* d{ static_cast<Derived*>(b) };
		std::cout << "The name of the Derived is: " << d->getName() << '\n';
	}

	delete b;

	return 0;
}
```

但如果您要经历所有的困难来实现这一点（并支付调用虚拟函数和处理结果的成本），那么您最好只使用dynamic_cast。

还要考虑一下，如果我们的对象实际上是从derived派生的某个类（让我们称之为D2），会发生什么情况。上面的检查b->getClassID() == ClassID::derived将失败，因为getClassID()将返回ClassID::D2，它不等于ClassID::derived。然而，将D2 dynamic_cast转为Derived可以成功，因为D2是更下层派生的！

***
## dynamic_cast和引用

尽管上述所有示例都显示了指针的dynamic_cast（这更常见），但dynamic_cast也可以与引用一起使用。这类似于dynamic_cast如何处理指针

```C++
#include <iostream>
#include <string>
#include <string_view>

class Base
{
protected:
	int m_value;

public:
	Base(int value)
		: m_value{value}
	{
	}

	virtual ~Base() = default;
};

class Derived : public Base
{
protected:
	std::string m_name;

public:
	Derived(int value, std::string_view name)
		: Base{value}, m_name{name}
	{
	}

	const std::string& getName() const { return m_name; }
};

int main()
{
	Derived apple{1, "Apple"}; // 创建 Derived apple
	Base& b{ apple }; // 将 base 引用到 apple
	Derived& d{ dynamic_cast<Derived&>(b) }; // dynamic cast 引用，而不是指针

	std::cout << "The name of the Derived is: " << d.getName() << '\n'; // 可以通过 d 访问到 Derived::getName

	return 0;
}
```

由于C++没有“空引用”，因此dynamic_cast在失败时不能返回空引用。相反，如果操作引用的dynamic_cast失败，则抛出类型为std::bad_cast的异常。在本教程的后面部分中，我们将讨论异常。

***
## dynamic_cast与static_cast

新程序员有时会对何时使用static_cast与dynamic_cast感到困惑。答案很简单：使用static_cast，除非是类型向下转换，在这种情况下，dynamic_cast通常是更好的选择。然而，您还应该考虑完全避免强制转换，只使用虚函数。

***
## 向下转换 vs 虚函数

有些开发人员认为dynamic_cast是邪恶的，并且表示糟糕的类设计。这些程序员说应该使用虚函数。

通常，应优先使用虚函数而不是类型向下转换。然而，有时向下转换是更好的选择：

1. 当您不能修改基类以添加虚函数时（例如，因为基类是标准库的一部分）
2. 当您需要访问特定于派生类的内容（例如，仅存在于派生类中的访问函数）
3. 当将虚函数添加到基类中没有意义时（例如基类没有适当的返回值）如果不需要实例化基类，则在这里可以选择使用纯虚函数。

***
## 关于dynamic_cast和RTTI

运行时类型信息（RTTI，run-time type information）是C++的一项功能，它在运行时暴露有关对象数据类型的信息。dynamic_cast利用了此功能。由于RTTI具有相当大的空间性能开销，因此一些编译器允许您将RTTI关闭。当然，如果这样做，dynamic_cast将无法正常工作。

***