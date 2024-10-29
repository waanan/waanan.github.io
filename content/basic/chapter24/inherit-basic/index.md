---
title: "基本继承"
date: 2024-10-08T17:45:57+08:00
---

我们已经讨论了什么是抽象意义上的继承，现在讨论一下如何在C++中使用它。

C++中的继承发生在类之间。在继承（是一个，is-a）关系中，被继承的类称为父类、基类或超类，而进行继承的类则称为子类或派生类。

{{< img src="./fruit.jpg" title="水果层次">}}

在上图中，水果 是父类，苹果 和 香蕉 都是子类。

{{< img src="./shape.jpg" title="形状层次">}}

在上图中，三角形 既是形状的子类，也是 等边三角形 的父对象。

子类从父类继承行为（成员函数）和属性（成员变量）（受将在未来课程中介绍的一些访问限制的限制）。继承的变量和函数成为子类的成员。

因为子类是独立的类，所以它们（当然）可以有自己的特定于该类的成员。稍后我们将看到一个例子。

***
## Person类

这里有一个简单的类来表示一般的人：

```C++
#include <string>
#include <string_view>

class Person
{
// 简单示意，所以成员全是public
public:
    std::string m_name{};
    int m_age{};

    Person(std::string_view name = "", int age = 0)
        : m_name{ name }, m_age{ age }
    {
    }

    const std::string& getName() const { return m_name; }
    int getAge() const { return m_age; }

};
```

因为这个Person类被设计为表示一般的人，所以我们只定义了对任何类型的人都通用的成员。每个人（无论性别、职业等……）都有名字和年龄，因此这些都在这里表示。

注意，在这个例子中，将所有变量和函数设置为public的。这是为了使这些示例保持简单。通常，我们会将变量设为私有。将在本章后面讨论访问控制以及这些访问控制如何与继承交互。

***
## BaseballPlayer类

假设我们想编写一个程序来跟踪一些棒球运动员的信息。棒球运动员需要包含特定于棒球运动员的信息——例如，我们可能希望存储运动员的击球平均数，以及他们击出的本垒打次数。

这是我们不完整的棒球手类：

```C++
class BaseballPlayer
{
// 简单示意，所以成员全是public
public:
    double m_battingAverage{};
    int m_homeRuns{};

    BaseballPlayer(double battingAverage = 0.0, int homeRuns = 0)
       : m_battingAverage{battingAverage}, m_homeRuns{homeRuns}
    {
    }
};
```

现在，我们还想跟踪棒球运动员的姓名和年龄，之前已经将该信息作为Person类的一部分。

对于如何向BaseballPlayer添加姓名和年龄，我们有三个选择：

1. 将姓名和年龄直接作为成员添加到BaseballPlayer类。这可能是最糟糕的选择，因为我们正在复制已经存在于Person类中的代码。Person的任何更新都必须在BaseballPlayer中进行。
2. 使用组合将Person添加为BaseballPlayer的成员。但我们必须问自己，“棒球运动员里有Person吗”？这听起来很奇怪。所以这不是正确的范例。
3. 让BaseballPlayer从Person继承这些属性。请记住，继承表示“是一个”关系。棒球运动员是人吗？是的，所以继承在这里是一个很好的选择。

***
## 使BaseballPlayer成为派生类

要使BaseballPlayer从Person类继承，语法相当简单。在类BaseballPlayer声明之后，使用冒号、单词“public”和希望继承的类的名称。这称为public继承。在以后的课程中，我们将详细讨论public继承的含义。

```C++
// BaseballPlayer publicly 继承 Person
class BaseballPlayer : public Person
{
public:
    double m_battingAverage{};
    int m_homeRuns{};

    BaseballPlayer(double battingAverage = 0.0, int homeRuns = 0)
       : m_battingAverage{battingAverage}, m_homeRuns{homeRuns}
    {
    }
};
```

在层次关系图上，继承看起来像这样：

{{< img src="./BaseballPlayerInheritance.gif" title="棒球手继承层级">}}

当BaseballPlayer从Person继承时，BaseballPlayer从Person获取成员函数和变量。此外，BaseballPlayer还定义了自己的两个成员：m_battingAverage和m_homeRuns。这是有意义的，因为这些属性特定于棒球运动员，而不是任何人。

因此，BaseballPlayer对象将具有4个成员变量：来自BaseballPlayer的m_battingAverage和m_homeRuns，以及来自Person的m_name和m_age。

这很容易验证：

