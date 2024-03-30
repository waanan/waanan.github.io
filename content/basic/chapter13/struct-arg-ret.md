---
title: "结构体作为函数的输入与输出"
date: 2024-03-08T13:20:57+08:00
---

考虑由3个松散变量表示的员工：

```C++
int main()
{
    int id { 1 };
    int age { 24 };
    double wage { 52400.0 };

    return 0;
}
```

如果要将此员工传递给函数，必须传递三个变量：

```C++
#include <iostream>

void printEmployee(int id, int age, double wage)
{
    std::cout << "ID:   " << id << '\n';
    std::cout << "Age:  " << age << '\n';
    std::cout << "Wage: " << wage << '\n';
}

int main()
{
    int id { 1 };
    int age { 24 };
    double wage { 52400.0 };

    printEmployee(id, age, wage);

    return 0;
}
```

虽然传递3个单独的员工变量并不是那么糟糕，但考虑需要传递多个员工变量的函数。独立传递每个变量将非常容易出错。此外，如果向员工添加新属性（例如名称），现在必须修改所有函数声明、定义和函数调用，以接受新的参数！

***
## 传递结构（通过引用）

与单个变量相比，使用结构的一大优势是，我们可以将整个结构传递给需要与成员一起工作的函数。结构通常通过引用传递（通常通过常量引用），以避免进行复制。

```C++
#include <iostream>

struct Employee
{
    int id {};
    int age {};
    double wage {};
};

void printEmployee(const Employee& employee) // note pass by reference here
{
    std::cout << "ID:   " << employee.id << '\n';
    std::cout << "Age:  " << employee.age << '\n';
    std::cout << "Wage: " << employee.wage << '\n';
}

int main()
{
    Employee joe { 14, 32, 24.15 };
    Employee frank { 15, 28, 18.27 };

    // Print Joe's information
    printEmployee(joe);

    std::cout << '\n';

    // Print Frank's information
    printEmployee(frank);

    return 0;
}
```

在上面的示例中，我们将整个Employee传递给printEmployere（）（两次，一次用于joe，一次为frank）。

上述程序输出：

因为我们传递的是整个结构对象（而不是单个成员），所以无论结构对象有多少个成员，我们都只需要一个参数。而且，在将来，如果我们决定向Employee结构中添加新成员，则不必更改函数声明或函数调用！新成员将自动包含在内。

{{< alert success >}}
**相关内容**

在第12.6课中，我们讨论了何时按值传递结构与按引用传递结构——按常量左值传递引用。

{{< /alert >}}

***
## 正在返回结构

考虑这样的情况，我们有一个函数需要返回三维笛卡尔空间中的一个点。这样的点有3个属性：x坐标、y坐标和z坐标。但函数只能返回一个值。那么我们如何将所有3个坐标返回给用户呢？

一种常见的方法是返回结构：

```C++
#include <iostream>

struct Point3d
{
    double x { 0.0 };
    double y { 0.0 };
    double z { 0.0 };
};

Point3d getZeroPoint()
{
    // We can create a variable and return the variable (we'll improve this below)
    Point3d temp { 0.0, 0.0, 0.0 };
    return temp;
}

int main()
{
    Point3d zero{ getZeroPoint() };

    if (zero.x == 0.0 && zero.y == 0.0 && zero.z == 0.0)
        std::cout << "The point is zero\n";
    else
        std::cout << "The point is not zero\n";

    return 0;
}
```

这将打印：

结构通常按值返回，以便不返回悬空引用。

在上面的getZeroPoint（）函数中，我们创建了一个新的命名对象（temp），以便可以返回它：

```C++
Point3d getZeroPoint()
{
    // We can create a variable and return the variable (we'll improve this below)
    Point3d temp { 0.0, 0.0, 0.0 };
    return temp;
}
```

对象（temp）的名称在这里并不真正提供任何文档值。

我们可以通过返回临时（未命名/匿名）对象来稍微改进函数：

```C++
Point3d getZeroPoint()
{
    return Point3d { 0.0, 0.0, 0.0 }; // return an unnamed Point3d
}
```

在这种情况下，将构造临时Point3d，将其复制回调用方，然后在表达式末尾销毁。请注意，这是多么干净（一行对两行，并且不需要了解temp是否被多次使用）。

{{< alert success >}}
**相关内容**

我们在第14.13课——临时类对象中更详细地讨论了匿名对象。

{{< /alert >}}

***
## 推导返回类型

在函数具有显式返回类型（例如Point3d）的情况下，我们甚至可以在return语句中省略该类型：

```C++
Point3d getZeroPoint()
{
    // We already specified the type at the function declaration
    // so we don't need to do so here again
    return { 0.0, 0.0, 0.0 }; // return an unnamed Point3d
}
```

还要注意，由于在这种情况下，我们返回所有零值，因此可以使用空大括号来返回初始化的值Point3d：

```C++
Point3d getZeroPoint()
{
    // We can use empty curly braces to value-initialize all members
    return {};
}
```

***
## 结构是一个重要的构建块

虽然结构本身很有用，但类（是C++和面向对象编程的核心）直接构建在我们在这里介绍的概念之上。很好地理解结构（特别是数据成员、成员选择和默认成员初始化）将使您更容易过渡到类。

***
## 测验时间

问题#1

您正在运行一个网站，并且您正在尝试计算您的广告收入。编写一个程序，允许您输入3个数据：

1. 观看了多少广告。
2. 用户点击广告的百分比。
3. 每次点击广告的平均收入。


将这3个值存储在结构中。将该结构传递给另一个打印每个值的函数。print函数还应打印当天的收入（将3个字段相乘）。

显示提示

显示解决方案

问题#2

创建一个结构来保存分数。结构应该具有整数分子和整数分母成员。

编写一个函数从用户处读入分数，并使用它读入两个分数对象。编写另一个函数将两个分数相乘，并将结果返回为分数（不需要减少分数）。编写另一个函数来打印分数。

程序的输出应与以下内容匹配：

将两个分数相乘时，所得分子是两个分子的乘积，所得分母是两个分母的乘积。

显示解决方案

问题#3

在上一个测验问题的解决方案中，为什么getFraction（）按值而不是按引用返回？

显示解决方案

