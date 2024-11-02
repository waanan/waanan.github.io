---
title: "派生类的构造函数与初始化"
date: 2024-10-08T17:45:57+08:00
---

在过去的两节课中，我们探讨了C++继承的一些基础知识以及派生类的初始化顺序。在本课中，将更仔细地了解派生类初始化中的构造函数。这里继续使用在上一课中开发的简单Base和Derived类：

```C++
class Base
{
public:
    int m_id {};
 
    Base(int id=0)
        : m_id{ id }
    {
    }
 
    int getId() const { return m_id; }
};
 
class Derived: public Base
{
public:
    double m_cost {};
 
    Derived(double cost=0.0)
        : m_cost{ cost }
    {
    }
 
    double getCost() const { return m_cost; }
};
```

对于非派生类，构造函数只需初始化自己的成员。例如，考虑Base。可以如下所示创建基本对象：

```C++
int main()
{
    Base base{ 5 }; // 使用 Base(int) 构造函数

    return 0;
}
```

下面是实例化base时实际发生的情况：

1. 内存分配
2. 找到合适的构造函数
3. 对成员变量进行列表初始化
4. 构造函数体中的代码被执行
5. 实例化完成，构造函数返回

这很简单。对于派生类，事情稍微复杂一些：

```C++
int main()
{
    Derived derived{ 1.3 }; // 使用 Derived(double) 构造函数

    return 0;
}
```

下面是实例化derived时实际发生的情况：

1. 分配内存（需要能装下Base和Derived部分）
2. 找到合适的Derived构造函数
3. Base部分使用对应的Base构造函数进行构造。如果没有显式声明的构造函数，则使用默认构造函数。
4. 对成员变量进行列表初始化
5. 构造函数体中的代码被执行
6. 实例化完成，构造函数返回

这种情况和无继承情况之间唯一的真正区别是，在派生类的构造函数做任何实质性的事情之前，必须首先调用基类构造函数。Base构造函数设置对象的Base部分，然后控制返回给派生类构造函数，这时才允许派生类构造函数完成其作业。

***
## 初始化基类成员

我们所编写的Derived类的当前缺点之一是，在创建Deriveed对象时无法初始化m_id。如果在创建派生对象时，要同时设置m_cost（来自对象的Derived部分）和m_id（来自对象中的Base部分），该怎么办？

新程序员通常尝试如下解决此问题：

```C++
class Derived: public Base
{
public:
    double m_cost {};

    Derived(double cost=0.0, int id=0)
        // 无法工作
        : m_cost{ cost }
        , m_id{ id }
    {
    }

    double getCost() const { return m_cost; }
};
```

这是一个很好的尝试，几乎是正确的想法。我们确实需要向构造函数中添加另一个参数，否则C++将无法知道要将m_id初始化为什么值。

然而，C++不允许在构造函数的成员设定项列表中设置继承来的成员变量。换句话说，成员变量的值只能在属于与变量相同的类的构造函数的成员设定项列表中设置。

C++为什么要这样做？答案与常量和引用变量有关。考虑如果m_id为常量会发生什么？由于常量必须在创建时用值初始化，因此基类构造函数必须在创建变量时设置其值。然而，当基类构造函数完成时，派生类构造函数的成员设定项列表随后被执行。这样，每个派生类都有机会修改该变量，并可能更改其值！通过将变量的初始化限制为这些变量所属的类的构造函数，C++确保所有变量只初始化一次。

最终结果是，上面的示例无法工作，因为m_id是从Base继承的，在成员设定项列表中只能初始化非继承而来的变量。

然而，继承而来的变量仍然可以构造函数的主体中更改其值。因此，新程序员也经常尝试这样做：

```C++
class Derived: public Base
{
public:
    double m_cost {};

    Derived(double cost=0.0, int id=0)
        : m_cost{ cost }
    {
        m_id = id;
    }

    double getCost() const { return m_cost; }
};
```

虽然在这种情况下这实际上是可行的，但如果m_id是常量或引用，则它将无法工作（因为常量值和引用必须在构造函数的成员设定项列表中初始化）。它也是低效的，因为m_id被设置了两次值：一次在基类构造函数的成员设定项列表中，一次在派生类构造函数的主体中。最后，如果基类在构造期间需要使用该值，该怎么办？将无法访问它，因为它直到Derived的构造函数被执行时才被设置（这几乎是最后发生的）。

