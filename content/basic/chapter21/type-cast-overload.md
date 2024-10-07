---
title: "重载类型转换"
date: 2024-08-20T12:01:51+08:00
---

C++允许您将一种数据类型转换为另一种。下面的示例显示了将int转换为double的过程：

```C++
int n{ 5 };
auto d{ static_cast<double>(n) }; // int 转换为 double
```

C++知道如何在内置数据类型之间进行转换。然而，它不知道如何转换其它任何用户定义的类。这就是重载类型转换操作符可以发挥的作用。

用户定义的转换允许将类转换为另一种数据类型。请看以下示例：

```C++
class Cents
{
private:
    int m_cents{};
public:
    Cents(int cents=0)
        : m_cents{ cents }
    {
    }

    int getCents() const { return m_cents; }
    void setCents(int cents) { m_cents = cents; }
};
```

这个类相当简单：它将一些Cents作为int保存，并提供访问函数来获取和设置m_cents的数量。它还提供了一个构造函数，用于将int转换为Cents。

如果我们可以将int转换为Cents（通过构造函数），那么我们是否也可以将Cents转换回int？

在下面的示例中，必须使用getCents() 将Cents变量转换回int，以便可以使用 printInt() 打印它：

```C++
#include <iostream>

void printInt(int value)
{
    std::cout << value;
}

int main()
{
    Cents cents{ 7 };
    printInt(cents.getCents()); // 打印 7

    std::cout << '\n';

    return 0;
}
```

如果我们已经编写了许多以int作为参数的函数，那么我们的代码将被对 getCents() 的调用弄得乱七八糟。

为了简化操作，可以通过重载int类型转换来提供用户定义的转换。这将允许将Cents类直接转换为int。下面的示例显示了如何完成此操作：

```C++
class Cents
{
private:
    int m_cents{};
public:
    Cents(int cents=0)
        : m_cents{ cents }
    {
    }

    // 重载int转换
    operator int() const { return m_cents; }

    int getCents() const { return m_cents; }
    void setCents(int cents) { m_cents = cents; }
};
```

需要注意三点：

1. 为了使自定义的类可以转换为int，新增了一个成员函数“operator int()”。注意“operator” 和要转换到的类型之间有个空格，而且这样的函数一定不能是static成员函数。

2. 自定义的转换函数，不能有任何参数，也没有任何方式传递参数。但是这里仍然有一个隐式的 “*this” 参数，指向隐式的被转换的对象。

3. 自定义的转换函数，不能有返回类型。函数名（例如上面的 int）就是代表着返回类型。


现在，在上面的示例中，可以这样调用printInt()：

```C++
#include <iostream>

int main()
{
    Cents cents{ 7 };
    printInt(cents); // 打印 7

    std::cout << '\n';

    return 0;
}
```

编译器将首先注意到函数printInt()采用整数参数。然后它将注意到变量cents不是int。最后，它将查看我们是否提供了一种将cents转换为int的方法。由于我们提供了，它将调用“operator int()”函数，该函数返回int，并且返回的int将被传递给printInt()。

这样的类型转换也可以通过static_cast显式调用：

```C++
std::cout << static_cast<int>(cents);
```

您可以提供用户定义的对任何数据类型的转换，包括您自己的程序定义的数据类型！

这里有一个名为Dollars的新类，提供重载的Cents转换：

```C++
class Dollars
{
private:
    int m_dollars{};
public:
    Dollars(int dollars=0)
        : m_dollars{ dollars }
    {
    }

     // 允许从 Dollars 转换到 Cents
     operator Cents() const { return Cents{ m_dollars * 100 }; }
};
```

这允许我们将Dollars对象直接转换为Cents对象！这允许您执行以下操作：

```C++
#include <iostream>

class Cents
{
private:
    int m_cents{};
public:
    Cents(int cents=0)
        : m_cents{ cents }
    {
    }

    // 重载 int 转换
    operator int() const { return m_cents; }

    int getCents() const { return m_cents; }
    void setCents(int cents) { m_cents = cents; }
};

class Dollars
{
private:
    int m_dollars{};
public:
    Dollars(int dollars=0)
        : m_dollars{ dollars }
    {
    }

    // 允许从 Dollars 转换到 Cents
    operator Cents() const { return Cents { m_dollars * 100 }; }
};

void printCents(Cents cents)
{
    std::cout << cents; // cents 会隐式的转换为 int
}

int main()
{
    Dollars dollars{ 9 };
    printCents(dollars); // dollars 可以隐式的转换为 Cents

    std::cout << '\n';

    return 0;
}
```

因此，该程序将打印值：

```C++
900
```

这很有道理，因为9美元是900美分！

***
## 显式类型转换

就像我们可以标记构造函数为explicit，以便它们不能用于隐式转换一样，出于相同的原因，也可以使重载类型转换标记为explicit。只能显式调用显式类型转换（例如，不能使用复制初始化或通过使用类似static_cast的显式转换）。

```C++
#include <iostream>

class Cents
{
private:
    int m_cents{};
public:
    Cents(int cents=0)
        : m_cents{ cents }
    {
    }

    explicit operator int() const { return m_cents; } // 现在标记为 explicit

    int getCents() const { return m_cents; }
    void setCents(int cents) { m_cents = cents; }
};

class Dollars
{
private:
    int m_dollars{};
public:
    Dollars(int dollars=0)
        : m_dollars{ dollars }
    {
    }

    operator Cents() const { return Cents { m_dollars * 100 }; }
};

void printCents(Cents cents)
{
    std::cout << static_cast<int>(cents); // explicit，因此必须使用显式类型转换
}

int main()
{
    Dollars dollars{ 9 };
    printCents(dollars);

    std::cout << '\n';

    return 0;
}
```

类型转换通常应标记为explicit。如果转换以低廉的成本转换为类似的用户定义类型，则可以例外。“Dollars::operator Cents()”类型转换被标记为为非显式，因为没有理由不让Dollars对象用于预期为Cents的任何地方。

{{< alert success >}}
**最佳实践**

类型转换应标记为explicit，除非要转换的类本质上是同义的。

{{< /alert >}}

***
## 转换构造函数与重载类型转换

重载类型转换和转换构造函数执行类似的角色：重载类型转换允许我们定义一个函数，该函数将某些程序定义的类型a转换为其他类型b。转换构造函数允许我们定义从其他类型b创建某些程序定义类型a的函数。那么，您应该何时使用它们呢？

通常，转换构造函数应该优先于重载类型转换。

在一些情况下，应使用重载类型转换：

1. 提供到基本类型或你无法修改的类的转换（因为不能为这些类型定义构造函数）。最惯用的地方是，能够在条件语句中使用对象的情况下提供到bool的转换。

2. 当不希望正在构造的类型知道被转换的类型时。这有助于避免循环依赖。

对于最后一点，例如，std::string具有一个构造函数，用于从std::string_view创建std::string。这意味着\<string\>必须包含\<string_view\>。如果std::string_view有一个构造函数来从std::string创建std::string_view，则\<string_view\>将需要包括\<string\>，这将导致头文件之间的循环依赖。

相反，std::string具有一个重载类型转换，该类型转换处理从std::string到std::string_view的转换（这很好，因为它已经包括\<string_view\>）。std::string_view则根本不知道std::string的任何细节，因此不需要包含\<string\>。这样，就避免了循环依赖。

***
