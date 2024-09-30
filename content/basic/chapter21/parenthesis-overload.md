---
title: "重载括号运算符"
date: 2024-08-20T12:01:51+08:00
---

到目前为止，您看到的所有重载操作符都允许您定义操作符参数的类型，但不能定义参数的数量（根据操作符的类型固定）。例如，operator==总是采用两个参数，而operator！总是要一个。括号操作符（operator（））是一个特别有趣的操作符，它允许您改变它所采用的参数的类型和数量。

有两件事需要记住：首先，括号操作符必须实现为成员函数。其次，在非面向对象C++中，（）操作符用于调用函数。在类的情况下，operator（）只是一个普通的操作符，它像任何其他重载操作符一样调用函数（命名为operator（））。

***
## 一个例子

让我们看一个有助于重载此运算符的示例：

```C++
class Matrix
{
private:
    double data[4][4]{};
};
```

矩阵是线性代数的一个关键组件，通常用于进行几何建模和3D计算机图形工作。在这种情况下，您需要认识的只是Matrix类是一个4×4的二维双精度数组。

在关于重载下标运算符的课程中，您学习了我们可以重载运算符[]以提供对专用一维数组的直接访问。然而，在这种情况下，我们希望访问私有二维数组。由于运算符[]仅限于单个参数，因此仅让我们索引二维数组是不够的。

然而，由于（）操作符可以接受任意多的参数，因此我们可以声明一个接受两个整数索引参数的operator（）版本，并使用它访问二维数组。下面是一个例子：

```C++
#include <cassert> // for assert()

class Matrix
{
private:
    double m_data[4][4]{};

public:
    double& operator()(int row, int col);
    double operator()(int row, int col) const; // for const objects
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

现在，让我们再次重载（）运算符，这一次是以一种完全不需要参数的方式：

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
    // reset all elements of the matrix to 0.0
    for (int row{ 0 }; row < 4; ++row)
    {
        for (int col{ 0 }; col < 4; ++col)
        {
            m_data[row][col] = 0.0;
        }
    }
}
```

下面是我们的新示例：

```C++
#include <iostream>

int main()
{
    Matrix matrix{};
    matrix(1, 2) = 4.5;
    matrix(); // erase matrix
    std::cout << matrix(1, 2) << '\n';

    return 0;
}
```

产生结果：

由于（）操作符非常灵活，因此很容易将其用于许多不同的目的。然而，强烈建议这样做，因为（）符号并不能真正指示操作符正在做什么。在上面的示例中，最好将擦除功能编写为一个名为clear（）或erase（）的函数，因为matrix.erase（.）比matrix（.）更容易理解（它可以做任何事情！）。

***
## 玩函子的乐趣

Operator（）通常也被重载以实现functor（或函数对象），这是像函数一样操作的类。函子比普通函数的优点是函子可以将数据存储在成员变量中（因为它们是类）。

这里有一个简单的函子：

```C++
#include <iostream>

class Accumulator
{
private:
    int m_counter{ 0 };

public:
    int operator() (int i) { return (m_counter += i); }

    void reset() { m_counter = 0; } // optional 
};

int main()
{
    Accumulator acc{};
    std::cout << acc(1) << '\n'; // prints 1
    std::cout << acc(3) << '\n'; // prints 4

    Accumulator acc2{};
    std::cout << acc2(10) << '\n'; // prints 10
    std::cout << acc2(20) << '\n'; // prints 30
    
    return 0;
}
```

请注意，使用Accumulator看起来就像进行普通函数调用，但Accumulatorobject存储的是累积值。

关于函子的好处是，我们可以根据需要实例化任意多个单独的函子对象，并同时使用它们。函数也可以有其他成员函数（例如，reset（））来执行方便的操作。

***
## 结论

Operator（）有时会重载两个参数来索引多维数组，或检索一维数组的子集（使用两个参数定义要返回的子集）。其他任何东西都可能更好地编写为具有更具描述性的名称的成员函数。

Operator（）也经常重载以创建函子。尽管简单的函子（如上面的示例）相当容易理解，但函子通常用于更高级的编程主题，值得自己学习。

***
## 测验时间

问题#1

编写一个名为MyString的类，该类保存std:：string.Overload operator<<以输出字符串.Overload operator（）以返回从第一个参数的索引开始的子字符串（作为MyString）。子字符串的长度应由第二个参数定义。

应运行以下代码：

```C++
int main()
{
    MyString s { "Hello, world!" };
    std::cout << s(7, 5) << '\n'; // start at index 7 and return 5 characters

    return 0;
}
```

这应该打印出来

提示：您可以使用std:：string:：substr来获取std:：string的子字符串。

显示解决方案

问题#2

这个测验问题是额外的学分。

>步骤#1

如果我们不需要修改返回的子串，为什么上面的方法效率低下？

显示解决方案

>步骤#2

我们可以做些什么呢？

显示解决方案

>步骤#3

从上一个测验解决方案更新operator（），以将子字符串作为std:：string_view返回。

提示：std:：string:：substr（）返回标准：：string.std:：string_view:：subs（）返回一个标准：：string_view。请非常小心，不要返回悬空的std:：string_view！。

显示提示

显示提示

显示解决方案

