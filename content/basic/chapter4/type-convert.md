---
title: "类型转换和static_cast简介"
date: 2023-10-09T20:06:10+08:00
---

***
## 隐式类型转换

考虑以下程序：

```C++
#include <iostream>

void print(double x) // 参数是 double 类型
{
	std::cout << x << '\n';
}

int main()
{
	print(5); // 但我们传递了一个int类型的数字

	return 0;
}
```

在上面的示例中，print() 函数有一个类型为double的参数，但调用方正在传入类型为int的值5。在这种情况下会发生什么？

在大多数情况下，C++将允许我们将一个基本类型的值转换为另一个基础类型。将值从一种类型转换为另一种类型的过程称为类型转换。因此，int参数5将被转换为双精度值5.0，然后复制到参数x中。print() 函数将打印该值，从而产生以下输出：

```C++
5
```

编译器在没有显式询问我们的情况进行的类型转换，称为隐式类型转换。正如上面的例子——我们没有明确地告诉编译器将整数值5转换为双精度值5.0。相反，该函数需要一个双精度值，我们传入一个整数。编译器将注意到不匹配，并隐式地将整数转换为双精度浮点数。

下面是一个类似的示例，其中我们的参数是int变量，而不是int值：

```C++
#include <iostream>

void print(double x) //  参数是 double 类型
{
	std::cout << x << '\n';
}

int main()
{
	int y { 5 };
	print(y); // y 是 int 类型的变量

	return 0;
}
```

这与上面的工作原理相同。int变量y（5）保存的值将转换为双精度值5.0，然后复制到参数x中。

***
## 类型转换会生成新值

即使被称为转换，类型转换实际上也不会更改转换前的值或类型。相反，要转换的值用作输入，并且转换产生目标类型的新值。

在上面的示例中，转换不会将变量y从int类型更改为double。相反，转换使用y（5）的值作为输入来创建新的双精度值（5.0）。然后将该双精度值传递给函数print。

{{< alert success >}}
**关键点**

类型转换从其它类型的值生成目标类型的新值。

{{< /alert >}}

***
## 隐式类型转换警告

虽然隐式类型转换对于大多数情况来说是OK的，但在少数情况下，它存在问题。考虑下面的程序，它类似于上面的示例：

```C++
#include <iostream>

void print(int x) // 参数是 int 类型
{
	std::cout << x << '\n';
}

int main()
{
	print(5.5); // warning: 传入了一个 double 值

	return 0;
}
```

在这个程序中，我们将print() 更改为采用int参数，函数调用现在传入双精度值5.5。与上面类似，编译器将使用隐式类型转换，以便将双精度值5.5转换为int类型的值，以便可以将其传递给函数print()。

与初始示例不同，当编译该程序时，编译器将生成关于可能丢失数据的某种警告。并且，如果您启用了“将警告视为错误”的选项，编译器将中止编译过程。

编译和运行时，此程序将打印以下内容：

```C++
5
```

请注意，尽管我们传入了值5.5，但程序打印了5。由于整数值不能保存分数，因此当双精度值5.5隐式转换为int时，分数部分将被删除，并且仅保留整数值。

由于将浮点值转换为整数值会导致删除分数部分，因此编译器在执行从浮点到整数值的隐式类型转换时将警告我们。即使我们传入不带分数分量的浮点值，编译器可能仍然会警告我们转换是不安全的。

{{< alert success >}}
**关键洞点**

某些类型转换始终是安全的（例如int到double），而其他类型转换可能会导致在转换过程中更改值（例如double到int）。不安全的隐式转换通常会生成编译器警告，或（在列表初始化的情况下）错误。

这是列表初始化是首选初始化形式的主要原因之一。列表初始化将确保在隐式类型转换时丢失值信息：

```C++
int main()
{
    double d { 5 }; // okay: int 转 double 安全
    int x { 5.5 }; // error: double 转 int 不安全

    return 0;
}
```

{{< /alert >}}

{{< alert success >}}
**相关内容**

隐式类型转换是一个很有意义的主题。在以后的课程中，我们将更深入地研究这个主题。

{{< /alert >}}

***
## 通过static_cast操作符进行显式类型转换

回到我们最近的print()示例，如果我们故意想将双精度值传递给采用整数的函数，关闭“将警告视为错误”只是让程序通过编译是一个坏主意，因为这样每次编译时都会有警告（我们将很快学会忽略），我们有可能忽视关于更严重问题的警告。

C++支持第二种类型转换方法，称为显式类型转换。显式类型转换允许我们（程序员）显式地告诉编译器将值从一种类型转换为另一种类型，并且我们对转换的结果承担全部责任（这意味着，如果转换导致值的丢失，则是我们的错）。

要执行显式类型转换，在大多数情况下，我们将使用static_cast操作符。语法看起来有点滑稽：

```C++
static_cast<新类型>(表达式)
```

