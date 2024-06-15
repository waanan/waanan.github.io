---
title: "临时类对象"
date: 2024-04-09T13:02:20+08:00
---

考虑以下示例：

```C++
#include <iostream>

int add(int x, int y)
{
    int sum{ x + y }; // 将 x + y 的结果存储到sum中
    return sum;       // 返回sum的值
}

int main()
{
    std::cout << add(5, 3) << '\n';

    return 0;
}
```

在 add() 函数中，变量sum用于存储表达式x+y的结果。然后在return语句中对该变量求值，产生要返回的值。虽然这有时可能对调试有用（因此如果需要，可以检查sum的值），但它实际上通过定义一个对象（该对象随后仅使用一次）使函数比需要的更复杂。

在大多数情况下，变量只使用一次，实际上不需要这个变量。相反，可以直接将表达式放到需要变量的位置。下面是以这种方式重写的 add() 函数：

```C++
#include <iostream>

int add(int x, int y)
{
    return x + y; // 直接返回 x + y 计算的结果
}

int main()
{
    std::cout << add(5, 3) << '\n';

    return 0;
}
```

这不仅适用于返回值，也适用于大多数函数参数。例如：

```C++
#include <iostream>

void printValue(int value)
{
    std::cout << value;
}

int main()
{
    int sum{ 5 + 3 };
    printValue(sum);

    return 0;
}
```

可以改成这样：

```C++
#include <iostream>

void printValue(int value)
{
    std::cout << value;
}

int main()
{
    printValue(5 + 3);

    return 0;
}
```

请注意，这使代码干净了点。不需要定义变量并为其命名。不需要阅读整个函数来确定该变量是否实际用于其他地方。因为5+3是一个表达式，它只用于这一行。

请注意，这仅在接受右值表达式的情况下有效。在需要左值表达式的情况下，必须有一个对象：

```C++
#include <iostream>

void addOne(int& value) // 传递 non-const 引用需要左值输入
{
    ++value;
}

int main()
{
    int sum { 5 + 3 };
    addOne(sum);   // okay, sum 是左值

    addOne(5 + 3); // 编译错误: 5 + 3 不是左值

    return 0;
}
```

***
## 临时类对象

同样的问题也适用于类类型。

下面的示例类似于上面的示例，但使用程序定义的类类型IntPair而不是int：

```C++
#include <iostream>

class IntPair
{
private:
    int m_x{};
    int m_y{};

public:
    IntPair(int x, int y)
        : m_x { x }, m_y { y }
    {}

    int x() const { return m_x; }
    int y() const { return m_y; }
};

void print(IntPair p)
{
    std::cout << "(" << p.x() << ", " << p.y() << ")\n";        
}
        
int main()
{
    // 情况 1: 传递变量
    IntPair p { 3, 4 };
    print(p); // 打印 (3, 4)
    
    return 0;
}
```

在情况1中，实例化变量IntPair p，然后将p传递给函数print()。

然而，p只使用一次，函数print()将接受右值，因此实际上没有理由在这里定义变量。所以让我们去掉p。

可以通过传递临时对象而不是命名变量来实现这一点。临时对象（有时称为匿名对象或未命名对象）是没有名称且仅在单个表达式期间存在的对象。

有两种常用的方法来创建临时类类型对象：

```C++
#include <iostream>

class IntPair
{
private:
    int m_x{};
    int m_y{};

public:
    IntPair(int x, int y)
        : m_x { x }, m_y { y }
    {}

    int x() const { return m_x; }
    int y() const{ return m_y; }
};

void print(IntPair p)
{
    std::cout << "(" << p.x() << ", " << p.y() << ")\n";        
}
        
int main()
{
    // 情况 1: 传递变量
    IntPair p { 3, 4 };
    print(p);

    // 情况 2: 构造临时 IntPair 然后传递给函数
    print(IntPair { 5, 6 } );

    // 情况 3: 隐式将 { 7, 8 } 转换为 Intpair 然后传递给函数
    print( { 7, 8 } );
    
    return 0;
}
```

在案例2中，告诉编译器构造一个IntPair对象，并用{5,6}初始化它。因为该对象没有名称，所以它是临时的。然后将临时对象传递给函数 print() 的参数p。当函数调用返回时，临时对象被销毁。

在案例3中，也创建了一个临时IntPair对象，以传递给函数print()。然而，由于没有显式地指定要构造的类型，编译器将从函数参数中推断出必要的类型（IntPair），然后隐式地将{7,8}转换为IntPair对象。

总结如下：

```C++
IntPair p { 1, 2 }; // 创建命名对象 p 初始值为 { 1, 2 }
IntPair { 1, 2 };   // 创建临时对象 初始值为 { 1, 2 }
{ 1, 2 };           // 编译器尝试将 { 1, 2 } 转换问临时对象
```

将在后续课程中更详细地讨论最后一种情况。

可能更常见的是看到与返回值一起使用的临时对象：

```C++
#include <iostream>

class IntPair
{
private:
    int m_x{};
    int m_y{};

public:
    IntPair(int x, int y)
        : m_x { x }, m_y { y }
    {}

    int x() const { return m_x; }
    int y() const { return m_y; }
};

void print(IntPair p)
{
    std::cout << "(" << p.x() << ", " << p.y() << ")\n";        
}

// 情况 1: 创建命名对象并返回
IntPair ret1()
{
    IntPair p { 3, 4 };
    return p;
}

// 情况 2: 创建临时对象并返回
IntPair ret2()
{
    return IntPair { 5, 6 };
}

// 情况 3: 隐式将 { 7, 8 } 转换为 IntPair 并返回
IntPair ret3()
{
    return { 7, 8 };
}
     
int main()
{
    print(ret1());
    print(ret2());
    print(ret3());

    return 0;
}
```

本例中的情况类似于前一示例中的情况。

{{< alert success >}}
**注**

这里使用的是class，但本课中的所有内容都同样适用于可使用聚合初始化的结构。

{{< /alert >}}

***
## 一些注意事项

首先，就像在int的情况下一样，当在表达式中使用时，临时类对象是右值。因此，这样的对象只能在接受右值表达式的情况下使用。

其次，会在定义点创建临时对象，并在定义它们的完整表达式的末尾销毁它们。

***
