---
title: "空指针"
date: 2024-02-19T14:35:47+08:00
---

在上一课中，我们介绍了指针的基础知识，指针是保存另一个对象地址的对象。可以使用解引用运算符（*）来访问该地址保存的对象：

```C++
#include <iostream>

int main()
{
    int x{ 5 };
    std::cout << x << '\n'; // 打印变量 x 的值

    int* ptr{ &x }; // ptr 保存 x 的地址
    std::cout << *ptr << '\n'; // 使用解引用访问ptr存储的地址所指向的值（x）

    return 0;
}
```

上面的示例打印：

```C++
5
5
```

在上一课中，我们还注意到指针可以不指向任何东西。在本课中，我们将进一步探讨此类指针（以及不指向任何内容的各种含义）。

***
## 空指针

除了实际内存地址，指针还可以保存一个特定的值：空值。空值（通常缩写为null）是一个特殊的值，表示某物没有值。当指针持有空值时，这意味着指针没有指向任何东西。这样的指针称为空指针。

创建空指针的最简单方法是使用值初始化：

```C++
int main()
{
    int* ptr {}; // ptr 是一个空指针，不指定任何对象
 
    return 0;
}
```

因为我们可以使用赋值来更改指针指向的内容，所以最初设置为null的指针稍后可以更改为指向有效对象：

```C++
#include <iostream>

int main()
{
    int* ptr {}; // ptr 是空指针

    int x { 5 };
    ptr = &x; // ptr 现在指向 x

    std::cout << *ptr << '\n'; // 解引用ptr，打印x
 
    return 0;
}
```

{{< alert success >}}
**最佳实践**

如果不是用有效对象的地址初始化指针，则将其置空。

{{< /alert >}}

***
## nullptr关键字

就像关键字true和false表示布尔字面值一样，nullptr关键字表示空指针字面值。可以使用nullptr显式地初始化指针或为指针分配null值。

```C++
int main()
{
    int* ptr { nullptr }; // 使用nullptr，显示声明ptr是空指针

    int value { 5 };
    int* ptr2 { &value }; // ptr2 是有效的指针
    ptr2 = nullptr; // 将 ptr2 设置为nullptr

    someFunction(nullptr); // 可以将nullptr作为函数参数传递

    return 0;
}
```

在上面的示例中，我们使用赋值将ptr2的值设置为nullptr，使ptr2成为空指针。

***
## 解引用空指针会导致未定义的行为

就像取消对悬挂（或野生）指针的引用导致未定义的行为一样，取消对空指针的引用也会导致未定义行为。在大多数情况下，它会使应用程序崩溃。

下面的程序说明了这一点，当您运行应用程序时，它可能会异常崩溃或终止（继续，尝试它，您不会伤害您的机器）：

```C++
#include <iostream>

int main()
{
    int* ptr {}; // Create a null pointer
    std::cout << *ptr << '\n'; // Dereference the null pointer

    return 0;
}
```

从概念上讲，这是有意义的。解引用指针意味着“转到指针指向的地址并访问那里的值”。空指针持有空值，这在语义上意味着指针没有指向任何东西。那么它将获得什么价值呢？

意外地解引用空指针和悬空指针是C++程序员最常见的错误之一，并且可能是C++程序在实践中崩溃的最常见原因。

{{< alert success >}}
**警告**

无论何时使用指针，都需要格外小心，不要让代码解引用空指针或悬空指针，因为这将导致未定义的行为（可能是应用程序崩溃）。

{{< /alert >}}

***
## 检查空指针

就像可以使用条件语句来测试布尔值的true或false一样，也可以使用条件语句测试指针是否具有值nullptr：

```C++
#include <iostream>

int main()
{
    int x { 5 };
    int* ptr { &x };

    if (ptr == nullptr) // 显式检查
        std::cout << "ptr is null\n";
    else
        std::cout << "ptr is non-null\n";

    int* nullPtr {};
    std::cout << "nullPtr is " << (nullPtr==nullptr ? "null\n" : "non-null\n"); // 显式检查

    return 0;
}
```

上述程序打印：

```C++
ptr is non-null
nullPtr is null
```

我们注意到整数值会隐式转换为布尔值：整数值0转换为布尔值false，任何其他整数值转换为布尔值true。

类似地，指针也将隐式转换为布尔值：空指针转换为布尔值false，非空指针转换成布尔值true。这允许我们跳过对nullptr的显式测试，可以只使用bool值的隐式转换来检查是否为空指针。以下程序等价于前一个程序：

