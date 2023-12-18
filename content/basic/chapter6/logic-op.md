---
title: "逻辑运算符"
date: 2023-12-07T13:09:17+08:00
---

虽然关系（比较）运算符可以用于测试特定条件是真还是假，但它们一次只能测试一个条件。通常，我们需要知道多个条件是否同时为真。例如，为了检查我们是否中了彩票，我们必须比较选择的所有多个号码是否与中奖号码匹配。在有6个数字的彩票中，这将涉及6次比较。在其他情况下，我们需要知道多个条件中的任何一个是否为真。例如，如果我们生病了，或者我们太累了，或者如果我们中了彩票，所以我们决定今天不上班。这将检查3个条件中的任何一个是否为真。

逻辑运算符提供了测试多个条件的能力。

C++有3个逻辑运算符：

| 运算符 |  符号  |  使用形式 |  结果 |
|  ----  | ----  | ----  | ----  |
| 逻辑非 | ! | !x | x为true，返回false，x为false，返回true |
| 逻辑AND | && | x && y | x与y均为true，返回true，否则返回false  |
| 逻辑OR | \|\| | x \|\| y | x或y为true，返回true，否则返回false |

***
## 逻辑NOT

在前面章节，我们已经遇到了一元运算符——逻辑NOT。这里总结一下它的作用：

| 操作数 |  结果  |
|  ----  | ----  |
| true | false |
| false | true |

如果逻辑NOT的操作数为true，则结果为false。如果逻辑NOT的操作数为false，则结果为true。换句话说，逻辑NOT将布尔值进行翻转。

逻辑NOT通常用于条件表达式：

```C++
bool tooLarge { x > 100 }; // x > 100，则 tooLarge 为ture
if (!tooLarge)
    // do something with x
else
    // print an error
```

需要注意的一点是，逻辑NOT具有非常高的优先级。新手程序员通常会犯以下错误：

```C++
#include <iostream>

int main()
{
    int x{ 5 };
    int y{ 7 };

    if (!x > y)
        std::cout << x << " is not greater than " << y << '\n';
    else
        std::cout << x << " is greater than " << y << '\n';

    return 0;
}
```

该程序打印：

```C++
5 is greater than 7
```

这怎么可能呢？答案是，由于逻辑NOT运算符的优先级高于大于运算符，因此表达式 !x > y 实际计算为 (!x) > y。由于x是5，(!x) 的计算结果为0，0 > y为false，因此执行else语句！

编写上述代码段的正确方法是：

```C++
#include <iostream>

int main()
{
    int x{ 5 };
    int y{ 7 };

    if (!(x > y))
        std::cout << x << " is not greater than " << y << '\n';
    else
        std::cout << x << " is greater than " << y << '\n';

    return 0;
}
```

这样，将首先计算x>y，然后逻辑NOT将翻转布尔结果。

{{< alert success >}}
**最佳实践**

如果逻辑NOT旨在对其他运算符的结果进行操作，则其他运算符及其操作数需要括在括号中。

{{< /alert >}}

***
## 逻辑OR

逻辑OR运算符用于测试两个条件中的任何一个是否为真。如果左操作数的计算结果为true，或右操作数的求值结果为true，或两者都为true时，则逻辑or运算符返回true。否则将返回false。

| 左操作数 | 右操作数 | 结果 |
|  ----  | ----  | ----  |
| true | true | true |
| true | false | true |
| false | true | true |
| false | false | false |

例如，考虑以下程序：

```C++
#include <iostream>

int main()
{
    std::cout << "Enter a number: ";
    int value {};
    std::cin >> value;

    if (value == 0 || value == 1)
        std::cout << "You picked 0 or 1\n";
    else
        std::cout << "You did not pick 0 or 1\n";
    return 0;
}
```

在这种情况下，我们使用逻辑OR运算符来测试左条件（value==0）或右条件（value=1）是否为真。如果其中一个（或两个）都为true，则逻辑or运算符的计算结果为true，这意味着执行If语句。如果两者都不为true，则逻辑OR运算符的计算结果为false，这意味着执行else语句。

