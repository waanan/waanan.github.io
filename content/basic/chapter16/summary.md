---
title: "第16章总结"
date: 2024-07-08T11:10:28+08:00
---

***
## 鼓励的话

这一章并不容易。讲解了许多内容，并发现了C++的一些缺点。恭喜你成功了！

数组是在C++程序中释放大量能量的关键之一。

***
## 章节回顾

容器是一种数据类型，为未命名对象（称为元素）的集合提供存储。当需要处理一组相关的值时，我们通常使用容器。

容器中元素的数量通常称为它的长度（有时称为大小）。在C++中，术语“大小”也通常用于表示容器中的元素数。在大多数编程语言（包括C++）中，容器是同质的，这意味着容器的元素需要具有相同的类型。

容器库是C++标准库的一部分，它包含实现一些常见类型容器的各种类类型。实现容器的类类型有时称为容器类。

数组是连续存储值序列的容器数据类型（意味着每个元素都放在相邻的内存位置，没有间隙）。数组允许快速、直接访问任何元素。

C++包含三种主要的数组类型:（C样式）数组、std::vector容器类和std:∶array容器类。

vector是C++标准容器库中实现数组的容器类之一。std::vector在\<vector\>头文件中定义为类模板，具有定义元素类型的模板类型参数。因此，std::vector\<int\>声明了一个std:∶vector，其元素的类型为int。

容器通常具有一个名为列表构造函数的特殊构造函数，该构造函数允许我们使用初始值设定项列表构造容器的实例(列表初始化)。

在C++中，访问数组元素的最常见方法是使用数组的名称和下标运算符（运算符[]）。为了选择特定的元素，在下标运算符的方括号内，提供一个整数值，用于标识要选择的元素。该整数值称为下标（非正式地称为索引）。第一个元素是使用索引0访问的，第二个元素是用索引1访问的，以此类推……因为索引以0开始，而不是1，所以我们说C++中的数组是从零开始的。

运算符[]不执行任何类型的边界检查，这意味着它不检查索引是否在0到N-1（包括0和N-1）的边界内。将无效索引传递给运算符[]将导致未定义的行为。

数组是少数允许随机访问的容器类型之一，这意味着可以以相同的速度直接访问容器中的每个元素，而不管容器中的元素数量如何。

在构造类类型对象时，匹配列表构造函数被选中，而不是其他匹配构造函数。使用不是元素值的初始值设定项构造容器时，请使用直接初始化。

```C++
std::vector v1 { 5 }; // 定义包含一个元素的vector `5`.
std::vector v2 ( 5 ); // 定义包含五个元素的vector，元素被值初始化
```

std::vector可以设置为const，但不能设置为constexpr。

每个标准库容器类都定义了一个名为size_type（有时写为T::size_type）的嵌套typedef成员，它是用于容器长度（和索引，如果支持）的类型的别名。size_type几乎总是std::size_t的别名，但可以重写（在极少数情况下）以使用不同的类型。可以合理地假设size_type是std::size_t的别名。

当访问容器类的size_type成员时，我们必须使用容器类的完全模板化名称来限定。例如，std::vector\<int\>::size_type。

我们可以使用size()成员函数询问容器类对象的长度，该函数将长度返回为无符号size_type。在C++17中，我们还可以使用std::size()非成员函数。

在C++20中，std::ssize()非成员函数，它以大型有符号整数类型（通常为std:∶ptrdiff_t，这是通常用作std::size_t的有符号对应项的类型）的形式返回长度。

使用at()成员函数访问数组元素会执行运行时边界检查（如果边界超出范围，则抛出类型为std::out_of_range的异常）。如果未捕获异常，则应用程序将被终止。

运算符[]和at()成员函数都支持使用非常数索引进行获取。然而，两者都希望索引的类型为size_type，这是一个无符号整数类型。当索引为非constexpr时，这会导致符号转换问题。

类型为std::vector的对象可以像任何其他对象一样传递给函数。这意味着，如果我们按值传递std::vector，将生成一个昂贵的副本。因此，我们通常通过（const）引用传递std::vector以避免这种复制。

我们可以使用函数模板将任何元素类型的std::vector传递到函数中。可以使用assert()来确保传入的vector具有正确的长度。

术语复制语义是指确定如何制作对象副本的规则。当我们说正在调用复制语义时，这意味着我们已经做了一些事情来制作对象的副本。

当数据的所有权从一个对象转移到另一个对象时，我们说数据已经移动。

