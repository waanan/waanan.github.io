---
title: "拷贝构造函数简介"
date: 2024-04-09T13:02:20+08:00
---

考虑以下程序：

```C++
#include <iostream>
 
class Fraction
{
private:
    int m_numerator{ 0 };
    int m_denominator{ 1 };
 
public:
    // 默认构造函数
    Fraction(int numerator=0, int denominator=1)
        : m_numerator{numerator}, m_denominator{denominator}
    {
    }

    void print() const
    {
        std::cout << "Fraction(" << m_numerator << ", " << m_denominator << ")\n";
    }
};

int main()
{
    Fraction f { 5, 3 };  // 调用 Fraction(int, int) 构造函数
    Fraction fCopy { f }; // 这里会调用什么构造函数?

    f.print();
    fCopy.print();

    return 0;
}
```

您可能会惊讶地发现，该程序编译得非常好，并产生以下结果：

```C++
Fraction(5, 3)
Fraction(5, 3)
```

让我们仔细看看这个程序是如何工作的。

变量f的初始化是调用Fraction(int, int)构造函数的标准列表初始化。

但下一行呢？变量fCopy的初始化显然也是一种初始化，构造函数用于初始化类。那么这一行调用的是什么构造函数呢？

答案是：拷贝构造函数。

***
## 拷贝构造函数

拷贝构造函数，可以使用相同类型的现有对象来做初始化。在拷贝构造函数执行之后，新创建的对象应该是传入对象的副本。

***
## 隐式拷贝构造函数

如果不为类提供拷贝构造函数，C++将为您创建public隐式拷贝构造函数。在上面的示例中，语句Fraction fCopy{f}；调用隐式拷贝构造函数以使用f初始化fCopy。

默认情况下，隐式拷贝构造函数将执行成员级初始化。这意味着将使用传入的对象的相应成员来初始化每个成员。在上面的示例中，使用f.m_numerator（值为5）初始化fCopy.m_numelator，并使用f.m_denominator（值为3）初始化fCopy.m_denoginator。

执行拷贝构造函数后，f和fCopy的成员具有相同的值，因此fCopy是f的副本。因此，对两者调用print()具有相同的结果。

***
## 定义自己的拷贝构造函数

还可以显式定义自己的拷贝构造函数。在本课中，将使拷贝构造函数打印一条消息，以便可以向您展示在进行拷贝时它确实在执行。

拷贝构造函数看起来就像您期望的那样：

```C++
#include <iostream>
 
class Fraction
{
private:
    int m_numerator{ 0 };
    int m_denominator{ 1 };
 
public:
    // 默认构造函数
    Fraction(int numerator=0, int denominator=1)
        : m_numerator{numerator}, m_denominator{denominator}
    {
    }

    // 拷贝构造函数
    Fraction(const Fraction& fraction)
        // 使用传入对象的成员来初始化对应的成员变量
        : m_numerator{ fraction.m_numerator }
        , m_denominator{ fraction.m_denominator }
    {
        std::cout << "Copy constructor called\n"; // 这里打印，是为了证明本函数确实被执行了
    }

    void print() const
    {
        std::cout << "Fraction(" << m_numerator << ", " << m_denominator << ")\n";
    }
};

int main()
{
    Fraction f { 5, 3 };  // 调用 Fraction(int, int) 构造函数
    Fraction fCopy { f }; // 调用 Fraction(const Fraction&) 拷贝构造函数

    f.print();
    fCopy.print();

    return 0;
}
```

运行此程序时，将打印：

```C++
Copy constructor called
Fraction(5, 3)
Fraction(5, 3)
```

在上面定义的拷贝构造函数在功能上等同于默认情况下获得的构造函数，只是我们添加了一个输出语句来证明拷贝构造函数实际上被调用。当用f初始化fCopy时，调用该拷贝构造函数。

拷贝构造函数除了复制对象之外，不应执行任何其他操作。这是因为编译器在某些情况下可能会优化拷贝构造函数。如果您依赖拷贝构造函数来执行某些行为，而不仅仅是复制，则该行为可能会发生，也可能不会发生。我们在后续类初始化讲解中进一步讨论了这一点。

{{< alert success >}}
**一个提醒**

访问控制以每个类为基础（而不是以每个对象为基础）。这意味着类的成员函数可以访问同一类型的任何类对象的私有成员。

在上面的Fraction拷贝构造函数中，可以直接访问参数fraction的private成员。否则，将不得不为每个成员设置访问函数。

{{< /alert >}}

{{< alert success >}}
**最佳实践**

拷贝构造函数除了复制之外应该没有其它副作用。

{{< /alert >}}

***
## 首选隐式拷贝构造函数

与隐式默认构造函数不做任何事情（因此很少是我们想要的）不同，隐式拷贝构造函数执行的成员级初始化通常正是我们想要做的。因此，在大多数情况下，使用隐式拷贝构造函数是完美的。

后面在讨论深拷贝与浅拷贝时，将看到在进行动态内存分配时需要覆盖拷贝构造函数的情况。

{{< alert success >}}
**最佳实践**

首选隐式拷贝构造函数，除非您有特定的原因创建自己的拷贝构造函数。

{{< /alert >}}

***
## 拷贝构造函数的参数必须是引用

