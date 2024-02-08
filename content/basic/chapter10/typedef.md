---
title: "typedef和类型别名"
date: 2024-01-31T13:21:38+08:00
---

## 类型别名

在C++中，using关键字是为现有数据类型创建别名的关键字。要创建这样的类型别名，我们使用using关键字，后跟类型别名的名称，然后是等号和现有数据类型。例如:

```C++
using Distance = double; // 将 Distance 定义为 double 的别名
```

一旦定义，类型别名就可以在需要类型的任何地方使用。例如，我们可以创建以类型别名为类型的变量:

```C++
Distance milesToDestination{ 3.4 }; // 定义一个 double 类型的变量
```

当编译器遇到类型别名时，它将类型别名替换为对应的类型。例如:

```C++
#include <iostream>

int main()
{
    using Distance = double; // 将 Distance 定义为 double 的别名

    Distance milesToDestination{ 3.4 }; // 定义一个 double 类型的变量

    std::cout << milesToDestination << '\n'; // 打印一个double值

    return 0;
}
```

这将打印:

```C++
3.4
```

在上面的程序中，我们首先将Distance定义为类型double的别名。

接下来，我们定义一个名为milesToDestination的变量，其类型为 Distance。因为编译器知道Distance是类型别名，所以它将使用别名类型，即double。因此，变量milesToDestination实际上被编译为double类型的变量，并且它在所有方面都将作为double。

最后，我们打印milesToDestination的值，它打印为double。

{{< alert success >}}
**对于高级读者**

类型别名也可以模板化。我们在后续介绍模版时介绍。

{{< /alert >}}

***
## 命名类型别名规则

从历史上看，类型别名的命名方式没有太多的一致性。有三种常见的命名约定:

1. 键入以“_t”后缀结尾的别名（“_t“是“Type”的缩写）。标准库通常将此约定用于全局范围的类型名称（如size_t和nullptr_t）。


该约定继承自C，过去在定义自己的类型别名（有时还包括其他类型）时最流行，但在现代C++中已不受欢迎。请注意，POSIX为全局范围的类型名称保留了“_t”后缀，因此使用此约定可能会导致POSIX系统上的类型命名冲突。

2. 键入以“_type”后缀结尾的别名。某些标准库类型（如std::string）使用此约定来命名嵌套类型别名（例如，std::string::size_type）。


但许多这样的嵌套类型别名根本不使用后缀（例如，std::string::iterator），因此这种用法是不一致的。

3. 键入不使用后缀的别名。


在现代C++中的约定是,命名您自己定义的类型别名（或任何其他类型），以大写字母开头，不使用后缀。大写字母有助于区分类型的名称与变量和函数的名称（以小写字母开头），并防止它们之间的命名冲突。

使用此命名约定时，通常会看到这种用法:

```C++
void printDistance(Distance distance); // Distance 是定义的类型
```

在这种情况下，Distance是类型，distance是参数名。C++是区分大小写的，所以这很好的工作。

{{< alert success >}}
**最佳实践**

以大写字母开头命名类型别名，不要使用后缀（除非您有特定的原因要这样做）。

{{< /alert >}}

***
## 类型别名不是不同的类型

别名实际上并不定义新的、不同的类型 —— 它只是为现有类型引入一个新的标识符。类型别名与对应的类型完全可互换。

这允许我们做语法上有效但语义上无意义的事情。例如:

```C++
int main()
{
    using Miles = long; // 定义 Miles 作为类型 long 的别名
    using Speed = long; // 定义 Speed 作为类型 long 的别名

    Miles distance { 5 }; // distance 定义为 long
    Speed mhz  { 3200 };  // mhz 定义为 long

    // 下面的赋值语法上有效 (但通常有语义问题)
    distance = mhz;

    return 0;
}
```

尽管在概念上，我们希望Miles和Speed具有不同的含义，但两者都只是long类型的别名。这实际上意味着Miles、Speed和long都可以互换使用。事实上，当我们将Speed类型的值赋给Miles类型的变量时，编译器只会看到我们将long类型的值赋值给long类型变量，它不会告警。

因为编译器不能防止类型别名出现这种语义错误，所以我们说别名不是类型安全的。尽管如此，它们仍然有用。

{{< alert success >}}
**警告**

必须注意不要混合使用在语义上不同的类型别名的值。

{{< /alert >}}

{{< alert success >}}
**旁白**

一些语言支持强类型定义（或强类型别名）的概念。强类型定义实际上创建了一个新类型，该类型具有原始类型的所有原始属性，但如果试图混合原始类型和强别名类型定义的值，编译器将抛出错误。从C++20开始，C++不直接支持强类型定义，但有相当多的第三方C++库实现了类似于强类型定义的行为。

