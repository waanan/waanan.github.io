---
title: "关系运算符和浮点比较"
date: 2023-12-07T13:09:17+08:00
---

关系运算符是用于比较两个值的运算符。有6个关系运算符：





您已经看到了其中的大多数工作原理，它们非常直观。每个操作符的计算结果都是布尔值true（1）或false（0）。

下面是将这些运算符与整数一起使用的一些示例代码：

```C++
#include <iostream>

int main()
{
    std::cout << "Enter an integer: ";
    int x{};
    std::cin >> x;

    std::cout << "Enter another integer: ";
    int y{};
    std::cin >> y;

    if (x == y)
        std::cout << x << " equals " << y << '\n';
    if (x != y)
        std::cout << x << " does not equal " << y << '\n';
    if (x > y)
        std::cout << x << " is greater than " << y << '\n';
    if (x < y)
        std::cout << x << " is less than " << y << '\n';
    if (x >= y)
        std::cout << x << " is greater than or equal to " << y << '\n';
    if (x <= y)
        std::cout << x << " is less than or equal to " << y << '\n';

    return 0;
}
```

以及样本运行的结果：

在比较整数时，这些运算符非常容易使用。

***
## 布尔条件值

默认情况下，if语句或条件运算符（以及其他一些位置）中的条件计算为布尔值。

许多新程序员将编写这样的语句：

```C++
if (b1 == true) ...
```

这是多余的，因为==true实际上不会向条件添加任何值。相反，我们应该写：

```C++
if (b1) ...
```

类似地，如下所示：

```C++
if (b1 == false) ...
```

最好写为：

```C++
if (!b1) ...
```

{{< alert success >}}
**最佳做法**

不要添加不必要的==或！=到条件。它使它们更难阅读，而不会提供任何额外的价值。

{{< /alert >}}

***
## 比较计算的浮点值可能会有问题

考虑以下程序：

```C++
#include <iostream>

int main()
{
    double d1{ 100.0 - 99.99 }; // should equal 0.01 mathematically
    double d2{ 10.0 - 9.99 }; // should equal 0.01 mathematically

    if (d1 == d2)
        std::cout << "d1 == d2" << '\n';
    else if (d1 > d2)
        std::cout << "d1 > d2" << '\n';
    else if (d1 < d2)
        std::cout << "d1 < d2" << '\n';
    
    return 0;
}
```

变量d1和d2的值都应为0.01。但此程序打印了意外的结果：

如果在调试器中检查d1和d2的值，您可能会看到d1=0.010000000000005116和d2=0.99999999997868。这两个数字都接近0.01，但d1大于，d2小于。

使用任何关系运算符比较浮点值都可能是危险的。这是因为浮点值不精确，浮点操作数中的小舍入错误可能会导致它们比预期的稍小或稍大。这可以抛开关系运算符。

{{< alert success >}}
**相关内容**

我们在第4.8课-浮点数中讨论了舍入错误。

{{< /alert >}}

***
## 浮点小于和大于

当小于（<）、大于（>）、小于等于（<=）和大于等于（>=）运算符与浮点值一起使用时，它们在大多数情况下都会产生可靠的答案（当操作数的值不相似时）。然而，如果操作数几乎相同，则应认为这些运算符不可靠。例如，在上面的示例中，d1>d2碰巧产生true，但如果数值错误朝着不同的方向发展，则也可能同样容易产生false。

如果操作数相似时得到错误答案的结果是可以接受的，那么使用这些操作符也是可以接受的。这是一个特定于应用程序的决策。

例如，考虑一个游戏（如太空入侵者），您希望确定两个移动对象（如导弹和外星人）是否相交。如果对象仍然相距很远，则这些运算符将返回正确的答案。如果这两个对象非常接近，您可能会得到答案。在这种情况下，错误的答案可能根本不会被注意到（它只是看起来像是差点儿打中或差点儿击中），游戏将继续。

***
## 浮点等式和不等式

等式运算符（==和！=）要麻烦得多。考虑运算符==，它仅在其操作数完全相等时返回true。因为即使最小的舍入误差也会导致两个浮点数不相等，所以当可能预期为true时，运算符==返回false的风险很高。运算符！=也有同样的问题。

