---
title: "重载比较运算符"
date: 2024-08-20T12:01:51+08:00
---

一共有六个比较运算符。重载这些比较运算符相对简单，因为它们遵循与重载其他运算符相同的模式。

由于比较运算符都是不修改其左操作数的二元运算符，因此我们重载比较运算符为友元函数。

下面是一个具有重载 运算符== 和 运算符!= 的Car类的示例。

```C++
#include <iostream>
#include <string>
#include <string_view>

class Car
{
private:
    std::string m_make;
    std::string m_model;

public:
    Car(std::string_view make, std::string_view model)
        : m_make{ make }, m_model{ model }
    {
    }

    friend bool operator== (const Car& c1, const Car& c2);
    friend bool operator!= (const Car& c1, const Car& c2);
};

bool operator== (const Car& c1, const Car& c2)
{
    return (c1.m_make == c2.m_make &&
            c1.m_model == c2.m_model);
}

bool operator!= (const Car& c1, const Car& c2)
{
    return (c1.m_make != c2.m_make ||
            c1.m_model != c2.m_model);
}

int main()
{
    Car corolla{ "Toyota", "Corolla" };
    Car camry{ "Toyota", "Camry" };

    if (corolla == camry)
        std::cout << "a Corolla and Camry are the same.\n";

    if (corolla != camry)
        std::cout << "a Corolla and Camry are not the same.\n";

    return 0;
}
```

这里的代码应该很简单。

操作符\< 和 操作符\> 呢？一辆车比另一辆车大或小意味着什么？通常没有这样的关系。由于 运算符\< 和 运算符\> 的结果不是很直观，因此这里最好不定义这些运算符。

然而，上述建议有一个例外。如果我们想对汽车列表进行排序，该怎么办？在这种情况下，我们可能希望重载比较运算符，以返回您最可能希望排序的方式。例如，重载 运算符\< , 汽车可以根据品牌和型号按字母顺序排序。

标准库中的一些容器类（保存其他类的类）需要元素重载运算符<，以便它们可以对元素进行排序。

下面是另一个重载所有6个逻辑比较运算符的示例：

```C++
#include <iostream>

class Cents
{
private:
    int m_cents;
 
public:
    Cents(int cents)
	: m_cents{ cents }
	{}
 
    friend bool operator== (const Cents& c1, const Cents& c2);
    friend bool operator!= (const Cents& c1, const Cents& c2);

    friend bool operator< (const Cents& c1, const Cents& c2);
    friend bool operator> (const Cents& c1, const Cents& c2);

    friend bool operator<= (const Cents& c1, const Cents& c2);
    friend bool operator>= (const Cents& c1, const Cents& c2);
};

bool operator== (const Cents& c1, const Cents& c2)
{
    return c1.m_cents == c2.m_cents;
}

bool operator!= (const Cents& c1, const Cents& c2)
{
    return c1.m_cents != c2.m_cents;
}

bool operator> (const Cents& c1, const Cents& c2)
{
    return c1.m_cents > c2.m_cents;
}

bool operator< (const Cents& c1, const Cents& c2)
{
    return c1.m_cents < c2.m_cents;
}

bool operator<= (const Cents& c1, const Cents& c2)
{
    return c1.m_cents <= c2.m_cents;
}

bool operator>= (const Cents& c1, const Cents& c2)
{
    return c1.m_cents >= c2.m_cents;
}

int main()
{
    Cents dime{ 10 };
    Cents nickel{ 5 };
 
    if (nickel > dime)
        std::cout << "a nickel is greater than a dime.\n";
    if (nickel >= dime)
        std::cout << "a nickel is greater than or equal to a dime.\n";
    if (nickel < dime)
        std::cout << "a dime is greater than a nickel.\n";
    if (nickel <= dime)
        std::cout << "a dime is greater than or equal to a nickel.\n";
    if (nickel == dime)
        std::cout << "a dime is equal to a nickel.\n";
    if (nickel != dime)
        std::cout << "a dime is not equal to a nickel.\n";

    return 0;
}
```

这也是相当简单的。

{{< alert success >}}
**最佳实践**

只定义对类有直观意义的重载运算符。

{{< /alert >}}

***
## 最大限度地减少相对冗余

在上面的示例中，请注意每个重载比较运算符的实现是多么相似。重载的比较运算符往往具有高度冗余，实现越复杂，冗余就越多。

幸运的是，许多比较运算符可以使用其他比较运算符来实现：

1. 运算符!= 可以实现为 !（运算符==）
2. 运算符> 可以实现为 运算符<，只要参数的顺序翻转
3. 运算符>= 可以实现为  !（运算符<）
4. 运算符<= 可以实现为  !（运算符>）


这意味着我们只需要实现运算符==和运算符<的逻辑，然后可以根据这两个定义其他四个比较运算符！下面是一个更新的Cents示例，说明了这一点：

```C++
#include <iostream>

class Cents
{
private:
    int m_cents;

public:
    Cents(int cents)
        : m_cents{ cents }
    {}

    friend bool operator== (const Cents& c1, const Cents& c2) { return c1.m_cents == c2.m_cents; }
    friend bool operator!= (const Cents& c1, const Cents& c2) { return !(operator==(c1, c2)); }

    friend bool operator< (const Cents& c1, const Cents& c2) { return c1.m_cents < c2.m_cents; }
    friend bool operator> (const Cents& c1, const Cents& c2) { return operator<(c2, c1); }

    friend bool operator<= (const Cents& c1, const Cents& c2) { return !(operator>(c1, c2)); }
    friend bool operator>= (const Cents& c1, const Cents& c2) { return !(operator<(c1, c2)); }

};

int main()
{
    Cents dime{ 10 };
    Cents nickel{ 5 };

    if (nickel > dime)
        std::cout << "a nickel is greater than a dime.\n";
    if (nickel >= dime)
        std::cout << "a nickel is greater than or equal to a dime.\n";
    if (nickel < dime)
        std::cout << "a dime is greater than a nickel.\n";
    if (nickel <= dime)
        std::cout << "a dime is greater than or equal to a nickel.\n";
    if (nickel == dime)
        std::cout << "a dime is equal to a nickel.\n";
    if (nickel != dime)
        std::cout << "a dime is not equal to a nickel.\n";

    return 0;
}
```

这样，如果我们需要更改某些内容，我们只需要更新operator==和operator<，而不是所有六个比较运算符！

***
## 太空船 运算符<=>  （C++20）

C++20引入了太空船运算符（operator\<=\>），它允许我们将需要写的比较函数的数量减少到最多2个，有时仅1个，我们将在后续的某一课中进行讨论！

***