{{< /alert >}}

***
## 类型别名的作用域

由于作用域是标识符的属性，因此类型别名标识符遵循与变量标识符相同的作用域规则:在块内定义的类型别名具有块作用域，并且仅在该块内可用，而在全局命名空间中定义的类型别名具有全局作用域，并且可用到文件末尾。在上面的示例中，Miles和Speed仅在main()函数中可用。

如果需要在多个文件中使用一个或多个类型别名，可以在头文件中定义它们，并将这个头文件include到需要使用定义的任何代码文件中:

mytypes.h:

```C++
#ifndef MYTYPES_H
#define MYTYPES_H

    using Miles = long;
    using Speed = long;

#endif
```

以这种方式引入的类型别名将导入全局命名空间，因此具有全局作用域。

***
## 类型定义

typedef（“类型定义”的缩写）是为类型创建别名的较旧方法。要创建typedef别名，使用typedef关键字:

```C++
// 下面创建类型别名的效果是一致的
typedef long Miles;
using Miles = long;
```

由于向后兼容性的原因，Typedef仍然存在C++中，但在现代C++中，它们在很大程度上已被类型别名所取代。

Typedef有几个语法问题。首先，很容易忘记是typedef的名称还是要别名的类型的名称哪个在前面。下面哪个是正确的？

```C++
typedef Distance double; // 错误 (原始名称在前)
typedef double Distance; // 正确 (原始名称在前)
```

幸运的是，在这种情况下写错，编译器会报错。

其次，typedef的语法可能会因更复杂的类型而变得难看。例如，下面是一个难以阅读的typedef，以及一个等效的（并且稍微容易阅读）类型别名:

```C++
typedef int (*FcnType)(double, char); // FcnType 很难理解
using FcnType = int(*)(double, char); // FcnType 少容易阅读
```

在上面的typedef定义中，新类型的名称（FcnType）隐藏在定义的中间，而在类型别名中，新类别的名称和定义的其余部分由等号分隔。

第三，名称“typedef”表示正在定义一个新类型，但这不是真的。typedef只是一个别名。

{{< alert success >}}
**最佳实践**

与typedef相比，优先使用类型别名。

{{< /alert >}}

***
## 何时应使用类型别名？

我们已经介绍了类型别名是什么，那么让我们讨论一下它们的用途。

***
## 使用类型别名进行与平台无关的编码

类型别名的主要用途之一是隐藏特定于平台的详细信息。在某些平台上，int是2个字节，而在其他平台上，它是4个字节。因此，在编写独立于平台的代码时，使用int存储超过2个字节的信息可能是危险的。

由于char、short、int和long没有指示它们的大小，因此跨平台程序通常使用类型别名来定义包含类型大小（以位为单位）的别名。例如，int8_t是8位有符号整数，int16_t是16位有符号整数，int32_t是32位有符号整数。以这种方式使用类型别名有助于防止错误，并使我们更清楚地了解对变量大小所做的假设。

为了确保每个别名类型解析为正确大小的类型，这种类型别名通常与预处理器指令一起使用:

```C++
#ifdef INT_2_BYTES
using int8_t = char;
using int16_t = int;
using int32_t = long;
#else
using int8_t = char;
using int16_t = short;
using int32_t = int;
#endif
```

在整数仅为2个字节的机器上，可以#define INT_2_BYTES（作为编译器/预处理器设置），这将使用上部分定义的别名。在整数为4个字节的机器上，未定义INT_2_BYTES将导致使用底部的一组类型别名。通过这种方式，只要INT_2_BYTES定义正确，int8_t将解析为1字节整数，int16_t将分解为2字节整数，而int32_t将解为4字节整数（使用适合于正在编译程序的机器的char、short、int和long组合）。

固定宽度整数类型（如std::int16_t和std::uint32_t）和size_t类型实际上只是各种基本类型的类型别名。

这也是为什么在使用std::cout打印8位固定宽度整数时，很可能会得到字符值。例如:

```C++
#include <cstdint> // 引入固定宽度整数
#include <iostream>

int main()
{
    std::int8_t x{ 97 }; // int8_t 通常是 signed char 的别名
    std::cout << x << '\n';

    return 0;
}
```

该程序打印:

```C++
a
```

因为std::int8_t通常是signed char的别名，所以变量x可能被定义为有符号字符。char类型将其值打印为ASCII字符，而不是整数值。

***
## 使用类型别名使复杂类型更易于阅读

