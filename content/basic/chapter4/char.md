---
title: "字符"
date: 2023-10-09T20:06:10+08:00
---

到目前为止，我们研究的基本数据类型包含保存数字（整数和浮点）或真/假值（布尔）。但如果我们想存储字母或标点符号呢？

```C++
#include <iostream>

int main()
{
    std::cout << "Would you like a burrito? (y/n)";

    // 想让用户输入 'y' or 'n' 的字符
    // 如何做到？

    return 0;
}
```

char数据类型被设计为保存单个字符。字符可以是单个英文字母、数字、符号或空白。

char数据类型是整型，这意味着底层值存储为整数。与布尔值0被解释为false而非零，1被解释为true的方式类似，char变量存储的整数被解释为ASCII字符。

ASCII（ American Standard Code for Information Interchange，美国信息交换标准代码），它定义了一种特殊的编码方法，将英语字符（加上一些其他符号）表示为0到127之间的数字（称为ASCII码）。例如，ASCII码97被解释为字符'a'。

字符文本总是放在单引号之间（例如'g'、'1'、''）。

下面是ASCII字符的完整表格：

|  编号 |  字符  |  编号 |  字符  |  编号 |  字符  |  编号 |  字符  |
|  ----  | ----  |  ----  | ----  |  ----  | ----  |  ----  | ----  |
| 0 | NUL (null) | 32 | (space) | 64 | @ | 96 | ` |
| 1 | SOH (start of header) | 33 | ! | 65 | A | 97 | a |
| 2 | STX (start of text) | 34 | ” | 66 | B | 98 | b |
| 3 | ETX (end of text) | 35 | # | 67 | C | 99 | c |
| 4 | EOT (end of transmission) | 36 | $ | 68 | D | 100 | d |
| 5 | ENQ (enquiry) | 37 | % | 69 | E | 101 | e |
| 6 | ACK (acknowledge) | 38 | & | 70 | F | 102 | f |
| 7 | BEL (bell) | 39 | ’ | 71 | G | 103 | g |
| 8 | BS (backspace) | 40 | ( | 72 | H | 104 | h |
| 9 | HT (horizontal tab) | 41 | ) | 73 | I | 105 | i |
| 10 | LF (line feed/new line) | 42 | * | 74 | J | 106 | j |
| 11 | VT (vertical tab) | 43 | + | 75 | K | 107 | k |
| 12 | FF (form feed / new page) | 44 | , | 76 | L | 108 | l |
| 13 | CR (carriage return) | 45 | - | 77 | M | 109 | m |
| 14 | SO (shift out) | 46 | . | 78 | N | 110 | n |
| 15 | SI (shift in) | 47 | / | 79 | O | 111 | o |
| 16 | DLE (data link escape) | 48 | 0 | 80 | P | 112 | p |
| 17 | DC1 (data control 1) | 49 | 1 | 81 | Q | 113 | q |
| 18 | DC2 (data control 2) | 50 | 2 | 82 | R | 114 | r |
| 19 | DC3 (data control 3) | 51 | 3 | 83 | S | 115 | s |
| 20 | DC4 (data control 4) | 52 | 4 | 84 | T | 116 | t |
| 21 | NAK (negative acknowledge) | 53 | 5 | 85 | U | 117 | u |
| 22 | SYN (synchronous idle) | 54 | 6 | 86 | V | 118 | v |
| 23 | ETB (end of transmission block) | 55 | 7 | 87 | W | 119 | w |
| 24 | CAN (cancel) | 56 | 8 | 88 | X | 120 | x |
| 25 | EM (end of medium) | 57 | 9 | 89 | Y | 121 | y |
| 26 | SUB (substitute) | 58 | : | 90 | Z | 122 | z |
| 27 | ESC (escape) | 59 | ; | 91 | [ | 123 | {  |
| 28 | FS (file separator) | 60 | < | 92 | \ | 124 | \| |
| 29 | GS (group separator) | 61 | = | 93 | ] | 125 | }  |
| 30 | RS (record separator) | 62 | > | 94 | ^ | 126 | ~  |
| 31 | US (unit separator) | 63 | ? | 95 | _ | 127 | DEL (delete)  |

字符0-31被称为不可打印字符，它们主要用于格式化和控制打印机。其中大多数现在已经过时了。如果尝试打印这些字符，结果取决于您的操作系统（您可能会得到一些类似表情符号的字符）。

字符32-127被称为可打印字符，它们表示大多数计算机用于显示基本英语文本的字母、数字字符和标点符号。

***
## 字符变量初始化

可以使用字符文本初始化字符变量：

```C++
char ch2{ 'a' }; // 使用 'a' (对应存储为数字 97) 初始化字符变量
```

您也可以用整数初始化字符，但应该避免这种情况

```C++
char ch1{ 97 }; // 使用数字 97 ('a') 初始化字符变量
```

{{< alert success >}}
**警告**

注意不要将字符与整数混淆。以下两个初始化不相同：

```C++
char ch{5}; // 使用数字 5 (存储为 5)
char ch{'5'}; // 使用字符 '5' (存储为 53)
```

{{< /alert >}}

***
## 打印字符

使用std::cout打印字符时，std::cout将字符变量输出为ASCII字符：

```C++
#include <iostream>

