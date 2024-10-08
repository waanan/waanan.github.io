---
title: "使用成员函数重载运算符"
date: 2024-08-20T12:01:51+08:00
---

在前面，我们学习了使用友元函数和普通函数重载运算符。下面来学习如何使用成员函数来重载运算符。

使用成员函数重载运算符与使用友元函数重载运算符非常相似。使用成员函数重载运算符时：

1. 重载运算符是左操作数的成员函数。
2. 左操作数成为隐式*this对象
3. 所有其他操作数都成为函数参数。

下面是使用友元函数重载operator+的方法：

```C++
#include <iostream>

class Cents
{
private:
    int m_cents {};

public:
    Cents(int cents)
        : m_cents { cents } { }

    // 重载 Cents + int
    friend Cents operator+(const Cents& cents, int value);

    int getCents() const { return m_cents; }
};

// 注: 这个函数不是成员函数!
Cents operator+(const Cents& cents, int value)
{
    return Cents(cents.m_cents + value);
}

int main()
{
	const Cents cents1 { 6 };
	const Cents cents2 { cents1 + 2 };
	std::cout << "I have " << cents2.getCents() << " cents.\n";
 
	return 0;
}
```

将友元函数重载运算符转换为成员函数重载运算符很容易：

1. 重载操作符定义为成员函数，而不是友元函数 (Cents::operator+ 而不是 友元 operator+)
2. 左边的参数移除掉，因为它现在变成隐式的 *this 对象
3. 函数体内，所有左边的参数的使用的地方可以移除掉 (例如 cents.m_cents 变为 m_cents, 因为它已经使用了 *this)


现在，使用成员函数方法重载相同的运算符：

```C++
#include <iostream>

class Cents
{
private:
    int m_cents {};

public:
    Cents(int cents)
        : m_cents { cents } { }

    // 重载 Cents + int
    Cents operator+(int value) const;

    int getCents() const { return m_cents; }
};

// 注: 这个函数是成员函数!
// 友元函数的cents参数，现在被隐式的 *this 替代 
Cents Cents::operator+ (int value) const
{
    return Cents { m_cents + value };
}

int main()
{
	const Cents cents1 { 6 };
	const Cents cents2 { cents1 + 2 };
	std::cout << "I have " << cents2.getCents() << " cents.\n";
 
	return 0;
}
```

注意，操作符的用法没有改变（在这两种情况下，都是cents1+2），我们只是简单地以不同的方式定义了函数。我们的双参数友元函数变成了单参数成员函数，友元版本中最左边的参数（cents）成为成员函数版本中的隐式*this。

让我们仔细看看表达式cents1+2的计算方式。

在友元函数版本中，表达式cents1+2变为函数调用operator+（cents1，2）。注意，有两个函数参数。这很简单。

在成员函数版本中，表达式cents1+2变为函数调用cents1.operator+（2）。请注意，现在只有一个显式函数参数，并且cents1已成为对象前缀。编译器隐式地将对象前缀转换为名为\*this的最左侧隐藏参数。因此在现实中，cents1.operator+（2）变为operator+（&cents1,2），这几乎与友元版本相同。

这两种情况产生相同的结果，只是方式略有不同。

因此，如果我们可以将操作符重载为友元函数或成员函数，我们应该使用哪个操作符？为了回答这个问题，还有一些事情你需要知道。

***
## 并非所有内容都可以作为友元函数重载

赋值（=）、下标（[]）、函数调用（（））和成员选择（->）运算符必须重载为成员函数，因为语言要求它们是成员函数。

***
## 并非所有内容都可以作为成员函数重载

在前面重载I/O操作符中，我们使用友元函数方法为Point类重载操作符<<。以下是我们如何做到这一点的例子：

```C++
#include <iostream>
 
class Point
{
private:
    double m_x {};
    double m_y {};
    double m_z {};
 
public:
    Point(double x=0.0, double y=0.0, double z=0.0)
        : m_x { x }, m_y { y }, m_z { z }
    {
    }
 
    friend std::ostream& operator<< (std::ostream& out, const Point& point);
};
 
std::ostream& operator<< (std::ostream& out, const Point& point)
{
    // 因为 operator<< 是 Point 的友元, 因此可以直接访问Point的成员
    out << "Point(" << point.m_x << ", " << point.m_y << ", " << point.m_z << ")";
 
    return out;
}
 
int main()
{
    Point point1 { 2.0, 3.0, 4.0 };
 
    std::cout << point1;
 
    return 0;
}
```

然而，我们不能将运算符<<作为成员函数重载。为什么呢？因为重载运算符必须添加为左操作数的成员。在这种情况下，左操作数是std::ostream类型的对象。std::ostream固定为标准库的一部分。我们不能修改类声明来将重载添加为std::ostream的成员函数。

这需要将运算符<< 重载为正常函数（首选）或友元函数。

类似地，尽管我们可以将操作符+（Cents，int）作为成员函数重载（正如我们上面所做的），但我们不能将操作符＋（int，Cents）作为成员函式重载，因为int不是可以向其添加成员的类。

通常，如果左操作数不是类（例如int），或者是无法修改的类（例如std::ostream），我们将无法使用成员重载。

***
## 何时使用普通、友元或成员函数重载

在大多数情况下，语言让您自行决定是使用重载的普通/友元版本还是成员函数版本。然而，两者中的一个通常是比另一个更好的选择。

当处理不修改左操作数的二元运算符（例如，运算符+）时，通常首选普通函数或友元函数版本，因为它适用于所有参数类型（即使左操作数不是类对象，或者是不可修改的类）。普通或友元函数版本具有“对称性”的额外优势，因为所有操作数都成为显式参数（而不是左操作数变为*this，右操作数变为了显式参数）。

当处理确实修改左操作数的二元运算符（例如，运算符+=）时，通常首选成员函数版本。在这些情况下，最左边的操作数始终是类类型，在该类型上直接操作也是很自然的。因为最右边的操作数成为显式参数，所以不会混淆谁被修改，谁被求值。

一元运算符通常也作为成员函数重载，因为成员版本没有参数。

以下经验法则可以帮助您确定哪种形式最适合给定的情况：

1. 如果重载赋值（=）、下标（[]）、函数调用（（））或成员选择（->），请作为成员函数进行重载。
2. 如果要重载一元运算符，请作为成员函数进行重载。
3. 如果重载不修改其左操作数的二元运算符（例如，运算符+），请作为普通函数（首选）或友元函数进行重载。
4. 如果重载修改其左操作数的二元运算符，但左侧操作数不允许添加成员函数（例如，运算符<<，它具有ostream类型的左操作数）的类定义中，请作为普通函数（首选）或友元函数进行重载。
5. 如果重载修改其左操作数的二元运算符（例如，运算符+=），并且可以修改左操作数的定义，请作为成员函数进行修改。

***

{{< prevnext prev="/basic/chapter21/overload-io/" next="/basic/chapter21/unary-op-overload/" >}}
21.3 重载I/O运算符
<--->
21.5 重载一元运算符+、-和！
{{< /prevnext >}}
