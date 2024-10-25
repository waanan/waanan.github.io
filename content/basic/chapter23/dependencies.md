---
title: "依赖关系"
date: 2024-10-08T17:40:35+08:00
---

到目前为止，我们已经探索了3种类型的关系：组合、聚合和关联。现在来看最简单的一个：依赖关系。

非正式来讲，我们使用术语依赖性来表示一个对象对于给定的任务依赖于另一个对象。例如，如果摔断了脚，就得依赖拐杖才能走动。花依靠蜜蜂授粉，以生长果实或繁殖。

当一个对象调用另一个对象的功能以完成某些特定任务时，就会发生依赖关系。这是一种比关联弱的关系。对所依赖的对象的任何更改都可能会破坏调用者的正常执行。依赖关系始终是单向关系。

您已经见过多次的依赖关系的一个很好的例子是std::ostream。我们使用std::ostream类将内容打印到控制台。

例如：

```C++
#include <iostream>
 
class Point
{
private:
    double m_x{};
    double m_y{};
    double m_z{};
 
public:
    Point(double x=0.0, double y=0.0, double z=0.0): m_x{x}, m_y{y}, m_z{z}
    {
    }
 
    friend std::ostream& operator<< (std::ostream& out, const Point& point); // Point 依赖了 std::ostream
};
 
std::ostream& operator<< (std::ostream& out, const Point& point)
{
    // 因为 operator<< 是 Point 的友元函数, 可以直接访问 Point 的成员变量
    out << "Point(" << point.m_x << ", " << point.m_y << ", " << point.m_z << ')';
 
    return out;
}
 
int main()
{
    Point point1 { 2.0, 3.0, 4.0 };
 
    std::cout << point1; // 程序这里依赖了 std::cout
 
    return 0;
}
```

在上面的代码中，Point与std::ostream没有直接关系，但它依赖于std:∶ostream，因为 operator<<  使用std::ostream将Point打印到控制台。

***
## 依赖与关联

关于依赖关系与关联的区别，通常存在一些困惑。

在C++中，关联是一种关系，其中一个类作为成员与相关联的类保持直接或间接的“链接”。例如，Doctor类具有指向其Patient的指针数组作为成员。你可以随时问医生谁是病人。Driver类将拥有的Car的id保存为整数成员。驾驶员总是知道与它相关的汽车。

依赖项通常不是成员。相反，所依赖的对象通常根据需要实例化（如打开要向其写入数据的文件），或作为参数传递到函数中（如上面重载 operator<< 中的std::ostream）。

***

{{< prevnext prev="/basic/chapter23/association/" next="/basic/chapter23/container-class/" >}}
23.3 关联
<--->
23.5 容器类
{{< /prevnext >}}