因此，通常应避免将这些运算符与浮点操作数一起使用。

上面有一个值得注意的例外情况：可以将低精度（几个有效数字）浮点文本与相同类型的相同文本值进行比较。

例如，如果函数返回这样的文本（通常为0.0，有时为1.0），则可以安全地对相同类型的相同文本值进行直接比较：

```C++
if (someFcn() == 0.0) // okay if someFcn() returns 0.0 as a literal only
    // do something
```

或者，如果我们有一个可以保证是文本的const或constexpr浮点变量，则可以安全地进行直接比较：

```C++
constexpr double gravity { 9.8 }
if (gravity == 9.8) // okay if gravity was initialized with a literal
    // we're on earth
```

为什么这样做有效？考虑双精度文字0.0。这个文本在内存中有一些特定和唯一的表示。因此，0.0==0.0应始终为真。0.0的副本也应该始终等于0.0。因此，我们可以安全地将返回文本0.0的函数（这是0.0的副本）或用文本0.0初始化的变量（这是0.05的副本）与文本0.0进行比较。

{{< alert success >}}
**警告**

避免使用运算符==和运算符！=比较浮点值（如果有机会计算这些值）。

{{< /alert >}}

{{< alert success >}}
**提示**

可以将低精度（几个有效数字）浮点文本与相同类型的相同文本值进行比较。

{{< /alert >}}

***
## 比较浮点数（高级/可选读取）

那么，我们如何合理地比较两个浮点操作数，看看它们是否相等呢？

实现浮点相等最常见的方法是使用一个函数来查看两个数字是否几乎相同。如果它们“足够接近”，那么我们称它们相等。用于表示“足够接近”的值传统上称为epsilon。Epsilon通常被定义为一个小正数（例如0.00000001，有时写为1e-8）。

新开发人员通常尝试编写自己的“足够接近”函数，如下所示：

```C++
#include <cmath> // for std::abs()

// absEpsilon is an absolute value
bool approximatelyEqualAbs(double a, double b, double absEpsilon)
{
    // if the distance between a and b is less than or equal to absEpsilon, then a and b are "close enough"
    return std::abs(a - b) <= absEpsilon;
}
```

std:：abs（）是<cmath>标头中的函数，它返回其参数的绝对值。因此，std:：abs（a-b）<=absEpsilon检查a和b之间的距离是否小于或等于传入的表示“足够近”的ε值。如果a和b足够近，函数返回true以指示它们相等。否则，它返回false。

虽然这个函数可以工作，但它不是很好。0.00001的ε对于1.0左右的输入很好，对于0.0000001左右的输入太大，对于10000之类的输入太小。

这意味着每次调用该函数时，我们都必须选择一个适合我们输入的ε。如果我们知道我们必须根据输入的大小按比例缩放ε，我们不妨修改函数来为我们做这件事。

著名计算机科学家唐纳德·克努特（Donald Knuth）在其著作《计算机编程的艺术》（the Art of computer Programming，Volume II）：半数值算法（Addison Wesley，1969）中提出了以下方法：

```C++
#include <algorithm> // for std::max
#include <cmath>     // for std::abs

// Return true if the difference between a and b is within epsilon percent of the larger of a and b
bool approximatelyEqualRel(double a, double b, double relEpsilon)
{
	return (std::abs(a - b) <= (std::max(std::abs(a), std::abs(b)) * relEpsilon));
}
```

在这种情况下，ε不是绝对数，而是相对于a或b的大小。

让我们更详细地研究一下这个看起来疯狂的函数是如何工作的。在<=运算符的左侧，std:：abs（a-b）将a和b之间的距离作为正数告诉我们。

在<=运算符的右侧，我们需要计算我们愿意接受的“足够接近”的最大值。为此，算法选择a和b中较大的一个（作为数字整体大小的粗略指示器），然后将其乘以relEpsilon。在该函数中，relEpsilon表示百分比。例如，如果我们想说“足够近”意味着a和b在a和b中较大者的1%以内，则我们传入0.01的relEpsilon（1%=1/100=0.01）。relEpsilion的值可以调整为最适合情况的任何值（例如，0.002的epsilon意味着在0.2%以内）。

