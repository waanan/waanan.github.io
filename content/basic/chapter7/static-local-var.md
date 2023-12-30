---
title: "静态局部变量"
date: 2023-12-18T16:52:52+08:00
---

术语静态(static)是C++语言中最令人困惑的术语之一，很大程度上是因为static在不同的上下文中具有不同的含义。

在前面的课程中，我们介绍了全局变量具有静态存储期（static duration），这意味着它们在程序启动时创建，在程序结束时销毁。

我们还讨论了static关键字如何让全局标识符具有内部链接，这意味着标识符只能在定义它的文件中使用。

在本课中，我们将探索将static关键字应用于局部变量时的作用。

***
## 静态局部变量

通过前面的学习，我们知道局部变量在默认情况下具有自动存储期，这意味着它们在定义点创建，并在退出代码块时销毁。

对局部变量使用static关键字会将其存储期从自动存储期更改为静态存储期。这意味着现在在程序开始时创建变量，并在程序结束时销毁（就像全局变量一样）。因此，即使静态变量超出范围，它也将保留其值！

示例是显示自动存储期和静态存储期局部变量之间的差异的最简单方法。

自动存储期（默认）：

```C++
#include <iostream>

void incrementAndPrint()
{
    int value{ 1 }; // 自动存储期（默认
    ++value;
    std::cout << value << '\n';
} // value变量被销毁

int main()
{
    incrementAndPrint();
    incrementAndPrint();
    incrementAndPrint();

    return 0;
}
```

每次调用incrementAndPrint() 时，都会创建一个名为value的变量，并为其赋值1。incrementAndPrint() 将值递增为2，然后打印值2。当incrementAndPrint()完成运行时，变量离开作用域并被销毁。因此，该程序输出：

```C++
2
2
2
```

现在考虑这个程序的另一个版本，使用静态局部变量。这个程序和上面的程序之间的唯一区别是，通过使用static关键字，将局部变量从自动存储期更改为静态存储期:

```C++
#include <iostream>

void incrementAndPrint()
{
    static int s_value{ 1 }; // 使用static，将s_value变为静态存储期，该变量只会初始化一次
    ++s_value;
    std::cout << s_value << '\n';
} // s_value 没有被销毁，但不可再被访问，以为已经离开了作用域

int main()
{
    incrementAndPrint();
    incrementAndPrint();
    incrementAndPrint();

    return 0;
}
```

在该程序中，由于s_value声明为静态，因此它是在程序启动时创建的。

可以在程序启动时，将静态局部变量初始化为0或具有constexpr的值。

没有初始化或非constexpr初始化的静态局部变量在程序启动时以零初始化。首次遇到变量定义时，将重新初始化。之后的调用将跳过该定义，不会进行重新初始化。因为它具有静态存储期，所以未显式初始化的静态局部变量在默认情况下将被零初始化。

由于s_value具有constexpr初始值设定项1，因此将在程序启动时初始化s_value。

当s_value在函数末尾离开作用域时，它不会被销毁。每次调用函数incrementAndPrint() 时，s_value的值保持之前留下的值。因此，该程序输出：

```C++
2
3
4
```

就像使用“g_”为全局变量添加前缀一样，通常使用“s_”为静态（静态存储期）局部变量添加前缀。

静态存储期局部变量最常见的用途之一是用于唯一ID生成器。想象一个程序，其中有许多相似的对象（例如，一个游戏，其中您受到许多僵尸的攻击，或者一个模拟，其中您显示许多三角形）。如果在创建时为每个对象提供唯一的标识符，则可以更容易地区分对象以进行进一步调试。

使用静态存储期局部变量很容易生成唯一的ID号：

```C++
int generateID()
{
    static int s_itemID{ 0 };
    return s_itemID++; // 制作 s_itemID的拷贝, s_itemID加一, 返回拷贝的值
}
```

