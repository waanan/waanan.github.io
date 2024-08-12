---
title: "数组和循环"
date: 2024-07-08T11:10:28+08:00
---

在本章第一节中，我们介绍了当有许多相关的单个变量时出现的可扩展性挑战。在本课中，将重新介绍该问题，然后讨论数组如何帮助我们优雅地解决此类问题。

***
## 可变与可扩展性挑战

考虑这样一种情况，想要找到一个班级学生的平均考试成绩。为了使这些例子简洁，假设这个班只有5个学生。

下面是可以使用单个变量解决此问题的方法：

```C++
#include <iostream>

int main()
{
    // 分配 5 五个整形变量 (每一个名字不同)
    int testScore1{ 84 };
    int testScore2{ 92 };
    int testScore3{ 76 };
    int testScore4{ 81 };
    int testScore5{ 56 };

    int average { (testScore1 + testScore2 + testScore3 + testScore4 + testScore5) / 5 };

    std::cout << "The class average is: " << average << '\n';

    return 0;
}
```

这是大量的变量和大量的输入。想象一下，要为30名学生或600名学生做多少工作。此外，如果添加了新的成绩，则必须声明、初始化新变量，并将其添加到平均计算中。记得更新除数吗？如果忘记了，那么现在有一个语义错误。每当必须修改现有代码时，都有引入错误的风险。

现在，您知道了，当有一组相关的变量时，应该使用数组。因此，用std::vector替换单个变量：

```C++
#include <iostream>
#include <vector>

int main()
{
    std::vector testScore { 84, 92, 76, 81, 56 };
    std::size_t length { testScore.size() };
    
    int average { (testScore[0] + testScore[1] + testScore[2] + testScore[3] + testScore[4])
        / static_cast<int>(length) };

    std::cout << "The class average is: " << average << '\n';

    return 0;
}
```

这更好——显著减少了定义的变量的数量，平均计算的除数现在直接由数组的长度确定。

但平均计算仍然是一个问题，因为必须手动逐个列出每个元素。因为必须显式地列出每个元素，所以该代码仅适用于有固定长度的数组。如果我们还希望能够平均其他长度的数组，则需要为每个不同的数组长度编写一个新的平均计算。

真正需要的是某种方法来访问每个数组元素，而不必显式列出每个元素。

***
## 循环

在前面的课程中，我们注意到数组下标不需要是常量表达式——它们可以是运行时表达式。这意味着可以使用变量的值作为索引。

还请注意，在前一示例的平均计算中使用的数组索引是升序：0、1、2、3、4。因此，如果有某种方法将变量按顺序设置为值0、1、2、3和4，那么可以只使用该变量作为数组索引。我们已经知道如何做到这一点——使用for循环。

让我们使用for循环重写上面的示例，其中循环变量用作数组索引：

```C++
#include <iostream>
#include <vector>

int main()
{
    std::vector testScore { 84, 92, 76, 81, 56 };
    std::size_t length { testScore.size() };

    int average { 0 };
    for (std::size_t index{ 0 }; index < length; ++index) // index 从 0 增长到 length-1
        average += testScore[index];                      // 将 `index` 位置对应的值进行累加
    average /= static_cast<int>(length);                  // 计算平均值

    std::cout << "The class average is: " << average << '\n';

    return 0;
}
```

这应该是相当简单的。索引从0开始，testScore[0]添加到average，并且索引增加到1。testScore[1]加到average上，索引增加到2。最终，当索引增加到5时，index \< length为false，循环终止。

此时，循环将testScore[0]、testScore[1]、testScore[2]、testScre[3]和testScole[4]的值添加到average。

最后，通过将累积值除以数组长度来计算平均值。

该解决方案在可维护性方面是理想的。循环迭代的次数由数组的长度确定，循环变量用于执行所有数组索引。不再需要手动列出每个数组元素。

