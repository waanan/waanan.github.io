---
title: "字面值常量"
date: 2023-11-28T13:19:42+08:00
---

字面值是直接插入到代码中的值。例如：

```C++
return 5;                     // 5 是整数字面值
bool myNameIsAlex { true };   // true 是bool字面值
double d { 3.4 };             // 3.4 是double 字面值
std::cout << "Hello, world!"; // "Hello, world!" 是 C语言格式的字符串字面值
```

字面值有时被称为字面值常量，因为它们的值无法重新定义（5总是指整数值5）。

***
## 字面值的类型

就像对象有类型一样，所有字面值都有类型。字面值的类型是从字面值的值中推导出来的。例如，作为整数（例如5）的字面值被推断为int类型。

默认情况下：

|  字面值 | 样例 |  类型  |
|  ---- | ----  | ----  |
| 整数 | 5, 0, -3 | int |
| bool | true, false | bool |
| 浮点数 | 1.2, 0.0, 3.4 | double (not float!) |
| 字符 | 'a', '\n' | char |
| C语言格式的字符串 | "Hello, world!" | const char[14] |

***
## 字面值后缀

如果字面值的默认类型不符合需要，则可以通过添加后缀来更改字面值的类型：

|  类别 | 后缀 |  类型  |
|  ---- | ----  | ----  |
| integral | u or U | unsigned int |
| integral | l or L | long |
| integral | ul, uL, Ul, UL, lu, lU, Lu, LU | unsigned long |
| integral | ll or LL | long long |
| integral | ull, uLL, Ull, ULL, llu, llU, LLu, LLU | unsigned long long |
| integral | z or Z | The signed version of std::size_t (C++23) |
| integral | uz, uZ, Uz, UZ, zu, zU, Zu, ZU | std::size_t (C++23) |
| floating point | f or F | float |
| floating point | l or L | long double |
| string | s | std::string |
| string | sv | std::string_view |

大多数后缀不区分大小写。由于小写L在某些字体中看起来像数字1，因此一些开发人员更喜欢使用大写字面值。

{{< alert success >}}
**最佳实践**

首选字面值后缀L（大写）而不是l（小写）。

{{< /alert >}}

***
## 整型字面值

通常不需要为整型字面值使用后缀，但以下是示例：

```C++
#include <iostream>

int main()
{
    std::cout << 5 << '\n';  // 5 (无后缀) 是类型 int (默认情况)
    std::cout << 5L << '\n'; // 5L 是类型 long
    std::cout << 5u << '\n'; // 5u 是类型 unsigned int

    return 0;
}
```

在大多数情况下，即使在初始化非int的整型时，也可以使用无后缀的int字面值：

```C++
#include <iostream>

int main()
{
    int a { 5 };          // ok: 类型匹配
    unsigned int b { 6 }; // ok: 编译器会转换数字成 unsigned int
    long c { 7 };         // ok: 编译器会转换数字成 long

    return 0;
}
```

在这种情况下，编译器将把int转换为适当的类型。

***
## 浮点字面值

默认情况下，浮点字面值的类型为double。要使它们成为float字面值，应使用F（或f）后缀：

```C++
#include <iostream>

int main()
{
    std::cout << 5.0 << '\n';  // 5.0 (无后缀) 是类型 double (默认情况)
    std::cout << 5.0f << '\n'; // 5.0f 是类型 float

    return 0;
}
```

新手程序员通常会对以下编译器警告感到困惑：

```C++
float f { 4.1 }; // warning: 4.1 is a double literal, not a float literal
```

因为4.1没有后缀，所以字面值的类型是double，而不是float。当编译器确定字面值的类型时，它并不关心您对字面值所做的操作（例如，在本例中，使用它来初始化float变量）。由于字面值（double）的类型与它用于初始化的变量（float）的类型不匹配，因此必须将字面值转换为float，以便随后可以使用它来初始化变量f。将值从double转换为float可能会导致精度损失，因此编译器将发出警告。

这里的解决方案是以下之一：

```C++
float f { 4.1f }; // 使用 'f' 后缀声明字面值
double d { 4.1 }; // 将变量类型改为double
```

***
## 浮点字面值的科学表示法

声明浮点字面值有两种不同的方法：

```C++
double pi { 3.14159 }; // 3.14159 是标准写法
double avogadro { 6.02e23 }; // 6.02 x 10^23 是科学计数法写法
```

在第二种形式中，指数后面的数字可以是负数：