要执行不等式（！=）而不是等式，只需调用此函数，并使用逻辑NOT运算符（！）来翻转结果：

```C++
if (!approximatelyEqualRel(a, b, 0.001))
    std::cout << a << " is not equal to " << b << '\n';
```

请注意，虽然近似EqualRel（）函数在大多数情况下都有效，但它并不完美，特别是当数字接近零时：

```C++
#include <algorithm> // for std::max
#include <cmath>     // for std::abs
#include <iostream>

// Return true if the difference between a and b is within epsilon percent of the larger of a and b
bool approximatelyEqualRel(double a, double b, double relEpsilon)
{
	return (std::abs(a - b) <= (std::max(std::abs(a), std::abs(b)) * relEpsilon));
}

int main()
{
    // a is really close to 1.0, but has rounding errors
    constexpr double a{ 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 };

    constexpr double relEps { 1e-8 };
    constexpr double absEps { 1e-12 };
    
    // First, let's compare a (almost 1.0) to 1.0.
    std::cout << approximatelyEqualRel(a, 1.0, relEps) << '\n';
 
    // Second, let's compare a-1.0 (almost 0.0) to 0.0
    std::cout << approximatelyEqualRel(a-1.0, 0.0, relEps) << '\n';

    return 0;
}
```

也许令人惊讶的是，它返回了：

第二个调用未按预期执行。数学简单地分解到接近零的程度。

避免这种情况的一种方法是使用绝对ε（正如我们在第一种方法中所做的那样）和相对ε（就像我们在Knuth方法中所作的那样）：

```C++
// Return true if the difference between a and b is less than or equal to absEpsilon, or within relEpsilon percent of the larger of a and b
bool approximatelyEqualAbsRel(double a, double b, double absEpsilon, double relEpsilon)
{
    // Check if the numbers are really close -- needed when comparing numbers near zero.
    if (std::abs(a - b) <= absEpsilon)
        return true;

    // Otherwise fall back to Knuth's algorithm
    return approximatelyEqualRel(a, b, relEpsilon);
}
```

在该算法中，我们首先检查a和b在绝对项上是否接近，这处理了a和b都接近于零的情况。absEpsilon参数应设置为非常小的值（例如1e-12）。如果失败，那么我们回到Knuth的算法，使用相对ε。

下面是我们以前测试这两种算法的代码：

```C++
#include <algorithm> // for std::max
#include <cmath>     // for std::abs
#include <iostream>

// Return true if the difference between a and b is within epsilon percent of the larger of a and b
bool approximatelyEqualRel(double a, double b, double relEpsilon)
{
	return (std::abs(a - b) <= (std::max(std::abs(a), std::abs(b)) * relEpsilon));
}

// Return true if the difference between a and b is less than or equal to absEpsilon, or within relEpsilon percent of the larger of a and b
bool approximatelyEqualAbsRel(double a, double b, double absEpsilon, double relEpsilon)
{
    // Check if the numbers are really close -- needed when comparing numbers near zero.
    if (std::abs(a - b) <= absEpsilon)
        return true;

    // Otherwise fall back to Knuth's algorithm
    return approximatelyEqualRel(a, b, relEpsilon);
}

int main()
{
    // a is really close to 1.0, but has rounding errors
    constexpr double a{ 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 };

    constexpr double relEps { 1e-8 };
    constexpr double absEps { 1e-12 };
    
    std::cout << approximatelyEqualRel(a, 1.0, relEps) << '\n';     // compare "almost 1.0" to 1.0
    std::cout << approximatelyEqualRel(a-1.0, 0.0, relEps) << '\n'; // compare "almost 0.0" to 0.0

    std::cout << approximatelyEqualAbsRel(a, 1.0, absEps, relEps) << '\n';     // compare "almost 1.0" to 1.0
    std::cout << approximatelyEqualAbsRel(a-1.0, 0.0, absEps, relEps) << '\n'; // compare "almost 0.0" to 0.0

    return 0;
}
```

可以看到，近似EqualAbsRel（）正确地处理小输入。

浮点数的比较是一个困难的话题，没有一种“一刀切”的算法适用于所有情况。然而，absEpsilon为1e-12、relEpsilon为1e-8的近似EqualyAbsRel（）函数应该足以处理您将遇到的大多数情况。

