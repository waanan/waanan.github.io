---
title: "向派生类添加新功能"
date: 2024-10-08T17:45:57+08:00
---

使用派生类的最大好处之一是能够重用已经编写的代码。您可以继承基类功能，然后添加新功能、修改现有功能或隐藏不需要的功能。在这节课和接下来的几节课中，我们将更仔细地了解每一件事情是如何完成的。

首先，让我们从一个简单的基类开始：

```C++
#include <iostream>

class Base
{
protected:
    int m_value {};

public:
    Base(int value)
        : m_value { value }
    {
    }

    void identify() const { std::cout << "I am a Base\n"; }
};
```

现在，让我们创建一个从Base继承的派生类。因为我们希望派生类能够在实例化对象时设置m_value的值，所以我们将在Derived构造函数初始化列表中调用Base构造函数。

```C++
class Derived: public Base
{
public:
    Derived(int value)
        : Base { value }
    {
    }
};
```

***
## 向派生类添加新功能

在上面的示例中，由于我们可以访问基类的源代码，因此如果需要，可以直接向Base添加功能。

有时，我们可能可以访问基类，但不想修改它。请考虑这样的情况：您使用了外部的开源库，但需要一些额外的功能。您可以添加到原始代码中，但这不是最好的解决方案。如果外部库有了更新，该怎么办？要么您的添加内容将被覆盖，要么您必须手动将它们迁移到更新中，这既耗时又有风险。

或者，有时甚至不可能修改基类。考虑标准库中的代码。我们无法修改作为标准库一部分的代码。但我们能够从这些类继承，然后将自己的功能添加到派生类中。第三方库也是如此，可能为您提供了头文件，但代码是预编译成二进制的。

在任何一种情况下，最好的答案都是派生自己的类，并将想要的功能添加到派生类中。

Base类中一个明显的遗漏是少了public访问m_value的函数。我们可以通过在Base类中添加访问函数来纠正这一点——但为了示例起见，我们将它添加到派生类中。由于m_value已在基类中声明为protected，因此Derived可以直接访问它。

要将新功能添加到派生类中，只需像正常那样在派生类中声明该功能：

```C++
class Derived: public Base
{
public:
    Derived(int value)
        : Base { value }
    {
    }

    int getValue() const { return m_value; }
};
```

现在，在类外部将能够对Derived类型的对象调用getValue()来访问m_value的值。

```C++
int main()
{
    Derived derived { 5 };
    std::cout << "derived has value " << derived.getValue() << '\n';

    return 0;
}
```

这将产生以下结果：

```C++
derived has value 5
```

尽管这可能是显而易见的，但Base类型的对象不能访问Derived中的getValue()函数。以下情况将无法工作：

```C++
int main()
{
    Base base { 5 };
    std::cout << "base has value " << base.getValue() << '\n';

    return 0;
}
```

这是因为Base中没有getValue()函数。函数getValue()属于Derived。因为Derived是Base，所以Derived可以访问Base中的内容。然而，Base无权访问Derived中的任何内容。

***