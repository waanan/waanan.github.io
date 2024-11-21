---
title: "虚函数和多态"
date: 2024-11-04T13:14:53+08:00
---

在上一课中，我们看了一些使用基类指针或引用指向派生类里例子，这有可能简化代码。然而，在每种情况下，都会遇到问题，即基类指针或引用只能调用函数的基类版本，而不能调用派生类版本。

以下是这种行为的一个简单示例：

```C++
#include <iostream>
#include <string_view>

class Base
{
public:
    std::string_view getName() const { return "Base"; }
};

class Derived: public Base
{
public:
    std::string_view getName() const { return "Derived"; }
};

int main()
{
    Derived derived {};
    Base& rBase{ derived };
    std::cout << "rBase is a " << rBase.getName() << '\n';

    return 0;
}
```

打印：

```C++
rBase is a Base
```

因为rBase是一个Base引用，所以它调用Base::getName()，即使它实际上引用了Derived对象的Base部分。

在本课中，我们将展示如何使用虚函数来解决这个问题。

***
## 虚函数

虚函数是一种特殊类型的成员函数，当被调用时，它解析为被引用或指向的对象的实际类型函数的最底层派生版本。

如果派生函数具有与函数的基类版本相同的签名（名称、参数类型以及是否为const）和返回类型，则认为它是匹配的。这些行为称为「覆盖」。

要使函数虚拟化，只需将“virtual”关键字放在函数声明之前。

下面是上面程序带有虚函数的示例：

```C++
#include <iostream>
#include <string_view>

class Base
{
public:
    virtual std::string_view getName() const { return "Base"; } // 注：这里添加了 virtual 关键字
};

class Derived: public Base
{
public:
    virtual std::string_view getName() const { return "Derived"; }
};

int main()
{
    Derived derived {};
    Base& rBase{ derived };
    std::cout << "rBase is a " << rBase.getName() << '\n';

    return 0;
}
```

这打印：

```C++
rBase is a Derived
```

一些现代编译器可能会报错，类具有虚函数和可访问的非虚析构函数。如果是这样，请向基类添加一个虚析构函数。在上述程序中，将以下内容添加到Base的定义中：

```C++
virtual ~Base() = default;
```

因为rBase是对Derived对象的Base部分的引用，所以当对rBase.getName()计算时，它通常会解析为Base::getName()。然而，Base::getName()是虚函数，程序会去看看是否有更底层的派生版本的函数可用于派生对象。在这种情况下，它将解析为Derived::getName()！

让我们来看一个稍微复杂一些的例子：

```C++
#include <iostream>
#include <string_view>

class A
{
public:
    virtual std::string_view getName() const { return "A"; }
};

class B: public A
{
public:
    virtual std::string_view getName() const { return "B"; }
};

class C: public B
{
public:
    virtual std::string_view getName() const { return "C"; }
};

class D: public C
{
public:
    virtual std::string_view getName() const { return "D"; }
};

int main()
{
    C c {};
    A& rBase{ c };
    std::cout << "rBase is a " << rBase.getName() << '\n';

    return 0;
}
```

你认为这个程序会输出什么？

让我们看看这是如何工作的。首先，我们实例化一个C类对象。rBase是一个A引用，我们将其设置为引用C对象的A部分。最后，我们调用rBase.getName()。rBase.getName()的计算结果为A::getName()。但是，A::getName()是虚函数，因此编译器将调用A和C之间最底层派生的匹配。在这种情况下，就是C::getName()。请注意，它不会调用D::getName（），因为我们的原始对象是C，而不是D，所以只考虑A和C之间的函数。

因此，我们的程序输出：

```C++
rBase is a C
```

请注意，虚函数解析仅在通过指针或对类类型对象的引用调用虚成员函数时有效。因为编译器可以区分指针或引用的类型与指向或被引用的对象的类型。我们在上面的例子中看到了这一点。

直接在对象上调用虚成员函数（不通过指针或引用）将始终调用属于该对象同一类型的成员函数。例如：

```C++
C c{};
std::cout << c.getName(); // 会永远调用 C::getName

A a { c }; // 将 c 的 A 部分 拷贝给 a (不要写这样的代码)
std::cout << a.getName(); // 会永远调用 A::getName
```

***
## 多态

在编程中，多态性是指一个实体具有多种形式的能力（术语“多态性”字面意思是“多种形式”）。例如，考虑以下两个函数声明：

```C++
int add(int, int);
double add(double, double);
```

标识符add有两种形式：add(int, int) 和 add(double, double)。

「编译时多态」是指编译器解析的多态形式。这些包括函数重载解析和模板解析。

「运行时多态」是指在运行时解析的多态形式。这包括虚函数解析。

***
## 更复杂的例子

让我们再看一下上一课中使用的动物示例。这是原始的类，以及一些测试代码：

