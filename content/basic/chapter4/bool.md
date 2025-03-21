---
title: "布尔值（Boolean）"
date: 2023-10-09T20:06:10+08:00
---

在现实生活中，问题通常可以用“是”或“否”来回答。“苹果是水果吗？”是的。“你喜欢芦笋吗？”不喜欢。

现在考虑一个类似的说法，可以用“真”或“假”来回答：“苹果是水果”。这显然是真的。或者，“我喜欢芦笋”怎么样。绝对错误。

这类句子只有两种可能的结果：yes/true或no/false。如此常见，以至于许多编程语言都包含一种特殊的类型来处理它们。该类型称为布尔类型（注意：布尔（Boolean）在英语中大写，因为它是以其发明者乔治·布尔的名字命名的）。

***
## 布尔变量

布尔变量是只能有两个可能值的变量：true和false。

要声明布尔变量，我们使用关键字bool。

```C++
bool b;
```

要初始化布尔变量或将true或false值赋给布尔变量，我们使用关键字true和false。

```C++
bool b1 { true };
bool b2 { false };
b1 = false;
bool b3 {}; // 默认初始化成 false
```

正如一元减号运算符（-）可以用于使整数为负一样，逻辑NOT运算符（！）可以用于将布尔值从true翻转为false，或从false翻转为true：

```C++
bool b1 { !true }; // b1 初始化成 false
bool b2 { !false }; // b2 初始化成 true
```

布尔值实际上不是作为单词“true”或“false”存储在布尔变量中。相反，它们存储为整数：true变为整数1，false变为整数0。类似地，当计算布尔值时，它们实际上不会计算为“true”或“false”。它们的计算结果为整数0（false）或1（true）。因为布尔实际上存储整数，所以它们被认为是整型。

***
## 打印布尔值

打印布尔值时，std::cout打印0表示false，打印1表示true:

```C++
#include <iostream>

int main()
{
    std::cout << true << '\n'; // true 求值结果是 1
    std::cout << !true << '\n'; // !true 求值结果是 0

    bool b{false};
    std::cout << b << '\n'; // b 是 false, 求值结果是 0
    std::cout << !b << '\n'; // !b 是 true, 求值结果是 1
    return 0;
}
```

输出：

```C++
1
0
0
1
```

如果希望std::cout打印“true”或“false”，而不是0或1，则可以使用std::boolalpha。下面是一个示例：

```C++
#include <iostream>

int main()
{
    std::cout << true << '\n';
    std::cout << false << '\n';

    std::cout << std::boolalpha; // 以  true ， false 格式打印bool

    std::cout << true << '\n';
    std::cout << false << '\n';
    return 0;
}
```

将打印：

```C++
1
0
true
false
```

可以使用std::noboolalpha关闭。

***
## 整数到布尔转换

不能使用列表初始化，用整数初始化布尔值：

```C++
#include <iostream>

int main()
{
	bool b{ 4 }; // 错误: 发生数据范围舍入
	std::cout << b << '\n';
	
	return 0;
}
```

然而，在整数可以转换为布尔值的其它地方，整数0转换为false，任何其他整数转换为true。

```C++
#include <iostream>

int main()
{
	std::cout << std::boolalpha; // 以  true ， false 格式打印bool

	bool b1 = 4 ; // 拷贝初始化允许隐式的将 int 转成 bool
	std::cout << b1 << '\n';

	bool b2 = 0 ; // 拷贝初始化允许隐式的将 int 转成 bool
	std::cout << b2 << '\n';

	
	return 0;
}
```

这将打印：

```C++
true
false
```

注：bool b1 = 4; 可能会生成警告。如果是这样，则必须禁用 将警告视为错误 的规则才能编译。

***
## 输入布尔值

从std::cin获取输入的布尔值有时会难倒新程序员。

考虑以下程序：

```C++
#include <iostream>

int main()
{
	bool b{}; // 列表初始化默认为 false
	std::cout << "Enter a boolean value: ";
	std::cin >> b;
	std::cout << "You entered: " << b << '\n';

	return 0;
}
```

```C++
Enter a Boolean value: true
You entered: 0
```

等等，发生了什么？

结果表明，std::cin只接受布尔变量的两个输入：0和1（不是true或false）。任何其他输入都将导致std::cin读取失败但不报错。在这种情况下，由于我们输入了true，std::cin默默地失败了。失败的输入也将使变量归零，因此b的赋值也为false。因此，当std::cout打印b的值时，它打印0。

要允许std:：cin接受“false”和“true”作为输入，必须启用std::boolalpha选项：

```C++
#include <iostream>

int main()
{
	bool b{};
	std::cout << "Enter a boolean value: ";

	// 允许用户输入 'true' or 'false' 作为bool变量的值
	// 大小写敏感, True or TRUE 都不行
	std::cin >> std::boolalpha;
	std::cin >> b;

	std::cout << "You entered: " << b << '\n';

	return 0;
}
```

然而，当启用std:：boolalpha时，“0”和“1”将不再解释为布尔输入（它们都解析为“false”，就像任何非“true”输入一样）。

{{< alert success >}}
**警告**

启用std:：boolalpha将仅允许接受小写的“false”或“true”。不接受大写字母的输入。

{{< /alert >}}

***
## 布尔返回值

布尔值通常用作检查某些内容是否为真的函数的返回值。此类函数通常以单词is（例如isEqual）或has（例如hasCommonDivisor）开头命名。

考虑下面的例子：

```C++
#include <iostream>

// x与y相等返回true, 不然返回false
bool isEqual(int x, int y)
{
    return (x == y); // 操作符== ， x 等于y，返回true，否则返回false
}

int main()
{
    std::cout << "Enter an integer: ";
    int x{};
    std::cin >> x;

    std::cout << "Enter another integer: ";
    int y{};
    std::cin >> y;

    std::cout << std::boolalpha; // 以  true ， false 格式打印bool
    
    std::cout << x << " and " << y << " are equal? ";
    std::cout << isEqual(x, y) << '\n'; // isEqual返回true或false

    return 0;
}
```

下面是该程序两次运行的输出：

```C++
Enter an integer: 5
Enter another integer: 5
5 and 5 are equal? true
```

```C++
Enter an integer: 6
Enter another integer: 4
6 and 4 are equal? false
```

这是如何运行的？首先读取x和y的整数值。然后，计算表达式“isEqual（x，y）”。在第一次运行中，这导致对isEqual（5,5）的函数调用。在该函数中，计算5==5，生成值true。值true返回给调用者，由std::cout打印。在第二次运行中，对isEqual（6,4）的调用返回值false。

***

{{< prevnext prev="/basic/chapter4/float/" next="/basic/chapter4/if/" >}}
4.7 浮点数
<--->
4.9 if语句简介
{{< /prevnext >}}
