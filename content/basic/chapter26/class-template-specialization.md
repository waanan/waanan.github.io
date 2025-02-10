---
title: "类模板特化"
date: 2025-01-22T20:47:14+08:00
---

在上一课中，我们看到了如何特化函数，以便为特定数据类型提供不同的功能。事实证明，不仅可以特化函数，还可以特化类！

考虑这样一种情况，您需要一个存储8个对象的类。下面是一个简化的类模板：

```C++
#include <iostream>

template <typename T>
class Storage8
{
private:
    T m_array[8];

public:
    void set(int index, const T& value)
    {
        m_array[index] = value;
    }

    const T& get(int index) const
    {
        return m_array[index];
    }
};

int main()
{
    // 定义int的 Storage8
    Storage8<int> intStorage;

    for (int count{ 0 }; count < 8; ++count)
        intStorage.set(count, count);

    for (int count{ 0 }; count < 8; ++count)
        std::cout << intStorage.get(count) << '\n';

    // 定义bool的 Storage8
    Storage8<bool> boolStorage;
    for (int count{ 0 }; count < 8; ++count)
        boolStorage.set(count, count & 3);

	std::cout << std::boolalpha;

    for (int count{ 0 }; count < 8; ++count)
    {
        std::cout << boolStorage.get(count) << '\n';
    }

    return 0;
}
```

此示例打印

```C++
0
1
2
3
4
5
6
7
false
true
true
true
false
true
true
true
```

该类完全是展示性的，Storage8\<bool\>的实现效率很低。由于所有变量都必须有地址，并且CPU不能寻址任何小于一个字节的内容，因此所有变量的大小都必须至少为一个字节。因此，bool类型的变量最终使用整个字节，即使从技术上讲，它只需要一个bit位来存储其true或false值！因此，布尔值是1位有用的信息和7位浪费的空间。我们的Storage8\<bool\>类包含8个bool，相当于1个字节的有用信息和7个字节的浪费空间。

事实证明，使用一些基本的位运算，可以将所有8个布尔值压缩为单个字节，从而完全消除浪费的空间。然而，为了做到这一点，当与类型bool一起使用时，我们需要修改该类，将8个bool的数组替换为大小为单个字节的变量。虽然我们可以创建一个全新的类来这样做，但这有一个缺点：我们必须给它一个不同的名称。然后，程序员必须记住，Storage8\<T\>是用于非布尔类型的，而Storage8Bool（或我们命名的新类）是用于bool的。这是我们希望避免的不必要的复杂性。幸运的是，C++为我们提供了一种更好的方法：类模板特化。

***
## 类模板特化

类模板特化允许我们特化特定的模板类。在这种情况下，我们将使用类模板特化来编写Storage8\<bool\>的定制版本，该版本将优先于通用Storage8\<T\>类。类模板特化被视为完全独立的类，即使它们是以与模板化类相同的方式实例化的。这意味着我们可以改变关于特化类的任何东西，包括它的实现方式，甚至它公开的函数，就像它是一个独立的类一样。

就像所有模板一样，编译器必须能够看到特化的完整定义才能使用它。定义类模板特化需要首先定义非特化的类。

下面是专用Storage8\<bool\>类的一个示例：

```C++
#include <cstdint>

// 首先定义非特化的类模版
template <typename T>
class Storage8
{
private:
    T m_array[8];

public:
    void set(int index, const T& value)
    {
        m_array[index] = value;
    }

    const T& get(int index) const
    {
        return m_array[index];
    }
};

// 现在定义特化的类模版
template <> // 下面是无模版参数的类模版
class Storage8<bool> // 针对 bool 特化 Storage8
{
// 下面是标准的类实现细节

private:
    std::uint8_t m_data{};

public:
    // 不用完全操心这里的实现细节
    void set(int index, bool value)
    {
        // 找到要操作的bit
        // 然后我们会给对应的bit赋值
        auto mask{ 1 << index };

        if (value)  // 如果需要set 对应的bit 为 1
            m_data |= mask;   // 使用 bit - or 来进行操作 
        else  // 如果需要设置对应的 bit 为 0
            m_data &= ~mask;  // 使用 bit - and 来进行操作
	}

    bool get(int index)
    {
        // 找到要读取的bit
        auto mask{ 1 << index };
        // bit - and 提取对应位置的值
        // 结果会隐式的转换为 bool
        return (m_data & mask);
    }
};

// 一些使用样例
int main()
{
    // 定义int的 Storage8  (实例化 Storage8<T>, T = int)
    Storage8<int> intStorage;

    for (int count{ 0 }; count < 8; ++count)
    {
        intStorage.set(count, count);
	}

    for (int count{ 0 }; count < 8; ++count)
    {
        std::cout << intStorage.get(count) << '\n';
    }

    // 定义bool的 Storage8  (实例化 Storage8<bool> 特化版本)
    Storage8<bool> boolStorage;

    for (int count{ 0 }; count < 8; ++count)
    {
        boolStorage.set(count, count & 3);
    }

	std::cout << std::boolalpha;

    for (int count{ 0 }; count < 8; ++count)
    {
        std::cout << boolStorage.get(count) << '\n';
    }

    return 0;
}
```

首先，请注意，我们的特化类模板以模板\<\>开始。template关键字告诉编译器后面是模板，空的尖括号表示没有任何模板参数。在这种情况下，没有任何模板参数，因为我们将唯一的模板参数（T）替换为特定类型（bool）。

