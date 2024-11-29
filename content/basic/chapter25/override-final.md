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

因为rBase是对B对象的A引用，所以这里的目的是使用虚函数来访问B::getName1()和B::get Name2()。但是，由于B::getName1()采用不同的参数（short而不是int），因此它不被视为A::getName1()的重载。更阴险的是，因为B::getName2()是const，而A::getName2()不是常量，所以B::getName2()不被视为A::getName2()的重载。

因此，该程序打印：

```C++
A
A
```

在这种特殊情况下，因为A和B只是打印它们的名字，所以很容易看出我们把重载搞砸了，并且调用了错误的虚函数。然而，在更复杂的程序中，函数的行为或返回值没有打印出来，这些问题可能很难调试。

为了帮助解决那些应该被重载但实际上没有的问题，可以通过将重写说明符放在函数签名之后（函数级常量说明符放在同一个位置），将重写说明符应用于任何虚拟函数。

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
	std::string_view getName1(short int x) override { return "B"; } // compile error, function is not an override
	std::string_view getName2(int x) const override { return "B"; } // compile error, function is not an override
	std::string_view getName3(int x) override { return "B"; } // okay, function is an override of A::getName3(int)

};

int main()
{
	return 0;
}
```

上面的程序产生了两个编译错误：一个是B:：getName1（），一个是B：：getName2（），因为两者都没有覆盖前面的函数。B： ：getName3（）确实覆盖了A:：getName2（），因此该行不会产生错误。

因为使用覆盖说明符不会带来性能损失，而且它有助于确保您确实覆盖了您认为拥有的函数，所以所有虚拟覆盖函数都应该使用覆盖说明符进行标记。此外，由于覆盖说明符意味着virtual，因此不需要使用覆盖说明符和virtual关键字标记函数。

{{< alert success >}}
**最佳实践**

在基类中的虚函数上使用virtual关键字。

在派生类中的重写函数上使用重写说明符（但不要使用virtual关键字）。这包括虚拟析构函数。


{{< /alert >}}

