---
title: "Constexpr和consteval函数"
date: 2023-11-28T13:19:42+08:00
---

在前面章节中，我们引入了constexpr关键字，用于创建编译时（符号）常量。我们还引入了常量表达式，这些表达式可以在编译时计算，而不是在运行时计算。

考虑使用两个constexpr变量的以下程序：

```C++
#include <iostream>

int main()
{
    constexpr int x{ 5 };
    constexpr int y{ 6 };

    std::cout << (x > y ? x : y) << " is greater!\n";

    return 0;
}
```

这将产生以下结果：

```C++
6 is greater!
```

由于x和y是constexpr，编译器可以在编译时计算常量表达式 (x > y ? x : y)，得到结果 6。因为这个表达式不再需要在运行时求值，所以我们的程序将运行得更快。

然而，在print语句的中间有一个非平凡的表达式并不理想——如果表达式是命名函数，会更好。下面是使用函数的相同示例：

```C++
#include <iostream>

int greater(int x, int y)
{
    return (x > y ? x : y); // 比较操作在这里
}

int main()
{
    constexpr int x{ 5 };
    constexpr int y{ 6 };

    std::cout << greater(x, y) << " is greater!\n"; // 运行时才会计算

    return 0;
}
```

该程序产生与前一程序相同的输出。但将表达式放在函数中有一个缺点：对 greater(x, y) 的调用将在运行时执行。通过使用函数（这有利于模块化和文档），我们已经失去了在编译时运行代码的能力（这对性能有害）。

那么我们该如何解决这个问题呢？

***
## Constexpr函数可以在编译时计算

constexpr函数，其返回值可以在编译时计算。要使函数成为constexpr函数，只需在返回类型之前使用constexpr关键字。下面是一个与上面类似的程序，使用constexpr函数：

```C++
#include <iostream>

constexpr int greater(int x, int y) // 是一个 constexpr 函数
{
    return (x > y ? x : y);
}

int main()
{
    constexpr int x{ 5 };
    constexpr int y{ 6 };

    // 稍后解释这里为啥使用变量
    constexpr int g { greater(x, y) }; // 编译时计算

    std::cout << g << " is greater!\n";

    return 0;
}
```

这将产生与前一示例相同的输出，但函数调用 greater(x, y) 将在编译时计算，而不是在运行时计算！

当编译到对应的函数调用时，编译器将计算函数调用的返回值，然后用返回值替换函数调用。

因此在我们的示例中，对 greater(x, y) 的调用将被函数调用的结果替换，即整数值6。换句话说，编译器将编译以下内容：

```C++
#include <iostream>

int main()
{
    constexpr int x{ 5 };
    constexpr int y{ 6 };

    constexpr int g { 6 }; // greater(x, y) 被计算并被返回值 6 取代

    std::cout << g << " is greater!\n";

    return 0;
}
```

为了有资格进行编译时计算，函数必须具有constexpr返回类型，并且在编译时计算时不能调用任何非constexpr函数。此外，对函数的调用必须传递constexpr参数（例如，constexpr变量或文本）。

上面示例中的greater() 函数定义和函数调用满足这些要求，因此它可以进行编译时求值。

{{< alert success >}}
**注**

在本文后面的部分中，我们将使用术语“有资格进行编译时求值”，因此请记住这个定义。

{{< /alert >}}

***
## Constexpr函数也可以在运行时求值

具有constexpr返回值的函数也可以在运行时求值，在这种情况下，它们将返回非 constexpr结果。例如：

```C++
#include <iostream>

constexpr int greater(int x, int y)
{
    return (x > y ? x : y);
}

int main()
{
    int x{ 5 }; // not constexpr
    int y{ 6 }; // not constexpr

    std::cout << greater(x, y) << " is greater!\n"; // 运行时才会计算

    return 0;
}
```

在本例中，由于参数x和y不是constexpr，因此无法在编译时调用函数。该函数仍将在运行时调用方，并将返回值作为非constexpr int返回。

{{< alert success >}}
**关键点**

允许在编译时或运行时计算具有constexpr返回类型的函数，以便单个函数可以同时满足这两种情况。

否则，您需要有单独的函数（具有constexpr返回类型的函数和具有constexpr返回类型的功能）。这不仅需要重复的代码，这两个函数还需要具有不同的名称！

这也是C++不允许constexpr函数参数的原因。constexpr函数参数将意味着只能使用constexper参数调用函数。但情况并非如此——在运行时对函数求值时，可以使用非constexpr参数调用constexpr函数。

{{< /alert >}}

***
## 那么，constexpr函数何时在编译时求值？

您可能认为constexpr函数将尽可能在编译时求值，但不幸的是，情况并非如此。

根据C++标准，在需要常量表达式的地方使用返回值，则有资格进行编译时计算的constexpr函数必须在编译时计算。否则，编译器可以在编译时或运行时自由计算函数。

