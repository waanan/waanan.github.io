---
title: "运算符优先级和结合性"
date: 2023-12-07T13:09:17+08:00
---

***
## 简介

本章建立在第1.8课的概念之上——字面值和操作符简介。快速回顾如下：

运算是一个涉及零个或多个输入值（称为操作数）的数学过程，该过程产生新的值称之为输出值。要执行的特定操作由运算符（通常是符号或符号对）表示。

例如，我们都知道2+3等于5。在这种情况下，文字2和3是操作数，符号+是对操作数应用数学加法以产生新值5的运算符。

在本章中，我们将讨论与运算符相关的主题，并探索C++支持的许多常见运算符。

***
## 复合表达式的求值

现在，让我们考虑一个复合表达式，例如4+2\*3。应该将其分组为(4+2)\*3（计算结果为18），还是4+(2\*3)（计算值为10）？使用普通的数学优先规则（乘法在加法之前），我们知道上面的表达式应该分组为4+(2\*3)，产生值10。但编译器如何知道呢？

为了计算表达式，编译器必须执行两项操作：

1. 在编译时，编译器必须解析表达式，并确定操作数如何与运算符分组。这是通过优先级和结合性规则来完成的，我们将稍后讨论。
2. 在编译时或运行时，计算操作数并执行操作以产生结果。


***
## 运算符优先级

为了帮助解析复合表达式，所有运算符都被分配了一个优先级。优先级较高的运算符首先与操作数分组。

从下面的表格中可以看出，乘法和除法（优先级5）的优先级高于加法和减法（优先级6）。因此，在加法和减法之前，乘法和除法将与操作数分组。换句话说，4 + 2 \* 3将被分组为4 + (2 \* 3)。

***
## 运算符结合性

考虑像7-4-1这样的复合表达式。应该将其分组为（7-4）-1，其计算结果为2，还是7-（4-1），其计算值为4？由于两个减法运算符具有相同的优先级，编译器不能单独使用优先级来确定应该如何对其进行分组。

如果表达式中具有相同优先级的两个运算符彼此相邻，则运算符的结合性告诉编译器是从左到右计算运算符，还是从右到左计算运算符。减法具有优先级6，优先级6中的运算符具有从左到右的结合性。因此，该表达式从左到右分组：（7-4）-1。

***
## 运算符优先级和结合性表

下表是一个参考图表，您可以在将来参考它来解决您遇到的任何优先级或结合性问题。

