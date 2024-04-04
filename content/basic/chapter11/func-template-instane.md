---
title: "函数模板实例化"
date: 2024-02-10T01:33:43+08:00
---

在上一课中，我们介绍了函数模板，并将普通的max()函数转换为max\<T\>函数模板:

```C++
template <typename T>
T max(T x, T y)
{
    return (x < y) ? y : x;
}
```

在本课中，我们将重点讨论如何使用函数模板。

***
## 使用函数模板

函数模板实际上不是函数——它们的代码不是直接编译或执行的。相反，函数模板有一项工作:生成函数。

要使用max\<T\>函数模板，可以使用以下语法进行函数调用:

```C++
max<实际类型>(参数一, 参数二); // 实际类型，可能是int，或double 或其它
```

这看起来很像普通的函数调用——主要区别是尖括号中添加了类型（称为模板参数），它指定了将用于代替模板类型T的实际类型。

让我们用一个简单的例子来看看:

```C++
#include <iostream>

template <typename T>
T max(T x, T y)
{
    return (x < y) ? y : x;
}

int main()
{
    std::cout << max<int>(1, 2) << '\n'; // 实例化并调用函数 max<int>(int, int)

    return 0;
}
```

当编译器遇到函数调用max\<int\>(1, 2)时，它将确定max\<int\>(int, int)的函数定义不存在。因此，编译器将使用max\<T\>函数模板来创建一个。

从函数模板（具有模板类型）创建函数（具有特定类型）的过程称为函数模板实例化（简称实例化）。当这个过程由于函数调用而发生时，它被称为隐式实例化。实例化函数通常称为函数实例（简称实例）或模板函数。函数实例在所有方面都是正常函数。

实例化函数的过程很简单:编译器本质上克隆函数模板，并用我们指定的实际类型（int）替换模板类型（T）。

因此，当我们调用max\<int\>(1, 2)时，实例化的函数如下所示:

```C++
template<> // 类型参数，传进来的是int
int max<int>(int x, int y) // 对应生成的函数 max<int>(int, int)
{
    return (x < y) ? y : x;
}
```

下面是与上面相同的示例，显示了编译器在完成所有实例化后实际编译的内容:

```C++
#include <iostream>

// 函数模版的声明 (这里不再需要对应的定义了)
template <typename T> 
T max(T x, T y);

template<>
int max<int>(int x, int y) // 对应生成的函数 max<int>(int, int)
{
    return (x < y) ? y : x;
}

int main()
{
    std::cout << max<int>(1, 2) << '\n'; // 实例化并调用函数 max<int>(int, int)

    return 0;
}
```

您可以自己编译它，并查看它的运行情况。函数模板仅在每个转换单元中首次进行函数调用时实例化。对函数的进一步调用被路由到已经实例化的函数。

相反，如果没有对函数模板进行函数调用，则函数模板将不会在该转换单元中实例化。

让我们看另一个例子:

```C++
#include <iostream>

template <typename T>
T max(T x, T y) // 函数模版 max(T, T)
{
    return (x < y) ? y : x;
}

int main()
{
    std::cout << max<int>(1, 2) << '\n';    // 实例化并调用函数 max<int>(int, int)
    std::cout << max<int>(4, 3) << '\n';    // 调用已经实例化的函数 max<int>(int, int)
    std::cout << max<double>(1, 2) << '\n'; // 实例化并调用函数 max<double>(double, double)

    return 0;
}
```

这与前面的示例类似，但我们的函数模板这次将用于生成两个函数:一次用int替换T，另一次用double替换T。在所有实例化之后，程序将如下所示:

