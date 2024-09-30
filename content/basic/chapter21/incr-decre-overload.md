---
title: "重载递增和递减运算符"
date: 2024-08-20T12:01:51+08:00
---

重载increment（++）和decrement（--）操作符非常简单，只有一个小的例外。实际上，递增和递减运算符有两个版本：前缀递增和递减（例如++x；--y；）和后缀递增和递减 (例如 x++; y--;)。

由于增量和减量运算符都是一元运算符，并且它们修改其操作数，因此最好将它们重载为成员函数。我们将首先处理前缀版本，因为它们是最简单的。

***
## 重载前缀递增和递减

重载前缀递增和递减运算符与重载任何正常的一元运算符完全相同。下面通过示例进行演示：

```C++
#include <iostream>

class Digit
{
private:
    int m_digit{};
public:
    Digit(int digit=0)
        : m_digit{digit}
    {
    }

    Digit& operator++();
    Digit& operator--();

    friend std::ostream& operator<< (std::ostream& out, const Digit& d);
};

Digit& Digit::operator++()
{
    // 如果数字是 9, 回绕到 0
    if (m_digit == 9)
        m_digit = 0;
    // 否则增加到下一个
    else
        ++m_digit;

    return *this;
}

Digit& Digit::operator--()
{
    // 如果数字是 0, 回绕到 9
    if (m_digit == 0)
        m_digit = 9;
    // 否则减少到下一个
    else
        --m_digit;

    return *this;
}

std::ostream& operator<< (std::ostream& out, const Digit& d)
{
	out << d.m_digit;
	return out;
}

int main()
{
    Digit digit { 8 };

    std::cout << digit;
    std::cout << ++digit;
    std::cout << ++digit;
    std::cout << --digit;
    std::cout << --digit;

    return 0;
}
```

我们的Digit类处理0到9之间的数字。我们重载了递增和递减，因此它们对数字进行递增/递减，如果数字的递增/递减超出范围，则进行环绕。

此示例打印：

```C++
89098
```

请注意，我们返回了*this。重载的递增和递减运算符返回当前隐式对象，因此可以将多个运算符“链接”在一起。

***
## 重载后缀递增和递减

通常，当函数具有相同的名称但具有不同的数量和/或不同类型的参数时，可以重载它们。然而，考虑前缀和后缀递增和递减运算符的情况。两者具有相同的名称（例如，运算符++），是一元的，并且采用相同类型的一个参数。那么，在重载时如何区分这两者呢？

C++语言规范提供了一个特列来处理这种情况：编译器查看重载运算符是否具有int参数。如果重载运算符具有int参数，则该运算符是后缀重载。如果重载运算符没有参数，则该运算符是前缀重载。

下面是上面的Digit类，其中包含前缀和后缀重载：

```C++
class Digit
{
private:
    int m_digit{};
public:
    Digit(int digit=0)
        : m_digit{digit}
    {
    }

    Digit& operator++(); // 无参数，前缀
    Digit& operator--(); // 无参数，前缀

    Digit operator++(int); // 有int参数，后缀
    Digit operator--(int); // 有int参数，后缀

    friend std::ostream& operator<< (std::ostream& out, const Digit& d);
};

// 无参数，前缀
Digit& Digit::operator++()
{
    // 如果数字是 9, 回绕到 0
    if (m_digit == 9)
        m_digit = 0;
    // 否则增加到下一个
    else
        ++m_digit;

    return *this;
}

// 无参数，前缀
Digit& Digit::operator--()
{
    // 如果数字是 0, 回绕到 9
    if (m_digit == 0)
        m_digit = 9;
    // 否则减少到下一个
    else
        --m_digit;

    return *this;
}

// 有int参数，后缀
Digit Digit::operator++(int)
{
    // 使用当前值创建一个临时变量
    Digit temp{*this};

    // 使用前缀版本去递增一下
    ++(*this); // 调用对应的运算符

    // 返回临时对象
    return temp; // 返回保存的状态
}

// 有int参数，后缀
Digit Digit::operator--(int)
{
    // 使用当前值创建一个临时变量
    Digit temp{*this};

    // 是用前缀版本去递减一下
    --(*this); // 调用对应的运算符

    // 返回临时对象
    return temp; // 返回保存的状态
}

std::ostream& operator<< (std::ostream& out, const Digit& d)
{
	out << d.m_digit;
	return out;
}

int main()
{
    Digit digit { 5 };

    std::cout << digit;
    std::cout << ++digit; // 调用 Digit::operator++();
    std::cout << digit++; // 调用 Digit::operator++(int);
    std::cout << digit;
    std::cout << --digit; // 调用 Digit::operator--();
    std::cout << digit--; // 调用 Digit::operator--(int);
    std::cout << digit;

    return 0;
}
```

结果打印

```C++
5667665
```

这里发生了一些有趣的事情。首先，请注意，通过在后缀版本上提供整数参数来区分前缀和后缀运算符。其次，因为在函数实现中没有使用该参数，所以我们甚至没有给它命名。这告诉编译器将该变量视为占位符，这意味着它不会警告我们声明了一个变量，但从未使用过它。

第三，注意前缀和后缀操作符执行相同的工作——它们都增加或减少对象。两者之间的区别在于它们返回的值。重载的前缀运算符在对象递增或递减后返回该对象。这是相当简单的。只需增加或减少成员变量，然后返回*this。

另一方面，后缀操作符需要返回对象递增或递减之前的状态。这导致了一个难题——如果增加或减少对象，将无法返回对象在增加或减少之前的状态。另一方面，如果在递增或递减对象之前返回该对象的状态，则永远不会调用递增或递减。

解决此问题的典型方法是使用临时变量，该变量在对象的值递增或递减之前保存该对象的值。然后，对象本身可以递增或递减。最后，将临时变量返回给调用者。通过这种方式，调用者接收对象递增或递减之前的副本，但对象本身是递增或递减的。注意，这意味着重载操作符的返回值必须是非引用，因为我们不能返回对局部变量的引用，该局部变量将在函数退出时被销毁。还要注意，这意味着后缀操作符通常不如前缀操作符性能好，因为实例化临时变量并按值而不是按引用返回会增加开销。

最后，请注意，我们编写了后缀版本，它调用前缀版本来完成大部分工作。这减少了重复代码，并使类在将来更容易修改。

***