可以将多个逻辑OR语句串在一起：

```C++
if (value == 0 || value == 1 || value == 2 || value == 3)
     std::cout << "You picked 0, 1, 2, or 3\n";
```

新程序员有时会混淆逻辑OR运算符（||）和按位OR运算符（|）。尽管它们的名称中都有OR，但它们执行不同的功能。混淆它们可能会导致不正确的结果。

***
## 逻辑AND

逻辑AND运算符用于测试两个操作数是否都为true。如果两个操作数都为true，则逻辑AND返回true。否则，它返回false。

| 左操作数 | 右操作数 | 结果 |
|  ----  | ----  | ----  |
| true | true | true |
| true | false | false |
| false | true | false |
| false | false | false |

例如，我们可能想知道变量x的值是否在10和20之间。这实际上是两个条件：我们需要知道x是否大于10，以及x是否小于20。

```C++
#include <iostream>

int main()
{
    std::cout << "Enter a number: ";
    int value {};
    std::cin >> value;

    if (value > 10 && value < 20)
        std::cout << "Your value is between 10 and 20\n";
    else
        std::cout << "Your value is not between 10 and 20\n";
    return 0;
}
```

在这种情况下，我们使用逻辑AND运算符来测试左条件（值>10）和右条件（值<20）是否都为真。如果两者都为true，则逻辑AND运算符的计算结果为true并执行If语句。如果两者都不为真，或者只有一个为真，则逻辑AND运算符的计算结果为false，然后执行else语句。

与逻辑OR一样，您可以将许多逻辑AND语句串在一起：

```C++
if (value > 10 && value < 20 && value != 16)
    // do something
else
    // do something else
```

如果所有这些条件都为true，则将执行If语句。如果这些条件中的任何一个为false，则将执行else语句。

与逻辑OR和按位OR一样，新程序员有时会混淆逻辑AND运算符（&&）和按位AND运算符。

***
## 短路求值

为了使逻辑AND返回true，两个操作数的计算结果都必须为true。如果左操作数的计算结果为false，则不管右操作数的结果是true还是false，逻辑“AND”知道它必须返回false。在这种情况下，逻辑AND运算符将立即返回false，不计算右边的操作数！这称为短路求值。

类似地，如果逻辑OR的左操作数为true，则整个OR条件的计算结果必为true。

短路求值，是另一个可以说明为什么不应在复合表达式中使用导致副作用的运算符的例子。请考虑以下代码片段：

```C++
if (x == 1 && ++y == 2)
    // do something
```

如果x不等于1，则整个条件语句的结果必为false，因此++y不会被求值！因此，只有当x的计算结果为1时，y才会递增，这可能不是您想要的！

{{< alert success >}}
**警告**

短路计算可能会导致逻辑AND和逻辑OR不能计算右边的操作数。避免将具有副作用的表达式与这些运算符一起使用。

{{< /alert >}}

{{< alert success >}}
**关键点**

操作数可以以任何顺序求值的规则，逻辑OR和逻辑and运算符是一个例外，因为标准明确规定左操作数必须首先求值。

{{< /alert >}}

{{< alert success >}}
**对于高级读者**

只有这些运算符的内置版本才能执行短路求值。如果重载这些操作符以使它们与您自己的类型一起工作，则这些重载操作符将不会执行短路操作。

{{< /alert >}}

***
## 混合使用AND和OR

在同一表达式中混合使用逻辑AND和逻辑OR运算符通常是不可避免的，但这是一个充满潜在危险的领域。

因为逻辑AND和逻辑OR看起来像一对，所以许多程序员假设它们具有相同的优先级（就像加法/减法和乘法/除法）。然而，逻辑AND的优先级高于逻辑OR，因此逻辑AND运算符将在逻辑OR运算符之前计算（除非它们已被括号括起来）。

新手程序员通常会编写 value1 || value2 && value3 这样的表达式。由于逻辑“AND”具有更高的优先级，因此它的计算结果为 value1 ||（value2 && value3），而不是（value1 || value2）&& value3。如果假设从左到右执行（就像加法/减法或乘法/除法那样），将得到一个没有预料到的结果！

