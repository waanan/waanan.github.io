---
title: "重载I/O运算符"
date: 2024-08-20T12:01:51+08:00
---

对于具有多个成员变量的类，在屏幕上打印每个单独的变量可能会很快变得令人厌烦。例如，考虑以下类：

```C++
class Point
{
private:
    double m_x{};
    double m_y{};
    double m_z{};

public:
    Point(double x=0.0, double y=0.0, double z=0.0)
      : m_x{x}, m_y{y}, m_z{z}
    {
    }

    double getX() const { return m_x; }
    double getY() const { return m_y; }
    double getZ() const { return m_z; }
};
```

如果要将此类的实例打印到屏幕上，则必须执行以下操作：

```C++
Point point { 5.0, 6.0, 7.0 };

std::cout << "Point(" << point.getX() << ", " <<
    point.getY() << ", " <<
    point.getZ() << ')';
```

当然，实现一个可重用的函数来做这件事更有意义。下面我们创建了print()函数，其工作方式如下：

```C++
class Point
{
private:
    double m_x{};
    double m_y{};
    double m_z{};

public:
    Point(double x=0.0, double y=0.0, double z=0.0)
      : m_x{x}, m_y{y}, m_z{z}
    {
    }

    double getX() const { return m_x; }
    double getY() const { return m_y; }
    double getZ() const { return m_z; }

    void print() const
    {
        std::cout << "Point(" << m_x << ", " << m_y << ", " << m_z << ')';
    }
};
```

虽然这要好得多，但它仍然有一些缺点。因为print()返回void，所以不能在输出语句的中间调用它。相反，您必须这样做：

```C++
int main()
{
    const Point point { 5.0, 6.0, 7.0 };

    std::cout << "My point is: ";
    point.print();
    std::cout << " in Cartesian space.\n";
}
```

如果可以简单地键入：

```C++
Point point{5.0, 6.0, 7.0};
cout << "My point is: " << point << " in Cartesian space.\n";
```

并得到相同的结果。将不会在多个语句之间分解输出，也不必记住您命名的print函数。

幸运的是，通过重载<<运算符，可以实现该功能！


***
## 重载operator<<

重载运算符<<类似于重载运算符+（它们都是二元运算符），只是参数类型不同。

考虑表达式"std::cout << point"。运算符<<，操作数是什么？左操作数是std::cout对象，右操作数是Point类对象。std::cout实际上是一个类型为std::ostream的对象。因此，我们的重载函数将如下所示：

```C++
// std::ostream 是 std::cout 对象的类型
friend std::ostream& operator<< (std::ostream& out, const Point& point);
```

Point类的运算符<<的实现相当简单——因为C++已经知道如何使用运算符<<输出double，并且我们的成员都是double，所以我们可以简单地使用运算符<<来输出Point的成员变量。下面是上面的Point类，新增重载运算符<<。

```C++
#include <iostream>

class Point
{
private:
    double m_x{};
    double m_y{};
    double m_z{};

public:
    Point(double x=0.0, double y=0.0, double z=0.0)
      : m_x{x}, m_y{y}, m_z{z}
    {
    }

    friend std::ostream& operator<< (std::ostream& out, const Point& point);
};

std::ostream& operator<< (std::ostream& out, const Point& point)
{
    // 因为 operator<< 是 Point 类的友元, 所以可以直接访问私有成员变量
    out << "Point(" << point.m_x << ", " << point.m_y << ", " << point.m_z << ')'; // 这里做实际输出

    return out; // 返回 std::ostream 以便可以链式调用 operator<<
}

int main()
{
    const Point point1 { 2.0, 3.0, 4.0 };

    std::cout << point1 << '\n';

    return 0;
}
```

这非常简单——请注意，我们的输出行与前面编写的print()函数中的行非常相似。最显著的区别是，std::cout已成为参数out（当调用函数时，它将是对std::cout的引用）。

这里最棘手的部分是返回类型。使用算术运算符，我们通过值计算并返回单个结果。然而，如果您试图通过值返回std::ostream，则会得到一个编译器错误。发生这种情况是因为std::ostream明确禁止复制。

在这种情况下，我们返回左边参数作为引用。这不仅防止生成std::ostream的副本，还允许我们将输出命令“链接”在一起，例如"std::cout<< point << std::endl；"。

考虑如果运算符<< 返回void，会发生什么情况。当编译器计算"std::cout << point << '\n'; "时，由于优先级/关联性规则，它将该表达式计算为"（std::cout << point）<< '\n'；"。"std::cout << point"将调用我们的返回void重载操作符<< 函数，该函数返回void。然后部分计算的表达式变为：" void << '\n'；"，这毫无意义！

