---
title: "输入和输出参数"
date: 2024-02-19T14:35:47+08:00
---

函数及其调用者通过两种机制相互通信：参数和返回值。调用函数时，调用方提供输入，函数通过其参数接收这些输入。这些参数可以通过值、引用或地址传递。

通常，我们通过值或常量引用传递参数。但有时可能需要采取其他方式。

***
## 作为输入的参数

在大多数情况下，函数参数仅用于接收来自调用者的输入。

```C++
#include <iostream>

void print(int x) // x 是输入参数
{
    std::cout << x << '\n';
}

void print(const std::string& s) // s 是输入参数
{
    std::cout << s << '\n';
}

int main()
{
    print(5);
    std::string s { "Hello, world!" };
    print(s);

    return 0;
}
```

输入参数通常通过值或常量引用传递。

***
## 输出参数

通过（非常量）引用（或地址）传递的函数参数允许函数修改作为参数传递的对象的值。这为函数提供了一种方法，在由于某种原因使用返回值不足够的情况下，将数据返回给调用方。

仅用于将信息返回给调用者的函数参数称为输出参数。

例如：

```C++
#include <cmath>    // for std::sin() 和 std::cos()
#include <iostream>

// sinOut 和 cosOut 是输出参数
void getSinCos(double degrees, double& sinOut, double& cosOut)
{
    // sin() 和 cos() 需要弧度, 而不是角度, 所以需要转换下
    constexpr double pi { 3.14159265358979323846 }; // π的值
    double radians = degrees * pi / 180.0;
    sinOut = std::sin(radians);
    cosOut = std::cos(radians);
}
 
int main()
{
    double sin { 0.0 };
    double cos { 0.0 };
 
    double degrees{};
    std::cout << "Enter the number of degrees: ";
    std::cin >> degrees;

    // getSinCos 将会同时返回sin和cos计算的结果
    getSinCos(degrees, sin, cos);
 
    std::cout << "The sin is " << sin << '\n';
    std::cout << "The cos is " << cos << '\n';

    return 0;
}
```

该函数有一个参数degrees（通过值传递）作为输入，并“返回”两个参数（通过引用）作为输出。

我们用后缀“out”来命名这些输出参数。这有助于提醒调用方，传递给这些参数的初始值无关紧要，并且应该期望它们被覆盖。按照惯例，输出参数通常是最右边的参数。

让我们更详细地探讨一下这是如何工作的。首先，main函数创建局部变量sin和cos。它们通过引用（而不是通过值）传递到函数getSinCos()中。这意味着函数getSinCos()可以访问main()中的实际sin和cos变量，而不仅仅是副本。getSinCos()相应地将新值分配给sin和cos（分别通过引用sinOut和cosOut），这将覆盖sin和cos中的旧值。函数main()然后打印这些更新的值。

如果sin和cos是通过值而不是引用传递的，getSinCos()将更改sin和cos的副本，在函数末尾丢弃对副本的任何更改。但由于sin和cos是通过引用传递的，因此（通过引用）对sin或cos所做的任何更改都将持久化到函数之外。因此，可以使用该机制将值返回给调用者。

***
## 输出参数的语法不自然

输出参数虽然有效，但有一些缺点。

首先，调用方必须实例化（和初始化）对象，并将它们作为参数传递。这些对象必须能够被赋值，这意味着它们不能成为常量。

其次，由于调用方必须传入对象，因此这个对象不能是临时对象。

下面的示例显示了这两个缺点：

```C++
#include <iostream>

int getByValue()
{
    return 5;
}

void getByReference(int& x)
{
    x = 5;
}

int main()
{
    // 按值返回
    [[maybe_unused]] int x{ getByValue() }; // 可以用来初始化变量
    std::cout << getByValue() << '\n';      // 可以用来当做临时对象

    // 使用输出参数
    int y{};                // 首先需要初始化一个可被赋值的对象
    getByReference(y);      // 使用函数为该对象赋值
    std::cout << y << '\n'; // 然后使用该对象

    return 0;
}
```

正如所看到的，使用out参数的语法有点不自然。

***
## 输出参数，无法明确的看到传入的对象会被更改

