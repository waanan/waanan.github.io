---
title: "静态成员变量"
date: 2024-06-24T18:56:16+08:00
---

在之前，我们介绍了全局变量和静态局部变量。这两种类型的变量都具有静态存储期，这意味着它们在程序开始时创建，在程序结束时销毁。这样的变量保持其值，即使它们超出变量作用域。

例如：

```C++
#include <iostream>

int generateID()
{
    static int s_id{ 0 }; // 静态局部变量
    return ++s_id;
}

int main()
{
    std::cout << generateID() << '\n';
    std::cout << generateID() << '\n';
    std::cout << generateID() << '\n';

    return 0;
}
```

该程序打印：

```C++
1
2
3
```

请注意，静态局部变量s_id在多个函数调用中保持了其值。

类类型为static关键字带来了另外两种用法：静态成员变量和静态成员函数。幸运的是，这些用法相当简单。在本课中，将讨论静态成员变量，在下一节中，讨论静态成员函数。

***
## 静态成员变量

在研究应用于成员变量的static关键字之前，首先考虑以下类：

```C++
#include <iostream>

struct Something
{
    int value{ 1 };
};

int main()
{
    Something first{};
    Something second{};
    
    first.value = 2;

    std::cout << first.value << '\n';
    std::cout << second.value << '\n';

    return 0;
}
```

当实例化一个类对象时，每个对象的存储都是完全互相隔离的。在这种情况下，因为声明了两个Something类对象，所以最后得到了value的两个副本：first.value和second.value。first.value与second.value不同。因此，上面的程序打印：

```C++
2
1
```

通过使用static关键字，可以使类的成员变量成为静态的。与普通成员变量不同，静态成员变量由类的所有对象共享。考虑以下程序，类似于上面的程序：

```C++
#include <iostream>

struct Something
{
    static int s_value; // 现在是 static
};

int Something::s_value{ 1 }; // 初始化 s_value 为 1

int main()
{
    Something first{};
    Something second{};

    first.s_value = 2;

    std::cout << first.s_value << '\n';
    std::cout << second.s_value << '\n';
    return 0;
}
```

该程序产生以下输出：

```C++
2
2
```

因为s_value是一个静态成员变量，所以s_value在类的所有对象之间共享。因此，first.s_value与second.s_value是相同的变量。上面的程序显示，使用first设置的值可以使用second访问！

***
## 静态成员不与类对象关联

尽管可以通过类的对象访问静态成员（如上面的示例中的first.s_value和second.s_value所示），但即使类的对象没有被实例化，静态成员也存在！这是有意义的：它们在程序开始时创建，在程序结束时销毁，因此它们的生命周期不像普通成员那样绑定到类对象。

本质上，静态成员是存在于类的作用域内的全局变量。类的静态成员和命名空间内的普通变量之间没有什么区别。

由于静态成员s_value独立于任何类对象存在，因此可以使用类名和域解析操作符（在本例中为Something::s_value）直接访问它：

```C++
class Something
{
public:
    static int s_value; // 声明静态成员变量
};

int Something::s_value{ 1 }; // 定义静态成员变量 (下面进行讨论)

int main()
{
    // 注: 这里不再实例化任何 Something 的对象

    Something::s_value = 2;
    std::cout << Something::s_value << '\n';
    return 0;
}
```

在上面的片段中，s_value由类名Something来进行使用，而不是通过对象使用。请注意，甚至还没有实例化Something类型的对象，但仍然能够访问和使用Something::s_value。这是访问静态成员的首选方法。

{{< alert success >}}
**关键点**

静态成员是位于类的作用域内的全局变量。

{{< /alert >}}

{{< alert success >}}
**最佳实践**

使用类名和域解析运算符（ :: ）访问静态成员。

{{< /alert >}}

***
## 定义和初始化静态成员变量

当在类类型中声明静态成员变量时，告诉编译器静态成员变量的存在，但不是实际定义它（很像前向声明）。由于静态成员变量本质上是全局变量，因此必须在全局作用域内显式定义（并可选地初始化）类外部的静态成员。

在上面的示例中，我们通过这一行来执行此操作：

```C++
int Something::s_value{ 1 }; // 定义静态成员变量
```

这一行有两个用途：它实例化静态成员变量（就像全局变量一样），并对其进行初始化。在本例中，提供的是初始化值1。如果未提供初始值设定项，则默认情况下静态成员变量为零初始化。