相反，通过返回out参数作为返回类型，（std::cout << point）返回std::cout。然后，剩余部分计算的表达式变为：" std::cout << '\n'；"！

每当我们希望重载的二元运算符以这种方式可链接时，应该（通过引用）返回左操作数。在这种情况下，通过引用返回左边参数是可以的——因为左边参数是由调用函数传入的，所以当被调用函数返回时，它必须仍然存在。因此，不必担心返回一个悬空引用。

为了证明它是有效的，请考虑下面的示例，该示例将Point类与 重载运算符<< 一起使用：

```C++
#include <iostream>

class Point
{
private:
    double m_x{};
    double m_y{};
    double m_z{};

public:
    Point(double x=0.0, double y=0.0, double z=0.0)
      : m_x{x}, m_y{y}, m_z{z}
    {
    }

    friend std::ostream& operator<< (std::ostream& out, const Point& point);
};

std::ostream& operator<< (std::ostream& out, const Point& point)
{
    //  因为 operator<< 是 Point 类的友元, 所以可以直接访问私有成员变量
    out << "Point(" << point.m_x << ", " << point.m_y << ", " << point.m_z << ')';

    return out;
}

int main()
{
    Point point1 { 2.0, 3.5, 4.0 };
    Point point2 { 6.0, 7.5, 8.0 };

    std::cout << point1 << ' ' << point2 << '\n';

    return 0;
}
```

这将产生以下结果：

```C++
Point(2, 3.5, 4) Point(6, 7.5, 8)
```

在上面的示例中，操作符<< 是友元函数，因为它需要直接访问Point的私有成员。然而，如果可以通过getter访问成员，那么操作符<< 可以实现为非友元函数。

***
## 重载operator>>

也可以重载输入运算符。这是以类似于重载输出运算符的方式完成的。您需要知道的关键一点是，std::cin是一个类型为std::istream的对象。下面是添加了重载运算符>>的Point类：

```C++
#include <iostream>

class Point
{
private:
    double m_x{};
    double m_y{};
    double m_z{};

public:
    Point(double x=0.0, double y=0.0, double z=0.0)
      : m_x{x}, m_y{y}, m_z{z}
    {
    }

    friend std::ostream& operator<< (std::ostream& out, const Point& point);
};

std::ostream& operator<< (std::ostream& out, const Point& point)
{
    //  因为 operator<< 是 Point 类的友元, 所以可以直接访问私有成员变量
    out << "Point(" << point.m_x << ", " << point.m_y << ", " << point.m_z << ')';

    return out;
}

// 注意 point 参数是非 const，因为我们需要修改它
// 注 这里实现为非友元函数
std::istream& operator>> (std::istream& in, Point& point)
{
    double x{};
    double y{};
    double z{};
    
    in >> x >> y >> z;

    if (in)                     // 如果所有的输入都ok
        point = Point{x, y, z}; // 覆盖现有的point对象
        
    return in;
}

int main()
{
    std::cout << "Enter a point: ";

    Point point{};
    std::cin >> point;

    std::cout << "You entered: " << point << '\n';

    return 0;
}
```

假设用户输入3.0 4.5 7.26作为输入，程序将产生以下结果：

```C++
You entered: Point(3, 4.5, 7.26)
```

在这个实现中，我们使用操作符=来覆盖point中的值。因为operator=是public可用的，这意味着不需要operator>>成为友元函数。

***
## 防止部分提取

您可能期望看到Point的重载操作符>>实现得更像这样：

```C++
// 假设这个操作符，是Point的友元函数，可以直接修改私有成员
std::istream& operator>> (std::istream& in, Point& point)
{
    // 这版本的代码可能有部分提取的问题
    in >> point.m_x >> point.m_y >> point.m_z;
    
    return in;
}
```

然而，这种实现可能导致部分提取。考虑一下如果用户输入“3.0 a b”作为输入会发生什么。3.0将被提取为m_x。对m_y和m_z的提取都将失败，这意味着m_y与m_z将被设置为0.0。我们的point将部分被输入覆盖，部分被零覆盖。

对于Point对象，这可能是一个可接受的结果。但假设我们输入的是分数。提取分母失败会将分母设置为0.0，这可能会在以后导致除以零错误。

由于这个原因，最好存储所有输入，直到我们可以验证所有输入是否成功，然后才覆盖对象。

***
## 结论

重载 operator<< 和 operator>> 使将类输出到屏幕和接受来自控制台的用户输入变得非常容易。

***

