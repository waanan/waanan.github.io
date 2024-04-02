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
## 通过引用传递结构体

与单个变量相比，使用结构体的一大优势是，可以将整个结构体传递给函数。结构体通常通过引用传递（通常是常量引用），以避免进行复制。

```C++
#include <iostream>

struct Employee
{
    int id {};
    int age {};
    double wage {};
};

void printEmployee(const Employee& employee) // 注： 通过引用传递
{
    std::cout << "ID:   " << employee.id << '\n';
    std::cout << "Age:  " << employee.age << '\n';
    std::cout << "Wage: " << employee.wage << '\n';
}

int main()
{
    Employee joe { 14, 32, 24.15 };
    Employee frank { 15, 28, 18.27 };

    // 打印 Joe 的信息
    printEmployee(joe);

    std::cout << '\n';

    // 打印 Frank 的信息
    printEmployee(frank);

    return 0;
}
```

在上面的示例中，将整个Employee传递给printEmployere()（一次用于joe，一次为frank）。

上述程序输出：

```C++
ID:   14
Age:  32
Wage: 24.15

ID:   15
Age:  28
Wage: 18.27
```

因为传递的是整个结构体对象（而不是单个成员变量），所以无论有多少个成员变量，都只需要一个参数。而且，如果决定向Employee结构体中添加新成员变量，则不必更改函数声明或函数调用！新成员变量将自动包含在内。

***
## 结构体作为返回值

考虑这样的情况，有一个函数需要返回三维空间中的一个点。这样的点有3个属性：x坐标、y坐标和z坐标。但函数只能返回一个值。那么如何将所有3个坐标返回给用户呢？

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
    // 创建一个临时变量并返回
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

```C++
The point is zero
```

结构体通常按值返回，避免返回悬空引用。

在上面的getZeroPoint() 函数中，创建了一个新的命名对象（temp），以便可以返回它：

```C++
Point3d getZeroPoint()
{
    // 创建一个临时变量并返回
    Point3d temp { 0.0, 0.0, 0.0 };
    return temp;
}
```

对象（temp）的名称在这里没有任何说明文档的能力。

因此可以通过返回临时（未命名/匿名）对象来稍微改进函数：

```C++
Point3d getZeroPoint()
{
    return Point3d { 0.0, 0.0, 0.0 }; // 返回一个未命名的 Point3d
}
```

在这种情况下，将构造临时Point3d，将其复制回调用方，然后在表达式末尾销毁。这里比上面更加简洁（一行对两行，并且不需要了解temp是否被多次使用）。

***
## 返回类型推导

在函数具有显式返回类型（例如Point3d）的情况下，甚至可以在return语句中省略该类型：

```C++
Point3d getZeroPoint()
{
    // 因为函数声明中已经指定返回类型
    // 因此这里无需再指定
    return { 0.0, 0.0, 0.0 }; // 返回一个未命名的 Point3d
}
```

还要注意，由于在这种情况下，如果想要返回一个为零的结构体，可以使用空大括号来返回Point3d：

```C++
Point3d getZeroPoint()
{
    // 空大括号，来进行值初始化
    return {};
}
```

***
## 结构体是一个很重要的代码组件

结构体很有用，类（是C++和面向对象编程的核心）直接构建在这里介绍的概念之上。很好地理解结构体（特别是数据成员、成员选择和默认成员初始化）将使您更容易过渡到类。

***

{{< prevnext prev="/basic/chapter13/struct-member-default-init/" next="/basic/chapter13/struct-other/" >}}
13.6 成员变量的默认初始化
<--->
13.8 结构体杂项
{{< /prevnext >}}
