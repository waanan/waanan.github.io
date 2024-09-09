---
title: "多维std::array"
date: 2024-08-13T13:06:02+08:00
---

在上一课中，我们讨论了C型多维数组。

```C++
    // C 样式的 二维 数组
    int arr[3][4] { 
        { 1, 2, 3, 4 },
        { 5, 6, 7, 8 },
        { 9, 10, 11, 12 }};
```

但正如您所知，我们通常希望避免使用C样式的数组（除非它们用于存储全局数据）。

在本课中，我们将了解多维数组如何与std::array一起工作。

***
## 没有标准库多维数组类

注意，std::array实现为一维数组。因此，您应该问的第一个问题是，“是否有用于多维数组的标准库类？”答案是……没有。太糟糕了。

***
## 二维std::array

创建std::array的二维数组的标准方法是创建一个std:∶array，其中模板类型参数是另一个std::array。这导致了这样的情况:

```C++
    std::array<std::array<int, 4>, 3> arr {{  // 双重大括号
        { 1, 2, 3, 4 },
        { 5, 6, 7, 8 },
        { 9, 10, 11, 12 }}};
```

关于这一点，有许多“有趣”的事情需要注意:

1. 当初始化多维std::array时，我们需要使用双大括号（之前讨论过）。
2. 语法冗长，难以阅读。
3. 由于模板的嵌套方式，数组维度被切换。我们需要一个具有3行4个元素的数组，因此arr\[3\]\[4\]是自然的。std::array\<std::array\<int, 4\>, 3\> 则非常奇怪。


索引二维std::array元素的工作方式与索引二维C样式数组类似:

```C++
    std::cout << arr[1][2]; // 打印第1行2列
```

我们还可以将二维std::array传递给函数，就像一维std::array:

```C++
#include <array>
#include <iostream>

template <typename T, std::size_t Row, std::size_t Col>
void printArray(const std::array<std::array<T, Col>, Row> &arr)
{
    for (const auto& arow: arr)   // 获取每一行
    {
        for (const auto& e: arow) // 获取行中的每个元素
            std::cout << e << ' ';

        std::cout << '\n';
    }
}

int main()
{
    std::array<std::array<int, 4>, 3>  arr {{
        { 1, 2, 3, 4 },
        { 5, 6, 7, 8 },
        { 9, 10, 11, 12 }}};

    printArray(arr);

    return 0;
}
```

真恶心。这是一个二维std::array。三维或更高的std::array甚至更冗长！

***
## 使用别名模板简化二维std::array

在之前我们介绍了类型别名，并注意到类型别名的用途之一是使复杂类型更易于使用。然而，对于普通类型别名，我们必须显式指定所有模板参数。例如。

```C++
using Array2dint34 = std::array<std::array<int, 4>, 3>;
```

这允许我们在需要int的3×4二维std::array的任何位置使用Array2dint34。但请注意，对于要使用的元素类型和维度的每个组合，我们都需要一个这样的别名！

这是使用别名模板的完美地方，它允许我们将类型别名的元素类型、行长度和列长度指定为模板参数！

```C++
// 二维 std::array 的别名模版
template <typename T, std::size_t Row, std::size_t Col>
using Array2d = std::array<std::array<T, Col>, Row>;
```

然后，我们可以在任何需要int的3×4二维std::array的地方使用Array2d\<int，3，4\>。这要好得多！

下面是一个完整的示例:

```C++
#include <array>
#include <iostream>

// 二维 std::array 的别名模版
template <typename T, std::size_t Row, std::size_t Col>
using Array2d = std::array<std::array<T, Col>, Row>;

// 使用 Array2d 作为函数参数，需要指定模版参数
template <typename T, std::size_t Row, std::size_t Col>
void printArray(const Array2d<T, Row, Col> &arr)
{
    for (const auto& arow: arr)   // 获取每一个行
    {
        for (const auto& e: arow) // 获取行中的每个元素
            std::cout << e << ' ';

        std::cout << '\n';
    }
}

int main()
{
    // 定义3行4列的二维数组
    Array2d<int, 3, 4> arr {{
        { 1, 2, 3, 4 },
        { 5, 6, 7, 8 },
        { 9, 10, 11, 12 }}};

    printArray(arr);

    return 0;
}
```

请注意，这是多么简洁和易于使用！

关于别名模板的一个妙处是，我们可以以任何顺序定义模板参数。由于std::array首先指定元素类型，然后指定维度。但我们可以灵活地首先定义行或列。由于C样式的数组定义是首先定义行的，因此我们使用先行后列来定义别名模板。

该方法还可以很好地扩展到更高维的std::array:

```C++
// 三维 std::array 的别名模版
template <typename T, std::size_t Row, std::size_t Col, std::size_t Depth>
using Array3d = std::array<std::array<std::array<T, Depth>, Col>, Row>;
```

***
## 获取二维数组的维数长度

对于一维std::arry，我们可以使用size()成员函数（或std:∶size()）来获取数组的长度。但当我们有一个二维std::array时，我们该怎么办呢？在这种情况下，size()将仅返回第一个维度的长度。

