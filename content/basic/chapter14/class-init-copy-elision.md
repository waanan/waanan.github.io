---
title: "类初始化和复制省略"
date: 2024-04-09T13:02:20+08:00
---

回到第1.4课——变量赋值和初始化，我们讨论了具有基本类型的对象的6种基本初始化类型：

```C++
int a;         // no initializer (default initialization)
int b = 5;     // initializer after equals sign (copy initialization)
int c( 6 );    // initializer in parentheses (direct initialization)

// List initialization methods (C++11)
int d { 7 };   // initializer in braces (direct list initialization)
int e = { 8 }; // initializer in braces after equals sign (copy list initialization)
int f {};      // initializer is empty braces (value initialization)
```

所有这些初始化类型对于具有类类型的对象都有效：

```C++
#include <iostream>

class Foo
{
public:
    
    // Default constructor
    Foo()
    {
        std::cout << "Foo()\n";
    }

    // Normal constructor
    Foo(int x)
    {
        std::cout << "Foo(int) " << x << '\n';
    }

    // Copy constructor
    Foo(const Foo&)
    {
        std::cout << "Foo(const Foo&)\n";
    }
};

int main()
{
    // Calls Foo() default constructor
    Foo f1;           // default initialization
    Foo f2{};         // value initialization (preferred)
    
    // Calls foo(int) normal constructor
    Foo f3 = 3;       // copy initialization (non-explicit constructors only)
    Foo f4(4);        // direct initialization
    Foo f5{ 5 };      // direct list initialization (preferred)
    Foo f6 = { 6 };   // copy list initialization (non-explicit constructors only)

    // Calls foo(const Foo&) copy constructor
    Foo f7 = f3;      // copy initialization
    Foo f8(f3);       // direct initialization
    Foo f9{ f3 };     // direct list initialization (preferred)
    Foo f10 = { f3 }; // copy list initialization

    return 0;
}
```

在现代C++中，复制初始化、直接初始化和列表初始化本质上做了相同的事情——它们初始化对象。

对于所有类型的初始化：

1. 初始化类类型时，将检查该类的构造函数集，并使用重载解析来确定最佳匹配的构造函数。这可能涉及参数的隐式转换。
2. 初始化非类类型时，隐式转换规则用于确定隐式转换是否存在。


还值得注意的是，在某些情况下，不允许某些形式的初始化（例如，在构造函数成员初始值设定项列表中，我们只能使用直接形式的初始化，而不能使用复制初始化）。

{{< alert success >}}
**关键洞察力**

初始化表单之间有三个关键区别：

1. 列表初始化不允许缩小转换。
2. 复制初始化仅考虑非显式构造函数/转换函数。我们将在第14.16课中讨论这一点——转换构造函数和显式关键字。
3. 列表初始化将匹配的列表构造函数优先于其他匹配的构造函数。我们将在第16.2课中讨论这一点——介绍std:：vector和list构造函数。


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
    Something s { Something { 5 } }; // focus on this line
    s.print();

    return 0;
}
```

在上面的变量s的初始化中，我们首先构造一个临时Something，用值5初始化（它使用Somethine（int）构造函数）。然后使用该临时变量来初始化s。由于临时变量和s具有相同的类型（它们都是Something对象），因此通常会在此处调用Somethine（const Something&）复制构造函数，以将临时变量中的值复制到s中。最终结果是s用值5初始化。

如果没有任何优化，上述程序将打印：

然而，这个程序是不必要的低效，因为我们不得不进行两个构造函数调用：一个是对Something（int）的调用，另一个是对于Something&的调用。请注意，上面的最终结果与我们编写的内容相同：

```C++
Something s { 5 }; // only invokes Something(int), no copy constructor
```

这个版本产生相同的结果，但更有效，因为它只调用Something（int）（不需要复制构造函数）。

***
## 复制省略号

由于编译器可以自由地重写语句来优化它们，因此人们可能想知道编译器是否可以优化掉不必要的副本，并处理Somethings{Something{5}}；好像我们一开始就写了一些东西。

答案是肯定的，这样做的过程称为复制省略。复制省略是一种编译器优化技术，允许编译器删除不必要的对象复制。换句话说，在编译器通常调用复制构造函数的情况下，编译器可以自由重写代码，以避免完全调用复制构造函数。当编译器优化掉对复制构造函数的调用时，我们说构造函数已被省略。

与其他类型的优化不同，复制省略不受“仿佛”规则的约束。也就是说，即使复制构造函数有副作用（例如将文本打印到控制台），也允许复制省略来省略复制构造函数！这就是为什么复制构造函数不应该具有复制以外的副作用——如果编译器省略对复制构造函数的调用，副作用将不会执行，程序的可观察行为将改变！

我们可以在上面的例子中看到这一点。如果在C++17编译器上运行该程序，它将产生以下结果：

编译器省略了复制构造函数以避免不必要的复制，因此，打印“复制构造函数”的语句不会执行！由于复制省略，我们程序的可观察行为发生了变化！

{{< alert success >}}
**相关内容**

我们在第5.4课中讨论了类似规则——常量表达式和编译时优化。

{{< /alert >}}

***
## 按值传递和按值返回中的复制省略

复制构造函数通常在使用与参数相同类型的参数按值传递或按值返回时调用。然而，在某些情况下，这些副本可以省略。以下程序演示了其中的一些情况：

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
	return Something{}; // calls Something() and copy constructor
}

Something nrvo()
{
	Something s{}; // calls Something()
	return s;      // calls copy constructor
}

int main()
{
	std::cout << "Initializing s1\n";
	Something s1 { rvo() }; // calls copy constructor

	std::cout << "Initializing s2\n";
	Something s2 { nrvo() }; // calls copy constructor

        return 0;
}
```

如果没有优化，上述程序将调用复制构造函数4次：

1. 当rvo将某物返回到main时。
2. 使用rvo（）的返回值初始化s1时，执行一次。
3. nrvo返回s到main时一次。
4. 使用nrvo（）的返回值初始化s2时一次。


然而，由于复制省略，编译器很可能会省略大多数或所有这些复制构造函数调用。Visual Studio 2022省略3种情况（它不省略nrvo（）按值返回的情况），GCC省略所有4种情况。

记住编译器何时执行/不执行复制省略并不重要。只要知道这是编译器将在可能的情况下执行的优化，如果您希望看到您的复制构造函数被调用，而它没有被调用，那么复制省略可能就是原因。

***
## 复制省略勘误表

在C++17之前，复制省略严格来说是编译器可以进行的可选优化。在C++17中，在某些情况下，复制省略是强制性的。

在可选的省略情况下，即使对复制构造函数的实际调用被省略，也必须有可访问的复制构造函数（例如，未删除）。

在强制省略情况下，可访问的复制构造函数不需要可用（换句话说，即使删除了复制构造函数，也可能发生强制省略）。

