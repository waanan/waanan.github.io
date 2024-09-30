---
title: "重载下标运算符"
date: 2024-08-20T12:01:51+08:00
---

使用数组时，我们通常使用下标运算符（[]）来索引数组的特定元素：

```C++
myArray[0] = 7; // 将7赋值给数组的第0个元素
```

然而，考虑以下IntList类，该类有数组作为成员变量：

```C++
class IntList
{
private:
    int m_list[10]{};
};

int main()
{
    IntList list{};
    // 如何从 m_list 访问元素?
    return 0;
}
```

由于m_list成员变量是私有的，因此不能直接从变量m_list中访问它。这意味着无法直接获取或设置m_list数组中的值。那么，我们如何获得或将元素放入列表中呢？

在没有操作符重载的情况下，典型的方法是创建访问函数：

```C++
class IntList
{
private:
    int m_list[10]{};

public:
    void setItem(int index, int value) { m_list[index] = value; }
    int getItem(int index) const { return m_list[index]; }
};
```

虽然这是有效的，但它不是特别友好的用户。考虑以下示例：

```C++
int main()
{
    IntList list{};
    list.setItem(2, 3);

    return 0;
}
```

我们是将元素2设置为值3，还是将元素3设置为值2？在没有看到setItem（）的定义的情况下，根本不清楚。

您也可以只返回整个列表并使用 操作符[] 访问元素：

```C++
class IntList
{
private:
    int m_list[10]{};

public:
    int* getList() { return m_list; }
};
```

虽然这也有效，但在语法上很奇怪：

```C++
int main()
{
    IntList list{};
    list.getList()[2] = 3;

    return 0;
}
```

***
## 重载运算符[]

在这种情况下，更好的解决方案是重载下标运算符（[]），以允许访问m_list的元素。下标运算符是必须重载为成员函数的运算符之一。重载 运算符[] 的函数将始终采用一个参数：用户放在大括号之间的下标。在IntList示例中，我们期望用户传入整数索引，并返回对应的结果。

```C++
#include <iostream>

class IntList
{
private:
    int m_list[10]{};

public:
    int& operator[] (int index)
    {
        return m_list[index];
    }
};

/*
// 也可以放在函数外实现
int& IntList::operator[] (int index)
{
    return m_list[index];
}
*/

int main()
{
    IntList list{};
    list[2] = 3; // 赋值
    std::cout << list[2] << '\n'; // 获取值

    return 0;
}
```

现在，每当我们在类的对象上使用下标操作符（[]）时，编译器将从m_list成员变量返回相应的元素！这允许我们直接获取和设置m_list的值。

这在语法上和从理解的角度来看都很容易。当list\[2\]求值时，编译器首先检查是否存在重载 运算符[] 函数。如果存在，它将括号内的值（在本例中为2）作为参数传递给函数。

请注意，尽管可以为函数参数提供默认值，但实际上使用没有下标的 运算符[] 被认为是无效的语法，无法编译通过。

{{< alert success >}}
**提示**

C++23增加了对具有多个下标的重载 运算符[] 的支持。

{{< /alert >}}

***
## 运算符[]返回引用的原因

让我们仔细看看  list\[2\] = 3  是如何计算的。由于下标运算符的优先级高于赋值运算符，因此 list\[2\] 首先求值。list\[2\]调用 运算符[]，我们定义了该操作符返回对 list.mlist\[2\] 的引用。由于 运算符[] 返回引用，因此它返回实际的 list.m_list\[2\] 数组元素。这个部分表达式求值变为 list.m_list\[2\] = 3 ，这是一个简单的赋值。

赋值语句左侧的任何值都必须是左值（具有实际内存地址的变量）。由于 运算符[] 的结果可以用于赋值的左侧（例如，list\[2\] = 3），因此 运算符[] 返回的值必须是左值。事实证明，引用总是左值，因为您只能引用具有内存地址的变量。因此，通过返回引用，编译器可以确信我们正在返回左值。

考虑如果 运算符[] 按值而不是按引用返回整数，会发生什么情况。list\[2\] 将调用 操作符[]，该操作符将返回 list.mlist\[2\] 的值。例如，如果 m_list\[2\] 的值为6，则 运算符[] 将返回值6。list\[2\] = 3 的部分计算结果为 6 = 3，这没有意义！如果尝试执行此操作，C++编译器将报错：