```C++
#include <iostream>

// 函数模版的声明 (这里不再需要对应的定义了)
template <typename T>
T max(T x, T y); 

template<>
int max<int>(int x, int y) // 对应生成的函数 max<int>(int, int)
{
    return (x < y) ? y : x;
}

template<>
double max<double>(double x, double y) // 对应生成的函数 max<double>(double, double)
{
    return (x < y) ? y : x;
}

int main()
{
    std::cout << max<int>(1, 2) << '\n';    // 实例化并调用函数 max<int>(int, int)
    std::cout << max<int>(4, 3) << '\n';    // 调用已经实例化的函数 max<int>(int, int)
    std::cout << max<double>(1, 2) << '\n'; // 实例化并调用函数 max<double>(double, double)

    return 0;
}
```

这里需要注意的另一件事是:当我们实例化max\<double\>时，实例化的函数具有double类型的参数。但因为我们提供了int参数，所以这些参数将隐式转换为double。

***
## 模板参数推导

在大多数情况下，我们想要用于实例化的实际类型将匹配函数参数的类型。例如:

```C++
std::cout << max<int>(1, 2) << '\n'; // 显示标记我们要调用 max<int>
```

在这个函数调用中，我们指定了要用int替换T，但也用int值调用函数。

在参数类型与所需的实际类型匹配的情况下，我们不需要指定实际类型——相反，我们可以使用模板参数推导，让编译器从函数调用中的参数类型推断出应该使用的实际类型。

例如，不用像这样进行函数调用:

```C++
std::cout << max<int>(1, 2) << '\n'; // 显示标记我们要调用 max<int>
```

我们可以改为执行以下操作之一:

```C++
std::cout << max<>(1, 2) << '\n';
std::cout << max(1, 2) << '\n';
```

在这两种情况下，编译器都会看到我们没有提供实际类型，因此它将尝试从函数参数中推断实际类型，这将允许它生成一个max()函数，其中所有模板参数都与提供的参数的类型匹配。在这个例子中，编译器将推断，使用实际类型为int，函数模板max\<T\>可以实例化函数max\<int\>(int, int)，其中两个模板参数（int）的类型与提供的参数（int）的类型匹配。

这两种情况之间的差异与编译器如何从一组重载函数中解析函数调用有关。在最上面的情况下（带空尖括号），编译器在确定要调用哪个重载函数时将仅考虑max\<int\>模板函数重载。在底部情况下（没有尖括号），编译器将同时考虑max\<int\>模板函数重载和max非模板函数重载。

例如:

```C++
#include <iostream>

template <typename T>
T max(T x, T y)
{
    std::cout << "called max<int>(int, int)\n";
    return (x < y) ? y : x;
}

int max(int x, int y)
{
    std::cout << "called max(int, int)\n";
    return (x < y) ? y : x;
}

int main()
{
    std::cout << max<int>(1, 2) << '\n'; // 调用max<int>(int, int)
    std::cout << max<>(1, 2) << '\n';    // 推导 max<int>(int, int) (不考虑非模版函数)
    std::cout << max(1, 2) << '\n';      // 调用 max(int, int)

    return 0;
}
```

请注意，第三个函数调用的语法看起来与普通函数调用完全相同！在大多数情况下，这是我们推荐的使用函数模版的语法。

这有几个原因:

1. 语法更简洁。
2. 很少同时具有匹配的非模板函数和函数模板。
3. 如果我们确实有匹配的非模板函数和匹配的函数模板，我们通常更喜欢调用非模板函数。

最后一点可能不明显。函数模板具有适用于多个类型的实现——但因此，它必须是泛型的。非模板函数仅处理类型的特定组合。它可以具有比函数模板版本更优化或更专用于这些特定类型的实现。例如:

```C++
#include <iostream>

// 这个函数模版，用于许多类型，因此它的实现比较简单
template <typename T>
void print(T x)
{
    std::cout << x; // 按默认打印方式输出x
}

// 这个函数只处理bool值，因此可以做针对性的处理
// 打印一个bool值
void print(bool x)
{
    std::cout << std::boolalpha << x; // 打印 true 或 false, 而不是 1 或 0
}

int main()
{
    print<bool>(true); // 调用 print<bool>(bool) -- 打印 1
    std::cout << '\n';

    print<>(true);     // 推导为 print<bool>(bool) (不考虑非模版函数) -- 打印 1
    std::cout << '\n';

    print(true);       // 调用 print(bool) -- 打印 true
    std::cout << '\n';

    return 0;
}
```

