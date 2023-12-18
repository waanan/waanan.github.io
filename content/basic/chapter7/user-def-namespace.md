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

C++允许我们通过namespace关键字定义自己的命名空间。在自己的程序中创建的命名空间通常称为用户定义的命名空间（尽管称它们为程序定义的命名空间更准确）。

命名空间的语法如下：

我们从namespace关键字开始，后面是名称空间的标识符，然后是大括号，其中包含名称空间的内容。

在历史上，命名空间名称没有大写，许多样式指南仍然建议使用这种约定。

我们建议以大写字母开始命名空间名称。然而，任何一种风格都应被视为可接受。

命名空间必须在全局范围内或在另一个命名空间内定义。与函数的内容很相似，命名空间的内容通常缩进一级。有时，您可能会看到在命名空间的右大括号后面放置了可选的分号。

下面是使用名称空间重写的上一示例中的文件的示例：

foo.cpp：

```C++
namespace Foo // define a namespace named Foo
{
    // This doSomething() belongs to namespace Foo
    int doSomething(int x, int y)
    {
        return x + y;
    }
}
```

goo.cpp:

```C++
namespace Goo // define a namespace named Goo
{
    // This doSomething() belongs to namespace Goo
    int doSomething(int x, int y)
    {
        return x - y;
    }
}
```

现在，foo.cpp中的doSomething（）位于foo命名空间中，goo.cpp.中的doSomething）位于goo命名空间中。让我们看看重新编译程序时会发生什么。

主.cpp：

```C++
int doSomething(int x, int y); // forward declaration for doSomething

int main()
{
    std::cout << doSomething(4, 3) << '\n'; // which doSomething will we get?
    return 0;
}
```

答案是，我们现在得到另一个错误！

在这种情况下，编译器满意（通过我们的前向声明），但链接器在全局命名空间中找不到doSomething的定义。这是因为我们的两个doSomething版本都不在全局命名空间中！它们现在位于各自名称空间的范围内！

有两种不同的方法可以通过范围解析操作符或使用语句（我们将在本章后面的课程中讨论）来告诉编译器要使用哪个版本的doSomething（）。

对于后面的示例，为了便于阅读，我们将示例分解为一个文件解决方案。

{{< alert success >}}
**对于高级读者**

首选以大写字母开头的命名空间名称的一些原因：

1. 通常以大写字母开头命名程序定义的类型。对程序定义的命名空间使用相同的约定是一致的（特别是在使用限定名（如Foo:：x）时，其中Foo可以是命名空间或类类型）。
2. 它有助于防止与其他系统提供的或库提供的小写名称发生命名冲突。
3. C++20标准文档使用这种样式。
4. C++核心指南文档使用这种风格。


{{< /alert >}}

***
## 使用范围解析运算符（：：）访问命名空间

告诉编译器在特定命名空间中查找标识符的最佳方法是使用范围解析操作符（：：）。范围解析操作符告诉编译器，应该在左侧操作数的范围内查找右侧操作数指定的标识符。

下面是一个使用范围解析操作符告诉编译器我们显式希望使用Foo命名空间中的doSomething（）版本的示例：

```C++
#include <iostream>

namespace Foo // define a namespace named Foo
{
    // This doSomething() belongs to namespace Foo
    int doSomething(int x, int y)
    {
        return x + y;
    }
}

namespace Goo // define a namespace named Goo
{
    // This doSomething() belongs to namespace Goo
    int doSomething(int x, int y)
    {
        return x - y;
    }
}

int main()
{
    std::cout << Foo::doSomething(4, 3) << '\n'; // use the doSomething() that exists in namespace Foo
    return 0;
}
```

这会产生预期的结果：

如果我们想使用Goo中的doSomething（）版本：

```C++
#include <iostream>

namespace Foo // define a namespace named Foo
{
    // This doSomething() belongs to namespace Foo
    int doSomething(int x, int y)
    {
        return x + y;
    }
}

namespace Goo // define a namespace named Goo
{
    // This doSomething() belongs to namespace Goo
    int doSomething(int x, int y)
    {
        return x - y;
    }
}

int main()
{
    std::cout << Goo::doSomething(4, 3) << '\n'; // use the doSomething() that exists in namespace Goo
    return 0;
}
```

这将产生以下结果：

范围解析操作符非常棒，因为它允许我们显式地选择要查看的名称空间，因此没有潜在的歧义。我们甚至可以执行以下操作：

```C++
#include <iostream>

namespace Foo // define a namespace named Foo
{
    // This doSomething() belongs to namespace Foo
    int doSomething(int x, int y)
    {
        return x + y;
    }
}

namespace Goo // define a namespace named Goo
{
    // This doSomething() belongs to namespace Goo
    int doSomething(int x, int y)
    {
        return x - y;
    }
}

int main()
{
    std::cout << Foo::doSomething(4, 3) << '\n'; // use the doSomething() that exists in namespace Foo
    std::cout << Goo::doSomething(4, 3) << '\n'; // use the doSomething() that exists in namespace Goo
    return 0;
}
```

这将产生以下结果：

***
## 使用没有名称前缀的范围解析运算符

范围解析操作符也可以在标识符之前使用，而不提供命名空间名称（例如：：doSomething）。在这种情况下，在全局命名空间中查找标识符（例如doSomething）。

```C++
#include <iostream>

void print() // this print() lives in the global namespace
{
	std::cout << " there\n";
}

namespace Foo
{
	void print() // this print() lives in the Foo namespace
	{
		std::cout << "Hello";
	}
}

int main()
{
	Foo::print(); // call print() in Foo namespace
	::print();    // call print() in global namespace (same as just calling print() in this case)

	return 0;
}
```