static_cast从表达式中获取值作为输入，并返回转换为newtype指定的类型的值（例如int、bool、char、double）。

让我们使用static_cast更新之前的程序：

```C++
#include <iostream>

void print(int x)
{
	std::cout << x << '\n';
}

int main()
{
	print( static_cast<int>(5.5) ); // 显示的将 double 值 5.5 转换为 int

	return 0;
}
```

因为我们现在显式将双精度值5.5转换为int值，所以编译器不会在编译时生成关于可能丢失数据的警告（这意味着我们可以启用“将警告视为错误”）。

{{< alert success >}}
**关键点**

每当您看到使用尖括号（<>）的C++语法（不包括预处理器）时，尖括号之间的东西很可能是类型。这通常是C++处理需要参数化类型的代码的方式。

{{< /alert >}}

{{< alert success >}}
**相关内容**

C++支持其他类型的强制转换。在以后的课程中，我们将详细讨论不同类型的类型转换——显式类型转换（casting）和static_cast。

{{< /alert >}}

***
## 使用static_cast将char转换为int

在前面关于字符串的课程中，我们看到使用std::cout打印char值会打印为字符：

```C++
#include <iostream>

int main()
{
    char ch{ 97 }; // 97 是 ASCII 码 'a'
    std::cout << ch << '\n';

    return 0;
}
```

这将打印：

```C++
a
```

如果要打印整数值而不是char，可以使用static_cast将值从char转换为int：

```C++
#include <iostream>

int main()
{
    char ch{ 97 }; // 97 是 ASCII 码 'a'
    std::cout << ch << " has value " << static_cast<int>(ch) << '\n'; // 将 ch 转换为 int

    return 0;
}
```

这将打印：

```C++
a has value 97
```

值得注意的是，static_cast的参数作为表达式求值。当我们传入变量时，该变量被求值以产生值，然后该值被转换为新类型。变量本身不受类型转换的影响。在上面的例子中，变量ch仍然是一个char，即使在我们将其值转换为int之后，它仍然保持相同的值。

***
## 将无符号数字转换为有符号数字

要将无符号数字转换为有符号数字，还可以使用static_cast运算符：

```C++
#include <iostream>

int main()
{
    unsigned int u { 5 };
    int s { static_cast<int>(u) }; // 将变量 u 的值转换为 int

    std::cout << s << '\n';
    return 0;
}
```

static_cast操作符不执行任何范围检查，因此如果将值强制转换为超出表示范围的类型，则将导致未定义的行为。因此，如果无符号int的值大于有符号int可以容纳的最大值，则上述从无符号int到int的转换将产生不可预测的结果。

{{< alert success >}}
**警告**

如果要转换的值不适合新类型的范围，static_cast操作符将产生未定义的行为。

{{< /alert >}}

***
## std::int8_t和std::uint8_t的行为可能类似于字符，而不是整数

如 固定宽度整数和size_t 中所述，大多数编译器定义和处理std::int8_t和std::uint8_t（以及相应的快速和最小固定宽度类型），分别与有符号char和无符号char类型相同。现在我们已经介绍了字符是什么，我们可以证明这在哪里会有问题：

```C++
#include <cstdint>
#include <iostream>

int main()
{
    std::int8_t myInt{65};      // 初始化 myInt 为 65
    std::cout << myInt << '\n'; // 我们可能期望打印 65

    return 0;
}
```

因为std::int8_t将自己描述为int，所以您可能会被欺骗，认为上面的程序将打印整数值65。然而，在大多数系统上，该程序将改为打印A（将myInt视为字符）。然而，这并不确定（在某些系统上，它实际上可以打印65）。

如果要确保将std::int8_t或std::uint8_t对象视为整数，则可以使用static_cast将该值转换为整数：

```C++
#include <cstdint>
#include <iostream>

int main()
{
    std::int8_t myInt{65};
    std::cout << static_cast<int>(myInt) << '\n'; // 将会一直打印 65

    return 0;
}
```

在将std::int8_t视为字符的情况下，来自控制台的输入也可能导致问题：

```C++
#include <cstdint>
#include <iostream>

int main()
{
    std::cout << "Enter a number between 0 and 127: ";
    std::int8_t myInt{};
    std::cin >> myInt;

    std::cout << "You entered: " << static_cast<int>(myInt) << '\n';

    return 0;
}
```

该程序的示例运行：

```C++
Enter a number between 0 and 127: 35
You entered: 51
```

下面是正在发生的事情。当std::int8_t被视为字符时，我们的输入被解释为字符，而不是整数。所以当我们输入35时，我们实际上输入了两个字符，'3'和'5'。因为char对象只能包含一个字符，所以提取了'3'（'5'留在输入流中，以便以后可能的提取）。因为字符'3'具有ASCII码位51，所以值51存储在myInt中，然后我们将其打印为int。

相反，其他固定宽度类型将始终打印并作为整数值输入。

***
