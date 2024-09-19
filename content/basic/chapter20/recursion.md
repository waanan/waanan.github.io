---
title: "递归"
date: 2024-08-20T10:49:32+08:00
---

如果一个函数调用了自身，那么我们就说这里发生了递归。下面是一个编写得不好的递归函数的示例：

```C++
#include <iostream>

void countDown(int count)
{
    std::cout << "push " << count << '\n';
    countDown(count-1); // countDown() 递归的调用自身
}

int main()
{
    countDown(5);

    return 0;
}
```

当调用countDown(5)时，打印“push 5”，并调用countDown(4)。countDown(4)打印“push 4”并调用countDown(3)。countDown(3)打印“push 3”并调用countDown(2)。countDown(n)调用countDown(n-1)的序列无限重复，形成了无限的递归调用。

在上一节课中，我们了解到每个函数调用都会导致函数相关数据放在调用栈上。由于countDown()函数从不返回（它只是再次调用countDown()），因此该信息永远不会从栈中弹出！因此，在某个时刻，计算机将耗尽栈内存，导致栈溢出，程序将崩溃或终止。在作者的机器上，该程序在终止之前倒数到-11732！

{{< alert success >}}
**注**

尾调用是发生在函数尾部（结束）的函数调用。具有递归尾部调用的函数对于编译器来说相当容易优化为迭代（非递归）函数。如果编译器进行了这样的优化，上面示例的函数不会导致系统耗尽栈空间。如果您运行上面的程序，并且它永远运行不会终止，则很可能发生了这种情况。

{{< /alert >}}


***
## 递归终止条件

递归函数调用通常像普通函数调用一样工作。然而，上面的程序说明了递归函数最重要的区别：必须包含递归终止条件，否则它们将“永远”运行（实际上，直到调用栈耗尽内存）。递归终止是一种判断条件，当满足该条件时，将导致递归函数停止调用自身。

递归终止通常涉及使用if语句。下面是使用终止条件（和一些额外的输出）重新设计的函数：

```C++
#include <iostream>

void countDown(int count)
{
    std::cout << "push " << count << '\n';

    if (count > 1) // 终止判断
        countDown(count-1);

    std::cout << "pop " << count << '\n';
}

int main()
{
    countDown(5);
    return 0;
}
```

现在，当我们运行程序时，countDown() 将首先输出以下内容：

```C++
push 5
push 4
push 3
push 2
push 1
```

如果此时查看调用栈，您将看到以下内容：

```C++
countDown(1)
countDown(2)
countDown(3)
countDown(4)
countDown(5)
main()
```

由于终止条件，countDown(1)不调用countDow(0)——相反，“if语句”不执行，因此它打印“pop 1”，然后终止。此时，countDown(1)从栈中弹出，函数返回到countDow(2)。countDown(2)在调用countDown(1)结束后的点位恢复执行，因此它打印“pop 2”，然后终止。递归函数调用随后从栈中弹出，直到countDown的所有实例都被弹出。

因此，该程序整体的输出是：

```C++
push 5
push 4
push 3
push 2
push 1
pop 1
pop 2
pop 3
pop 4
pop 5
```

值得注意的是，“push”输出是按前向顺序发生的，因为它们发生在递归函数调用之前。“pop”输出以相反的顺序出现，因为它们发生在递归函数调用之后，因为函数正在从栈中弹出（这与它们放入的顺序相反）。

***
## 一个更有用的例子

我们已经讨论了递归函数调用的基本机制，那么来看一看另一个稍微更典型的递归函数：

```C++
// 计算 1 到 sumto 之和
// 如果是负数，返回 0
int sumTo(int sumto)
{
    if (sumto <= 0)
        return 0; // 判断非预期的输入 (终止条件)
    if (sumto == 1)
        return 1; // 正常输入时的基础情形 (终止条件)

    return sumTo(sumto - 1) + sumto; // 递归调用
}
```

让我们看看当用参数sumto=5调用这个函数时会发生什么。

```C++
sumTo(5) 被调用, 5 <= 1 是 false, return sumTo(4) + 5.
sumTo(4) 被调用, 4 <= 1 是 false, return sumTo(3) + 4.
sumTo(3) 被调用, 3 <= 1 是 false, return sumTo(2) + 3.
sumTo(2) 被调用, 2 <= 1 是 false, return sumTo(1) + 2.
sumTo(1) 被调用, 1 <= 1 是 true,  return 1.  遇到终止条件
```

现在，回退调用栈（在每个函数返回时将其从调用栈中弹出）：

