---
title: "数值转换"
date: 2024-01-31T13:21:38+08:00
---

在上一课中，介绍了数值提升，这是将特定的较窄的数字类型转换为可以有效处理的较宽的数字类型（通常是int或double）。

C++支持另一类数值类型转换，称为数值转换。这些数值转换涵盖基本类型之间的其他类型转换。

有五种基本类型的数值转换。

```C++
short s = 3; // int to short
long l = 3; // int to long
char ch = s; // short to char
unsigned int u = 3; // int to unsigned int
```

```C++
float f = 3.0; // double to float
long double ld = 3.0; // double to long double
```

```C++
int i = 3.5; // double to int
```

```C++
double d = 3; // int to double
```

```C++
bool b1 = 3; // int to bool
bool b2 = 3.0; // double to bool
```

{{< alert success >}}
**关键点**

数值提升规则涵盖的任何类型转换都是数值提升，而不是数值转换。

{{< /alert >}}

{{< alert success >}}
**旁白**

大括号初始化严格禁止某些类型的数值转换（下一课将详细介绍），因此我们在本课中使用复制初始化（它没有任何此类限制），以保持示例简单。

{{< /alert >}}

***
## 安全与潜在的不安全转换

与数值提升（始终保持值，因此“安全”）不同，某些数值转换在某些情况下不保持值。这种转换被称为“不安全”（尽管“潜在不安全”更准确，因为在其他情况下，这些转换是保值的）。

数值转换中的三个类别：

1. 目标类型可以精确的保存当前类型的所有值，这是安全的数值转换

例如，int到long和short到double是安全的转换，因为源值始终可以转换为目标类型的等效值。

```C++
int main()
{
    int n { 5 };
    long l = n; // okay, 产出 long 5

    short s { 5 };
    double d = s; // okay, 产出 double 5.0

    return 0;
}
```

编译器通常不会针对隐式的保留源值转换产生警告。

使用保值转换，转换的值始终可以转换回源类型，从而产生与原始值等效的值：

```C++
#include <iostream>

int main()
{
    int n = static_cast<int>(static_cast<long>(3)); // 将 int 3 转到 long 再转回 int
    std::cout << n << '\n';                         // 打印 3

    char c = static_cast<char>(static_cast<double>('c')); // 将 char 'c' 转到 double 再转回 char
    std::cout << c << '\n';                               // 打印 'c'

    return 0;
}
```

2. 数值重解释的转换，是潜在不安全的转换。因为转换后的值可能不在原来的类型的范围内。有符号与无符号之前的转换就属于这一种。

例如，将signed int转换为unsigned int时：

```C++
int main()
{
    int n1 { 5 };
    unsigned int u1 { n1 }; // okay: 转换成 unsigned int 5 (值会保留)

    int n2 { -5 };
    unsigned int u2 { n2 }; // bad: 会生成超过 signed int范围的超大数字

    return 0;
}
```

在u1的情况下，有符号int值5被转换为无符号int值5。在这种情况下保留该值。

在u2的情况下，有符号int值-5被转换为无符号int。由于无符号int不能表示负数，因此结果将是一个不在有符号int范围内的大整数值。在这种情况下，不会保留该值。

这种值更改通常是不符合预期的，并且通常会导致程序表现出意外的或实现定义的行为。

{{< alert success >}}
**警告**

尽管重新解释转换可能不安全，但大多数编译器默认情况下都会禁用有符号/无符号转换警告。

这是因为在现代C++的某些领域（例如使用标准库数组时），有符号/无符号转换很难避免。实际上，大多数这样的转换实际上不会导致值更改。因此，启用这样的警告可能会导致许多的虚假警告，淹没了正常的其它警告。

如果选择禁用此类警告，请特别注意这些类型之间的无意转换（特别是在将数据传递给采用相反符号的参数的函数时）。

{{< /alert >}}

使用重新解释转换转换的值可以转换回源类型，从而产生与原始值相等的值（即使初始转换产生的值超出源类型的范围）。

```C++
#include <iostream>

int main()
{
    int u = static_cast<int>(static_cast<unsigned int>(-5)); // 将 '-5' 转换成 unsigned 再转回来
    std::cout << u << '\n'; // prints -5
    
    return 0;
}
```

{{< alert success >}}
**对于高级读者**

在C++20之前，转换超出有符号值范围的无符号值在技术上是未定义的行为（由于允许有符号整数可以使用与无符号整数不同的二进制表示形式）。但在实践中，在现代系统上一般无此问题。

C++20现在要求有符号整数使用补码。因此，转换规则有了定义，因此上述转换现在被明确定义为重新解释的转换。

