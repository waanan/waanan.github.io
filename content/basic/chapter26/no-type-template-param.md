---
title: "模板非类型参数"
date: 2025-01-22T20:47:14+08:00
---

在前面的课程中，您已经学习了如何使用类型作为模板参数来创建与类型无关的函数和类。模板类型参数是占位符，它被替换为作为参数传入的类型。

然而，类型并不是唯一可用的模板参数。模板类和函数可以使用另一种称为非类型参数的模板参数。

***
## 非类型参数

模板非类型参数是一个模板参数，其中参数的类型是预定义的，并替换为作为参数传入的constexpr值。

非类型参数可以是以下任何类型：

1. 整型
2. 枚举类型
3. 指向类对象的指针或引用
4. 指向函数的指针或引用
5. 指向类成员函数的指针或引用
6. std::nullptr_t
7. 浮点类型（C++20后）


在下面的示例中，我们创建了一个同时使用类型参数和非类型参数的非动态（静态）数组类。类型参数控制静态数组的数据类型，而int非类型参数控制静态数组的大小。

```C++
#include <iostream>

template <typename T, int size> // size 是一个 int 非类型参数
class StaticArray
{
private:
    // 非类型参数控制数组的大小
    T m_array[size] {};

public:
    T* getArray();
	
    T& operator[](int index)
    {
        return m_array[index];
    }
};

// 这里展示如何在类外部定义带非类型模版参数的函数
template <typename T, int size>
T* StaticArray<T, size>::getArray()
{
    return m_array;
}

int main()
{
    // 声明装了12个int的数组
    StaticArray<int, 12> intArray;

    // 按顺序填装，然后逆序打印
    for (int count { 0 }; count < 12; ++count)
        intArray[count] = count;

    for (int count { 11 }; count >= 0; --count)
        std::cout << intArray[count] << ' ';
    std::cout << '\n';

    // 声明装了4个double的数组
    StaticArray<double, 4> doubleArray;

    for (int count { 0 }; count < 4; ++count)
        doubleArray[count] = 4.4 + 0.1 * count;

    for (int count { 0 }; count < 4; ++count)
        std::cout << doubleArray[count] << ' ';

    return 0;
}
```

该代码产生以下内容：

```C++
11 10 9 8 7 6 5 4 3 2 1 0
4.4 4.5 4.6 4.7
```

关于上面的示例，值得注意的一点是，我们不必动态分配m_array成员变量！这是因为对于StaticArray类的任何给定实例，大小必须为constexpr。例如，如果实例化StaticArray\<int, 12\>，编译器将size替换为12。因此，m_array的类型为int\[12\]，可以静态分配。

此功能由标准库的类std::array使用。分配std::array\<int, 5\>时，int是类型参数，5是非类型参数！

请注意，如果尝试使用非constexpr值实例化模板非类型参数，则将无法工作：

```C++
template <int size>
class Foo
{
};

int main()
{
    int x{ 4 }; // x 不是 constexpr
    Foo<x> f; // 错误: 模版非类型参数必须是 constexpr

    return 0;
}
```

在这种情况下，编译器将发出错误。

***