```C++
C:VCProjectsTest.cpp(386) : error C2106: '=' : left operand must be l-value
```

***
## const对象的重载运算符[]

在上面的IntList示例中，操作符[] 是非常量，我们可以将其用作左值来更改非常量对象的状态。然而，如果IntList对象是常量，该怎么办？在这种情况下，将无法调用运算符[]的非常量版本，因为这将允许我们潜在地更改常量对象的状态。

好消息是，我们可以分别定义非常量和常量版本的 运算符[]。非常量版本将与非常量对象一起使用，而常量版本将与常量对象一起使用。

```C++
#include <iostream>

class IntList
{
private:
    int m_list[10]{ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 }; // 给定一些初始值

public:
    // 适用非常量对象，可以用来赋值
    int& operator[] (int index)
    {
        return m_list[index];
    }

    // 适用常量对象: 只能用来访问
    // 这个函数也是返回引用，来避免数据拷贝
    const int& operator[] (int index) const
    {
        return m_list[index];
    }
};

int main()
{
    IntList list{};
    list[2] = 3; // okay: 调用非 const operator[]
    std::cout << list[2] << '\n';

    const IntList clist{};
    // clist[2] = 3; // 编译会失败: clist[2] 返回 const 引用, 无法进行赋值
    std::cout << clist[2] << '\n';

    return 0;
}
```

***
## 删除常量重载和非常量重载之间的重复代码

在上面的示例中，请注意 "int& IntList::operator[]（int）" 和 "const int& IntList::operator[]（int）const" 的实现是相同的。唯一的区别是函数的返回类型。

在实现非常简单（例如，单行）的情况下，让两个函数使用相同的实现是好的（并且是首选的）。这引入的少量冗余不值得删除。

但是，如果这些操作符的实现很复杂，需要许多语句，该怎么办？例如，验证索引是否实际有效可能很重要，这需要向每个函数添加许多冗余代码行。

在这种情况下，由许多重复语句引入的冗余更成问题，并且希望有一个可以用于两个重载函数的单个实现。但如何做呢？通常，我们只需根据另一个函数来实现当前函数（例如，让一个函数调用另一个）。但在当前情况下，这有点棘手。函数的const版本不能调用函数的非const版本，因为这需要丢弃常量对象的const属性。虽然函数的非const版本可以调用函数的const版本，但当我们需要返回非const引用时，函数的const版本会返回const引用。幸运的是，有一种方法可以解决这个问题。

首选解决方案如下：

1. 实现函数的const版本的逻辑。
2. 让非const函数调用const函数，并使用const_cast删除const。


结果解决方案如下所示：

```C++
#include <iostream>
#include <utility> // for std::as_const

class IntList
{
private:
    int m_list[10]{ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 }; // 给定一些初始值

public:
    int& operator[] (int index)
    {
        // 使用 std::as_const 获取 `this` 对象的const版本 (作为引用) 
        // 以便可以调用const版本的 operator[]
        // 然后使用 const_cast 丢弃返回值的const属性
        return const_cast<int&>(std::as_const(*this)[index]);
    }

    const int& operator[] (int index) const
    {
        return m_list[index];
    }
};

int main()
{
    IntList list{};
    list[2] = 3; // okay: 调用 非const 版本的 operator[]
    std::cout << list[2] << '\n';

    const IntList clist{};
    // clist[2] = 3; // 编译失败: clist[2] 返回 const 引用, 无法进行赋值
    std::cout << clist[2] << '\n';

    return 0;
}
```

通常，使用const_cast删除const是我们希望避免的，但在这种情况下，这是可以接受的。如果调用了非const重载，则我们知道正在处理非const对象。可以删除对非常量对象的const引用上的const属性。


对于高级读者，在C++23中，通过使用本教程系列中尚未介绍的几个功能，我们可以做得更好：