让我们研究几个案例来进一步探讨这一点：

```C++
#include <iostream>

constexpr int greater(int x, int y)
{
    return (x > y ? x : y);
}

int main()
{
    constexpr int g { greater(5, 6) };            // case 1: 编译时求值
    std::cout << g << " is greater!\n";

    int x{ 5 }; // not constexpr
    std::cout << greater(x, 6) << " is greater!\n"; // case 2: 运行时求值

    std::cout << greater(5, 6) << " is greater!\n"; // case 3: 可能在编译时求值，可能在运行时求值

    return 0;
}
```

在情况1中，我们使用constexpr参数调用greater()，因此它有资格在编译时求值。constexpr变量g的初始值设定项必须是常量表达式，因此在需要常量表达式的上下文中使用返回值。因此，必须在编译时计算greater() 。

在案例2中，我们使用一个非constexpr参数调用greater() 。因此，不能在编译时计算greater() ，必须在运行时计算。

案例3是一个有趣的案例。再次使用constexpr参数调用greater() 函数，因此它可以进行编译时计算。然而，返回值没有在需要常量表达式的上下文中使用（运算符 << 总是在运行时执行），因此编译器可以自由选择是在编译时还是在运行时计算对greater() 的调用！

请注意，编译器的优化级别设置可能会影响它决定在编译时还是在运行时计算函数。这也意味着您的编译器可能会为调试版本和发布版本做出不同的选择（因为调试版本通常关闭了优化）。

{{< alert success >}}
**关键点**

如果在需要常量表达式的地方使用返回值，则有资格在编译时计算的constexpr函数将仅在编译时求值。否则，不能保证编译时计算。

因此，constexpr函数最好被认为是“可以在常量表达式中使用”，而不是“将在编译时求值”。

{{< /alert >}}

{{< alert success >}}
**最佳实践**

除非您有特定的理由不这样做，否则通常应将可以成为constexpr的函数设置为constexpr。

{{< /alert >}}

***
## 确定constexpr函数调用是在编译时还是在运行时求值

在C++20之前，没有可用于执行此操作的标准语言工具。

在C++20中，std::is_constant_evaluated() （在<type_traits>标头中定义）返回一个布尔值，指示当前函数调用是否在常量上下文中执行。这可以与条件语句相结合，以允许函数在编译时与运行时求值时的行为不同。

```C++
#include <type_traits> // for std::is_constant_evaluated

constexpr int someFunction()
{
    if (std::is_constant_evaluated()) // 如果在编译时求值
        // do something
    else // 如果在运行时求值
        // do something else  
}
```

巧妙地使用，可以让函数在编译时求值时产生一些可观察的差异（例如返回特殊值），然后根据该结果推断它是如何求值的。

***
## 强制在编译时计算constexpr函数

无法告诉编译器，constexpr函数应该尽可能在编译时求值（在非常量表达式中使用返回值的情况下）。

然而，通过确保在需要常量表达式的地方使用返回值，我们可以强制有资格在编译时计算的constexpr函数在编译时实际计算。

最常见的方法是使用返回值来初始化constexpr变量（这就是我们在前面的示例中使用变量“g”的原因）。不幸的是，这需要在我们的程序中引入一个新变量，以确保编译时求值，这是丑陋的，并降低了代码的可读性。

然而，在C++20中，有一个更好的解决方法来解决这个问题，我们稍后将介绍。

***
## Consteval C++20标准

C++20引入了关键字consteval，用于指示函数必须在编译时求值，否则将导致编译错误。这种函数称为即时函数（immediate functions）。

```C++
#include <iostream>

consteval int greater(int x, int y) // function 现在是 consteval
{
    return (x > y ? x : y);
}

int main()
{
    constexpr int g { greater(5, 6) };              // ok: 在编译时求值
    std::cout << g << '\n';

    std::cout << greater(5, 6) << " is greater!\n"; // ok: 在编译时求值

    int x{ 5 }; // not constexpr
    std::cout << greater(x, 6) << " is greater!\n"; // error: consteval 函数必须在编译时求值

    return 0;
}
```

在上面的示例中，对greater() 的前两个调用将在编译时计算。无法在编译时计算对 greater(x, 6) 的调用，因此将导致编译错误。

{{< alert success >}}
**最佳实践**

如果由于某种原因（例如性能），函数必须在编译时运行，请使用consteval。

{{< /alert >}}

***
## C++20使用consteval使constexpr在编译时执行

consteval函数的缺点是这样的函数不能在运行时求值，这使得它们不如constexpr函数灵活。因此，有一种方便的方法来强制constexpr函数在编译时求值（即使在不需要常量表达式的情况下使用返回值），这样我们就可以在可能的情况下进行编译时计算，在不能进行运行时计算时，也可以进行运行时求值。

consteval函数提供了一种实现这种情况的方法，通过使用一个助手函数：

