---
title: "数据隐藏（封装）的好处"
date: 2024-04-09T13:02:20+08:00
---

在上一课中，提到了类的成员变量通常被设置为私有的。第一次学习类的程序员通常很难理解您为什么要这样做。毕竟，将变量设置为私有意味着它们不能被公共域访问。至多，这在编写类时需要做更多的工作。在最坏的情况下，它可能看起来完全没有意义（特别是如果为私有成员数据提供公共访问功能）。

这个问题的答案是如此基础，我们将在这个主题上花费整节课程！

让我们从一个类比开始。

在现代生活中，可以使用许多机械或电子设备。用遥控器打开/关闭电视。踩下油门踏板使汽车向前行驶。可以通过拨动开关来打开灯。所有这些设备都有一些共同点：它们提供了一个简单的用户界面（一组按钮、踏板、开关等……），允许执行按键操作。

这些设备的实际操作方式是隐藏的。当按下遥控器上的按钮时，不需要知道遥控器如何与电视通信。当踩下汽车上的油门时，并不需要知道内燃机是如何使车轮转动的。当拍照时，不需要知道传感器是如何收集光线并将其转化为像素图像的。

接口和实现的这种分离非常有用，因为它允许我们使用对象，而不必了解它们是如何工作的——相反，只需要了解如何与它们交互。这大大降低了使用这些对象的复杂性，并增加了能够与之交互的对象的数量。

***
## 类类型中的实现和接口

出于类似的原因，接口和实现的分离在编程中很有用。但首先，让我们定义关于类类型的接口和实现的含义。

类类型的接口，定义类类型的用户将如何与类类型的对象交互。由于只能从类类型外部访问公共成员，因此类类型的公共成员形成其接口。因此，由公共成员组成的接口有时称为公共接口。

接口是类的作者和类的用户之间的隐式契约。如果现有接口被更改，则使用它的任何代码都可能会无法使用。因此，确保类类型的接口设计良好且稳定（不要改变太多）是很重要的。

类类型的实现，由实际使类按预期行为的代码组成。这包括存储数据的成员变量，以及包含程序逻辑和操作成员变量的成员函数。

***
## 数据隐藏（封装）

在编程中的数据隐藏，通过对用户隐藏程序定义的数据类型的实现，来强制实现接口和实现分离。

{{< alert success >}}
**术语**

术语封装有时也用于指代数据隐藏。然而，该术语也用于指将数据和功能捆绑在一起（不考虑访问控制），因此其使用可能是不明确的。在本教程系列中，将假设所有封装的类都实现了数据隐藏。

{{< /alert >}}

***
## 如何实现数据隐藏

在C++类类型中实现数据隐藏很简单。

首先，确保类类型的数据成员是私有的（因此用户不能直接访问它们）。成员函数体中的语句已经不能被用户直接访问。

其次，确保成员函数是公共的，以便用户可以调用它们。

通过遵循这些规则，强制类类型的用户使用公共接口操作对象，并防止他们直接访问实现细节。

在C++中定义的类应该使用数据隐藏。事实上，标准库提供的所有类都是这样做的。另一方面，结构体不应使用数据隐藏，因为具有非公共成员会阻止它们被视为聚合。

以这种方式定义类需要类作者做一些额外的工作。并且要求类的用户使用公共接口，这似乎比直接提供对成员变量的公共访问更麻烦。但这样做提供了大量有用的好处，有助于鼓励类的可重用性和可维护性。将在本课的剩余部分讨论这些好处。

***
## 数据隐藏使类更易于使用，并降低了复杂性

要使用封装的类，不需要知道它是如何实现的。只需要理解它的接口：哪些成员函数是公开可用的，它们采用什么参数，以及它们返回什么值。

例如：

```C++
#include <iostream>
#include <string_view>

int main()
{
    std::string_view sv{ "Hello, world!" };
    std::cout << sv.length();

    return 0;
}
```

在这个简短的程序中，没有看到如何实现std::string_view的详细信息。也无法看到一个std::string_view有多少数据成员，它们的名称是什么，或者它们是什么类型。也不知道length()成员函数如何返回正在查看的字符串的长度。

最重要的是，不必知道！这个程序效果符合预期。需要知道的只是如何初始化类型为std::string_view的对象，以及length()成员函数返回的内容。

