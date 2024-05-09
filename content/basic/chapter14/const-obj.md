---
title: "Const类对象和Const成员函数"
date: 2024-04-09T13:02:20+08:00
---

在前面，我们知道基本数据类型（int、double、char等）的对象可以通过const关键字设置为常量。所有常变量都必须在创建时初始化。

```C++
const int x;      // 编译失败: 未初始化
const int y{};    // ok: 值初始化
const int z{ 5 }; // ok: 列表初始化
```

类似地，通过使用const关键字，类类型对象（结构体、类和联合）也可以成为const。这样的对象也必须在创建时初始化。

```C++
struct Date
{
    int year {};
    int month {};
    int day {};
};

int main()
{
    const Date today { 2020, 10, 14 }; // const class 类型的对象

    return 0;
}
```

就像普通变量一样，当需要确保类类型对象在创建后不会被修改时，通常将它们设置为const（或constexpr）。

***
## 不允许修改常量对象的数据成员

一旦初始化了常量类类型对象，就不允许任何修改它的数据成员的操作，因为这将违反const属性。这包括直接更改成员变量（如果它们是public的），或调用设置成员变量的成员函数。

```C++
struct Date
{
    int year {};
    int month {};
    int day {};

    void incrementDay()
    {
        ++day;
    }
};

int main()
{
    const Date today { 2020, 10, 14 }; // const

    today.day += 1;        // 编译失败: 不能修改const 对象的成员变量
    today.incrementDay();  // 编译失败: 不能调用修改const 对象成员变量的成员函数

    return 0;
}
```

***
## Const对象不能调用非const成员函数

您可能会惊讶地发现，此代码也会导致编译错误：

```C++
#include <iostream>

struct Date
{
    int year {};
    int month {};
    int day {};

    void print()
    {
        std::cout << year << '/' << month << '/' << day;
    }
};

int main()
{
    const Date today { 2020, 10, 14 }; // const

    today.print();  // 编译失败: 不能调用非const成员函数

    return 0;
}
```

即使print()不尝试修改成员变量，对today.print()的调用仍然是无法编译。这是因为print()成员函数本身没有声明为const。编译器不允许对常量对象调用非const成员函数。

***
## Const成员函数

为了解决上述问题，需要使print()成为const成员函数。来保证不会修改对象或调用任何非const成员函数（因为它们可能会修改对象）。

使print()成为const成员函数很容易——只需将const关键字附加到函数原型中，在参数列表之后，在函数体之前：

```C++
#include <iostream>

struct Date
{
    int year {};
    int month {};
    int day {};

    void print() const // 现在是个const成员函数
    {
        std::cout << year << '/' << month << '/' << day;
    }
};

int main()
{
    const Date today { 2020, 10, 14 }; // const

    today.print();  // ok: const 对象可以调用 const 成员函数

    return 0;
}
```

在上面的例子中，print()是一个const成员函数，这意味着可以在const对象上调用它（例如today）。

试图更改成员变量或调用非const成员函数的const成员函数将导致发生编译器错误。例如：

```C++
struct Date
{
    int year {};
    int month {};
    int day {};

    void incrementDay() const // 设置为 const
    {
        ++day; // 编译失败: const 成员函数不能修改成员变量
    }
};

int main()
{
    const Date today { 2020, 10, 14 }; // const

    today.incrementDay();

    return 0;
}
```

在本例中，incrementDay() 已标记为const成员函数，但它试图更改day。这将导致编译器错误。

{{< alert success >}}
**对于高级读者**

对于在类定义之外定义的成员函数，const关键字必须同时用于类定义中的函数声明和类定义之外的函数定义。我们在后续进行举例。

构造函数不能设置为const，因为它们需要初始化或修改对象的成员。

{{< /alert >}}

***
## 可以在非常量对象上调用const成员函数

也可以在非常量对象上调用const成员函数：

```C++
#include <iostream>

struct Date
{
    int year {};
    int month {};
    int day {};

    void print() const // const
    {
        std::cout << year << '/' << month << '/' << day;
    }
};

int main()
{
    Date today { 2020, 10, 14 }; // non-const

    today.print();  // ok: 可以调用

    return 0;
}
```

由于const成员函数可以在常量和非常量对象上调用，因此如果成员函数不修改对象的状态，则应将其设置为常量。

一旦成员函数成为const，就可以在常量对象上调用该函数。

{{< alert success >}}
**最佳实践**

不（并且永远不会）修改对象状态的成员函数应成为const，以便可以在常量和非常量对象上调用它。

{{< /alert >}}

***
## 通过常量引用传递的常量对象

尽管实例化常量局部变量是创建常量对象的一种方法，但获取常量对象的更常见方法是通过常量引用将对象传递给函数。

在前面，介绍了通过常量引用而不是通过值传递类类型参数的优点。概括地说，按值传递类类型参数会导致生成类的副本（这很慢）——大多数情况下，不需要副本，对原始参数的引用工作得很好，并避免生成副本。

你能找出下面的代码有什么问题吗？

```C++
#include <iostream>

struct Date
{
    int year {};
    int month {};
    int day {};

    void print() // non-const
    {
        std::cout << year << '/' << month << '/' << day;
    }
};

void doSomething(const Date &date)
{
    date.print();
}

int main()
{
    Date today { 2020, 10, 14 }; // non-const
    today.print();

    doSomething(today);

    return 0;
}
```

答案是，在doSomething()函数内部，date被视为常量对象（因为它是通过常量引用传递的）。对于该常量，调用非const成员函数print()。由于不能对常量对象调用非const成员函数，这将导致编译错误。

修复很简单：将 print() 设置为 const:

```C++
#include <iostream>

struct Date
{
    int year {};
    int month {};
    int day {};

    void print() const // now const
    {
        std::cout << year << '/' << month << '/' << day;
    }
};

void doSomething(const Date &date)
{
    date.print();
}

int main()
{
    Date today { 2020, 10, 14 }; // non-const
    today.print();

    doSomething(today);

    return 0;
}
```

现在，在函数doSomething() 中，const date将能够成功调用const成员函数print()。

***
## 成员函数常量和非常量重载

最后，尽管不经常这样做，但可以重载成员函数，使其具有同一函数的const版本和非const版本。这是因为const限定符被认为是函数签名的一部分，所以两个仅在const上不同的函数被认为是不同的。

```C++
#include <iostream>

struct Something
{
    void print()
    {
        std::cout << "non-const\n";
    }

    void print() const
    {
        std::cout << "const\n";
    }
};

int main()
{
    Something s1{};
    s1.print(); // 调用 print()

    const Something s2{};
    s2.print(); // 调用 print() const
    
    return 0;
}
```

这将打印：

```C++
non-const
const
```

当返回值的const需要不同时，通常会使用const和非const版本重载函数。这是相当罕见的。

***

{{< prevnext prev="/basic/chapter14/member_func/" next="/basic/chapter14/public-private/" >}}
14.2 成员函数
<--->
14.4 公共和私有成员以及访问说明符
{{< /prevnext >}}