```C++
#include <iostream>

int main()
{
    int x { 5 };
    int* ptr { &x };

    // 隐式转换：空指针转换为布尔值false，非空指针转换成布尔值true
    if (ptr) // 隐式转换为bool值
        std::cout << "ptr is non-null\n";
    else
        std::cout << "ptr is null\n";

    int* nullPtr {};
    std::cout << "nullPtr is " << (nullPtr ? "non-null\n" : "null\n"); // 隐式

    return 0;
}
```

{{< alert success >}}
**警告**

条件语句只能用于区分空指针和非空指针。没有方便的方法来确定非空指针是指向有效对象还是悬空（指向无效对象）。

{{< /alert >}}

***
## 使用nullptr避免悬空指针

在上面，提到解引用空指针或悬空指针将导致未定义的行为。因此，需要确保代码不会做这些事情。

在尝试解引用指针之前使用条件来确保指针非空，可以轻松避免解引用空指针：

```C++
if (ptr) // 如果ptr不是空指针
    std::cout << *ptr << '\n'; // 可以解引用
else
    // 只能做其它不会解引用的操作 (打印错误信息等)
```

但悬空的指针呢？因为没有办法检测指针是否悬空，所以需要避免在程序中有任何悬空指针。可以通过确保任何不指向有效对象的指针都设置为nullptr来实现这一点。

这样，在解引用指针之前，我们只需要测试它是否为null——如果它不为null，我们假设指针没有悬空。

不幸的是，避免悬空指针并不总是容易的：当对象被销毁时，指向该对象的任何指针都将悬空。这样的指针不会自动为空！程序员有责任确保刚刚被销毁的对象的所有指针都正确设置为nullptr。

{{< alert success >}}
**最佳实践**

指针应该保存有效对象的地址，或者设置为nullptr。这样，我们只需要测试指针是否为null，并且可以假设任何非null指针都是有效的。

{{< /alert >}}

{{< alert success >}}
**警告**

当对象被销毁时，指向被销毁对象的任何指针都将悬空（它们不会自动设置为nullptr）。您有责任检测这些情况，并确保随后将这些指针设置为nullptr。

{{< /alert >}}

***
## 旧式的空指针字面值：0和NULL

在较旧的代码中，您可能会看到使用了另外两个字面值，而不是nullptr。

第一个是0。在指针的上下文中，文本0被专门定义为表示空值，并且是唯一被允许分配给指针的整形值。

```C++
int main()
{
    float* ptr { 0 };  // ptr 是空指针 (样例，实际请不要这样写)

    float* ptr2; // ptr2 未被初始化
    ptr2 = 0; // ptr2 现在是空指针 (样例，实际请不要这样写)

    return 0;
}
```

此外，还有一个名为NULL的预处理器宏（在 cstddef 头文件中定义）。该宏继承自C，通常用于指示空指针。

```C++
#include <cstddef> // for NULL

int main()
{
    double* ptr { NULL }; // ptr 是空指针

    double* ptr2; // ptr2 未被初始化
    ptr2 = NULL; // ptr2 现在是空指针

    return 0;
}
```

在现代C++中，应该避免0和NULL（而是使用nullptr）。

{{< alert success >}}
**旁白**

在现代体系结构上，地址0通常用于表示空指针。然而，C++标准并不保证该值，并且一些体系结构使用其他值。当在空指针的上下文中使用时，文本0将被转换为对应体系结构用于表示空指针的任何地址。

{{< /alert >}}

***
## 尽可能支持引用而不是指针

指针和引用都能够间接访问其他对象。

指针具有额外的能力，可以更改它们所指向的内容，并指向null。然而，这些指针功能本身也是危险的：空指针有被解引用的风险，并且更改指针指向的内容的功能可以使创建悬空指针变得更容易：

```C++
int main()
{
    int* ptr { };
    
    {
        int x{ 5 };
        ptr = &x; // ptr指向一个马上要被销毁的对象 (不太可能通过引用有这个能力)
    } // ptr 现在是指向无效对象的悬空指针

    if (ptr) // 判断ptr是否为空指针
        std::cout << *ptr; // 未定义的行为

    return 0;
}
```

由于引用不能绑定到null，因此我们不必担心null引用。并且，由于在创建时引用必须绑定到有效对象，然后不能重新设置，因此悬空引用更难创建。

因为引用更安全，所以优先使用引用而不是指针，除非需要指针提供的额外功能。

***

{{< prevnext prev="/basic/chapter12/pointer-intro/" next="/basic/chapter12/const-ptr/" >}}
12.6 指针简介
<--->
12.8 指针与常量
{{< /prevnext >}}
