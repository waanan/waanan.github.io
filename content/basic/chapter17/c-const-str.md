---
title: "常量C样式字符串"
date: 2024-08-13T13:06:02+08:00
---

在上一课）中，我们讨论了如何创建和初始化C样式字符串对象：

```C++
#include <iostream>

int main()
{
    char name[]{ "Alex" }; // C-style string
    std::cout << name << '\n';

    return 0;
}
```

C++支持两种不同的方法来创建C样式的字符串常量：

```C++
#include <iostream>

int main()
{
    const char name[] { "Alex" };        // case 1: 使用 C样式字符串字面值 初始化 C样式字符串 常量
    const char* const color{ "Orange" }; // case 2: 指向 C样式字符串的 常量指针

    std::cout << name << ' ' << color << '\n';

    return 0;
}
```

这将打印：

```C++
Alex Orange
```

虽然上述两种方法产生相同的结果，但C++处理这些方法的内存分配略有不同。

在案例1中，“Alex”被放在（可能是只读的）内存中的某处。然后，程序为长度为5的C样式数组（四个显式字符加上空终止符）分配内存，并用字符串“Alex”初始化该内存。因此，我们最终得到了“Alex”的两个副本——一个在全局内存中的某个位置，另一个由name拥有。由于name是常量（并且永远不会被修改），因此制作副本的效率很低。

在案例2中，编译器如何处理这一点是由实现定义的。通常发生的情况是，编译器将字符串“Orange”放在只读内存的某处，然后用字符串的地址初始化指针。

出于优化目的，编译器可以将多个字符串字面值放在相同的位置。例如：

```C++
const char* name1{ "Alex" };
const char* name2{ "Alex" };
```

这是两个不同的字符串变量，具有相同的值。由于这些字符串是常量，编译器可以选择通过只存放一份“Alex”到内存中，并且name1和name2都指向相同的地址。

***
## 使用常量C样式字符串的类型推导

使用C样式字符串字面值的类型推导相当简单：

```C++
    auto s1{ "Alex" };  // 推导为 const char*
    auto* s2{ "Alex" }; // 推导为 const char*
    auto& s3{ "Alex" }; // 推导为 const char(&)[5]
```

***
## 输出指针和C样式字符串

您可能已经注意到std::cout处理不同类型指针的方式有一些有趣的地方。

考虑以下示例：

```C++
#include <iostream>

int main()
{
    int narr[]{ 9, 7, 5, 3, 1 };
    char carr[]{ "Hello!" };
    const char* ptr{ "Alex" };

    std::cout << narr << '\n'; // narr 退化为 int*
    std::cout << carr << '\n'; // carr 退化为 char*
    std::cout << ptr << '\n'; // name 本来就是 char*

    return 0;
}
```

在作者的机器上，打印了：

```C++
003AF738
Hello!
Alex
```

为什么int数组打印地址，而字符数组打印为字符串？

答案是输出流（例如，std::cout）对您的意图做出了一些假设。如果您向它传递一个非字符指针，它将简单地打印该指针的内容（指针持有的地址）。然而，如果您向它传递类型为char\*或const char\*的对象，它将假定您打算打印字符串。因此，它将打印指向的字符串，而不是打印指针的值（地址）！

虽然这在大多数情况下是需要的，但它可能会导致意外的结果。考虑以下情况：

```C++
#include <iostream>

int main()
{
    char c{ 'Q' };
    std::cout << &c;

    return 0;
}
```

在这种情况下，程序员打算打印变量c的地址。然而，&c的类型是char*，因此std::cout尝试将其打印为字符串！因为c不是以null结尾的，所以我们得到了未定义的行为。

在作者的机器上，打印了：

```C++
Q╠╠╠╠╜╡4;¿■A
```

它为什么这样做？首先，它假设&c（类型为char*）是c样式的字符串。因此它打印了“Q”，然后继续。接下来是一堆垃圾。最终，它遇到了一些内存，其中包含一个0值，它将该值解释为空终止符，因此它停止了。根据变量c之后内存中的内容，您看到的可能会有所不同。

这种情况在现实生活中不太可能发生（因为您不太可能真正想要打印内存地址），但它说明了事情是如何在幕后工作的，以及程序是如何在无意中偏离轨道的。

如果您确实想打印字符指针的地址，请将其static_cast为类型const void*：

```C++
#include <iostream>

int main()
{
    const char* ptr{ "Alex" };

    std::cout << ptr << '\n';                           // ptr 按 C样式字符串打印
    std::cout << static_cast<const void*>(ptr) << '\n'; // 打印 ptr 的地址
    
    return 0;
}
```

{{< alert success >}}
**相关内容**

我们在后续讨论 void*——空指针。在这里使用它不需要知道它是如何工作的。

{{< /alert >}}

***
## 优先使用std::string_view而不是C样式的字符串常量

在现代C++中，几乎没有理由使用C样式的字符串常量。相反，应该优先使用constexpr std::string_view对象，它们往往同样快，并且行为更一致。

***
