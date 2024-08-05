---
title: "传递std::vector"
date: 2024-07-08T11:10:28+08:00
---

类型为std::vector的对象可以像任何其他对象一样传递给函数。这意味着，如果按值传递std::vector，将生成一个昂贵的副本。因此，通常通过（const）引用传递std::vector以避免这种复制。

对于std::vector，存储的元素类型是对象类型信息的一部分。因此，当使用std::vector作为函数参数时，必须显式指定元素类型：

```C++
#include <iostream>
#include <vector>

void passByRef(const std::vector<int>& arr) // 这里必须显示指定 <int>
{
    std::cout << arr[0] << '\n';
}

int main()
{
    std::vector primes{ 2, 3, 5, 7, 11 };
    passByRef(primes);

    return 0;
}
```

***
## 传递不同元素类型的std::vector

由于passByRef()函数需要std::vector\<int\>，因此无法传递具有不同元素类型的vector：

```C++
#include <iostream>
#include <vector>

void passByRef(const std::vector<int>& arr)
{
    std::cout << arr[0] << '\n';
}

int main()
{
    std::vector primes{ 2, 3, 5, 7, 11 };
    passByRef(primes);  // ok: 这是 std::vector<int>

    std::vector dbl{ 1.1, 2.2, 3.3 };
    passByRef(dbl); // 编译失败: std::vector<double> 不能转换为 std::vector<int>

    return 0;
}
```

在C++17或更新版本中，或许您想尝试使用CTAD来解决此问题：

```C++
#include <iostream>
#include <vector>

void passByRef(const std::vector& arr) // 编译失败: CTAD 不能被用来推导函数参数
{
    std::cout << arr[0] << '\n';
}

int main()
{
    std::vector primes{ 2, 3, 5, 7, 11 }; // okay: 使用 CTAD 推导为 std::vector<int>
    passByRef(primes);

    return 0;
}
```

尽管在定义vector变量时，CTAD可以从初始值设定项中推断出它的元素类型，但CTAD（目前）不能处理函数参数。

我们以前见过这种问题，只有参数类型不同的重载函数。这是一个使用函数模板的好地方！可以创建一个元素类型作为模版参数的函数模板，然后C++将使用该函数模板来实例化具有实际类型的函数。

可以创建如下的函数模板：

```C++
#include <iostream>
#include <vector>

template <typename T>
void passByRef(const std::vector<T>& arr)
{
    std::cout << arr[0] << '\n';
}

int main()
{
    std::vector primes{ 2, 3, 5, 7, 11 };
    passByRef(primes); // ok: 编译器会实例化 passByRef(const std::vector<int>&)

    std::vector dbl{ 1.1, 2.2, 3.3 };
    passByRef(dbl);    // ok: 编译器会实例化 passByRef(const std::vector<double>&)

    return 0;
}
```

在上面的示例中，创建了一个名为passByRef()的函数模板，该模板具有类型为"const std::vector\<T\>&"的参数。T在上一行的模板参数声明中定义：template \<typename T\>。T是一个标准的类型模板参数，允许调用方指定元素类型。

因此，当从 main() 调用 passByRef(primes) 时（其中primes定义为std::vector\<int\>），编译器将实例化并调用void passByRef(const std::vector\<int\>& arr)。

当从 main() 调用 passByRef(dbl) 时（其中dbl定义为std::vector\<double\>），编译器将实例化并调用void passByRef(const std::vector\<double\>& arr)。

因此，我们创建了一个函数模板，可以实例化函数来处理任何元素类型和长度的std::vector参数！

***
## 使用通用模板或缩写函数模板传递std::vector

我们还可以创建一个函数模板，该模板将接受任何类型的对象：

```C++
#include <iostream>
#include <vector>

template <typename T>
void passByRef(const T& arr) // 将会接收有任意 operator[] 方法的arr对象
{
    std::cout << arr[0] << '\n';
}

int main()
{
    std::vector primes{ 2, 3, 5, 7, 11 };
    passByRef(primes); // ok: 编译器会实例化 passByRef(const std::vector<int>&)

    std::vector dbl{ 1.1, 2.2, 3.3 };
    passByRef(dbl);    // ok: 编译器会实例化 passByRef(const std::vector<double>&)

    return 0;
}
```

在C++20中，可以使用缩写的函数模板（通过auto参数）来执行相同的操作：

```C++
#include <iostream>
#include <vector>

void passByRef(const auto& arr) // 缩写函数模板
{
    std::cout << arr[0] << '\n';
}

int main()
{
    std::vector primes{ 2, 3, 5, 7, 11 };
    passByRef(primes); // ok: 编译器会实例化 passByRef(const std::vector<int>&)

    std::vector dbl{ 1.1, 2.2, 3.3 };
    passByRef(dbl);    // ok: 编译器会实例化 passByRef(const std::vector<double>&)

    return 0;
}
```

这两个模版都将接受任何类型的将编译的参数。在编写希望对不仅仅是std::vector进行操作的函数时，这是理想的。例如，上面的函数也可以在std::array、std::string或我们甚至没有考虑过的其他类型上工作。

该方法的潜在缺点是，如果函数被传递给一个能编译过但在语义上没有意义的类型的对象，它可能会导致错误。

***
## 断言数组长度

考虑以下模板函数，该函数类似于上面给出的函数：

```C++
#include <iostream>
#include <vector>

template <typename T>
void printElement3(const std::vector<T>& arr)
{
    std::cout << arr[3] << '\n';
}

int main()
{
    std::vector arr{ 9, 7, 5, 3, 1 };
    printElement3(arr);

    return 0;
}
```

虽然printElement3(arr)在这种情况下工作良好，但在该程序中有一个潜在的错误等待粗心的程序员。看到了吗？

上面的程序打印索引为3的数组元素的值。只要数组具有索引为3的有效元素，这是可以的。然而，编译器很乐意让您传入索引3超出界限的数组。例如：

```C++
#include <iostream>
#include <vector>

template <typename T>
void printElement3(const std::vector<T>& arr)
{
    std::cout << arr[3] << '\n';
}

int main()
{
    std::vector arr{ 9, 7 }; // 只有2个元素的数组 (下标只有 0 和 1 有效)
    printElement3(arr);

    return 0;
}
```

这会导致未定义的行为。

这里的一个选项是对arr.size()进行断言，当在调试模式配置中运行时，它将捕获此类错误。由于 std::vector::size() 是一个非常量表达式函数，因此只能在运行时断言。

最好的选择是避免对传入的数组长度进行假设。

***

{{< prevnext prev="/basic/chapter16/vec-len/" next="/basic/chapter16/vec-ret-move/" >}}
16.2 vector与无符号长度和下标问题
<--->
16.4 返回std::vector，移动语义简介
{{< /prevnext >}}