在上面的示例中，：：print（）的执行方式与我们在没有范围解析的情况下调用print（。因此，在这种情况下，使用范围解析操作符是多余的。但下一个示例将展示一种情况，其中没有名称空间的范围解析操作符可能很有用。

***
## 命名空间内的标识符解析

如果使用命名空间内的标识符，并且没有提供范围解析，编译器将首先尝试在同一命名空间中查找匹配的声明。如果没有找到匹配的标识符，编译器将依次检查每个包含的命名空间，以查看是否找到匹配，最后检查全局命名空间。

```C++
#include <iostream>

void print() // this print() lives in the global namespace
{
	std::cout << " there\n";
}

namespace Foo
{
	void print() // this print() lives in the Foo namespace
	{
		std::cout << "Hello";
	}

	void printHelloThere()
	{
		print();   // calls print() in Foo namespace
		::print(); // calls print() in global namespace
	}
}

int main()
{
	Foo::printHelloThere();

	return 0;
}
```

这将打印：

在上面的示例中，调用print（）时未提供范围解析。由于print（）的这种使用是在Foo命名空间内，编译器将首先查看是否可以找到Foo:：print（）的声明。由于存在一个，因此调用Foo:：print（）。

如果没有找到Foo:：print（），编译器将检查包含的命名空间（在本例中为全局命名空间），以查看它是否可以在那里匹配print（）。

注意，我们还使用了不带名称空间（：：print（））的范围解析操作符来显式调用print（。

***
## 命名空间中内容的前向声明

在第2.11课——头文件中，我们讨论了如何使用头文件来传播前向声明。对于命名空间内的标识符，这些转发声明也需要在同一命名空间内：

添加。小时

```C++
#ifndef ADD_H
#define ADD_H

namespace BasicMath
{
    // function add() is part of namespace BasicMath
    int add(int x, int y);
}

#endif
```

添加.cpp

```C++
#include "add.h"

namespace BasicMath
{
    // define the function add() inside namespace BasicMath
    int add(int x, int y)
    {
        return x + y;
    }
}
```

主.cpp

```C++
#include "add.h" // for BasicMath::add()

#include <iostream>

int main()
{
    std::cout << BasicMath::add(4, 3) << '\n';

    return 0;
}
```

如果add（）的前向声明没有放在命名空间BasicMath中，则add（。）将改为在全局命名空间中定义，编译器将抱怨它没有看到对BasicMath:：add（4，3）的调用的声明。如果函数add（）的定义不在命名空间BasicMath内，则链接器将抱怨它找不到用于调用BasicMath:：add（4，3）的匹配定义。

***
## 允许多个命名空间块

在多个位置（跨多个文件或同一文件中的多个位置）声明命名空间块是合法的。命名空间中的所有声明都被视为命名空间的一部分。

圆形.h：

```C++
#ifndef CIRCLE_H
#define CIRCLE_H

namespace BasicMath
{
    constexpr double pi{ 3.14 };
}

#endif
```

生长.h：

```C++
#ifndef GROWTH_H
#define GROWTH_H

namespace BasicMath
{
    // the constant e is also part of namespace BasicMath
    constexpr double e{ 2.7 };
}

#endif
```

主.cpp：

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

这完全符合您的预期：

标准库广泛使用了该功能，因为每个标准库头文件都在该头文件中包含的命名空间std块内包含其声明。否则，整个标准库必须在单个头文件中定义！

请注意，此功能还意味着您可以将自己的功能添加到std命名空间。这样做在大多数情况下都会导致未定义的行为，因为std命名空间有一个特殊的规则，禁止从用户代码进行扩展。

{{< alert success >}}
**警告**

不要将自定义功能添加到std命名空间。

{{< /alert >}}

***
## 嵌套命名空间

名称空间可以嵌套在其他名称空间中。例如：

```C++
#include <iostream>

namespace Foo
{
    namespace Goo // Goo is a namespace inside the Foo namespace
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

请注意，因为名称空间Goo在名称空间Foo内，所以我们将add访问为Foo:：Goo:：add。

由于C++17，嵌套命名空间也可以这样声明：

```C++
#include <iostream>

namespace Foo::Goo // Goo is a namespace inside the Foo namespace (C++17 style)
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

这相当于前面的示例。

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
    namespace Active = Foo::Goo; // active now refers to Foo::Goo

    std::cout << Active::add(1, 2) << '\n'; // This is really Foo::Goo::add()

    return 0;
} // The Active alias ends here
```

名称空间别名的一个很好的优点：如果您想要将Foo:：Goo中的功能移动到不同的位置，您可以只更新活动别名以反映新的目标，而不必查找/替换Foo:∶Goo的每个实例。

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
    namespace Active = V2; // active now refers to V2
 
    std::cout << Active::add(1, 2) << '\n'; // We don't have to change this
 
    return 0;
}
```

值得注意的是，C++中的名称空间最初不是作为实现信息层次结构的方法设计的——它们主要是作为防止命名冲突的机制设计的。作为这一点的证据，请注意，整个标准库都位于单个名称空间std:：下（其中一些嵌套名称空间用于较新的库功能）。一些较新的语言（如C#）在这方面与C++不同。

通常，应该避免深度嵌套的命名空间。

***
## 何时应使用命名空间

在应用程序中，名称空间可以用于将特定于应用程序的代码与以后可以重用的代码（例如，数学函数）分离开来。例如，物理函数和数学函数可以进入一个命名空间（例如，math:：）。另一种语言和本地化功能（例如Lang:：）。

当您编写要分发给其他人的库或代码时，请始终将代码放在命名空间中。在其中使用库的代码可能不遵循最佳实践——在这种情况下，如果库的声明不在名称空间中，则发生命名冲突的可能性很高。另一个优点是，将库代码放在命名空间中还允许用户使用编辑器的自动完成和建议功能来查看库的内容。
