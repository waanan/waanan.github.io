---
title: "动态分配数组"
date: 2024-08-19T20:25:40+08:00
---

除了动态分配单个值外，我们还可以动态分配数组。与固定数组（其中数组大小必须在编译时固定）不同，动态分配数组允许我们在运行时选择数组长度（这意味着长度不需要是constexpr）。

要动态分配数组，我们使用数组形式new和delete（通常称为new[]和delete[]）：

```C++
#include <cstddef>
#include <iostream>

int main()
{
    std::cout << "Enter a positive integer: ";
    std::size_t length{};
    std::cin >> length;

    int* array{ new int[length]{} }; // 使用 数组 new.  注意这里长度不再需要是常量了!

    std::cout << "I just allocated an array of integers of length " << length << '\n';

    array[0] = 5; // 将第 0 个元素设置为 5

    delete[] array; // 使用 数组 delete 进行回收

    // 这里未将数组设置为nullptr，因为马上array变量要超出作用域了

    return 0;
}
```

因为我们分配的是数组，C++知道这里使用new的数组版本，而不是new的单个值的版本。

动态分配的数组的长度的类型为std::size_t。如果您使用的是非constexpr int，则需要将长度static_cast转换为std::size_t。因为这被认为是一个窄化转换，编译器将发出警告。

请注意，由于此内存是从堆上空间分配的，因此数组的大小可能相当大。您可以运行上面的程序，并分配长度为1000000（甚至可能是100000000）的数组，而不会出现问题。试试看！因此，需要在C++中分配大量内存的程序通常是这样做的。

{{< alert success >}}
**注**

在这些课程中，我们将动态分配C样式的数组，这是最常见的动态分配数组类型。

虽然可以动态分配std::array，但在这种情况下，通常最好使用非动态分配的std:∶vector。

{{< /alert >}}

***
## 动态删除数组

删除动态分配的数组时，我们必须使用delete的数组版本，即delete[]。

这告诉操作系统它需要清理多个变量，而不是单个变量。新程序员最常见的错误之一，是在删除动态分配的数组时使用delete而不是delete[]。在数组上使用非数组形式的delete将导致未定义的行为，例如数据损坏、内存泄漏、崩溃或其他问题。

数组delete[]的一个常见问题是，“delete[]如何知道要删除多少内存？”。答案是，数组 new[]跟踪分配给变量的内存量，因此数组 delete[]可以删除适当的量。不幸的是，程序员无法访问此大小/长度。

***
## 动态数组使用几乎与固定数组相同

在学习C样式数组退化时，我们知道固定数组保存第一个数组元素的内存地址。还了解到，固定数组可以衰减为指向数组第一个元素的指针。在这种衰减形式中，固定数组的长度不可用（因此，通过sizeof()也不能获得数组的大小），但在其他方面几乎没有区别。

动态数组也是指向数组的第一个元素的指针。因此，它具有相同的限制，因为它不知道其长度或大小。动态数组的功能与退化的固定数组相同，但程序员负责通过delete[]关键字释放动态数组。

***
## 初始化动态分配的数组

如果要将动态分配的数组初始化为0，语法非常简单：

```C++
int* array{ new int[length]{} };
```

在C++11之前，没有简单的方法将动态数组初始化为非零值（初始化列表仅适用于固定数组）。这意味着您必须循环遍历数组并显式分配元素值。

```C++
int* array = new int[5];
array[0] = 9;
array[1] = 7;
array[2] = 5;
array[3] = 3;
array[4] = 1;
```

这超级讨厌！

然而，从C++11开始，现在可以使用初始化列表初始化动态数组！

```C++
int fixedArray[5] = { 9, 7, 5, 3, 1 }; // 初始化固定数组
int* array{ new int[5]{ 9, 7, 5, 3, 1 } }; // C++11开始，初始化动态分配的数组
// 使用auto，可以避免写两遍类型名
auto* array{ new int[5]{ 9, 7, 5, 3, 1 } };
```

注意，该语法在数组长度和初始值列表之间没有运算符=。

为了一致性，还可以使用统一初始化来初始化固定数组：

```C++
int fixedArray[]{ 9, 7, 5, 3, 1 }; // C++11 中初始化固定数组
char fixedArray[]{ "Hello, world!" }; // C++11 中初始化固定数组
```

显式声明数组的长度是可选的。

***
## 调整数组大小

动态分配数组允许您在分配时设置数组长度。然而，C++并没有提供一种内置的方法来调整已经分配的数组的大小。可以通过动态分配新数组、复制元素并删除旧数组来绕过此限制。然而，这很容易出错，特别是当元素类型是Class时（这些类具有管理如何创建它们的特殊规则）。

因此，我们建议避免自己这样做。请改用std::vector。

***

{{< prevnext prev="/basic/chapter19/new-delete/" next="/basic/chapter19/destructor/" >}}
19.0 使用new和delete进行动态分配内存
<--->
19.2 再谈析构函数
{{< /prevnext >}}