{{< alert success >}}
**最佳实践**

当调用从函数模板实例化的函数时，使用正常的函数调用语法（除非函数模板版本优于匹配的非模板函数）。

{{< /alert >}}

***
## 具有非模板参数的函数模板

可以创建同时具有模板参数和非模板参数的函数模板。模板类型参数可以与任何类型匹配，而非模板参数的工作方式类似于普通函数的参数。

例如:

```C++
// T 是模板类型参数
// double 是非模版参数
template <typename T>
int someFcn (T, double)
{
    return 5;
}

int main()
{
    someFcn(1, 3.4); // 匹配 someFcn(int, double)
    someFcn(1, 3.4f); // 匹配 someFcn(int, double) -- float 被提升为 double
    someFcn(1.2, 3.4); // 匹配 someFcn(double, double)
    someFcn(1.2f, 3.4); // 匹配 someFcn(float, double)
    someFcn(1.2f, 3.4f); // 匹配 someFcn(float, double) -- float 被提升为 double

    return 0;
}
```

此函数模板具有模板化的第一个参数，但第二个参数固定是类型double。请注意，返回类型也可以设置为任何类型。在上面的情况下，我们的函数将始终返回一个int值。

***
## 实例化函数不一定能通过编译

考虑以下程序:

```C++
#include <iostream>

template <typename T>
T addOne(T x)
{
    return x + 1;
}

int main()
{
    std::cout << addOne(1) << '\n';
    std::cout << addOne(2.3) << '\n';

    return 0;
}
```

编译器将有效地编译和执行以下内容:

```C++
#include <iostream>

template <typename T>
T addOne(T x);

template<>
int addOne<int>(int x)
{
    return x + 1;
}

template<>
double addOne<double>(double x)
{
    return x + 1;
}

int main()
{
    std::cout << addOne(1) << '\n';   // 调用 addOne<int>(int)
    std::cout << addOne(2.3) << '\n'; // 调用 addOne<double>(double)

    return 0;
}
```

这将产生以下结果:

```C++
2
3.3
```

但如果我们试着这样做呢？

```C++
#include <iostream>
#include <string>

template <typename T>
T addOne(T x)
{
    return x + 1;
}

int main()
{
    std::string hello { "Hello, world!" };
    std::cout << addOne(hello) << '\n';

    return 0;
}
```

当编译器尝试解析addOne(hello)时，它找不到与addOne(std::string)匹配的非模板函数，但它将找到我们的addOne(T)函数模板，并确定它可以从中生成addOne(std::string)函数。因此，编译器将生成并编译以下内容:

```C++
#include <iostream>
#include <string>

template <typename T>
T addOne(T x);

template<>
std::string addOne<std::string>(std::string x)
{
    return x + 1;
}

int main()
{
    std::string hello{ "Hello, world!" };
    std::cout << addOne(hello) << '\n';

    return 0;
}
```

然而，这将产生编译错误，因为当x是std::string时，x+1没有意义。这里最明显的解决方案就是不要用类型为std::string的参数调用addOne()。

***
## 实例化函数在语义上可能并不总是有意义

编译器将成功编译实例化的函数模板，只要它在语法上有意义。然而，编译器没有任何方法来检查这样的函数在语义上是否确实有意义。

例如:

```C++
#include <iostream>

template <typename T>
T addOne(T x)
{
    return x + 1;
}

int main()
{
    std::cout << addOne("Hello, world!") << '\n';

    return 0;
}
```

在本例中，我们对C样式的字符串字面值调用addOne()。这在语义上到底意味着什么？谁知道呢！