|  优先级/结合性 |  运算符  |  描述 |  模式 |
|  ----  | ----  | ----  | ----  |
| 1 L->R | :: | 全局命名空间（一元） | ::name |
|  | :: | 命名空间（二元） | class_name::member_name |
| 2 L->R | () | 括号 | (expression) |
| | () | 函数调用 | function_name(parameters) |
| | () | 初始化 | type name(expression) |
| | {} | 列表初始化 | type name{expression} |
| | type() | 类型转换 | new_type(expression) |
| | type{} | 类型转换 | new_type{expression} |
| | [] | 数组下标取值 | pointer[expression] |
| | . | 取对象成员 | object.member_name |
| | -> | 取对象指针的成员 | object_pointer->member_name |
| | ++ | 后自增 | lvalue++ |
| | –– | 后自减 | lvalue–– |
| | typeid | 运行时类型信息 |  typeid(type) or typeid(expression)|
| | const_cast | 去掉类型的const限定 | const_cast<type>(expression) |
| | dynamic_cast | 运行时类型转换 | dynamic_cast<type>(expression) |
| | reinterpret_cast | 强制类型转换 | reinterpret_cast<type>(expression) |
| | static_cast | 编译时类型转换 | static_cast<type>(expression) |
| | sizeof… | 获取模板打包的参数个数 | sizeof…(expression) |
| | noexcept | 编译时异常检查 | noexcept(expression) |
| | alignof | 获取类型对齐方式 | alignof(type) |
| 3 R->L | + | 一元加 | +expression |
| | - | 一元减 | -expression |
| | ++ | 前自增 | ++lvalue |
| | -- | 前自减 | ––lvalue |
| | ! | 逻辑非 | !expression |
| | not | 逻辑非 | not expression |
| | ~ | 按位取反 | ~expression |
| | (type) | c样式类型转换 | (new_type)expression |
| | sizeof | 求字节大小 | sizeof(type) or sizeof(expression) |
| | co_await | 异步Await调用 | co_await expression (C++20) |
| | & | 取对象地址 | &lvalue |
| | * | 解引用 | *expression |
| | new | 动态内存分配 | new type |
| | new[] | 动态数组内存分配 | new type[expression] |
| | delete | 动态内存回收 | delete pointer |
| | delete[] | 动态数组内存回收 | delete[] pointer |
| 4 L->R | ->* | 成员指针访问 | object_pointer->*pointer_to_member |
| | .* | 成员对象访问 | object.*pointer_to_member |
| 5 L->R | * | 乘 | expression * expression |
| | / | 除 | expression / expression |
| | %| 余数 | expression % expression |
| 6 L->R | + | 加 | expression + expression |
| | - | 减 | expression - expression |
| 7 L->R | << | 按位左移/插入 | expression << expression |
| | >> | 按位右移/提取 | expression >> expression |
| 8 L->R | <=> | 三向比较 | expression <=> expression |
| 9 L->R | < | 小于比较 | expression < expression |
| | <= | 小于等于比较 | expression <= expression |
| | > | 大于比较 | expression > expression |
| | >= | 大于等于比较 | expression >= expression |
| 10 L->R | == | 相等比较 | expression == expression |
| | != | 不相等比较 | expression != expression |
| 11 L->R | & | 按位 And | expression & expression |
| 12 L->R | ^ | 按位 XOR | expression ^ expression |
| 13 L->R | \| | 按位 OR | expression \| expression |
| 14 L->R | && | 逻辑 AND | expression && expression |
| | and | 逻辑 AND | expression and expression |
| 15 L->R | \|\| | 逻辑 OR | expression \|\| expression |
| | or | 逻辑 OR  | expression or expression |
| 16 R->L | throw | 抛出异常 | throw expression |
| | co_yield | Yield 表达式 (C++20) | co_yield expression |
| | ?: | 条件表达式 | expression ? expression : expression |
| | = | 赋值 | lvalue = expression |
| | *= | 乘赋值 | lvalue *= expression |
| | /= | 除赋值 | lvalue /= expression |
| | %= | 余数赋值 | lvalue %= expression |
| | += | 加赋值 | lvalue += expression |
| | -= | 减赋值 | lvalue -= expression |
| | <<= | 按位左移赋值 | lvalue <<= expression |
| | >>= | 按位右移赋值 | lvalue >>= expression |
| | &= | 按位And赋值 | lvalue &= expression |
| | \|= | 按位Or赋值 | lvalue \|= expression |
| | ^= | 按位Xor赋值 | lvalue ^= expression |
| 17 L->R | , | 逗号运算符 | expression, expression |

备注：

1. 优先级1是最高的优先级，级别17是最低的优先级。具有更高优先级的运算符首先对其操作数进行分组。
2. L->R表示从左到右的结合性。
3. R->L表示从右到左的结合性。


您应该已经认识了其中的几个运算符，例如+、-、*、/、（）和sizeof。然而，除非您有使用另一种编程语言的经验，否则您现在可能无法理解该表中的大多数运算符。我们将在本章中介绍其中的许多，其余的将在需要时介绍。

请注意，运算符<<处理按位左移和插入，而运算符>>处理按位右移和提取。编译器可以根据操作数的类型确定要执行的操作。

{{< alert success >}}
**Q： 指数运算符在哪里？**

C++不包含进行求幂的运算符（运算符^在C++代表按位XOR）。我们在——余数和指数中更多地讨论了指数运算。

{{< /alert >}}

***
## 圆括号

根据优先规则，4+2\*3将分组为4+（2\*3）。但如果我们实际上是指（4+2）\*3呢？就像在普通数学中一样，在C++中，我们可以根据需要显式地使用括号来设置操作数的分组。这是因为括号具有最高的优先级之一，所以括号内部的内容优先分组。

***
## 使用括号使复合表达式更容易理解

现在考虑类似x&&y||z的表达式。它的计算结果是 ( x && y ) || z 还是 x &&( y || z)？您可以在表中查找，并看到&&优先于||。但运算符和优先级太多了，很难记住它们。并且也不希望必须始终查表才能理解复合表达式的求值方式。