在同一表达式中混合逻辑AND和逻辑OR时，最好显式地用括号括起每个运算符及其操作数。这有助于防止优先级错误，使代码更易于阅读，并清楚地定义表达式的计算方式。例如，与其写 value1 && value2 || value3 && value4，不如写入（value1 && value2）||（value3 && value4）。

{{< alert success >}}
**最佳实践**

在单个表达式中混合逻辑AND和逻辑OR时，请显式地用括号括起每个操作，以确保它们计算您想要的结果。

{{< /alert >}}

***
## 德摩根定律

许多程序员也会犯这样的错误，认为 !(x && y) 与 !x && !y 相同.不幸的是，您不能以这种方式“分发”逻辑NOT。

德摩根定律告诉我们，在这些情况下：

+ !(x && y) 等于 !x || !y
+ !(x || y) 等于 !x && !y

换句话说，当您分发逻辑NOT时，还需要将逻辑AND翻转为逻辑OR，反之亦然！

当试图使复杂的表达式更容易阅读时，这有时是有用的。

***
## 逻辑异或（XOR）操作符在哪里？

逻辑异或是某些语言中提供的逻辑运算符，用于测试两个条件中只有一个为真：

| 左操作数 | 右操作数 | 结果 |
|  ----  | ----  | ----  |
| true | true | false |
| true | false | true |
| false | true | true |
| false | false | false |

C++不提供显式逻辑异或运算符（operator^是按位异或，而不是逻辑异或）。与逻辑OR或逻辑AND不同，逻辑XOR不能进行短路计算。因此，用逻辑OR和逻辑and运算符构造逻辑XOR运算符是一项挑战。

然而，当操作数为bool类型时，运算符 != 生与逻辑异或相同的结果：

因此，逻辑异或可以如下实现：

```C++
if (a != b) ... // a XOR b, 假定a与b是 bool
```

这可以扩展到多个操作数，如下所示：

```C++
if (a != b != c) ... // a XOR b XOR c, 假定a，b，c是 bool
```

如果操作数不是bool类型，运算符 != 实现的逻辑异或将无法按预期工作。

{{< alert success >}}
**对于高级读者**

如果需要一种与非布尔操作数一起使用的逻辑异或形式，可以将操作数static_cast为bool：

```C++
if (static_cast<bool>(a) != static_cast<bool>(b) != static_cast<bool>(c)) ... // a XOR b XOR c, 对于任何可以转换为bool的类型有效
```

然而，这有点冗长。下面的技巧（利用运算符 ! 可以隐式地将其操作数转换为bool的事实）也有效，并且更简洁：

```C++
if (!!a != !!b != !!c) // a XOR b XOR c, 对于任何可以转换为bool的类型有效
```

这两个方法都不是非常直观的，因此如果您使用它们，请添加合适的注释。

{{< /alert >}}

***
## 可选的运算符表示形式

C++中的许多运算符（如运算符 || ）的名称只是符号。从历史上看，并不是所有的键盘和语言标准都支持键入这些运算符所需的所有符号。因此，C++支持使用单词而不是符号的运算符的另一组关键字。例如，可以使用关键字 or 或来代替 ||。

在这里可以找到完整的列表。特别值得注意的是以下三个方面：

| 操作符 | 可替代的关键字 |
|  ----  | ----  |
| && | and |
| \|\| | or |
| ! | not |

这意味着以下内容等价：

```C++
std::cout << !a && (b || c);
std::cout << not a and (b or c);
```

虽然这些替代名称现在似乎更容易理解，但大多数有经验的C++开发人员更喜欢使用符号名称，而不是关键字名称。因此，我们建议学习和使用符号名称，因为这是在现有代码中使用的。

***

{{< prevnext prev="/basic/chapter6/relation-op/" next="/basic/chapter6/summary/" >}}
6.5 关系运算符和浮点比较
<--->
6.7 第六章总结
{{< /prevnext >}}
