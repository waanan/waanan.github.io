---
title: "固定宽度整数和size_t"
date: 2023-10-09T20:06:10+08:00
---

在前面关于整数的课程中，我们讨论了C++仅保证整数变量具有最小大小——但它们实际可能取值范围更大，这取决于具体的系统。

***
## 为什么整数变量的大小不固定？

简短的回答是，这可以追溯到C，当时计算机速度很慢，性能是最重要的。C选择故意将整数的大小保持为可修改状态，以便编译器实现者可以为int选择在目标计算机体系结构上性能最好的大小。

***
## 这不好吗？

按照现代标准，是的。作为一名程序员，必须处理具有不确定范围的类型有点可笑。

考虑int类型。int的最小大小是2个字节，但在现代架构上通常是4个字节。如果您假设int是4个字节，因为这是最有可能的，那么您的程序可能会在int实际上是2个字节的架构上发生错误行为（因为您可能将需要4个字节的值存储在2字节的变量中，这将导致溢出或未定义的行为）。如果假设int只有2个字节以确保最大兼容性，那么在int为4个字节的系统上，每个整数浪费2个字节，内存使用量加倍！

***
## 固定宽度整数

为了解决上述问题，C99定义了一组固定宽度的整数（在stdint.h头中），这些整数在任何体系结构上都保证大小相同。

这些定义如下：

|  类型 |  类别  |  范围 |
|  ----  | ----  | ----  |
| std::int8_t | 一字节有符号 | -128 to 127 |
| std::uint8_t | 一字节无符号 | 0 to 255 |
| std::int16_t | 两字节有符号 | -32,768 to 32,767 |
| std::uint16_t | 两字节无符号 | 0 to 65,535 |
| std::int32_t | 四字节有符号 | -2,147,483,648 to 2,147,483,647 |
| std::uint32_t | 四字节无符号 | 0 to 4,294,967,295 |
| std::int64_t | 八字节有符号 | -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807 |
| std::uint64_t | 八字节无符号 | 0 to 18,446,744,073,709,551,615 |

C++正式采用这些固定宽度的整数作为C++11的一部分。可以通过包含<cstdint>头来访问它们，它们在std命名空间中定义。下面是一个示例：

```C++
#include <cstdint> // 引入 固定宽度整数
#include <iostream>

int main()
{
    std::int16_t i{5};
    std::cout << i << '\n';
    return 0;
}
```

固定宽度整数有两个缺点。

首先，不能保证在所有架构上的固定宽度整数都是可以使用的。某些系统上不支持一些对应长度的整数，这会导致您的程序无法在此类架构上编译。然而，考虑到大多数现代架构已经标准化了8/16/32/64位变量，这不太可能是一个问题，除非您的程序需要移植到一些奇特的大型机或嵌入式平台。

其次，如果使用一个固定宽度的整数，在某些架构上它可能比更大的类型要运行的慢。例如，如果您需要一个保证为32位的整数，您决定使用std::int32_t，但您的CPU实际上可能在处理64位整数时更快。当然，您的CPU可以更快地处理给定类型，并不意味着您的程序总体上会更快——现代程序通常受到内存速度限制而不是CPU的限制，并且较大的内存占用可能导致程序比更快的CPU处理运行起来慢得多。如果不进行实际测量，很难知道这一点。

***
## 快速整数和至小整数

为了帮助解决上述缺点，C++还定义了两个可选整数集。

快速类型（std::int_fast#_t和std::uint_fast#_t）提供最快的有符号/无符号整数类型，宽度至少为#位（其中#=8、16、32或64）。例如，std::int_fast32_t将为您提供最快的有符号整数类型，该类型至少为32位。所谓最快，我们是指CPU可以最快地处理的整数类型。

至小类型（std::int_least#_t和std::uint_least#_t）提供宽度至少为#位的最小有符号/无符号整数类型（其中#=8、16、32或64）。例如，std::uint_least32_t将为您提供最小的无符号整数类型，该类型至少为32位。

下面是作者的Visual Studio（32位控制台应用程序）中的一个示例：

```C++
#include <cstdint> // 引入 固定宽度整数
#include <iostream>

int main()
{
	std::cout << "least 8:  " << sizeof(std::int_least8_t) * 8 << " bits\n";
	std::cout << "least 16: " << sizeof(std::int_least16_t) * 8 << " bits\n";
	std::cout << "least 32: " << sizeof(std::int_least32_t) * 8 << " bits\n";
	std::cout << '\n';
	std::cout << "fast 8:  " << sizeof(std::int_fast8_t) * 8 << " bits\n";
	std::cout << "fast 16: " << sizeof(std::int_fast16_t) * 8 << " bits\n";
	std::cout << "fast 32: " << sizeof(std::int_fast32_t) * 8 << " bits\n";

	return 0;
}
```

这产生了以下结果：

```C++
least 8:  8 bits
least 16: 16 bits
least 32: 32 bits

fast 8:  8 bits
fast 16: 32 bits
fast 32: 32 bits
```

您可以看到，std::int_least16_t是16位，而std::int_fast16_t实际上是32位。这是因为在作者的机器上，32位整数的处理速度比16位整数快。

