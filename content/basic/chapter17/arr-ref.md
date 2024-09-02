---
title: "通过std::reference_wrapper创建引用的数组"
date: 2024-08-13T13:06:02+08:00
---

在上一课中，我们提到了数组可以包含任何对象类型的元素。这包括基本类型（例如int）的对象和具有复合类型（例如指向int的指针）的对象。

```C++
#include <array>
#include <iostream>
#include <vector>

int main()
{
    int x { 1 };
    int y { 2 };

    [[maybe_unused]] std::array valarr { x, y };   // int 数组
    [[maybe_unused]] std::vector ptrarr { &x, &y }; // 指针数组
    
    return 0;
}
```

然而，由于引用不是对象，因此不能创建引用数组。数组的元素也必须是可分配的，并且不能重新放置引用。

```C++
#include <array>
#include <iostream>

int main()
{
    int x { 1 };
    int y { 2 };

    [[maybe_unused]] std::array<int&, 2> refarr { x, y }; // 编译失败: 不能创建引用的数据

    int& ref1 { x };
    int& ref2 { y };
    [[maybe_unused]] std::array valarr { ref1, ref2 }; // ok: 这是一个 std::array<int, 2>, 而不是引用的数组

    return 0;
}
```

如果需要引用数组，有一个解决方法。

在本课中，将在示例中使用std::array，但这同样适用于所有数组类型。

***
## std::reference_wrapper

std::reference_wrapper是一个标准库类模板，位于\<functional\>头文件中。它接受类型模板参数T，然后表现得像对T的可修改左值引用。

关于std::reference_wrapper，有几点值得注意:

1. Operator=将重置std::reference_wrapper（更改正在引用的对象）。
2. std::reference_wrapper\<T\>将隐式转换为T&。
3. get()成员函数可用于获取T&。当我们想要更新被引用对象的值时，这很有用。


下面是一个简单的例子:

```C++
#include <array>
#include <functional> // for std::reference_wrapper
#include <iostream>

int main()
{
    int x { 1 };
    int y { 2 };
    int z { 3 };

    std::array<std::reference_wrapper<int>, 3> arr { x, y, z };
    
    arr[1].get() = 5; // 修改下标 1 处的值

    std::cout << arr[1] << y << '\n'; // 修改了 arr[1] 和 y, 打印 55
    
    return 0;
}
```

此示例打印以下内容:

```C++
55
```

请注意，我们必须使用arr\[1\].get()=5，而不是arr\[1\]=5。后者是不明确的，因为编译器无法判断我们是否打算将std::reference_wrapper\<int\>重置为值5（无论如何都是非法的）或更改正在引用的值。使用get（）可以消除这一点的歧义。

当打印arr\[1\]时，编译器将意识到它不能打印std::reference_wrapper\<int\>，因此它将隐式地将其转换为int&，然后可以打印它。因此，不需要在这里使用get()。

***
## std::ref和std::cref

在C++17之前，CTAD（类模板参数演绎）不存在，因此需要显式列出类类型的所有模板参数。因此，要创建std::reference_wrapper\<int\>，可以执行以下任一操作:

```C++
    int x { 5 };

    std::reference_wrapper<int> ref1 { x };        // C++11
    auto ref2 { std::reference_wrapper<int>{ x }}; // C++11
```

在长的名称和必须显式列出模板参数的方式之下，创建许多这样的引用包装器可能是一件痛苦的事情。

为了简化操作，c++提供了std::ref()和std::cref()函数作为快捷方式来创建std::reference_wrapper和con std::reference_ wrapper包装的对象。请注意，这些函数可以与auto一起使用，以避免必须显式指定模板参数。

```C++
    int x { 5 };
    auto ref { std::ref(x) };   // C++11, 推导为 std::reference_wrapper<int>
    auto cref { std::cref(x) }; // C++11, 推导为 std::reference_wrapper<const int>
```

当然，既然我们在C++17中有了CTAD，我们也可以这样做:

```C++
    std::reference_wrapper ref1 { x };        // C++17
    auto ref2 { std::reference_wrapper{ x }}; // C++17
```

但由于std::ref()和std::cref()的拼写较短，因此它们仍然广泛用于创建std::reference_wrapper对象。

***

{{< prevnext prev="/basic/chapter17/arr-of-class/" next="/basic/chapter17/arr-enum/" >}}
17.3 std::array与类类型元素
<--->
17.5 std::array和枚举
{{< /prevnext >}}
