---
title: "使用友元函数重载算术运算符"
date: 2024-08-20T12:01:51+08:00
---

C++中最常用的一些运算符是算术运算符——即加号运算符（+）、减号运算符（-）、乘法运算符（*）和除法运算符（/）。注意，所有的算术运算符都是二元运算符——这意味着它们采用两个操作数——在运算符的两侧。这四个操作符都以完全相同的方式重载。

有三种不同的方法来重载运算符：成员函数、友元函数和普通函数。在本课中，我们将介绍友元函数方法（因为它对于大多数二进制运算符来说更直观）。下一课，我们将讨论正常函数方法。最后，在本章后面的课程中，我们将介绍成员函数方法。当然，我们还将更详细地总结何时使用哪一个。

***
## 使用友元函数重载运算符

考虑以下class：

```C++
class Cents
{
private:
	int m_cents {};

public:
	Cents(int cents) : m_cents{ cents } { }
	int getCents() const { return m_cents; }
};
```

下面的示例显示如何重载运算符（+），以便将两个“Cents”对象添加到一起：

```C++
#include <iostream>

class Cents
{
private:
	int m_cents {};

public:
	Cents(int cents) : m_cents{ cents } { }

	// 声明一个友元函数
	friend Cents operator+(const Cents& c1, const Cents& c2);

	int getCents() const { return m_cents; }
};

// 注: 这个函数不是成员函数
Cents operator+(const Cents& c1, const Cents& c2)
{
	// 可以直接访问m_cents，因为本函数是 Cents 的友元函数
	// 返回 int，触发Cents的构造函数
	return c1.m_cents + c2.m_cents;
}

int main()
{
	Cents cents1{ 6 };
	Cents cents2{ 8 };
	Cents centsSum{ cents1 + cents2 };
	std::cout << "I have " << centsSum.getCents() << " cents.\n";

	return 0;
}
```

这将产生以下结果：

```C++
I have 14 cents.
```

重载加号运算符（+）就像声明一个名为operator+的函数一样简单，给它两个我们想要添加的操作数类型的参数，选择适当的返回类型，然后编写函数。

在Cents对象的情况下，实现operator+()函数非常简单。首先，参数类型：在这个版本的operator+中，把两个Cents对象加到一起，因此函数将采用两个类型为Cents的对象作为输入。其次，返回类型：我们的operator+将返回类型为Cents的结果，因此这是我们的返回类型。

最后，实现：要将两个Cents对象添加到一起，需要从每个Cents对象中使用m_Cents成员。因为重载operator+()函数是类的友元，所以可以直接访问参数的m_cents成员。此外，由于m_cents是一个整数，并且C++知道如何使用内置版本的加号运算符将整数相加在一起，因此我们可以简单地使用+运算符来进行加法。

重载减法运算符（-）也很简单：

```C++
#include <iostream>

class Cents
{
private:
	int m_cents {};

public:
	explicit Cents(int cents) : m_cents{ cents } { }

	// Cents + Cents 实现为友元函数
	friend Cents operator+(const Cents& c1, const Cents& c2);

	// Cents - Cents 实现为友元函数
	friend Cents operator-(const Cents& c1, const Cents& c2);

	int getCents() const { return m_cents; }
};

// 注: 这个函数不是成员函数
Cents operator+(const Cents& c1, const Cents& c2)
{
	// 可以直接访问m_cents，因为本函数是 Cents 的友元函数
	// 返回 int，触发Cents的构造函数
	return Cents { c1.m_cents + c2.m_cents };
}

// 注: 这个函数不是成员函数
Cents operator-(const Cents& c1, const Cents& c2)
{
	// 可以直接访问m_cents，因为本函数是 Cents 的友元函数
	// 返回 int，触发Cents的构造函数
	return Cents { c1.m_cents - c2.m_cents };
}

int main()
{
	Cents cents1{ 6 };
	Cents cents2{ 2 };
	Cents centsSum{ cents1 - cents2 };
	std::cout << "I have " << centsSum.getCents() << " cents.\n";

	return 0;
}
```

重载乘法运算符（\*）和除法运算符（/）就像分别定义运算符\*和运算符/的函数一样容易。

***
## 可以在类内定义友元函数

友元函数不是类的成员，但如果需要，它们仍然可以在类中定义：

```C++
#include <iostream>

class Cents
{
private:
	int m_cents {};

public:
	explicit Cents(int cents) : m_cents{ cents } { }

	// Cents + Cents 实现为友元函数
    // 这个函数实现，放在类中，但它不是类的成员函数
	friend Cents operator+(const Cents& c1, const Cents& c2)
	{
		// 可以直接访问m_cents，因为本函数是 Cents 的友元函数
		// 返回 int，触发Cents的构造函数
		return Cents { c1.m_cents + c2.m_cents };
	}

	int getCents() const { return m_cents; }
};

int main()
{
	Cents cents1{ 6 };
	Cents cents2{ 8 };
	Cents centsSum{ cents1 + cents2 };
	std::cout << "I have " << centsSum.getCents() << " cents.\n";

	return 0;
}
```

对于具有平凡实现的重载操作符，这是很好的。

***
## 为不同类型的操作数重载运算符

