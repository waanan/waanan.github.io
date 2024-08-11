---
title: "std::vector\<bool\>"
date: 2024-07-08T11:10:28+08:00
---

vector有一个有趣的技巧。std::vector\<bool\>有一个特殊的实现，通过类似地将8个布尔值压缩到一个字节中，可以更有效地节省布尔值的空间。

与为位操作而设计的std::bitset不同，std:∶vector\<bool\>缺少位操作成员函数。

{{< alert success >}}
**对于高级读者**

当模板类对特定模板类型参数具有不同的实现时，这称为类模板特化。后续章节进行讨论。

{{< /alert >}}

***
## 使用std::vector\<bool\>

在大多数情况下，std::vector\<bool\>的工作方式与普通的std:∶vector类似:

```C++
#include <iostream>
#include <vector>

int main()
{
    std::vector<bool> v { true, false, false, true, true };
    
    for (int i : v)
        std::cout << i << ' ';
    std::cout << '\n';

    // 将索引 4 位置的值改为 false
    v[4] = false;

    for (int i : v)
        std::cout << i << ' ';
    std::cout << '\n';

    return 0;
}
```

在作者的64位机器上，打印:

```C++
1 0 0 1 1
1 0 0 1 0
```

***
## std::vector\<bool\>权衡

然而，std::vector\<bool\>有一些折衷，用户应该注意。

首先，std::vector\<bool\>有相当高的开销（ sizeof(std::vector\<bool\>) 在作者的机器上是40个字节），因此除非分配的布尔值比体系结构的开销多，否则不会节省内存。

其次，std::vector\<bool\>的性能高度依赖于实现（因为实现甚至不需要进行优化，更不用说做好它了）。根据本文，高度优化的实现可能比替代方案快得多。然而，优化不佳的实现将更慢。

第三，也是最重要的一点，std::vector\<bool\>不是vector（它在内存中不需要是连续的），它也不包含bool值（它包含一组bit），也不满足C++对容器的定义。

尽管在大多数情况下，std::vector\<bool\>的行为类似于vector，但它与标准库的其余部分并不完全兼容。与其他元素类型一起使用的代码可能无法与std::vector\<bool\>一起使用。

例如，当T是除bool之外的任何类型时，以下代码都有效:

```C++
template<typename T>
void foo( std::vector<T>& v )
{
    T& first = v[0]; // 获取第一个元素的引用
    // 对first做一些操作
}
```

***
## 避免std::vector\<bool\>

现代的共识是，通常应该避免使用std::vector\<bool\>，因为性能的提高不太值得不兼容的头痛，因为它不是一个适当的容器。

不幸的是，默认情况下启用了std::vector\<bool\>的优化版本，并且没有办法禁用它。已经有人提议废弃std::vector\<bool\>，并且正在确定bool的压缩vector可能是什么样子（可能作为未来的std::dynamic_bitset）。

我们的建议如下:

1. 当在编译时已知所需的比特数，没有超过中等数量的布尔值要存储（例如，低于64k），并且有限的运算符和成员函数集（例如，缺少迭代器支持）满足您的要求时，请使用（constexpr）std::bitset。
2. 当您需要一个可调整大小的布尔值容器并且不需要节省空间时，首选std::vector\<char\>。该类型的行为类似于普通容器。
3. 当需要动态比特集对其执行位操作时，支持动态比特集的第三方实现（如boost::dynamic_bitset）。这样的类型不会假装是标准库容器，而不是标准库容器。


{{< alert success >}}
**最佳实践**

使用constexpr std::bitset、std:∶vector\<char\>或第三方动态比特集，而不是std::vector\<bool\>。

{{< /alert >}}

