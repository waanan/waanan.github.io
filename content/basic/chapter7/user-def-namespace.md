---
title: "自定义命名空间和作用域解析操作符"
date: 2023-12-18T16:52:52+08:00
---

在之前，我们介绍了命名冲突和命名空间的概念。提醒一下，当两个相同的标识符被引入同一作用域时，就会发生命名冲突，编译器无法决定使用哪个标识符。当这种情况发生时，编译器或链接器将产生错误，因为它们没有足够的信息来解决歧义。

{{< alert success >}}
**关键点**

随着程序变得越来愈大，标识符的数量增加，这反过来导致发生命名冲突的概率显著增加。由于给定范围中的每个名称都可能与同一范围中的其他名称发生潜在冲突，因此标识符的线性增加将导致潜在冲突的指数增加！这是在尽可能小的范围内定义标识符的关键原因之一。

{{< /alert >}}

让我们重新查看命名冲突的示例，然后展示如何使用名称空间来改进。在下面的示例中，foo.cpp和goo.cpp 是包含执行不同操作但具有相同名称和参数的函数的源文件。

foo.cpp：

```C++
// 这个 doSomething() 将参数相加
int doSomething(int x, int y)
{
    return x + y;
}
```

goo.cpp:

```C++
// 这个 doSomething() 将参数相减
int doSomething(int x, int y)
{
    return x - y;
}
```

main.cpp：

```C++
#include <iostream>

int doSomething(int x, int y); // 前向声明 doSomething

int main()
{
    std::cout << doSomething(4, 3) << '\n'; // 实际调用的是哪个 doSomething ?
    return 0;
}
```

如果该项目仅包含foo.cpp或goo.cpp之一（但不同时包含两者），则它将编译通过并运行，而不会发生意外。然而，将两者编译到同一个程序中，会将两个具有相同名称和参数的不同函数引入到同一作用域（全局作用域）中，这会导致命名冲突。因此，链接器将提示错误：

```C++
goo.cpp:3: multiple definition of `doSomething(int, int)'; foo.cpp:3: first defined here
```

请注意，此错误发生是因为重复定义，因此函数doSomething是否被调用并不重要。

解决此问题的一种方法是重命名其中一个函数，以便名称不再冲突。但这也需要更改所有函数被调用的位置，很麻烦，并且容易出错。避免冲突的更好方法是将函数放入自己的命名空间中。基于这个原因，标准库被移动到std命名空间中。

***
## 定义自己的命名空间

C++允许我们通过namespace关键字定义自己的命名空间。在程序中创建的命名空间称为用户定义命名空间。

命名空间的语法如下：

```C++
namespace 命名空间标识符
{
    // 命名空间中的内容
}
```

从namespace关键字开始，后面是名称空间的标识符（即命名空间的名称），然后是大括号，其中包含名称空间中的内容。

在历史上，命名空间名称一般不大写，许多样式指南仍然建议使用这种约定。

{{< alert success >}}
**对于高级读者**

首选以大写字母开头的命名空间名称的一些原因：

1. 通常以大写字母开头命名用户自定义的类型。在使用限定名（如Foo::x, 其中Foo可以是命名空间或class名）时，命名空间与用户自定义类型一致。
2. 有助于防止与系统提供的或库提供的小写名称发生命名冲突。
3. C++20标准文档使用这种样式。
4. C++核心指南文档使用这种风格。

{{< /alert >}}

这里建议以大写字母开始命名空间名称。然而，任何一种风格都应被视为可接受。

命名空间必须在全局范围内或在另一个命名空间内定义。与函数中内容缩进类似，命名空间的内容通常缩进一级。有时，您可能会看到在命名空间的右大括号后面放置了可选的分号。

下面使用名称空间重写上一示例：

foo.cpp：

```C++
namespace Foo // 定义了命名空间 Foo
{
    // doSomething() 在命名空间 Foo 中
    int doSomething(int x, int y)
    {
        return x + y;
    }
}
```

goo.cpp:

```C++
namespace Goo // 定义了命名空间 Goo
{
    // doSomething() 在命名空间 Goo 中
    int doSomething(int x, int y)
    {
        return x - y;
    }
}
```

现在，foo.cpp中的doSomething() 位于Foo命名空间中，goo.cpp中的doSomething() 位于Goo命名空间中。让我们看看重新编译程序时会发生什么。

main.cpp：

```C++
int doSomething(int x, int y); // 前向声明 doSomething

int main()
{
    std::cout << doSomething(4, 3) << '\n'; // 实际调用的是哪个 doSomething ?
    return 0;
}
```

答案是，我们现在得到另一个错误！

```C++
ConsoleApplication1.obj : error LNK2019: unresolved external symbol "int __cdecl doSomething(int,int)" (?doSomething@@YAHHH@Z) referenced in function _main
```

在这种情况下，程序可以编译通过（因为有前向声明），但链接器在全局命名空间中找不到doSomething的定义。这是因为两个 doSomething 都不在全局命名空间中！它们现在位于各自名称空间的范围内！

通过域解析操作符，有两种不同的方法，来告诉编译器要使用哪个版本的 doSomething()。

对于后面的示例，为了便于阅读，我们将示例代码放在同一文件中。


***
## 使用域解析操作符（ :: ）访问命名空间

在特定命名空间中查找标识符的最佳方法是使用域解析操作符（ :: ）。域解析操作符告诉编译器，应该在左侧操作数的范围内查找右侧操作数指定的标识符。

下面是一个使用域解析操作符,显式使用Foo命名空间中的 doSomething() 版本的示例：

```C++
#include <iostream>

