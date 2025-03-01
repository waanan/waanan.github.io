---
title: "异常规格和noexcept"
date: 2025-02-12T14:07:59+08:00
---

查看典型的函数声明，无法确定函数是否可能引发异常：

```C++
int doSomething(); // 这个函数是否会抛出异常?
```

在上面的示例中，doSomething()是否会引发异常？现在还不清楚。但在某些情况下，答案是重要的。在前面异常的危险和缺点中，我们描述了在调用栈展开期间从析构函数中抛出的异常会导致程序停止。如果doSomething()可以引发异常，那么从析构函数（或不希望引发异常的任何其他位置）调用它是有风险的。尽管我们可以让析构函数处理掉doSomething()引发的异常（因此这些异常不会传播到析构函数之外），但我们必须记住这样做，并且我们必须确保覆盖可能引发的所有不同类型的异常。

虽然注释可能有助于枚举函数是否引发异常（以及什么类型的异常），但文档可能会变得过时，并且编译器不会强制检查注释。

异常规格是一种语言机制，最初设计用于记录函数可能部分抛出的异常类型。虽然大多数异常规格现在都已弃用或删除，但有一个有用的异常规格，我们将在本课中介绍。

***
## noexcept说明符

在C++中，所有函数都被分类为不抛出或潜在抛出异常。不抛出函数承诺不抛出调用方可见的异常。

要将函数定义为不抛出异常，可以使用noexcept说明符。为此，在函数声明中使用noexcept关键字，放在函数参数列表的右侧：

```C++
void doSomething() noexcept; // 这个 function 承诺不抛出异常
```

注意，noexcept实际上并不阻止函数抛出异常或调用其他可能抛出异常的函数。只要noexcept函数在内部捕获和处理这些异常，并且这些异常不往上抛出，就没有问题。

如果未处理的异常将超出noexcept函数，则将调用std::terminate。并且，如果从noexcept函数内部调用std::terminate，调用栈展开可能会发生，也可能不会发生（取决于实现和优化），这意味着在终止之前，对象可能会被正确销毁，也可能没有被正确销毁。

与仅在返回值上不同的函数很相似，不能重载仅在异常规格上不同的函数。

{{< alert success >}}
**关键点**

noexcept函数做出的不抛出调用方可见的异常的承诺是契约承诺，而不是编译器强制执行的承诺。因此，虽然调用noexcept函数应该是安全的，但noexcept函数往上抛出异常，会导致契约被破坏，从而导致程序终止！

由于这个原因，最好不要让noexcept函数与异常混用，或者调用可能引发异常的函数！

{{< /alert >}}

***
## noexcept函数和异常

以下程序说明了各种情况下noexcept函数和异常的行为：

```C++
#include <iostream>

class Doomed
{
public:
    ~Doomed()
    {
        std::cout << "Doomed destructed\n";
    }
};

void thrower()
{
    std::cout << "Throwing exception\n";
    throw 1;
}

void pt()
{
    std::cout << "pt (potentally throwing) called\n";
    // 调用栈展开时，这个对象会被析构
    Doomed doomed{};
    thrower();
    std::cout << "This never prints\n";
}

void nt() noexcept
{
    std::cout << "nt (noexcept) called\n";
    // 调用栈展开时，这个对象会被析构
    Doomed doomed{};
    thrower();
    std::cout << "this never prints\n";
}

void tester(int c) noexcept
{
    std::cout << "tester (noexcept) case " << c << " called\n";
    try
    {
        (c == 1) ? pt() : nt();
    }
    catch (...)
    {
        std::cout << "tester caught exception\n";
    }
}

int main()
{
    std::cout << std::unitbuf; // 每次处理后，清空buffer
    std::cout << std::boolalpha; // 将 bool 打印为 true/false
    tester(1);
    std::cout << "Test successful\n\n";
    tester(2);
    std::cout << "Test successful\n";

    return 0;
}
```

在作者的机器上，该程序打印：

