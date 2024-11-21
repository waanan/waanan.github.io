---
title: "指向派生对象的基类指针和引用"
date: 2024-11-04T13:14:53+08:00
---

在前一章中，我们学习了如何使用继承从现有类去派生新类。在本章中，我们将关注继承最重要和最强大的方面之一——虚函数。

但在讨论什么是虚函数之前，让我们首先看下为什么需要虚函数。

在创建派生类时，它由多个部分组成：继承来基类的部分，自身的部分。

例如，这里有一个简单的例子：

```C++
#include <string_view>

class Base
{
protected:
    int m_value {};

public:
    Base(int value)
        : m_value{ value }
    {
    }

    std::string_view getName() const { return "Base"; }
    int getValue() const { return m_value; }
};

class Derived: public Base
{
public:
    Derived(int value)
        : Base{ value }
    {
    }

    std::string_view getName() const { return "Derived"; }
    int getValueDoubled() const { return m_value * 2; }
};
```

当我们创建Derived对象时，它包含Base部分（首先构造）和Derived部分（其次构造）。记住，继承意味着两个类之间的is-a关系。由于Base是基础，因此Derived包含Base部分是适当的。

***
## 指针、引用和派生类

应该很直观，我们可以设置对派生对象的指针和引用：

```C++
#include <iostream>

int main()
{
    Derived derived{ 5 };
    std::cout << "derived is a " << derived.getName() << " and has value " << derived.getValue() << '\n';

    Derived& rDerived{ derived };
    std::cout << "rDerived is a " << rDerived.getName() << " and has value " << rDerived.getValue() << '\n';

    Derived* pDerived{ &derived };
    std::cout << "pDerived is a " << pDerived->getName() << " and has value " << pDerived->getValue() << '\n';

    return 0;
}
```

这会产生以下输出：

```C++
derived is a Derived and has value 5
rDerived is a Derived and has value 5
pDerived is a Derived and has value 5
```

然而，由于Derived有一个Base部分，一个更有趣的问题是，C++是否允许我们设置对Derived对象的Base指针或引用。事实证明，是可以的。

```C++
#include <iostream>

int main()
{
    Derived derived{ 5 };

    // 下面都是合法的!
    Base& rBase{ derived }; // rBase 是 左值引用
    Base* pBase{ &derived };

    std::cout << "derived is a " << derived.getName() << " and has value " << derived.getValue() << '\n';
    std::cout << "rBase is a " << rBase.getName() << " and has value " << rBase.getValue() << '\n';
    std::cout << "pBase is a " << pBase->getName() << " and has value " << pBase->getValue() << '\n';

    return 0;
}
```

这会产生结果：

```C++
derived is a Derived and has value 5
rBase is a Base and has value 5
pBase is a Base and has value 5
```

这个结果可能不是您最初期望的那样！

由于rBase和pBase是Base引用和指针，因此它们只能看到Base的成员（或Base继承的基类，即使派生对象的Derived::getName() 覆盖了Base::getName()。因此，它们调用Base::getName()，这就是rBase和pBase它们是Base而不是Derived的原因。

请注意，这也意味着不能使用rBase或pBase调用Derived::getValueDoubled()。他们看不到任何Derived中的内容。

这里是另一个稍微复杂一些的示例，我们将在下一课中继续使用：

```C++
#include <iostream>
#include <string_view>
#include <string>

class Animal
{
protected:
    std::string m_name;

    // 将构造函数设置为 protected
    // 因为我们不想Animal被直接构造
    // 但是派生类仍然可以使用
    Animal(std::string_view name)
        : m_name{ name }
    {
    }

    Animal(const Animal&) = delete;
    Animal& operator=(const Animal&) = delete;

public:
    std::string_view getName() const { return m_name; }
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

int main()
{
    const Cat cat{ "Fred" };
    std::cout << "cat is named " << cat.getName() << ", and it says " << cat.speak() << '\n';

    const Dog dog{ "Garbo" };
    std::cout << "dog is named " << dog.getName() << ", and it says " << dog.speak() << '\n';

    const Animal* pAnimal{ &cat };
    std::cout << "pAnimal is named " << pAnimal->getName() << ", and it says " << pAnimal->speak() << '\n';

    pAnimal = &dog;
    std::cout << "pAnimal is named " << pAnimal->getName() << ", and it says " << pAnimal->speak() << '\n';

    return 0;
}
```

这产生结果：

```C++
cat is named Fred, and it says Meow
dog is named Garbo, and it says Woof
pAnimal is named Fred, and it says ???
pAnimal is named Garbo, and it says ???
```

