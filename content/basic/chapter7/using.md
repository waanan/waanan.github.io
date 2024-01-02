---
title: "using声明和using指令"
date: 2023-12-18T16:52:52+08:00
---

您可能在许多教科书和教程中见过该程序:

```C++
#include <iostream>

using namespace std;

int main()
{
    cout << "Hello world!\n";

    return 0;
}
```

一些旧的IDE还将使用类似的程序自动填充新的C++项目（因此您可以立即编译某些内容，而不是从空白文件开始）。

如果看到这个，说明您的教科书、教程或编译器可能已过时。在本课中，我们将探索原因。

***
## 一堂简短的历史课

在C++支持命名空间之前，在std命名空间中的所有名称都在全局命名空间中。这导致用户程序的标识符非常容易与标准库标识符之间发生命名冲突。在老C++版本下工作的程序可能与较新版本的C++发生命名冲突。

1995年，命名空间被标准化，标准库中的所有功能都被移出全局命名空间，移到命名空间std中。这一更改使那些没有使用std::前缀的旧代码无法编译。

任何研究过大型代码库的人都知道，对代码库的任何更改（无论多么微不足道）都有破坏程序的风险。将移动到std命名空间中的每个名称更新为使用std::前缀是一个巨大的风险。

快进到今天——如果您经常使用标准库，在每一个标准库的内中之前输入std::是一项重复且枯燥的事情，在某些情况下，可能会使代码更难阅读。

C++以using语句的形式为这两个问题提供了一些解决方案。

但首先，让我们定义两个术语。

***
## 限定与未限定的名称

名称可以是限定（qualified）的，也可以是不限定（unqualified.）的。

限定名是包含关联域的名称。通常，使用域解析操作符（::）用命名空间限定名称。例如:

```C++
std::cout // 标识符 cout 被限定在命名空间 std
::foo // 标识符 foo 被限定在全局命名空间
```

非限定名称是不包括域限定符的名称。例如，cout和x是非限定名称，因为它们不包括关联的作用域。

{{< alert success >}}
**对于高级读者**

名称也可以由类名限定，或者使用成员选择操作符（.或->）由类对象限定。例如:

```C++
class C;

C::s_member; // s_member 被 类 C 限定
obj.x; // x 被 类的对象 obj 限定
ptr->y; // y 被 类的对象指针 ptr 限定
```

{{< /alert >}}

***
## using声明

减少反复键入std::的一种方法是使用using声明语句。using声明允许我们使用非限定名称（没有域名称）作为限定名称的别名。

下面是我们的基本Hello world程序，在第5行使用using声明:

```C++
#include <iostream>

int main()
{
   using std::cout; // 这一行告诉编译器 cout 指代 std::cout
   cout << "Hello world!\n"; // 所以没有 std:: 前缀的版本，在这里可以使用

   return 0;
} // using声明，退出当前作用域，失效
```

使用 using std::cout；告诉编译器我们将使用std命名空间中的对象cout。因此，每当它看到cout时，它都会假设我们是指std::cout。如果std::cout和cout的某些其他用法之间存在命名冲突，则首选std::cout。因此，在第6行上，我们可以键入cout而不是std::cout。

在这个琐碎的示例中，这并没有节省多少工作，但如果在函数中多次使用cout，则using声明可以使代码更具可读性。请注意，每个单独的名称都需要单独的using声明（例如，一个用于std::cout，一个用来std::cin，等等…）。

using声明从声明点到对应作用域结束都是有效的。

尽管该方法不如使用std::前缀版本时含义更明确，但它通常被认为是安全的和可接受的（在函数内部使用时）。

***
## using指令

另一种简化方法是使用using指令。稍微简化了一点，using指令将命名空间中的所有标识符导入using指令的作用域。

这是我们的Hello world程序，在第5行有一个using指令:

```C++
#include <iostream>

int main()
{
   using namespace std; // 这个using指令告诉编译器，std命名空间内的所有标识符，在using指令的作用域内，都可以无前缀使用
   cout << "Hello world!\n"; // 所以没有 std:: 前缀的版本，在这里可以使用

   return 0;
} //using指令，退出当前作用域，失效
```

