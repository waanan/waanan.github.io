---
title: "虚析构函数、虚赋值函数以及虚函数重写"
date: 2024-11-04T13:14:53+08:00
---

## 虚析构函数

尽管C++为类提供了默认析构函数，但有时您会希望提供自己的析构函数，特别是当类需要释放内存时。如果处理继承，则应该始终使析构函数成为虚函数。考虑以下示例：

```C++
#include <iostream>
class Base
{
public:
    ~Base() // 注: 非 virtual
    {
        std::cout << "Calling ~Base()\n";
    }
};

class Derived: public Base
{
private:
    int* m_array {};

public:
    Derived(int length)
      : m_array{ new int[length] }
    {
    }

    ~Derived() // 注: 非 virtual (您的编译器可能会因此有警告)
    {
        std::cout << "Calling ~Derived()\n";
        delete[] m_array;
    }
};

int main()
{
    Derived* derived { new Derived(5) };
    Base* base { derived };

    delete base;

    return 0;
}
```

注意：如果编译上面的示例，编译器可能会警告您有关非虚析构函数的信息（这是本例中有意设置的）。您可能需要禁用「将警告视为错误」的编译器选项才能编译通过。

由于base是Base指针，因此在“delete base;”时，程序会查看base析构函数是否是虚函数。它不是，因此它假设它只需要调用Base析构函数。我们可以从上面的示例打印的事实中看到这一点：

```C++
Calling ~Base()
```

然而，我们确实希望delete函数调用Derived的析构函数（它将随后调用Base的析构函数），否则m_array将不会被删除。通过将Base的析构函数设置为virtual可以实现这一点:

```C++
#include <iostream>
class Base
{
public:
    virtual ~Base() // note: virtual
    {
        std::cout << "Calling ~Base()\n";
    }
};

class Derived: public Base
{
private:
    int* m_array {};

public:
    Derived(int length)
      : m_array{ new int[length] }
    {
    }

    virtual ~Derived() // note: virtual
    {
        std::cout << "Calling ~Derived()\n";
        delete[] m_array;
    }
};

int main()
{
    Derived* derived { new Derived(5) };
    Base* base { derived };

    delete base;

    return 0;
}
```

现在，该程序产生以下结果：

```C++
Calling ~Derived()
Calling ~Base()
```

与普通virtual成员函数一样，如果基类函数是虚函数，则所有派生类的重写都将被视为虚函数。没有必要仅为了将其标记为virtual而创建空的派生类析构函数。

请注意，如果希望基类具有一个为空的虚析构函数，则可以这样定义析构函数：

```C++
virtual~base（）=default；//生成虚拟默认析构函数
```

## 虚赋值函数

可以使赋值运算符成为virtual的。然而，与析构函数的情况不同，virtual赋值操作符确实可能会造成大量的bug，并进入了本教程范围之外的一些高级主题。因此，为了简单起见，我们建议您暂时不要考虑这种情况。

## 忽略virtual

有一些很少的情况，您可能希望忽略函数的虚拟化。例如，考虑以下代码：

```C++
#include <string_view>
class Base
{
public:
    virtual ~Base() = default;
    virtual std::string_view getName() const { return "Base"; }
};

class Derived: public Base
{
public:
    virtual std::string_view getName() const { return "Derived"; }
};
```

在某些情况下，您可能希望指向Derived对象的Base指针调用Base::getName()，而不是Derived::getName()。为此，只需使用域解析操作符：

```C++
#include <iostream>
int main()
{
    Derived derived {};
    const Base& base { derived };

    // 调用 Base::getName() 而不是 Derived::getName()
    std::cout << base.Base::getName() << '\n';

    return 0;
}
```

您可能不会经常使用它，但知道至少是可以实现的。

## 应该让所有的析构函数都是virtual的吗？

这是新程序员常见的问题。如上面的示例所述，如果基类析构函数未标记为virtual，则稍后删除指向派生对象的基类指针，则程序有泄漏内存的风险。避免这种情况的一种方法是将所有析构函数标记为虚拟的。但应该这样做吗？

说“是”很容易，因此您以后可以使用任何类作为基类——但这样做会降低性能（将virtual指针添加到类的每个实例）。因此，你必须平衡成本，以及你的意图。

我们建议如下：如果类没有显式地设计为基类，那么通常最好没有虚拟成员和虚析构函数。该类仍然可以通过组合使用。如果类被设计为用作基类和/或具有任何虚函数，则它应该始终具有虚析构函数。

如果决定使类不可继承，那么下一个问题是，是否可以强制执行这一点。

传统智慧（正如备受推崇的C++专家Herb Sutter最初提出的那样）建议避免非虚析构函数内存泄漏情况，如下所示：“基类析构函数应该是public的和virtual的，或者是protected的和非virtual的。”不能使用基类指针删除具有protected的析构函数的基类，这阻止了通过基类指针来删除派生类对象。

不幸的是，这也阻止了外部对基类析构函数的任何使用。这意味着：
1. 我们不应该动态地分配基类对象，因为我们没有常规的方法来删除它们（有非常规的变通方法，但很恶心）。
2. 我们甚至不能静态地分配基类对象，因为当它们超出作用域时，析构函数是不可访问的。

换句话说，使用这种方法，为了使派生类安全，我们必须使基类本身实际上不可用。

既然final说明符已经引入到语言中，我们的建议如下：
1. 如果希望继承类，请确保析构函数是virtual的和public的。
2. 如果您不想任何人继承您的类，请将您的类标记为final。这将首先防止其他类从中继承，而不会对类本身施加任何其他使用限制。

***

{{< prevnext prev="/basic/chapter25/override-final/" next="/basic/chapter25/early-bind-late-bind/" >}}
25.2 override和final说明符
<--->
25.4 静态绑定和动态绑定
{{< /prevnext >}}
