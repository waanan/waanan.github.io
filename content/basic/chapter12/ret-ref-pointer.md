---
title: "引用或指针作为函数返回值"
date: 2024-02-19T14:35:47+08:00
---

在前面的课程中，讨论了在通过值传递参数时，将值的副本传递到函数参数中。对于基本类型（复制成本较低）。但对于类类型（如std::string），复制通常是昂贵的。可以通过使用传递（常量）引用（或传递地址）来避免制作昂贵的副本。

当按值返回时，我们遇到了类似的情况：返回值的副本被传递回调用方。如果函数的返回类型是类类型，则这可能很昂贵。

```C++
std::string returnByValue(); // 返回值是 std::string 的拷贝 (昂贵)
```

***
## 引用作为返回值

在将类类型传递回调用方的情况下，可能希望通过引用返回结果。通过引用，返回绑定到所return对象的引用，这避免了复制返回值。要通过引用返回，只需将函数的返回值定义为引用类型：

```C++
std::string&       returnByReference(); // 返回一个已经存在的 std::string 的引用 (代价低)
const std::string& returnByReferenceToConst(); // 返回一个已经存在的 std::string 的const引用 (代价低)
```

下面是简单的代码样例：

```C++
#include <iostream>
#include <string>

const std::string& getProgramName() // 返回一个 const 引用
{
    static const std::string s_programName { "Calculator" }; // 静态存储期, 程序结束后才会销毁

    return s_programName;
}

int main()
{
    std::cout << "This program is named " << getProgramName();

    return 0;
}
```

该程序打印：

```C++
This program is named Calculator
```

由于getProgramName()返回常量引用，因此在执行return s_programName;时，getProgramName() 将返回对s_programName的常量引用（从而避免复制）。然后，调用者可以使用该常量引用来访问s_programName。

***
## 通过引用返回的对象必须在函数返回后存在

使用按引用返回有一个主要的警告：必须确保被引用的对象比返回引用的函数寿命长。否则，返回的引用将悬空（引用已被破坏的对象），并且使用该引用将导致未定义的行为。

在上面的程序中，由于s_programName具有静态存储期，因此s_programName将一直存在到程序结束。当main()访问返回的引用时，它实际上正在访问s_programName，因为s_programName直到稍后才会被销毁。

现在，让我们修改上面的程序，展示函数返回悬空引用时发生的情况：

```C++
#include <iostream>
#include <string>

const std::string& getProgramName()
{
    const std::string programName { "Calculator" }; // 现在是一个普通的局部变量, 函数结束后销毁

    return programName;
}

int main()
{
    std::cout << "This program is named " << getProgramName(); // 未定义的行为

    return 0;
}
```

该程序的结果未定义。当getProgramName()返回时，将返回绑定到局部变量programName的引用。然后，由于programName是具有自动存储期的局部变量，因此programName在函数末尾被销毁。这意味着返回的引用现在处于悬空状态，在main()函数中使用programName会导致未定义的行为。

如果试图通过引用返回局部变量（上面的程序甚至可能无法编译），现代编译器将产生警告或错误，但编译器有时在检测更复杂的情况时会遇到困难。

{{< alert success >}}
**警告**

通过引用返回的对象必须存在于返回引用的函数结束之后，否则将导致悬空引用。切勿通过引用返回（非静态）局部变量或临时变量。

{{< /alert >}}

***
## 生命周期扩展不能跨函数边界

让我们看一个通过引用返回临时对象的示例：

```C++
#include <iostream>

const int& returnByConstReference()
{
    return 5; // 返回临时对象的const引用
}

int main()
{
    const int& ref { returnByConstReference() };

    std::cout << ref; // 未定义的行为
    return 0;
}
```

在上面的程序中，returnByConstReference() 返回整数字面值，但函数的返回类型是const int&。这需要创建绑定到值为5的临时对象的临时引用。然后返回对临时对象的临时引用。

当返回值绑定到另一个常量引用 ref（在main()中）时，被延长生命周期的临时对象已经被销毁。因此，ref被绑定到悬空引用，使用ref将导致未定义的行为。

下面是一个不太明显的例子，同样不起作用：