```C++
#include <iostream>
#include <string>
#include <string_view>

class Animal
{
protected:
    std::string m_name {};

    // 将构造函数设置为 protected
    // 因为我们不想Animal被直接构造
    // 但是派生类仍然可以使用
    Animal(std::string_view name)
        : m_name{ name }
    {
    }

public:
    const std::string& getName() const { return m_name; }
    std::string_view speak() const { return "???"; }
};

class Cat: public Animal
{
public:
    Cat(std::string_view name)
        : Animal{ name }
    {
    }

    std::string_view speak() const { return "Meow"; }
};

class Dog: public Animal
{
public:
    Dog(std::string_view name)
        : Animal{ name }
    {
    }

    std::string_view speak() const { return "Woof"; }
};

void report(const Animal& animal)
{
    std::cout << animal.getName() << " says " << animal.speak() << '\n';
}

int main()
{
    Cat cat{ "Fred" };
    Dog dog{ "Garbo" };

    report(cat);
    report(dog);

    return 0;
}
```

这打印：

```C++
Fred says ???
Garbo says ???
```

以下是speak()函数变为虚函数的类：

```C++
#include <iostream>
#include <string>
#include <string_view>

class Animal
{
protected:
    std::string m_name {};

    // 将构造函数设置为 protected
    // 因为我们不想Animal被直接构造
    // 但是派生类仍然可以使用
    Animal(std::string_view name)
        : m_name{ name }
    {
    }

public:
    const std::string& getName() const { return m_name; }
    virtual std::string_view speak() const { return "???"; }
};

class Cat: public Animal
{
public:
    Cat(std::string_view name)
        : Animal{ name }
    {
    }

    virtual std::string_view speak() const { return "Meow"; }
};

class Dog: public Animal
{
public:
    Dog(std::string_view name)
        : Animal{ name }
    {
    }

    virtual std::string_view speak() const { return "Woof"; }
};

void report(const Animal& animal)
{
    std::cout << animal.getName() << " says " << animal.speak() << '\n';
}

int main()
{
    Cat cat{ "Fred" };
    Dog dog{ "Garbo" };

    report(cat);
    report(dog);

    return 0;
}
```

这打印：

```C++
Fred says Meow
Garbo says Woof
```

按预期执行！

当计算animal.speak()时，程序会注意到animal::speak()是一个虚函数。在animal引用Cat对象的animal部分的情况下，程序会查看animal和Cat之间的所有类，看看是否可以找到更底层派生的函数。在这种情况下，它会找到Cat::speak()。在animal引用Dog对象的animal部分的情况下，程序将函数调用解析为Dog::speak()。

请注意，我们没有将Animal::getName()设置为virtual。这是因为getName()在任何派生类中都不会被重写，因此没有必要。

同样，以下数组示例现在按预期工作：

```C++
Cat fred{ "Fred" };
Cat misty{ "Misty" };
Cat zeke{ "Zeke" };

Dog garbo{ "Garbo" };
Dog pooky{ "Pooky" };
Dog truffle{ "Truffle" };

// 存储指向动物的数组，里面装着指向Cat和Dog的指针
Animal* animals[]{ &fred, &garbo, &misty, &pooky, &truffle, &zeke };

for (const auto* animal : animals)
    std::cout << animal->getName() << " says " << animal->speak() << '\n';
```

这打印：

```C++
Fred says Meow
Garbo says Woof
Misty says Meow
Pooky says Woof
Truffle says Woof
Zeke says Meow
```

尽管这两个例子只使用了Cat和Dog，但我们从Animal派生的任何其他类也可以与我们的report()函数和Animal数组一起使用，而无需进一步修改！这可能是虚拟函数的最大好处——能够以一种新派生类可以自动使用旧代码而无需修改的方式构建程序！

警告：为了使用派生类函数，派生类函数的签名必须与基类虚函数的签名完全匹配。如果派生类函数具有不同的参数类型，程序可能仍然可以很好地编译，但虚函数不会按预期解析。在下一课中，我们将讨论如何防范这种情况。

请注意，如果一个函数被标记为virtual，则派生类中的所有匹配的重载函数也都会被隐式地视为virtual，即使它们没有被显式地标记为virtual。

反之则不然——派生类中的virtual重载不会隐式地使基类函数成为virtual的。

***
## 虚函数的返回类型

在正常情况下，虚函数的返回类型及其重载必须匹配。考虑以下示例：

```C++
class Base
{
public:
    virtual int getValue() const { return 5; }
};

class Derived: public Base
{
public:
    virtual double getValue() const { return 6.78; }
};
```

在这种情况下，Derived::getValue()不被视为Base::getValue()的匹配重载，编译将失败。

***
## 不要从构造函数或析构函数调用虚函数

这是另一个经常抓住毫无戒心的新程序员的陷阱。你不应该从构造函数或析构函数调用虚函数。为什么？

请记住，创建派生类时，首先构造Base部分。如果你从Base构造函数调用一个虚拟函数，而类的Derived部分甚至还没有创建，它将无法调用该函数的Derived版本，因为Derived函数没有Derived对象部分可供处理。在C++中，它将调用Base版本。

析构函数也存在类似的问题。如果在基类析构函数中调用虚函数，它将始终解析为函数的基类版本，因为类的派生部分已经被销毁。

***
## 虚函数的缺点

既然大多数时候你都希望你的函数是virtual的，为什么不把所有功能都virtual化呢？答案是：因为它效率低下——解析虚拟函数调用比解析常规函数调用需要更长的时间。此外，编译器还必须为每个具有一个或多个虚函数的类对象分配一个额外的指针。我们将在本章的后续课程中对此进行更多讨论。

***