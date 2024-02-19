---
title: "通过常量值引用"
date: 2024-02-19T14:35:47+08:00
---

与对非常量的引用（它只能绑定到可修改的左值）不同，对常量的引用可以绑定到可更改的左值、不可修改的左值和右值。因此，如果我们使引用参数为const，则它将能够绑定到任何类型的参数：

```C++
#include <iostream>

void printValue(const int& y) // y is now a const reference
{
    std::cout << y << '\n';
}

int main()
{
    int x { 5 };
    printValue(x); // ok: x is a modifiable lvalue

    const int z { 5 };
    printValue(z); // ok: z is a non-modifiable lvalue

    printValue(5); // ok: 5 is a literal rvalue

    return 0;
}
```

通过常量引用传递与通过引用传递提供相同的主要好处（避免复制参数），同时还保证函数不能更改被引用的值。

例如，不允许以下内容，因为ref是常量：

```C++
void addOne(const int& ref)
{
    ++ref; // not allowed: ref is const
}
```

在大多数情况下，我们不希望函数修改参数的值。

现在，我们可以理解允许常量左值引用绑定到右值的动机：没有该功能，就无法将文本（或其他右值）传递给使用逐引用传递的函数！

{{< alert success >}}
**最佳做法**

支持通过常量引用传递，而不是通过非常量引用传递，除非您有特定的原因需要这样做（例如，函数需要更改参数的值）。

{{< /alert >}}

***
## 混合旁路值和旁路参考

具有多个参数的函数可以确定每个参数是按值传递还是按引用单独传递。

例如：

```C++
#include <string>

void foo(int a, int& b, const std::string& c)
{
}

int main()
{
    int x { 5 };
    const std::string s { "Hello, world!" };

    foo(5, x, s);

    return 0;
}
```

在上面的示例中，第一个参数通过值传递，第二个通过引用传递，第三个通过常量引用传递。

***
## 何时通过（常量）引用

由于类类型的复制成本可能很高（有时显著如此），因此类类型通常通过常量引用传递，而不是通过值传递，以避免对参数进行昂贵的复制。基本类型的复制成本很低，因此它们通常是通过值传递的。

{{< alert success >}}
**最佳做法**

根据经验，通过值传递基本类型，通过常量引用传递类（或结构）类型。

通过值传递的其他常见类型：枚举类型和std:：string_view。要通过（const）引用传递的其他常见类型：std:：string、std:∶array和std::vector。

{{< /alert >}}

***
## 传递值与传递引用的成本高级

并非所有的类类型都需要通过引用传递。你可能想知道为什么我们不只是通过引用来传递所有内容。在本节（可选阅读）中，我们讨论了传递值与传递引用的成本，并改进了最佳实践，以确定何时应使用每种方法。

有两个关键点可以帮助我们理解何时应该按值传递而不是按引用传递：

首先，复制对象的成本通常与两个因素成比例：

1. 对象的大小。使用更多内存的对象复制需要更多的时间。
2. 任何额外的设置成本。一些类类型在实例化时执行额外的设置（例如，打开文件或数据库，或分配一定数量的动态内存来保存可变大小的对象）。每次复制对象时都必须支付这些设置成本。


另一方面，将引用绑定到对象总是很快的（大约与复制基本类型的速度相同）。

其次，通过引用访问对象比通过普通变量标识符访问对象稍微贵一些。使用变量标识符，正在运行的程序可以直接转到分配给该变量的存储器地址，并直接访问该值。对于引用，通常有一个额外的步骤：程序必须首先访问引用以确定引用的对象，然后才能转到该对象的内存地址并访问值。编译器有时也可以使用通过值传递的对象来优化代码，比使用通过引用传递的对象的代码更高。这意味着为访问通过引用传递的对象而生成的代码通常比为通过值传递的对象生成的代码慢。

我们现在可以回答为什么不通过引用传递所有内容的问题：

1. 对于复制成本较低的对象，复制的成本类似于绑定的成本，因此我们倾向于传递值，因此生成的代码将更快。
2. 对于复制成本高昂的对象，复制的成本占主导地位，因此我们倾向于通过（常量）引用来避免进行复制。


最后一个问题是，我们如何定义“廉价复制”？这里没有绝对的答案，因为这因编译器、用例和架构而异。然而，我们可以制定一个很好的经验法则：如果对象使用2个或更少的内存“字”（其中“字”由内存地址的大小近似），并且它没有设置成本，则复制对象的成本很低。

以下程序定义了一个类似于宏的函数，可用于确定类型（或对象）是否可以相应地廉价复制：

```C++
#include <iostream>

// Function-like macro that evaluates to true if the type (or object) is equal to or smaller than
// the size of two memory addresses
#define isSmall(T) (sizeof(T) <= 2 * sizeof(void*))

struct S
{
    double a;
    double b;
    double c;
};

int main()
{
    std::cout << std::boolalpha; // print true or false rather than 1 or 0
    std::cout << isSmall(int) << '\n'; // true
    std::cout << isSmall(double) << '\n'; // true
    std::cout << isSmall(S) << '\n'; // false

    return 0;
}
```

