---
title: "为代码计时"
date: 2024-08-19T20:14:59+08:00
---

在编写代码时，有时会遇到不确定某个方法是否更具性能的情况。那怎么说呢？

一种简单的方法是对代码进行计时，以查看运行代码所需的时间。C++11在chrono库中提供了一些功能来实现这一点。然而，使用chrono库有点神秘。好消息是，我们可以轻松地将所需的所有计时功能封装到一个类中，然后可以在自己的程序中使用。

如下：

```C++
#include <chrono> // for std::chrono 函数

class Timer
{
private:
	// 嵌套类型的别名，让后面代码更简洁
	using Clock = std::chrono::steady_clock;
	using Second = std::chrono::duration<double, std::ratio<1> >;
	
	std::chrono::time_point<Clock> m_beg { Clock::now() };

public:
	void reset()
	{
		m_beg = Clock::now();
	}
	
	double elapsed() const
	{
		return std::chrono::duration_cast<Second>(Clock::now() - m_beg).count();
	}
};
```

就是这样！为了使用它，我们在主函数的顶部（或我们想开始计时的任何位置）实例化一个Timer对象，然后每当我们想知道程序运行到那个点需要多长时间时，就调用elapsed()成员函数。

```C++
#include <iostream>

int main()
{
    Timer t;

    // 下面写一些需要计时的代码

    std::cout << "Time elapsed: " << t.elapsed() << " seconds\n";

    return 0;
}
```

现在，让我们在一个实际的例子中使用它，其中我们对10000个元素的数组进行排序。首先，让我们使用在前一章中开发的选择排序算法：

```C++
#include <array>
#include <chrono> // for std::chrono functions
#include <cstddef> // for std::size_t
#include <iostream>
#include <numeric> // for std::iota

const int g_arrayElements { 10000 };

class Timer
{
private:
    //  嵌套类型的别名，让后面代码更简洁
    using Clock = std::chrono::steady_clock;
    using Second = std::chrono::duration<double, std::ratio<1> >;

    std::chrono::time_point<Clock> m_beg{ Clock::now() };

public:

    void reset()
    {
        m_beg = Clock::now();
    }

    double elapsed() const
    {
        return std::chrono::duration_cast<Second>(Clock::now() - m_beg).count();
    }
};

void sortArray(std::array<int, g_arrayElements>& array)
{

    // 迭代数组的每个位置
    // (出了最后一个，因为在最终它肯定已经排序好了)
    for (std::size_t startIndex{ 0 }; startIndex < (g_arrayElements - 1); ++startIndex)
    {
        // smallestIndex 是遍历过程中，最小的元素的位置
        // 开始时，最小的肯定是遍历开始的位置
        std::size_t smallestIndex{ startIndex };

        // 在剩余的数组中，尝试找一个更小的元素
        for (std::size_t currentIndex{ startIndex + 1 }; currentIndex < g_arrayElements; ++currentIndex)
        {
            // 如果找到更小的
            if (array[currentIndex] < array[smallestIndex])
            {
                // 记录它的位置
                smallestIndex = currentIndex;
            }
        }

        // smallestIndex 现在记录的是数组最小的元素
        // 与起始位置的元素互换 (将它放置到正确的位置)
        std::swap(array[startIndex], array[smallestIndex]);
    }
}

int main()
{
    std::array<int, g_arrayElements> array;
    std::iota(array.rbegin(), array.rend(), 1); // 数组中填充 10000 到 1

    Timer t;

    sortArray(array);

    std::cout << "Time taken: " << t.elapsed() << " seconds\n";

    return 0;
}
```

在作者的机器上，三次运行产生0.0507、0.0506和0.0498的计时。所以我们可以说大约0.05秒。

现在，让我们使用标准库中的std::sort进行相同的测试。

```C++
#include <algorithm> // for std::sort
#include <array>
#include <chrono> // for std::chrono functions
#include <cstddef> // for std::size_t
#include <iostream>
#include <numeric> // for std::iota

const int g_arrayElements { 10000 };

class Timer
{
private:
    // 嵌套类型的别名，让后面代码更简洁
    using Clock = std::chrono::steady_clock;
    using Second = std::chrono::duration<double, std::ratio<1> >;

    std::chrono::time_point<Clock> m_beg{ Clock::now() };

public:

    void reset()
    {
        m_beg = Clock::now();
    }

    double elapsed() const
    {
        return std::chrono::duration_cast<Second>(Clock::now() - m_beg).count();
    }
};

int main()
{
    std::array<int, g_arrayElements> array;
    std::iota(array.rbegin(), array.rend(), 1); // 数组中填充 10000 到 1

    Timer t;

    std::ranges::sort(array); // 从 C++20 开始支持
    // 如果编译器不支持c++20，采用如下的写法
    // std::sort(array.begin(), array.end());

    std::cout << "Time taken: " << t.elapsed() << " seconds\n";

    return 0;
}
```

