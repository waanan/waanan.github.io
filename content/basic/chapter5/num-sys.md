---
title: "数字系统（十进制、二进制、十六进制和八进制）"
date: 2023-11-28T13:19:42+08:00
---

在日常生活中，我们使用十进制数进行计数，其中每个数字可以是0、1、2、3、4、5、6、7、8或9。十进制也称为“基数10”，因为有10个可能的数字（0到9）。在这个系统中，我们这样计数：0、1、2、3、4、5、6、7、8、9、10、11……默认情况下，C++程序中的数字假设为十进制。

```C++
int x { 12 }; // 12 默认是十进制
```

在二进制中，只有2个数字：0和1，因此它被称为“基数2”。在二进制中，我们这样计数：0，1，10，11，100，101，110，111…

十进制和二进制是数字系统的两个例子。C++中有4种主要的数字系统。按流行程度排序，它们是：十进制（以10为基数）、二进制（以2为基数），十六进制（以16为基数）和八进制（以8为基数）。

{{< alert success >}}
**注**

本节是可选的。

以后的少量课程将出现十六进制数，因此在继续之前，您至少应该对该概念有一个大致的熟悉。

{{< /alert >}}

***
## 八进制和十六进制

八进制是以8为基数——也就是说，唯一可用的数字是：0、1、2、3、4、5、6和7。在八进制中，我们这样计数：0，1，2，3，4，5，6，7，10，11，12，…（注意：没有8和9，所以我们从7跳到10）。



要使用八进制文字，请在文字前面加上0（零）：

```C++
#include <iostream>

int main()
{
    int x{ 012 }; // 0 before the number means this is octal
    std::cout << x << '\n';
    return 0;
}
```

该程序打印：

为什么是10而不是12？因为默认情况下数字以十进制输出，12八进制=10十进制。

Octal几乎从未使用过，我们建议您避免使用它。

十六进制是以16为基数。在十六进制中，我们这样计数：0，1，2，3，4，5，6，7，8，9，A，B，C，D，E，F，10，11，12…

要使用十六进制文本，请在文本前面加上0x。

```C++
#include <iostream>

int main()
{
    int x{ 0xF }; // 0x before the number means this is hexadecimal
    std::cout << x << '\n';
    return 0;
}
```

该程序打印：

因为十六进制数字有16个不同的值，所以我们可以说一个十六进制数字包含4位。因此，可以使用一对十六进制数字来精确表示整个字节。

考虑值为0011 1010 0111 1111 1001 1000 0010 0110的32位整数。由于数字的长度和重复性，这不容易阅读。在十六进制中，相同的值为：3A7F 9826，这更简洁。因此，十六进制值通常用于表示内存地址或内存中的原始数据（其类型未知）。

***
## 二进制文字

在C++14之前，不支持二进制文本。然而，十六进制文本为我们提供了一种有用的解决方法（您可能仍然会在现有的代码库中看到）：

```C++
#include <iostream>

int main()
{
    int bin{};    // assume 16-bit ints
    bin = 0x0001; // assign binary 0000 0000 0000 0001 to the variable
    bin = 0x0002; // assign binary 0000 0000 0000 0010 to the variable
    bin = 0x0004; // assign binary 0000 0000 0000 0100 to the variable
    bin = 0x0008; // assign binary 0000 0000 0000 1000 to the variable
    bin = 0x0010; // assign binary 0000 0000 0001 0000 to the variable
    bin = 0x0020; // assign binary 0000 0000 0010 0000 to the variable
    bin = 0x0040; // assign binary 0000 0000 0100 0000 to the variable
    bin = 0x0080; // assign binary 0000 0000 1000 0000 to the variable
    bin = 0x00FF; // assign binary 0000 0000 1111 1111 to the variable
    bin = 0x00B3; // assign binary 0000 0000 1011 0011 to the variable
    bin = 0xF770; // assign binary 1111 0111 0111 0000 to the variable

    return 0;
}
```

