---
title: "非限定作用域枚举"
date: 2024-03-08T13:20:57+08:00
---

C++包含许多有用的基本数据类型和复合数据类型。但对于我们想要做的事情，这些类型并不总是足够的。

例如，在程序中，需要记录苹果是红色、黄色还是绿色，或者衬衫是什么颜色。如果只有基本类型可用，应该如何做到这一点？

或许可以使用某种隐式映射（0=红色，1=绿色，2=蓝色）将颜色存储为整数值：

```C++
int main()
{
    int appleColor{ 0 }; // 苹果是红色
    int shirtColor{ 1 }; // 衬衫是绿色

    return 0;
}
```

但这一点也不直观，并且在代码中使用魔数是有害的。可以通过使用constexpr变量来去除魔数：

```C++
constexpr int red{ 0 };
constexpr int green{ 1 };
constexpr int blue{ 2 };

int main()
{
    int appleColor{ red };
    int shirtColor{ green };

    return 0;
}
```

虽然这对于可读性更好一些，但程序员仍然需要判断appleColor和shirtColor（类型为int），是指保存在颜色符号的集合里的一个（它们可能在别处定义，在单独的文件中定义）。

通过使用类型别名，可以使该程序更清楚一些：

```C++
using Color = int; // 定义一个类型别名 Color

// 下面是Color可能的值
constexpr Color red{ 0 };
constexpr Color green{ 1 };
constexpr Color blue{ 2 };

int main()
{
    Color appleColor{ red };
    Color shirtColor{ green };

    return 0;
}
```

但阅读此代码的人仍然必须理解，这些颜色符号常量旨在与Color类型的变量一起使用，但至少该类型现在具有唯一的名称，因此搜索Color将能够找到关联的符号常量集。

然而，因为Color只是int的别名，所以我们仍然有一个问题，即没有任何东西强制正确使用这些颜色符号常量。仍然可以这样做：

```C++
Color eyeColor{ 8 }; // 语法上正确, 但在语义上无含义
```

此外，如果我们在调试器中调试这些变量，将只看到Color的整数值（例如0），而不是其意义（红色），这会使我们更难判断程序是否正确。

幸运的是，可以做得更好。

考虑一下布尔类型。bool特别有趣的是它只有两个定义的值：true和false。可以直接使用true或false（作为字面值），或者可以实例化bool对象，并让它保存这些值中的任何一个。此外，编译器能够将布尔类型与其他类型区分开来。这意味着可以重载函数，并定制这些函数在传递布尔值时的行为。

如果有能力定义自定义类型，可以定义与该类型相关联的值的集合，那么将有完美的工具来优雅地解决上面的挑战。

***
## 枚举

枚举（也称为枚举类型）是一种复合数据类型，其值限制为一组命名符号常量（）。

C++支持两种枚举：非限定作用域枚举（我们现在将讨论）和限定作用域枚举（在本章后面将讨论）。

因为枚举是程序定义的类型，所以每个枚举都需要在使用之前完全定义（前向声明是不够的）。

***
## 非限定作用域枚举

非限定作用域枚举是通过enum关键字定义的。

枚举类型最好通过示例来教授，所以让我们定义一个可以保存一些颜色值的非限定作用域枚举。将在下面解释它是如何工作的。

```C++
// 定义名为 Color 的非限定作用域枚举
enum Color
{
    // 下面是枚举的元素
    // 这些符号常量，标识了所有可能出现值的集合
    // 这些元素以逗号分隔
    red,
    green,
    blue, // 最后一个元素的结尾逗号是可选的，推荐带上
}; // 枚举定义必须以分号结尾

int main()
{
    // 定义Color类型的一些变量
    Color apple { red };   // 苹果是红色
    Color shirt { green }; // 衬衫是绿色
    Color cup { blue };    // 杯子是蓝色

    Color socks { white }; // 错误: white 不是 Color 定义的枚举元素
    Color hat { 2 };       // 错误: 2 不是 Color 定义的枚举元素

    return 0;
}
```

通过使用enum关键字来开始，告诉编译器正在定义一个非限定作用域枚举，将其命名为Color。

在一对花括号内，为颜色类型定义枚举元素：red、green和blue。它们定义了类型Color限制的特定值。每个枚举元素必须用逗号（不是分号）分隔--最后一个元素后面的尾随逗号是可选的，但建议使用以保持一致性。

最常见的做法是每行定义一个枚举元素，但在简单的情况下（枚举元素数量较少），它们都可以在一行上定义。

Color的类型定义以分号结尾。现在已经完全定义了枚举类型Color！