namespace Foo // 定义了命名空间 Foo
{
    // doSomething() 在命名空间 Foo 中
    int doSomething(int x, int y)
    {
        return x + y;
    }
}

namespace Goo // 定义了命名空间 Goo
{
    // doSomething() 在命名空间 Goo 中
    int doSomething(int x, int y)
    {
        return x - y;
    }
}

int main()
{
    std::cout << Foo::doSomething(4, 3) << '\n'; // 使用的是命名空间 Foo 中的 doSomething
    return 0;
}
```

这会产生预期的结果：

```C++
7
```

如果想使用Goo中的 doSomething() ：

```C++
#include <iostream>

namespace Foo // 定义了命名空间 Foo
{
    // doSomething() 在命名空间 Foo 中
    int doSomething(int x, int y)
    {
        return x + y;
    }
}

namespace Goo // 定义了命名空间 Goo
{
    // doSomething() 在命名空间 Goo 中
    int doSomething(int x, int y)
    {
        return x - y;
    }
}

int main()
{
    std::cout << Goo::doSomething(4, 3) << '\n'; // 使用的是命名空间 Goo 中的 doSomething
    return 0;
}
```

这将产生以下结果：

```C++
1
```

域解析操作符非常有用，因为它允许我们显式地选择要查看的名称空间，因此没有潜在的歧义。我们甚至可以执行以下操作：

```C++
#include <iostream>

namespace Foo // 定义了命名空间 Foo
{
    // doSomething() 在命名空间 Foo 中
    int doSomething(int x, int y)
    {
        return x + y;
    }
}

namespace Goo // 定义了命名空间 Goo
{
    // doSomething() 在命名空间 Goo 中
    int doSomething(int x, int y)
    {
        return x - y;
    }
}

int main()
{
    std::cout << Foo::doSomething(4, 3) << '\n'; // 使用的是命名空间 Foo 中的 doSomething
    std::cout << Goo::doSomething(4, 3) << '\n'; // 使用的是命名空间 Goo 中的 doSomething
    return 0;
}
```

这将产生以下结果：

```C++
7
1
```

***
## 使用无名称前缀的域解析操作符

域解析操作符也可以在标识符之前使用，而不提供命名空间名称（例如 ::doSomething）。在这种情况下，在全局命名空间中查找标识符。

```C++
#include <iostream>

void print() // 这个 print() 在全局命名空间
{
	std::cout << " there\n";
}

namespace Foo
{
	void print() // 这个 print() 在 Foo 命名空间
	{
		std::cout << "Hello";
	}
}

int main()
{
	Foo::print(); // 调用 Foo 命名空间中的 print()
	::print();    // 调用 全局命名空间中的 print() (这里与只输入print()效果一样)

	return 0;
}
```

在上面的示例中，::print() 的执行方式与直接调用 print() 行为一致。因此，在这种情况下，使用域解析操作符是多余的。但下一个示例将展示一种情况，使用无名称前缀的域解析操作符可能很有用。

***
## 命名空间内的标识符解析

如果使用命名空间内的标识符，并且没有提供域解析，编译器将首先尝试在同一命名空间中查找匹配的声明。如果没有找到匹配的标识符，编译器将依次检查外围每个层级的命名空间，以查看是否找到匹配，直到检查全局命名空间。

```C++
#include <iostream>

void print() // 这个 print() 在全局命名空间
{
	std::cout << " there\n";
}

namespace Foo
{
	void print() // 这个 print() 在 Foo 命名空间
	{
		std::cout << "Hello";
	}

	void printHelloThere()
	{
		print();   // 调用 Foo 命名空间中的 print()
		::print(); // 调用 全局命名空间中的 print()
	}
}

int main()
{
	Foo::printHelloThere();

	return 0;
}
```

这将打印：

```C++
Hello there
```

在上面的示例中，第一次调用 print() 时未提供域解析。由于 print() 的使用是在Foo命名空间内，编译器将首先查看是否可以找到Foo::print() 的声明。存在一个，因此调用Foo::print() 。

注意，我们还使用了不带名称空间（ ::print() ）的形式，来调用全局命名空间中的 print() 函数。

***
## 命名空间中内容的前向声明

在前面的课程，我们讨论了如何使用头文件来传播前向声明。对于命名空间内的标识符，前向声明也需要在同一命名空间内：

add.h

```C++
#ifndef ADD_H
#define ADD_H

namespace BasicMath
{
    // 函数 add() 在命名空间 BasicMath 中
    int add(int x, int y);
}

#endif
```

add.cpp

```C++
#include "add.h"

