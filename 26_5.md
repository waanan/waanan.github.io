---
title: "虚拟表"
date: 2024-11-04T13:14:53+08:00
---

考虑以下程序：

```C++
#include <iostream>
#include <string_view>

class Base
{
public:
    std::string_view getName() const { return "Base"; }                // not virtual
    virtual std::string_view getNameVirtual() const { return "Base"; } // virtual
};

class Derived: public Base
{
public:
    std::string_view getName() const { return "Derived"; }
    virtual std::string_view getNameVirtual() const override { return "Derived"; }
};

int main()
{
    Derived derived {};
    Base& base { derived };

    std::cout << "base has static type " << base.getName() << '\n';
    std::cout << "base has dynamic type " << base.getNameVirtual() << '\n';

    return 0;
}
```

首先，让我们看看对base.getName（）的调用。由于这是一个非虚函数，编译器可以使用实际类型的base（base）来确定（在编译时）它应该解析为base:：getName（）。

尽管它看起来几乎相同，但对base.getNameVirtual（）的调用必须以不同的方式解析。由于这是一个虚拟函数调用，编译器必须使用基的动态类型来解析调用，并且直到运行时，基的动态型才是可知的。因此，只有在运行时才能确定对base.getNameVirtual（）的此特定调用解析为Derived:：getNameVirtual。

那么，虚函数实际上是如何工作的呢？

***
## 虚拟表

C++标准没有指定应该如何实现虚拟函数（该细节由实现决定）。

然而，C++实现通常使用一种称为虚拟表的后期绑定形式来实现虚拟函数。

虚拟表是用于以动态/延迟绑定方式解析函数调用的函数的查找表。虚拟表有时使用其他名称，例如“vtable”、“虚拟函数表”、“虚方法表”或“调度表”。在C++中，虚函数解析有时称为动态调度。

由于使用虚拟函数不需要知道虚拟表的工作方式，因此可以将此部分视为可选阅读。

虚拟表实际上相当简单，尽管用语言描述它有点复杂。首先，每个使用虚拟函数的类（或从使用虚拟函数得来的类）都有一个对应的虚拟表。该表只是编译器在编译时设置的静态数组。虚拟表包含类的对象可以调用的每个虚拟函数的一个条目。该表中的每个条目都只是一个函数指针，它指向该类可以访问的最派生的函数。

其次，编译器还添加了一个隐藏指针，该指针是基类的成员，我们将其称为*__vptr*__vptr是在创建类对象时（自动）设置的，以便它指向该类的虚拟表。与this指针（它实际上是编译器用于解析自引用的函数参数）不同，*__vptr是真正的指针成员。因此，它使分配的每个类对象都增大了一个指针的大小。它还意味着*__vptr由派生类继承，这一点很重要。

现在，您可能对这些东西是如何组合在一起感到困惑，因此让我们来看一个简单的示例：

```C++
class Base
{
public:
    virtual void function1() {};
    virtual void function2() {};
};

class D1: public Base
{
public:
    void function1() override {};
};

class D2: public Base
{
public:
    void function2() override {};
};
```

因为这里有3个类，所以编译器将设置3个虚拟表：一个用于Base，一个用于D1，另一个用于D2。

编译器还向使用虚拟函数的大多数基类添加隐藏指针成员。尽管编译器会自动执行此操作，但我们将它放在下一个示例中，只是为了显示它的添加位置：

```C++
class Base
{
public:
    VirtualTable* __vptr;
    virtual void function1() {};
    virtual void function2() {};
};

class D1: public Base
{
public:
    void function1() override {};
};

class D2: public Base
{
public:
    void function2() override {};
};
```

创建类对象时，*__vptr设置为指向该类的虚拟表。例如，创建Base类型的对象时，*__vptr设置为指向Base的虚拟表。构造D1或D2类型的对象时，*__vptr被设置为分别指向D1或D1的虚拟表。

现在，让我们讨论如何填写这些虚拟表。因为这里只有两个虚拟函数，所以每个虚拟表都有两个条目（一个用于function1（），另一个用于function2（））。请记住，当填充这些虚拟表时，每个条目都用该类类型的对象可以调用的最派生的函数填充。

基本对象的虚拟表很简单。Base类型的对象只能访问Base的成员。基地无权访问D1或D2功能。因此，function1的条目指向Base:：function1（），function 2的条目指向Base:：function2（）。

D1的虚拟表稍微复杂一些。类型D1的对象可以访问D1和Base的成员。然而，D1重写了function1（），使D1:：functionl（）比Base:：fuction1（）派生得多。因此，function1的条目指向D1:：function1（）。D1尚未重写function2（），因此function2中的条目将指向Base:：function2.（）。

D2的虚拟表类似于D1，只是函数1的条目指向Base:：function1（），函数2的条目指向D2:：fuction2（）。

下面是这方面的图片：



尽管这个图看起来有点疯狂，但它确实非常简单：每个类中的*__vptr指向该类的虚拟表。虚拟表中的条目指向允许该类的对象调用的函数的最派生版本。

因此，请考虑创建D1类型的对象时会发生什么：

```C++
int main()
{
    D1 d1 {};
}
```

由于d1是d1对象，因此d1将其*__vptr设置为d1虚拟表。

现在，让我们将基本指针设置为D1：

```C++
int main()
{
    D1 d1 {};
    Base* dPtr = &d1;

    return 0;
}
```

请注意，由于dPtr是基指针，因此它仅指向d1的base部分。然而，还要注意*__vptr位于类的Base部分，因此dPtr可以访问该指针。最后，注意dPtr->__vptr指向D1虚拟表！因此，即使dPtr是Base*类型，它仍然可以访问D1的虚拟表（通过__vptr）。

那么，当我们试图调用dPtr->function1（）时会发生什么呢？

```C++
int main()
{
    D1 d1 {};
    Base* dPtr = &d1;
    dPtr->function1();

    return 0;
}
```

首先，程序识别function1（）是一个虚函数。其次，程序使用dPtr->__vptr来访问D1的虚拟表。第三，它在D1的虚拟表中查找要调用的function1（）的哪个版本。已将其设置为D1:：function1（）。因此，dPtr->function1（）解析为D1:：functionl（）！

现在，您可能会说，“但如果dPtr确实指向Base对象而不是D1对象，它还会调用D1:：function1（）吗？”。答案是否定的。

```C++
int main()
{
    Base b {};
    Base* bPtr = &b;
    bPtr->function1();

    return 0;
}
```

在这种情况下，当创建b时，b.__vptr指向Base的虚拟表，而不是D1的虚拟表格。由于bPtr指向b，因此bPtr->__vptr也指向Base的虚拟表。function1（）的Base虚拟表条目指向Base:：function1。因此，bPtr->function1（）解析为Base:：function2（），这是Base对象应该能够调用的functionl（）的最派生版本。

通过使用这些表，编译器和程序能够确保函数调用解析为适当的虚函数，即使您只使用指向基类的指针或引用！

由于几个原因，调用虚拟函数比调用非虚拟函数慢：首先，我们必须使用*__vptr来访问适当的虚拟表。其次，我们必须索引虚拟表，以找到要调用的正确函数。只有这样，我们才能调用函数。因此，我们必须执行3个操作才能找到要调用的函数，而不是对普通间接函数调用执行2个操作，或对直接函数调用执行一个操作。然而，对于现代计算机，这种增加的时间通常是相当微不足道的。

另外，作为提醒，任何使用虚拟函数的类都有一个*__vptr，因此该类的每个对象都将大一个指针。虚拟功能很强大，但它们确实有性能成本。