```C++
#include <iostream>

const int& returnByConstReference(const int& ref)
{
    return ref;
}

int main()
{
    // 案例 1: 直接绑定
    const int& ref1 { 5 }; // 延长生命周期
    std::cout << ref1 << '\n'; // okay

    // 案例 2: 间接绑定
    const int& ref2 { returnByConstReference(5) }; // ref2会绑定到悬空引用
    std::cout << ref2 << '\n'; // 未定义的行为

    return 0;
}
```

在案例2中，创建一个临时对象来保存值5，函数参数ref绑定到该对象。该函数只是将该引用返回给调用方，然后调用方使用该引用来初始化ref2。因为这不是到临时对象的直接绑定（而是通过函数简介传递），所以生命周期延长不适用。这使得ref2悬空，其后续使用是未定义的行为。

{{< alert success >}}
**警告**

生命周期延长不能跨函数边界工作。

{{< /alert >}}

***
## 不通过引用返回非常量静态局部变量

在上面的示例中，通过引用返回常量静态局部变量，以简单的方式说明通过引用返回的机制。然而，通过引用返回非常量静态局部变量是相当不常见的，通常应该避免。下面是一个简化的示例，它说明了可能发生的一个问题：

```C++
#include <iostream>
#include <string>

const int& getNextId()
{
    static int s_x{ 0 }; // 注 : s_x 非 const 
    ++s_x; // 产生下一个 id
    return s_x; // 返回 s_x 的引用
}

int main()
{
    const int& id1 { getNextId() }; // id1 是引用
    const int& id2 { getNextId() }; // id2 是引用

    std::cout << id1 << id2 << '\n';

    return 0;
}
```

该程序打印：

```C++
22
```

这是因为id1和id2引用的是同一个对象（静态变量s_x），所以当任何东西（例如getNextId()）修改该值时，所有引用现在都在访问修改后的值。

通过引用返回非常量静态局部变量的程序通常会出现的另一个问题是，没有标准化的方法将s_x重置回默认状态。这样的程序必须使用非惯用解决方案（例如，重置函数参数），或者只能通过退出并重新启动程序来重置。

虽然上面的例子有点傻，但程序员有时会为了优化目的而尝试上面的代码，然后他们的程序无法按预期工作。

如果通过引用返回的局部变量的创建成本很高，有时会通过常量引用返回常量静态局部变量。但这比较罕见。

返回对常量全局变量的常量引用，有时也是一种封装对全局变量的访问的方法。虽然全局变量是邪恶的，但当有意和小心地使用时，这也是可以的。

{{< alert success >}}
**最佳做法**

避免返回对非常量局部静态变量的引用。

{{< /alert >}}

***
## 函数返回值用来初始化/赋值给普通变量时会生成拷贝副本

如果函数返回引用，并且该引用用于初始化或赋值给非引用变量，则将复制返回值（就像它是按值返回的一样）。

```C++
#include <iostream>
#include <string>

const int& getNextId()
{
    static int s_x{ 0 };
    ++s_x;
    return s_x;
}

int main()
{
    const int id1 { getNextId() }; // id1 是一个普通变量， 会接受 getNextId() 返回引用值的一个拷贝
    const int id2 { getNextId() }; // id2 是一个普通变量， 会接受 getNextId() 返回引用值的一个拷贝

    std::cout << id1 << id2 << '\n';

    return 0;
}
```

在上面的示例中，getNextId() 返回引用，但id1和id2是非引用变量。在这种情况下，将返回引用的值复制到普通变量中。因此，该程序打印：

```C++
12
```

当然，这也违背了通过引用返回值的目的。

还要注意，如果程序返回悬空引用，则在进行复制之前，该引用处于悬空状态，这将导致未定义的行为：

```C++
#include <iostream>
#include <string>

const std::string& getProgramName() // 返回一个悬空引用
{
    const std::string programName{ "Calculator" };

    return programName;
}

int main()
{
    std::string name { getProgramName() }; // 赋值一个悬空引用的值
    std::cout << "This program is named " << name << '\n'; // 未定义的行为

    return 0;
}
```

***
## 可以通过引用返回函数的引用参数

在相当多的情况下，通过引用返回对象是有意义的，我们将在以后的课程中遇到许多这样的情况。现在可以展示一个有用的例子。

