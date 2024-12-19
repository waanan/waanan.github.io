---
title: "override和final说明符"
date: 2024-11-04T13:14:53+08:00
---

为了解决继承的一些常见挑战，C++有两个与继承相关的标识符：override和final。请注意，这些标识符不是关键字——它们是普通单词，只有在特定语境中使用时才具有特殊含义。C++标准称它们为“具有特殊含义的标识符”，但它们通常被称为“说明符”。

final的使用不多，但override是一个非常棒的功能，你应该经常使用。在本课中，我们将研究这两种情况，以及虚函数重载返回类型必须匹配规则的一个例外。

***
## override说明符

正如我们在上一课中提到的，只有当派生类虚函数的签名和返回类型与基类函数完全匹配时，它才被视为重载。这可能会导致无意中的问题，即原本期望作为重载的函数实际上不是。

考虑以下示例：

```C++
#include <iostream>
#include <string_view>

class A
{
public:
	virtual std::string_view getName1(int x) { return "A"; }
	virtual std::string_view getName2(int x) { return "A"; }
};

class B : public A
{
public:
	virtual std::string_view getName1(short x) { return "B"; } // 注: 参数是 short
	virtual std::string_view getName2(int x) const { return "B"; } // 注: 函数是 const
};

int main()
{
	B b{};
	A& rBase{ b };
	std::cout << rBase.getName1(1) << '\n';
	std::cout << rBase.getName2(2) << '\n';

	return 0;
}
```

因为rBase是对B对象的A引用，所以这里的目的是使用虚函数来访问B::getName1()和B::get Name2()。但是，由于B::getName1()采用不同的参数（short而不是int），因此它不被视为A::getName1()的重载。更阴险的是，因为B::getName2()是const，而A::getName2()不是const，所以B::getName2()不被视为A::getName2()的重载。

因此，该程序打印：

```C++
A
A
```

在这种特殊情况下，因为我们打印了A和B，所以很容易看出我们把重载搞砸了，调用了错误的虚函数。然而，在更复杂的程序中，函数的行为或返回值没有打印出来，这些问题可能很难调试。

为了帮助解决那些应该被重载但实际上没有被重载的问题，可以通过将override说明符放在函数签名之后（函数 const 说明符放在同一个位置）。

如果函数没有重写基类函数（或应用于非虚函数），编译器将把该函数标记为错误。

```C++
#include <string_view>

class A
{
public:
	virtual std::string_view getName1(int x) { return "A"; }
	virtual std::string_view getName2(int x) { return "A"; }
	virtual std::string_view getName3(int x) { return "A"; }
};

class B : public A
{
public:
	std::string_view getName1(short int x) override { return "B"; } // 编译失败, 这个函数不是一个重载
	std::string_view getName2(int x) const override { return "B"; } // 编译失败, 这个函数不是一个重载
	std::string_view getName3(int x) override { return "B"; } // okay, 是 A::getName3(int) 的重载

};

int main()
{
	return 0;
}
```

上面的程序产生了两个编译错误：一个是B::getName1()，一个是B::getName2()，因为两者都没有覆盖A的函数。B::getName3()确实覆盖了A::getName2()，因此该行不会产生编译错误。

使用override说明符不会带来性能损失，而且它有助于确保您确实重载了您认为应该重载的函数，所以所有虚函数都应该使用override说明符进行标记。此外，由于override说明符意味着virtual，因此不需要使用override说明符和virtual关键字同时标记函数。

{{< alert success >}}
**最佳实践**

在基类中的虚函数上使用virtual关键字。

在派生类中的重载函数上使用override说明符（但不要使用virtual关键字）。这包括虚析构函数。

{{< /alert >}}

***
## final说明符

在某些情况下，您可能不希望有人能够重写虚拟函数或从类继承。最后一个说明符可用于告诉编译器强制执行此操作。如果用户试图重写一个函数或从指定为final的类继承，编译器将给出编译错误。

在我们想限制用户重写函数的情况下，最后一个说明符与重写说明符在同一个地方使用，如下所示：

