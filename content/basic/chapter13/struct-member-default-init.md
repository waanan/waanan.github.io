---
title: "成员变量的默认初始化"
date: 2024-03-08T13:20:57+08:00
---

当定义结构体（或类）类型时，可以为每个成员提供默认的初始化值，作为类型定义的一部分。该过程称为非静态成员初始化，初始化值称为默认成员初始值设定项。

下面是一个示例：

```C++
struct Something
{
    int x;       // 无初始化值 (bad)
    int y {};    // 值初始化
    int z { 2 }; // 显示的默认值
};

int main()
{
    Something s1; // s1.x 未初始化, s1.y 是 0, s1.z 是 2

    return 0;
}
```

在上面的Something定义中，x没有默认值，y是默认初始化的值，z具有默认值2。如果用户在实例化类型为Something的对象时没有提供显式初始化值，则将使用这些默认值。

s1对象没有初始值设定项，因此s1的成员被初始化为其默认值。s1.x没有默认的初始值设定项，因此它保持未初始化状态。s1.y是默认情况下初始化的值，因此它获得值0。s1.z用值2初始化。

请注意，尽管我们没有为s1.z提供显式初始值设定项，但它被初始化为非零值，因为提供了默认值。

{{< alert success >}}
**对于高级读者**

CTAD（类模板参数推导--后续介绍）不能用于非静态成员初始化。

{{< /alert >}}

***
## 显式初始化值优先于默认值

列表初始化中的显式值始终优先于成员变量默认的初始化值。

```C++
struct Something
{
    int x;       // 无默认初始值 (不好)
    int y {};    // 值初始化
    int z { 2 }; // 显示设置初始值
};

int main()
{
    Something s2 { 5, 6, 7 }; // 使用显示初始值设置 s2.x, s2.y, 和 s2.z (不使用默认值)
   
    return 0;
}
```

在上述情况下，s2对每个成员变量都有显式的初始化值，因此根本不使用默认的成员初始值。这意味着s2.x、s2.y和s2.z分别初始化为值5、6和7。

***
## 存在默认值时，初始化列表中可以缺少初始化值

在上一课中，我们注意到，如果使用聚合初始化，但初始化值的数量小于成员变量的数量，则所有剩余的成员都将被值初始化。然而，如果为给定成员提供了默认初始值，则将改用该默认值初始化。

```C++
struct Something
{
    int x;       // 无默认初始值 (不好)
    int y {};    // 值初始化
    int z { 2 }; // 显示设置初始值
};

int main()
{
    Something s3 {}; // 值初始化 s3.x, 使用默认值初始化 s3.y 和 s3.z
   
    return 0;
}
```

在上面的例子中，s3是用空列表初始化的，因此缺少所有的初始值设定项。这意味着如果默认成员变量初始值设定项存在，则将使用它，否则将进行值初始化。因此，s3.x（没有默认的初始值）初始化为0，s3.y是默认初始化为零，而s3.z默认为值2。

***
## 重新审视初始化

如果使用初始化列表设置聚合类型的对象：

1. 如果存在显式初始化值，则使用该显式值。
2. 如果缺少初始值设定项，并且存在默认成员初始值设定项，则使用默认值。
3. 如果缺少初始值设定项，并且不存在默认成员初始值设定项，则会进行值初始化。


如果未使用初始化列表：

1. 如果存在默认成员初始值设定项，则使用默认值。
2. 如果不存在默认的成员初始值设定项，则该成员将保持未初始化状态。


成员始终按声明的顺序初始化。

下面的示例概括了所有可能性：

```C++
struct Something
{
    int x;       // 无默认初始值 (不好)
    int y {};    // 值初始化
    int z { 2 }; // 显示设置初始值
};

int main()
{
    Something s1;             // 未使用初始化列表: s1.x 未初始化, s1.y 和 s1.z 使用默认值
    Something s2 { 5, 6, 7 }; // 显示初始化列表: s2.x, s2.y, 和 s2.z 使用设置的值(未使用默认值)
    Something s3 {};          // 缺少初始值设定项: s3.x 值初始化, s3.y 和 s3.z 使用默认值
   
    return 0;
}
```

要注意的情况是s1.x。由于s1没有初始值设定项列表，并且x没有默认的成员初始值，因此s1.x保持未初始化状态（这不符合最佳实践，因为应该始终初始化变量）。

***
## 始终为成员提供默认值

为了避免未初始化成员的可能性，只需确保每个成员都有一个默认值（显式默认值或空的大括号对）。这样，无论是否提供初始值设定项列表，成员都将使用某些值进行初始化。

考虑以下结构体，它为所有成员都设置了默认值：

```C++
struct Fraction
{
	int numerator { }; // 应该使用 { 0 } , 但为了演示，这里使用值初始化
	int denominator { 1 };
};

int main()
{
	Fraction f1;          // f1.numerator 为 0, f1.denominator 为 1
	Fraction f2 {};       // f2.numerator 为 0, f2.denominator 为 1
	Fraction f3 { 6 };    // f3.numerator 为 6, f3.denominator 为 1
	Fraction f4 { 5, 8 }; // f4.numerator 为 5, f4.denominator 为 8

	return 0;
}
```

这里在所有情况下，成员变量都是初始化了的。

{{< alert success >}}
**最佳实践**

为所有成员提供默认值。这确保即使变量定义未使用初始值列表，也会初始化成员。

{{< /alert >}}

***
## 聚合的默认初始化与值初始化

回顾上述示例中的两行：

```C++
	Fraction f1;          // f1.numerator 为 0, f1.denominator 为 1
	Fraction f2 {};       // f2.numerator 为 0, f2.denominator 为 1
```

您会注意到，f1是默认初始化的，f2是值初始化的，但结果是相同的（numerator初始化为0，denominator初始化为1）。那么应该选择哪一个呢？

值初始化情况（f2）更安全，因为它将确保任何没有默认值的成员都被值初始化。

首选值初始化还有一个好处——它与初始化其他类型对象的方式一致。一致有助于防止错误。

也就是说，程序员对类类型使用默认初始化，而不是值初始化比较常见。部分是由于历史原因（因为值初始化直到C++11才引入），部分是因为存在某些的情况（对于非聚合），其中默认初始化可能效率更高（后面在构造函数中讲解）。

因此，在本教程中，不会强烈要求对结构和体类强制使用值初始化，但建议这样做。

{{< alert success >}}
**最佳实践**

对于聚合类型，首选值初始化（有空大括号），而不是默认初始化（没有大括号）。

{{< /alert >}}

***

{{< prevnext prev="/basic/chapter13/struct-init/" next="/basic/chapter13/struct-arg-ret/" >}}
13.5 结构体初始化
<--->
13.7 结构体作为函数的输入与输出
{{< /prevnext >}}