{{< alert success >}}
**作为旁白…**

如果我们说在另一个数字0.00001范围内的任何数字应被视为相同的数字，则：

1. 1和1.0001将不同，但1和1.00001将相同。这不是不合理的。
2. 0.0000001和0.00001应相同。这似乎不太好，因为这些数字相差两个数量级。
3. 10000和10000.0001是不同的。这似乎也不太好，因为考虑到数字的大小，这些数字几乎没有什么不同。


{{< /alert >}}

***
## 使近似等于函数constexpr高级

在C++23中，通过添加constexpr关键字，可以将两个近似等于函数设置为constexpr:

```C++
// C++23 version
#include <algorithm> // for std::max
#include <cmath>     // for std::abs (constexpr in C++23)

// Return true if the difference between a and b is within epsilon percent of the larger of a and b
constexpr bool approximatelyEqualRel(double a, double b, double relEpsilon)
{
	return (std::abs(a - b) <= (std::max(std::abs(a), std::abs(b)) * relEpsilon));
}

// Return true if the difference between a and b is less than or equal to absEpsilon, or within relEpsilon percent of the larger of a and b
constexpr bool approximatelyEqualAbsRel(double a, double b, double absEpsilon, double relEpsilon)
{
    // Check if the numbers are really close -- needed when comparing numbers near zero.
    if (std::abs(a - b) <= absEpsilon)
        return true;

    // Otherwise fall back to Knuth's algorithm
    return approximatelyEqualRel(a, b, relEpsilon);
}
```

然而，在C++23之前，我们遇到了一个问题。如果在常量表达式中调用这些constexpr函数，则它们将失败：

```C++
int main()
{
    // a is really close to 1.0, but has rounding errors
    constexpr double a{ 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 };

    constexpr double relEps { 1e-8 };
    constexpr double absEps { 1e-12 };

    constexpr bool same { approximatelyEqualAbsRel(a, 1.0, absEps, relEps) }; // compile error: must be initialized by a constant expression
    std::cout << same << '\n';

    return 0;
}
```

这是因为在常量表达式中使用的constexpr函数不能调用非常量的consteExpr函数，并且std:：abs直到C++23才成为constexpr。

但这很容易修复——我们可以将std:：abs丢弃为自己的constexpr绝对值实现。

```C++
// Prior to C++23 version
#include <algorithm> // for std::max
#include <iostream>

// Our own constexpr implementation of std::abs (for use prior to C++23)
// In C++23, use std::abs
// constAbs() can be called like a normal function, but can handle different types of values (e.g. int, double, etc...)
template <typename T>
constexpr T constAbs(T x)
{
    return (x < 0 ? -x : x);
}

// Return true if the difference between a and b is within epsilon percent of the larger of a and b
constexpr bool approximatelyEqualRel(double a, double b, double relEpsilon)
{
    return (constAbs(a - b) <= (std::max(constAbs(a), constAbs(b)) * relEpsilon));
}

// Return true if the difference between a and b is less than or equal to absEpsilon, or within relEpsilon percent of the larger of a and b
constexpr bool approximatelyEqualAbsRel(double a, double b, double absEpsilon, double relEpsilon)
{
    // Check if the numbers are really close -- needed when comparing numbers near zero.
    if (constAbs(a - b) <= absEpsilon)
        return true;

    // Otherwise fall back to Knuth's algorithm
    return approximatelyEqualRel(a, b, relEpsilon);
}

int main()
{
    // a is really close to 1.0, but has rounding errors
    constexpr double a{ 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 };

    constexpr double relEps { 1e-8 };
    constexpr double absEps { 1e-12 };

    constexpr bool same { approximatelyEqualAbsRel(a, 1.0, absEps, relEps) };
    std::cout << same << '\n';

    return 0;
}
```

{{< alert success >}}
**相关内容**

我们在第5.8课-constexpr和consteval函数中介绍了constexpr函数。

{{< /alert >}}

{{< alert success >}}
**对于高级读者**

上面的constAbs（）版本是一个函数模板，它允许我们编写可以处理不同类型值的单个定义。我们在第10.15课——函数模板中介绍了函数模板。

{{< /alert >}}