移动语义是指确定如何将数据从一个对象移动到另一个对象的规则。当调用移动语义时，将移动任何可以移动的数据成员，并复制任何无法移动的数据乘员。移动数据而不是复制数据的能力可以使移动语义比复制语义更有效，特别是当我们可以用廉价的移动代替昂贵的副本拷贝时。

通常，当用相同类型的对象初始化或为对象分配相同类型的属性时，将使用复制语义（假设没有省略副本）。当对象的类型支持移动语义，并且从中分配的初始值设定项或对象是右值时，将自动使用移动语义。

我们可以按值返回支持移动的类型（如std::vector和std:∶string）。这样的类型将以较低的成本移动其值，而不是制作昂贵的副本。

以某种顺序访问容器的每个元素称为遍历，或遍历容器。

循环通常用于遍历数组，循环变量用作索引。请注意off-by-one错误，其中循环体执行少了一次或多了一次。

基于范围的for循环（有时也称为for-each循环）允许遍历容器，而不必执行显式索引。遍历容器时，优先使用for-each。

使用基于范围的for循环的类型演绎（auto），让编译器推断数组元素的类型。每当您通常通过（const）引用传递该元素类型时，元素声明都应该使用（cont）引用。考虑始终使用const auto&，除非您需要处理副本。这将确保即使后来更改了图元类型，也不会进行复制。

非限定作用域枚举可以用作索引，并有助于提供有关索引含义的任何信息。

每当我们需要表示数组长度的枚举元素时，添加额外的“count”枚举元素是有用的。您可以断言或static_assert数组的长度等于计数枚举元素，以确保使用预期数量的初始值设定项初始化数组。

数组的长度必须在实例化点定义，然后不能更改的数组称为固定大小数组或固定长度数组。动态数组（也称为可调整大小的数组）是一个数组，其大小可以在实例化后更改。这种调整大小的能力使std::vector变得特别。

实例化后，可以通过调用具有新的所需长度的resize()成员函数来调整std::vector的大小。

在std::vector的上下文中，容量是std:∶vector为多少个元素分配了存储，长度是当前正在使用的元素数。我们可以通过capacity()成员函数询问std::vector的容量。

当std::vector更改其管理的存储量时，此过程称为重新分配。由于重新分配通常需要复制数组中的每个元素，因此重新分配是一个昂贵的过程。因此，我们希望尽可能避免重新分配。

下标运算符（运算符[]）和at()成员函数的有效索引基于vector的长度，而不是容量。

vector有一个名为shrink_to_fit()的成员函数，该函数请求vector收缩其容量以匹配其长度。此请求不具有约束力。

项添加到栈和从栈中删除的顺序可以描述为后进先出（LIFO）。添加到堆栈上的最后一个元素将是移除的第一个元素。在编程中，栈是一种容器数据类型，其中元素的插入和删除以后进先出的方式发生。这通常通过名为push和pop的两个操作来实现。

std::vector成员函数push_back()和emplace_back()将增加std:∶vector的长度，并在容量不足以插入值时导致重新分配。当push触发重新分配时，std::vector通常会分配一些额外的容量，以允许添加其他元素，而不会在下次添加元素时触发另一个重新分配。

resize()成员函数更改vector的长度和容量。reserve()成员函数仅更改容量

要增加std::vector中的元素数，请执行以下操作:

1. 通过索引访问vector时使用resize()。这将更改vector的长度，以便索引有效。
2. 使用栈操作访问vector时，请使用reserve()。这会在不更改vector长度的情况下增加容量。

push_back()和emplace_back() 都将元素推送到栈上。如果要推送的对象已经存在，则push_back()和emplace_back()是等效的。然而，在我们创建临时对象以将其推送到vector上的情况下，emplace_back()可能更有效。在创建要添加到容器的新临时对象时，或者在需要访问显式构造函数时，首选emplace_back()。否则，首选push_back()。

std::vector\<bool\>有一个特殊的实现，通过类似地将8个布尔值压缩到一个字节中，可以更有效地节省布尔值的空间。

std::vector\<bool\>不是vector（它在内存中不需要是连续的），也不包含bool值（它包含一组bit），它也不满足C++对容器的定义。尽管在大多数情况下，std::vector\<bool\>的行为类似于vector，但它与标准库的其余部分并不完全兼容。与其他元素类型一起使用的代码可能无法与std::vector\<bool\>一起使用。因此，通常应避免使用std::vector\<bool\>。

***

{{< prevnext prev="/basic/chapter16/vec-bool/" next="/basic/chapter17/arr-intro/" >}}
16.11 std::vector<bool>
<--->
17.0 std::array简介
{{< /prevnext >}}