那么，在创建派生类对象时，如何正确初始化m_id？

在迄今为止的所有示例中，当我们实例化Derived类对象时，Base部分是使用默认的Base构造函数创建的。为什么它总是使用默认的Base构造函数？因为我们从来没有告诉它不要这样做！

幸运的是，C++使我们能够显式地选择将调用哪个基类构造函数！为此，只需在派生类的成员初始值设定项列表中添加对基类构造函数的调用：

```C++
class Derived: public Base
{
public:
    double m_cost {};

    Derived(double cost=0.0, int id=0)
        : Base{ id } // 使用 id 调用 Base(int) 构造函数!
        , m_cost{ cost }
    {
    }

    double getCost() const { return m_cost; }
};
```

现在，当我们执行此代码时：

```C++
#include <iostream>

int main()
{
    Derived derived{ 1.3, 5 }; // 使用 Derived(double, int) 构造函数
    std::cout << "Id: " << derived.getId() << '\n';
    std::cout << "Cost: " << derived.getCost() << '\n';

    return 0;
}
```

基类构造函数 Base(int) 用于将m_id初始化为5，派生类构造函数用于将m_cost初始化为1.3！

因此，程序将打印：

```C++
Id: 5
Cost: 1.3
```

更详细地说，下面是发生的情况：

1. 分配derived的内存
2. Derived(double, int) 构造函数被调用，cost = 1.3, id = 5.
3. 编译器看到，这里调用基类的构造函数 Base(int)，id = 5
4. 基类构造函数执行成员初始化列表，将 m_id 设置为 5
5. 基类构造函数的函数体执行，这里为空，不发生任何事情
6. 从基类构造函数返回
7. 派生类构造函数执行成员初始化列表，将 m_cost 设置为 1.3
8. 派生类构造函数的函数体执行，这里为空，不发生任何事情
9. 派生类构造函数返回

这看起来有点复杂，但实际上非常简单。所发生的一切是，Derived构造函数正在调用特定的Base构造函数来初始化对象的Base部分。由于m_id位于对象的Base部分，因此Base构造函数是唯一可以且应该初始化该值的构造函数。

注意，在Derived构造函数成员设定项列表中的何处调用Base构造函数并不重要——它总是首先执行。

***
## 将成员变量设置为private

我们已经知道了如何初始化基类成员，现在没有必要将成员变量保持为public的。我们再次将成员变量设置为private的，这是应该的。

任何人都可以访问public成员。private成员只能由同一类的成员函数访问。注意，这意味着派生类不能直接访问基类的private成员！派生类将需要使用访问函数来访问基类的私有成员。

参考以下示例：

```C++
#include <iostream>

class Base
{
private: // 成员现在设置为 private
    int m_id {};
 
public:
    Base(int id=0)
        : m_id{ id }
    {
    }
 
    int getId() const { return m_id; }
};

class Derived: public Base
{
private: // 成员现在是 private
    double m_cost;

public:
    Derived(double cost=0.0, int id=0)
        : Base{ id } // 使用 id 调用 Base(int) 构造函数
        , m_cost{ cost }
    {
    }

    double getCost() const { return m_cost; }
};

int main()
{
    Derived derived{ 1.3, 5 }; // 使用 Derived(double, int) 构造函数
    std::cout << "Id: " << derived.getId() << '\n';
    std::cout << "Cost: " << derived.getCost() << '\n';

    return 0;
}
```

在上面的代码中，我们将m_id和m_cost设置为private。这很好，因为我们使用相关的构造函数来初始化它们，并使用public访问函数来获取值。

按预期打印：

```C++
Id: 5
Cost: 1.3
```

在下一课中，我们将详细讨论访问说明符。

***
## 另一个例子

让我们看一看以前使用过的另一个类：

```C++
#include <string>
#include <string_view>

class Person
{
public:
    std::string m_name;
    int m_age {};

    Person(std::string_view name = "", int age = 0)
        : m_name{ name }, m_age{ age }
    {
    }

    const std::string& getName() const { return m_name; }
    int getAge() const { return m_age; }
};

// BaseballPlayer public 继承 Person
class BaseballPlayer : public Person
{
public:
    double m_battingAverage {};
    int m_homeRuns {};

    BaseballPlayer(double battingAverage = 0.0, int homeRuns = 0)
       : m_battingAverage{ battingAverage },
         m_homeRuns{ homeRuns }
    {
    }
};
```

