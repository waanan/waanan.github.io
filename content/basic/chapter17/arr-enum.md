---
title: "std::array和枚举"
date: 2024-08-13T13:06:02+08:00
---

在之前，我们讨论过，可以使用枚举作为数组的长度和索引。

既然已经了解过constexpr std::array，接下来继续讨论并展示一些额外的技巧。

***
## 使用静态断言确保适当数量的数组初始值设定项

当使用CTAD初始化constexpr std::array时，编译器将根据初始值设定项的数量推断数组的长度。如果提供的初始值设定项少于应有的数量，则数组将比预期的短，并且访问它可能导致未定义的行为。

例如:

```C++
#include <array>
#include <iostream>

enum StudentNames
{
    kenny, // 0
    kyle, // 1
    stan, // 2
    butters, // 3
    cartman, // 4
    max_students // 5
};

int main()
{
    constexpr std::array testScores { 78, 94, 66, 77 }; // oops, 只有 4 个元素

    std::cout << "Cartman got a score of " << testScores[StudentNames::cartman] << '\n'; // 无效的索引，导致未定义的行为

    return 0;
}
```

如果需要检查constexpr std::array中的初始值设定项数量时，可以使用静态断言执行此操作:

```C++
#include <array>
#include <iostream>

enum StudentNames
{
    kenny, // 0
    kyle, // 1
    stan, // 2
    butters, // 3
    cartman, // 4
    max_students // 5
};

int main()
{
    constexpr std::array testScores { 78, 94, 66, 77 };

    // 确保学生都有一个分数
    static_assert(std::size(testScores) == max_students); // 编译失败: static_assert 不满足条件

    std::cout << "Cartman got a score of " << testScores[StudentNames::cartman] << '\n';

    return 0;
}
```

这样，如果稍后添加新的枚举器，但忘记向testScores添加相应的初始值设定项，则程序将无法编译。

您还可以使用静态断言来确保两个不同的constexpr std::array具有相同的长度。

***
## 使用constexpr数组实现更好的枚举输入和输出

在之前的I/O操作符重载简介中，我们介绍了输入和输出枚举器名称的几种方法。为了帮助完成这项任务，有了将枚举转换为字符串的辅助函数，反之亦然。这些函数都有自己的字符串文本集合，必须专门编码逻辑来检查每个函数:

```C++
constexpr std::string_view getPetName(Pet pet)
{
    switch (pet)
    {
    case cat:   return "cat";
    case dog:   return "dog";
    case pig:   return "pig";
    case whale: return "whale";
    default:    return "???";
    }
}

constexpr std::optional<Pet> getPetFromString(std::string_view sv)
{
    if (sv == "cat")   return cat;
    if (sv == "dog")   return dog;
    if (sv == "pig")   return pig;
    if (sv == "whale") return whale;

    return {};
}
```

这意味着如果要添加新的枚举元素，必须记住更新这些函数。

让我们稍微改进一下这些函数。在枚举器的值从0开始并按顺序继续的情况下（这对于大多数枚举都是正确的），可以使用array来保存每个枚举器的名称。

这允许我们做两件事:

```C++
#include <array>
#include <iostream>
#include <string>
#include <string_view>

namespace Color
{
    enum Type
    {
        black,
        red,
        blue,
        max_colors
    };

    // 使用 sv 后缀， 这样 std::array 中保存的元素类型为 std::string_view
    using namespace std::string_view_literals; // 引入 sv 后缀
    constexpr std::array colorName { "black"sv, "red"sv, "blue"sv };

    // 确保每个枚举值，都有对应的字符串
    static_assert(std::size(colorName) == max_colors);
};

constexpr std::string_view getColorName(Color::Type color)
{
    // 可以使用枚举元素获取到对应的字符串
    return Color::colorName[color];
}

// 设置 operator<< 如何输出 Color
// std::ostream 是 std::cout 的类型
// 返回值和参数都是引用 (避免制作额外的副本)!
std::ostream& operator<<(std::ostream& out, Color::Type color)
{
    return out << getColorName(color);
}

// 设置 operator>> 如何输入 Color
// 传递 non-const 引用，以便修改 color的值
std::istream& operator>> (std::istream& in, Color::Type& color)
{
    std::string input {};
    std::getline(in >> std::ws, input);

    // 遍历名称列表，看能否找到匹配的
    for (std::size_t index=0; index < Color::colorName.size(); ++index)
    {
        if (input == Color::colorName[index])
        {
            // 如果找到，可以根据下标，获取到对应的枚举值
            color = static_cast<Color::Type>(index);
            return in;
        }
    }

    // 如果没找到，已经是输入不对
    // 将输入 stream 设置成 fail 状态
    in.setstate(std::ios_base::failbit);

    // 提取失败, operator>> 对于基础类型，会返回0初始化的数据
    // 注释掉下面一行，对于 color 会执行同样的逻辑
    // color = {};
    return in;
}

int main()
{
    auto shirt{ Color::blue };
    std::cout << "Your shirt is " << shirt << '\n';

    std::cout << "Enter a new color: ";
    std::cin >> shirt;
    if (!std::cin)
        std::cout << "Invalid\n";
    else
        std::cout << "Your shirt is now " << shirt << '\n';

    return 0;
}
```

