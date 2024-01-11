---
title: "函数参数简介"
date: 2023-10-09T20:06:10+08:00
---

上一课中，学习了让函数将值返回给函数调用者。创建在该程序中模块化getValueFromUser函数：

```C++
#include <iostream>

int getValueFromUser()
{
 	std::cout << "Enter an integer: ";
	int input{};
	std::cin >> input;  

	return input;
}

int main()
{
	int num { getValueFromUser() };

	std::cout << num << " doubled is: " << num * 2 << '\n';

	return 0;
}
```

然而，如果我们想将输出的处理也放到函数中，该怎么办？可以尝试这样的操作：

```C++
#include <iostream>

int getValueFromUser()
{
 	std::cout << "Enter an integer: ";
	int input{};
	std::cin >> input;  

	return input;
}

// 这个函数无法编译通过
void printDouble()
{
	std::cout << num << " doubled is: " << num * 2 << '\n';
}

int main()
{
	int num { getValueFromUser() };

	printDouble();

	return 0;
}
```

这无法编译通过，因为函数printDouble不知道标识符num是什么。或者我们可以尝试在函数printDouble() 中将num定义为变量：

```C++
void printDouble()
{
	int num{}; // 新增一行
	std::cout << num << " doubled is: " << num * 2 << '\n';
}
```

虽然这解决了编译器错误并使程序可编译，但程序仍然无法正常工作（它始终打印“0 doubled is：0”）。这里问题的核心是函数printDouble未访问到用户输入的值。

我们需要某种方法将变量num的值传递给函数printDouble，以便printDouple可以在函数体中使用该值。

***
## 函数参数

函数参数是函数头中定义的变量。函数参数的工作方式与函数内定义的变量几乎相同，但有一点不同：它们是用函数调用方提供的值初始化的。

函数参数在函数头中定义，它们放在函数名后面的括号之间，多个参数用逗号分隔。

下面是具有不同数量参数的函数的一些示例：

```C++
// 本函数无参数
// 不依赖调用函数的任何数据
void doPrint()
{
    std::cout << "In doPrint()\n";
}

// 本函数有一个参数x
// 调用函数需要提供一个值给x
void printValue(int x)
{
    std::cout << x  << '\n';
}

// 本函数有两个参数，x与y
// 调用函数需要提供两个值，分别给x与y
int add(int x, int y)
{
    return x + y;
}
```

参数是在进行函数调用时从调用方传递给函数的值：

```C++
doPrint(); // 没有参数
printValue(6); // 参数是6
add(2, 3); // 参数是2，3
```

请注意，调用时多个参数也由逗号分隔。

***
## 参数如何工作

调用函数时，函数的所有参数都被创建为变量，并且每个值都被复制到匹配的参数中。该过程称为传递值。

例如：

```C++
#include <iostream>

// 本函数有两个参数，x与y
// 调用函数需要提供两个值，分别给x与y
void printValues(int x, int y)
{
    std::cout << x << '\n';
    std::cout << y << '\n';
}

int main()
{
    printValues(6, 7); // 函数调用，传递6，7，分别给x和y

    return 0;
}
```

当使用参数6和7调用函数printValues时，将创建printValue的参数x并用值6初始化，创建printValues的参数y并用值7初始化。

运行结果输出：
```C++
6
7
```

请注意，调用时传递值的数量通常必须与函数参数的数量匹配，否则编译器将抛出错误。传递给函数的参数可以是任何有效的表达式（因为传递的本质上只是参数的初始值设定项，初始值设定值可以是任何合法的表达式的计算结果）。

***
## 修复问题代码

现在，可以修复课程顶部演示的程序：

```C++
#include <iostream>

int getValueFromUser()
{
 	std::cout << "Enter an integer: ";
	int input{};
	std::cin >> input;  

	return input;
}

void printDouble(int value) // 这个函数有一个value参数
{
	std::cout << value << " doubled is: " << value * 2 << '\n';
}

int main()
{
	int num { getValueFromUser() };

	printDouble(num);

	return 0;
}
```

在该程序中，变量num首先用用户输入的值初始化。然后，调用函数printDouble，并将num的值复制到函数printDouble的参数中。函数printDouble然后使用参数value的值。

***
## 使用函数的返回值作为参数

在上面的问题中，我们可以看到变量num仅使用一次，将函数getValueFromUser的返回值传输到函数printDouble调用的参数。

我们可以将上述示例稍微简化如下：

```C++
#include <iostream>

int getValueFromUser()
{
 	std::cout << "Enter an integer: ";
	int input{};
	std::cin >> input;  

	return input;
}

void printDouble(int value)
{
	std::cout << value << " doubled is: " << value * 2 << '\n';
}

int main()
{
	printDouble(getValueFromUser());

	return 0;
}
```

现在，我们直接使用函数getValueFromUser的返回值作为函数printDouble的参数！

