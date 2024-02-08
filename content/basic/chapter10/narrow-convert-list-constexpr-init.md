---
title: "窄化转换、列表初始化和constexpr初始化"
date: 2024-01-31T13:21:38+08:00
---

在上一课中，我们介绍了数值转换，它涵盖了基本类型之间的各种不同类型的转换。

***
## 窄化转换

在C++中，窄化转换（narrowing conversion）是一种潜在的不安全的数值转换，其中目标类型可能无法保存源类型的所有值。

以下转换被定义为窄化转换：

1. 从浮点类型到整型。
2. 从浮点类型到级别较窄或较低的浮点类型，除非要转换的值是constexpr并且在目标类型的范围内（即使目标类型的精度不足以存储数字的所有有效数字）。
3. 从整数类型转换为浮点类型，除非要转换的值是constexpr，并且其值可以精确存储在目标类型中。
4. 从整型转换为不能表示原始类型的所有值的另一整型，除非要转换的值是constexpr，并且其值可以精确存储在目标类型中。这包括从宽到窄的整数转换，以及整数符号转换（有符号到无符号，反之亦然）。


在大多数情况下，隐式窄化转换将导致编译器警告，但有符号/无符号转换除外（根据编译器的配置方式，这可能会产生警告，也可能不会产生警告）。

应尽可能避免窄化转换，因为它们可能不安全，是潜在错误的来源。

***
## 有意的显式进行窄化转换

窄化转换并不总是可以避免的——对于函数调用尤其如此，其中函数参数和传入的类型可能不匹配，并且需要窄化转换。

在这种情况下，最好使用static_cast将隐式窄化转换替换为显式窄化转换。这样做有助于记录窄化转换是有意的，并将禁止任何编译器警告或错误。

例如：

```C++
void someFcn(int i)
{
}

int main()
{
    double d{ 5.0 };
    
    someFcn(d); // bad: 隐式的窄化转换可能导致编译器告警

    // good: 告诉编译器，这里的窄化是有意的，无需告警
    someFcn(static_cast<int>(d)); // 不会产生告警
    
    return 0;
}
```

{{< alert success >}}
**最佳实践**

如果需要执行窄化转换，请使用static_cast进行显式转换。

{{< /alert >}}

***
## 大括号初始化不允许窄化转换

使用大括号初始化时不允许窄化转换（这是首选此初始化形式的主要原因之一），尝试这样做将产生编译错误。

例如：

```C++
int main()
{
    int i { 3.5 }; // 编译失败

    return 0;
}
```

Visual Studio生成以下错误：

```C++
error C2397: conversion from 'double' to 'int' requires a narrowing conversion
```


如果您确实希望在大括号初始化中进行窄化转换，请使用static_cast做显式转换：

```C++
int main()
{
    double d { 3.5 };

    // static_cast<int> 将 double 转 int, 用转换后的结果初始化变量 i
    int i { static_cast<int>(d) }; 

    return 0;
}
```

***
## 一些constexpr转换不被认为是窄化

如果窄化转换的源值，在运行时才能确定，那么转换的结果也知道到运行时才能知道，所以是否能保留原值，也知道运行时才能确定。例如：

```C++
#include <iostream>

void print(unsigned int u) // 注: unsigned
{
    std::cout << u << '\n';
}

int main()
{
    std::cout << "Enter an integral value: ";
    int n{};
    std::cin >> n; // 输入 5 或 -5
    print(n);      // 转换成unsigned，无法确定能否保留原值

    return 0;
}
```

在上面的程序中，编译器不知道将为n输入什么值。当调用print(n)时，将在那时执行从int到unsigned int的转换。转换结果可能是保留原值的，也可能不保留原值，这取决于输入的值。因此，启用了有符号/无符号警告的编译器将针对这种情况发出警告。

然而，您可能已经注意到，大多数窄化转换定义都有一个以“除非要转换的值是constexpr和…”的条件。例如，当转换是“从整型到不能表示原始类型的所有值的另一整型，除非被转换的值是constexpr，并且其值可以精确存储在目标类型中”时，转换是窄化的。

当窄化转换的源值为constexpr时，编译器一定可以知道要转换的特定值。在这种情况下，编译器可以自己执行转换，然后检查值是否被完全保留。如果未能完全保留该值，编译器可能会因错误而停止编译。如果完全保留该值，则转换不会被认为是窄化的（并且编译器可以用转换的结果替换整个转换，这样替换是安全的）。

例如：

```C++
#include <iostream>

int main()
{
    constexpr int n1{ 5 };   // note: constexpr
    unsigned int u1 { n1 };  // okay: 这里的转换不被认为窄化

    constexpr int n2 { -5 }; // note: constexpr
    unsigned int u2 { n2 };  // 编译失败: 原值n2无法在u2里完全保存下来

    return 0;
}
```

让我们将规则“从整型到不能表示原始类型的所有值的另一整型，除非被转换的值是constexpr，并且其值可以精确存储在目标类型中”应用于上述两个转换。

在n1和u1的情况下，n1是int，u1是unsigned int，因此这是从整型到另一整型的转换，不能表示原始类型的所有值。然而，n1是constexpr，其值5可以在目标类型中精确表示（作为无符号值5）。因此，这不被认为是窄化转换，并且允许使用n1初始化u1。

在n2和u2的情况下，情况类似。尽管n2是constexpr，但它的值-5不能在目标类型中精确表示，因此这被认为是一种窄化转换，并且由于我们正在进行列表初始化，编译器将报错并停止编译。

奇怪的是，从浮点类型到整型的转换没有constexpr排除子句，因此即使要转换的值是constexpr。并且适合目标类型的存储范围，这些转换也始终被认为是窄化转换：

```C++
int n { 5.0 }; // 编译失败: 窄化转换
```

***
## 使用constexpr进行列表初始化

当列表初始化非int/非double对象时，这些constexpr子句非常有用，因为我们可以使用int或double字面值（或constexper对象）作为初始化值。

这使我们能够避免：

1. 在大多数情况下必须使用字面值后缀
2. 必须使用static_cast来扰乱初始化


例如：

```C++
int main()
{
    // 这样写可以免除字面值后缀
    unsigned int u { 5 }; // okay (不需要使用 `5u`)
    float f { 1.5 };      // okay (不需要使用 `1.5f`)

    // 可以不用 static_casts
    constexpr int n{ 5 };
    double d { n };       // okay (不需要 static_cast)
    short s { 5 };        // okay (不需要 static_cast)

    return 0;
}
```

这也适用于复制和直接初始化。

值得一提的一个警告：只要值在目标类型的范围内，就允许使用constexpr值来初始化较窄的浮点类型，即使目标类型没有足够的精度来精确存储该值！

{{< alert success >}}
**关键点**

浮点类型按以下顺序排序（从大到小）：

1. Long double
2. Double
3. Float
{{< /alert >}}

因此，这样的操作是合法的，不会产生错误：

```C++
int main()
{
    float f { 1.23456789 }; // 不是窄化转换, 即使发生了精度丢失!

    return 0;
}
```

然而，在这种情况下，编译器可能仍然会发出警告（如果使用-Wconversion编译标志，GCC和Clang会发出警告）。

***

{{< prevnext prev="/basic/chapter10/num-convert/" next="/basic/chapter10/arithmetic-convert/" >}}
10.2 数值转换
<--->
10.4 算术转换
{{< /prevnext >}}