```C++
#include <string_view>

class A
{
public:
	virtual std::string_view getName() const { return "A"; }
};

class B : public A
{
public:
	// note use of final specifier on following line -- that makes this function not able to be overridden in derived classes
	std::string_view getName() const override final { return "B"; } // okay, overrides A::getName()
};

class C : public B
{
public:
	std::string_view getName() const override { return "C"; } // compile error: overrides B::getName(), which is final
};
```

在上面的代码中，B:：getName（）重写了A:：getName（），这很好。但是B:：getName（）有最后一个说明符，这意味着对该函数的任何进一步重写都应被视为错误。事实上，C:：getName（）试图重写B:：getName（）（这里的重写说明符不相关，只是为了良好实践），所以编译器会给出编译错误。

如果我们想阻止从类继承，则在类名后应用最后一个说明符：

```C++
#include <string_view>

class A
{
public:
	virtual std::string_view getName() const { return "A"; }
};

class B final : public A // note use of final specifier here
{
public:
	std::string_view getName() const override { return "B"; }
};

class C : public B // compile error: cannot inherit from final class
{
public:
	std::string_view getName() const override { return "C"; }
};
```

在上面的例子中，类B被声明为final。因此，当C试图从B继承时，编译器将给出编译错误。

***
## 协变返回类型

有一种特殊情况，派生类虚函数重写可以具有与基类不同的返回类型，但仍被视为匹配的重写。如果虚拟函数的返回类型是指针或对某个类的引用，则重写函数可以返回对派生类的指针或引用。这些被称为协变返回类型。以下是一个示例：

```C++
#include <iostream>
#include <string_view>

class Base
{
public:
	// This version of getThis() returns a pointer to a Base class
	virtual Base* getThis() { std::cout << "called Base::getThis()\n"; return this; }
	void printType() { std::cout << "returned a Base\n"; }
};

class Derived : public Base
{
public:
	// Normally override functions have to return objects of the same type as the base function
	// However, because Derived is derived from Base, it's okay to return Derived* instead of Base*
	Derived* getThis() override { std::cout << "called Derived::getThis()\n";  return this; }
	void printType() { std::cout << "returned a Derived\n"; }
};

int main()
{
	Derived d{};
	Base* b{ &d };
	d.getThis()->printType(); // calls Derived::getThis(), returns a Derived*, calls Derived::printType
	b->getThis()->printType(); // calls Derived::getThis(), returns a Base*, calls Base::printType

	return 0;
}
```

This prints:

```C++
called Derived::getThis()
returned a Derived
called Derived::getThis()
returned a Base
```

关于协变返回类型的一个有趣的注意事项：C++不能动态选择类型，所以你总是会得到与被调用函数的实际版本匹配的类型。

在上面的例子中，我们首先调用d.getThis（）。由于d是Derived，因此调用Derived:：getThis（），它返回Derived*。然后，这个Derive*用于调用非虚函数Derived:：printType（）。

现在是一个有趣的案例。然后我们调用b->getThis（）。变量b是一个指向派生对象的基指针。Base:：getThis（）是一个虚函数，因此它调用Derive:：getThis（）。虽然Derived:：getThis（）返回Derived*，但由于该函数的Base版本返回Base*，因此返回的Derived*s被向上转换为Base*。因为Base:：printType（）是非虚的，所以调用了Base:：print Type（）。

换句话说，在上面的例子中，只有当你首先使用一个类型为Derived对象的对象调用getThis（）时，你才会得到Derived*。

请注意，如果printType（）是虚拟的而不是非虚拟的，那么b->getThis（）（Base*类型的对象）的结果将经历虚拟函数解析，并且Derived:：printType（。

协方差返回类型通常用于虚拟成员函数返回指向包含该成员函数的类的指针或引用的情况（例如，Base:：getThis（）返回Base*，Derive:：getThiss（）返回Derive*）。然而，这并不是绝对必要的。协方差返回类型可用于重写成员函数的返回类型从基虚成员函数的回报类型派生的任何情况。

***