接下来，我们将\<bool\>添加到类名中，表示我们特化了类Storage8的bool版本。

所有其他更改都只是类实现细节。为了使用该类，您不需要理解位逻辑是如何工作的。

请注意，该特化类使用std::uint8_t（1字节无符号int）。

现在，当我们实例化对象类型Storage\<T\>时，其中T不是bool，我们将获得从通用Storage8\<T\>类模板化的版本。当我们实例化Storage8\<bool\>类型的对象时，我们将获得刚刚创建的专用版本。请注意，我们保持了两个类的公开接口相同——虽然C++为我们提供了根据需要添加、删除或更改Storage8\<bool\>函数的自由支配权，但保持一致的接口意味着程序员可以以完全相同的方式使用这两个类。

正如您所料，这将打印与使用Storage8\<bool\>的非特化版本的上一个示例相同的结果：

```C++
0
1
2
3
4
5
6
7
false
true
true
true
false
true
true
true
```

***
## 特化成员函数

在上一课中，我们介绍了以下示例：

```C++
#include <iostream>

template <typename T>
class Storage
{
private:
    T m_value {};
public:
    Storage(T value)
      : m_value { value }
    {
    }

    void print()
    {
        std::cout << m_value << '\n';
    }
};

int main()
{
    // 定义一些 storage
    Storage i { 5 };
    Storage d { 6.7 };

    // 进行打印
    i.print();
    d.print();
}
```

我们的愿望是特化print()函数，以便它以科学记数法打印双精度。使用类模板特化，我们可以为Storage定义一个特化的类：

```C++
#include <iostream>

template <typename T>
class Storage
{
private:
    T m_value {};
public:
    Storage(T value)
      : m_value { value }
    {
    }

    void print()
    {
        std::cout << m_value << '\n';
    }
};

// 显示特化 Storage<double> 类
// 注意下面有大量的重复
template <>
class Storage<double>
{
private:
    double m_value {};
public:
    Storage(double value)
      : m_value { value }
    {
    }

    void print();
};

// 在外名定义函数，因为这样会让类声明简短
// 这是一个普通（非特化）成员函数定义（它是Storage<double>类的成员函数）
void Storage<double>::print()
{
    std::cout << std::scientific << m_value << '\n';
}

int main()
{
    // 定义一些 storage
    Storage i { 5 };
    Storage d { 6.7 }; // 使用特化版本 Storage<double>

    // 进行打印
    i.print(); // 调用 Storage<int>::print (实例化 Storage<T>)
    d.print(); // 调用 Storage<double>::print (实例化 显示特化的 Storage<double>)
}
```

然而，请注意这里有多少冗余。我们复制了整个类定义，以便可以更改一个成员函数！

幸运的是，我们可以做得更好。C++不要求我们显式特化Storage\<double\>来显式特化Storage\<double\>::print()。相反，我们可以让编译器从Storage\<T\>中隐式特化Storage\<double\>，并提供仅Storage\<double\>::print()的显式特化！如下所示：

```C++
#include <iostream>

template <typename T>
class Storage
{
private:
    T m_value {};
public:
    Storage(T value)
      : m_value { value }
    {
    }

    void print()
    {
        std::cout << m_value << '\n';
    }
};

// 这是一个成员函数显式特化
// 显式成员函数特化不是隐式 inline, 所以如果要放在头文件要手动标记为inline
template<>
void Storage<double>::print()
{
    std::cout << std::scientific << m_value << '\n';
}

int main()
{
    // 定义一些 storage
    Storage i { 5 };
    Storage d { 6.7 }; // 会导致 Storage<double> 实例化

    // 进行打印
    i.print(); // 调用 Storage<int>::print (实例化 Storage<T>)
    d.print(); // 调用 Storage<double>::print (实例化 显示特化的 Storage<double>::print())
}
```

就这样！

如前一课中所述，显式函数特化不是隐式内联的，因此如果在头文件中定义Storage\<double\>::print()，我们应该将其标记为inline。

***
## 定义类模板特化的位置

为了使用特化，编译器必须能够看到非特化类和特化类的完整定义。如果编译器只能看到非特化类的定义，则它将使用该定义而不是特化版本。

由于这个原因，特化的类和函数通常在非特化类的定义下方的头文件中定义，因此include单个头文件会include非特化的类别和所有特化类。这确保了只要还可以看到非特化类，就始终可以看到特化类。

如果仅在单个翻译单元中需要特化，则可以在该翻译单元的源文件中定义它。由于其他翻译单位将无法看到特化的定义，他们将继续使用非特化版本。

注意不要将特化放在其自己的单独头文件中，因为我们的目的是将特化的头文件包含在需要特化的任何翻译单元中。设计基于头文件的存在或不存在而透明地更改行为的代码是一个坏主意。例如，如果您打算使用特化，但忘记包含特化的头文件，则最终可能会使用非特化版本。如果您打算使用非特化，那么include的头文件可能传递了包含特化的头文件，您可能最终还是会使用特化版本。

***

{{< prevnext prev="/basic/chapter26/func-template-specialization/" next="/basic/chapter26/part-template-special/" >}}
26.2 函数模板特化
<--->
26.4 部分模板特化
{{< /prevnext >}}