namespace BasicMath
{
    // 函数 add() 定义在命名空间 BasicMath 中
    int add(int x, int y)
    {
        return x + y;
    }
}
```

main.cpp

```C++
#include "add.h" // for BasicMath::add()

#include <iostream>

int main()
{
    std::cout << BasicMath::add(4, 3) << '\n';

    return 0;
}
```

如果 add() 的前向声明没有放在命名空间BasicMath中，则 add() 将改为在全局命名空间中定义，编译器将告警，没有看到对 BasicMath::add(4, 3) 的调用函数的声明。如果函数 add() 的定义不在命名空间BasicMath内，则链接器将告警，找不到用于调用 BasicMath::add(4, 3) 的匹配定义。

***
## 单个命名空间可以存在多个文件中

在多个位置（跨多个文件或同一文件中的多个位置）声明命名空间块是合法的。命名空间中的所有声明都被视为命名空间的一部分。

circle.h:

```C++
#ifndef CIRCLE_H
#define CIRCLE_H

namespace BasicMath
{
    constexpr double pi{ 3.14 };
}

#endif
```

growth.h:

```C++
#ifndef GROWTH_H
#define GROWTH_H

namespace BasicMath
{
    // 常量 e 也是命名空间 BasicMath 的一部分
    constexpr double e{ 2.7 };
}

#endif
```

main.cpp:

```C++
#include "circle.h" // for BasicMath::pi
#include "growth.h" // for BasicMath::e

#include <iostream>

int main()
{
    std::cout << BasicMath::pi << '\n';
    std::cout << BasicMath::e << '\n';

    return 0;
}
```

结果完全符合预期：

```C++
3.14
2.7
```

标准库广泛使用了该功能。否则，整个标准库必须在单个头文件中定义！

请注意，此功能还意味着您可以将自己的定义添加到std命名空间。这样做在大多数情况下都会导致未定义的行为，因为std命名空间有一个特殊的规则，禁止从用户代码进行扩展。

{{< alert success >}}
**警告**

不要将自定义功能添加到std命名空间。

{{< /alert >}}

***
## 嵌套命名空间

命名空间可以嵌套在其他命名空间中。例如：

```C++
#include <iostream>

namespace Foo
{
    namespace Goo // Goo 命名空间 在 Foo 命名空间 中
    {
        int add(int x, int y)
        {
            return x + y;
        }
    }
}

int main()
{
    std::cout << Foo::Goo::add(1, 2) << '\n';
    return 0;
}
```

请注意，因为名称空间Goo在名称空间Foo内，所以访问add需要写为 Foo::Goo::add。

在C++17，嵌套命名空间也可以这样声明：

```C++
#include <iostream>

namespace Foo::Goo // Goo 命名空间 在 Foo 命名空间 中 (C++17 样式)
{
  int add(int x, int y)
  {
    return x + y;
  }
}

int main()
{
    std::cout << Foo::Goo::add(1, 2) << '\n';
    return 0;
}
```

这等价于前面的示例。

***
## 命名空间别名

由于在嵌套命名空间中键入变量或函数的限定名可能会很痛苦，C++允许您创建命名空间别名，这允许我们暂时将一长串命名空间缩短为较短的名称空间：

```C++
#include <iostream>

namespace Foo::Goo
{
    int add(int x, int y)
    {
        return x + y;
    }
}

int main()
{
    namespace Active = Foo::Goo; // active 现在指代 Foo::Goo

    std::cout << Active::add(1, 2) << '\n'; // 这等价于 Foo::Goo::add()

    return 0;
} // Active 别名这里失效
```

名称空间别名的一个很好的优点：如果您想要将 Foo::Goo 中的功能移动到不同的位置，您可以只更新 Active 这个别名以指代新的目标，而不必查找/替换Foo:∶Goo的每个实例。

```C++
#include <iostream>
 
namespace Foo::Goo
{
}

namespace V2
{
    int add(int x, int y)
    {
        return x + y;
    }
}
 
int main()
{
    namespace Active = V2; // active 现在指代 V2
 
    std::cout << Active::add(1, 2) << '\n'; // 这一行不用修改
 
    return 0;
}
```

值得注意的是，C++中的名称空间最初不是作为实现信息层次结构的方法设计的——它们主要是作为防止命名冲突。这一点的证据，请注意，整个标准库都位于单个命名空间 std:: 下（其中一些嵌套名称空间是较新的库功能）。一些较新的语言（如C#）在这方面与C++不同。

通常，应该避免深度嵌套的命名空间。

***
## 何时应使用命名空间

在应用程序中，命名空间可以用于将特定于应用程序的代码与可以重用的代码（例如，数学函数）分离开来。例如，物理函数和数学函数可以放在一个命名空间（例如，math::）。

当编写要分发给其他人的库或代码时，请始终将代码放在命名空间中。如果不遵守这个规则，则发生命名冲突的可能性很高。

***

{{< prevnext prev="/basic/chapter7/code-block/" next="/" >}}
7.0 代码块
<--->
主页
{{< /prevnext >}}
