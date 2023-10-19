---
title: "字面值和操作符简介"
date: 2023-10-09T20:06:10+08:00
---

***
## 字面值

考虑以下两个语句：

```C++
std::cout << "Hello world!";
int x { 5 };
```

"Hello world!" 和 "5" 是什么？它们是字面值。字面值（也称为字面值常量）是直接写在源代码中的固定值。

同变量一样，字面值也有值和类型。与变量（其值可以分别通过初始化和赋值来设置和更改）不同，字面值的值是固定的（5总是5）。
这就是为什么字面值被称为常量。

为了进一步理清字面值和变量之间的差异，让我们来看看个简短的程序：

```C++
#include <iostream>

int main()
{
    std::cout << 5 << '\n'; // 打印字面值

    int x { 5 };
    std::cout << x << '\n'; // 打印变量
    return 0;
}
```

在第5行，我们将值5打印到控制台。当编译器编译它时，将生成导致std::cout打印值5的代码。该值5被编译为可执行文件，可以直接使用。

在第7行，我们创建了一个名为x的变量，并用值5初始化它。编译器将生成将值5复制到给定给x的任何内存位置的代码。在第8行，当我们打印x时，编译器将生成std::cout获取x的内存位置（其值为5）并打印对应值的代码。

因此，两个输出语句执行相同的操作（打印值5）。但在字面值的情况下，可以直接打印值5。对于变量，必须从变量表示的内存中获取值5。

这也解释了为什么字面值是常量，而变量可以更改。字面值直接放在可执行文件中，可执行文件本身在创建后不能更改。变量的值放在内存中，并且可以在可执行文件运行时更改内存的值。

{{< alert success >}}
**关键点**

字面值是直接插入到源代码中的值。这些值通常直接出现在可执行代码中（除非它们被优化）。

对象和变量表示保存值的内存位置。这些值可以按需获取。

{{< /alert >}}

***
## 操作符

在数学中，运算是一个涉及零个或多个输入值（称为操作数）的数学过程，该过程产生新的值被称为输出值。要执行的特定操作由一个称为操作符的符号表示。

例如，我们知道2+3等于5。在这种情况下，文字2和3是操作数，符号 + 是操作符。

例如：

```C++
#include <iostream>

int main()
{
    std::cout << 1 + 2 << '\n';

    return 0;
}
```

在该程序中，字面值1和2是加号（+）操作符的操作数，该操作符产生输出值3。然后将该输出值打印到控制台。在C++中，输出值通常称为返回值。

您可能已经非常熟悉数学中常见的标准算术操作符，包括加法（+）、减法（-）、乘法（*）和除法（/）。在C++中，赋值（=）也是操作符，插入（<<）、提取（>>）和相等（==）也是操作符。虽然大多数操作符的名称都有符号（例如+、或==），但也有许多操作符是关键字（例如new、delete和throw）。

C++中的操作符有四种不同的操作数个数：

一元操作符作用于一个操作数。一元操作符的一个例子是-操作符。例如，给定-5，操作符 - 接受文本操作数5，并翻转其符号以产生新的输出值-5。

二元操作符作用于两个操作数（通常称为左操作数和右操作数，因为左操作数出现在操作符的左侧，而右操作数显示在操作符的右侧）。二元操作符的一个例子是+操作符。例如，给定3+4，操作符+取左操作数3和右操作数4，并应用数学加法来产生新的输出值7。插入（<<）和提取（>>）操作符是二元操作符，左侧采用std::cout或std::cin，右侧采用要输出的值或要输入的变量。

三元操作符作用于三个操作数。在C++（条件操作符）中只有一个，我们将在后面介绍。

零元操作符作用于零操作数。在C++（throw操作符）中也只有其中一个，我们稍后也将介绍它。

请注意，一些操作符具有多个含义，这取决于它们的使用方式。例如，操作符-有两种使用方式。它可以以一元形式用于反转数字的符号（例如，将5转换为-5，或反之亦然），也可以以二进制形式用于进行减法（例如，4-3）。

***
## 操作符链接

操作符可以链接在一起，以便一个操作符的输出可以用作另一个操作符的输入。例如，2*3+4，乘法操作符优先，并将左操作数2和右操作数3转换为返回值6（它成为加法操作符的左操作数）。接下来，执行加号操作符，并将左操作数6和右操作数4转换为新值10。

在深入研究操作符主题时，我们将更多地讨论操作符的执行顺序。现在，只需知道算术操作符的执行顺序与它们在标准数学中的执行顺序相同：首先是圆括号，然后是指数，然后是乘法和除法，然后是加法和减法。这种排序有时缩写为PEMDAS。

***
## 返回值和副作用

C++中的大多数操作符只使用它们的操作数来计算返回值。例如，-5产生返回值-5，2+3产生返回值5。有几个操作符不产生返回值（例如delete和throw）。我们稍后将介绍这些功能。

一些操作符具有其他行为。一个操作符（或函数），除了产生返回值之外，还有一些可观察的效果，称为有副作用。例如，当计算x=5时，赋值操作符具有将值5赋值给变量x的副作用。即使在操作符完成执行后，x的更改值也是可见的（例如，通过打印x的值）。std::cout << 5 会产生将5打印到控制台的副作用。我们可以观察到，即在std::cout << 5 完成执行后，5也已打印到控制台。

具有副作用的操作符通常用于产生对应的副作用，而不是用于获取这些操作符产生的返回值。

{{< alert success >}}
**对于高级读者**

对于我们主要为获取返回值调用的操作符（例如，操作符+或操作符*），它们的返回值通常是显而易见的（例如，操作数的和或积）。

对于我们主要针对其副作用调用的操作符（例如，操作符=或操作符<<），它们产生的返回值并不总是显而易见的。例如，您希望x=5具有什么返回值？

操作符=和操作符<<（用于将值输出到控制台时）都返回其左操作数。因此，x=5返回x，std::cout<<5返回std:∶cout。这样做是为了可以链接这些操作符。

例如，x=y=5计算为x=（y=5）。首先y=5将5赋值给y。然后，该操作返回y，然后可以将y赋值给x。

std::cout << "Hello" << "world" 的计算结果为（std::cout << "Hello"）<< "world"。这首先将“Hello”打印到控制台。该操作返回std::cout，然后可以使用它将“world！”打印到控制台。
{{< /alert >}}

***
{{< prevnext prev="/basic/chapter1/whitespace/" next="" >}}
空白字符
<--->

{{< /prevnext >}}