不必关心这些细节会显著降低程序的复杂性，从而减少错误。与任何其他原因相比，这是封装的关键优势。

想象一下，如果您必须理解如何实现std::string、std::vector或std::cout才能使用它们，C++会变得多么复杂！

***
## 数据隐藏允许我们维护不变量

之前我们介绍了类不变量的概念，这些条件在对象的整个生命周期中都必须为真，以便对象保持有效状态。

考虑以下程序：

```C++
#include <iostream>
#include <string>

struct Employee // 成员默认是 public
{
    std::string name{ "John" };
    char firstInitial{ 'J' }; // 需要是name的首字母

    void print() const
    {
        std::cout << "Employee " << name << " has first initial " << firstInitial << '\n';
    }
};

int main()
{
    Employee e{}; // 默认是 "John" 和 'J'
    e.print();

    e.name = "Mark"; // name 是 "Mark"
    e.print(); // 但是首字母是错的

    return 0;
}
```

该程序打印：

```C++
John has first initial J
Mark has first initial J
```

Employee结构体具有一个类不变量，即firstInitial应始终等于name的第一个字符。不满足的话print()函数将打印出错误的结果。

因为名称name是公共的，所以main()中的代码能够将e.name设置为“Mark”，并且firstInitial成员不会更新。不变量被破坏了，对print()的第二次调用没有按预期工作。

当为用户提供对类实现的直接访问时，他们将负责维护所有不变量——他们可能不会这样做（可能根本不会）。将此负担放在用户身上会增加许多复杂性。

让我们重写此程序，使成员变量私有化，并公开成员函数以设置Employee的名称：

```C++
#include <iostream>
#include <string>
#include <string_view>

class Employee // 成员默认是 private
{
    std::string m_name{};
    char m_firstInitial{};

public:
    void setName(std::string_view name)
    {
        m_name = name;
        m_firstInitial = name.front(); // 使用 std::string::front() 获取 `name` 的第一个字母
    }

    void print() const
    {
        std::cout << "Employee " << m_name << " has first initial " << m_firstInitial << '\n';
    }
};

int main()
{
    Employee e{};
    e.setName("John");
    e.print();

    e.setName("Mark");
    e.print();

    return 0;
}
```

该程序现在按预期工作：

```C++
John has first initial J
Mark has first initial M
```

从用户的角度来看，唯一的变化是，他们不是直接为name赋值，而是调用成员函数setName()，该函数设置m_name和m_firstInitial。用户免除了必须维护此不变量的负担！

***
## 数据隐藏允许更好地进行错误检测（和处理）

在上面的程序中，m_firstInitial必须与m_name的第一个字符匹配。因为m_firstInitial独立于m_name存在，通过将数据成员m_firstInitial替换为返回第一个初始值的成员函数，可以删除该变量：

```C++
#include <iostream>
#include <string>

class Employee
{
    std::string m_name{ "John" };

public:
    void setName(std::string_view name)
    {
        m_name = name;
    }

    // 使用 std::string::front() 获取 `m_name` 的首字母
    char firstInitial() const { return m_name.front(); }

    void print() const
    {
        std::cout << "Employee " << m_name << " has first initial " << firstInitial() << '\n';
    }
};

int main()
{
    Employee e{}; // 默认初始化为 "John"
    e.setName("Mark");
    e.print();

    return 0;
}
```

然而，这个程序有另一个类不变量。花点时间看看你能不能确定它是什么？

答案是m_name不应该是空字符串（因为每个Employee都应该有一个名称）。如果将m_name设置为空字符串，则不会立即发生任何错误。但如果随后调用firstInitial()，则std::string的front()成员将尝试获取空字符串的第一个字母，这将导致未定义的行为。

理想情况下，希望防止m_name为空。

如果用户对m_name成员具有公共访问权限，他们可以自行设置m_name = ""，我们无法防止这种情况发生。

然而，因为我们强制用户通过公共接口函数 setName() 设置m_name，所以可以让 setName() 验证用户是否传入了有效的名称。如果名称不为空，则可以将其分配给m_name。如果名称是空字符串，可以做许多事情来响应：

1. 忽略请求
2. assert检查
3. 抛出异常
4. 等等