如果通过引用将参数传递到函数中，则通过引用返回该参数是安全的。为了将参数传递给函数，参数必须存在于调用方的作用域中。当被调用的函数返回时，该对象必定仍然存在于调用方的作用域中。

下面是一个简单示例：

```C++
#include <iostream>
#include <string>

// 接收两个 std::string 对象, 返回按字母排序较小的那个
const std::string& firstAlphabetical(const std::string& a, const std::string& b)
{
	return (a < b) ? a : b; // 可以使用 operator< 在 std::string 上，来比较哪个字符按字母排序较小
}

int main()
{
	std::string hello { "Hello" };
	std::string world { "World" };

	std::cout << firstAlphabetical(hello, world) << '\n';

	return 0;
}
```

这将打印：

```C++
Hello
```

在上面的函数中，调用者通过const引用传入两个std::string对象，并且这些字符串中按字母顺序比较，排在前面的一个通过const引用返回。如果我们使用了按值传递和按值返回，我们将制作多达3个std::string的副本（每个参数一个，返回值一个）。通过使用按引用传递/按引用返回，可以避免这些副本。

***
## 当右值传递给函数的常量引用参数时，该参数可以通过常量引用return

当实际传递给常量引用参数的值是右值时，仍然可以通过常量引用返回该参数。

这是因为在创建右值的完整表达式结束之前，它们不会被破坏。

首先，让我们看一看这个例子：

```C++
#include <iostream>
#include <string>

std::string getHello()
{
    return std::string{"Hello"};
}

int main()
{
    const std::string s{ getHello() };

    std::cout << s;
    
    return 0;
}
```

在这种情况下，getHello() 按值返回std::string，这是一个右值。然后使用该右值来初始化s。在s的初始化之后，创建右值的表达式已经完成求值，并且右值被销毁。

现在，来看一个类似的示例：

```C++
#include <iostream>
#include <string>

const std::string& foo(const std::string& s)
{
    return s;
}

std::string getHello()
{
    return std::string{"Hello"};
}

int main()
{
    const std::string s{ foo(getHello()) };

    std::cout << s;
    
    return 0;
}
```

这种情况下唯一的区别是，右值在初始化s之前，通过const引用传递给foo()，然后通过const引用返回给调用方。其他所有操作都是相同的。

***
## 调用者可以通过函数返回的引用修改对应的对象

当参数通过非常量引用传递给函数时，函数可以使用引用来修改参数的值。

类似地，当从函数返回非常量引用时，调用方可以使用该引用来修改返回的值。

下面是一个示例：

```C++
#include <iostream>

// 接受两个非常量引用, 通过引用返回较大的那个
int& max(int& x, int& y)
{
    return (x > y) ? x : y;
}

int main()
{
    int a{ 5 };
    int b{ 6 };

    max(a, b) = 7; // 将 a 与 b 之间较大的设置为 7

    std::cout << a << b << '\n';
        
    return 0;
}
```

在上面的程序中，max(a, b) 使用a和b作为参数调用max()函数。引用参数x绑定到a，引用参数y绑定到b。然后，函数确定x（5）和y（6）中哪个更大。在这种情况下，这是y，因此函数将y（仍然绑定到b）返回给调用方。然后，调用者将值7分配给这个返回的引用。

因此，表达式max(a, b) = 7 等价于 b=7。

这将打印：

```C++
57
```

***
## 按地址返回

按地址返回与按引用返回的工作原理几乎相同，只是返回的是对象的指针，而不是对象的引用。按地址返回与按引用返回具有相同的主要告警——按地址返回的对象必须在函数返回之后仍在存在，否则调用方将收到一个悬空指针。

按地址返回比按引用返回的主要优势是，如果没有要返回的有效对象，可以使函数返回nullptr。例如，假设有一个要搜索的学生列表。如果在列表中找到要查找的学生，则可以返回表示匹配学生的对象的指针。如果找不到任何匹配的学生，可以返回nullptr，表示找不到匹配的学生对象。

按地址返回的主要缺点是，调用方必须记住，在解引用返回值之前执行nullptr检查，否则可能会发生空指针解引用，并导致未定义的行为。由于这种危险，应首选通过引用返回而不是通过地址返回，除非需要返回“空对象”的能力。

***
