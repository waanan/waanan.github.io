---
title: "类初始化和拷贝省略"
date: 2024-04-09T13:02:20+08:00
---

在前面，我们讨论了具有基本类型的对象的6种基本初始化类型：

```C++
int a;         // 无初始值 (默认初始化)
int b = 5;     // 等号后跟初始值 (拷贝初始化)
int c( 6 );    // 初始值在括号中 (直接初始化)

// 列表初始化 (C++11)
int d { 7 };   // 初始值在大括号中 (直接列表初始化)
int e = { 8 }; // 等号后跟大括号中的初始值 (拷贝列表初始化)
int f {};      // 空的大括号 (值初始化)
```

所有这些初始化方式对于具有类类型的对象都有效：

```C++
#include <iostream>

class Foo
{
public:
    
    // 默认构造函数
    Foo()
    {
        std::cout << "Foo()\n";
    }

    // 普通构造函数
    Foo(int x)
    {
        std::cout << "Foo(int) " << x << '\n';
    }

    // 拷贝构造函数
    Foo(const Foo&)
    {
        std::cout << "Foo(const Foo&)\n";
    }
};

int main()
{
    // 调用 Foo() 默认构造函数
    Foo f1;           // 默认构造函数
    Foo f2{};         // 值初始化 (优先使用)
    
    // 调用 foo(int) 普通构造函数
    Foo f3 = 3;       // 拷贝初始化 (非显式构造)
    Foo f4(4);        // 直接初始化
    Foo f5{ 5 };      // 直接列表初始化 (优化使用)
    Foo f6 = { 6 };   // 拷贝列表初始化 (非显式构造)

    // 调用 foo(const Foo&) 拷贝构造函数
    Foo f7 = f3;      // 拷贝初始化
    Foo f8(f3);       // 直接初始化
    Foo f9{ f3 };     // 直接列表初始化 (优化使用)
    Foo f10 = { f3 }; // 拷贝列表初始化

    return 0;
}
```

在现代C++中，拷贝初始化、直接初始化和列表初始化本质上做了相同的事情——它们初始化对象。

对于所有类型的初始化：

1. 初始化类类型时，将检查该类的构造函数集，并使用重载解析来确定最佳匹配的构造函数。这可能涉及参数的隐式转换。
2. 初始化非类类型时，隐式转换规则用于确定隐式转换是否存在。


还值得注意的是，在某些情况下，不允许某些形式的初始化（例如，在构造函数成员初始值设定项列表中，只能使用直接形式的初始化，而不能使用拷贝初始化）。

{{< alert success >}}
**关键点**

各种初始化之间有三个关键区别：

1. 列表初始化不允许窄化转换。
2. 拷贝初始化仅考虑非explict构造函数/转换函数。将在下一节进行介绍。
3. 列表初始化将匹配的列表构造函数优先于其他匹配的构造函数。将在后续进行讨论。

{{< /alert >}}

***
## 不必要的副本

考虑这个简单的程序：

```C++
#include <iostream>

class Something
{
    int m_x{};

public:
    Something(int x)
        : m_x{ x }
    {
        std::cout << "Normal constructor\n";
    }

    Something(const Something& s)
        : m_x { s.m_x }
    {
        std::cout << "Copy constructor\n";
    }

    void print() const { std::cout << "Something(" << m_x << ")\n"; }
};

int main()
{
    Something s { Something { 5 } }; // 注意这一行
    s.print();

    return 0;
}
```

在上面的变量s的初始化中，首先构造一个临时Something，用值5初始化（使用 Somethine(int) 构造函数）。然后使用该临时变量来初始化s。由于临时变量和s具有相同的类型（它们都是Something对象），因此通常会在此处调用 Somethine(const Something&) 拷贝构造函数，以将临时变量中的值复制到s中。最终结果是s用值5初始化。

如果没有任何优化，上述程序将打印：

```C++
Normal constructor
Copy constructor
Something(5)
```

