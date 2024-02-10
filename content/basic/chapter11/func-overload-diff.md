---
title: "被重载函数之间互相区分"
date: 2024-02-10T01:33:43+08:00
---

在上一课中介绍了函数重载的概念，它允许我们创建具有相同名称的多个函数，只要每个同名函数具有不同的参数类型（或者可以以其他方式区分函数）。

在本课中，我们将更仔细地看一看重载函数是如何区分的。未正确区分的重载函数将导致编译器报错。

***
## 如何区分重载函数

| 函数属性 |  是否用于区分  |  注 |
| ----  | ----  | ----  |
| 参数个数 | 是 |  |
| 参数类型 | 是 | 排除参数的类型别名，const限定符。但包含省略号 |
| 返回类型 | 否 | |

请注意，函数的返回类型不用于区分重载函数。我们稍后将对此进行更多讨论。

{{< alert success >}}
**对于高级读者**

对于类的成员函数，还应考虑其他函数级别限定符，包括 const ， volatile 以及 Ref 限定符。

例如，常量成员函数可以与其他相同的非常量成员函数区分开来（即使它们共享相同的参数集）。

{{< /alert >}}

***
## 基于参数个数的重载

只要每个重载函数具有不同数量的参数，就可以区分重载函数。例如：

```C++
int add(int x, int y)
{
    return x + y;
}

int add(int x, int y, int z)
{
    return x + y + z;
}
```

编译器可以很容易地区分，具有两个整数参数的函数调用应该是add(int, int)，而具有三个整数参数的函数调用应是add(int, int, int)。

***
## 基于参数类型的重载

只要每个重载函数的参数类型列表是不同的，就可以区分函数。例如，以下所有重载都是不同的：

```C++
int add(int x, int y); // 整数版本
double add(double x, double y); // 浮点数版本
double add(int x, double y); // 整数与浮点数混合版本
double add(double x, int y); // 整数与浮点数混合版本
```

由于类型别名（或typedef）不是不同的类型，因此使用类型别名的重载函数与使用原始类型的函数没有区别。例如，以下所有函数都无法区分（并将导致编译错误）：

```C++
typedef int Height; // typedef
using Age = int; // 类型别名

void print(int value);
void print(Age value); // 无法与 print(int) 区分
void print(Height value); // 无法与 print(int) 区分
```

对于通过值传递的参数，也不考虑const 限定符。因此，以下函数不被认为是有区别的：

```C++
void print(int);
void print(const int); // 无法与 print(int) 区分
```

{{< alert success >}}
**对于高级读者**

我们还没有介绍省略号，但省略号参数被认为是一种独特的参数类型：

```C++
void foo(int x, int y);
void foo(int x, ...); // 可以与 foo(int, int) 区分开
```

因此，对foo(4, 5)的调用将匹配foo(int, int)，而不是foo(int, ...)。

{{< /alert >}}

***
## 函数的返回类型不用于区分

在区分重载函数时，不考虑函数的返回类型。

考虑这样的情况，您希望编写一个返回随机数的函数，但需要一个返回int的版本，以及另一个返回double的版本。您可能会尝试这样做：

```C++
int getRandomValue();
double getRandomValue();
```

在Visual Studio 2019上，这会导致以下编译器错误：

```C++
error C2556: 'double getRandomValue(void)': overloaded function differs only by return type from 'int getRandomValue(void)'
```

这是有意义的。如果您是编译器，并且看到了以下语句：

```C++
getRandomValue();
```

您将调用两个重载函数中的哪一个？这无法区分清楚。

解决此问题的最佳方法是为函数指定不同的名称：

```C++
int getRandomInt();
double getRandomDouble();
```

{{< alert success >}}
**旁白**

这是一个有意的设计，因为它确保函数调用的行为可以独立于表达式的其余部分来确定，从而使理解复杂表达式变得简单得多。换句话说，我们总是可以仅基于函数调用中的参数来确定调用函数的哪个版本。如果返回值用于区分，那么我们就没有一种简单的语法方法来判断调用了函数的哪个重载——我们还必须理解返回值是如何使用的，这需要更多的分析。

{{< /alert >}}

***
## 类型签名

函数的类型签名（type signature）被定义为函数头中用于区分函数的部分。在C++中，这包括函数名、参数数量、参数类型和函数级限定符。它显然不包括返回类型。

***
## 名称修饰（Name mangling）

{{< alert success >}}
**旁白**

编译器编译函数时，它执行名称修饰，这意味着函数的编译结果的名称将根据各种标准（如参数的数量和类型）更改（“修饰”），以便链接器可以有唯一的名称来使用。

例如，某些原型为int fcn()的函数可能会编译为__fcn_v，而int fcn(int)可能编译为__fcn_i。因此，虽然在源代码中，两个重载函数共享一个名称，但在编译结果代码中，名称实际上是唯一的。

对于名称应该如何被修饰没有标准化，因此不同的编译器将产生不同的修饰后的名称。

{{< /alert >}}

***
