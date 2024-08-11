---
title: "使用枚举值来作为数组索引"
date: 2024-07-08T11:10:28+08:00
---

数组的一个可读性问题是整数索引不向程序员提供关于索引含义的任何信息。

考虑一个包含5个测试分数的数组：

```C++
#include <vector>

int main()
{
    std::vector testScores { 78, 94, 66, 77, 14 };

    testScores[2] = 76; // 这是什么含义?
}
```

testScores\[2\]代表的学生是谁？

***
## 使用非限定作用域枚举器进行索引

我们花了大量时间讨论了std::vector\<T\>::operator[]（以及其他可以使用下标的C++容器类）的索引具有类型size_type，这通常是std::size_t的别名。因此，我们的索引要么需要是类型std::size_t，或者可以转换过去。

由于非限定作用域枚举将隐式转换为std::size_t，这意味着可以使用它作为数组索引来帮助记录索引的含义：

```C++
#include <vector>

namespace Students
{
    enum Names
    {
        kenny, // 0
        kyle, // 1
        stan, // 2
        butters, // 3
        cartman, // 4
        max_students // 5
    };
}

int main()
{
    std::vector testScores { 78, 94, 66, 77, 14 };

    testScores[Students::stan] = 76; // 现在更新的是 stan 的分数

    return 0;
}
```

这样，每个数组元素表示的内容就清楚得多。

由于枚举元素是隐式constexpr，因此将枚举数转换为无符号整数类型不被视为窄化转换，从而避免了有符号/无符号索引问题。

***
## 使用非constexpr非限定作用域枚举进行索引

非限定作用域枚举的基础类型是实现定义的（因此，可以是有符号或无符号整数类型）。由于枚举元素是隐式constexpr，因此只要坚持使用非限定作用域枚举进行索引，就不会遇到符号转换问题。

然而，如果定义枚举类型的非constexpr变量，然后尝试使用该变量索引std::vector，则在任何将非限定作用域枚举元素视为有符号数的平台上，都可能会收到符号转换警告：

```C++
#include <vector>

namespace Students
{
    enum Names
    {
        kenny, // 0
        kyle, // 1
        stan, // 2
        butters, // 3
        cartman, // 4
        max_students // 5
    };
}

int main()
{
    std::vector testScores { 78, 94, 66, 77, 14 };
    Students::Names name { Students::stan }; // non-constexpr

    testScores[name] = 76; // 可能收到符号转换告警，因为 Student::Names 可能默认底层是有符号类型

    return 0;
}
```

在这种特殊情况下，可以将name声明为constexpr（以便从constexpr 有符号整型到std::size_t的转换是非窄化的）。然而，当初始值设定项不是常量表达式时，这将不起作用。

另一个选项是显式将枚举的基础类型指定为无符号整数：

```C++
#include <vector>

namespace Students
{
    enum Names : unsigned int // 显示声明底层类型是 unsigned int
    {
        kenny, // 0
        kyle, // 1
        stan, // 2
        butters, // 3
        cartman, // 4
        max_students // 5
    };
}

int main()
{
    std::vector testScores { 78, 94, 66, 77, 14 };
    Students::Names name { Students::stan }; // non-constexpr

    testScores[name] = 76; // name 是 unsigned，因此没有类型转换

    return 0;
}
```

在上面的示例中，由于name现在保证为无符号int，因此可以将其转换为std::size_t，而不会出现符号转换问题。

***
## 使用计数枚举元素

注意，我们在枚举器列表的末尾定义了一个名为max_students的额外枚举元素。如果所有先前的枚举元素都使用默认值（推荐），则此枚举元素将具有与前面枚举器的计数匹配的默认值。在上面的示例中，max_students的值为5，因为前面定义了5个枚举元素。非正式地，我们将其称为计数枚举器，因为它的值表示先前定义的枚举器的计数。

然后，该计数枚举器可以用于任何需要对先前枚举器进行计数的地方。例如：

```C++
#include <iostream>
#include <vector>

namespace Students
{
    enum Names
    {
        kenny, // 0
        kyle, // 1
        stan, // 2
        butters, // 3
        cartman, // 4
        max_students // 5
    };
}

int main()
{
    std::vector<int> testScores(Students::max_students); // 创建有 5 个元素的数组

    testScores[Students::stan] = 76; // 更新 stan 的分数

    std::cout << "The class has " << Students::max_students << " students\n";

    return 0;
}
```