```C++
#include <iostream>

// 使用函数模板 (C++20) 和 `auto` 返回类型，让这个函数可以在任何类型上使用
// 你不需要知道这个函数为什么可以工作
consteval auto compileTime(auto value)
{
    return value;
}

constexpr int greater(int x, int y) // function is constexpr
{
    return (x > y ? x : y);
}

int main()
{
    std::cout << greater(5, 6) << '\n';              // 可能在编译时求值
    std::cout << compileTime(greater(5, 6)) << '\n'; // 在编译时求值

    int x { 5 };
    std::cout << greater(x, 6) << '\n';              // greater函数仍可在运行时求值

    return 0;
}
```

这满足了我们的需求，因为consteval函数需要常量表达式作为参数——因此，如果我们使用constexpr函数的返回值作为consteval函数的参数，则必须在编译时对constexper函数求值！consteval函数只是将该参数作为其自己的返回值返回，因此调用方仍然可以使用它。

注意，consteval函数按值返回。虽然在运行时这样做可能效率低下（如果值是复制成本很高的类型，例如std::string），但在编译时，这并不重要，因为对consteval函数的整个调用将简单地替换为计算的返回值。

{{< alert success >}}
**相关内容**

我们在——函数的类型推导中介绍自动返回类型。我们在——具有多个模板类型的函数模板中介绍了缩写函数模板（auto参数）。

{{< /alert >}}

***
## Constexpr/consteval函数隐式内联

因为constexpr函数可以在编译时求值，所以编译器必须能够在调用该函数的所有点上看到constexpl函数的完整定义。前向声明是不够的，即使实际的函数定义稍后出现在同一编译单元中。

这意味着在多个文件中调用的constexpr函数需要将其定义包含在对应的文件中——这通常会违反单定义规则。为了避免这样的问题，constexpr函数是隐式内联的，这使得它们不受单定义规则的约束。

因此，constexpr函数通常在头文件中定义，因此它们可以被 #include 在任何需要完整定义的.cpp文件中。

出于相同的原因，consteval函数也隐式内联。

{{< alert success >}}
**规则**

编译器必须能够看到constexpr或consteval函数的完整定义，而不仅仅是前向声明。

{{< /alert >}}

{{< alert success >}}
**最佳实践**

在单个源文件（.cpp）中使用的constexpr/consteval函数，需要在使用它们之前的地方定义。

在多个源文件中使用的constexpr/consteval函数，需要将它们定义在头文件，以便将它们包含在每个源文件中。

{{< /alert >}}

***
## constexpr/consteval函数参数不是constexpr，但可以用作其他constexpr函数的参数

constexpr函数的参数不是constexpr（因此不能在常量表达式中使用）。这样的参数可以声明为const（在这种情况下，它们被视为运行时常量），但不能声明为constexpr。这是因为constexpr函数可以在运行时求值（如果参数是编译时常量，则这是不可能的）。

然而，在一种情况下会发生异常：constexpr函数可以将这些参数作为参数传递给另一个constexper函数，并且可以在编译时解析后续的constexpr。这允许在编译时调用其他constexpr函数（递归地包括它们自己）时仍然解析constexper函数。

也许令人惊讶的是，consteval函数的参数也不被认为是函数中的constexpr（即使consteval.函数只能在编译时求值）。这一决定是为了一致性而作出的。

{{< alert success >}}
**相关内容**

如果在函数中需要constexpr参数（例如，在需要常量表达式的地方使用），请参见10.18——非类型模板参数。

{{< /alert >}}

***
## constexpr函数可以调用非常量表达式函数吗？

答案是肯定的，但仅当constexpr函数在非常量上下文中求值时。当constexpr函数在常量上下文中求值时，不能调用非常量表达式函数（因为这样，constexpl函数将无法生成编译时常量值）。

允许调用非常量表达式函数，以便constexpr函数可以执行以下操作：

```C++
#include <type_traits> // for std::is_constant_evaluated

constexpr int someFunction()
{
    if (std::is_constant_evaluated()) // if compile-time evaluation
        return someConstexprFcn();    // calculate some value at compile time
    else                              // runtime evaluation
        return someNonConstexprFcn(); // calculate some value at runtime
}
```

现在考虑这个变体：

```C++
constexpr int someFunction(bool b)
{
    if (b)
        return someConstexprFcn();
    else
        return someNonConstexprFcn();
}
```

只要从未在常量表达式中调用someFunction（false），这就是合法的。

C++标准规定，constexpr函数必须为至少一组参数返回constexper值，否则它在技术上是格式错误的。因此，在constexpr函数中无条件调用非常量表达式函数会导致constexper函数格式错误。然而，编译器不需要为这种情况生成错误或警告——因此，编译器可能不会抱怨，除非您尝试在常量上下文中调用这样的constexpr函数。

因此，我们建议：

