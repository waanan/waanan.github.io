---
title: "派生类的构造顺序"
date: 2024-10-08T17:45:57+08:00
---

在上一课关于C++中的基本继承的内容中，学习了类可以从其他类继承成员和函数。在本课中，我们将更仔细地看一看在实例化派生类时发生的构造顺序。

首先，让我们介绍一些新的类，这些类将帮助我们说明一些重要的观点。

```C++
class Base
{
public:
    int m_id {};

    Base(int id=0)
        : m_id { id }
    {
    }

    int getId() const { return m_id; }
};

class Derived: public Base
{
public:
    double m_cost {};

    Derived(double cost=0.0)
        : m_cost { cost }
    {
    }

    double getCost() const { return m_cost; }
};
```

在这个例子中，Derived类是从Base类派生的。

{{< img src="./DerivedBase.gif" title="Derived继承">}}

由于Derived从Base继承函数和变量，因此您可以假设Base的成员被复制到Derived。然而，这不是真的。相反，我们可以将“Derived”视为一个由两部分组成的类：一部分“Derived”，一部分“Base”。

{{< img src="./DerivedBaseCombined.gif" title="Derived结构">}}

之前已经有大量例子，说明当我们实例化一个普通（非派生）类时会发生什么：

```C++
int main()
{
    Base base;

    return 0;
}
```

Base是一个非派生类，因为它不从任何其他类继承成员。C++为Base分配内存，然后调用Base的默认构造函数来进行初始化。

现在让我们看看实例化派生类时会发生什么：

```C++
int main()
{
    Derived derived;

    return 0;
}
```

实际运行时，您不会注意到与前面实例化非派生类Base的示例有任何不同。但在幕后，情况略有不同。如上所述，Derived实际上是两个部分：Base部分和Derived部分。当C++构造派生对象时，它分阶段进行。首先，构造最基本的基类（在继承树的顶部）。然后按顺序构造每个子类，直到最后构造当前的子类（位于继承树的底部）。

因此，当我们实例化Derived的实例时，首先构造Base部分（使用Base默认构造函数）。一旦Base部分完成，就构建Derived部分（使用Derived默认构造函数）。此时，没有更底层的派生类，因此工作结束。

这个过程实际上很容易说明

```C++
#include <iostream>

class Base
{
public:
    int m_id {};

    Base(int id=0)
        : m_id { id }
    {
        std::cout << "Base\n";
    }

    int getId() const { return m_id; }
};

class Derived: public Base
{
public:
    double m_cost {};

    Derived(double cost=0.0)
        : m_cost { cost }
    {
        std::cout << "Derived\n";
    }

    double getCost() const { return m_cost; }
};

int main()
{
    std::cout << "Instantiating Base\n";
    Base base;

    std::cout << "Instantiating Derived\n";
    Derived derived;

    return 0;
}
```

此程序产生以下结果：

```C++
Instantiating Base
Base
Instantiating Derived
Base
Derived
```

当构造Derived时，首先构造Derived的Base部分。这是有意义的：从逻辑上讲，没有父级，子级就不能存在。这也是做事情的安全方法：子类通常使用来自父类的变量和函数，但父类不知道子类的任何信息。首先实例化父类可以确保在创建派生类并准备使用它们时，这些变量已经初始化。

***
## 继承链的构造顺序

有时类是从其他类派生的，这些类本身也是从其他类派生的。例如：

```C++
#include <iostream>

class A
{
public:
    A()
    {
        std::cout << "A\n";
    }
};

class B: public A
{
public:
    B()
    {
        std::cout << "B\n";
    }
};

class C: public B
{
public:
    C()
    {
        std::cout << "C\n";
    }
};

class D: public C
{
public:
    D()
    {
        std::cout << "D\n";
    }
};
```

记住，C++总是首先构造“第一个”或“最基本”类。然后，它按顺序遍历继承树，并构造每个连续的派生类。

下面是一个简短的程序，它说明了整个继承链的创建顺序。

```C++
int main()
{
    std::cout << "Constructing A: \n";
    A a;

    std::cout << "Constructing B: \n";
    B b;

    std::cout << "Constructing C: \n";
    C c;

    std::cout << "Constructing D: \n";
    D d;
}
```

此代码打印以下内容：

```C++
Constructing A:
A
Constructing B:
A
B
Constructing C:
A
B
C
Constructing D:
A
B
C
D
```

***
## 结论

C++分阶段构造派生类，从最基本的类开始（位于继承树顶部），最终结束与当前的子类（在继承树的底部）。在构造每个类时，调用该类的适当构造函数来初始化类的该部分。您将注意到，本节中的示例类都使用了基类默认构造函数（为了简单起见）。在下一课中，我们将更仔细地研究构造函数在构造派生类过程中的作用（包括如何显式选择希望派生类使用的基类构造函数）。

***

{{< prevnext prev="/basic/chapter24/inherit-basic/" next="/" >}}
24.1 基本继承
<--->
主页
{{< /prevnext >}}