using namespace std; 告诉编译器将std命名空间中的所有名称导入到当前作用域（在本例中，是函数main() 的内部）。然后，当我们使用不含前缀的cout时，它将解析为std::cout。

using指令是为使用标准库内非限定名称的旧命名空间提供的解决方案。不必手动将每个非限定名称更新为限定名称（这是有风险的），可以在每个文件的顶部放置单个using指令（using namespace std;），所有已移动到std命名空间的名称仍然可以非限定使用。

{{< alert success >}}
**对于高级读者**

由于技术原因，using指令实际上并不会将名称导入到当前作用域中——相反，它们将名称导入外部作用域中（然而，这些名称不能从外部作用域访问——它们只能通过从using指令（或嵌套作用域）的作用域进行非限定（无前缀）查找来访问。

实际效果是（在嵌套名称空间内涉及多个using指令的一些奇怪的边缘情况之外），using指令的行为就像名称已导入到当前范围中一样。为了保持简单，我们在将名称导入当前作用域的简化理解下继续。

{{< /alert >}}

***
## using指令的问题（为什么应避免“using namespace std；”）

在现代C++中，与风险相比，using指令通常没有什么好处（节省了一些打字输入）。由于using指令从名称空间导入所有名称（可能包括许多您永远不会使用的名称），因此发生命名冲突的可能性显著增加（特别是在导入std名称空间时）。

为了便于说明，让我们看一个using指令导致歧义的示例:

```C++
#include <iostream>

namespace a
{
	int x{ 10 };
}

namespace b
{
	int x{ 20 };
}

int main()
{
	using namespace a;
	using namespace b;

	std::cout << x << '\n';

	return 0;
}
```

在上面的示例中，编译器无法确定main中的x是指a::x还是b::x。在这种情况下，它将无法编译，并出现“不明确的符号”错误。我们可以通过删除其中一个using语句、改用using声明或用显式域限定符（a::或b::）限定x来解决这个问题。

下面是另一个更微妙的例子:

```C++
#include <iostream> // 引入 std::cout

int cout() // 声明我们自己的 "cout"
{
    return 5;
}

int main()
{
    using namespace std; // 使 "cout" 可以指代 std::cout
    cout << "Hello, world!\n"; // uh oh!  这里的cout是指的哪一个？

    return 0;
}
```

在上面的示例中，编译器无法确定我们对cout的使用是指std::cout还是我们定义的cout函数，编译将再次失败，并出现“模糊符号”错误。尽管这个例子很小，但如果我们显式地以std::cout为前缀，则如下所示:

```C++
    std::cout << "Hello, world!\n"; // 告诉编译器使用的是 std::cout
```

或使用using声明而不是using指令:

```C++
    using std::cout; // 告诉编译器 cout 意味着 std::cout
    cout << "Hello, world!\n"; // 所以这里是 std::cout
```

那么我们的程序就不会有任何问题。虽然您可能不太可能编写名为“cout”的函数，但std命名空间中有数百个其他名称正等待与您的名称冲突。“count”，““min”，“max”，“search”，“sort”，等等。

即使using指令目前不会导致命名冲突，它也会使代码更容易受到未来冲突的影响。例如，如果代码包含随后会更新的某个库，则在更新的库中引入的所有新名称都可能与现有代码命名冲突。

还有一个更阴险的问题也可能发生。更新的库可能会引入一个函数，该函数不仅具有相同的名称，而且实际上更匹配某些函数调用（函数重载的情况）。在这种情况下，编译器可能会决定改用新函数，并且程序的行为将意外更改。

考虑以下程序:

foolib.h（某些第三方库的一部分）:

```C++
#ifndef FOOLIB_H
#define FOOLIB_H

namespace Foo
{
    // 假设这里是我们需要的一些功能
}
#endif
```

main.cpp:

```C++
#include <iostream>
#include <foolib.h> // 第三方库

int someFcn(double)
{
    return 1;
}

int main()
{
    using namespace Foo; // 这里为了不每次输入Foo前缀，使用了using指令
    std::cout << someFcn(0) << '\n'; //  0 应该写做 0.0, 但这是一个容易常忽略的问题

    return 0;
}
```

该程序运行并打印1。

现在，假设我们更新了foolib.我们的程序现在如下所示:

foolib.h（某些第三方库的一部分）:

```C++
#ifndef FOOLIB_H
#define FOOLIB_H

namespace Foo
{
    // 新增加的函数
    int someFcn(int)
    {
        return 2;
    }

    // 假设这里是我们需要的一些功能
}
#endif
```

main.cpp:

```C++
#include <iostream>
#include <foolib.h>

int someFcn(double)
{
    return 1;
}

int main()
{
    using namespace Foo; // 这里为了不每次输入Foo前缀，使用了using指令
    std::cout << someFcn(0) << '\n'; // 0 应该写做 0.0, 但这是一个容易常忽略的问题

    return 0;
}
```

我们的main.cpp文件根本没有更改，但该程序现在运行并打印2！

当编译器遇到函数调用时，它必须确定它应该与函数调用匹配的函数定义。在从一组可能匹配的函数中选择函数时，它更喜欢不需要参数转换的函数。由于0是整数，C++更喜欢将someFcn(0)与新引入的someFcn(int)（无转换）匹配，而不是someFcn(double)（需要从int到double的转换）。这导致程序结果发生意外变化。

如果使用using声明或显式域限定符，则不会发生这种情况。

最后，由于缺乏显式域前缀，读者很难分辨哪些函数是库的一部分，哪些是程序的一部分。例如，如果我们使用using指令:

```C++
using namespace ns;

int main()
{
    foo(); // 这是我们自己编写的函数，还是ns库中的?
}
```

不太容易看出对foo()的调用实际上是对ns::foo()还是对用户定义函数的foo()的调用。当您将鼠标悬停在一个名称上时，现代IDE应该能够为您消除这一点的歧义，但必须悬停在每个名称上，才能看到它来自何处。

如果没有using指令，它会更清楚:

```C++
int main()
{
    ns::foo(); // 很明显是ns库中的
    foo(); // 看起来像是用户自己编写的
}
```

在这个版本中，对ns::foo() 的调用显然是一个库调用。对foo() 的调用可能是对用户定义函数的调用（一些库，包括某些标准库头文件，确实将名称放入全局命名空间中，因此不能保证）。

***
## using声明和using指令的作用范围

如果在块中使用using声明或using指令，则名称仅适用于该块（它遵循正常的块作用域规则）。这是一件好事，因为它减少了在该块内发生命名冲突的机会。

如果在全局命名空间中使用using声明或using指令，则名称适用于文件的整个其余部分（它们具有文件范围）。

***
## 取消或替换using语句

一旦声明了using语句，就无法在声明它的范围内取消它或用其他using语句替换它。

```C++
int main()
{
    using namespace Foo;

    // 没用办法取消 "using namespace Foo" 的效果
    // 也没有办法替换 "using namespace Foo"

    return 0;
} // using namespace Foo效果在这里结束
```

您所能做的最好的事情是从一开始就使用块范围规则有意限制using语句的范围。

```C++
int main()
{
    {
        using namespace Foo;
        // 这里调用 Foo:: stuff
    } // using namespace Foo 失效
 
    {
        using namespace Goo;
        // 这里调用 Goo:: stuff
    } // using namespace Goo 失效

    return 0;
}
```

当然，通过显式地使用域解析操作符（::），可以避免所有这类头痛问题。

***
## using语句的最佳实践

避免using指令（特别是using namespace std；），除非是在特定的情况下（例如使用命名空间std::literals来访问s和sv文本后缀）。using声明通常被认为是在块内使用的安全声明。尽量避免它们在代码文件的全局命名空间中的使用，不要在头文件的全局命名空间中使用它们。

{{< alert success >}}
**最佳实践**

与使用using声明相比，显式的指定命名空间。尽可能避免using指令。using声明可以在块内使用。

{{< /alert >}}

{{< alert success >}}
**相关内容**

using关键字还用于定义类型别名，这与using语句无关。将在后续介绍类型别名时进行介绍。

{{< /alert >}}

***

{{< prevnext prev="/basic/chapter7/scope-duration-linkage/" next="/basic/chapter7/unname-namespace/" >}}
7.10 作用域、存储期和链接摘要
<--->
7.12 未命名与内联的命名空间
{{< /prevnext >}}