通常，您希望重载运算符与不同类型的操作数一起工作。例如，如果我们有Cents（4），我们可能希望将整数6加到该值上，以产生结果Cents（10）。

当C++计算表达式x+y时，x成为第一个参数，y成为第二个参数。当x和y具有相同的类型时，添加x+y或y+x并不重要——不管怎样，调用相同版本的操作符+。然而，当操作数具有不同的类型时，x+y不调用与y+x相同的函数。

例如，Cents（4）+6将调用运算符+（Cents，int），而6+Cents（4）将调用运算符＋（int，Cents）。因此，每当我们为不同类型的操作数重载二元运算符时，我们实际上需要编写两个函数——每种情况一个。下面是一个例子：

```C++
#include <iostream>

class Cents
{
private:
	int m_cents {};

public:
	explicit Cents(int cents) : m_cents{ cents } { }

	// Cents + int 实现为友元函数
	friend Cents operator+(const Cents& c1, int value);

	// int + Cents 实现为友元函数
	friend Cents operator+(int value, const Cents& c1);


	int getCents() const { return m_cents; }
};

// 注: 这个函数不是成员函数
Cents operator+(const Cents& c1, int value)
{
	// 可以直接访问m_cents，因为本函数是 Cents 的友元函数
	return Cents { c1.m_cents + value };
}

// 注: 这个函数不是成员函数
Cents operator+(int value, const Cents& c1)
{
	// 可以直接访问m_cents，因为本函数是 Cents 的友元函数
	return Cents { c1.m_cents + value };
}

int main()
{
	Cents c1{ Cents{ 4 } + 6 };
	Cents c2{ 6 + Cents{ 4 } };

	std::cout << "I have " << c1.getCents() << " cents.\n";
	std::cout << "I have " << c2.getCents() << " cents.\n";

	return 0;
}
```

注意，两个重载函数具有相同的实现——这是因为它们做相同的事情，它们只是以不同的顺序获取参数。

***
## 另一个例子

让我们来看另一个例子：

```C++
#include <iostream>

class MinMax
{
private:
	int m_min {}; // 遇到的最小值
	int m_max {}; // 遇到的最大值

public:
	MinMax(int min, int max)
		: m_min { min }, m_max { max }
	{ }

	int getMin() const { return m_min; }
	int getMax() const { return m_max; }

	friend MinMax operator+(const MinMax& m1, const MinMax& m2);
	friend MinMax operator+(const MinMax& m, int value);
	friend MinMax operator+(int value, const MinMax& m);
};

MinMax operator+(const MinMax& m1, const MinMax& m2)
{
	// 获取m1和m2的最小值
	int min{ m1.m_min < m2.m_min ? m1.m_min : m2.m_min };

	// 获取m1和m2的最大值
	int max{ m1.m_max > m2.m_max ? m1.m_max : m2.m_max };

	return MinMax { min, max };
}

MinMax operator+(const MinMax& m, int value)
{
	// 获取m和value的最小值
	int min{ m.m_min < value ? m.m_min : value };

	// 获取m和value的最大值
	int max{ m.m_max > value ? m.m_max : value };

	return MinMax { min, max };
}

MinMax operator+(int value, const MinMax& m)
{
	// 调用 operator+(MinMax, int)
	return m + value;
}

int main()
{
	MinMax m1{ 10, 15 };
	MinMax m2{ 8, 11 };
	MinMax m3{ 3, 12 };

	MinMax mFinal{ m1 + m2 + 5 + 8 + m3 + 16 };

	std::cout << "Result: (" << mFinal.getMin() << ", " <<
		mFinal.getMax() << ")\n";

	return 0;
}
```

MinMax类跟踪迄今为止看到的最小值和最大值。我们将+操作符重载了3次，因此可以将两个MinMax对象添加到一起，或者将整数加到MinMax对象。

此示例生成结果：

```C++
Result: (3, 16)
```

让我们再多谈一点关于“MinMax mFinal{m1+m2+5+8+m3+16}”的计算方法。请记住，运算符+从左到右求值，因此m1+m2首先求值。这将成为对operator+(m1，m2)的调用，它产生返回值MinMax（8，15）。然后MinMax（8，15）+5求值。这将成为对operator+(MinMax（8,15），5)的调用，它产生返回值MinMax（5,15）。然后，MinMax（5，15）+ 8以相同的方式求值，以生成MinMax（5,15）。然后MinMax（5，15）+m3求值以产生MinMax（3，15）。最后，MinMax（3，15）+16计算为MinMax（3,16）。然后使用该最终结果初始化mFinal。

换句话说，该表达式的计算结果为“MinMax mFinal=（（（（（m1+m2）+5）+8）+m3）+16）”，每个连续操作都返回一个MinMax对象，该对象成为后续运算符的左侧操作数。

***
## 重载运算符函数中，可以使用其他运算符

在上面的示例中，请注意，通过调用operator+（MinMax，int）（产生相同的结果）来定义operator＋（int，MinMax）。这允许我们将operator＋（int，MinMax）的实现减少到一行，通过最小化冗余并使函数更易于理解，使代码更易于维护。

通常可以通过调用其他重载运算符来定义重载运算符。如果这样做会产生更简单的代码，则应该这样做。

***