在作者的机器上，这产生了0.000693、0.000692和0.000699的结果。所以基本上在0.0007左右。

换句话说，在这种情况下，std::sort比我们自己编写的选择排序快100倍！

***
## 可能影响程序性能的事项

为程序的运行计时是相当简单的，但您的结果可能会受到许多事情的显著影响，并且了解如何正确测量以及哪些事情会影响计时非常重要。

首先，确保使用的是编译发布配置构建目标，而不是调试构建目标。调试构建目标通常会关闭优化，并且该优化会对结果产生重大影响。例如，使用调试构建目标，在作者的机器上运行上面的std::sort示例需要0.0235秒——是原来的33倍！

其次，您的计时结果可能会受到系统在后台执行的其他操作的影响。确保您的系统没有执行任何CPU、内存或硬盘密集型操作（例如，玩游戏、搜索文件、运行防病毒扫描或在后台安装更新）。例如网页在新的广告横幅中旋转并必须解析一堆javascript时，等看似无害的东西，可以暂时将CPU利用率提高到100%。在测量之前可以关闭的应用程序越多，结果的差异就越小。

第三，如果您的程序使用随机数生成器，则生成的随机数的特定序列可能会影响计时。例如，如果要对填充了随机数的数组进行排序，则结果可能会因运行而异，因为对数组进行排序所需的交换数量将因运行而变化。为了在程序的多个运行中获得更一致的结果，可以临时为随机数生成器设定固定值（而不是std::random_device或系统时钟），以便它在每次运行时生成相同的数字序列。然而，如果程序的性能高度依赖于生成的特定随机序列，这也可能导致总体上的误导性结果。

第四，确保您没有在计时等待用户输入，因为用户输入内容所需的时间不应该是计时考虑的一部分。如果需要用户输入，请考虑添加某种方式来提供不等待用户的输入（例如，来自文件的数据等）。

***
## 测量性能

测量程序的性能时，至少收集3个结果。如果结果都相似，则这些可能表示程序在该机器上的实际性能。否则，继续进行测量，直到有一组相似的结果（并了解哪些其他结果是偏差较大的值）。由于系统在某些运行期间在后台执行某些操作，因此出现一个或多个异常值并不罕见。

如果您的结果有很大的差异（并且没有很好地聚类），那么您的程序可能会受到系统上发生的其他事情的显著影响，或者受到应用程序中随机化的影响。

由于性能度量受许多因素（特别是硬件速度，但也包括操作系统、应用程序运行等）的影响，因此除了了解程序在您关心的特定机器上的运行情况之外，绝对性能度量（例如，“程序在10秒内运行”）通常没有那么有用。在不同的机器上，相同的程序可以在1秒、10秒或1分钟内运行。如果不实际测量不同硬件的能力，则很难知道。

然而，在单个机器上，相对性能测量可能是有用的。我们可以从程序的几个不同变体中收集性能结果，以确定哪个变体的性能最好。例如，如果变体1在10秒内运行，而变体2在8秒内运行，则无论该机器的绝对速度如何，变体2在所有类似机器上可能会更快。

测量第二个变体后，良好的健全性检查是再次测量第一个变体。如果第一个变体的结果与该变体的初始测量值一致，则两个变体的测量结果应具有合理的可比性。例如，如果变体1在10秒内运行，变体2在8秒内运行，然后我们再次测量变体1并获得10秒，那么我们可以合理地得出结论，两个变体的测量值都是相对准确的，并且变体2更快。

然而，如果第一个变体的结果不再与该变体的初始测量值一致，则机器上发生了影响性能的事情，并且很难区分测量差异是由于变体还是由于机器本身。在这种情况下，最好放弃现有的结果并重新测量。

***

{{< prevnext prev="/basic/chapter18/std-algorithm/" next="/basic/chapter19/new-delete/" >}}
18.2 算法标准库简介
<--->
19.0 使用new和delete进行动态分配内存
{{< /prevnext >}}