这里的要点是，可以检测到滥用，然后以我们认为最合适的方式处理它。

***
## 数据隐藏使得可以在不破坏现有程序的情况下更改实现细节

考虑这个简单的例子：

```C++
#include <iostream>

struct Something
{
    int value1 {};
    int value2 {};
    int value3 {};
};

int main()
{
    Something something;
    something.value1 = 5;
    std::cout << something.value1 << '\n';
}
```

虽然该程序工作良好，但如果决定更改类的实现细节，如下所示，会发生什么情况？

```C++
#include <iostream>

struct Something
{
    int value[3] {}; // 使用长度为3的数组
};

int main()
{
    Something something;
    something.value1 = 5;
    std::cout << something.value1 << '\n';
}
```

还没有介绍数组，但不用担心。这里的要点是，该程序不再能够编译，因为名为value1的成员不再存在，并且main() 中的语句仍在使用该标识符。

数据隐藏使我们能够在不破坏使用类的程序的情况下更改类的实现方式。

下面是使用函数访问m_value1的封装版本：

```C++
#include <iostream>

class Something
{
private:
    int m_value1 {};
    int m_value2 {};
    int m_value3 {};

public:
    void setValue1(int value) { m_value1 = value; }
    int getValue1() const { return m_value1; }
};

int main()
{
    Something something;
    something.setValue1(5);
    std::cout << something.getValue1() << '\n';
}
```

现在，将类的实现改回数组：

```C++
#include <iostream>

class Something
{
private:
    int m_value[3]; // 注: 更改了类的实现方式!

public:
    // 更新函数的实现，以匹配对应的成员变量
    void setValue1(int value) { m_value[0] = value; }
    int getValue1() const { return m_value[0]; }
};

int main()
{
    // 使用到类的地方不用做改动
    Something something;
    something.setValue1(5);
    std::cout << something.getValue1() << '\n';
}
```

因为没有更改类的公共接口，所以使用该接口的程序根本不需要更改，并且仍然以相同的方式运行。

类似地，如果小精灵在晚上偷偷溜进你的房子，用不同（但兼容）的技术更换你的电视遥控器的内部部件，你可能根本不会注意到！

***
## 具有接口的类更容易调试

最后，封装可以帮助您在出现问题时调试程序更容易。通常，当程序不能正常工作时，是因为一个成员变量被赋予了不正确的值。如果每个人都能够直接设置成员变量，那么跟踪哪段代码实际将成员变量修改为错误的值可能会很困难。这可能涉及断点监控修改成员变量的每个语句——有许多这样的语句。

然而，如果成员只能通过单个成员函数更改，那么可以简单地中断该单个函数，并观察每个调用方更改值。这可以更容易地确定谁是罪魁祸首。

***
## 优先使用非成员函数

在C++中，如果函数可以实现为非成员函数，请考虑将其实现为非会员函数，而不是成员函数。

这有许多好处：

1. 非成员函数不是类接口的一部分。因此，类的接口将更小、更直观，使类更容易理解。
2. 非成员函数强制封装，因为这样的函数必须通过类的公共接口工作。不存在仅仅因为方便而直接访问成员变量的诱惑。
3. 在更改类的实现时，不需要考虑非成员函数（只要接口没有以不兼容的方式更改）。
4. 非成员函数往往更容易调试。
5. 包含特定于应用程序的数据和逻辑的非成员函数可以与类的可重用部分分离。


下面是三个类似的例子，按从最坏到最好的顺序排列：

```C++
#include <iostream>
#include <string>

class Yogurt
{
    std::string m_flavor{ "vanilla" };

public:
    void setFlavor(std::string_view flavor)
    {
        m_flavor = flavor;
    }

    std::string_view getFlavor() const { return m_flavor; }

    // 最坏: 成员函数 print() 直接访问 m_flavor，但已经有一个 m_flavor 的 getter函数
    void print() const
    {
        std::cout << "The yogurt has flavor " << m_flavor << '\n';
    }
};

int main()
{
    Yogurt y{};
    y.setFlavor("cherry");
    y.print();

    return 0;
}
```

以上是最差的版本。当 m_flavor 的getter已经存在时，print() 成员函数直接访问m_flavor。如果类实现被更新，那么print() 也可能被修改。print() 打印的字符串是特定于应用程序的（使用该类的另一个应用程序可能希望打印其他内容，这将需要克隆或修改该类）。