为了减少错误，并在不使用优先级表的情况下使代码更容易理解，最好用括号括住复合表达式。

一个好的经验法则是：除了加法、减法、乘法和除法之外，用圆括号括住所有内容。

上述最佳实践还有一个例外：具有单个赋值运算符（并且没有逗号运算符）的表达式不需要将赋值的右操作数包装在括号中。

例如：

```C++
x = (y + z + w);   // 不需要这样
x = y + z + w;     // ojat

x = ((y || z) && w); // 赋值运算符右侧不需要括住
x = (y || z) && w;   // okay

x = (y *= z); // 有多个赋值，使用括号扩住更加容易理解
```

赋值运算符具有低优先级（只有很少使用的逗号运算符的优先更低）。因此，只要只有一个赋值（没有逗号），我们就知道右侧操作数将在赋值之前完全求值。

{{< alert success >}}
**最佳实践**

使用括号来明确复合表达式应该如何计算（即使它们在技术上是不必要的）。

{{< /alert >}}

{{< alert success >}}
**最佳实践**

具有单个赋值运算符的表达式不需要将赋值的右操作数包装在括号中。

{{< /alert >}}

***
## 求值计算 （evaluation ）

C++标准使用术语求值（evaluation ）来表示在表达式中执行运算符以产生值。优先级和结合规则确定值计算的顺序。

例如，给定表达式4+2\*3，由于优先级规则，该组为4+（2\*3）。必须首先计算2\*3，以便结果值6可以用作运算符+的右操作数。

{{< alert success >}}
**关键点**

优先级和结合性规则确定求值（运算符）的顺序。

{{< /alert >}}

***
## 操作数和函数参数的求值顺序大多是未指定的

在大多数情况下，操作数和函数参数的求值顺序是未指定的，这意味着它们可以按任何顺序求值。

考虑以下表达式：

```C++
a * b + c * d
```

从上面的优先级和结合性规则中，我们知道该表达式将被分组，就像我们键入了：

```C++
(a * b) + (c * d)
```

如果a是1，b是2，c是3，d是4，则该表达式将始终计算值14。

然而，优先级和结合性规则仅告诉我们运算符和操作数是如何分组的，以及值计算发生的顺序。它们不会告诉我们计算操作数或子表达式的顺序。编译器可以自由地按任何顺序计算操作数a、b、c或d。编译器还可以自由地首先计算a\*b或c\*d。

对于大多数表达式，这是无关紧要的。在上面的示例表达式中，变量a、b、c或d的值是按哪个顺序计算并不重要：计算的值总是14。这里没有歧义。

考虑一下这个程序，它包含一个新的C++程序员经常犯的错误：

```C++
#include <iostream>

int getValue()
{
    std::cout << "Enter an integer: ";

    int x{};
    std::cin >> x;
    return x;
}

int main()
{
    std::cout << getValue() + (getValue() * getValue()) << '\n'; // a + (b * c)
    return 0;
}
```

如果运行该程序并输入输入1、2和3，则可以假设该程序将计算1+（2\*3）并打印7。但这是在假设对getValue() 的调用将按从左到右的顺序计算。编译器可以选择不同的顺序。例如，如果编译器选择从右到左的顺序，则程序将计算3+（2\*1），这将为相同的输入打印5。

通过将每个函数调用放在单独的语句，可以使上述程序变得明确：

```C++
#include <iostream>

int getValue()
{
    std::cout << "Enter an integer: ";

    int x{};
    std::cin >> x;
    return x;
}

int main()
{
    int a{ getValue() }; // 先执行
    int b{ getValue() }; // 第二个执行
    int c{ getValue() }; // 第三个执行
    
    std::cout << a + (b * c) << '\n'; // 求值顺序不在重要

    return 0;
}
```

{{< alert success >}}
**关键点**

操作数、函数参数和子表达式可以按任何顺序计算。

{{< /alert >}}

{{< alert success >}}
**警告**

确保表达式（或函数调用）不依赖于操作数（或参数）求值顺序。

{{< /alert >}}

{{< alert success >}}
**相关内容**

具有副作用的运算符也可能导致意外的求值结果。我们在第6.3节中讨论了这一点——递增/递减运算符和副作用。

{{< /alert >}}

***