```C++
sumTo(1) returns 1.
sumTo(2) returns sumTo(1) + 2, 结果 1 + 2 = 3.
sumTo(3) returns sumTo(2) + 3, 结果 3 + 3 = 6.
sumTo(4) returns sumTo(3) + 4, 结果 6 + 4 = 10.
sumTo(5) returns sumTo(4) + 5, 结果 10 + 5 = 15.
```

这样，比较容易看到我们正在将1到传入的值之间的数字相加。

因为递归函数比较难通过阅读代码来理解，所以好的注释特别重要。

注意，在上面的代码中，我们使用值sumto-1而不是--sumto进行递归。这样做是因为操作符--有副作用，并且在给定表达式中多次应用有副作用的变量将导致未定义的行为。使用sumto-1可以避免副作用，使sumto在表达式中多次使用是安全的。

***
## 递归算法

递归函数通常首先递归的找到问题的子集，然后通过解决子集问题，来聚合得到最终的结果。在上面的算法中，sumTo(value)首先求解sumTo(value-1)，然后将结果与value的值相加，以找到sumTo(value)的解。

在许多递归算法中，一些输入产生普通的输出。例如，sumTo(1)直接输出1，并且不会从进一步的递归中受益。这种直接得到输出的场景称为基本情况。基本情况充当算法的终止条件。通常可以通过考虑输入0、1、""或null的输出来识别基本情况。

***
## 斐波那契数

最著名的数学递归算法之一是斐波那契数列。斐波那契数列出现在自然界的许多地方，例如树木的分枝、贝壳的螺旋、菠萝的小果、未卷曲的蕨类叶子和松果的排列。

斐波那契数在数学上定义为：

```C++

f(n) =	0 if n = 0
        1 if n = 1
        f(n-1) + f(n-2) if n > 1
```

因此，编写一个（不是非常有效的）递归函数来计算第n个斐波那契数是相当简单的：

```C++
#include <iostream>

int fibonacci(int count)
{
    if (count == 0)
        return 0; // 基本情况
    if (count == 1)
        return 1; // 基本情况
    return fibonacci(count-1) + fibonacci(count-2);
}

// 计算和展示前13个斐波那契数列
int main()
{
    for (int count { 0 }; count < 13; ++count)
        std::cout << fibonacci(count) << ' ';

    return 0;
}
```

运行程序会产生以下结果：

```C++
0 1 1 2 3 5 8 13 21 34 55 89 144
```

***
## 记忆算法

上面的递归Fibonacci算法不是非常有效，部分原因是每次调用Fibonaci非基本情况都会导致两次以上的Fibonaci调用。这会产生指数数量的函数调用（事实上，上面的示例调用fibonacci()1205次！）。可以使用一些技术来减少所需的调用数量。可以通过缓存昂贵的函数调用的结果，以便在相同的输入发生时直接返回结果。

下面是递归斐波那契算法的记忆版本：

```C++
#include <iostream>
#include <vector>

// count 这里是 std::size_t ，以便访问 std::vector 容易点
int fibonacci(std::size_t count)
{
	// 使用 std::vector 去缓存计算的结果
	static std::vector results{ 0, 1 };

	// 如果算过，那么直接返回结果
	if (count < std::size(results))
		return results[count];

	// 否则进行计算
	results.push_back(fibonacci(count - 1) + fibonacci(count - 2));
	return results[count];   
}

// 计算和展示前13个斐波那契数列
int main()
{
	for (int count { 0 }; count < 13; ++count)
		std::cout << fibonacci(static_cast<std::size_t>(count)) << ' ';

	return 0;
}
```

这个记忆版本进行了35次函数调用，这比原始算法的1205要好得多。

***
## 递归与迭代

关于递归函数，经常被问到的一个问题是，“如果您可以迭代地执行许多相同的任务（使用for循环或while循环），为什么要使用递归函数？”。事实证明，您总是可以迭代地解决递归问题——然而，对于稍微复杂的问题，递归版本通常更易于编写（和阅读）。例如，虽然可以迭代地编写斐波那契函数，但这稍微困难一些！（试试看！）

迭代函数（那些使用for循环或while循环的函数）几乎总是比它们的递归对应函数执行效率更高。这是因为每次调用函数时，在推送和弹出栈帧时都会发生一定量的开销。迭代函数避免了这种开销。

这并不是说迭代函数总是更好的选择。有时，函数的递归实现非常干净，也很容易编写，因此为了可维护性的好处，产生一点额外的开销是非常值得的，特别是如果算法不需要递归太多次来找到解决方案。

通常，当满足以下大多数条件时，递归是一个不错的选择：

1. 递归代码的实现要简单得多。
2. 递归深度可以是有限的。
3. 该算法的迭代版本需要管理数据栈。
4. 这不是代码的性能关键部分。

如果递归算法更易于实现，则以递归方式先实现，有需要再以后优化为迭代算法。

***