```C++
#include <iostream>
#include <string>

class Yogurt
{
    std::string m_flavor{ "vanilla" };

public:
    void setFlavor(std::string_view flavor)
    {
        m_flavor = flavor;
    }

    std::string_view getFlavor() const { return m_flavor; }

    // 好一点: 成员函数 print() 不直接访问成员
    void print(std::string_view prefix) const
    {
        std::cout << prefix << ' ' << getFlavor() << '\n';
    }
};

int main()
{
    Yogurt y{};
    y.setFlavor("cherry");
    y.print("The yogurt has flavor");

    return 0;
}
```

上面的版本更好，但仍然不足够好。print() 仍然是成员函数，但至少它现在不直接访问任何数据成员。如果类的成员有变动，print函数不需要跟着修改。print() 函数现在将打印的前缀作为参数prefix传入。但该函数仍然对如何打印内容施加约束（例如，它总是打印为prefix、空格、getFlavor()、换行符）。如果这不满足给定应用程序的需求，则需要添加另一个函数。

```C++
#include <iostream>
#include <string>

class Yogurt
{
    std::string m_flavor{ "vanilla" };

public:
    void setFlavor(std::string_view flavor)
    {
        m_flavor = flavor;
    }

    std::string_view getFlavor() const { return m_flavor; }
};

// 最佳: 非成员函数 print() 不是类接口的一部分
void print(const Yogurt& y)
{
        std::cout << "The yogurt has flavor " << y.getFlavor() << '\n';
}

int main()
{
    Yogurt y{};
    y.setFlavor("cherry");
    print(y);

    return 0;
}
```

以上版本是最好的。print() 现在是一个非成员函数。它不直接访问任何成员。即使类成员发生更改，也不需要更改print。此外，每个应用程序都可以提供自己的print() 函数，可以自行控制打印方式。

{{< alert success >}}
**最佳实践**

如果可能，最好将函数实现为非成员函数（特别是包含特定于应用程序的数据或逻辑的函数）。

{{< /alert >}}

{{< alert success >}}
**注**

为了使示例尽可能简洁，我们的许多示例都没有实现这种最佳实践。

{{< /alert >}}

***
## 类成员声明的顺序

在类之外编写代码时，需要声明变量和函数，然后才能使用它们。然而，在类内部，这种限制不存在。可以按自己喜欢的顺序排列成员。

那么应该如何排列它们呢？

这里有两个流派：

1. 首先列出私有成员，然后列出公共成员函数。这遵循了使用前声明的传统风格。任何查看您的类代码的人都会看到您在使用数据成员之前是如何定义它们的，这可以使阅读和理解实现细节变得更加容易。
2. 首先列出您的公共成员，并将您的私人成员放在底部。因为使用您的类的人对公共接口感兴趣，所以将您的公共成员放在首位会使他们需要的信息放在最前面，并将实现细节（最不重要的）放在最后。


在现代C++中，更通常推荐第二种方法（公共成员优先），特别与其他开发人员共享的代码。

{{< alert success >}}
**最佳实践**

首先声明公共成员，然后声明受保护成员，最后声明私有成员。这突出了公共接口，并淡化了实现细节。

{{< /alert >}}

{{< alert success >}}
**注**

本网站上的大多数示例使用与建议相反的声明顺序。因为在学习语言机制时，这种顺序更直观，这里我们专注于实现细节和剖析事物如何工作。

{{< /alert >}}

{{< alert success >}}
**对于高级读者**

Google C++风格指南推荐以下顺序：

1. 类型和类型别名（typedef、using、enum、嵌套结构体和类以及友元类型）
2. 静态常量
3. 工厂函数
4. 构造函数和赋值运算符
5. 析构函数
6. 所有其他函数（静态和非静态成员函数以及友元函数）
7. 数据成员（静态和非静态）

{{< /alert >}}

***

{{< prevnext prev="/basic/chapter14/member-func-ret-member-data-ref/" next="/basic/chapter14/construct/" >}}
14.6 成员函数返回对数据成员的引用
<--->
14.8 构造函数简介
{{< /prevnext >}}
