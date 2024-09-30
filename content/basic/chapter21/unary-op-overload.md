---
title: "重载一元运算符+、-和！"
date: 2024-08-20T12:01:51+08:00
---

与迄今为止看到的运算符不同，正（+）、负（-）和逻辑not（！）运算符都是一元运算符，这意味着它们只对一个操作数进行操作。因为它们只对应用它们的对象进行操作，所以通常一元运算符重载被实现为成员函数。所有三个操作符都以相同的方式实现。

让我们看看如何在前面的示例中使用的Cents类上实现操作符：

```C++
#include <iostream>

class Cents
{
private:
    int m_cents {};
 
public:
    Cents(int cents): m_cents{cents} {}
 
    // 重载 -Cents 作为成员函数
    Cents operator-() const;

    int getCents() const { return m_cents; }
};
 
// 注: 这个函数是成员函数!
Cents Cents::operator-() const
{
    return -m_cents; // 因为返回类型是Cents，这里有个int到Cents的隐式转换
}

int main()
{
    const Cents nickle{ 5 };
    std::cout << "A nickle of debt is worth " << (-nickle).getCents() << " cents\n";

    return 0;
}
```

这应该是直截了当的。我们的重载负运算符（-）是一个作为成员函数实现的一元运算符，因此它不带参数（它在*this对象上操作）。它返回一个Cents对象，该对象是原始Cents值的负数。因为操作符-不会修改Cents对象，所以我们可以（并且应该）将其设置为const函数（因此可以在const Cents对象上调用它）。

注意，负操作符和减法操作符之间没有混淆，因为它们具有不同数量的参数。

这是另一个例子。“operator！”是逻辑求反运算符——如果表达式的计算结果为“true”，则为“operator！”将返回false，反之亦然。我们通常将此应用于布尔变量，以测试它们是否为真：

```C++
if (!isHappy)
    std::cout << "I am not happy!\n";
else
    std::cout << "I am so happy!\n";
```

对于整数，0计算为false，其他任何值计算为true，所以“operator！”应用于整数时，如果整数值为0，则返回true，否则返回false。

扩展概念，我们可以说“operator！”，如果对象的状态为“false”、“zero”或默认初始化状态是什么，则应计算为true。

下面的示例显示对于用户定义的Point类进行“operator！”重载：

```C++
#include <iostream>

class Point
{
private:
    double m_x {};
    double m_y {};
    double m_z {};
 
public:
    Point(double x=0.0, double y=0.0, double z=0.0):
        m_x{x}, m_y{y}, m_z{z}
    {
    }
 
    // 转换成一个负的对应的量
    Point operator- () const;

    // 如果为原点，则返回true
    bool operator! () const;
 
    double getX() const { return m_x; }
    double getY() const { return m_y; }
    double getZ() const { return m_z; }
};

// 转换成一个负的对应的量
Point Point::operator- () const
{
    return { -m_x, -m_y, -m_z };
}

// 如果为原点，则返回true
bool Point::operator! () const
{
    return (m_x == 0.0 && m_y == 0.0 && m_z == 0.0);
}

int main()
{
    Point point{}; // 默认构造函数会初始化为 (0.0, 0.0, 0.0)

    if (!point)
        std::cout << "point is set at the origin.\n";
    else
        std::cout << "point is not set at the origin.\n";

    return 0;
}
```

对于Point重载的“operator！”，如果对应的对象在坐标（0.0、0.0、0.0），则返回布尔值“true”。因此，上述代码生成结果：

```C++
point is set at the origin.
```

***

{{< prevnext prev="/basic/chapter21/member-op-overload/" next="/basic/chapter21/compare-op-overload/" >}}
21.4 使用成员函数重载运算符
<--->
21.6 重载比较运算符
{{< /prevnext >}}