然而，这些快速和最少的整数有自己的缺点：首先，没有多少程序员真正使用它们，缺乏熟悉性可能会导致错误。其次，快速类型可能会导致内存浪费，因为它们的实际大小可能大于其名称所指示的大小。最严重的是，由于快速/至小整数的大小可以变化，因此您的程序可能会在不同体系结构上表现出不同的行为。例如：

```C++
#include <cstdint> // 引入 固定宽度整数
#include <iostream>

int main()
{
    std::uint_fast16_t sometype { 0 };
    --sometype; // 有意的出发溢出

    std::cout << sometype << '\n';

    return 0;
}
```

根据std::uint_fast16_t是16、32还是64位，此代码将产生不同的结果。

在对应的架构上严格测试程序之前，很难知道您的程序在哪里可能无法按预期工作。

***
## std::int8_t和std::uint8_t的行为可能类似于字符，而不是整数

由于C++规范中的疏忽，大多数编译器定义和处理std::int8_t和std::uint8_t（以及相应的快速和至小固定宽度类型）分别与有符号char和无符号char类型相同。这意味着这些8位类型的行为可能（也可能不会）与其他固定宽度类型的行为不同，这可能会导致错误。这种行为依赖于系统，因此在一个体系结构上正确运行的程序可能无法在另一个体系架构上正确编译或运行。

在类型转换章节，我们会介绍对应的例子。

在存储整数值时，通常最好避免使用std::int8_t和std::uint8_t（以及相关的快速和最少类型），并改用std::int16_t或std::uint16_t。

{{< alert success >}}
**警告**

8位固定宽度整数类型通常被视为字符而不是整数值（这可能因系统而异）。在大多数情况下，首选16位固定宽度整数类型。

{{< /alert >}}

***
## 最佳实践

鉴于上述提到的各种利弊，目前没有使用固定宽度整数的最佳实践。

我们的立场是，正确比快速更好，编译时失败比运行时失败更好。因此，如果需要具有固定大小的整数类型，我们建议避免使用快速/至少类型，而使用固定宽度类型。

{{< alert success >}}
**最佳做法**

1. 当整数的大小无关紧要时，首选int（例如，int始终适合2字节有符号整数的范围）。例如，如果您要求用户输入他们的年龄，或者从1数到10，那么int是16位还是32位并不重要（将适合任何一种情况）。这将涵盖您可能遇到的绝大多数情况。
2. 存储需要保证范围的数量时，首选std::int#_t。
3. 当执行位操作或需要定义良好的环绕行为时，首选std::uint#_t。

尽可能避免以下情况：

1. 持有数量的无符号类型
2. 8位固定宽度整数类型
3. 快速和至小固定宽度类型
4. 任何编译器特定的固定宽度整数——例如，Visual Studio定义__int8、__int16等…

{{< /alert >}}

***
## 什么是std::size_t？

考虑以下代码：

```C++
#include <iostream>

int main()
{
    std::cout << sizeof(int) << '\n';

    return 0;
}
```

在作者的机器上，此命令打印：

```C++
4
```


很简单，对吧？我们可以推断操作符sizeof返回整数值——但该返回值是什么整数类型？一个int？一个short？答案是sizeof（以及许多返回大小或长度值的函数）返回类型为std::size_t的值。size_t定义为无符号整数类型，通常用于表示对象的大小或长度。

有趣的是，我们可以使用sizeof操作符（它返回类型为std::size_t的值）来请求std::size_t本身的大小：

```C++
#include <cstddef> // 引入 std::size_t
#include <iostream>

int main()
{
	std::cout << sizeof(std::size_t) << '\n';

	return 0;
}
```

在作者的系统上编译为32位（4字节）控制台应用程序，它打印：

```C++
4
```

std::size_t在许多不同的头文件中定义，<cstddef> 是最好的头文件，因为它包含的其他已定义标识符的数量最少。

就像整数的大小可以根据系统而变化一样，std::size_t的大小也会变化。std::size_t保证是无符号的，至少16位，但在大多数系统上，它将相当于应用程序的地址宽度。也就是说，对于32位应用程序，std::size_t通常是32位无符号整数，对于64位应用程序来说，std::size_t通常是64位无符号整型。

系统上可创建的最大对象的大小（以字节为单位）等于std::size_t可以容纳的最大值。如果要创建更大的对象，sizeof将无法返回其大小，因为它将超出std::size_t的范围。

因此，任何大小（以字节为单位）大于std::size_t的对象都被视为格式错误（并将导致编译错误）。

例如，4字节无符号整数类型的范围是0到4294967295。假设std::size_t的大小为4个字节。这意味着在这样的系统上可以创建的最大对象是4294967295个字节。

{{< alert success >}}
**旁白**

std::size_t的大小给对象的大小施加了严格的数学上限。在实践中，最大的可创建对象大小可能小于该值（可能明显如此）。

一些编译器将最大的可创建对象限制为std::size_t最大值的一半）。

同时其他因素也可能起作用，例如计算机有多少连续内存可供分配。

{{< /alert >}}

***