在C++14中，可以通过使用0b前缀来使用二进制文本：

```C++
#include <iostream>

int main()
{
    int bin{};        // assume 16-bit ints
    bin = 0b1;        // assign binary 0000 0000 0000 0001 to the variable
    bin = 0b11;       // assign binary 0000 0000 0000 0011 to the variable
    bin = 0b1010;     // assign binary 0000 0000 0000 1010 to the variable
    bin = 0b11110000; // assign binary 0000 0000 1111 0000 to the variable

    return 0;
}
```

***
## 数字分隔符

由于长文本可能很难读取，C++14还增加了使用引号（'）作为数字分隔符的功能。

```C++
#include <iostream>

int main()
{
    int bin { 0b1011'0010 };  // assign binary 1011 0010 to the variable
    long value { 2'132'673'462 }; // much easier to read than 2132673462

    return 0;
}
```

还要注意，分隔符不能出现在值的第一个数字之前：

```C++
    int bin { 0b'1011'0010 };  // error: ' used before first digit of value
```

数字分隔符是纯视觉的，不会以任何方式影响文字值。

***
## 以十进制、八进制或十六进制输出值

默认情况下，C++以十进制输出值。然而，您可以通过使用std:：dec、std:∶oct和std::hex I/O操纵器来更改输出格式：

```C++
#include <iostream>

int main()
{
    int x { 12 };
    std::cout << x << '\n'; // decimal (by default)
    std::cout << std::hex << x << '\n'; // hexadecimal
    std::cout << x << '\n'; // now hexadecimal
    std::cout << std::oct << x << '\n'; // octal
    std::cout << std::dec << x << '\n'; // return to decimal
    std::cout << x << '\n'; // decimal

    return 0;
}
```

这将打印：

请注意，一旦应用，I/O操纵器将保持为将来的输出设置，直到再次更改。

***
## 输出二进制值

以二进制格式输出值有点困难，因为std:：cout没有内置此功能。幸运的是，C++标准库包含一个名为std:：bitset的类型，它将为我们完成这项工作（在<bitset>头中）。

要使用std:：bitset，我们可以定义一个std:∶bitset变量，并告诉std::bitset要存储多少位。位数必须是编译时间常量。可以用整数值（以任何格式，包括十进制、八进制、十六进制或二进制）初始化std:：bitset。

```C++
#include <bitset> // for std::bitset
#include <iostream>

int main()
{
	// std::bitset<8> means we want to store 8 bits
	std::bitset<8> bin1{ 0b1100'0101 }; // binary literal for binary 1100 0101
	std::bitset<8> bin2{ 0xC5 }; // hexadecimal literal for binary 1100 0101

	std::cout << bin1 << '\n' << bin2 << '\n';
	std::cout << std::bitset<4>{ 0b1010 } << '\n'; // create a temporary std::bitset and print it

	return 0;
}
```

这将打印：

在上述代码中，此行：

```C++
std::cout << std::bitset<4>{ 0b1010 } << '\n'; // create a temporary std::bitset and print it
```

用4位创建临时（未命名）std:：bitset对象，用二进制文字0b1010对其进行初始化，以二进制格式打印值，然后丢弃临时对象。

在C++20和C++23中，通过新的格式库（C++20）和打印库（C++23），我们有更好的选项：

```C++
#include <format> // C++20
#include <iostream>
#include <print> // C++23

int main()
{
    std::cout << std::format("{:b}\n", 0b1010); // C++20
    std::cout << std::format("{:#b}\n", 0b1010); // C++20

    std::print("{:b} {:#b}\n", 0b1010, 0b1010); // C++23

    return 0;
}
```

这将打印：

{{< alert success >}}
**相关内容**

我们在第O.1课中更详细地介绍了std:：bitset——通过std:∶bitset的位标志和位操作。

{{< /alert >}}