第一次调用此函数时，它返回0。第二次，它返回1。每次调用它时，它都会返回比上次调用它时高一的数字。可以将这些编号指定为对象的唯一ID。由于s_itemID是局部变量，因此它不能被其他函数“篡改”。

静态变量提供了全局变量的一些好处（它们在程序结束之前不会被销毁），同时将它们的可见性限制在代码块内。这使得它们更容易理解，使用起来也更安全，即使定期更改它们的值。

{{< alert success >}}
**最佳实践**

初始化静态局部变量。静态局部变量仅在第一次执行代码时初始化，而不是在后续调用中初始化。

{{< /alert >}}

***
## 静态局部常数

静态局部变量可以设置为const（或constexpr）。常量静态局部变量的一个很好的用途是当您有一个需要使用常量值的函数，但创建或初始化对象的成本很高（例如，您需要从数据库中读取值）。如果使用普通局部变量，则每次执行函数时都会创建和初始化该变量。使用const/constexpr静态局部变量，可以创建并初始化昂贵的对象一次，然后在调用函数时重用它。

***
## 不要使用静态局部变量来控制程序行为

考虑以下代码：

```C++
#include <iostream>

int getInteger()
{
	static bool s_isFirstCall{ true };

	if (s_isFirstCall)
	{
		std::cout << "Enter an integer: ";
		s_isFirstCall = false;
	}
	else
	{
		std::cout << "Enter another integer: ";
	}

	int i{};
	std::cin >> i;
	return i;
}

int main()
{
	int a{ getInteger() };
	int b{ getInteger() };

	std::cout << a << " + " << b << " = " << (a + b) << '\n';

	return 0;
}
```

该程序可能的执行结果：

```C++
Enter an integer: 5
Enter another integer: 9
5 + 9 = 14
```

这段代码做了它应该做的事情，但因为我们使用了静态局部变量，所以使代码更难理解。如果有人在没有读取getInteger()实现的情况下阅读main()中的代码，他们没有理由假设对getInteger()的两个调用执行了不同的操作。但这两个调用执行的操作确实不同，如果差异不仅仅是更改的提示，则可能会非常令人困惑。

假设我们要做一个加减法的计算器，以便输出如下所示：

```C++
Addition
Enter an integer: 5
Enter another integer: 9
5 + 9 = 14
Subtraction
Enter an integer: 12
Enter another integer: 3
12 - 3 = 9
```

我们可以尝试使用getInteger()来读取接下来的两个整数，就像我们对加法所做的那样。

```C++
int main()
{
  std::cout << "Addition\n";

  int a{ getInteger() };
  int b{ getInteger() };

  std::cout << a << " + " << b << " = " << (a + b) << '\n';

  std::cout << "Subtraction\n";

  int c{ getInteger() };
  int d{ getInteger() };

  std::cout << c << " - " << d << " = " << (c - d) << '\n';

  return 0;
}
```

但这行不通，输出是

```C++
Addition
Enter an integer: 5
Enter another integer: 9
5 + 9 = 14
Subtraction
Enter another integer: 12
Enter another integer: 3
12 - 3 = 9
```

（“Enter another integer”而不是“Enter an integer”）

getInteger() 不可重用，因为它具有内部状态（静态局部变量s_isFirstCall），无法从外部重置。尽管程序在第一次编写时工作得很好，但静态局部变量阻止我们以后重用该函数。

实现getInteger的更好方法是将s_isFirstCall作为参数传递。这允许调用者选择要打印的提示。

只有在整个程序中以及在程序的可预见未来，变量是唯一的，并且重置变量没有意义时，才应使用静态局部变量。

{{< alert success >}}
**最佳实践**

避免静态局部变量，除非该变量从不需要重置。

{{< /alert >}}

***

{{< prevnext prev="/basic/chapter7/share-const-global/" next="/basic/chapter7/scope-duration-linkage/" >}}
7.8 在多个文件中共享全局常量（使用内联变量）
<--->
7.10 作用域、存储期和链接摘要
{{< /prevnext >}}
