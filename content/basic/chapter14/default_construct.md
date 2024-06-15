---
title: "默认构造函数和默认参数"
date: 2024-04-09T13:02:20+08:00
---

默认构造函数是不接受参数的构造函数。通常，这是一个没有参数定义的构造函数。

下面是具有默认构造函数的类的示例：

```C++
#include <iostream>

class Foo
{
public:
    Foo() // 默认构造函数
    {
        std::cout << "Foo default constructed\n";
    }
};

int main()
{
    Foo foo{}; // 未设置初始参数, 调用 Foo 的默认构造函数

    return 0;
}
```

当上述程序运行时，将创建Foo类型的对象。由于未提供初始化值，因此调用默认构造函数Foo()，该构造函数将打印：

```C++
Foo default constructed
```

***
## 类类型的值初始化与默认初始化

如果类类型具有默认构造函数，则值初始化和默认初始化都将调用默认构造函数。因此，对于上述示例中的Foo类这样的类，以下内容本质上是等效的：

```C++
    Foo foo{}; // 值初始化, 调用 Foo 的默认构造函数
    Foo foo2;  // 默认初始化, 调用 Foo 的默认构造函数
```

然而，正如之前讲解（默认成员初始化）中所述，值初始化对于聚合更安全。由于很难区分类类型是聚合还是非聚合，因此推荐对所有类类型使用值初始化。

***
## 具有默认参数的构造函数

与所有函数一样，构造函数的最右侧参数可以具有默认参数。

例如：

```C++
#include <iostream>

class Foo
{
private:
    int m_x { };
    int m_y { };

public:
    Foo(int x=0, int y=0) // 有默认参数
        : m_x { x }
        , m_y { y }
    {
        std::cout << "Foo(" << m_x << ", " << m_y << ") constructed\n";
    }
};

int main()
{
    Foo foo1{};     // 调用 Foo(int, int) 使用默认参数
    Foo foo2{6, 7}; // 调用 Foo(int, int)

    return 0;
}
```

这将打印：

```C++
Foo(0, 0) constructed
Foo(6, 7) constructed
```

如果构造函数中的所有参数都有默认值，则构造函数是默认构造函数（因为它可以在没有参数的情况下调用）。

***
## 构造函数重载

由于构造函数是函数，因此可以重载它们。也就是说，可以有多个构造函数，以便可以按不同的方式构造对象：

```C++
#include <iostream>

class Foo
{
private:
    int m_x {};
    int m_y {};

public:
    Foo() // 默认构造函数
    {
        std::cout << "Foo constructed\n";
    }

    Foo(int x, int y) // 普通构造函数
        : m_x { x }, m_y { y }
    {
        std::cout << "Foo(" << m_x << ", " << m_y << ") constructed\n";
    }
};

int main()
{
    Foo foo1{};     // 调用 Foo()
    Foo foo2{6, 7}; // 调用 Foo(int, int)

    return 0;
}
```

上面的一个推论是，一个类应该只有一个默认构造函数。如果提供了多个默认构造函数，编译器将无法知道应使用哪个构造函数：

```C++
#include <iostream>

class Foo
{
private:
    int m_x {};
    int m_y {};

public:
    Foo() // 默认
    {
        std::cout << "Foo constructed\n";
    }

    Foo(int x=1, int y=2) // 默认
        : m_x { x }, m_y { y }
    {
        std::cout << "Foo(" << m_x << ", " << m_y << ") constructed\n";
    }
};

int main()
{
    Foo foo{}; // 编译失败: 不知道该调用哪个构造函数

    return 0;
}
```

在上面的示例中，实例化没有参数的foo，因此编译器将查找默认构造函数。将找到两个，这是有歧义的。将导致编译错误。

***
## 隐式默认构造函数

如果非聚合类类型对象没有用户声明的构造函数，编译器将生成public默认构造函数（以便类可以是值初始化的或默认初始化的）。此构造函数称为隐式默认构造函数。

考虑以下示例：

```C++
#include <iostream>

class Foo
{
private:
    int m_x{};
    int m_y{};

    // 注: 未声明构造函数
};

int main()
{
    Foo foo{};

    return 0;
}
```

该类没有用户声明的构造函数，因此编译器将为生成隐式默认构造函数。该构造函数将用于实例化foo{}。

隐式默认构造函数等效于在构造函数体中没有参数、没有成员初始化列表和语句的构造函数。换句话说，对于上面的Foo类，编译器生成：