在main()中，实例化了三个Color类型的变量：苹果用red初始化，衬衫用green初始化，杯子用blue初始化。并为每个对象分配内存。请注意，枚举类型的初始值设定项必须是该类型的已定义枚举元素之一。变量定义socks和hat会导致编译错误，因为初始值white和2不是Color的枚举元素。

枚举元素隐式为constexpr。

{{< alert success >}}
**一个提醒**

快速概括术语：

1. 枚举或枚举类型是程序定义的类型本身（例如，Color）。
2. 枚举元素是属于枚举的特定命名值（例如，red）。

{{< /alert >}}

***
## 枚举与枚举元素的命名

按照惯例，枚举类型的名称以大写字母开头（就像所有程序定义的类型一样）。

枚举元素必须具有名称。不幸的是，枚举元素没有通用的命名约定。常见的选择包括以小写字母开头（例如red）、以大写字母开头（Red）、所有字母大写（RED），带大写前缀（COLOR_red），或前缀为“k”（kColorRed）。

现代C++指南通常建议避免使用全大写命名，因为全大写通常用于预处理器宏，并且可能会发生冲突。我们还建议避免以大写字母开头的约定，因为以大写字母开始的名称通常是为程序定义的类型保留的。

{{< alert success >}}
**警告**

枚举不必命名，但在现代C++中应该避免未命名的枚举。

{{< /alert >}}

{{< alert success >}}
**最佳实践**

以大写字母开头命名枚举类型。以小写字母开头命名枚举元素。

{{< /alert >}}

***
## 不同枚举是不同的类型

创建的每个枚举类型都被认为是不同的类型，这意味着编译器可以将其与其他类型区分开来（不同于typedef或类型别名，它们被认为与它们所别名的类型相同）。

因此一个枚举类型中定义的元素，不能与另外的枚举类型混用：

```C++
enum Pet
{
    cat,
    dog,
    pig,
    whale,
};

enum Color
{
    black,
    red,
    blue,
};

int main()
{
    Pet myPet { black }; // 编译失败: black 不是 Pet 的元素
    Color shirt { pig }; // 编译失败: pig 不是 Color 的元素

    return 0;
}
```

无论如何，你可能不想要一件猪衬衫。

***
## 使用枚举

由于枚举元素是描述性的，因此它们对于增强代码可读性非常有用。当有一组很小的相关常量时，最好使用枚举类型。

通常定义的枚举包括一周中的几天、基本方向和一副卡片中的套装：

```C++
enum DaysOfWeek
{
    sunday,
    monday,
    tuesday,
    wednesday,
    thursday,
    friday,
    saturday,
};

enum CardinalDirections
{
    north,
    east,
    south,
    west,
};

enum CardSuits
{
    clubs,
    diamonds,
    hearts,
    spades,
};
```

有时，函数将向调用方返回状态代码，以指示函数是成功执行还是遇到错误。传统上，小负数用于表示不同的可能错误代码。例如：

```C++
int readFileContents()
{
    if (!openFile())
        return -1;
    if (!readFile())
        return -2;
    if (!parseFile())
        return -3;

    return 0; // success
}
```

然而，像这样使用魔数并不是很有描述性的。更好的方法是使用枚举类型：

```C++
enum FileReadResult
{
    readResultSuccess,
    readResultErrorFileOpen,
    readResultErrorFileRead,
    readResultErrorFileParse,
};

FileReadResult readFileContents()
{
    if (!openFile())
        return readResultErrorFileOpen;
    if (!readFile())
        return readResultErrorFileRead;
    if (!parseFile())
        return readResultErrorFileParse;

    return readResultSuccess;
}
```

然后调用方可以测试返回值是哪个枚举元素，这比测试特定整数值的返回结果更容易理解。

```C++
if (readFileContents() == readResultSuccess)
{
    // do something
}
else
{
    // print error message
}
```

枚举类型也可以在游戏编程中很好地使用，以识别不同类型的物品、怪物或地形。基本上，任何东西都是一组相关的元素。

例如：

```C++
enum ItemType
{
	sword,
	torch,
	potion,
};

int main()
{
	ItemType holding{ torch };

	return 0;
}
```

当用户需要在两个或多个选项之间进行选择时，枚举类型也可以成为有用的函数参数：

```C++
enum SortOrder
{
    alphabetical,
    alphabeticalReverse,
    numerical,
};

void sortData(SortOrder order)
{
    switch (order)
    {
        case alphabetical:
            // 使用正向的字母表排序
            break;
        case alphabeticalReverse:
            // 使用反向的字母表排序
            break;
        case numerical:
            // 使用数字顺序排序
            break;
    }
}
```