尽管到目前为止，我们只处理了简单的数据类型，但在高级C++中，在键盘上手动输入类型可能会非常复杂和冗长。例如，您可能会看到这样定义的函数和变量:

```C++
#include <string> // for std::string
#include <vector> // for std::vector
#include <utility> // for std::pair

bool hasDuplicates(std::vector<std::pair<std::string, int>> pairlist)
{
    // 这里可能有一些其它代码
    return false;
}

int main()
{
     std::vector<std::pair<std::string, int>> pairlist;

     return 0;
}
```

在需要使用该类型的任何地方键入std::vector<std::pair<std::string, int>> 都很麻烦，并且很容易出错。使用类型别名要容易得多:

```C++
#include <string> // for std::string
#include <vector> // for std::vector
#include <utility> // for std::pair

using VectPairSI = std::vector<std::pair<std::string, int>>; // 使用 VectPairSI 作为一个简短的别名

bool hasDuplicates(VectPairSI pairlist) // 使用 VectPairSI 作为参数的类型
{
    // 这里可能有一些其它代码
    return false;
}

int main()
{
     VectPairSI pairlist; // 初始化一个 VectPairSI 变量

     return 0;
}
```

好多了！现在，我们只需键入VectPairSI，而不是std::vector<std::pair<std::string, int>>。

如果您不知道std::vector、std::pair或所有这些疯狂的尖括号是什么，请不要担心。这里您真正需要理解的唯一一点是，类型别名允许您获取复杂的类型，并为它们提供一个更简单的名称，这使得代码更容易阅读，并节省输入难度。

这可能是类型别名的最佳用法。

***
## 使用类型别名来记录值的含义

类型别名也有助于代码文档化和理解。

对于变量，我们有变量的标识符来帮助记录变量的用途。但考虑函数的返回值的情况。数据类型（如char、int、long、double和bool）描述函数返回的值的类型，但更常见的是，我们想知道返回值的含义。

例如，给定以下函数:

```C++
int gradeTest();
```

我们可以看到返回值是一个整数，但整数意味着什么？字母等级？漏掉的问题数量？学生的号码？错误代码？谁知道呢！int的返回类型告诉我们的不多。如果幸运的话，函数的文档存在于我们可以参考的地方。如果我们运气不好，我们必须阅读代码并推断其目的。

现在，让我们使用类型别名执行等效版本:

```C++
using TestScore = int;
TestScore gradeTest();
```

TestScore的返回类型，使函数返回表示测试分数的目的变得更加明显。

在我们的经验中，仅仅创建类型别名来记录单个函数的返回类型是不值得的（使用注释代替）。但如果有多个函数传递或返回这样的类型，则创建类型别名可能是值得的。

***
## 使用类型别名以简化代码维护

类型别名还允许您更改对象的基础类型，而不必更新许多硬编码类型。例如，如果您使用short来保存学生的ID号，但后来又决定使用long来代替，则必须梳理大量代码，并将short替换为long。很可能很难确定哪些short类型的对象用于保存ID号，哪些用于其他目的。

然而，如果使用类型别名，则更改类型就像更新类型别名一样简单（例如，从 using StudentId = short; 切换到 using StudentId = long;）。

虽然这似乎是一个不错的好处，但无论何时更改类型，都必须谨慎，因为程序的行为也可能会更改。当将类型别名的类型更改为不同类型族中的类型时（例如，将整数更改为浮点值，或将有符号值更改为无符号值），这尤其需要留意！新类型可能存在比较或整数/浮点除法问题，或者旧类型没有的其他问题。如果将现有类型更改为其他类型，则应彻底重新测试代码。

***
## 缺点和结论

虽然类型别名提供了一些好处，但它们也在代码中引入了另一个需要理解的标识符。如果这没有被可读性或理解性的一些好处所抵消，那么类型别名弊大于利。

利用率较低的别名，会将我们熟悉的类型名称隐藏，并且我们无法直接搜索被隐藏的类型名称。在某些情况下（例如，使用智能指针，我们将在未来的一章中介绍），模糊类型信息也可能有害于理解类型应该如何工作。

由于这个原因，类型别名应该主要用于对代码可读性或代码维护有明显好处的情况。这既是一门科学，也是一门艺术。当类型别名可以在代码中的许多地方使用，而不是在较少的地方使用时，它们最有用。

***

{{< prevnext prev="/basic/chapter10/explicit-type-convert-static-cast/" next="/basic/chapter10/auto-type-object/" >}}
10.5 显式类型转换和static_cast
<--->
10.7 使用auto关键字的对象类型自动推导
{{< /prevnext >}}
