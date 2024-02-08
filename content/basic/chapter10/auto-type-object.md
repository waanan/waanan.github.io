---
title: "使用auto关键字的对象类型自动推导"
date: 2024-01-31T13:21:38+08:00
---

在这个简单的变量定义中隐藏着微妙的冗余：

```C++
double d{ 5.0 };
```

在C++中，我们需要为所有对象提供显式类型。因此，我们指定变量d是double类型。

然而，用于初始化d的字面值5.0也具有类型double（通过字面值的格式隐式确定）。

在我们希望变量及其初始值设定项具有相同类型的情况下，我们有效地提供了两次相同的类型信息。

***
## 初始化变量的类型推导

类型推导（Type deduction）是一种允许编译器从对象的初始值设定项推导对象类型的功能。要对变量使用类型推导，请使用auto关键字代替变量的类型：

```C++
int main()
{
    auto d{ 5.0 }; // 5.0 是 double 字面值, 所以 d 是 double 类型
    auto i{ 1 + 2 }; // 1 + 2 结果是 int, 所以 i 是 int 类型
    auto x { i }; // i 是 int, 所以 x 也是 int 类型

    return 0;
}
```

在第一种情况下，由于5.0是double字面值，编译器将推导变量d应该是double类型。在第二种情况下，表达式1+2产生一个int结果，因此变量i将为int类型。在第三种情况中，i以前被推导为int类型，因此x也将被推导为int。

由于函数调用是有效的表达式，因此当初始值设定项是非void函数调用时，我们也可以使用类型推导：

```C++
int add(int x, int y)
{
    return x + y;
}

int main()
{
    auto sum { add(5, 6) }; // add() 返回 int, 所以 sum 是 int 类型

    return 0;
}
```

add() 函数返回一个int值，因此编译器将推导变量sum的类型应该是int。

字面值后缀可以与类型推导结合使用，以指定特定类型：

```C++
int main()
{
    auto a { 1.23f }; // f 后缀导致 a 被推导为 float
    auto b { 5u };    // u 后缀导致 b 被推导为 unsigned int

    return 0;
}
```

类型推导不适用于没有初始值设定项或具有空初始值设定值的对象。当初始值设定项具有类型void（或任何其他不完整类型）时，它也将不起作用。因此，以下内容无效：

```C++
#include <iostream>

void foo()
{
}

int main()
{
    auto x;          // 编译器无法推导 x 的类型
    auto y{ };       // 编译器无法推导 y 的类型
    auto z{ foo() }; // z 不能是void类型, 所以本语句无效
    
    return 0;
}
```

尽管对基本数据类型使用类型推导只会节省几个按键，但在以后的课程中，我们将看到类型变得复杂和冗长的示例（在某些情况下，甚至可能很难理解）。在这些情况下，使用auto可以节省大量的键入。

{{< alert success >}}
**相关内容**

指针和引用的类型推导规则稍微复杂一些。我们在介绍到相关内容时讲解。

{{< /alert >}}

***
## 类型推导会删除const/constexpr限定符

在大多数情况下，类型推导将从推导的类型中删除const或constexpr限定符。例如：

```C++
int main()
{
    const int x { 5 }; // x 的类型是 const int
    auto y { x };      // y 的类型时 int (const 限定符被丢掉)

    return 0;
}
```

在上面的示例中，x具有类型const int，但当使用x作为初始值设定项来推导变量y的类型时，该类型被推导为int，而不是const int。

如果希望导出类型为const或constexpr，则必须自己提供const或constexpr。为此，只需将const或constexpr关键字与auto关键字一起使用：

```C++
int main()
{
    const int x { 5 };  // x 的类型是 const int (编译器常量)
    auto y { x };       // y 的类型是 int (const 限定符被丢掉)

    constexpr auto z { x }; // z 的类型是 constexpr int (constexpr 是需要手动指定的)

    return 0;
}
```

在这个例子中，从x推导出的类型将是int（const被删除），但因为我们在定义变量z的过程中重新添加了constexpr限定符，所以变量z将是constexpr int。

***
## 字符串字面值的类型推导

由于历史原因，C++中的字符串字面值具有奇怪的类型。因此，以下内容可能无法按预期工作：

```C++
auto s { "Hello, world" }; // s 的类型是 const char*, 而不是 std::string
```

如果希望从字符串字面值推导的类型为std:：string或std:∶string_view，则需要使用s或sv文字后缀：

```C++
#include <string>
#include <string_view>

int main()
{
    using namespace std::literals; // 方便我们使用 s 和 sv 后缀

    auto s1 { "goo"s };  // "goo"s 是 std::string 字面值, 所以 s1 的类型被推导为 std::string
    auto s2 { "moo"sv }; // "moo"sv 是 std::string_view 字面值, 所以 s2 的类型被推导为 std::string_view

    return 0;
}
```

但在这种情况下，最好不要使用类型推导。

***
## 类型推导的优点和缺点

类型推导不仅方便，而且还有许多其他好处。

首先，如果连续定义了两个或多个变量，则变量的名称将成行排列，有助于提高可读性：

```C++
// 不容易阅读
int a { 5 };
double b { 6.7 };

// 对齐，容易阅读
auto c { 5 };
auto d { 6.7 };
```

其次，类型推导仅适用于具有初始值设定项的变量，因此如果您习惯使用类型推导，它可以帮助避免无意中未初始化的变量：

```C++
int x; // oops, 忘记了初始化 x, 但编译器不会告警
auto y; // 编译器会报错，因为无法推导出变量y的类型
```

第三，您可以保证不会出现意外的影响性能的转换：

```C++
std::string_view getString();   // 返回 std::string_view 的一个函数

std::string s1 { getString() }; // bad: 从 std::string_view 转换为 std::string 可能很昂贵 (假设这不是您期望的行为)
auto s2 { getString() };        // good: 无需转换
```

类型推导也有一些缺点。

首先，类型推导在代码中掩盖了对象的类型信息。尽管一个好的IDE应该能够向您显示推导出的类型（例如，在鼠标悬停在变量上时），但在使用类型推导时，仍然容易犯关于类型的错误。

例如：

```C++
auto y { 5 }; // oops, 我们想要一个double变量，但无意中提供了一个int的字面值
```

在上面的代码中，如果我们显式地将y指定为类型double，那么即使我们意外地提供了int字面值初始设定项，y也会是double。但通过类型推导，y将被推导为int类型。

下面是另一个示例：

```C++
#include <iostream>

int main()
{
     auto x { 3 };
     auto y { 2 };

     std::cout << x / y << '\n'; // oops, 我们这里想要浮点数除法

     return 0;
}
```

在这个例子中，我们得到的是整数除法而不是浮点除法。

变量无符号时也会发生类似的情况。由于我们不想混合有符号值和无符号值，因此显式地知道变量具有无符号类型，通常不容易有混淆。

其次，如果初始值设定项的类型更改，则使用类型推导的变量的类型也将更改，这可能是意外的。考虑：

```C++
auto sum { add(5, 6) + gravity };
```

如果add的返回类型从int变为double，或者gravity从int变为了double时，sum的类型也将从int变到double。

总的来说，现代的共识是类型推导通常是安全的，并且这样做可以取消强调类型信息来使代码更具可读性，使代码的逻辑更好地突出。

***
