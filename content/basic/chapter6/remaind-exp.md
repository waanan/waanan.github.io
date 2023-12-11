---
title: "余数和指数"
date: 2023-12-07T13:09:17+08:00
---

***
## 余数运算符（operator%）

余数运算符（通常也称为模运算符）是在进行整数除法后返回余数的运算符。例如，7/4=1余数3。因此，7%4=3。另一个例子是，25/7=3余数4，因此25%7=4。余数运算符仅适用于整数操作数。

这对于测试一个数是否可以被另一个数整除（意味着在除法之后，没有余数）最有用：如果 x % y的计算结果为0，则我们知道x可以被y整除。

```C++
#include <iostream>

int main()
{
	std::cout << "Enter an integer: ";
	int x{};
	std::cin >> x;

	std::cout << "Enter another integer: ";
	int y{};
	std::cin >> y;

	std::cout << "The remainder is: " << x % y << '\n';

	if ((x % y) == 0)
		std::cout << x << " is evenly divisible by " << y << '\n';
	else
		std::cout << x << " is not evenly divisible by " << y << '\n';

	return 0;
}
```

下面是该程序的几个运行结果：

```C++
Enter an integer: 6
Enter another integer: 3
The remainder is: 0
6 is evenly divisible by 3
```

```C++
Enter an integer: 6
Enter another integer: 4
The remainder is: 2
6 is not evenly divisible by 4
```

现在，让我们尝试一个第二个数字大于第一个数字的示例：

```C++
Enter an integer: 2
Enter another integer: 4
The remainder is: 2
2 is not evenly divisible by 4
```

当第二个数字大于第一个数字时，第一个数字将是余数。

***
## 带负数的余数

余数运算符也可以处理负操作数。 x % y总是返回带x符号的结果。

运行上述程序：

```C++
Enter an integer: -6
Enter another integer: 4
The remainder is: -2
-6 is not evenly divisible by 4
```

```C++
Enter an integer: 6
Enter another integer: -4
The remainder is: 2
6 is not evenly divisible by -4
```

在这两种情况下，可以看到余数取第一个操作数的符号。

在第一个操作数可以为负的情况下，必须注意余数也可以为负。例如，您可能认为编写一个函数来返回数字是否为奇数，如下所示：

```C++
bool isOdd(int x)
{
    return (x % 2) == 1; // 当x是 -5 时判断错误
}
```

然而，当x是负奇数时，这将判断错误，例如-5，因为-5%2是-1，并且-1！=1

因此，如果要比较余数运算的结果，最好与0进行比较，因为0没有正数/负数问题：

```C++
bool isOdd(int x)
{
    return (x % 2) != 0; // 或者可以写成 return (x % 2)
}
```

{{< alert success >}}
**术语**

尽管运算符%通常被称为“模”或“模”运算符，但这可能会令人困惑，因为数学中的模，通常当一个（并且只有一个）操作数为负数时，产生与C++中的运算符%不同的结果。

例如，在数学中：
-21模4 = 3
-21余数4 = -1

因此，我们认为“余数”这个名称比“模”更准确地表示运算符%。

{{< /alert >}}

{{< alert success >}}
**最佳实践**

如果可能，最好将余数运算符（operator%）的结果与0进行比较。

{{< /alert >}}

***
## 指数运算符

您会注意到^运算符（在数学中通常用于表示指数）是C++中的逐位异或运算。C++不包含指数运算符。

要在C++中执行指数，请 #include <cmath> 标头，并使用 pow() 函数：

```C++
#include <cmath>

double x{ std::pow(3.0, 4.0) }; // 3的4次方
```

注意，函数pow() 的参数（和返回值）是double类型。由于浮点数中的舍入错误，pow() 的结果可能不精确（即使传递整数或整数）。

如果要进行整数求幂，最好使用自己的函数来完成。以下函数实现整数求幂（使用非直观的“平方求幂”算法以提高效率）：

```C++
#include <cassert> // for assert
#include <cstdint> // for std::int64_t
#include <iostream>

// note: exp 必须是非负整数
// note: 不执行越界检查
constexpr std::int64_t powint(std::int64_t base, int exp)
{
	assert(exp >= 0 && "powint: exp parameter has negative value");

	// 处理 base 为 0 的情况
	if (base == 0)
		return (exp == 0) ? 1 : 0;

	std::int64_t result{ 1 };
	while (exp > 0)
	{
		if (exp & 1)  // 如果exp 为奇数
			result *= base;
		exp /= 2;
		base *= base;
	}

	return result;
}

int main()
{
	std::cout << powint(7, 12) << '\n'; // 7 的 12 次方

	return 0;
}
```

结果：

```C++
13841287201
```

如果您不理解该函数的工作原理，请不要担心——您不需要理解它才能调用它。constexpr标记允许编译器在编译时计算该函数。

下面是上面检查溢出的指数函数的更安全版本：

```C++
#include <cassert> // for assert
#include <cstdint> // for std::int64_t
#include <iostream>
#include <limits> // for std::numeric_limits

// 一个更安全(但是稍慢) 的检查溢出的版本
// note: exp 必须是非负整数
// 如果发生越界，返回 std::numeric_limits<std::int64_t>::max()
constexpr std::int64_t powint_safe(std::int64_t base, int exp)
{
    assert(exp >= 0 && "powint_safe: exp parameter has negative value");

    // 处理 base 为 0 的情况
    if (base == 0)
        return (exp == 0) ? 1 : 0;

    std::int64_t result { 1 };

    // 为了确保越界更简单，将base调转为正数
    // 在返回结果时，再补上符号
    bool negativeResult{ false };

    if (base < 0)
    {
        base = -base;
        negativeResult = (exp & 1);
    }

    while (exp > 0)
    {
        if (exp & 1) // 如果exp 为奇数
        {
            // 检查结果是否会溢出
            if (result > std::numeric_limits<std::int64_t>::max() / base)
            {
                std::cerr << "powint_safe(): result overflowed\n";
                return std::numeric_limits<std::int64_t>::max();
            }

            result *= base;
        }

        exp /= 2;

        // 处理完成
        if (exp <= 0)
            break;

        // 需要继续迭代，则继续执行检查

        // 检查结果是否会溢出
        if (base > std::numeric_limits<std::int64_t>::max() / base)
        {
            std::cerr << "powint_safe(): base overflowed\n";
            return std::numeric_limits<std::int64_t>::max();
        }

        base *= base;
    }

    if (negativeResult)
        return -result;

    return result;
}
```

{{< alert success >}}
**警告**

在绝大多数情况下，整数求幂将溢出整数类型。这可能就是为什么这样的函数最初没有包含在标准库中。

{{< /alert >}}

***

{{< prevnext prev="/basic/chapter6/arithmetic-op/" next="/basic/chapter6/incre-decre/" >}}
6.1 算术运算符
<--->
6.3 自增/自减运算符和副作用
{{< /prevnext >}}
