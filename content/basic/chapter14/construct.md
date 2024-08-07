---
title: "构造函数简介"
date: 2024-04-09T13:02:20+08:00
---

当类类型是聚合时，可以使用聚合初始化：

```C++
struct Foo // Foo 是聚合
{
    int x {};
    int y {};
};

int main()
{
    Foo foo { 6, 7 }; // 使用聚合初始化

    return 0;
}
```

聚合初始化执行成员级初始化（成员按定义顺序初始化）。因此，当在上面的示例中实例化foo时，foo.x被初始化为6，而foo.y被初始化为7。

然而，一旦将任何成员变量设置为私有（以隐藏数据），类类型就不再是聚合（因为聚合不能有私有成员）。这意味着不再能够使用聚合初始化：

```C++
class Foo // Foo 不再是聚合 (有私有成员)
{
    int m_x {};
    int m_y {};
};

int main()
{
    Foo foo { 6, 7 }; // 编译失败: 不能使用聚合初始化

    return 0;
}
```

由于以下几个原因，不允许通过聚合初始化来初始化具有私有成员的类类型：

1. 聚合初始化需要知道类的实现（因为必须知道成员是什么，以及它们的定义顺序），这是在隐藏数据成员时有意避免的。
2. 如果类具有某种不变量，将依赖于用户以保证不变量的方式初始化类。

那么，如何初始化有私有成员变量的类呢？编译器为上例给出的错误消息提供了一条线索：“error:no matching constructor for initialization of'Foo'”

我们必须需要一个匹配的构造函数。但那到底是什么？

***
## 构造函数（constructor）

构造函数是一个特殊的成员函数，在创建非聚合类类型对象后会被自动调用。

定义非聚合类类型对象时，编译器会查看是否可以找到与调用方提供的初始化值（如果有）匹配的可访问构造函数。

1. 如果找到可访问的匹配构造函数，则为对象分配内存，然后调用构造函数。
2. 如果找不到可访问的匹配构造函数，则将提示编译错误。


除了确定如何创建对象之外，构造函数通常还执行两个功能：

1. 它们通常执行成员变量的初始化（通过成员初始化列表）
2. 它们可以执行其他设置功能（通过构造函数主体中的语句）。这可能包括检查初始化值、打开文件或数据库等…


在构造函数完成执行后，我们说对象已经“构造”好，对象现在应该处于一致的可用状态。

请注意，聚合不允许具有构造函数——因此，如果将构造函数添加到聚合中，它就不再是聚合。

{{< alert success >}}
**关键点**

许多新程序员对构造函数是否创建对象感到困惑。构造函数并不创建对象——编译器在构造函数调用之前为对象进行内存分配。然后对未初始化的对象调用构造函数。

然而，如果找不到一组初始值设定项匹配的构造函数，编译器将提示出错。因此，虽然构造函数不创建对象，但缺少匹配的构造函数将阻止创建对象。

{{< /alert >}}

***
## 构造函数的命名

与普通成员函数不同，构造函数有特定的命名规则：

1. 构造函数必须与类具有相同的名称（具有相同的大小写）。对于模板类，此名称不包括模板参数。
2. 构造函数没有返回类型。

由于构造函数通常是类接口的一部分，因此它们通常是public的。

***
## 基本构造函数示例

让我们在上面的示例中添加一个基本构造函数：

```C++
#include <iostream>

class Foo
{
private:
    int m_x {};
    int m_y {};

public:
    Foo(int x, int y) // 有两个初始值设定项的构造函数
    {
        std::cout << "Foo(" << x << ", " << y << ") constructed\n";
    }

    void print() const
    {
        std::cout << "Foo(" << m_x << ", " << m_y << ")\n";
    }
};

int main()
{
    Foo foo{ 6, 7 }; // 调用 Foo(int, int) 构造函数
    foo.print();

    return 0;
}
```

该程序现在将编译并生成结果：

```C++
Foo(6, 7) constructed
Foo(0, 0)
```

当编译器看到定义Foo Foo{6,7}时，它会查找将接受两个int参数的匹配Foo构造函数。Foo(int，int)是匹配项，因此编译器将允许定义。

在运行时，当foo被实例化时，为foo分配内存，然后调用Foo(int，int)构造函数，参数x为6，参数y为7。然后，构造函数的主体执行并打印 "Foo(6, 7) constructed"。

当调用print()成员函数时，成员m_x和m_y的值为0。这是因为尽管调用了Foo(int，int)构造函数，但它并没有实际初始化成员。将在下一课中演示如何做到这一点。

***
## 构造函数参数的隐式转换

在隐式类型转换中，可以注意到编译器将在函数调用中执行参数的隐式转换（如果需要），以匹配参数为不同类型的函数定义：

```C++
void foo(int, int)
{
}

int main()
{
    foo('a', true); // 可以匹配 foo(int, int)

    return 0;
}
```

对于构造函数来说，这没有什么不同：Foo(int，int) 构造函数将匹配隐式可转换为int的任何调用：

```C++
class Foo
{
public:
    Foo(int x, int y)
    {
    }
};

int main()
{
    Foo foo{ 'a', true }; // 可以匹配 Foo(int, int) 构造函数

    return 0;
}
```

***
## 构造函数不应为const

构造函数需要能够初始化正在构造的对象——因此，构造函数不能是const。

```C++
#include <iostream>

class Something
{
private:
    int m_x{};

public:
    Something() // 构造函数不应为const
    {
        m_x = 5; // 在 non-const 构造函数才能修改成员变量
    }

    int getX() const { return m_x; } // const
};

int main()
{
    const Something s{}; // const 对象, 隐式调用 (non-const) 构造函数

    std::cout << s.getX(); // 打印 5
    
    return 0;
}
```

通常，不能在常量对象上调用非const成员函数。然而，由于构造函数是隐式调用的，因此可以在常量对象上调用非const构造函数。

***
## 构造函数 vs Setter访问函数

构造函数被设计为在实例化点初始化整个对象。Setter访问函数旨在将值分配给现有对象的单个成员。

***

{{< prevnext prev="/basic/chapter14/data-hide/" next="/basic/chapter14/construct-member-init-list/" >}}
14.7 数据隐藏（封装）的好处
<--->
14.9 构造函数成员初始化列表
{{< /prevnext >}}
