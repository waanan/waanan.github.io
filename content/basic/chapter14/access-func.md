---
title: "访问函数"
date: 2024-04-09T13:02:20+08:00
---

在上一课中，讨论了public和private访问级别。作为提醒，类通常将其数据成员设置为私有，而私有成员不能由公共直接访问。

考虑以下Date类：

```C++
#include <iostream>

class Date
{
private:
    int m_year{ 2020 };
    int m_month{ 10 };
    int m_day{ 14 };

public:
    void print() const
    {
        std::cout << m_year << '/' << m_month << '/' << m_day << '\n';
    }
};

int main()
{
    Date d{};  // 创建一个 Date 对象
    d.print(); // 打印 date

    return 0;
}
```

虽然该类提供了一个 print() 成员函数来打印Date，但这可能不足以满足用户的需要。例如，如果date对象的用户想要获得年份，该怎么办？或者将年份更改为不同的值？他们将无法这样做，因为m_year是私有的（因此不能被公共直接访问）。

对于某些类，（在类所处上下文中）需要适当地获取或设置私有成员变量的值。

***
## 访问函数

访问函数是一个普通的公共成员函数，其任务是检索或更改私有成员变量的值。

访问函数有两种：getter和setter。Getter（有时也称为访问器）是返回私有成员变量值的public成员函数。Setter（有时也称为mutator）是设置私有成员变量值的public成员函数。

Getter通常被设置为const，因此可以在常量和非常量对象上调用它们。Setter应该是非const，因此它们需要修改数据成员。

为了便于说明，更新Date类，以拥有一整套getter和setter：

```C++
#include <iostream>

class Date
{
private:
    int m_year { 2020 };
    int m_month { 10 };
    int m_day { 14 };

public:
    void print()
    {
        std::cout << m_year << '/' << m_month << '/' << m_day << '\n';
    }

    int getYear() const { return m_year; }        // getter for year
    void setYear(int year) { m_year = year; }     // setter for year

    int getMonth() const  { return m_month; }     // getter for month
    void setMonth(int month) { m_month = month; } // setter for month

    int getDay() const { return m_day; }          // getter for day
    void setDay(int day) { m_day = day; }         // setter for day
};

int main()
{
    Date d{};
    d.setYear(2021);
    std::cout << "The year is: " << d.getYear() << '\n';

    return 0;
}
```

这将打印：

```C++
The year is: 2021
```

***
## 访问函数命名

访问函数没有通用命名约定。当然，有一些命名约定比其他约定更受欢迎。

1. 前缀为“get”和“set”：


```C++
    int getDay() const { return m_day; }  // getter
    void setDay(int day) { m_day = day; } // setter
```

使用“get”和“set”前缀的优点是，它清楚地表明，这些是访问函数（并且调用成本应该较低）。

2. 没有前缀：


```C++
    int day() const { return m_day; }  // getter
    void day(int day) { m_day = day; } // setter
```

这种风格更简洁，并且对getter和setter使用相同的名称（依赖于函数重载来区分两者）。C++标准库使用此约定。

无前缀约定的缺点是，这样设置day成员的值并不特别明显：

```C++
d.day(5); // 这看起来并不太像将 day 成员变量设置成 5?
```

3. 仅限“set”前缀：


```C++
    int day() const { return m_day; }     // getter
    void setDay(int day) { m_day = day; } // setter
```

选择上面哪一个是个人偏好的问题。然而，强烈建议对setter使用“set”前缀。Getter可以使用“get”前缀，也可以不使用前缀。

{{< alert success >}}
**关键点**

在私有数据成员前面加上“m_”的最好原因之一是避免数据成员和getter具有相同的名称（C++不支持这一点，尽管Java等其他语言支持）。

{{< /alert >}}

{{< alert success >}}
**提示**

在setter上使用“set”前缀，使它们改变对象的状态的语义更加明显。

{{< /alert >}}

***
## Getter应通过值或常量值引用返回

Getter应提供对数据的“只读”访问。因此，最佳实践是，它们应该通过值（如果制作成员的副本成本不高）或常量值引用（如果制作该成员的副本的成本很高）返回。

由于通过引用返回数据成员是一个非常重要的主题，因此将在后面更详细地讨论该主题。

***
## 访问函数的问题

关于应该使用或避免访问函数的情况，有相当多的讨论。许多开发人员会认为，访问函数的使用违反了良好的类设计（这是一个很容易填满整本书的主题）。

现在，我们将推荐一种务实的方法。创建类时，请考虑以下事项：

1. 如果您的类没有不变量约束，并且需要大量访问函数，请考虑使用结构体（其数据成员是公共的），提供对成员的直接访问。
2. 优先实现行为或操作，而不是访问函数。例如，不是实现setAlive(bool)这样的setter，而是实现kill() 和 revive() 函数。
3. 仅在public区域需要合理获取或设置单个成员的值的情况下提供访问函数。

***
## 如果要为数据提供public访问函数，为什么要将其私有化？

这是一个很好的问题。将在后续讲解数据隐藏（封装）的好处时进行讲解。

***

{{< prevnext prev="/basic/chapter14/public-private/" next="/basic/chapter14/member-func-ret-member-data-ref/" >}}
14.4 公共和私有成员以及访问说明符
<--->
14.6 成员函数返回对数据成员的引用
{{< /prevnext >}}
