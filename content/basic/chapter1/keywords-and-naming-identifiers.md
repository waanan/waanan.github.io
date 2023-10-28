---
title: "关键字和变量命名规则"
date: 2023-10-09T20:06:10+08:00
---

## 关键词

C++保留一组92个单词（从C++23开始）供自己使用。这些词被称为关键字（或保留词），并且每个关键字在C++语言中都有特殊的含义。

下面是所有C++关键字的列表（截止C++23）：


|     |    |   |    |
|  ----  | ----  | ----  | ----  |
| alignas | const_cast | int | static_assert |
| alignof | continue | long | static_cast |
| and | co_await (C++20) | mutable | struct |
| and_eq | co_return (C++20) | namespace | switch |
| asm | co_yield (C++20) | new | template |
| auto | decltype | noexcept | this |
| bitand | default | not | thread_local |
| bitor | delete | not_eq | throw |
| bool | do | nullptr | true |
| break | double | operator | try |
| case | dynamic_cast | or | typedef |
| catch | else | or_eq | typeid |
| char | enum | private | typename |
| char8_t (C++20) | explicit | protected | union |
| char16_t | export | public | unsigned |
| char32_t | extern | register | using |
| class | false | reinterpret_cast | virtual |
| compl | float | requires (C++20) | void |
| concept (C++20) | for | return | volatile |
| const | friend | short | wchar_t |
| consteval (C++20) | goto | signed | while |
| constexpr | if | sizeof | xor |
| constinit (C++20) | inline | static | xor_eq |



在C++20中添加了标记为（C++20）的关键字。如果编译器不兼容C++20（或确实具有C++20功能，但默认情况下已关闭），则这些关键字可能不起作用。

C++还定义了特殊标识符：override、final、import和module。当在某些上下文中使用时，它们具有特定的含义，但在其他情况下不保留。

您已经遇到了其中的一些关键字，包括int和return。除了一组操作符外，这些关键字和特殊标识符定义了C++的整个语言（不包括预处理器命令）。由于关键字和特殊标识符具有特殊含义，您的IDE可能会更改这些单词的文本颜色，使它们从其他标识符看起来更加明显。

当您完成本教程系列时，您将了解几乎所有这些单词的作用！

***
## 标识符命名规则

变量（或函数、类型或其他类型）的名称称为标识符。C++为您提供了很大的灵活性，可以根据需要命名标识符。然而，命名标识符时必须遵循一些规则：

1. 标识符不能是关键字。关键字被C++语言保留使用。
2. 标识符只能由字母（小写或大写）、数字和下划线字符组成。这意味着名称不能包含符号（下划线除外）或空白（空格或制表符）。
3. 标识符必须以字母（小写或大写）或下划线开头。它不能以数字开头。
4. C++区分大小写，因此区分大小写字母。nvalue不同于nValue不同于NVALUE。


***
## 标识符命名最佳实践

让我们讨论一下应该如何命名变量（或函数）。

首先，C++中的一个约定是变量名应该以小写字母开头。如果变量名是一个单词，则整个内容应该用小写字母书写。

```C++
int value; // 推荐

int Value; // 不推荐
int VALUE; // 不推荐
int VaLuE; // 不推荐
```

通常，函数名也以小写字母开头（尽管在这一点上存在一些分歧）。我们将遵循这个约定，因为函数main（所有程序都必须具有）以小写字母开头，C++标准库中的所有函数也是如此。

以大写字母开头的标识符名称通常用于用户定义的类型（例如结构、类和枚举，将在后面介绍所有这些）。

如果变量或函数名是多个单词，则有两种常见的约定：由下划线分隔的单词（有时称为蛇形命名法），或由首字母大写单词（有时候称为驼峰命名法，因为大写字母像骆驼上的驼峰一样竖起）。

```C++
int my_variable_name;   // 蛇形命名法
int my_function_name(); // 蛇形命名法

int myVariableName;   // 驼峰命名法
int myFunctionName(); // 驼峰命名法

int my variable name;   // 不合法（由空格分割）
int my function name(); // 不合法（由空格分割）

int MyVariableName;   // 不推荐 (应该由小写字母开头)
int MyFunctionName(); // 不推荐 (应该由小写字母开头)
```

在本教程中，我们通常将使用驼峰命名法，因为它更容易阅读（在密集的代码块中，很容易将下划线误认为空格）。但两者都很常见——C++标准库对变量和函数都使用下划线分割方法。有时您会看到两者的混合：用于变量的蛇形命名法和用于函数的驼峰命名法。

值得注意的是，如果您与他人一同编写代码，通常认为匹配您正在使用的代码的风格比严格遵循上面列出的命名约定要好。

其次，应该避免以下划线开头命名标识符，因为这些名称通常保留给操作系统、库和/或编译器使用。

第三，标识符应该明确它们所持有的值的含义（特别是在单位不明显的情况下）。标识符的命名方式应该有助于那些不知道您的代码做什么的人能够尽快地理解它。在代码编写完3个月后，当你再次查看你的程序时，你会忘记它是如何工作的，你会感谢你自己选择了有意义的变量名。

然而，给一个微不足道的变量一个过于复杂的名称会阻碍对程序的全面理解，这几乎与给一个广泛使用的标识符一个不适当的名称一样。因此，一个好的经验法则是使标识符的长度与它的使用范围成比例。具有平凡用途的标识符可以具有短名称（例如，i）。使用更广泛的标识符（例如，从程序中的许多不同位置调用的函数）应该具有更长、更具描述性的名称（例如，不要使用open，而是尝试使用openFileOnDisk）。

在任何情况下，避免缩写（除非它们是常见的/明确的）。尽管它们减少了编写代码所需的时间，但它们使代码更难阅读。代码的阅读次数远高于编写次数，您在编写代码时节省的时间是每个代码阅读者（包括未来的您）在阅读代码时浪费的时间。如果您希望更快地编写代码，请使用编辑器的自动完成功能。

对于变量声明，使用注释来描述变量将用于什么，或者解释任何其他可能不明显的东西。例如，假设我们已经声明了一个名为numberOfChars的变量，该变量应该存储一段文本中的字符数。文本“Hello World！”有10个、11个或12个字符吗？这取决于我们是包括空格还是标点符号。与其命名变量numberOfCharsIncludingWhitespaceAndPunctions（相当长），不如在声明行上或上面放置一个适当的注释，以帮助用户理解：

```C++
// 统计文本中的字符串长度，包含空格和标点
int numberOfChars;
```

{{< alert success >}}
**最佳实践**

在老的程序中更改代码时，使用该程序的约定（即使它们不符合现代最佳实践）。编写新程序时，请使用现代最佳实践。

{{< /alert >}}

***

{{< prevnext prev="/basic/chapter1/uninit-variable/" next="/basic/chapter1/whitespace/" >}}
1.5 未初始化的变量及未定义的行为
<--->
1.7 空白字符与代码样式
{{< /prevnext >}}