```C++
public:
    Foo() // 隐式生成的默认构造函数
    {
    }
```

当类没有数据成员时，隐式默认构造函数最有用。如果类具有数据成员，则可能希望使用用户提供的值来初始化它们，而隐式默认构造函数不足以实现这一点。

***
## 使用=default生成显式默认构造函数

在编写等效于隐式生成的默认构造函数时，可以告诉编译器为我们生成默认构造函数。该构造函数称为显式默认构造函数，可以通过使用=default语法来生成：

```C++
#include <iostream>

class Foo
{
private:
    int m_x {};
    int m_y {};

public:
    Foo() = default; // 生成显式默认构造函数

    Foo(int x, int y)
        : m_x { x }, m_y { y }
    {
        std::cout << "Foo(" << m_x << ", " << m_y << ") constructed\n";
    }
};

int main()
{
    Foo foo{}; // 调用 Foo() 默认构造函数

    return 0;
}
```

在上面的示例中，由于有一个用户声明的构造函数 Foo(int, int)，因此通常不会生成隐式默认构造函数。然而，因为已经告诉编译器生成这样的构造函数，所以会生成。该构造函数随后将由foo{}实例化使用。

{{< alert success >}}
**最佳实践**

与编写空的默认构造函数相比，优先使用显式默认构造函数（=default）。

{{< /alert >}}

***
## 显式默认构造函数与空的用户定义构造函数

至少有两种情况下，显式默认构造函数的行为与空的用户定义构造函数不同。

```C++
#include <iostream>

class User
{
private:
    int m_a; // 注: 无默认值
    int m_b {};

public:
    User() {} // 用户定义空的构造函数

    int a() const { return m_a; }
    int b() const { return m_b; }
};

class Default
{
private:
    int m_a; // 注: 无默认值
    int m_b {};

public:
    Default() = default; // 显式默认构造函数

    int a() const { return m_a; }
    int b() const { return m_b; }
};

class Implicit
{
private:
    int m_a; // 注: 无默认值
    int m_b {};

public:
    // 隐式默认构造函数

    int a() const { return m_a; }
    int b() const { return m_b; }
};

int main()
{
    User user{}; // 默认初始化
    std::cout << user.a() << ' ' << user.b() << '\n';

    Default def{}; // 零值初始化, 然后默认初始化
    std::cout << def.a() << ' ' << def.b() << '\n';

    Implicit imp{}; // 零值初始化, 然后默认初始化
    std::cout << imp.a() << ' ' << imp.b() << '\n';

    return 0;
}
```

在作者的机器上，此命令打印：

```C++
782510864 0
0 0
0 0
```

请注意，在默认初始化之前，user.a不是零初始化的，因此未初始化。

在实践中，这并不重要，因为您应该为所有数据成员提供默认的成员初始值设定项！

***
## 仅在有意义时创建默认构造函数

默认构造函数，允许在业务不提供初始值时，创建非聚合类类型的对象。因此，当不需要用户提供初始值，类的默认值有意义时，才需要提供默认构造函数。

例如：

```C++
#include <iostream>

class Fraction
{
private:
    int m_numerator{ 0 };
    int m_denominator{ 1 };

public:
    Fraction() = default;
    Fraction(int numerator, int denominator)
        : m_numerator{ numerator }
        , m_denominator{ denominator }
    {
    }

    void print() const
    {
        std::cout << "Fraction(" << m_numerator << ", " << m_denominator << ")\n";
    }
};

int main()
{
    Fraction f1 {3, 5};
    f1.print();

    Fraction f2 {}; // 生成 Fraction 0/1
    f2.print();

    return 0;
}
```

对于表示分数的类，允许用户创建没有初始值设定项的fraction对象是有意义的（在这种情况下，用户将获得分数0/1）。

现在考虑这个类：

```C++
#include <iostream>
#include <string>
#include <string_view>

class Employee
{
private:
    std::string m_name{ };
    int m_id{ };

public:
    Employee(std::string_view name, int id)
        : m_name{ name }
        , m_id{ id }
    {
    }

    void print() const
    {
        std::cout << "Employee(" << m_name << ", " << m_id << ")\n";
    }
};

int main()
{
    Employee e1 { "Joe", 1 };
    e1.print();

    Employee e2 {}; // 编译失败: 无匹配的构造函数
    e2.print();

    return 0;
}
```

对于表示雇员的类，允许创建没有名字的雇员是没有意义的。因此，这样的类不应该具有默认构造函数，因此如果类的用户尝试这样做，将出现编译错误。

***