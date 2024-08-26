---
title: "std::array与类类型元素"
date: 2024-08-13T13:06:02+08:00
---

数组不限于只能存放基本类型的元素。相反，std::array的元素可以是任何对象类型，包括复合类型。这意味着您可以创建指针的std::array，或结构体（或class）的std:::array

然而，初始化结构或类的std::array往往会绊倒新的程序员，因此我们将花一节课来明确地讨论这个主题。

{{< alert success >}}
**注**

在本课中，将使用结构体来说明我们的观点。该材料同样适用于类。

{{< /alert >}}

***
## 定义并分配结构体给std::array

让我们从一个简单的结构体开始:

```C++
struct House
{
    int number{};
    int stories{};
    int roomsPerStory{};
};
```

定义House的std::array并分配元素的工作方式与您预期的一样:

```C++
#include <array>
#include <iostream>

struct House
{
    int number{};
    int stories{};
    int roomsPerStory{};
};

int main()
{
    std::array<House, 3> houses{};

    houses[0] = { 13, 1, 7 };
    houses[1] = { 14, 2, 5 };
    houses[2] = { 15, 2, 4 };

    for (const auto& house : houses)
    {
        std::cout << "House number " << house.number
                  << " has " << (house.stories * house.roomsPerStory)
                  << " rooms.\n";
    }

    return 0;
}
```

上述输出如下:

```C++
House number 13 has 7 rooms.
House number 14 has 10 rooms.
House number 15 has 8 rooms.
```

***
## 初始化元素为结构体的std::array

只要明确了元素类型，初始化也可以像预期的那样工作:

```C++
#include <array>
#include <iostream>

struct House
{
    int number{};
    int stories{};
    int roomsPerStory{};
};

int main()
{
    constexpr std::array houses { // 使用CTAD去推导模版参数类型为 <House, 3>
            House{ 13, 1, 7 },
            House{ 14, 2, 5 },
            House{ 15, 2, 4 }
        };

    for (const auto& house : houses)
    {
        std::cout << "House number " << house.number
            << " has " << (house.stories * house.roomsPerStory)
            << " rooms.\n";
    }

    return 0;
}
```

在上面的示例中，使用CTAD将std::array的类型推断为std::array\<House，3\>。然后，提供3个House对象作为初始值设定项，这非常好。

***
## 初始化，而不显式指定每个初始值设定项的元素类型

在上面的示例中，您会注意到每个初始值设定项都要求我们列出元素类型:

```C++
    constexpr std::array houses {
            House{ 13, 1, 7 }, // 指定类型为 House
            House{ 14, 2, 5 }, // 这里也是
            House{ 15, 2, 4 }  // 这里也是
        };
```

但在分配案例中，不必这样做:

```C++
    // 编译器知道house中的每个元素类型为 House
    // 因此隐式的将右边的每个元素转换为 House
    houses[0] = { 13, 1, 7 };
    houses[1] = { 14, 2, 5 };
    houses[2] = { 15, 2, 4 };
```

所以你可能会想试试这样的方法:

```C++
    // 无法按预期工作
    constexpr std::array<House, 3> houses { // 告诉编译器每个元素都是一个 House
            { 13, 1, 7 }, // 这里不再声明元素类型
            { 14, 2, 5 },
            { 15, 2, 4 } 
        };
```

也许令人惊讶的是，这不起作用。让我们探索一下原因。

简要来说，std::array是定义为包含一个C样式数组的结构体，如下所示:

```C++
template<typename T, std::size_t N>
struct array
{
    T implementation_defined_name[N]; // C样式数组，有N个T类型的元素
}
```

因此，当我们尝试根据上面的内容初始化House时，编译器将如下解释初始化:

```C++
// 无法按预期工作
constexpr std::array<House, 3> houses { // 初始化 houses
    { 13, 1, 7 }, // 初始化 C 样式数组 implementation_defined_name
    { 14, 2, 5 }, // ?
    { 15, 2, 4 }  // ?
};
```

编译器将把{13,1,7}解释为houses的第一个成员的初始值设定项，这是具有实现定义名称的C样式数组。这将使用{13,1,7}初始化C样式数组元素0，其余成员将被零初始化。然后编译器会发现我们又提供了两个初始化值（{14，2，5}和{15，2，4}），并产生一个编译错误，告诉我们提供了太多的初始化值。

初始化上述的正确方法是添加一组额外的大括号，如下所示:

```C++
// 按预期工作
constexpr std::array<House, 3> houses { // 初始化 houses
    { // 额外的大括号，用来初始化作为成员变量的C样式数组 implementation_defined_name
        { 13, 4, 30 }, // 初始化元素 0
        { 14, 3, 10 }, // 初始化元素 1
        { 15, 3, 40 }, // 初始化元素 2
     }
};
```

请注意所需的额外大括号（在std::array结构体中开始的C样式数组成员的初始化）。在这个大括号中，可以单独初始化每个元素，每个元素都在自己的大括号中。

这就是为什么当元素类型需要值列表，并且我们没有显式地将元素类型作为初始值设定项的一部分提供时，将看到带有一组额外大括号的std::array初始化方式。

下面是一个完整的示例:

```C++
#include <array>
#include <iostream>

struct House
{
    int number{};
    int stories{};
    int roomsPerStory{};
};

int main()
{
    constexpr std::array<House, 3> houses {{ // 注意这里有两个大括号
        { 13, 1, 7 },
        { 14, 2, 5 },
        { 15, 2, 4 }
    }};

    for (const auto& house : houses)
    {
        std::cout << "House number " << house.number
                  << " has " << (house.stories * house.roomsPerStory)
                  << " rooms.\n";
    }

    return 0;
}
```

{{< alert success >}}
**注**

我们还没有介绍C样式数组，但出于本课的目的，您只需要知道的是“T implementation_defined_name\[N\];”代表的是 T类型的N个元素的固定大小数组。

本章后续会对C样式数组进行介绍。

{{< /alert >}}

{{< alert success >}}
**关键点**

当使用结构体、类或数组初始化std::array，并且不为每个初始值设定项提供元素类型时，您将需要一对额外的大括号，以便编译器正确解释要初始化的内容。

这是聚合初始化的需要，在这些情况下，其他标准库容器类型（使用列表构造函数）不需要双大括号。

{{< /alert >}}

***
## 大括号的省略

鉴于上述解释，您可能会想知道为什么上面的情况需要双大括号，但我们看到的所有其他情况都只需要单大括号:

```C++
#include <array>
#include <iostream>

int main()
{
    constexpr std::array<int, 5> arr { 1, 2, 3, 4, 5 }; // 单个大括号

    for (const auto n : arr)
        std::cout << n << '\n';

    return 0;
}
```

事实证明，您可以为此类数组提供双大括号:

```C++
#include <array>
#include <iostream>

int main()
{
    constexpr std::array<int, 5> arr {{ 1, 2, 3, 4, 5 }}; // 双大括号

    for (const auto n : arr)
        std::cout << n << '\n';

    return 0;
}
```

C++中的聚合支持一个名为大括号省略的概念，它为何时可以省略多个大括号制定了一些规则。通常，在使用单个值初始化std::array时，或者在使用类类型或数组进行初始化时，可以省略大括号，其中每个元素必须显式带上类型。

始终用双大括号初始化std::array没有坏处，因为它避免了必须考虑大括号省略是否适用于特定情况。或者，您可以尝试使用单大括号初始化，如果编译器无法识别它，它通常会告警。在这种情况下，可以快速添加一组额外的大括号。

***
## 另一个例子

这里还有一个例子，我们用Student结构初始化std::array。

```C++
#include <array>
#include <iostream>
#include <string_view>

// 每个学生有一个 id 和 name
struct Student
{
	int id{};
	std::string_view name{};
};

// 有 3 个学生的数组 (因为这里指明了类型，所以单括号足够了)
constexpr std::array students{ Student{0, "Alex"}, Student{ 1, "Joe" }, Student{ 2, "Bob" } };

const Student* findStudentById(int id)
{
	// 遍历所有学生
	for (auto& s : students)
	{
		// 返回指定id的学生
		if (s.id == id) return &s;
	}

	// 没有匹配到对应的id
	return nullptr;
}

int main()
{
	constexpr std::string_view nobody { "nobody" };

	const Student* s1 { findStudentById(1) };
	std::cout << "You found: " << (s1 ? s1->name : nobody) << '\n';

	const Student* s2 { findStudentById(3) };
	std::cout << "You found: " << (s2 ? s2->name : nobody) << '\n';

	return 0;
}
```

这将打印:

```C++
You found: Joe
You found: nobody
```

注意，由于std::array students是constexpr，因此findStudentById()函数必须返回常量指针，这意味着main()中的Student指针也必须是const。

***

{{< prevnext prev="/basic/chapter17/arr-pass-ret/" next="/basic/chapter17/arr-ref/" >}}
17.2 std::array作为函数参数或返回值
<--->
17.4 通过std::reference_wrapper创建引用的数组
{{< /prevnext >}}
