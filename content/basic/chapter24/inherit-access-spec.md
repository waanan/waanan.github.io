---
title: "继承和访问说明符"
date: 2024-10-08T17:45:57+08:00
---

在本章前面的课程中，您已经了解了一些关于继承如何工作的知识。在迄今为止的所有示例中，我们都使用了public继承。也就是说，派生类public继承基类。

在本课中，将更仔细地看一看public继承，以及其他两种类型的继承（private继承和protected继承）。还将探索不同类型的继承如何与访问说明符交互，以允许或限制对成员的访问。

之前，您已经看到了private和public访问说明符，它们决定了谁可以访问类的成员。简单回顾下，任何人都可以访问public成员。private成员只能由同一类或友元的成员函数访问。这意味着派生类不能直接访问基类的私有成员！

```C++
class Base
{
private:
    int m_private {}; // 只能被Base类的成员或者友元访问（派生类不能访问）
public:
    int m_public {}; // 任何人都可以访问
};
```

这非常简单，您现在应该已经很了解。

***
## protected访问说明符

在处理带继承的类时，事情变得有点复杂。C++有第三个访问说明符，之前没有谈到，因为它只在继承上下文中有用。protected访问说明符允许成员所属的类、友元类和派生类访问该成员。然而，不能从类外部访问protected的成员。

```C++
class Base
{
public:
    int m_public {}; // 可以被任何人访问
protected:
    int m_protected {}; // 可以被 Base 的成员, 友元, 及派生类访问
private:
    int m_private {}; // 只能被 Base 的成员和友元访问 (派生类不允许访问)
};

class Derived: public Base
{
public:
    Derived()
    {
        m_public = 1; // 允许: 派生类可以访问基类的public成员
        m_protected = 2; // 允许: 派生类可以访问基类的protected成员
        m_private = 3; // 不允许: 派生类不可以访问基类的private成员
    }
};

int main()
{
    Base base;
    base.m_public = 1; // 允许: 可以从外部访问类的public成员
    base.m_protected = 2; // 不允许: 不可以从外部访问类的protected成员
    base.m_private = 3; // 不允许: 不可以从外部访问类的private成员

    return 0;
}
```

在上面的示例中，可以看到受保护的基类成员m_protected可由派生类直接访问，但不能被外部访问。

***
## 何时应该使用protected访问说明符？

在基类中具有protected的成员时，派生类可以直接访问该成员。这意味着，如果以后更改有关protected的任何内容（类型、值的含义等），则可能需要同时更改基类和所有派生类。

当您（或您的团队）从自己的类中派生，并且派生类的数量是合理的时，使用protected访问说明符是可以的。如果您对基类的实现进行了更改，并且因此需要更新派生类，则可以自己进行更新（并且派生类的数量是有限的）。

使成员私有意味着其它类和派生类不能直接更改基类。这有助于将其它类或派生类与基类的实现更改隔离开来，并确保正确维护不变量。然而，这也意味着您的类可能需要更多的public（或protected）接口来支持外部或派生类操作所需的所有函数，这有对应的编码、测试和维护成本。

通常，如果可以，最好将成员设为私有的，并且仅在有派生类且构建和维护与其对应的public接口的成本太高时使用protected访问说明符。

***
## 不同类型的继承及其对访问的影响

类有三种不同的方式从其它类进行继承：public、protected和private。

为此，需指定要继承时的访问类型：

```C++
// 从 Base public 继承
class Pub: public Base
{
};

// 从 Base protected 继承
class Pro: protected Base
{
};

// 从 Base private 继承
class Pri: private Base
{
};

class Def: Base // 默认是 private 继承
{
};
```

如果不选择继承类型，C++默认为私有继承（就像如果不另行指定，则成员默认为私有访问一样）。

这为我们提供了9种组合：3个成员访问说明符（public、private 和 protected），以及3个继承类型（public，private 和 protected）。