也许令人惊讶的是，由于C++在语法上允许将整数值添加到字符串文本中（我们将在指针算术和下标中介绍这一点），因此上面的示例进行编译，并产生以下结果:

```C++
ello, world!
```

{{< alert success >}}
**警告**

编译器将实例化和编译语义上没有意义的函数模板，只要它们在语法上有效。您有责任确保使用有意义的参数调用函数模板。

{{< /alert >}}

{{< alert success >}}
**对于高级读者**

我们可以告诉编译器，应该禁止实例化具有某些参数的函数模板。这是通过使用函数模板特化来完成的，它允许我们为一组特定的模板参数重载函数模板，以及使用=delete，它告诉编译器，对函数的任何使用都应该产生编译错误。

```C++
#include <iostream>
#include <string>

template <typename T>
T addOne(T x)
{
    return x + 1;
}

// 使用函数模版特化，告知编译器使用 addOne(const char*) 函数会产生编译错误
template <>
const char* addOne(const char* x) = delete;

int main()
{
    std::cout << addOne("Hello, world!") << '\n'; // 编译失败

    return 0;
}
```

在后续章节，我们讨论函数模板特化。

{{< /alert >}}

***
## 在多个文件中使用函数模板

考虑以下程序，它不能正常工作:

main.cpp:

```C++
#include <iostream>

template <typename T>
T addOne(T x); // 函数模版前向声明

int main()
{
    std::cout << addOne(1) << '\n';
    std::cout << addOne(2.3) << '\n';

    return 0;
}
```

add.cpp:

```C++
template <typename T>
T addOne(T x) // function template definition
{
    return x + 1;
}
```

如果addOne是非模板函数，则该程序将正常工作:在main.cpp中，编译器看到addOne的前向声明已足够，并且链接器将main.cpp中对addOne()的调用连接到add.cpp的函数定义。

但由于addOne是模板，因此该程序无法工作，并且出现链接器错误:

```C++
1>Project6.obj : error LNK2019: unresolved external symbol "int __cdecl addOne<int>(int)" (??$addOne@H@@YAHH@Z) referenced in function _main
1>Project6.obj : error LNK2019: unresolved external symbol "double __cdecl addOne<double>(double)" (??$addOne@N@@YANN@Z) referenced in function _main
```

在main.cpp中，我们调用addOne\<int\>和addOne\<double\>。然而，由于编译器无法看到函数模板addOne的定义，因此它无法在main.cpp中实例化这些函数。但它确实看到了addOne的前向声明，并假设这些函数存在于其他地方，并将在稍后链接。

当编译器编译add.cpp时，它将看到函数模板addOne的定义。然而，在add.cpp中没有使用该模板，因此编译器不会实例化任何内容。最终结果是，链接器无法将main.cpp中对addOne\<int\>和addOne\<double\>的调用连接到实际函数，因为这些函数从未实例化。

{{< alert success >}}
**旁白**

如果add.cpp实例化了这些函数，程序将编译并链接得很好。但这样的解决方案是脆弱的，应该避免:

如果add.cpp中的代码后来被更改，导致这些函数不再被实例化，程序将无法链接成功。或者，如果main.cpp调用了addOne的不同版本（如addOne\<float\>），但该版本没有在add.cpp中实例化，则会遇到相同的问题。

{{< /alert >}}

解决此问题的最传统方法是将所有模板代码放在头（.h）文件中，而不是源（.cpp）文件:

add.h:

```C++
#ifndef ADD_H
#define ADD_H

template <typename T>
T addOne(T x) // 函数模版定义
{
    return x + 1;
}

#endif
```

main.cpp:

```C++
#include "add.h" // 引入对应的函数模版定义
#include <iostream>

int main()
{
    std::cout << addOne(1) << '\n';
    std::cout << addOne(2.3) << '\n';

    return 0;
}
```