正如之前所写的，BaseballPlayer仅初始化其自己的成员，而不指定要使用的Person构造函数。这意味着我们创建的每个BaseballPlayer都将使用默认的Person构造函数，该构造函数将m_age初始化为空，m_age初始化为0。因为在创建棒球运动员时为其指定名称和年龄是有意义的，所以我们应该修改此构造函数以添加这些参数。

下面是使用私有成员更新的类，其中BaseballPlayer类调用适当的Person构造函数来初始化继承的Person成员变量：

```C++
#include <iostream>
#include <string>
#include <string_view>

class Person
{
private:
    std::string m_name;
    int m_age {};

public:
    Person(std::string_view name = "", int age = 0)
        : m_name{ name }, m_age{ age }
    {
    }

    const std::string& getName() const { return m_name; }
    int getAge() const { return m_age; }

};
// BaseballPlayer public 继承 Person
class BaseballPlayer : public Person
{
private:
    double m_battingAverage {};
    int m_homeRuns {};

public:
    BaseballPlayer(std::string_view name = "", int age = 0,
        double battingAverage = 0.0, int homeRuns = 0)
        : Person{ name, age } // 调用 Person(std::string_view, int) 来初始化对应的成员
        , m_battingAverage{ battingAverage }, m_homeRuns{ homeRuns }
    {
    }

    double getBattingAverage() const { return m_battingAverage; }
    int getHomeRuns() const { return m_homeRuns; }
};
```

现在我们可以创建这样的BaseballPlayer：

```C++
#include <iostream>

int main()
{
    BaseballPlayer pedro{ "Pedro Cerrano", 32, 0.342, 42 };

    std::cout << pedro.getName() << '\n';
    std::cout << pedro.getAge() << '\n';
    std::cout << pedro.getBattingAverage() << '\n';
    std::cout << pedro.getHomeRuns() << '\n';

    return 0;
}
```

输出：

```C++
Pedro Cerrano
32
0.342
42
```

正如您可以看到的，基类的名称和年龄已经正确初始化，派生类的m_battingAverage和m_homeRuns也是如此。

***
## 继承链

继承链中的类的工作方式完全相同。

```C++
#include <iostream>

class A
{
public:
    A(int a)
    {
        std::cout << "A: " << a << '\n';
    }
};

class B: public A
{
public:
    B(int a, double b)
    : A{ a }
    {
        std::cout << "B: " << b << '\n';
    }
};

class C: public B
{
public:
    C(int a, double b, char c)
    : B{ a, b }
    {
        std::cout << "C: " << c << '\n';
    }
};

int main()
{
    C c{ 5, 4.3, 'R' };

    return 0;
}
```

在这个例子中，类C是从类B派生的，类B是从类A派生的。那么，当我们实例化类C的对象时会发生什么呢？

首先，main()调用C(int，double，char)。C构造函数调用B(int，double)。B构造函数调用A(int)。因为A不从任何人继承，这是我们要构造的第一个类。构造A，打印值5，并返回给B。构造B，打印值4.3，并将控制返回给C。构造C，打印值“R”，然后将控制返回到main()。就此结束！

因此，该程序打印：

```C++
A: 5
B: 4.3
C: R
```

值得一提的是，构造函数只能调用其直接父类的构造函数。因此，C构造函数不能直接调用或传递参数给A构造函数。C构造函数只能调用B构造函数（B来负责调用A构造函数）。

***
## 析构函数

当派生类被销毁时，每个析构函数都以与构造相反的顺序调用。在上面的例子中，当c被销毁时，首先调用c析构函数，然后调用B析构函数和A析构函数。

{{< alert success >}}
**警告**

如果基类具有虚函数，则析构函数也应该是虚函数的，否则在某些情况下，将导致未定义的行为。

{{< /alert >}}

***
## 总结

构造派生类时，派生类构造函数负责确定调用哪个基类构造函数。如果未指定基类构造函数，则将使用默认的基类构造函数。在这种情况下，如果找不到默认基类构造函数，编译器将提示错误。然后，按照从最初的基类到最终的派生类执行构造。

现在，您已经足够了解C++继承，可以创建自己的继承类了！

***