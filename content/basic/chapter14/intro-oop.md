---
title: "面向对象编程简介"
date: 2024-04-09T13:02:20+08:00
---

***
## 面向过程编程

在前面，我们在C++中将对象定义为“一块可用于存储值的内存”。具有名称的对象称为变量。C++程序由发送到计算机的指令的顺序列表组成，这些指令定义数据（通过对象）和对该数据执行的操作（通过语句和表达式组成的函数）。

到目前为止，我们一直在做一种称为面向过程编程的行为。在其中，重点是创建实现程序逻辑的“过程”（在C++中称为函数）。将数据对象传递给这些函数，这些函数对数据执行操作，然后可能返回一个结果供调用方使用。

在过程编程中，函数和这些函数操作的数据是单独的实体。程序员负责将函数和数据组合在一起，以产生所需的结果。这导致代码如下所示：

```C++
eat(you, apple);
```

现在，看看你周围的一切——你看到的每一个地方都是物体：书籍、建筑物、食物，甚至你。这类对象有两个主要组成部分：1）一些相关的属性（例如重量、颜色、大小、坚固性、形状等），以及2）它们可以表现的一些行为（例如打开、使其他东西变热等）。这些属性和行为是不可分割的。

在编程中，属性由对象表示，行为由函数表示。因此，过程编程比较糟糕地描述了现实，因为它分离了属性（对象）和行为（函数）。

***
## 什么是面向对象编程？

在面向对象编程（object-oriented programming，通常缩写为OOP）中，重点是创建合适的数据类型，里面包含对应的属性以及一组良好的行为函数。OOP中的术语“对象”是指可以从此类型中实例化的对象。

这导致代码看起来更像：

```C++
you.eat(apple);
```

这使得行为主体（you）、正在调用什么行为（eat）以及哪些对象是该行为的附件（apple）变得更清楚。

因为属性和行为不再是分开的，所以对象更容易模块化，这使得程序更容易编写和理解，并且还提供了更高程度的代码重用性。通过定义对象之间如何互相交互，这提供了一种更直观的处理数据的方法。

在下一课中，将讨论如何创建此类对象。

***
## 面向过程与面向对象程序示例

下面是一个面向过程风格的程序，打印动物的名称和腿的数量：

```C++
#include <iostream>
#include <string_view>

enum AnimalType
{
    cat,
    dog,
    chicken,
};

constexpr std::string_view animalName(AnimalType type)
{
    switch (type)
    {
    case cat: return "cat";
    case dog: return "dog";
    case chicken: return "chicken";
    default:  return "";
    }
}

constexpr int numLegs(AnimalType type)
{
    switch (type)
    {
    case cat: return 4;
    case dog: return 4;
    case chicken: return 2;
    default:  return 0;
    }
}


int main()
{
    constexpr AnimalType animal{ cat };
    std::cout << "A " << animalName(animal) << " has " << numLegs(animal) << " legs\n";

    return 0;
}
```

在这个程序中，编写了一些函数，这些函数允许我们做一些事情，如获取动物的腿数，以及获取动物的名称。

虽然这很好，但考虑一下当想更新这个程序时会发生什么，如果想添加动物蛇。向代码中添加蛇，需要修改AnimalType、numLegs()和animalName()。如果这是一个大的代码库，还需要更新使用AnimalType的任何其他相关函数——如果AnimalType在许多地方使用，那么可能有许多代码需要修改（很容易引入错误）。

现在，让我们使用OOP思维来编写相同的程序（产生相同的输出）：

```C++
#include <iostream>
#include <string_view>

struct Cat
{
    std::string_view name{ "cat" };
    int numLegs{ 4 };
};

struct Dog
{
    std::string_view name{ "dog" };
    int numLegs{ 4 };
};

struct Chicken
{
    std::string_view name{ "chicken" };
    int numLegs{ 2 };
};

int main()
{
    constexpr Cat animal;
    std::cout << "a " << animal.name << " has " << animal.numLegs << " legs\n";

    return 0;
}
```

在本例中，每个动物都是其自己的类型，并且该类型管理与该动物相关的所有内容。

现在考虑这样一个情况，如果想添加动物蛇。我们所要做的就是创建一个蛇类型。几乎不需要更改现有代码，这意味着破坏已经工作的代码的风险要小得多。

上面的猫、狗和鸡示例有许多重复（因为每个都定义了完全相同的成员集）。在这种情况下，创建通用的Animal结构并为每个动物创建实例可能更可取。但如果我们想向Chicken添加一个不适用于其他动物的新成员（例如，每天下蛋的个数），该怎么办？在后面会介绍，通过使用OOP模型，我们可以将该成员限制为只属于Chicken对象。

***
## OOP带来了其他好处

在学校，当你提交编程作业时，你的工作基本上已经完成。您的老师或助教将运行您的代码，以查看它是否产生正确的结果。根据运行结果，你会相应地被评分。然后您的代码大概率会被丢弃。

在实际工作中，当您将代码提交到其他开发人员使用的代码库中，或提交到真实用户使用的应用程序中时，这是一种完全不同的情况。一些新的操作系统或软件版本将破坏您的代码。用户将发现您所犯的一些逻辑错误。业务合作伙伴将需要一些新的功能。其他开发人员将需要在不破坏代码的情况下扩展您的代码。您的代码需要能够进化，并且它需要能够以最小的时间投入、最小的头痛和最小的破坏来做到这一点。

解决这些问题的最佳方法是尽可能保持代码的模块化（和非冗余）。为了帮助实现这一点，OOP还引入了许多其他有用的概念：继承、封装、抽象和多态。

我们将在适当的时候讨论所有这些都是什么，以及它们如何帮助减少代码的冗余，并更容易修改和扩展。一旦您正确地熟悉了OOP并使用了它，您可能永远不会想再回到纯过程编程。

也就是说，OOP并不能取代过程编程——相反，它在编程工具带中为您提供了额外的工具，以帮助在需要时管理复杂性。

***
## 术语“对象”

请注意，术语“对象”在不同地方有不同的含义，这会导致一定程度的混淆。在传统编程中，对象是存储值的存储空间。在面向对象编程中，“对象”意味着它既是传统编程意义上的对象，又是属性和行为的组合。在本教程中，将倾向于术语对象的传统含义，并在特别提到OOP对象时更倾向于术语“类对象”。

***