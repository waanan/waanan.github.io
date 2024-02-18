---
title: "具有多个模板类型的函数模板"
date: 2024-02-10T01:33:43+08:00
---

在前面，我们编写了一个函数模板来计算两个值的最大值：

```C++
#include <iostream>

template <typename T>
T max(T x, T y)
{
    return (x < y) ? y : x;
}

int main()
{
    std::cout << max(1, 2) << '\n';   // 会实例化 max(int, int)
    std::cout << max(1.5, 2.5) << '\n'; // 会实例化 max(double, double)

    return 0;
}
```

现在考虑以下类似的程序：

```C++
#include <iostream>

template <typename T>
T max(T x, T y)
{
    return (x < y) ? y : x;
}

int main()
{
    std::cout << max(2, 3.5) << '\n';  // 编译失败

    return 0;
}
```

您可能会惊讶地发现，这个程序无法编译。相反，编译器将发出一堆（可能看起来很疯狂）错误消息。在Visual Studio上，作者获得了以下信息：

```C++
Project3.cpp(11,18): error C2672: 'max': no matching overloaded function found
Project3.cpp(11,28): error C2782: 'T max(T,T)': template parameter 'T' is ambiguous
Project3.cpp(4): message : see declaration of 'max'
Project3.cpp(11,28): message : could be 'double'
Project3.cpp(11,28): message : or       'int'
Project3.cpp(11,28): error C2784: 'T max(T,T)': could not deduce template argument for 'T' from 'double'
Project3.cpp(4): message : see declaration of 'max'
```

在函数调用max(2, 3.5)中，我们传递两种不同类型的参数：一个int和一个double。因为我们在不使用尖括号来指定实际类型的情况下进行函数调用，编译器将首先查看max(int, double) 是否存在非模板匹配。无法找到一个。

接下来，编译器将查看是否可以找到函数模板匹配（使用模板参数推导）。然而，这也将失败，原因很简单：T只能表示单个类型。编译器无法将函数模板max<T>(T, T)实例化为具有两种不同参数类型的函数。换句话说，由于函数模板中的两个参数都是T类型，因此它们必须解析为相同的实际类型。

由于没有找到非模板匹配，也没有找到模板匹配，因此函数调用无法解析，并且我们得到一个编译错误。

您可能想知道为什么编译器不生成函数max<double>(double, double)，然后使用数值转换将int参数类型转换为double。答案很简单：类型转换仅在解析函数重载时进行，而不是在执行模板参数推导时。

这种类型转换的缺乏是故意的，至少有两个原因。首先，它有助于保持事情简单：自动模版类型参数推导只能找到精确匹配的结果。其次，它允许为希望确保两个或多个参数具有相同类型的情况创建函数模板（如上面的示例所示）。

我们必须找到另一个解决办法。幸运的是，我们可以（至少）用三种方法解决这个问题。

***
## 使用static_cast将参数转换为匹配类型

第一个解决方案是让调用者承担将参数转换为匹配类型的负担。例如：

```C++
#include <iostream>

template <typename T>
T max(T x, T y)
{
    return (x < y) ? y : x;
}

int main()
{
    std::cout << max(static_cast<double>(2), 3.5) << '\n'; // 将int转换为double，以便调用 max(double, double)

    return 0;
}
```

既然这两个参数都是double类型，编译器将能够实例化满足此函数调用的max(double, double)。

然而，这个解决方案不一定总能满足需求。

***
## 提供显式类型模板参数

如果我们已经编写了一个非模板max(double, double)函数，那么我们将能够调用max(int，double)，并通过隐式类型转换规则将int参数转换为double，以便可以解析到对应的函数调用：

```C++
#include <iostream>

double max(double x, double y)
{
    return (x < y) ? y : x;
}

int main()
{
    std::cout << max(2, 3.5) << '\n'; // int 参数会被转换为 double

    return 0;
}
```

