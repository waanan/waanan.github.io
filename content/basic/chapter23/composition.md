---
title: "对象组合"
date: 2024-10-08T17:40:35+08:00
---

## 对象组合

在现实生活中，复杂对象通常由更小、更简单的对象构建。例如，汽车是使用金属框架、发动机、一些轮胎、变速器、方向盘和大量其他零件制造的。计算机是由CPU、主板、一些内存等构建的……人是由较小的部分构建的：有一个头部、一个身体、腿、手臂等等。从较简单的对象构建复杂对象的过程称为对象组合。

广义地说，对象组合建模了两个对象之间的 “有一个” 关系。汽车”有一个“变速器。您的计算机“有一个”CPU。你”有一颗“心。复杂对象有时称为整体或父对象。较简单的对象通常称为零件、子对象或组件。

在C++中，结构体和类可以具有各种类型的数据成员（例如基本类型或其他类）。当我们用数据成员构建类时，本质上是在用简单的部分构造复杂的对象，这就是对象组合。由于这个原因，结构体和类被称为复合类型。

对象组合在C++中非常有用，因为它允许我们通过组合更简单、更容易管理的部分来创建复杂的类。这降低了复杂性，允许我们更快地编写代码，也错误更少，因为可以重用已经编写、测试和验证有效的代码。

***
## 对象组合的类型

对象组合有两个基本的子类型：组合和聚合。我们将在本课中研究组合，在下一节课中研究聚合。

术语注释：术语“组合”通常用于指组合和聚合，而不仅仅指组合类型。在本教程中，当同时指代这两者时，我们将使用术语“对象组合”，当我们专门指代合成子类型时，我们使用术语“组合”。

***
## 组合

要符合组合条件，对象和零件必须具有以下关系：

1. 部件（成员）是对象（类）的一部分
2. 部件（成员）一次只能属于一个对象（类）
3. 部件（成员）的存在由对象（类）管理
4. 部件（成员）不知道对象（类）的存在

一个很好的现实例子是一个人的身体和心脏之间的关系。让我们更详细地研究一下。

组合关系是部分-整体关系，其中部分必须构成整个对象的一部分。例如，心脏是一个人身体的一部分。组合中的部分一次只能是一个对象的一部分。心脏是一个人身体的一部分，不能同时成为其他人身体的一部份。

在组合关系中，对象负责部件的存在。通常，这意味着零件是在创建对象时创建的，而零件是在销毁对象时销毁的。但更广泛地说，它意味着对象以这样一种方式管理部件的寿命，使用对象的用户不需要参与。例如，创建身体时，也会创建心脏。当一个人的身体被摧毁时，他的心脏也被摧毁。正因为如此，组合有时被称为“死亡关系”。

最后，部分不知道整体的存在。你的心在幸福地运转，却不知道它是更大结构的一部分。我们称之为单向关系，因为身体知道心脏，而心脏不知道身体。

请注意，组合并不限制部件的转移。心脏可以从一个身体移植到另一个身体。然而，即使在移植后，它仍然满足组合物的要求（心脏现在由接收者拥有，并且只能是接收者对象的一部分，除非再次转移）。

无处不在的Fraction示例类是一个很好的组合示例：

```C++
class Fraction
{
private:
	int m_numerator;
	int m_denominator;
 
public:
	Fraction(int numerator=0, int denominator=1)
		: m_numerator{ numerator }, m_denominator{ denominator }
	{
	}
};
```

这个类有两个数据成员：分子和分母。分子和分母是分数的一部分（包含在其中）。它们一次不能属于多个分数。分子和分母不知道它们是分数的一部分，它们只保存整数。创建分数实例时，将创建分子和分母。当分数实例被破坏时，分子和分母也被破坏。

虽然对象组合模型是 ”有一个“ 关系（身体有心脏，分数有分母），但可以更准确地说，组合模型是 “一部分” 关系（心脏是身体的一部分，分子是分数的一部分）。组合通常用于建模物理关系，其中一个对象在物理上包含在另一个对象中。

对象组合的部分可以是单数或复数的——例如，心脏是身体里单数的，但身体包含10个手指（可以建模为数组）。

***
## 实现组合

组合是在C++中最容易实现的关系类型之一。它们通常创建为具有普通数据成员的结构体或类。因为这些数据成员直接作为结构体/类的一部分存在，所以它们的生命周期绑定到类实例本身的生命周期。

需要进行动态分配或释放的组合可以使用指针数据成员来实现。在这种情况下，组合类应该负责自己进行所有必要的内存管理（而不是类的用户）。

一般来说，如果可以使用组合来设计类，则应该优先使用组合设计类。使用组合设计的类是简单、灵活和健壮的（因为它们很好地进行自我清理）。

***
## 更多示例

许多游戏和模拟都有在棋盘、地图或屏幕上移动的生物或对象。所有这些生物/物体的一个共同点是它们都有一个位置。在本例中，我们将创建一个生物类，该生物类使用Point2D类来保存生物的位置。

首先，让我们设计Point2D类。我们的生物将生活在2d世界中，因此Point2D类将有2个维度，X和Y。我们将假设世界由离散的方形组成，因此这些维度将始终是整数。

Point2D.h：