```C++
tester (noexcept) case 1 called
pt (potentially throwing) called
Throwing exception
Doomed destructed
tester caught exception
Test successful

tester (noexcept) case 2 called
nt (noexcept) called
throwing exception
terminate called after throwing an instance of 'int'
```

然后程序中止。

让我们更详细地了解一下这里发生了什么。注意，tester是一个noexcept函数，因此承诺不会向调用方（main）抛出任何异常。

第一种情况说明，noexcept函数可以调用潜在的抛出函数，甚至可以处理这些函数抛出的任何异常。首先，调用tester(1)，它调用潜在的抛出函数pt()，该函数调用thrower()，抛出异常。该异常的第一个处理程序在tester()中，因此该异常展开调用栈（销毁在该过程中要析构的局部变量），并在tester()内捕获和处理该异常。由于tester()不向调用者（main）抛出此异常，因此这里没有违反noexcept，并且控制流返回到main。

第二种情况说明了当noexcept函数试图将异常传递回其调用方时发生的情况。首先，调用tester(2)，它调用noexcept函数nt()，该函数调用thrower()，抛出异常。此异常的第一个处理程序在tester()中。然而，nt()是noexcept，为了到达tester()中的处理程序，异常必须传播到nt()的调用方。这违反了nt()的noexcept，因此调用了std::terminate，我们的程序立即中止。在作者的机器上，调用栈没有被展开（doomed没有被析构）。

***
## 具有布尔参数的noexcept说明符

noexcept说明符具有可选的布尔参数。noexcept(true)相当于no exception，这意味着函数是不抛出异常的。noexcept(false)表示函数可能会抛出异常。这些参数通常仅用于模板函数，因为可以基于某些参数化值，动态决定创建的模板函数是否承诺抛出异常。

***
## 哪些函数标记为不抛出（noexcept）或潜在抛出异常

隐式不抛出的函数：

1. 析构函数

对于隐式或默认情况下不会抛出异常的函数：

1. 构造函数：默认构造、拷贝构造、移动构造
2. 赋值：拷贝、移动
3. 比较运算符（从C++20开始）


然而，如果这些函数中的任何一个调用（显式或隐式）另一个可能引发异常的函数，则所列出的函数也将被视为可能抛出异常。例如，如果类具有潜在抛出异常的构造函数的数据成员，则该类的构造函数也将被视为潜在抛出异常。作为另一个示例，如果拷贝赋值操作符调用可能引发异常的拷贝操作符，则拷贝赋值也可能抛出异常。

可能抛出异常的函数（如果未显式声明或默认情况下）：

1. 正常函数
2. 用户定义的构造函数
3. 用户定义的运算符

***
## noexcept运算符

noexcept运算符也可以在表达式内部使用。它接受表达式作为参数，如果编译器认为它将抛出异常或不抛出异常，则返回true或false。noexcept操作符在编译时静态检查，并且不会实际计算输入表达式。

```C++
void foo() {throw -1;}
void boo() {};
void goo() noexcept {};
struct S{};

constexpr bool b1{ noexcept(5 + 3) }; // true; ints 相加不会抛出异常
constexpr bool b2{ noexcept(foo()) }; // false; foo() 会抛出异常
constexpr bool b3{ noexcept(boo()) }; // false; boo() 隐式的标记为 noexcept(false)
constexpr bool b4{ noexcept(goo()) }; // true; goo()  显式的标记为 noexcept(true)
constexpr bool b5{ noexcept(S{}) };   // true; 一个 struct 的默认构造函数默认标记为 noexcept
```

noexcept运算符可以用于根据代码是否可能抛出异常来有条件地执行代码。这是实现某些异常安全行为保证所必需的，我们将在下一节中讨论。

***
## 异常安全保证

异常安全保证是关于发生异常时函数或类的行为的合同指南。异常安全保障有四个级别：

