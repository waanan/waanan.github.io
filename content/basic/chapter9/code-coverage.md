---
title: "代码覆盖率"
date: 2024-01-17T13:13:14+08:00
---

在上一课中，我们讨论了如何编写和保存简单的测试。在本课中，将讨论编写哪些类型的测试有助于确保代码正确。

***
## 代码覆盖率

术语代码覆盖率用于描述在测试时执行程序的源代码量。有许多不同的度量用于代码覆盖率。在下面的部分中，我们将介绍几个有用和流行的方法。

***
## 语句覆盖率

术语语句覆盖率是指代码中由测试例程执行的语句的百分比。

考虑以下函数：

```C++
int foo(int x, int y)
{
    int z{ y };
    if (x > y)
    {
        z = x;
    }
    return z;
}
```

将调用该函数，foo(1，0)，将对该函数提供完整的语句覆盖，因为函数中的每个语句都将执行。

对于isLowerVowel()函数：

```C++
bool isLowerVowel(char c)
{
    switch (c) // 语句 1
    {
    case 'a':
    case 'e':
    case 'i':
    case 'o':
    case 'u':
        return true; // 语句 2
    default:
        return false; // 语句 3
    }
}
```

该函数将需要两次调用来测试所有语句，因为在同一个函数调用中无法到达语句2和3。

虽然100%语句覆盖率的目标是好的，但它通常不足以确保正确性。

***
## 分支覆盖率

分支覆盖率是指已执行的分支的百分比，每个可能的分支单独计数。if语句有两个分支——一个分支在条件为true时执行，另一个分支则在条件为false时执行（即使没有相应的else语句要执行）。switch语句可以有多个分支。

```C++
int foo(int x, int y)
{
    int z{ y };
    if (x > y)
    {
        z = x;
    }
    return z;
}
```

前面对foo(1，0) 的调用为我们提供了100%的语句覆盖率，并测试了x > y的用例，但这只给了我们50%的分支覆盖率。我们需要再调用一次foo(0，1)来测试if语句不执行的用例。

```C++
bool isLowerVowel(char c)
{
    switch (c)
    {
    case 'a':
    case 'e':
    case 'i':
    case 'o':
    case 'u':
        return true;
    default:
        return false;
    }
}
```

在isLowerVowel()函数中，需要两个调用来提供100%的分支覆盖率：一个（如isLowerVowel('a')）用于测试第一个情况，另一个（isLowerVowel('q')）测试default情况。多个case标签，对应同一个执行语句的情况，有一个case标签的测试用例就已足够--如果这个用例能正常工作，其它所有的并列的case标签都可以。

现在考虑以下函数：

```C++
void compare(int x, int y)
{
	if (x > y)
		std::cout << x << " is greater than " << y << '\n'; // 情况 1
	else if (x < y)
		std::cout << x << " is less than " << y << '\n'; // 情况 2
	else
		std::cout << x << " is equal to " << y << '\n'; // 情况 3
}
```

这里需要3个调用来获得100%的分支覆盖率：compare(1，0)测试第一个if语句的肯定用例。compare(0, 1)测试第一个if语句的否定用例和第二个if声明的肯定用例。compare(0, 0)测试第一个和第二个if语句的否定用例，并执行else语句。因此，可以说该函数通过3次调用进行了可靠的测试（略优于1.8千亿亿次）。

{{< alert success >}}
**最佳实践**

目标是代码的100%分支覆盖率。

{{< /alert >}}

***
## 循环覆盖率

循环覆盖率（非正式地称为0、1、2测试）表示，如果代码中有循环，则应确保它在迭代0次、1次和2次时正常工作。如果它在2次迭代的情况下正确工作，则它应该在大于2的所有迭代中正确工作。因此，这三个测试涵盖了所有可能性（因为循环不能执行负次数）。

考虑以下程序：

```C++
#include <iostream>

void spam(int timesToPrint)
{
    for (int count{ 0 }; count < timesToPrint; ++count)
         std::cout << "Spam! ";
}
```

要在该函数中正确测试循环，应该调用它三次：spam(0) 测试零次迭代用例，spam(1) 测试一次迭代用例，以及spam(2) 测试两次迭代用例。如果参数2有效，则参数n应该有效，其中n>2。

{{< alert success >}}
**最佳实践**

使用0、1、2测试来确保循环在不同的迭代次数下正确工作。

{{< /alert >}}

***
## 测试不同类别的输入

在编写接受参数的函数时，或者在接受用户输入时，考虑不同类别的输入会发生什么。在这种情况下，我们使用术语“类别”来表示具有类似特征的一组输入。

例如，如果我编写了一个函数来产生整数的平方根，那么用什么值来测试它是有意义的？您可能会从一些正常值开始，如4。但用0和负数进行测试也是一个好主意。

下面是类别测试的一些基本准则：

对于整数，请确保考虑了函数如何处理负值、零值和正值。如果可能，还应该检查溢出。

对于浮点数，请确保您考虑了函数如何处理具有精度问题的值（比预期稍大或稍小的值）。用于测试的双精度类型值，好的选择，例如0.1和-0.1（用于测试比预期稍大的数字，如果预期是0.000x）以及0.6和-0.6（用于测试略小于预期的数字，如果预期是xxxxx.yy）。

对于字符串，请确保您考虑了函数如何处理空字符串、含字母数字字符串、具有空格的字符串（前导、尾随和内部）以及全部为空格的字符串。

如果函数采用指针，也不要忘记测试nullptr（将在后续介绍）。

{{< alert success >}}
**最佳实践**

测试不同类别的输入值，以确保您的代码单元正确处理它们。

{{< /alert >}}

***

{{< prevnext prev="/basic/chapter9/intro/" next="/basic/chapter9/common-semantic-errors/" >}}
9.0 代码测试简介
<--->
9.2 常见的语义错误
{{< /prevnext >}}