然而，很难知道类类型对象是否具有设置成本。最好假设大多数标准库类都有设置成本，除非您知道它们没有设置成本。

{{< alert success >}}
**最佳做法**

对于复制成本低的对象，首选传递值，对于复制成本高的对象，则首选传递常量引用。如果您不确定复制对象的成本是低还是高，请通过常量引用传递。

{{< /alert >}}

{{< alert success >}}
**作为旁白…**

我们在这里使用类似宏的预处理器函数，以便可以提供对象或类型名作为参数（普通函数不允许这样做）。

{{< /alert >}}

{{< alert success >}}
**提示**

如果sizeof（T）<=2*sizeof（void*）并且没有额外的设置成本，则T类型的对象复制成本很低。

{{< /alert >}}

***
## 对于函数参数，在大多数情况下，首选std:：string_view而不是const-std:：string&

在现代C++中经常出现的一个问题是：在编写具有字符串参数的函数时，参数的类型应该是const-std:：string&还是std:：string_view？

在大多数情况下，std:：string_view是更好的选择，因为它可以有效地处理更广泛的参数类型。

```C++
void doSomething(const std::string&);
void doSomething(std::string_view);   // prefer this in most cases
```

在某些情况下，使用const std:：string&参数可能更合适：

1. 如果您使用的是C++14或更高版本，则std:：string_view不可用。
2. 如果函数需要调用采用C样式字符串或std:：string参数的其他函数，则const std:∶string&可能是更好的选择，因为std::string_view不能保证以null结尾（C样式字符串函数所期望的），并且不能有效地转换回std:；string。


{{< alert success >}}
**最佳做法**

首选使用std:：string_view（按值）传递字符串，而不是使用const-std:：string&，除非您的函数调用其他需要C样式字符串或std:：string参数的函数。

{{< /alert >}}

***
## 为什么std:：string_view参数比const-std:：string Advanced更有效（&A）

在C++中，字符串参数通常是std:：string、std::string_view或C样式的string/string文本。

作为提醒：

1. 如果参数的类型与相应参数的类型不匹配，编译器将尝试隐式转换参数以匹配参数的类型。
2. 转换值将创建转换类型的临时对象。
3. 创建（或复制）std:：string_view的成本很低，因为std::string_view不会复制它正在查看的字符串。
4. 创建（或复制）std:：string可能代价很高，因为每个std:∶string对象都会复制该字符串。


下面的表格显示了当我们尝试传递每个类型时发生的情况：

使用std:：string_view值参数：

1. 如果我们传入一个std:：string参数，编译器将把std:：string转换为std:：string_view，这很便宜，因此这很好。
2. 如果我们传入一个std:：string_view参数，编译器将把该参数复制到该参数中，这是很便宜的，因此这很好。
3. 如果我们传入C样式的字符串或字符串文本，编译器将把它们转换为std:：string_view，这很便宜，因此这很好。


如您所见，std:：string_view以较低的成本处理所有三种情况。

使用const std:：string引用参数（&R）：

1. 如果我们传入一个std:：string参数，该参数将引用绑定到该参数，这是廉价的，因此这很好。
2. 如果传入std:：string_view参数，编译器将拒绝执行隐式转换，并产生编译错误。我们可以使用static_cast来执行显式转换（到std:：string），但这种转换代价很高（因为std:∶string将复制正在查看的字符串）。一旦完成转换，参数将引用绑定到结果，这是廉价的。但我们已经制作了一个昂贵的副本来进行转换，所以这不是很好。
3. 如果我们传入C样式的字符串或字符串文本，编译器将隐式地将其转换为std:：string，这很昂贵。所以这也不太好。


因此，const std:：string&parameter仅以较低的成本处理std:：string参数。

相同，代码形式：

```C++
#include <iostream>
#include <string>
#include <string_view>

void printSV(std::string_view sv)
{
    std::cout << sv << '\n';
}

void printS(const std::string& s)
{
    std::cout << s << '\n';
}

int main()
{
    std::string s{ "Hello, world" };
    std::string_view sv { s };

    // Pass to `std::string_view` parameter
    printSV(s);              // ok: inexpensive conversion from std::string to std::string_view
    printSV(sv);             // ok: inexpensive copy of std::string_view
    printSV("Hello, world"); // ok: inexpensive conversion of C-style string literal to std::string_view

    // pass to `const std::string&` parameter
    printS(s);              // ok: inexpensive bind to std::string argument
    printS(sv);             // compile error: cannot implicit convert std::string_view to std::string
    printS(static_cast<std::string>(sv)); // bad: expensive creation of std::string temporary
    printS("Hello, world"); // bad: expensive creation of std::string temporary

    return 0;
}
```

此外，我们需要考虑访问函数内部参数的成本。由于std:：string_view参数是普通对象，因此可以直接访问正在查看的字符串。访问std:：string&parameter需要额外的步骤来访问引用的对象，然后才能访问字符串。

