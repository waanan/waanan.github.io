---
title: "未命名与内联的命名空间"
date: 2023-12-18T16:52:52+08:00
---

C++有值得了解的两种命名空间变体，这一课是可选的。

***
## 未命名（匿名）命名空间

未命名命名空间（也称为匿名命名空间）是定义时没有名称的命名空间，如下所示：

```C++
#include <iostream>

namespace // 未命名的命名空间
{
    void doSomething() // 只能在本文件中访问
    {
        std::cout << "v1\n";
    }
}

int main()
{
    doSomething(); // 使用doSomething()，可以不用带命名空间限定符

    return 0;
}
```

这将打印：

```C++
v1
```

在未命名命名空间中声明的所有内容都被视为父命名空间的一部分。因此，即使函数doSomething() 在未命名的命名空间中定义，函数本身也可以在父命名空间（在本例中是全局命名空间）被访问，这就是为什么我们可以从main() 调用doSometing() ，而不需要任何限定符。

这可能会使未命名的命名空间看起来毫无用处。但未命名命名空间的另一个影响是，未命名命名空间内的所有标识符都被视为具有内部链接，这意味着在定义未命名命名空间所在的文件外部看不到未命名名称空间的内容。

对于函数，这实际上与将未命名命名空间中的所有函数定义为static函数相同。以下程序实际上与上面的程序相同：

```C++
#include <iostream>

static void doSomething() // 只能在本文件中访问
{
    std::cout << "v1\n";
}

int main()
{
    doSomething(); // 使用doSomething()，可以不用带命名空间限定符

    return 0;
}
```

当您有许多内容要确保它们具有内部连接时，通常会使用未命名命名空间。因为在单个未命名命名空间中集中定义此类内容，比将所有声明标记为static更容易。未命名的名称空间还将用户自定义的类型限制在本文件中，这方面没有替代的等效机制。

***
## 内联命名空间

现在考虑以下程序：

```C++
#include <iostream>

void doSomething()
{
    std::cout << "v1\n";
}

int main()
{
    doSomething();

    return 0;
}
```

这将打印：

```C++
v1
```

非常简单，对吧？

但假设您对doSomething() 不满意，并且希望以某种方式改进它，从而改变它的行为方式。但如果这样做，则可能会破坏使用旧版本的现有程序。怎么处理？

一种方法是使用不同的名称创建函数的新版本。但在许多更改的过程中，最终可能会得到一组名称几乎相同的函数（doSomething_v2、doSometthing_v3等）。

另一种方法是使用内联命名空间。内联命名空间是通常用于版本内容的命名空间。与未命名命名空间很相似，在内联命名空间内声明的任何内容都被视为父命名空间的一部分。然而，与未命名名称空间不同，内联名称空间不影响链接。

要定义内联命名空间，我们使用inline关键字：

```C++
#include <iostream>

inline namespace V1 // 定义内联命名空间 V1
{
    void doSomething()
    {
        std::cout << "V1\n";
    }
}

namespace V2 // 定义普通命名空间 V2
{
    void doSomething()
    {
        std::cout << "V2\n";
    }
}

int main()
{
    V1::doSomething(); // 调用v1版 doSomething()
    V2::doSomething(); // 调用v2版 doSomething()

    doSomething(); // 调用内联版本 doSomething() (V1)
 
    return 0;
}
```

这将打印：

```C++
V1
V2
V1
```

在上面的示例中，doSomething()的调用获得V1（内联版本）。想要使用较新版本的调用可以显式调用V2::doSomething()。这保留了现有程序的功能，同时允许较新的程序利用较新/更好的变体。

或者，如果要推送较新的版本：

```C++
#include <iostream>

namespace V1 // 定义普通命名空间 V1
{
    void doSomething()
    {
        std::cout << "V1\n";
    }
}

inline namespace V2 // 定义内联命名空间 V2
{
    void doSomething()
    {
        std::cout << "V2\n";
    }
}

int main()
{
    V1::doSomething(); // 调用v1版 doSomething()
    V2::doSomething(); // 调用v2版 doSomething()

    doSomething(); // 调用内联版本 doSomething() (V2)
 
    return 0;
}
```

这将打印：

```C++
V1
V2
V2
```


在本例中，默认情况下，doSomething()的所有调用方都将获得v2版本（更新和更好的版本）。仍然需要旧版本doSomething()的用户可以显式调用V1::doSometing()来访问旧的行为。这意味着需要V1版本的现有程序将需要用V1::doSomething全局替换doSomething，但如果函数命名良好，这通常不会有问题。

***
## 混合内联命名空间和未命名命名空间(选读)

命名空间可以是内联的，也可以是未命名的：

```C++
#include <iostream>

namespace V1 // 定义普通命名空间 V1
{
    void doSomething()
    {
        std::cout << "V1\n";
    }
}

inline namespace // 定义一个内联的未命名的命名空间
{
    void doSomething() // 内部链接
    {
        std::cout << "V2\n";
    }
}

int main()
{
    V1::doSomething(); // 调用v1版 doSomething()

    doSomething(); // 调用内联版本 doSomething() (未命名版本)

    return 0;
}
```

然而，在这种情况下，最好将匿名命名空间嵌套在内联命名空间中。这具有相同的效果（默认情况下，匿名命名空间内的所有函数都具有内部链接），但仍然为您提供了一个可以使用的显式命名空间名称：

```C++
#include <iostream>

namespace V1 // 定义普通命名空间 V1
{
    void doSomething()
    {
        std::cout << "V1\n";
    }
}

inline namespace V2 // 定义一个内联的命名空间 V2
{
    namespace // 匿名的命名空间
    {
        void doSomething() // 内部链接
        {
            std::cout << "V2\n";
        }

    }
}

int main()
{
    V1::doSomething(); // 调用v1版 doSomething()
    V2::doSomething(); // 调用v2版 doSomething()

    ::doSomething(); // 调用内联版本 doSomething() (V2)

    return 0;
}
```

***

{{< prevnext prev="/basic/chapter7/using/" next="/basic/chapter7/summary/" >}}
7.11 using声明和using指令
<--->
7.13 第七章总结
{{< /prevnext >}}