一个看似有吸引力（但潜在危险）的选项是获取所需维度的元素，然后对该元素调用size():

```C++
#include <array>
#include <iostream>

// 二维 std::array 的别名模版
template <typename T, std::size_t Row, std::size_t Col>
using Array2d = std::array<std::array<T, Col>, Row>;

int main()
{
    // 定义3行4列的二维数组
    Array2d<int, 3, 4> arr {{
        { 1, 2, 3, 4 },
        { 5, 6, 7, 8 },
        { 9, 10, 11, 12 }}};

    std::cout << "Rows: " << arr.size() << '\n';    // 获取第一个维度的长度 (行)
    std::cout << "Cols: " << arr[0].size() << '\n'; // 获取第二个维度的长度 (列), 如果第一个维度的长度为0，则该行为结果未定义!

    return 0;
}
```

为了获得第一个维度的长度，我们对数组调用size()。为了获得第二个维度的长度，我们首先调用arr\[0\]来获得第一个元素，然后对其调用size()。为了获得三维数组的第三维度的长度，我们将调用arr\[0\]\[0\].size（）。

然而，上面的代码是有缺陷的，因为如果除最后一个维度之外的任何维度的长度为0，它将产生未定义的行为！

更好的选择是使用函数模板直接从关联的非类型模板参数返回维度的长度:

```C++
#include <array>
#include <iostream>

// 二维 std::array 的别名模版
template <typename T, std::size_t Row, std::size_t Col>
using Array2d = std::array<std::array<T, Col>, Row>;

// 从非类型模板参数获取行的长度
template <typename T, std::size_t Row, std::size_t Col>
constexpr int rowLength(const Array2d<T, Row, Col>&)
{
    return Row;
}

// 从非类型模板参数获取列的长度
template <typename T, std::size_t Row, std::size_t Col>
constexpr int colLength(const Array2d<T, Row, Col>&)
{
    return Col;
}

int main()
{
    // 定义3行4列的二维数组
    Array2d<int, 3, 4> arr {{
        { 1, 2, 3, 4 },
        { 5, 6, 7, 8 },
        { 9, 10, 11, 12 }}};

    std::cout << "Rows: " << rowLength(arr) << '\n'; // 获取第一个维度的长度 (行)
    std::cout << "Cols: " << colLength(arr) << '\n'; // 获取第二个维度的长度 (列)

    return 0;
}
```

如果任何维度的长度为零，则这可以避免任何未定义的行为，因为它仅使用数组的类型信息，而不是数组的实际数据。这还允许我们根据需要轻松地将长度返回为int（不需要static_cast，因为从constexpr std::size_t转换为constexpr-int是非窄化的，因此隐式转换可以正常工作）。

***
## 展平二维数组

具有两个或多个维度的数组具有一些挑战:

1. 它们的定义和使用更加详细。
2. 获取维度数据的逻辑比较奇怪。
3. 它们越来越难迭代（每个维度都需要一个循环）。


使多维数组更易于使用的一种方法是展平它们。展平数组是降低数组维数的过程（通常降到单个维数）。

例如，我们可以创建具有Row*Col元素的一维数组，而不是创建具有Row行和Col列的二维数组。这使用单个维度为我们提供了相同的存储量。

然而，由于一维数组只有一个维度，因此不能将其作为多维数组使用。为了解决这个问题，我们可以提供一个模拟多维数组的接口。该接口将接受二维坐标，然后将它们映射到一维数组中的唯一位置。

下面是在C++11或更新版本中工作的这种方法的一个示例:

```C++
#include <array>
#include <iostream>
#include <functional>

// 看起来有两个维度的一维数组
template <typename T, std::size_t Row, std::size_t Col>
using ArrayFlat2d = std::array<T, Row * Col>;

// 允许我们按照二维数组使用一维数组的可修改视图
template <typename T, std::size_t Row, std::size_t Col>
class ArrayView2d
{
private:
    // 你可能想让 ArrayFlat2d 是指向arr的一个引用,
    // 但这样会让view无法拷贝，因为引用无法重置.
    // 使用 std::reference_wrapper 可以给我们引用语义的同时，仍然可以赋值.
    std::reference_wrapper<ArrayFlat2d<T, Row, Col>> m_arr {};

public:
    ArrayView2d(ArrayFlat2d<T, Row, Col> &arr)
        : m_arr { arr }
    {}

    // 使用一维下标访问 (使用 operator[])
    T& operator[](int i) { return m_arr.get()[static_cast<std::size_t>(i)]; }
    const T& operator[](int i) const { return m_arr.get()[static_cast<std::size_t>(i)]; }

    // 使用二维下标访问 (使用 operator(), 因为C++23之前 operator[] 不支持多维参数)
    T& operator()(int row, int col) { return m_arr.get()[static_cast<std::size_t>(row * cols() + col)]; }
    const T& operator()(int row, int col) const { return m_arr.get()[static_cast<std::size_t>(row * cols() + col)]; }

    // 在 C++23, 可以取消下面的注释，因为可以支持多个参数的operator[]了
//    T& operator[](int row, int col) { return m_arr.get()[static_cast<std::size_t>(row * cols() + col)]; }
//    const T& operator[](int row, int col) const { return m_arr.get()[static_cast<std::size_t>(row * cols() + col)]; }

    int rows() const { return static_cast<int>(Row); }
    int cols() const { return static_cast<int>(Col); }
    int length() const { return static_cast<int>(Row * Col); }
};

int main()
{
    // 定义 一维 数组 (3 行 4 列)
    ArrayFlat2d<int, 3, 4> arr {
        1, 2, 3, 4,
        5, 6, 7, 8,
        9, 10, 11, 12 };

    // 定义一维数组的二维视图
    ArrayView2d<int, 3, 4> arrView { arr };

    // 打印维度
    std::cout << "Rows: " << arrView.rows() << '\n';
    std::cout << "Cols: " << arrView.cols() << '\n';

    // 使用单个维度访问
    for (int i=0; i < arrView.length(); ++i)
        std::cout << arrView[i] << ' ';

    std::cout << '\n';

    // 使用两个维度访问
    for (int row=0; row < arrView.rows(); ++row)
    {
        for (int col=0; col < arrView.cols(); ++col)
            std::cout << arrView(row, col) << ' ';
        std::cout << '\n';
    }

    std::cout << '\n';

    return 0;
}
```

这将打印:

```C++
Rows: 3
Cols: 4
1 2 3 4 5 6 7 8 9 10 11 12
1 2 3 4
5 6 7 8
9 10 11 12
```

由于C++23之前，运算符[]只能接受的单个下标，因此有两种替代方法:

1. 请改用operator()，它可以接受多个下标。这使您可以使用[]进行单维度访问，使用（）进行多维索引。我们在上面选择了这种方法。
2. 让运算符[]返回一个子视图，该子视图也重载运算符[]，以便可以连接运算符[]。这更复杂，不能很好地扩展到更高的维度。


在C++23中，操作符[]被扩展为接受多个下标，因此您可以重载它来处理单个和多个下标。

***
## std::mdspan （C++23）

在C++23中引入的std::mdspan是一个可修改的视图，为连续的一维元素序列提供多维数组接口。std::mdspan不仅仅是只读视图（如std:∶string_view）——如果元素的底层序列是非常量的，则可以修改这些元素。

下面的示例打印与前面的示例相同的输出，但使用std::mdspan而不是我们自己的自定义视图:

```C++
#include <array>
#include <iostream>
#include <mdspan>

// 看起来有两个维度的一维数组
template <typename T, std::size_t Row, std::size_t Col>
using ArrayFlat2d = std::array<T, Row * Col>;

int main()
{
    // 定义 一维 数组 (3 行 4 列)
    ArrayFlat2d<int, 3, 4> arr {
        1, 2, 3, 4,
        5, 6, 7, 8,
        9, 10, 11, 12 };

    // 在 arr 上，定义一个二维的 span
    // std::mdspan需要数据的地址
    // 可以通过 data() 成员函数获取 std::array 或 std::vector 数据的地址
    std::mdspan mdView { arr.data(), 3, 4 };

    // 打印数组维度
    // std::mdspan 中称为 extents
    std::size_t rows { mdView.extents().extent(0) };
    std::size_t cols { mdView.extents().extent(1) };
    std::cout << "Rows: " << rows << '\n';
    std::cout << "Cols: " << cols << '\n';

    // 按一维进行打印
    // data_handle() 成员函数，提供一维的视图的访问
    // 对应我们的索引
    for (std::size_t i=0; i < mdView.size(); ++i)
        std::cout << mdView.data_handle()[i] << ' ';
    std::cout << '\n';

    // 按二维进行打印
    // 使用 multidimensional [] 访问元素
    for (std::size_t row=0; row < rows; ++row)
    {
        for (std::size_t col=0; col < cols; ++col)
            std::cout << mdView[row, col] << ' ';
        std::cout << '\n';
    }
    std::cout << '\n';

    return 0;
}
```

这应该相当简单，但有几点值得注意:

1. mdspan让我们定义一个具有任意多个维度的视图。
2. std::mdspan的构造函数的第一个参数应该是数组数据的指针。这可以是退化的C样式数组，或者我们可以使用std::array或std::vector的data（）成员函数来获取该数据。
3. 要在一维中索引std::mdspan，我们必须获取数组数据的指针，这可以使用data_handle()成员函数来完成。然后我们使用下标访问。
4. 在C++23中，操作符[]接受多个索引，因此我们使用\[row，col\]作为索引，而不是\[row\]\[col\]。

C++26将引入std::mdarray，它本质上是将std:∶array和std::mdspan结合到一个多维数组中！

***

{{< prevnext prev="/basic/chapter17/c-multi-arr/" next="/basic/chapter17/summary/" >}}
17.11 多维C样式数组
<--->
17.13 第17章总结
{{< /prevnext >}}