如果我们想添加或删除测试分数，可以只修改数组初始值设定项的数量，其余的代码仍然可以工作，而无需进一步更改！

以某种顺序访问容器的每个元素称为遍历，或遍历容器。遍历通常称为迭代，或者在容器上迭代或在容器中迭代。

{{< alert success >}}
**注**

由于容器类使用类型size_t作为长度和索引，因此在本课中，将执行相同的操作。将在后面讨论使用有符号长度和索引。

{{< /alert >}}

***
## 模板、数组和循环释放了可扩展性

数组提供了一种存储多个对象的方法，而不必命名每个元素。

循环提供了一种遍历数组的方法，而不必显式列出每个元素。

模板提供了一种参数化元素类型的方法。

模板、数组和循环一起允许我们编写可以在元素容器上操作的代码，而不管容器中的元素类型或元素数量！

为了进一步说明这一点，让我们重写上面的示例，将平均计算重构为函数模板：

```C++
#include <iostream>
#include <vector>

// 计算 std::vector 中平均值的函数模版
template <typename T>
T calculateAverage(const std::vector<T>& arr)
{
    std::size_t length { arr.size() };
    
    T average { 0 };                                      // 如果数组里的值类型为 T, 那么其平均值的类型应该也为 T
    for (std::size_t index{ 0 }; index < length; ++index) // 遍历所有的元素
        average += arr[index];                            // 进行相加
    average /= static_cast<int>(length);
    
    return average;
}

int main()
{
    std::vector class1 { 84, 92, 76, 81, 56 };
    std::cout << "The class 1 average is: " << calculateAverage(class1) << '\n'; // 计算 5 个 int 的平均值

    std::vector class2 { 93.2, 88.6, 64.2, 81.0 };
    std::cout << "The class 2 average is: " << calculateAverage(class2) << '\n'; // 计算 4 个 double的平均值
    
    return 0;
}
```

在上面的示例中，我们创建了函数模板calculateAverage()，它接受任意元素类型和任意长度的std::vector，并返回平均值。在main()中，我们演示了当使用5个int元素的数组或4个double元素的数组调用该函数时，该函数同样可以很好地工作！

calculateAverage() 将适用于支持函数内使用的运算符（ operator+=(T)，operator/=(int) ）的任何类型T。如果尝试使用不支持这些运算符的T，编译器将在尝试编译实例化函数模板时出错。

***
## 可以对数组和循环做什么

既然我们知道了如何使用循环遍历元素的容器，那么让我们看看可以使用容器遍历的最常见的事情。我们通常通过遍历容器来执行以下四项操作之一：

1. 根据现有的值，计算一个新值（平均值，求和 等）
2. 查询存在的元素（包括，是否确切匹配，匹配的个数，找到最大值 等）
3. 对每个元素进行操作（例如，打印每个元素，将每个元素乘2 等）
4. 对容器重新排序

其中的前三个相当简单。可以使用单个循环遍历数组，根据需要检查或修改每个元素。

重新排序容器的元素要复杂得多，因为这样做通常涉及在另一个循环中使用循环。虽然可以手动执行此操作，但通常最好使用标准库中的现有算法来执行此操作。将在未来的一章中讨论算法时更详细地讨论这一点。

***
## 数组和off-by-one错误

当使用索引遍历容器时，必须注意确保循环执行正确的次数。Off-by-one错误（循环体多执行或少执行一次）很容易发生。

通常，当使用索引遍历容器时，将从0开始索引，并循环直到索引<长度。

新程序员有时会意外地将索引<=长度用作循环条件。这将导致在索引==长度时执行循环，这将导致越界下标和未定义的行为。

***

{{< prevnext prev="/basic/chapter16/vec-ret-move/" next="/basic/chapter16/vec-loop-sign-index/" >}}
16.4 返回std::vector，移动语义简介
<--->
16.6 数组、循环和有符号下标
{{< /prevnext >}}