请注意，虽然这样的转换定义良好，但有符号数算术溢出（当算术运算产生可存储范围之外的值时发生）仍然是未定义的行为。

{{< /alert >}}

3. 有损转换，是潜在不安全的转换。因为可能会丢失数据。

例如，double到int是可能导致数据丢失的转换：

```C++
int i = 3.0; // okay: 转换到 int 3 (值会保留)
int j = 3.5; // 数据丢失: 转换到 int 3 (分数部分 0.5 丢失)
```

从双精度到单精度的转换也可能导致数据丢失：

```C++
float f = 1.2;        // okay: 转换到 float 1.2 (值会保留)
float g = 1.23456789; // 数据丢失: 转换到 float 1.23457 (精度丢失)
```

将丢失数据的值转换回源类型将导致与原始值不同的值：

```C++
#include <iostream>

int main()
{
    double d { static_cast<double>(static_cast<int>(3.5)) }; // 将 double 3.5 转 int 再转回
    std::cout << d << '\n'; // 打印 3

    double d2 { static_cast<double>(static_cast<float>(1.23456789)) }; // 将 double 1.23456789 转 float 再转回
    std::cout << d2 << '\n'; // 打印 1.23457

    return 0;
}
```

例如，如果将双精度值3.5转换为int值3，则分数分量0.5将丢失。当3转换回双精度时，结果是3.0，而不是3.5。

当执行隐式有损转换时，编译器通常会发出警告（或在某些情况下发出错误）。

{{< alert success >}}
**警告**

根据平台的不同，某些转换可能会分为不同的类别。

例如，int到double通常是安全的转换，因为int通常是4个字节，double一般是8个字节，并且在这样的系统上，所有可能的int值都可以表示为double。然而，在某些体系结构中，int和double都是8个字节。在这种架构上，int到double是有损转换！

我们可以通过将 long long值（必须至少为64位）转换为双精度并转回来演示这一点：

```C++
#include <iostream>

int main()
{
    std::cout << static_cast<long long>(static_cast<double>(10000000000000001LL));

    return 0;
}
```

这将打印：

```C++
10000000000000000
```

请注意，最后一个数字已经丢失！

{{< /alert >}}

***
## 关于数值转换的更多信息

数值转换的特定规则复杂而众多，因此这里是需要记住的最重要的事情。

在所有情况下，将值转换为范围不支持该值的类型将导致可能意外的结果。例如：

```C++
int main()
{
    int i{ 30000 };
    char c = i; // char 的范围是 -128 to 127

    std::cout << static_cast<int>(c) << '\n';

    return 0;
}
```

在这个例子中，我们为类型为char的变量分配了一个大整数（char 范围是-128到127）。这会导致字符溢出，并产生意外的结果：

```C++
48
```

请记住，无符号值的溢出是有标准定义的，有符号值的溢出会产生未定义的行为。

只要值适合较小类型的范围，则从较大的整数或浮点类型转换为相同族中的较小类型通常是有效的。例如：

```C++
    int i{ 2 };
    short s = i; // 从 int 转 short
    std::cout << s << '\n';

    double d{ 0.1234 };
    float f = d;
    std::cout << f << '\n';
```

这会产生预期的结果：

```C++
2
0.1234
```

在浮点值的情况下，由于较小类型的精度损失，可能会发生一些舍入。例如：

```C++
    float f = 0.123456789; // double 0.123456789 有 9 个有效数字, 单 float 值能支持 7 为
    std::cout << std::setprecision(9) << f << '\n'; // std::setprecision 定义在 iomanip 头文件
```

在这种情况下，我们会看到精度损失，因为单精度不能完全保存双精度的值：

```C++
0.123456791
```

只要值适合浮点类型的范围，从整数转换为浮点数通常可以工作。例如：

```C++
    int i{ 10 };
    float f = i;
    std::cout << f << '\n';
```

这会产生预期的结果：

```C++
10
```

只要值适合整数的范围，从浮点转换为整数可以工作，但任何小数都会丢失。例如：

```C++
    int i = 3.5;
    std::cout << i << '\n';
```

在此示例中，分数（.5）丢失，留下以下结果：

```C++
3
```

虽然数值转换规则可能看起来很可怕，但在现实中，如果您试图执行危险的操作（不包括一些有符号/无符号转换），编译器通常会警告您。

***

{{< prevnext prev="/basic/chapter10/promotion/" next="/basic/chapter10/narrow-convert-list-constexpr-init/" >}}
10.1 数值提升
<--->
10.3 窄化转换、列表初始化和constexpr初始化
{{< /prevnext >}}