在两个地方使用max_students：首先，创建一个长度为max_stuvents的std::vector，因此每个学生都有一个元素。还使用max_students打印学生人数。

这种技术也很好，因为如果稍后添加另一个枚举元素（就在max_students之前），那么max_stuvents将自动变大一个，并且所有使用max_stuments的数组都将更新为使用新长度，而不需要进一步修改。

```C++
#include <vector>
#include <iostream>

namespace Students
{
    enum Names
    {
        kenny, // 0
        kyle, // 1
        stan, // 2
        butters, // 3
        cartman, // 4
        wendy, // 5 (新增)
        // 这里可以添加后续的枚举
        max_students // now 6
    };
}

int main()
{
    std::vector<int> testScores(Students::max_students); // 现在分配6个元素

    testScores[Students::stan] = 76; // 仍然有效

    std::cout << "The class has " << Students::max_students << " students\n";

    return 0;
}
```

***
## 使用计数枚举元素断言数组长度

更常见的是，使用初始化列表创建数组。在这种情况下，断言容器的大小等于计数枚举元素是有用的。如果这个断言触发，那么枚举元素或初始化列表在某种程度上是不正确的。当新的枚举元素添加到枚举中，但新的初始化值没有添加到数组中时，很容易发生这种情况。

例如：

```C++
#include <cassert>
#include <iostream>
#include <vector>

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
    std::vector testScores { 78, 94, 66, 77, 14 };

    // 确保分数和学生个数可以对应
    assert(std::size(testScores) == max_students);

    return 0;
}
```

{{< alert success >}}
**提示**

如果数组是constexpr，则应该改为static_assert。std::vector不支持constexpr，但std:∶array（和C样式数组）支持。

{{< /alert >}}

***
## 数组和枚举类

由于非限定作用域枚举会污染命名空间，因此最好使用枚举类。

然而，由于枚举类没有到整数类型的隐式转换，因此在尝试将其枚举元素用作数组索引时，会遇到了一个问题：

```C++
#include <iostream>
#include <vector>

enum class StudentNames // 现在是枚举类
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
    // 编译失败: StudentNames 无法转换为 std::size_t
    std::vector<int> testScores(StudentNames::max_students);

    // 编译失败: StudentNames 无法转换为 std::size_t
    testScores[StudentNames::stan] = 76;

    // 编译失败: StudentNames 无法转换为任何 operator<< 能输出的类型
    std::cout << "The class has " << StudentNames::max_students << " students\n";

    return 0;
}
```

有两种方法可以解决这个问题。最明显的是，可以将枚举元素static_cast为整数：

```C++
#include <iostream>
#include <vector>

enum class StudentNames
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
    std::vector<int> testScores(static_cast<int>(StudentNames::max_students));

    testScores[static_cast<int>(StudentNames::stan)] = 76;

    std::cout << "The class has " << static_cast<int>(StudentNames::max_students) << " students\n";

    return 0;
}
```

然而，这不仅是一个痛苦的方式，也显著弄乱了代码。

更好的选择是使用之前介绍的一个助手函数，它允许我们使用一元运算符+将枚举类的枚举元素转换为整数值。

```C++
#include <iostream>
#include <type_traits> // for std::underlying_type_t
#include <vector>

enum class StudentNames
{
    kenny, // 0
    kyle, // 1
    stan, // 2
    butters, // 3
    cartman, // 4
    max_students // 5
};

// 重载 一元 + 运算符 将 StudentNames 转换为 底层类型
constexpr auto operator+(StudentNames a) noexcept
{
    return static_cast<std::underlying_type_t<StudentNames>>(a);
}

int main()
{
    std::vector<int> testScores(+StudentNames::max_students);

    testScores[+StudentNames::stan] = 76;

    std::cout << "The class has " << +StudentNames::max_students << " students\n";

    return 0;
}
```

然而，如果您要进行大量枚举元素到整数的转换，那么最好只在名称空间（或类）中使用标准枚举。

***