```C++
#include <iostream>
#include <string>
#include <string_view>

class Person
{
public:
    std::string m_name{};
    int m_age{};

    Person(std::string_view name = "", int age = 0)
        : m_name{name}, m_age{age}
    {
    }

    const std::string& getName() const { return m_name; }
    int getAge() const { return m_age; }

};

// BaseballPlayer publicly 继承 Person
class BaseballPlayer : public Person
{
public:
    double m_battingAverage{};
    int m_homeRuns{};

    BaseballPlayer(double battingAverage = 0.0, int homeRuns = 0)
       : m_battingAverage{battingAverage}, m_homeRuns{homeRuns}
    {
    }
};

int main()
{
    // 创建一个新的 BaseballPlayer 对象
    BaseballPlayer joe{};
    // 设置 name (因为 m_name 是 public)
    joe.m_name = "Joe";
    // 打印 name
    std::cout << joe.getName() << '\n'; // 使用从父类继承的 getName() 函数

    return 0;
}
```

打印值：

```C++
Joe
```

这将通过编译并运行，因为Joe是BaseballPlayer，并且所有BaseballPlayer对象都有一个m_name成员变量和一个从Person类继承的getName()成员函数。

***
## Employee派生类

现在让我们编写另一个也继承自Person的类。这一次，我们将编写一个Employee类。雇员“是”人，因此使用继承是适当的：

```C++
// Employee publicly 继承 Person
class Employee: public Person
{
public:
    double m_hourlySalary{};
    long m_employeeID{};

    Employee(double hourlySalary = 0.0, long employeeID = 0)
        : m_hourlySalary{hourlySalary}, m_employeeID{employeeID}
    {
    }

    void printNameAndSalary() const
    {
        std::cout << m_name << ": " << m_hourlySalary << '\n';
    }
};
```

Employee从Person继承m_name和m_age（以及两个访问函数），并添加另外两个成员变量和自己的成员函数。请注意，printNameAndSalary()使用它所属的类（Employee::m_hourlySalary）和父类（Person::m_name）中的变量。

这给了我们一个类似这样的层级图：

{{< img src="./EmployeeInheritance.gif" title="Employee继承层级">}}

请注意，Employee和BaseballPlayer没有任何直接关系，即使它们都继承自Person。

下面是一个使用Employee的示例:

```C++
#include <iostream>
#include <string>
#include <string_view>

class Person
{
public:
    std::string m_name{};
    int m_age{};

    Person(std::string_view name = "", int age = 0)
        : m_name{name}, m_age{age}
    {
    }

    const std::string& getName() const { return m_name; }
    int getAge() const { return m_age; }

};

// Employee publicly 继承 Person
class Employee: public Person
{
public:
    double m_hourlySalary{};
    long m_employeeID{};

    Employee(double hourlySalary = 0.0, long employeeID = 0)
        : m_hourlySalary{hourlySalary}, m_employeeID{employeeID}
    {
    }

    void printNameAndSalary() const
    {
        std::cout << m_name << ": " << m_hourlySalary << '\n';
    }
};

int main()
{
    Employee frank{20.25, 12345};
    frank.m_name = "Frank"; // m_name 是 public，所以可以这么写

    frank.printNameAndSalary();

    return 0;
}
```

打印：

```C++
Frank: 20.25
```

***
## 继承链

可以从派生类再进行继承。这样做时没有什么值得注意或特别的东西——一切都像上面的例子那样进行。

例如，让我们编写一个Supervisor类。Supervisor是Employee，也是Person。我们已经编写了一个Employee类，因此让我们使用它作为从中派生的类。

```C++
class Supervisor: public Employee
{
public:
    // Supervisor 可以管理最多 5 个 employees
    long m_overseesIDs[5]{};
};
```

现在，我们的层级视图如下所示：

{{< img src="./SupervisorInheritance.gif" title="Supervisor继承层级">}}

所有Supervisor对象都继承Employee和Person的函数和变量，并添加自己的m_overviewsIDs成员变量。

通过构建这样的继承链，我们可以创建一组非常通用的可重用类（在上层），并在每个继承级别上逐渐变得更具体。

***
## 为什么这种继承有用？

从基类继承意味着我们不必在派生类中重新定义来自基类的信息。我们通过继承自动接收基类的成员函数和成员变量，然后简单地添加所需的附加函数或成员变量。这不仅节省了工作，还意味着如果我们更新或修改基类（例如，添加新函数或修复错误），我们的所有派生类都将自动继承更改！

例如，如果我们曾经向Person添加了一个新函数，那么Employee、Supervisor和BaseballPlayer将自动获得对它的访问权限。如果我们向Employme添加了一种新变量，那么Supervisor也将获得对它进行访问的权限。这允许我们以简单、直观和低维护的方式构造新类！

***
## 结论

继承允许我们通过让其他类继承其成员来重用类。在以后的课程中，我们将继续探索这是如何工作的。

***

{{< prevnext prev="/basic/chapter24/inherit-intro/" next="/basic/chapter24/derived-class-cons-order/" >}}
24.0 继承简介
<--->
24.2 派生类的构造顺序
{{< /prevnext >}}