那么这两者之间的区别是什么？简而言之，当继承成员时，被继承成员的访问说明符可以更改（仅在派生类中），具体取决于使用的继承类型。换句话说，在基类中是public的或protected的成员可以更改派生类中的访问说明符。

这似乎有点令人困惑，但其实并没有那么复杂。我们将在本课的其余部分详细探讨。

请先记住以下规则：

1. 类始终可以访问其自己的（非继承的）成员。
2. 成员是否是public访问，基于正在访问的类中该成员是否为public。
3. 派生类从父类继承的成员，其访问说明符取决于该成员在父类中的访问说明符和使用的继承类型。

***
## public继承

public继承是迄今为止最常用的继承类型。事实上，您很少会看到或使用其他类型的继承，因此您的主要关注点应该是理解这一部分。幸运的是，public继承也是最容易理解的。当public继承基类时，继承的public成员保持public，而继承的protected成员保持protected。继承的private成员保持不可访问，因为它们在基类中是私有的。

|  基类中的访问说明符 |  public继承时对应的派生类的访问说明符  |
|  ----  | ----  |
| Public | Public |
| Protected | Protected |
| Private | 不可访问 |

下面是一个示例：

```C++
class Base
{
public:
    int m_public {};
protected:
    int m_protected {};
private:
    int m_private {};
};

class Pub: public Base // 注: public 继承
{
    // Public 继承意味着:
    // 基类 Public 仍然保持 public (所以 m_public 是 public)
    // 基类 Protected 继承来的成员保持 protected (所以 m_protected 是 protected)
    // 基类 Private 继承来的成员 是不可访问的 (所以 m_private 不可访问)
public:
    Pub()
    {
        m_public = 1; // okay: m_public 是 public
        m_protected = 2; // okay: m_protected 是 protected
        m_private = 3; // 不 okay: 派生类中 m_private 不可访问
    }
};

int main()
{
    // 类外部进行访问
    Base base;
    base.m_public = 1; // okay: m_public 在 Base 中是 public
    base.m_protected = 2; // 不 okay: m_protected 在 Base 中是 protected
    base.m_private = 3; // 不 okay: m_private 在 Base 中是 private 

    Pub pub;
    pub.m_public = 1; // okay: m_public 在 Pub 中是 public
    pub.m_protected = 2; // 不 okay: m_protected 在 Pub 中是 protected
    pub.m_private = 3; // 不 okay: m_private 在 Pub 中是不可访问的

    return 0;
}
```

除非有特定的理由，否则您应该使用public继承。

***
## protected继承

protected继承是最不常用的继承方法。除非在非常特殊的情况下，它几乎从未被使用过。通过protected继承，pulbic成员和protected成员变为protected，private成员将无法访问。

由于这种形式的继承非常罕见，因此我们将跳过该示例，并仅用一个表进行总结：

|  基类中的访问说明符 |  protected继承时对应的派生类的访问说明符  |
|  ----  | ----  |
| Public | Protected |
| Protected | Protected |
| Private | 不可访问 |

***
## private继承

通过private继承，基类的所有成员都作为private继承。这意味着私有成员不可访问，protected成员和public成员变为私有成员。

```C++
class Base
{
public:
    int m_public {};
protected:
    int m_protected {};
private:
    int m_private {};
};

class Pri: private Base // 注: 私有继承
{
    // Private 继承意味着:
    // 基类 Public 继承来的成员变为 private (所以 m_public 是 private)
    // 基类 Protected 继承来的成员变为 private (所以 m_protected 是 private)
    // 基类 Private 继承来的成员 是不可访问的 (所以 m_private 是不可访问)
public:
    Pri()
    {
        m_public = 1; // okay: m_public 在 Pri 中是private
        m_protected = 2; // okay: m_protected 在 Pri 中是 private
        m_private = 3; // 不 okay: 派生类不能访问基类的私有成员
    }
};

int main()
{
    // 在类外部进行访问
    Base base;
    base.m_public = 1; // okay: m_public 在 Base 中是 public
    base.m_protected = 2; // 不 okay: m_protected 在 Base 中是 protected
    base.m_private = 3; // 不 okay: m_private 在 Base 中是 private

    Pri pri;
    pri.m_public = 1; // 不 okay: m_public 在 Pri 中是 private
    pri.m_protected = 2; // 不 okay: m_protected 在 Pri 中是 private
    pri.m_private = 3; // 不 okay: m_private 在 Pri 中是不可访问的

    return 0;
}
```