这样，任何需要访问模板的文件都可以include相关的头文件，并且模板定义将由预处理器复制到源文件中。然后，编译器将能够实例化所需的任何函数。

您可能想知道为什么这不会导致违反单定义规则（ODR）。ODR表示，类型、模板、内联函数和内联变量允许在不同的文件中具有相同的定义。因此，如果将模板定义复制到多个文件中，则没有问题（只要每个定义相同）。

但实例化函数本身又如何呢？如果一个函数在多个文件中实例化，如何不导致违反ODR？答案是，从模板隐式实例化的函数是隐式内联的。正如您所知，内联函数可以在多个文件中定义，只要每个文件中的定义相同。

{{< alert success >}}
**关键点**

模板定义不受单定义规则中，每个程序只需要对象一个定义的限制，因此将相同的模板定义包含在多个源文件中不是问题。并且从函数模板隐式实例化的函数是隐式内联的，因此可以在多个文件中定义它们，只要每个定义都相同。

模板本身不是内联的，因为内联的概念仅适用于变量和函数。

{{< /alert >}}

下面是另一个将函数模板放置在头文件中的示例，因此它可以包含在多个源文件中:

max.h:

```C++
#ifndef MAX_H
#define MAX_H

template <typename T>
T max(T x, T y)
{
    return (x < y) ? y : x;
}

#endif
```

foo.cpp:

```C++
#include "max.h" // 引入函数模版定义 max<T>(T, T)
#include <iostream>

void foo()
{
	std::cout << max(3, 2) << '\n';
}
```

main.cpp:

```C++
#include "max.h" // 引入函数模版定义 for max<T>(T, T)
#include <iostream>

void foo(); // 前向声明函数 foo

int main()
{
    std::cout << max(3, 5) << '\n';
    foo();

    return 0;
}
```

在上面的示例中，main.cpp和foo.cpp都inclue了"max.h"，因此这两个文件中的代码可以使用max\<T\>(T, T)函数模板。

{{< alert success >}}
**最佳实践**

多个文件中需要的模板应该在头文件中定义，然后在需要的地方使用include引用。这允许编译器查看完整的模板定义，并在需要时实例化模板。

{{< /alert >}}

***
## 泛型编程

由于模板类型可以替换为任何实际类型，因此模板类型有时称为泛型类型。由于模板可以不受特定类型限制地编写，因此使用模板编程有时被称为泛型编程。尽管C++通常非常关注类型和类型检查，但相比之下，泛型编程让我们能够专注于算法的逻辑和数据结构的设计，而不必太担心类型信息。

***
## 结论

一旦您习惯了编写函数模板，您就会发现它们实际上并不比具有实际类型的函数需要更长的时间来编写。通过最小化需要编写和维护的代码量，函数模板可以显著减少代码维护工作和错误。

函数模板确实有一些缺点，我们不能不提到它们。首先，编译器将使用一组唯一的参数类型为每个函数调用创建（和编译）一个函数。因此，虽然函数模板编写起来很紧凑，但它们可以扩展为疯狂的代码量，这可能导致代码膨胀和编译时间变慢。函数模板的更大缺点是，它们往往会产生疯狂、不可读的错误消息，这些错误消息比常规函数的编译错误消息更难破译。这些错误消息可能相当吓人，但一旦您理解了它们试图告诉您的内容，它们指出的问题通常很容易解决。

与模板为编程工具包带来的功能和安全性相比，这些缺点相当小，因此可以在任何需要类型灵活性的地方自由使用模板！一个好的经验法则是首先创建普通函数，然后如果您发现需要不同参数类型的重载，则将它们转换为函数模板。

{{< alert success >}}
**最佳实践**

使用函数模板编写泛型代码。

{{< /alert >}}

***

{{< prevnext prev="/basic/chapter11/func-template/" next="/basic/chapter11/func-template-mutli-type/" >}}
11.5 函数模板
<--->
11.7 具有多个模板类型的函数模板
{{< /prevnext >}}