当将函数的返回值赋给对象时，很明显，对象的值正在被修改：

```C++
x = getByValue(); // 显然x被修改
```

这清楚地表明，应该期望x的值发生变化。

然而，让我们再次查看上例中对getSinCos()的函数调用：

```C++
    getSinCos(degrees, sin, cos);
```

从这个函数调用中，无法明确的看出degrees是输入参数，sin和cos是输出参数。如果调用者没有意识到sin和cos将被修改，则可能会导致语义错误。

使用按地址传递而不是按引用传递，可以较为明确的看到输入的对象可能会被修改。

考虑以下示例：

```C++
void foo1(int x);  // 按值传递
void foo2(int& x); // 按引用传递
void foo3(int* x); // 按地址传递

int main()
{
    int i{};
 
    foo1(i);  // 无法修改 i
    foo2(i);  // 可以修改 i
    foo3(&i); // 可以修改 i

    int *ptr { &i };
    foo3(ptr); // 可以修改 i

    return 0;
}
```

请注意，在对foo3(&i)的调用中，必须传入&i，而不是i，这有助于更清楚地说明，应该期望i被修改。

然而，这并不是傻瓜式的，因为foo(ptr)允许foo()修改i，并且不需要调用者获取i的地址。

调用者还可能认为可以传入nullptr作为有效参数。现在需要该函数来执行空指针检查和处理，这增加了更多的复杂性。这种添加空指针处理，通常会比按引用传递容易造成更多的问题。

基于所有这些原因，应避免使用输出参数，除非不存在其它的选项。

***
## 输入/输出参数

在极少数情况下，函数会先使用传入的参数，然后对其进行修改。这样的参数称为输入输出参数。输入输出参数的工作方式与输出参数相同，并且具有所有相同的挑战。

***
## 何时使用非常量引用

如果要通过引用传递以避免复制参数，则几乎应该始终传递常量引用。

然而，在两种情况下，传递非常量引用可能是更好的选择。

首先，当参数是输入输出参数时，传递非常量引用。由于已经传入了需要返回的对象，因此只修改该对象通常更简单，性能更好。

```C++
void someFcn(Foo& inout)
{
    // 修改 inout
}

int main()
{
    Foo foo{};
    someFcn(foo); // foo 在调用后会被修改, 但可能不太明显看出来

    return 0;
}
```

给函数起一个好的名称可以帮助：

```C++
void modifyFoo(Foo& inout)
{
    // 修改 inout
}

int main()
{
    Foo foo{};
    modifyFoo(foo); // foo 在调用后会被修改, 稍微可读一点

    return 0;
}
```

另一种方法是改为按值传递对象或按常量引用传递，并按值返回新对象，然后调用者可以将其分配回原始对象：

```C++
Foo someFcn(const Foo& in)
{
    Foo foo { in }; // 拷贝
    // 修改 foo
    
    // 返回 foo
    return foo;
}

int main()
{
    Foo foo{};
    foo = someFcn(foo); // 明显看出foo被修改，但代码性能差

    return 0;
}
```

这具有传统的返回语法的好处，但需要制作两个额外的副本（有时编译器可以优化掉其中一个副本）。

第二，函数会修改输出参数，但按值返回时复制对象的成本非常高，传递非常量引用。特别是在代码的性能关键部分多次调用该函数时。

```C++
void generateExpensiveFoo(Foo& out)
{
    // 修改 out
}

int main()
{
    Foo foo{};
    generateExpensiveFoo(foo); // foo 在调用后会被修改

    return 0;
}
```

也就是说，对象的复制成本非常昂贵，求助于返回对象的非常规方法是值得的。

{{< alert success >}}
**对于高级读者**

上面最常见的例子是，当函数需要用数据填充大型C样式数组或std::vector。

{{< /alert >}}

***

{{< prevnext prev="/basic/chapter12/ret-ref-pointer/" next="/basic/chapter12/auto-type-deduct-ptr-ref-const/" >}}
12.11 引用或指针作为函数返回值
<--->
12.13 指针、引用和常量的类型自动推导
{{< /prevnext >}}