拷贝构造函数的参数必须是左值引用或常量左值引用。由于拷贝构造函数不应修改参数，因此最好使用常量左值引用。

{{< alert success >}}
**最佳实践**

如果编写自己的拷贝构造函数，则参数应该是常量左值引用。

{{< /alert >}}

***
## 按值传递（和按值返回）与拷贝构造函数

当对象通过值传递时，它被复制到参数中。当它和参数是相同的类类型时，通过隐式调用拷贝构造函数来进行复制。类似地，当对象按值返回给调用方时，将隐式调用拷贝构造函数来进行复制。

可以在下面的示例中看到这两种情况：

```C++
#include <iostream>

class Fraction
{
private:
    int m_numerator{ 0 };
    int m_denominator{ 1 };

public:
    // 默认构造函数
    Fraction(int numerator = 0, int denominator = 1)
        : m_numerator{ numerator }, m_denominator{ denominator }
    {
    }

    // 拷贝构造函数
    Fraction(const Fraction& fraction)
        : m_numerator{ fraction.m_numerator }
        , m_denominator{ fraction.m_denominator }
    {
        std::cout << "Copy constructor called\n";
    }

    void print() const
    {
        std::cout << "Fraction(" << m_numerator << ", " << m_denominator << ")\n";
    }
};

void printFraction(Fraction f) // f 按值传递
{
    f.print();
}

Fraction generateFraction(int n, int d)
{
    Fraction f{ n, d };
    return f;
}

int main()
{
    Fraction f{ 5, 3 };

    printFraction(f); // f 按值复制到参数中，使用拷贝构造函数

    Fraction f2{ generateFraction(1, 2) }; // Fraction 按值返回，使用拷贝构造函数

    printFraction(f2); // f2 按值复制到参数中，使用拷贝构造函数

    return 0;
}
```

在上面的示例中，对printFraction(f) 的调用按值传递f。调用拷贝构造函数将f从main复制到函数printFraction的f参数中。

当generateFraction将Fraction返回到main时，将再次隐式调用拷贝构造函数。当将f2传递给printFraction时，第三次调用拷贝构造函数。

在作者的机器上，此示例打印：

```C++
Copy constructor called
Fraction(5, 3)
Copy constructor called
Copy constructor called
Fraction(1, 2)
```

如果编译并执行上面的示例，您可能会发现只发生两次对拷贝构造函数的调用。这是一种称为拷贝省略（copy elision）的编译器优化。。

***
## 使用 = default 生成默认拷贝构造函数

如果类没有拷贝构造函数，编译器将隐式为我们生成一个。如果愿意，可以使用=default语法显式请求编译器为我们创建默认的拷贝构造函数：

```C++
#include <iostream>
 
class Fraction
{
private:
    int m_numerator{ 0 };
    int m_denominator{ 1 };
 
public:
    // 默认构造函数
    Fraction(int numerator=0, int denominator=1)
        : m_numerator{numerator}, m_denominator{denominator}
    {
    }

    // 显示请求 默认的拷贝构造函数
    Fraction(const Fraction& fraction) = default;

    void print() const
    {
        std::cout << "Fraction(" << m_numerator << ", " << m_denominator << ")\n";
    }
};

int main()
{
    Fraction f { 5, 3 };
    Fraction fCopy { f };

    f.print();
    fCopy.print();

    return 0;
}
```

***
## 使用 = delete 以防止复制

有时会遇到这样的情况，即不希望某个类的对象是可复制的。可以通过使用「=delete」语法将拷贝构造函数标记为「删除」来防止这种情况：

```C++
#include <iostream>
 
class Fraction
{
private:
    int m_numerator{ 0 };
    int m_denominator{ 1 };
 
public:
    // 默认构造函数
    Fraction(int numerator=0, int denominator=1)
        : m_numerator{numerator}, m_denominator{denominator}
    {
    }

    // 删除拷贝构造函数，防止类的对象实例能被复制
    Fraction(const Fraction& fraction) = delete;

    void print() const
    {
        std::cout << "Fraction(" << m_numerator << ", " << m_denominator << ")\n";
    }
};

int main()
{
    Fraction f { 5, 3 };
    Fraction fCopy { f }; // 编译失败: 拷贝构造函数被删除了

    return 0;
}
```

在该示例中，当编译器查找构造函数以使用f初始化fCopy时，它将看到拷贝构造函数已被删除。这将导致它发出编译错误。

{{< alert success >}}
**旁白**

您还可以通过将拷贝构造函数设置为私有（因为私有函数不能被public调用）来防止public复制类对象。然而，私有副本构造函数仍然可以从类的其他成员调用，因此除非需要，否则不建议使用此解决方案。

{{< /alert >}}

{{< alert success >}}
**对于高级读者**

有一个众所周知的C++原则，如果类需要用户定义的拷贝构造函数、析构函数或拷贝赋值运算符，那么它可能需要所有这三个。在C++11中，新增了两个，将移动构造函数和移动赋值运算符添加到列表中。

不遵循这个原则可能会导致代码出现故障。在讨论动态内存分配时，将重新讨论这些。

{{< /alert >}}

***

{{< prevnext prev="/basic/chapter14/tmp_obj/" next="/basic/chapter14/class-init-copy-elision/" >}}
14.12 临时类对象
<--->
14.14 类初始化和拷贝省略
{{< /prevnext >}}