许多语言使用枚举来定义布尔值——毕竟，布尔值本质上只是具有两个枚举元素的枚举类型：false和true！然而，在C++中，true和false被定义为关键字，而不是枚举器。

由于枚举很小，并且复制成本很低，因此可以通过值传递（并返回）它们。

***
## 非范围枚举的范围

无范围枚举之所以如此命名，是因为它们将其枚举器名称放入与枚举定义本身相同的范围中（而不是像命名空间那样创建新的范围区域）。

例如，给定此程序：

```C++
enum Color // this enum is defined in the global namespace
{
    red, // so red is put into the global namespace
    green,
    blue, 
};

int main()
{
    Color apple { red }; // my apple is red

    return 0;
}
```

颜色枚举在全局范围中定义。因此，所有枚举名称（红色、绿色和蓝色）也都进入全局范围。这会污染全局范围，并显著增加命名冲突的可能性。

这样做的一个后果是不能在同一范围内的多个枚举中使用枚举器名称：

```C++
enum Color
{
    red,
    green,
    blue, // blue is put into the global namespace
};

enum Feeling
{
    happy,
    tired,
    blue, // error: naming collision with the above blue
};

int main()
{
    Color apple { red }; // my apple is red
    Feeling me { happy }; // I'm happy right now (even though my program doesn't compile)

    return 0;
}
```

在上面的示例中，两个非范围枚举（颜色和感觉）都将具有相同名称的枚举器蓝色放入全局范围。这会导致命名冲突和随后的编译错误。

无范围枚举还为其枚举器提供命名范围区域（就像命名空间充当中声明的名称的命名范围区域一样）。这意味着我们可以按如下方式访问未范围枚举的枚举器：

```C++
enum Color
{
    red,
    green,
    blue, // blue is put into the global namespace
};

int main()
{
    Color apple { red }; // okay, accessing enumerator from global namespace
    Color raspberry { Color::red }; // also okay, accessing enumerator from scope of Color

    return 0;
}
```

通常，在不使用范围解析操作符的情况下访问未范围枚举器。

***
## 避免枚举器命名冲突

有许多常见的方法可以防止未范围枚举器命名冲突。

一个选项是用枚举本身的名称作为每个枚举器的前缀：

```C++
enum Color
{
    color_red,
    color_blue,
    color_green,
};

enum Feeling
{
    feeling_happy,
    feeling_tired,
    feeling_blue, // no longer has a naming collision with color_blue
};

int main()
{
    Color paint { color_blue };
    Feeling me { feeling_blue };

    return 0;
}
```

这仍然会污染名称空间，但通过使名称更长、更唯一，减少了命名冲突的机会。

更好的选择是将枚举类型放在提供单独作用域区域的内容中，例如命名空间：

```C++
namespace Color
{
    // The names Color, red, blue, and green are defined inside namespace Color
    enum Color
    {
        red,
        green,
        blue,
    };
}

namespace Feeling
{
    enum Feeling
    {
        happy,
        tired,
        blue, // Feeling::blue doesn't collide with Color::blue
    };
}

int main()
{
    Color::Color paint{ Color::blue };
    Feeling::Feeling me{ Feeling::blue };

    return 0;
}
```

这意味着我们现在必须用作用域区域的名称作为枚举和枚举器名称的前缀。

一个相关的选项是使用作用域枚举（它定义自己的作用域区域）。我们将很快讨论范围枚举（13.4——范围枚举（枚举类））。

或者，如果枚举仅在单个函数体中使用，则应在函数内部定义枚举。这将枚举及其枚举器的范围限制为仅限于该函数。这种枚举的枚举器将隐藏全局范围中定义的同名枚举器。

{{< alert success >}}
**对于高级读者**

类还提供范围区域，通常将与类相关的枚举类型放在类的范围区域内。我们在第15.3课——嵌套类型（成员类型）中讨论了这一点。

{{< /alert >}}

{{< alert success >}}
**最佳做法**

更喜欢将枚举放在命名范围区域（如命名空间或类）内，以便枚举器不会污染全局命名空间。

{{< /alert >}}

***
## 与普查员进行比较

我们可以使用相等运算符（operator==和operator！=）来测试枚举是否具有特定枚举器的值。

```C++
#include <iostream>

enum Color
{
    red,
    green,
    blue,
};

int main()
{
    Color shirt{ blue };

    if (shirt == blue) // if the shirt is blue
        std::cout << "Your shirt is blue!";
    else
        std::cout << "Your shirt is not blue!";

    return 0;
}
```

在上面的示例中，我们使用if语句来测试shirt是否等于枚举器blue。这为我们提供了一种基于枚举所持有的枚举器来限制程序行为的方法。

在下一课中，我们将更多地利用这一点。

***