请注意，此静态成员定义不受访问控制的约束：您可以定义和初始化该值，即使它在类中声明为 private（或 protected）。

如果类在头（.h）文件中定义，则静态成员定义通常放在类的关联代码文件中（例如Something.cpp）。如果类是在源（.cpp）文件中定义的，则静态成员定义通常直接放在类的下面。不要将静态成员定义放在头文件中（就像全局变量一样，如果该头文件被多次包含，则最终将得到多个定义，这将导致编译错误）。

***
## 类定义内静态成员变量的初始化

有几个快捷方式。首先，当静态成员是常量整型（包括char和bool）或常量枚举时，可以在类定义内初始化静态成员：

```C++
class Whatever
{
public:
    static const int s_value{ 4 }; // 静态 const int 可以在类内部直接定义和初始化
};
```

在上面的示例中，由于静态成员变量是常量int。因此允许使用此快捷方式，因为这些特定的常量类型是编译时常量。

在前面讲解跨多个文件共享全局常量（使用内联变量）中，引入了内联变量，这是允许具有多个定义的变量。C++17允许静态成员成为内联变量：

```C++
class Whatever
{
public:
    static inline int s_value{ 4 }; // 静态内联变量可以直接定义和初始化
};
```

无论这些变量是否为常量，都可以在类定义内初始化它们。这是定义和初始化静态成员的首选方法。

由于constexpr成员是隐式内联的（从C++17开始），因此也可以在类定义内初始化静态constexpr成员，而无需显式使用inline关键字：

```C++
#include <string_view>

class Whatever
{
public:
    static constexpr double s_value{ 2.2 }; // ok
    static constexpr std::string_view s_view{ "Hello" }; // 甚至支持类类型的 静态 constexpr 定义和初始化
};
```

{{< alert success >}}
**最佳实践**

将静态成员设为内联或constexpr，以便可以在类定义内初始化它们。

{{< /alert >}}

***
## 静态成员变量的示例

为什么在类中使用静态变量？一种用法是为类的每个实例分配唯一的ID。下面是一个示例：

```C++
#include <iostream>

class Something
{
private:
    static inline int s_idGenerator { 1 };
    int m_id {};

public:
    // 获取下一个id值
    Something() : m_id { s_idGenerator++ } 
    {    
    }

    int getID() const { return m_id; }
};

int main()
{
    Something first{};
    Something second{};
    Something third{};

    std::cout << first.getID() << '\n';
    std::cout << second.getID() << '\n';
    std::cout << third.getID() << '\n';
    return 0;
}
```

该程序打印：

```C++
1
2
3
```

由于s_idGenerator由所有Something对象共享，因此在创建新的Somethine对象时，构造函数使用s_idGenerator的当前值初始化m_id，然后s_idGenerator加一。这确保每个实例化的Something对象接收唯一的id（按创建顺序递增）。

在调试时为每个对象提供唯一的ID会有所帮助，因为它可以用于区分在其他情况下具有相同数据的对象。当使用数据数组时，这一点尤其明显。

当类需要使用查找表（例如，用于存储一组预计算值的数组）时，静态成员变量也很有用。通过将查找表设置为静态，所有对象只存在一个副本，而不是为每个实例化的对象创建一个副本。这可以节省大量内存。

***
## 只有静态成员可以使用类型演绎（auto和CTAD）

静态成员可以使用auto从初始值设定项推断其类型，或者使用类模板参数推断（CTAD）从初始值设置项推断模板类型参数。

非静态成员不能使用auto或CTAD。

做出这种区分的原因相当复杂，但归根结底，非静态成员可能会发生某些情况，从而导致歧义或非直观的结果。静态成员不会发生这种情况。因此，非静态成员不能使用这些功能。

```C++
#include <utility> // for std::pair<T, U>

class Foo
{
private:
    auto m_x { 5 };           // 非静态成员不能使用 auto
    std::pair m_v { 1, 2.3 }; // 非静态成员不能使用 CTAD

    static inline auto s_x { 5 };           // 静态成员可以使用 auto
    static inline std::pair s_v { 1, 2.3 }; // 静态成员可以使用 CTAD

public:
    Foo() {};
};

int main()
{
    Foo foo{};
    
    return 0;
}
```

***