然而，当编译器进行模板参数推导时，它不会进行任何类型转换。幸运的是，如果指定要使用的显式类型模板参数，则不必使用模板参数推导：

```C++
#include <iostream>

template <typename T>
T max(T x, T y)
{
    return (x < y) ? y : x;
}

int main()
{
    // 显示声明类型 double, 编译器无需进行模板类型推导
    std::cout << max<double>(2, 3.5) << '\n';

    return 0;
}
```

在上面的示例中，我们将显式调用max<double>(2, 3.5)。因为已经明确指定T应该替换为double，所以编译器不会使用模板参数推导。相反，它将只实例化函数max<double>(double, double)，然后转换任何不匹配的参数。int参数将隐式转换为double。

虽然这比使用static_cast更具可读性，但如果我们在对max进行函数调用时根本不必考虑类型，那就更好了。

***
## 具有多个模板类型参数的函数模板

问题的根源是，我们只为函数模板定义了单个模板类型参数（T），然后指定两个参数必须是同一类型。

解决这个问题的最好方法是重写函数模板，使我们的参数可以解析为不同的类型。我们现在将使用两个（T和U）：

```C++
#include <iostream>

template <typename T, typename U> // 使用两个模板类型参数 T 和 U
T max(T x, U y) // x 是类型 T, y 是类型 U
{
    return (x < y) ? y : x; // uh ，这里有个隐式的窄化转换
}

int main()
{
    std::cout << max(2, 3.5) << '\n';

    return 0;
}
```

因为我们已经用模板类型T定义了x，用模板类型U定义了y，所以x和y现在可以独立地解析它们的类型。当我们调用max(2, 3.5)时，T是int，U是double。编译器将为我们实例化max<int，double>(int, double)。

然而，上面的代码仍然有一个问题：double优先于int，因此我们的条件运算符将返回double。但我们的函数被定义为返回T——在T解析为int的情况下，double返回值将窄化转换为int，这将产生编译告警（以及可能的数据丢失）。

相反，将返回类型设置为U并不能解决问题，因为我们总是可以在函数调用中翻转操作数的顺序，翻转T和U的类型。

我们如何解决这个问题？这是自动返回类型的一个很好的用途——我们让编译器从return语句中推断出返回类型应该是什么：

```C++
#include <iostream>

template <typename T, typename U>
auto max(T x, U y)
{
    return (x < y) ? y : x;
}

int main()
{
    std::cout << max(2, 3.5) << '\n';

    return 0;
}
```

这个版本的max现在可以很好地处理不同类型的操作数。

{{< alert success >}}
**关键点**

每个模板类型参数都将独立解析其类型。

这意味着具有两个类型参数T和U的模板可以将T和U解析为不同的类型，或者它们可以解析为相同的类型。

{{< /alert >}}

***
## 函数模板简化（C++20）

C++20引入了auto关键字的新用法：当auto关键字用作普通函数中的参数类型时，编译器将自动将函数转换为函数模板，每个auto参数都成为独立的模板类型参数。用于创建函数模板的方法称为简写函数模板（abbreviated function template）。

例如：

```C++
auto max(auto x, auto y)
{
    return (x < y) ? y : x;
}
```

在C++20中是以下内容的简写：

```C++
template <typename T, typename U>
auto max(T x, U y)
{
    return (x < y) ? y : x;
}
```

这与我们上面编写的max函数模板相同。

在希望每个模板类型参数都是独立类型的情况下，最好使用这种形式，因为删除模板参数声明行会使代码更简洁和可读。

当您希望多个自动参数为同一类型时，没有一种简明的方法来使用简写函数模板。也就是说，对于这样的内容，没有简单的缩写函数模板：

```C++
template <typename T>
T max(T x, T y) // 两个参数是相同的类型
{
    return (x < y) ? y : x;
}
```

{{< alert success >}}
**最佳实践**

可以将简写的函数模板与auto参数一起使用，每个auto参数都应该是独立的类型（并且您的语言标准设置为C++20或更高版本）。

{{< /alert >}}

***