然而，这个程序有些低效，因为不得不进行两个构造函数调用：一个是对 Something(int) 的调用，另一个是对于 Somethine(const Something&) 的调用。请注意，上面的最终需要的print结果与如下代码效果一样：

```C++
Something s { 5 }; // 只调用 Something(int), 不需要拷贝构造函数
```

这个版本产生相同的结果，但更有效，因为它只调用 Something(int) （不需要拷贝构造函数）。

***
## 拷贝省略

由于编译器可以自由地重写语句来优化它们，因此人们可能想知道编译器是否可以优化掉不必要的副本，并处理 Something s{Something{5}}；。

答案是肯定的，这样做的过程称为拷贝省略。拷贝省略是一种编译器优化技术，允许编译器删除不必要的对象复制。换句话说，在编译器通常调用拷贝构造函数的情况下，编译器可以自由重写代码，以避免调用拷贝构造函数。当编译器优化掉对拷贝构造函数的调用时，可以说拷贝构造函数已被省略。

与其他类型的优化不同，拷贝省略不受“仿佛”规则的约束。也就是说，即使拷贝构造函数有副作用（例如将文本打印到控制台），也允许拷贝省略来省略拷贝构造函数！这就是为什么拷贝构造函数不应该具有复制以外的副作用——如果编译器省略对拷贝构造函数的调用，副作用将不会执行，程序的可观察行为将改变！

可以在上面的例子中看到这一点。如果在C++17编译器上运行该程序，它将产生以下结果：

```C++
Normal constructor
Something(5)
```

编译器省略了拷贝构造函数以避免不必要的复制，因此，打印“Copy constructor”的语句不会执行！由于拷贝省略，程序的可观察行为发生了变化！

***
## 按值传递和按值返回中的拷贝省略

拷贝构造函数通常在参数按值传递或按值返回时调用。在某些情况下，这些副本可以内自动省略。以下程序演示了其中的一些情况：

```C++
#include <iostream>
class Something
{
public:
	Something() = default;
	Something(const Something&)
	{
		std::cout << "Copy constructor called\n";
	}
};

Something rvo()
{
	return Something{}; // 调用 Something() 和 拷贝构造
}

Something nrvo()
{
	Something s{}; // 调用 Something()
	return s;      // 调用 拷贝构造
}

int main()
{
	std::cout << "Initializing s1\n";
	Something s1 { rvo() }; // 调用 拷贝构造

	std::cout << "Initializing s2\n";
	Something s2 { nrvo() }; // 调用 拷贝构造

    return 0;
}
```

如果没有优化，上述程序将调用拷贝构造函数4次：

1. 当rvo将Something返回到main时。
2. 使用rvo()的返回值初始化s1时，执行一次。
3. nrvo返回s到main时一次。
4. 使用nrvo()的返回值初始化s2时一次。


然而，由于拷贝省略，编译器很可能会省略大多数或所有这些拷贝构造函数调用。Visual Studio 2022省略3种情况（它不省略nrvo()按值返回的情况），GCC省略所有4种情况。

记住编译器何时执行/不执行拷贝省略并不重要。只要知道这是编译器将在可能的情况下执行的优化，如果期望看到您的拷贝构造函数被调用，而它没有被调用，那么拷贝省略可能就是原因。

***
## 拷贝省略勘误表

在C++17之前，拷贝省略严格来说是编译器可以进行的可选优化。在C++17中，在某些情况下，拷贝省略是强制性的。

在可选的省略情况下，即使对拷贝构造函数的实际调用被省略，也必须有可访问的拷贝构造函数。

在强制省略情况下，可访问的拷贝构造函数不需要存在（换句话说，即使删除了拷贝构造函数，也可能发生强制省略）。

***

{{< prevnext prev="/basic/chapter14/copy-construct/" next="/basic/chapter14/convert-construct-explict/" >}}
14.13 拷贝构造函数简介
<--->
14.15 转换构造函数和explicit关键字
{{< /prevnext >}}
