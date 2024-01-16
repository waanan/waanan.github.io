---
title: "全局随机数"
date: 2024-01-02T10:33:49+08:00
---

如果想在多个函数或文件中使用随机数生成器，会发生什么情况？一种方法是在main()函数中创建（并播种）PRNG，然后将其传递到需要它的任何地方。但可能这只偶尔使用的东西，但却有大量的传递。并且在许多不同的地方，传递这样的对象会给代码增加许多混乱。

或者，您可以在每个需要它的函数中创建静态局部std::mt19937变量（静态变量，以便它只被播种一次）。然而，让每个使用随机数生成器的函数定义并播种其自己的本地生成器是多余的，并且对每个生成器的调用量较低，也可能会导致质量较低的结果。

我们真正想要的是一个单一的PRNG对象，可以在任何地方共享和访问，跨越所有函数和文件。这里的最佳选项是创建全局随机数生成器对象。还记得我们是如何告诉您避免非常量全局变量的吗？这是一个例外。

下面是一个简单的、仅含头文件的解决方案，您可以将其包含在任何使用全局随机数的文件中：

random.h:

```C++
#ifndef RANDOM_MT_H
#define RANDOM_MT_H

#include <chrono>
#include <random>

// 只有头文件，内部的 Random 命名空间提供了播种好的Mersenne Twister PRNG的全局访问能力
// 可以在任意文件中直接引入使用 ( inline 关键字避免了单定义规则的报错)
namespace Random
{
	// 返回一个播种好的 Mersenne Twister
	inline std::mt19937 generate()
	{
		std::random_device rd{};

		// 返回一个时间戳以及由7个std::random_device产出的随机数组成的种子序列
		std::seed_seq ss{
			static_cast<std::seed_seq::result_type>(std::chrono::steady_clock::now().time_since_epoch().count()),
				rd(), rd(), rd(), rd(), rd(), rd(), rd() };

		return std::mt19937{ ss };
	}

	// 全局的 std::mt19937 对象.
	// inline 关键字，意味着该对象在整个程序中只有一个
	inline std::mt19937 mt{ generate() }; // 生成一个播种好的std::mt19937对象

	// 产出在 [min, max] 间的一个随机数
	inline int get(int min, int max)
	{
		return std::uniform_int_distribution{min, max}(mt);
	}
}

#endif
```

以及如何使用它的示例程序:

主.cpp:

```C++
#include "Random.h" // 引入 Random::mt, Random::get(), 以及 Random::generate()
#include <iostream>

int main()
{
	// 可以使用 Random::get() 去获得一个范围内的随机数

	std::cout << Random::get(1, 6) << '\n';   // 产出在1到6之间的随机数

	// 可以定义另外一个分布，使用全局的 Random::mt 来产出随机数

	// 创建一个新的随机数生成器，来均匀的生成1到6之间的数字
	std::uniform_int_distribution die6{ 1, 6 };

	// 打印一堆随机数
	for (int count{ 1 }; count <= 10; ++count)
	{
		// 可以直接访问 Random::mt
		std::cout << die6(Random::mt) << '\t'; // 投掷一次筛子，得到结果
	}

	std::cout << '\n';

	return 0;
}
```

通常，当头文件包含在多个源文件中时，在头文件中定义变量和函数将导致违反单定义规则（ODR）。然而，这里已经将mt变量和对应函数声明为inline，这允许在不违反ODR的情况下具有重复的定义，只要这些定义都相同。因为使用的#include 来引入头文件（而不是手动键入它们，或复制/粘贴它们），所以可以确保它们是相同的。

我们必须克服的另一个挑战是如何初始化全局Random::mt对象，因为我们希望它是自播种的，以便不必记住显式调用初始化函数。初始值设定项必须是表达式。为了初始化std::mt19937，需要几个辅助对象（std:∶random_device和std::seed_seq），这些对象必须定义为语句。这就是辅助函数派上用场的地方。函数调用是表达式，因此可以使用函数的返回值作为初始值设定项。在函数中，可以有需要的任何语句组合。因此，generate()函数创建并返回一个完全种子化的std::mt19937对象（使用系统时钟和std::random_device种子化），用作全局random::mt对象的初始值设定项。

一旦引用“Random.h”，可以用两种方法之一使用它:

1. 可以调用Random::get()在两个值之间生成一个随机数（前闭后闭）。
2. 可以通过Random::mt直接访问std::mt19937对象，并对其执行任何操作。

***