```C++
double electronCharge { 1.6e-19 }; // 电子的电荷量是 is 1.6 x 10^-19
```

***
## 字符串常量

在编程中，字符串是用于表示文本（如名称、单词和句子）的连续字符的集合。

您编写的第一个C++程序可能如下所示：

```C++
#include <iostream>
 
int main()
{
    std::cout << "Hello, world!";
    return 0;
}
```

"Hello，world" 是一个字符串字面值。字符串字面值放在双引号之间，以将它们标识为字符串（而字符字面值放在单引号之间）。

由于字符串通常在程序中使用，因此大多数现代编程语言都包含基本的字符串数据类型。由于历史原因，字符串不是C++中的基本类型。相反，它们有一种奇怪、复杂的类型，很难使用（一旦我们涵盖了解释它们如何工作所需的更多基础知识，我们将在以后的课程中讨论如何/为什么）。这样的字符串通常称为C字符串或C样式的字符串，因为它们是从C语言继承的。

关于C样式的字符串字面值，有两件不明显的事情值得了解。

空终止符的原因也是历史性的：它可以用于确定字符串的结束位置。

与C样式字符串字面值不同，std:：string和std::string_view创建临时对象。这些临时对象必须立即使用，因为它们在创建它们的完整表达式的末尾被销毁。

{{< alert success >}}
**对于高级读者**

这就是字符串“Hello，world！”的类型为constchar[14]而不是constchar/13]的原因——隐藏的空终止符计为字符。

{{< /alert >}}

{{< alert success >}}
**关键洞察力**

C样式字符串字面值是在程序开始时创建的常量对象，并保证在整个程序中存在。

{{< /alert >}}

{{< alert success >}}
**相关内容**

我们在第5.9课——std:：string简介和第5.10课——std:：string_view简介中分别讨论了std:∶string和std::string_view字面值。

{{< /alert >}}

***
## 神奇的数字

幻数是一个字面意思不清楚或以后可能需要更改的字面值（通常是数字）。

下面是两个显示幻数示例的语句：

```C++
constexpr int maxStudentsPerSchool{ numClassrooms * 30 };
setMax(30);
```

在这些上下文中，字面值30是什么意思？在前一种情况下，你可能会猜到这是每个班级的学生数量，但这并不立即明显。在后者中，谁知道呢。我们必须查看函数才能知道它做什么。

在复杂的程序中，除非有注释来解释，否则很难推断字面值表示什么。

使用幻数通常被认为是不好的做法，因为除了没有提供它们用于什么的上下文之外，如果值需要更改，它们还会带来问题。假设学校购买了新课桌，使他们能够将班级规模从30人提高到35人，我们的计划需要反映这一点。

为此，我们需要将一个或多个字面值从30更新为35。但哪些字面值呢？maxStudentsPerSchool初始值设定项中的30似乎很明显。但用作setMax（）参数的30呢？这30个与其他30个的含义相同吗？如果是，则应更新。否则，它应该被单独处理，否则我们可能会在其他地方破坏我们的程序。如果进行全局搜索和替换，则可能会在setMax（）的参数不应更改时无意中更新该参数。因此，您必须检查字面值30的每个实例的所有代码（其中可能有数百个），然后单独确定是否需要更改。这可能非常耗时（并且容易出错）。

幸运的是，通过使用符号常量，可以轻松解决上下文的缺乏和更新相关的问题：

```C++
constexpr int maxStudentsPerClass { 30 };
constexpr int totalStudents{ numClassrooms * maxStudentsPerClass }; // now obvious what this 30 means

constexpr int maxNameLength{ 30 };
setMax(maxNameLength); // now obvious this 30 is used in a different context
```

常量的名称提供了上下文，我们只需要在一个位置更新值，就可以在整个程序中更改值。

请注意，幻数并不总是数字——它们也可以是字面值（例如名称）或其他类型。

在不太可能改变的明显上下文中使用的字面值通常不被认为是神奇的。值-1、0、0.0和1通常用于以下上下文：

```C++
int idGenerator { 0 };         // fine: we're starting our id generator with value 0
idGenerator = idGenerator + 1; // fine: we're just incrementing our generator
```

其他数字在上下文中也可能是显而易见的（因此，不被认为是神奇的）：

```C++
int kmtoM(int km)
{
    return km * 1000; // fine: it's obvious 1000 is a conversion factor
}
```

{{< alert success >}}
**最佳做法**

在代码中避免使用幻数（改用constexpr变量）。

{{< /alert >}}

