---
title: "第五章总结与测验"
date: 2023-11-28T13:19:42+08:00
---

***
## 章节回顾

常数是在程序执行期间不能更改的值。C++支持两种类型的常量：命名常量和文本。

命名常量是与标识符关联的常量值。常量变量是一种命名常量，与具有替换文本的类对象宏一样。

文字常量是与标识符无关的常量值。

其值不能更改的变量称为常量变量。const关键字可用于使变量成为常量。必须初始化常量变量。通过值传递或通过值返回时避免使用const。

类型限定符是应用于修改类型行为方式的类型的关键字。从C++23开始，C++仅支持const和volatile作为类型限定符。

常量表达式是可以在编译时计算的表达式。必须在运行时计算的表达式有时称为运行时表达式。

编译时常量是一个常量，其值在编译时已知。运行时常量是一个常量，其初始化值直到运行时才知道。

constexpr变量必须是编译时常量，并用常量表达式初始化。函数参数不能是constexpr。

文字是直接插入到代码中的值。文字具有类型，文字后缀可以用于从默认类型更改文字的类型。

幻数是一个字面意思不清楚或以后可能需要更改的字面值（通常是数字）。不要在代码中使用幻数。相反，请使用符号常量。

在日常生活中，我们用十进制数计数，十进制数有10个数字。计算机使用二进制，它只有2个数字。C++还支持八进制（以8为基数）和十六进制（以16为基数）。这些都是数字系统的例子，它们是用于表示数字的符号（数字）的集合。

条件运算符（？：）（有时也称为算术if运算符）是三元运算符（接受3个操作数的运算符）。给定形式为c的条件运算？x:y，如果条件c的计算结果为true，则将计算x，否则将计算y。条件运算符通常需要用括号括起来，如下所示：

1. 在复合表达式（具有其他运算符的表达式）中使用时，用圆括号括住整个条件运算符。
2. 为了可读性，如果条件包含任何运算符（函数调用运算符除外），请用括号括起来。


内联扩展是一个过程，其中函数调用被被调用函数定义中的代码替换。使用inline关键字声明的函数称为inline函数。

内联函数和变量有两个主要要求：

1. 编译器需要能够在使用函数的每个转换单元中看到内联函数或变量的完整定义（前向声明本身并不足够）。如果还提供了转发声明，则定义可以发生在使用点之后。
2. 内联函数或变量的每个定义都必须相同，否则将导致未定义的行为。


在现代C++中，术语inline已经演变为“允许多个定义”。因此，内联函数是允许在多个文件中定义的函数。C++17引入了内联变量，这些变量允许在多个文件中定义。

内联函数和变量对于仅标头库特别有用，这是一个或多个实现某些功能的标头文件（不包括.cpp文件）。

constexpr函数是一个函数，其返回值可以在编译时计算。要使函数成为constexpr函数，只需在返回类型之前使用constexpl关键字。Constexpr函数仅在需要常量表达式的上下文中使用时才保证在编译时求值。否则，它们可以在编译时（如果符合条件）或运行时进行计算。

常量函数是必须在编译时计算的函数。

Constexpr函数和consteval函数隐式内联。

字符串是用于表示文本（如名称、单词和句子）的连续字符的集合。字符串文本总是放在双引号之间。C++中的字符串字面值是C样式的字符串，它的类型很奇怪，很难使用。

string提供了一种简单、安全的处理文本字符串的方法。std:：string位于<string>头中。string的初始化和复制开销很大。

string_view提供对现有字符串（C样式字符串文本、std:：string或char数组）的只读访问，而不进行复制。正在查看已销毁的字符串的std:：string_view有时称为悬挂视图。当修改std:：string时，该std:∶string中的所有视图都将无效，这意味着这些视图现在无效。使用无效的视图（而不是重新验证它）将产生未定义的行为。

由于整个程序都存在C样式的字符串文本，因此可以将std:：string_view设置为C样式的string文本，甚至可以从函数中返回这样的std::string_view。

子字符串是现有字符串中的连续字符序列。

***
## 测验时间

问题#1

为什么命名常量通常比文字常量更好？

为什么const/constexpr变量通常比#定义的符号常量更好？

显示解决方案

问题#2

在以下代码中查找3个问题（影响4行）。

```C++
#include <cstdint> // for std::uint8_t
#include <iostream>

int main()
{
  std::cout << "How old are you?\n";

  std::uint8_t age{};
  std::cin >> age;

  std::cout << "Allowed to drive a car in Texas [";

  if (age >= 16)
    std::cout << "x";
  else
    std::cout << " ";

  std::cout << "]\n";

  return 0;
}
```

样本输出值

显示解决方案

问题#3

将const和/或constexpr添加到以下程序：

```C++
#include <iostream>

// gets height from user and returns it
double getTowerHeight()
{
	std::cout << "Enter the height of the tower in meters: ";
	double towerHeight{};
	std::cin >> towerHeight;
	return towerHeight;
}

// Returns height from ground after "seconds" seconds
double calculateHeight(double towerHeight, int seconds)
{
	double gravity{ 9.8 };

	// Using formula: [ s = u * t + (a * t^2) / 2 ], here u(initial velocity) = 0
	double distanceFallen{ (gravity * (seconds * seconds)) / 2.0 };
	double currentHeight{ towerHeight - distanceFallen };

	return currentHeight;
}

// Prints height every second till ball has reached the ground
void printHeight(double height, int seconds)
{
	if (height > 0.0)
		std::cout << "At " << seconds << " seconds, the ball is at height: " << height << " meters\n";
	else
		std::cout << "At " << seconds << " seconds, the ball is on the ground.\n";
}

void calculateAndPrintHeight(double towerHeight, int seconds)
{
	double height{ calculateHeight(towerHeight, seconds) };
	printHeight(height, seconds);
}

int main()
{
	double towerHeight{ getTowerHeight() };

	calculateAndPrintHeight(towerHeight, 0);
	calculateAndPrintHeight(towerHeight, 1);
	calculateAndPrintHeight(towerHeight, 2);
	calculateAndPrintHeight(towerHeight, 3);
	calculateAndPrintHeight(towerHeight, 4);
	calculateAndPrintHeight(towerHeight, 5);

	return 0;
}
```

显示解决方案

问题#4

std:：string和std:：string_view之间的主要区别是什么？

使用std:：string_view时会出现什么问题？

显示解决方案

问题#5

编写一个程序，询问两个人的姓名和年龄，然后打印哪个人年龄更大。

下面是程序一次运行的输出示例：

显示提示

显示解决方案

问题#6

完成以下程序：

```C++
#include <iostream>

// Write the function getQuantityPhrase() here

// Write the function getApplesPluralized() here

int main()
{
    std::cout << "Mary has " << getQuantityPhrase(3) << " " << getApplesPluralized(3) << ".\n";

    std::cout << "How many apples do you have? ";
    int numApples{};
    std::cin >> numApples;

    std::cout << "You have " << getQuantityPhrase(numApples) << " " << getApplesPluralized(numApples) << ".\n";
 
    return 0;
}
```

样本输出：

getQuantityPhrase（）应采用表示某物数量的单个int参数，并返回以下描述符：

1. 0=“否”
2. 1=“单个”
3. 2=“几个”
4. 3=“少量”
5. >3=“多”


getApplesPlural（）应采用表示苹果数量的单个int参数参数，并返回以下内容：

1. 1=“苹果”
2. 否则=“苹果”


此函数应使用条件运算符。

这两个函数都应该正确使用constexpr。

显示提示

显示解决方案