尽管该程序更简洁（并且清楚地表明，用户读取的值将不用于其他用途），但您可能也会发现这种“紧凑语法”有点难以阅读。如果您更愿意使用上一个含变量的版本，也是可以的。

***
## 参数和返回值如何一起工作

通过同时使用参数和返回值，我们可以创建将数据作为输入的函数，对其进行一些计算，并将值返回给调用者。

下面是一个非常简单的函数的示例，该函数将两个数字相加，并将结果返回给调用者：

```C++
#include <iostream>

// add() 使用2个整数作为输入，返回它们的和
// x and y 的值由调用函数决定
int add(int x, int y)
{
    return x + y;
}

// main 函数没有参数
int main()
{
    std::cout << add(4, 5) << '\n'; // 4 和 5 被传递给add
    return 0;
}
```

执行从main的顶部开始。当计算add(4，5)时，调用函数add，参数x用值4初始化，参数y用值5初始化。

函数add中的return语句计算x+y以产生值9，然后将该值返回给main。然后将该值9发送到std::cout，以便在控制台上打印。

输出：

```C++
9
```

{{< img src="./ParametersReturn.webp" title="函数调用行为">}}

***
## 更多示例

让我们看一下更多的函数调用：

```C++
#include <iostream>

int add(int x, int y)
{
    return x + y;
}

int multiply(int z, int w)
{
    return z * w;
}

int main()
{
    std::cout << add(4, 5) << '\n'; //  add() x=4, y=5, x+y=9
    std::cout << add(1 + 2, 3 * 4) << '\n'; // add() x=3, y=12, x+y=15

    int a{ 5 };
    std::cout << add(a, a) << '\n'; // (5 + 5)

    std::cout << add(1, multiply(2, 3)) << '\n'; // 1 + (2 * 3)
    std::cout << add(1, add(2, 3)) << '\n'; // 1 + (2 + 3)

    return 0;
}
```

该程序生成输出：

```C++
9
15
10
7
6
```

main函数中第一个语句很简单。

在第二条语句中，参数是在传递之前进行求值的表达式。在这种情况下，1+2的计算结果为3，因此3被复制到参数x。3*4的计算结果是12，因此12被复制到了参数y。add（3，12）结果为15。

下一对语句也相对简单：

```C++
    int a{ 5 };
    std::cout << add(a, a) << '\n'; // (5 + 5)
```

在这种情况下，调用add()，其中a的值被复制到参数x和y中。由于a的值为5，因此add(a, a)=add(5, 5)，结果为值10。

让我们看一看这一组中的第一个棘手的语句：

```C++
    std::cout << add(1, multiply(2, 3)) << '\n'; // 1 + (2 * 3)
```

执行函数add时，程序需要确定参数x和y的值。x很简单，我们将整数1传递给x。要获得参数y的值，它需要首先计算multiply(2, 3)。程序调用multiply并初始化z=2和w=3，因此multiply(2, 3)返回整数值6。返回值6现在可以用于初始化add函数的y参数。add(1, 6)返回整数7，然后将其传递给std::cout进行打印。

更明确地说：add(1, multiply(2, 3))求值为add(1, 6)，计算为7

下面的语句看起来很棘手，因为add()的参数之一是另一个add()函数。

```C++
    std::cout << add(1, add(2, 3)) << '\n'; // 1 + (2 + 3)
```

但这种情况与前面的情况完全相同。add(2,3) 首先解析，返回值为5。现在它可以解析为add(1, 5)，它的计算结果为值6，该值被传递给std::cout以进行打印。

更明确地说：add(1, add(2, 3)) 求值为add(1, 5) => 求值为6

***
## 未使用的参数

在某些情况下，将遇到参数未被使用的函数。

举个小例子：

```C++
void doSomething(int count) // warning: 参数count未被使用
{
    // 函数体中没有用到 count
}

int main()
{
    doSomething(4);
}
```

就像未使用的局部变量一样，编译器可能会警告已定义但未使用的参数。

在函数定义中，函数参数的名称是可选的。因此，在函数参数需要存在但未在函数体中使用的情况下，可以简单地省略名称。没有名称的参数称为未命名参数：

```C++
void doSomething(int) // ok: 未命名参数
{
}
```

Google C++样式指南建议使用注释来记录未命名参数的名称：

```C++
void doSomething(int /*count*/)
{
}
```

{{< alert success >}}
**关键点**

如果简单地删除未使用的函数参数，则对该函数的任何现有调用都将变异失败（因为函数调用将提供比函数可以接受的更多的参数）。

{{< /alert >}}

***
## 结论

函数参数和返回值是让函数可重用的关键机制，不必知道预先的输入，我们可以给出对应的计算结果。

***

{{< prevnext prev="/basic/chapter2/func-ret-void/" next="/basic/chapter2/local-var/" >}}
2.2 无返回值函数
<--->
2.4 局部变量
{{< /prevnext >}}