我们在这里看到了相同的问题。因为pAnimal是一个Animal指针，所以它只能看到类的Animal部分。因此，pAnimal->speak()调用Animal::speak。

***
## 使用指向基类的指针和引用

现在您可能会说，“上面的示例似乎有点傻。当使用派生对象时，为什么要设置指向派生对象基类的指针或引用？”事实证明，有许多很好的原因。

首先，假设您想编写一个打印动物名称和声音的函数。如果不使用指向基类的指针，则必须使用重载函数来编写它，例如：

```C++
void report(const Cat& cat)
{
    std::cout << cat.getName() << " says " << cat.speak() << '\n';
}

void report(const Dog& dog)
{
    std::cout << dog.getName() << " says " << dog.speak() << '\n';
}
```

看起来很简单，但是如果有30种不同的动物，会发生什么？必须编写30个几乎相同的函数！另外，如果你添加了一种新的动物，你也必须为它编写一个新函数。考虑到唯一真正的区别是参数的类型，这是一种巨大的时间浪费。

而且，由于猫和狗是从动物中衍生出来的，猫和狗都有动物的部分。因此，我们应该能够做这样的事情：

```C++
void report(const Animal& rAnimal)
{
    std::cout << rAnimal.getName() << " says " << rAnimal.speak() << '\n';
}
```

这将允许我们传入从Animal派生的任何类，甚至是我们在编写函数后创建的类！不是每个派生类一个函数，而是得到一个可以与从Animal派生的所有类一起工作的函数！

当然，问题是，由于rAnimal是一个Animal引用，因此rAnimal.speak()将调用Animal::speak。

其次，假设您有3只猫和3只狗，您希望将它们放在一个数组中以便于访问。由于数组只能保存一种类型的对象，如果没有指向基类的指针或引用，因此您必须为每个派生类型创建不同的数组，如下所示：

```C++
#include <array>
#include <iostream>

// 上面例子中的 Cat 和 Dog 

int main()
{
    const auto& cats{ std::to_array<Cat>({{ "Fred" }, { "Misty" }, { "Zeke" }}) };
    const auto& dogs{ std::to_array<Dog>({{ "Garbo" }, { "Pooky" }, { "Truffle" }}) };

    // 在 C++20 以前
    // const std::array<Cat, 3> cats{{ { "Fred" }, { "Misty" }, { "Zeke" } }};
    // const std::array<Dog, 3> dogs{{ { "Garbo" }, { "Pooky" }, { "Truffle" } }};

    for (const auto& cat : cats)
    {
        std::cout << cat.getName() << " says " << cat.speak() << '\n';
    }

    for (const auto& dog : dogs)
    {
        std::cout << dog.getName() << " says " << dog.speak() << '\n';
    }

    return 0;
}
```

现在，考虑一下如果你有30种不同类型的动物会发生什么。你需要30个数组，每种动物一个！然而，由于猫和狗都是从Animal派生而来的，因此我们应该能够这样做：

```C++
#include <array>
#include <iostream>

// 上面例子中的 Cat 和 Dog 

int main()
{
    const Cat fred{ "Fred" };
    const Cat misty{ "Misty" };
    const Cat zeke{ "Zeke" };

    const Dog garbo{ "Garbo" };
    const Dog pooky{ "Pooky" };
    const Dog truffle{ "Truffle" };

    // 存储指向动物的数组，里面装着指向Cat和Dog的指针
    const auto animals{ std::to_array<const Animal*>({&fred, &garbo, &misty, &pooky, &truffle, &zeke }) };

    // 在 C++20 前, 数组大小需要显示指定
    // const std::array<const Animal*, 6> animals{ &fred, &garbo, &misty, &pooky, &truffle, &zeke };

    for (const auto animal : animals)
    {
        std::cout << animal->getName() << " says " << animal->speak() << '\n';
    }

    return 0;
}
```

在编译和执行时，不幸的是，数组“animals”的每个元素都是指向Animal的指针，这意味着Animal->speak()将调用Animal::speak。

输出是:

```C++
Fred says ???
Garbo says ???
Misty says ???
Pooky says ???
Truffle says ???
Zeke says ???
```

这两种技术都可以为我们节省大量的时间和精力，但它们有相同的问题。基类的指针或引用调用函数的基类版本，而不是派生类版本。需要有某种方法可以使这些基类指针调用函数的派生类版本而不是基类版本。

现在，想猜一猜虚函数是用于什么目的？

***