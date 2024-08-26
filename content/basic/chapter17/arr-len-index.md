---
title: "std::array长度和索引"
date: 2024-08-13T13:06:02+08:00
---

在讨论std::vector和无符号长度和下标问题中，我们了解到让标准库容器类对长度和索引使用无符号值是不幸的决定。因为std::array是标准库容器类，所以它也会遇到相同的问题。

在本课中，将回顾索引和获取std::array长度的方法。由于std::vector和std::array具有类似的接口，这些只做简单回顾。但由于只有std::array完全支持constexpr，所以将更多地关注这点。

在继续之前，请回忆下“符号转换是窄化转换，constexpr除外”。

***
## std::array的长度的类型为std::size_t

std::array实现为模板结构，其声明如下:

```C++
template<typename T, std::size_t N> // N 是非类型模版参数
struct array;
```

正如您所看到的，表示数组长度（N）的非类型模板参数的类型为std::size_t，std::size_t是一个大型无符号整数类型。

因此，当定义std::array时，长度非类型模板参数必须具有类型std::size_t，或者可以转换为类型std::size_t。由于该值必须是constexpr，因此在使用有符号整数值时不会遇到符号转换问题，因为编译器会自动在编译时将有符号整数值转换为std::size_t，而不会将其视为窄化转换。

***
## std::array的长度和索引的类型为size_type，它始终是std::size_t

就像std::vector一样，std::array定义了一个名为size_type的嵌套typedef成员，它是用于容器长度（和索引）的类型的别名。在std::array的情况下，size_type始终是std::size_t的别名。

请注意，定义std::array长度的非类型模板参数被显式定义为std::size_t，而不是size_type。这是因为size_type是std::array的成员，并且在该点没有定义。这是唯一显式使用std::size_t的地方——其他地方都使用size_type。

***
## 获取std::array的长度

有三种常用的方法来获取std::array对象的长度。

首先，我们可以使用size()成员函数（该函数将长度返回为无符号 size_type）来获取std::array对象的长度:

```C++
#include <array>
#include <iostream>

int main()
{
    constexpr std::array arr { 9.0, 7.2, 5.4, 3.6, 1.8 };
    std::cout << "length: " << arr.size() << '\n'; // 返回长度的类型为 `size_type` (`std::size_t` 的别名)
    return 0;
}
```

这将打印:

```C++
length: 5
```

与同时具有length()和size()成员函数（执行相同的操作）的std::string和std::string_view不同，std::array（以及C++中的大多数其他容器类型）仅具有size()。

其次，在C++17中，我们可以使用std::size()非成员函数（对于std::array，该函数仅调用size()成员函数，从而将长度返回为无符号size_type）。

```C++
#include <array>
#include <iostream>

int main()
{
    constexpr std::array arr{ 9, 7, 5, 3, 1 };
    std::cout << "length: " << std::size(arr); // C++17, 返回长度的类型为 `size_type` (`std::size_t` 的别名)

    return 0;
}
```

最后，在C++20中，我们可以使用std::ssize()非成员函数，该函数将长度返回为一个大的有符号整数类型（通常为std::ptrdiff_t）:

```C++
#include <array>
#include <iostream>

int main()
{
    constexpr std::array arr { 9, 7, 5, 3, 1 };
    std::cout << "length: " << std::ssize(arr); // C++20, 返回长度为一个大的有符号整数类型

    return 0;
}
```

这是三个函数中唯一一个将长度返回为有符号类型的函数。

***
## 获取std::array的长度作为constexpr值

由于std::array的长度是constexpr，因此上面的每个函数都将以constexp值的形式返回std::array的长度（即使在非constexpr std::array对象上调用）！这意味着可以在常量表达式中使用这些函数中的任何一个，并且返回的长度可以隐式转换为int，而不会进行窄化转换:

```C++
#include <array>
#include <iostream>

int main()
{
    std::array arr { 9, 7, 5, 3, 1 }; // 注: arr不是const
    constexpr int length{ std::size(arr) }; // ok: 返回值是 constexpr std::size_t，并且可以被转换为int，不会发生窄化转换

    std::cout << "length: " << length << '\n';

    return 0;
}
```

***
## 使用运算符[]或at()成员函数访问std::array

在上一课中，我们介绍了访问std::array的最常见方法是使用下标操作符（操作符[]）。在这种情况下不进行边界检查，传入无效索引将导致未定义的行为。

就像std::vector一样，std::array也有一个at()成员函数，该函数执行运行时边界检查。建议避免使用此函数，因为通常希望在访问之前进行边界检查，或者希望进行编译时边界检查。

这两个函数都要求索引的类型为size_type（std::size_t）。

如果使用constexpr值调用这两个函数中的任何一个，编译器将对std::size_t执行constexpr转换。这不被认为是窄化转换，因此您不会在这里遇到符号问题。

然而，如果使用非constexpr有符号整数值调用这两个函数中的任何一个，则将认为对std::size_t的窄化转换，编译器可能会发出警告。

***
## std::get()对constexpr索引执行编译时边界检查

由于std::array的长度是constexpr，因此如果我们的索引也是constexp值，则编译器应该能够在编译时验证constexpl索引是否在数组的边界内（如果constexpn索引超出边界，则停止编译）。

然而，操作符[]不进行边界检查，at()成员函数仅执行运行时边界检查。函数参数不能是constexpr（即使是constexpr或consteval函数），那么如何传递constexpr索引呢？

要在有constexpr索引时进行编译时边界检查，可以使用std::get()函数模板，该模板将索引作为非类型模板参数:

```C++
#include <array>
#include <iostream>

int main()
{
    constexpr std::array prime{ 2, 3, 5, 7, 11 };

    std::cout << std::get<3>(prime); // 打印索引 3 位置的元素
    std::cout << std::get<9>(prime); // 无效索引 (编译失败)

    return 0;
}
```

在std::get()的实现内部，有一个static_assert，它检查以确保非类型模板参数小于数组长度。如果不是，则static_assert将因编译错误而停止编译过程。

由于模板参数必须是constexpr，因此只能使用constexpr索引调用std::get()。

***

{{< prevnext prev="/basic/chapter17/arr-intro/" next="/basic/chapter17/arr-pass-ret/" >}}
17.0 std::array简介
<--->
17.2 std::array作为函数参数或返回值
{{< /prevnext >}}