int main()
{
    char ch1{ 'a' };
    std::cout << ch1; // 打印字符 'a'

    char ch2{ 98 }; // 初始化为字符 'b' (不推荐)
    std::cout << ch2; // 打印字符 'b'


    return 0;
}
```

结果：

```C++
ab
```

我们还可以直接输出字符文本：

```C++
std::cout << 'c';
```

这将产生以下结果：

```C++
c
```

***
## 输入字符

以下程序要求用户输入字符，然后打印出字符：

```C++
#include <iostream>

int main()
{
    std::cout << "Input a keyboard character: ";

    char ch{};
    std::cin >> ch;
    std::cout << "You entered: " << ch << '\n';

    return 0;
}
```

下面是运行的输出：

```C++
Input a keyboard character: q
You entered: q
```

请注意，std::cin允许您输入多个字符。然而，变量ch只能容纳1个字符。因此，只有第一个输入字符被提取到变量ch中。其余的用户输入留在std::cin的输入缓冲区中，并且可以通过后续继续调用std:∶cin来提取。

您可以在以下示例中看到此行为：

```C++
#include <iostream>

int main()
{
    std::cout << "Input a keyboard character: "; // 假设此时用户输入 "abcd"

    char ch{};
    std::cin >> ch; // ch = 'a', "bcd" 被缓存起来
    std::cout << "You entered: " << ch << '\n';

    // 注: 下面的cin不需要用户再输入了, 读的是缓冲区的数据!
    std::cin >> ch; // ch = 'b', "cd" 被缓存
    std::cout << "You entered: " << ch << '\n';
    
    return 0;
}
```

如果您想一次读入多个字符（例如，读入名称、单词或句子），则需要使用字符串而不是字符。字符串是连续字符的集合（字符串可以包含多个符号）。我们将在（std::string简介）中讨论。

***
## 字符大小、范围和符号

char由C++定义，大小始终为1个字节。默认情况下，字符可以有符号或无符号（尽管它通常是有符号的）。如果使用字符来保存ASCII字符，则不需要指定符号（因为有符号和无符号字符都可以保存0到127之间的值）。

如果使用char来保存小的整数（除非显式的优化存储空间，否则不应该这样做），那么应该始终指定它是有符号的还是无符号的。有符号字符可以容纳-128到127之间的数字。无符号字符可以容纳0到255之间的数字。

***
## 转义

C++中有一些字符具有特殊意义。这些字符称为转义字符。转义字符以'\'（反斜杠）字符开头，然后是后面的字母或数字。

您已经看过了最常见的转义序列：'\n'，可用于打印换行：

```C++
#include <iostream>

int main()
{
    int x { 5 };
    std::cout << "The value of x is: " << x << '\n'; // 单引号包围的 \n 表示是单个字符
    std::cout << "First line\nSecond line\n";        // \n 也可以放在一个字符串里
    return 0;
}
```

输出：

```C++
The value of x is: 5
First line
Second line
```

另一个常用的转义字符是'\t'，它表示一个水平制表符（Tab）：

```C++
#include <iostream>

int main()
{
    std::cout << "First part\tSecond part";
    return 0;
}
```

输出：

```C++
First part	Second part
```

其他三个值得注意的转义序列是：
1. \\' 单引号
2. \\" 双引号
3. \\\ 反斜杠

下面是所有转义序列的表：

|  名称 |  符号  |  含义 |
|  ----  | ----  |  ----  |
| 告警（Alert） | \a | 发出告警，例如响铃 |
| 退格（Backspace） | \b | 将光标往后移一格 |
| 换页（Formfeed） | \f | 将光标移动到下一页 |
| 换行（Newline） | \n | 将光标移动到下一行 |
| 回车（Carriage return） | \r | 将光标移动到行的开头 |
| 水平制表（Horizontal tab） | \t | 水平制表符 |
| 垂直制表（Vertical tab） | \v | 垂直制表符 |
| 单引号（Single quote） | \\' | 单引号 |
| 双引号（Double quote） | \\" | 双引号 |
| 反斜杠（Backslash） | \\\ | 反斜杠 | 
| 问号（Question mark） | \\? | 问号 |
| 八进制数字（Octal number） | \\(number) | 按八进制解释为数字 |
| 十六进制数字（Hex number） | \x(number) | 按十六进制解释为数字 |

下面是一些示例：

```C++
#include <iostream>