```C++
#ifndef POINT2D_H
#define POINT2D_H

#include <iostream>

class Point2D
{
private:
    int m_x;
    int m_y;

public:
    // 默认构造函数
    Point2D()
        : m_x{ 0 }, m_y{ 0 }
    {
    }

    // 特化的构造函数
    Point2D(int x, int y)
        : m_x{ x }, m_y{ y }
    {
    }

    // 重载输出函数
    friend std::ostream& operator<<(std::ostream& out, const Point2D& point)
    {
        out << '(' << point.m_x << ", " << point.m_y << ')';
        return out;
    }

    // 访问函数
    void setPoint(int x, int y)
    {
        m_x = x;
        m_y = y;
    }

};

#endif
```

注意，因为我们已经在头文件中实现了所有函数（为了保持示例的简洁），所以没有Point2D.cpp。

Point2d类有自己的内部成员：位置值x和y是Point2d的一部分，它们的寿命与给定Point2d实例的寿命相关联。

现在让我们来设计生物。Creature将具有几个属性：名称（将是字符串）和位置（将是Point2D类）。

Creature.h：

```C++
#ifndef CREATURE_H
#define CREATURE_H

#include <iostream>
#include <string>
#include <string_view>
#include "Point2D.h"

class Creature
{
private:
    std::string m_name;
    Point2D m_location;

public:
    Creature(std::string_view name, const Point2D& location)
        : m_name{ name }, m_location{ location }
    {
    }

    friend std::ostream& operator<<(std::ostream& out, const Creature& creature)
    {
        out << creature.m_name << " is at " << creature.m_location;
        return out;
    }

    void moveTo(int x, int y)
    {
        m_location.setPoint(x, y);
    }
};
#endif
```

Creature也有自己内部的成员。名称和位置是它的一部分，也与它们所属生物的生命周期息息相关。

最后，main.cpp：

```C++
#include <string>
#include <iostream>
#include "Creature.h"
#include "Point2D.h"

int main()
{
    std::cout << "Enter a name for your creature: ";
    std::string name;
    std::cin >> name;
    Creature creature{ name, { 4, 7 } };
	
    while (true)
    {
        // 打印生物的名称和位置
        std::cout << creature << '\n';

        std::cout << "Enter new X location for creature (-1 to quit): ";
        int x{ 0 };
        std::cin >> x;
        if (x == -1)
            break;

        std::cout << "Enter new Y location for creature (-1 to quit): ";
        int y{ 0 };
        std::cin >> y;
        if (y == -1)
            break;
		
        creature.moveTo(x, y);
    }

    return 0;
}
```

运行结果：

```C++
Enter a name for your creature: Marvin
Marvin is at (4, 7)
Enter new X location for creature (-1 to quit): 6
Enter new Y location for creature (-1 to quit): 12
Marvin is at (6, 12)
Enter new X location for creature (-1 to quit): 3
Enter new Y location for creature (-1 to quit): 2
Marvin is at (3, 2)
Enter new X location for creature (-1 to quit): -1
```

***
## 组合的变体

尽管大多数组合在创建时直接创建其部分，在销毁时直接销毁其部分，但一些变体稍微改变了这些规则。

例如：

1. 组合可能会将某些部分的创建推迟到需要它们时。例如，在用户为字符串分配一些要保存的数据之前，字符串类可能不会创建动态字符数组。
2. 组合可以选择直接使用输入的部分，而不是自己创建该部分。
3. 组合可以将其部分的销毁委托给其他对象（例如，委托给垃圾收集的例程）。

这里的关键点是，组合来管理其部分，使用组合的用户不需要管理任何东西。

***
## 组合和类成员

当谈到对象组合时，新程序员经常问的一个问题是，“我应该在什么时候使用类成员，而不是直接实现功能？”。例如，与其使用Point2D类来实现Creature的位置，不如将2个整数添加到Creature类中，并在Creature类别中编写代码来处理定位。然而，使Point2D成为单独的类（也是Creature的成员）有许多好处：

1. 每个单独的类都相对简单和直接，只做一件任务。这使得每个类都容易编写和理解，因为它们更聚焦自己的任务。例如Point2D只用关心位置相关的事情。
2. 每个类都有完整的功能，使得它们可以重用。例如，可以在不同的应用中复用Point2D类。或者creature对象可能需要多个位置（例如它想到达的位置），这时简单的增加另外一个Point2D成员就行。
3. 父类用来做最复杂的工作，关注于协调所有成员间的数据流动。这有助于减少外部父类的复杂度，因为它可以把任务分配给它的成员，成员知道如何做具体的细节事项。例如，当移动Creature时，实际工作分派给Point类。Point类知道如何去设置位置，而Creature类无需知道具体的细节如何实现。

在我们的示例中，Creature不必担心位置点是如何实现的，或者名称是如何存储的，这是有意义的。Creature的工作不是去了解那些细节。Creature的工作是设计如何协调数据流，并确保每个类成员都知道它应该做什么。由各个类来担心他们自己如何做对应的细节。

{{< alert success >}}
**提示**

一个好的经验法则是，应该构建单独的类来完成单个任务。该任务应该是存储和操作某种类型的数据（例如，Point2D，std::string），或者是协调其成员（例如，Creature）。理想情况下不能两者兼而有之。

{{< /alert >}}

***

{{< prevnext prev="/basic/chapter23/object-relation/" next="/basic/chapter23/aggregation/" >}}
23.0 对象关系
<--->
23.2 聚合
{{< /prevnext >}}
