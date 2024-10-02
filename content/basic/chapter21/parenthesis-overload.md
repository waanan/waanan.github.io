---
title: "重载括号运算符"
date: 2024-08-20T12:01:51+08:00
---

到目前为止，您看到的所有重载操作符都允许您定义参数的类型，但不能定义参数的数量（根据操作符的类型固定）。例如，operator==总是采用两个参数，而operator！总是要一个参数。括号操作符（ operator() ）是一个特别有趣的操作符，它允许您改变它所采用的参数的类型和数量。

有两件事需要记住：首先，括号操作符必须实现为成员函数。其次，在非面向对象的C++中，「operator()」用于调用函数。在类中，「operator()」只是一个普通的操作符，它像任何其他重载操作符一样调用函数（只是命名为「operator()」 ）。

***
## 一个例子

让我们看一个示例：

```C++
class Matrix
{
private:
    double data[4][4]{};
};
```

矩阵是线性代数的一个关键组件，通常用于进行几何建模和3D图形。在上面的示例，Matrix类是一个4×4的二维double数组。

我们可以重载「operator[]」以提供对专用一维数组的直接访问。然而，在上面的情况下，希望访问private二维数组。由于「operator[]」仅限于单个参数，因此是无能为力的。

然而，由于「operator()」可以接受任意多的参数，因此我们可以声明一个接受两个整数索引参数的「operator()」版本，并使用它访问二维数组。下面是一个例子：

```C++
#include <cassert> // for assert()

class Matrix
{
private:
    double m_data[4][4]{};

public:
    double& operator()(int row, int col);
    double operator()(int row, int col) const; // for const 对象
};

double& Matrix::operator()(int row, int col)
{
    assert(row >= 0 && row < 4);
    assert(col >= 0 && col < 4);

    return m_data[row][col];
}

double Matrix::operator()(int row, int col) const
{
    assert(row >= 0 && row < 4);
    assert(col >= 0 && col < 4);

    return m_data[row][col];
}
```

现在，我们可以声明矩阵并像这样访问其元素：

```C++
#include <iostream>

int main()
{
    Matrix matrix;
    matrix(1, 2) = 4.5;
    std::cout << matrix(1, 2) << '\n';

    return 0;
}
```

产生结果：

```C++
4.5
```

现在，让我们再次重载「operator()」，这一次新增一个不需要参数的重载函数：

```C++
#include <cassert> // for assert()
class Matrix
{
private:
    double m_data[4][4]{};

public:
    double& operator()(int row, int col);
    double operator()(int row, int col) const;
    void operator()();
};

double& Matrix::operator()(int row, int col)
{
    assert(row >= 0 && row < 4);
    assert(col >= 0 && col < 4);

    return m_data[row][col];
}

double Matrix::operator()(int row, int col) const
{
    assert(row >= 0 && row < 4);
    assert(col >= 0 && col < 4);

    return m_data[row][col];
}

void Matrix::operator()()
{
    // 将所有的值重置为 0.0
    for (int row{ 0 }; row < 4; ++row)
    {
        for (int col{ 0 }; col < 4; ++col)
        {
            m_data[row][col] = 0.0;
        }
    }
}
```

下面是新示例：

```C++
#include <iostream>

int main()
{
    Matrix matrix{};
    matrix(1, 2) = 4.5;
    matrix(); // 清空matrix
    std::cout << matrix(1, 2) << '\n';

    return 0;
}
```

产生结果：

```C++
0.0
```

由于「operator()」非常灵活，因此很容易将其用于许多不同的目的。然而，强烈不建议这样做，因为「（）」并不能真正指示操作符正在做什么。在上面的示例中，最好将清空功能编写为一个名为 clear() 或 erase() 的函数，因为 matrix.erase() 比 matrix() 的行为更容易理解。

***
## 函子（函数对象）

「operator()」通常也被重载以实现functor（函子，即函数对象），这是像函数一样操作的类对象。函子比普通函数的优点是函子可以将数据存储在成员变量中（因为它们是类的对象）。

这里有一个简单的函子：

```C++
#include <iostream>

class Accumulator
{
private:
    int m_counter{ 0 };

public:
    int operator() (int i) { return (m_counter += i); }

    void reset() { m_counter = 0; } 
};

int main()
{
    Accumulator acc{};
    std::cout << acc(1) << '\n'; // 打印 1
    std::cout << acc(3) << '\n'; // 打印 4

    Accumulator acc2{};
    std::cout << acc2(10) << '\n'; // 打印 10
    std::cout << acc2(20) << '\n'; // 打印 30
    
    return 0;
}
```

请注意，使用Accumulator看起来就像进行普通函数调用，但acc对象存储的是累积的值。

关于函子的好处是，可以根据需要实例化任意多个单独的函子对象，并同时使用它们。函子也可以有其他成员函数（例如， reset（） ）来执行方便的操作。

***
## 结论

「operator()」有时会重载两个参数来索引多维数组。但其它任何需求，都可以更好的实现为使用可读的有函数名的成员函数。

「operator()」也经常重载以创建函子。尽管简单的函子（如上面的示例）相当容易理解，但函子通常用于更高级的编程主题，有需要再学习即可。

***