1. 无保证——不能保证如果抛出异常会发生什么（例如，类可能处于不可用状态）
2. 基本保证——如果抛出异常，则不会泄漏内存，并且对象仍然可用，但程序的状态可能已经被修改。
3. 强保证——如果抛出异常，则不会泄漏内存，并且不会更改程序状态。这意味着函数必须完全成功，或者在失败时没有副作用。如果故障发生在最初修改任何内容之前，这很容易，但也可以通过回滚所有更改来实现，以便程序返回到故障前状态。
4. 不抛出/无失败保证——函数将始终成功，或者失败了也不会向调用方抛出异常。异常在函数内部就处理妥善。noexcept说明符映射到此级别的异常安全保证。

让我们更详细地看一下不抛出/无失败保证：

不抛出保证：如果函数失败，则不会抛出异常。相反，它将返回错误代码或忽略问题。当处理异常当前异常导致的调用栈展开期间，需要不抛出保证；例如，所有析构函数都应该有不抛出保证（就像那些析构函数调用的任何函数一样）。不抛出的代码示例：

1. 析构函数和内存释放/清理函数

无失败保证：函数将总是成功地完成它试图执行的操作（因此从不需要抛出异常，因此，无失败是一种略强的不抛出形式）。不失败的代码示例：

1. 移动构造函数和移动赋值
2. 交换函数
3. 容器上的清除/擦除/重置功能
4. 对std::unique_ptr的操作

***
## 何时使用noexcept

仅仅因为代码没有显式抛出任何异常，并不意味着您应该在代码周围撒上noexcept。默认情况下，大多数函数都可能抛出异常，因为您的函数调用其它函数，被调函数可能会抛出异常。

有几个很好的理由将函数标记为noexcept：

1. 可以安全调用的函数，如析构函数
2. noexcept函数可以使编译器执行一些在其他情况下不可用的优化。由于noexcept函数不会向函数外部抛出异常，编译器不必操心运行时进行调用栈展开，这可以使它生成更快的代码。
3. 在一些重要的情况下，知道函数是noexcept允许我们在自己的代码中产生更有效的实现：标准库容器（如std::vector）是noexcept感知的，并将使用noexcept操作符来确定在某些地方是使用移动语义（更快）还是拷贝语义（较慢）。我们在下一节中进行介绍（std::move_if_noexcept)。

标准库的策略是仅在不抛出异常的函数上使用noexcept。可能引发但实际上不引发异常（由于实现）的函数通常不会标记为noexcept。

对于您自己的代码，始终将以下标记为noexcept：

1. 移动构造函数
2. 移动赋值运算符
3. Swap函数

请考虑将以下标记为noexcept：

1. 要表示不抛出或无失败保证的函数（例如，记录可以从析构函数或其他noexcept函数安全调用它们）
2. 拷贝构造函数和拷贝赋值运算符（以利用优化）。
3. 析构函数。析构函数隐式为noexcept（只要所有成员变量都具有noexcept析构函数）。

{{< alert success >}}
**最佳实践**

如果您不确定函数是否应该具有无故障/无抛出保证，那么出于谨慎的考虑，请不要用noexcept标记它。撤消使用noexcept的决定违反了对用户关于函数行为的接口承诺，并且可能会破坏现有代码。而在最初不是noexcept的函数中添加noexcept来增强保证通常被认为是安全的。

{{< /alert >}}

***
## 动态异常规格（可选阅读）

在C++11之前和C++17之前，使用动态异常规范来代替noexcept。动态异常规范语法使用throw关键字列出函数可以直接或间接引发的异常类型：

```C++
int doSomething() throw(); // 不抛出异常
int doSomething() throw(std::out_of_range, int*); // 可能抛出 std::out_of_range 或 int*
int doSomething() throw(...); // 可能抛出任何异常
```

由于不完整的编译器实现、与模板函数的一些不兼容、对它们如何工作的常见误解以及标准库大多不使用它们的事实，动态异常规格在C++11中被弃用，并从C++17和C++20的语言中删除。

***