以表格形式总结：

|  基类中的访问说明符 |  private继承时对应的派生类的访问说明符  |
|  ----  | ----  |
| Public | Private |
| Protected | Private |
| Private | 不可访问 |


当派生类与基类没有明显的关系，但在内部使用基类实现时，private继承可能很有用。在这种情况下，我们可能不希望基类的public接口通过派生类的对象公开。

在实践中，很少使用private继承。

***
## 最后一个示例

```C++
class Base
{
public:
	int m_public {};
protected:
	int m_protected {};
private:
	int m_private {};
};
```

Base可以无限制地访问其自己的成员。在外部只能访问m_public。派生类可以访问m_public和m_protected。

```C++
class D2 : private Base // 注: private 继承
{
	// private 继承意味着:
    // 基类 Public 继承来的成员变为 private
    // 基类 Protected 继承来的成员变为 private
    // 基类 Private 继承来的成员 是不可访问的
public:
	int m_public2 {};
protected:
	int m_protected2 {};
private:
	int m_private2 {};
};
```

D2可以无限制地访问其自己的成员。D2可以访问Base的m_public和m_protected成员，但不能访问m_private。由于D2私有继承了Base，因此当通过D2访问时，m_public和m_protected现在被认为是私有的。这意味着当使用D2对象时，外部不能访问这些变量。

```C++
class D3 : public D2
{
    // Public 继承意味着:
    // 基类 Public 仍然保持 public
    // 基类 Protected 继承来的成员保持 protected
    // 基类 Private 继承来的成员 是不可访问的
public:
	int m_public3 {};
protected:
	int m_protected3 {};
private:
	int m_private3 {};
};
```

D3可以无限制地访问自己的成员。D3可以访问D2的m_public2和m_protected2成员，但不能访问m_private2。由于D3 public继承了D2，因此当通过D3访问时，m_public2和m_protected2保留其访问说明符。D3无法访问Base的m_private，它在Base中已经是私有的。它也无法访问Base的m_protected或m_public的权限，当D2继承它们时，它们都成为私有的。

***
## 总结

访问说明符、继承类型和派生类的交互方式导致了许多混淆。这里尽可能地尝试和澄清事情：

首先，类（和友元）总是可以访问其自己的非继承来的成员。访问说明符仅影响外部和派生类是否可以访问这些成员。

其次，当派生类继承成员时，对应的访问说明符可以在派生类中被更改。这不会影响派生类自己的（非继承的）成员（它们有自己的访问说明符）。它仅影响从外部和从派生类是否可以访问这些继承来的成员。

下面是所有访问说明符和继承类型组合的表：

|  基类中的访问说明符 |  public继承时对应的派生类的访问说明符  |  private继承时对应的派生类的访问说明符  |  protected继承时对应的派生类的访问说明符  |
|  ----  | ----  | ----  | ----  |
| Public | Public | Private | Protected |
| Protected | Protected | Private | Protected |
| Private | 不可访问 | 不可访问 | 不可访问 |

作为最后一点，尽管在上面的示例中，我们只显示了使用成员变量的示例，但这些访问规则对所有成员（例如，在类中声明的成员函数和类型）都有效。

***

{{< prevnext prev="/basic/chapter24/derived-class-cons-init/" next="/basic/chapter24/add-new-func-to-derived-class/" >}}
24.3 派生类的构造函数与初始化
<--->
24.5 向派生类添加新功能
{{< /prevnext >}}