int main()
{
    std::cout << "\"This is quoted text\"\n";
    std::cout << "This string contains a single backslash \\\n";
    std::cout << "6F in hex is char '\x6F'\n";
    return 0;
}
```

打印：

```C++
"This is quoted text"
This string contains a single backslash \
6F in hex is char 'o'
```

{{< alert success >}}
**警告**

转义字符以反斜杠（\）开头，而不是正斜杠（/）。如果无意中使用了正斜杠，它可能仍然可以编译，但不会产生所需的结果。

{{< /alert >}}

***
## 将字符放在单引号和双引号中有什么区别？

单个字符总是放在单引号中（例如'a'、'+'、'5'）。一个字符只能表示一个符号（例如，字母A、加号、数字5）。

双引号之间的文本（例如"Hello，world！"）被视为多个字符组成的字符串。后续在字符串章节进行介绍。

{{< alert success >}}
**最佳做法**

将独立字符放在单引号中（例如，'t'或'\n'，而不是"t"或"\n"）。这有助于编译器更有效地优化。

{{< /alert >}}

***
## 避免多字符文本

出于向后兼容性的原因，许多C++编译器支持''中包含多个字符（例如'56'）, 具体代表的功能因编译器而异。由于它们不是C++标准的一部分，并且它们的值没有严格定义，因此应该避免这样使用。

有时会这个特性给新程序员带来困扰。考虑以下简单程序：

```C++
#include <iostream>

int add(int x, int y)
{
 | return x + y;
}

int main()
{
 | std::cout << add(1, 2) << '/n';

 | return 0;
}
```

程序员希望该程序打印值3和换行。但相反，在作者的机器上，它输出以下内容：

```C++
312142
```

这里的问题是，程序员意外地使用了'/n'（由正斜杠和'n'字符组成的多字符文本），而不是'\n'（换行符的转义序列）。程序首先正确打印3（加法（1，2）的结果）。但随后它打印'/n'的值，该值在作者的机器上的值是12142。

{{< alert success >}}
**最佳实践**

避免多字符文本（例如'56'）。

{{< /alert >}}

{{< alert success >}}
**警告**

确保换行使用的是转义字符'\n'，而不是多字符文本'/n'。

{{< /alert >}}

***
## 其他char类型wchar_t、char8_t、char16_t和char32_t

在几乎所有情况下都应该避免wchar_t（与Windows API接口时除外）。其大小由实现定义，不可靠。它在很大程度上已被弃用（deprecated）。

就像ASCII将整数0-127映射到美式英语字符一样，存在其他字符编码标准来将整数映射到其他语言中的字符。ASCII之外最著名的映射是Unicode标准，它将144000多个整数映射到许多不同语言中的字符。由于Unicode包含如此多的字符，因此单个Unicode码需要32位来表示字符（称为UTF-32）。然而，Unicode字符也可以使用多个16位或8位整数（分别称为UTF-16和UTF-8）进行编码。

char16_t和char32_t被添加到C++11中，以提供对16位和32位Unicode字符的显式支持。char8_t添加到C++20中。这些字符类型的大小分别与std::uint_least16_t、std::uint_least32_t和std::uint_least8_t相同（但它们是不同的类型）。从理论上讲，这意味着char#_t类型可以大于#指定的位数（除非您正在使用深奥的体系结构，否则它们应该相同）。

除非计划使程序与Unicode兼容，否则不需要使用char8_t、char16_t或char32_t。Unicode和文本的本地化不在本教程的范围内，因此我们将不再进一步介绍它。

一般情况下，在处理字符（和字符串）时，应该只使用ASCII字符。使用其他字符集的字符可能会导致显示不正确。

{{< alert success >}}
**作为旁白…**

术语“已弃用（deprecated）”意味着“仍然受支持，但不再建议使用，因为它已被更好的东西取代，或者不再被认为是安全的”。

{{< /alert >}}

***

{{< prevnext prev="/basic/chapter4/if/" next="/" >}}
4.9 if语句简介
<--->
主页
{{< /prevnext >}}