这将打印:

```C++
Your shirt is blue
Enter a new color: red
Your shirt is now red
```

***
## 基于范围的循环和枚举

有时，我们会遇到这样的情况，即迭代枚举元素是有用的。虽然可以使用具有整数索引的for循环来实现这一点，但这可能需要将整数索引静态强制转换为枚举类型。

```C++
#include <array>
#include <iostream>
#include <string_view>

namespace Color
{
    enum Type
    {
        black,
        red,
        blue,
        max_colors
    };

    // 使用 sv 后缀， 这样 std::array 中保存的元素类型为 std::string_view
    using namespace std::string_view_literals; // for sv suffix
    constexpr std::array colorName { "black"sv, "red"sv, "blue"sv };

    // 确保每个枚举值，都有对应的字符串
    static_assert(std::size(colorName) == max_colors);
};

constexpr std::string_view getColorName(Color::Type color)
{
    return Color::colorName[color];
}

// 设置 operator<< 如何输出 Color
// std::ostream 是 std::cout 的类型
// 返回值和参数都是引用 (避免制作额外的副本)!
std::ostream& operator<<(std::ostream& out, Color::Type color)
{
    return out << getColorName(color);
}

int main()
{
    // 使用for 循环去遍历所有的color
    for (int i=0; i < Color::max_colors; ++i )
        std::cout << static_cast<Color::Type>(i) << '\n';

    return 0;
}
```

不幸的是，基于范围的for循环不允许迭代枚举的枚举元素:

```C++
#include <array>
#include <iostream>
#include <string_view>

namespace Color
{
    enum Type
    {
        black,
        red,
        blue,
        max_colors
    };

    // 使用 sv 后缀， 这样 std::array 中保存的元素类型为 std::string_view
    using namespace std::string_view_literals; // for sv suffix
    constexpr std::array colorName { "black"sv, "red"sv, "blue"sv };

    // 确保每个枚举值，都有对应的字符串
    static_assert(std::size(colorName) == max_colors);
};

constexpr std::string_view getColorName(Color::Type color)
{
    return Color::colorName[color];
}

// 设置 operator<< 如何输出 Color
// std::ostream 是 std::cout 的类型
// 返回值和参数都是引用 (避免制作额外的副本)!
std::ostream& operator<<(std::ostream& out, Color::Type color)
{
    return out << getColorName(color);
}

int main()
{
    for (auto c: Color::Type) // 编译失败: 不能遍历枚举
        std::cout << c < '\n';

    return 0;
}
```

有许多创造性的解决方案。由于我们可以在数组上使用基于范围的for循环，因此最简单的解决方案之一是创建一个包含每个枚举元素的constexpr std::array，然后对其进行迭代。此方法仅在枚举元素具有唯一值时有效。

```C++
#include <array>
#include <iostream>
#include <string_view>

namespace Color
{
    enum Type
    {
        black,     // 0
        red,       // 1
        blue,      // 2
        max_colors // 3
    };

    using namespace std::string_view_literals; // for sv suffix
    constexpr std::array colorName { "black"sv, "red"sv, "blue"sv };
    static_assert(std::size(colorName) == max_colors);

    constexpr std::array types { black, red, blue }; // 一个 std::array 包含所有的枚举元素
    static_assert(std::size(types) == max_colors);
};

constexpr std::string_view getColorName(Color::Type color)
{
    return Color::colorName[color];
}

// 设置 operator<< 如何输出 Color
// std::ostream 是 std::cout 的类型
// 返回值和参数都是引用 (避免制作额外的副本)!
std::ostream& operator<<(std::ostream& out, Color::Type color)
{
    return out << getColorName(color);
}

int main()
{
    for (auto c: Color::types) // ok: 可以在 std::array 使用基于范围的 for 循环
        std::cout << c << '\n';

    return 0;
}
```

在上面的示例中，由于Color::types的元素类型是Color::type，因此变量c将被推导为Color::type，这正是我们想要的！

这将打印:

```C++
black
red
blue
```

***

{{< prevnext prev="/basic/chapter17/arr-ref/" next="/basic/chapter17/c-arr/" >}}
17.4 通过std::reference_wrapper创建引用的数组
<--->
17.6 C样式数组简介
{{< /prevnext >}}