```C++
#include <iostream>

class IntList
{
private:
    int m_list[10]{ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 }; // 给定一些初始值

public:
    // 使用显示对象参数 (self) 和 auto&& 去自动区分 const 和 非const
    auto&& operator[](this auto&& self, int index)
    {
        // Complex code goes here
        return self.m_list[index];
    }
};

int main()
{
    IntList list{};
    list[2] = 3; // okay: 调用 非const 版本的 operator[]
    std::cout << list[2] << '\n';

    const IntList clist{};
    // clist[2] = 3; // 编译失败: clist[2] 返回 const 引用, 无法进行赋值
    std::cout << clist[2] << '\n';

    return 0;
}
```

***
## 检测下标的有效性

重载下标操作符的另一个优点是，可以使它比直接访问数组更安全。通常，在访问数组时，下标运算符不会检查索引是否有效。例如，编译器不会对以下代码报错：

```C++
int list[5]{};
list[7] = 3; // 下标 7 超出了 list 的边界!
```

然而，如果我们知道数组的大小，可以重载下标运算符进行边界检查，以确保索引在界限内：

```C++
#include <cassert> // for assert()
#include <iterator> // for std::size()

class IntList
{
private:
    int m_list[10]{};

public:
    int& operator[] (int index)
    {
        assert(index >= 0 && static_cast<std::size_t>(index) < std::size(m_list));

        return m_list[index];
    }
};
```

在上面的示例中，我们使用了assert（）函数来确保索引有效。如果断言中的表达式的计算结果为false（这意味着用户传入了无效索引），则程序将以错误消息结束，这比访问无效数据要好得多。这可能是进行这种错误检查的最常见方法。

如果不想使用断言，则可以改用If语句或您喜欢的错误处理方法（例如引发异常、调用std::exit等）：

```C++
#include <iterator> // for std::size()

class IntList
{
private:
    int m_list[10]{};

public:
    int& operator[] (int index)
    {
        if (!(index >= 0 && static_cast<std::size_t>(index) < std::size(m_list)))
        {
            // 处理异常的索引
        }

        return m_list[index];
    }
};
```

***
## 指向对象的指针和重载运算符[]不能混用

如果试图在指向对象的指针上调用 运算符[]，C++将假定您正在尝试索引该类型对象的数组。

考虑以下示例：

```C++
#include <cassert> // for assert()
#include <iterator> // for std::size()

class IntList
{
private:
    int m_list[10]{};

public:
    int& operator[] (int index)
    {
        return m_list[index];
    }
};

int main()
{
    IntList* list{ new IntList{} };
    list [2] = 3; // 错误: 这里会认为访问的是 IntList数组的 第二个元素
    delete list;

    return 0;
}
```

因为我们不能将整数赋给IntList，所以这不会通过编译。然而，如果整数赋值是有效的，则这将通过编译并运行，结果是未定义的行为。

正确的语法是首先解引用指针（使用括号，因为 运算符[] 的优先级高于 运算符*），然后调用 运算符[]：

```C++
int main()
{
    IntList* list{ new IntList{} };
    (*list)[2] = 3; // 先获取到 IntList 对象, 然后调用重载函数 operator[]
    delete list;

    return 0;
}
```

这是丑陋的，容易出错。如果不需要，不要设置指向对象的指针。

***
## 函数参数不需要是整型

如上所述，C++将用户键入的内容作为参数传递给重载函数。在大多数情况下，这将是一个整数值。然而，这不是必需的——事实上，您可以定义重载 操作符[] 接受您想要的任何类型的值。您可以将重载 运算符[] 定义为接受double、std::string或其他任何类型的运算符。

下面是一个荒谬的例子，只是为了让您看到它的工作原理：

```C++
#include <iostream>
#include <string_view> // C++17

class Stupid
{
private:

public:
	void operator[] (std::string_view index);
};

// 让 operator[] 去打印东西，但其实有些荒谬
// 这里是为了演示，重载函数的参数不一定非是 整形
void Stupid::operator[] (std::string_view index)
{
	std::cout << index;
}

int main()
{
	Stupid stupid{};
	stupid["Hello, world!"];

	return 0;
}
```

如您所料，此打印：

```C++
Hello, world!
```

在编写某些类型的类（如使用单词作为索引的类）时，重载 运算符[] 将std::string作为参数可能很有用。

***
