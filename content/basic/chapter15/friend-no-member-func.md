---
title: "友元非成员函数"
date: 2024-06-24T18:56:16+08:00
---

在之前，我们一直在宣扬访问控制的优点，它提供了一种机制来控制谁可以访问类的各个成员。私有成员只能由类的其他成员访问，而公共成员可以由每个人访问。我们讨论了保持数据私有化的好处，以及创建供非成员使用的公共接口。

然而，在某些情况下，这种安排要么是不充分的，要么是不理想的。

例如，考虑一个专注于管理某些数据集的存储类。现在假设您也想显示该数据，但处理显示的代码将有许多选项，因此很复杂。您可以将存储管理功能和显示管理功能放在同一个类中，但这会使事情变得混乱，并形成复杂的界面。您还可以将它们分开：存储类管理存储，而其他一些显示类管理所有的显示功能。这创造了一个很好的责任分离。但显示类随后将无法访问存储类的私有成员，并且可能无法执行其工作。

或者，在语法上，我们可能更喜欢使用非成员函数而不是成员函数（我们将在下面展示一个例子）。重载运算符时通常是这种情况，这是我们将在以后的课程中讨论的主题。但非成员函数也有相同的问题——它们不能访问类的私有成员。

如果访问函数（或其他公共成员函数）已经存在，并且对于我们试图实现的任何功能都足够，那么很好——可以（并且应该）只使用它们。但在某些情况下，这些函数并不存在。然后呢？

一种选择是向类中添加新的成员函数，以允许其他类或非成员函数执行它们在其他情况下无法执行的任何工作。但我们可能不希望允许公共访问这些东西——也许这些东西高度依赖于实现，或者容易被滥用。

真正需要的是在个案基础上颠覆访问控制系统的某种方法。

***
## friend是神奇的

这些挑战的答案是friend。

在类的主体中，可以使用友元声明（使用friend关键字）来告诉编译器，其他一些类或函数现在是友元。在C++中，友元是一个类或函数（成员或非成员），它被授予对另一个类的私有和受保护成员的完全访问权限。通过这种方式，类可以有选择地授予其他类或函数对其成员的完全访问权限，而不会影响其他任何内容。

例如，如果我们的存储类使display类成为朋友，那么display类将能够直接访问存储类的所有成员。display类可以使用这种直接访问来实现存储类的显示，同时在结构上保持独立。

友元声明不受访问控制的影响，因此它在类主体中的位置并不重要。

既然我们知道了什么是友元，那么让我们看一看将友谊授予非成员函数、成员函数和其他类的特定示例。在本课中，将讨论友元非成员函数，然后在下一课学习友元类和友元成员函数。

{{< alert success >}}
**关键点**

友谊总是由其成员将被访问的类授予（而不是由希望访问的类或函数授予）。在访问控制和授予友谊之间，类始终保留控制谁可以访问其成员的能力。

{{< /alert >}}

***
## 友元非成员函数

友元函数是一个函数（成员或非成员），可以访问类的私有成员和受保护成员，就像它是该类的成员一样。在所有其他方面，友元函数是正常的函数。

让我们看一个简单类的示例，该类使非成员函数成为友元：

```C++
#include <iostream>

class Accumulator
{
private:
    int m_value { 0 };

public:
    void add(int value) { m_value += value; }

    // 这里是友元声明，授予非成员函数  void print(const Accumulator& accumulator) 对 Accumulator 的访问能力
    friend void print(const Accumulator& accumulator);
};

void print(const Accumulator& accumulator)
{
    // 因为 print() 是 Accumulator 的友元
    // 因此可以访问 Accumulator 的私有变量
    std::cout << accumulator.m_value;
}

int main()
{
    Accumulator acc{};
    acc.add(5); // 将 5 加到 accumulator

    print(acc); // 调用 print() 非成员函数

    return 0;
}
```

在这个例子中，声明了一个名为 print() 的非成员函数，该函数接受Accumulator类的对象。因为 print() 不是Accumulator类的成员，所以它通常不能访问私有成员m_value。然而，Accumulator类有一个友元声明，使「void print(const Accumulator& accumulator)」成为友元。

请注意，因为 print() 是非成员函数（因此没有隐式对象），所以必须显式地将Accumulator对象传递给 print() 。

***
## 在类内定义友元非成员

类似于成员函数可以在类内定义（如果需要），友元非成员函数也可以在类中定义。下面的示例在Accumulator类中定义友元非成员函数 print() ：

```C++
#include <iostream>

class Accumulator
{
private:
    int m_value { 0 };

public:
    void add(int value) { m_value += value; }

    // 类中定义的友元非成员函数
    friend void print(const Accumulator& accumulator)
    {
    // 因为 print() 是 Accumulator 的友元
    // 因此可以访问 Accumulator 的私有变量
        std::cout << accumulator.m_value;
    }
};

int main()
{
    Accumulator acc{};
    acc.add(5); // 将 5 加到 accumulator

    print(acc); // 调用 print() 非成员函数

    return 0;
}
```

尽管您可能会假设，由于 print() 是在Accumulator中定义的，这使得print() 成为Accumulator的成员，但事实并非如此。因为 print() 被定义为友元，所以它被视为非成员函数（就像它是在Accumulator外部定义的一样）。

***
## 语法上优先使用友元非成员函数

在本课的介绍中提到，有时我们可能更喜欢使用非成员函数而不是成员函数。现在展示一个例子。

```C++
#include <iostream>

class Value
{
private:
    int m_value{};

public:
    explicit Value(int v): m_value { v }  { }

    bool isEqualToMember(const Value& v) const;
    friend bool isEqualToNonmember(const Value& v1, const Value& v2);
};

bool Value::isEqualToMember(const Value& v) const
{
    return m_value == v.m_value;
}

bool isEqualToNonmember(const Value& v1, const Value& v2)
{
    return v1.m_value == v2.m_value;
}

int main()
{
    Value v1 { 5 };
    Value v2 { 6 };

    std::cout << v1.isEqualToMember(v2) << '\n';
    std::cout << isEqualToNonmember(v1, v2) << '\n';

    return 0;
}
```

在这个例子中，定义了两个类似的函数，用于检查两个Value对象是否相等。isEqualToMember()是成员函数，isEquallToNonmember() 是非成员函数。让我们专注于如何定义这些函数。

在isEqualToMember()中，隐式传递一个对象，显式传递另一个对象。函数的实现反映了这一点，必须在思想上协调m_value属于隐式对象，而v.m_value则属于显式参数。

在isEqualToNonmember()中，两个对象都是显式传递的。这导致函数实现中更好的对称性，因为m_value成员有一个显式的前缀。

您可能仍然更喜欢调用语法v1.isEqualToMember(v2)，而不是isEquallToNonmember(v1, v2)。但当我们讨论操作符重载时，将看到这个主题再次出现。

***
## 多个友元

一个函数可以同时是多个类的友元。例如，考虑以下示例：

```C++
#include <iostream>

class Humidity; // 前向声明 Humidity

class Temperature
{
private:
    int m_temp { 0 };
public:
    explicit Temperature(int temp) : m_temp { temp } { }

    friend void printWeather(const Temperature& temperature, const Humidity& humidity); // 这一行需要 Humidity 的前向声明
};

class Humidity
{
private:
    int m_humidity { 0 };
public:
    explicit Humidity(int humidity) : m_humidity { humidity } {  }

    friend void printWeather(const Temperature& temperature, const Humidity& humidity);
};

void printWeather(const Temperature& temperature, const Humidity& humidity)
{
    std::cout << "The temperature is " << temperature.m_temp <<
       " and the humidity is " << humidity.m_humidity << '\n';
}

int main()
{
    Humidity hum { 10 };
    Temperature temp { 12 };

    printWeather(temp, hum);

    return 0;
}
```

关于这个例子，有三点值得注意。首先，由于printWeather() 平等地使用湿度和温度，因此将其作为其中一个的成员是没有意义的。非成员函数工作得更好。其次，因为printWeather() 是湿度和温度的友元，所以它可以从这两个类的对象访问私有数据。最后，请注意示例顶部的以下行：

```C++
class Humidity;
```

这是湿度类的前向声明。类前向声明的作用与函数前向声明相同——它们将稍后定义的标识符告知编译器。然而，与函数不同，类没有返回类型或参数，因此类前向声明总是简单的类名（除非它们是类模板）。

如果没有这一行，编译器将在解析Temperature中的友元声明时告诉我们它不知道Humidity是什么。

***
## 友元不是违反了数据隐藏的原则吗？

不。友元是由进行数据隐藏的类授予的，该类期望友元访问其私有成员。将友元视为类本身的扩展，具有相同的访问权限。因此，访问是预期的，而不是违规。

如果使用得当，友元可以使程序更易于维护，因为它允许在从设计角度看有意义时分离函数（而不是出于访问控制的原因必须将其保持在一起）。或者当使用非成员函数。

然而，因为友元可以直接访问类的实现，所以对类的实现的更改通常也需要对友元进行更改。如果一个类有许多友元（或者那些友元有友元），这可能会导致连锁反应。

在实现友元函数时，尽可能使用公共接口而不是直接访问成员。这将有助于将您的友元函数与未来的实现更改隔离开来，并减少需要在以后修改和/或重新测试的代码。

{{< alert success >}}
**最佳实践**

友元函数应该尽可能使用类接口而不是直接访问。

{{< /alert >}}

***
## 与友元函数相比，优先使用非友元函数

在讨论数据隐藏（封装）的好处中，我们提到应该更喜欢非成员函数，而不是成员函数。出于同样的原因，应该更喜欢非友元函数而不是友元函数。

例如，在下面的示例中，如果Accumulator的实现被更改（例如，我们重命名m_value），那么print()的实现也需要更改：

```C++
#include <iostream>

class Accumulator
{
private:
    int m_value { 0 }; // 如果重名这里

public:
    void add(int value) { m_value += value; } // 这里需要修改

    friend void print(const Accumulator& accumulator);
};

void print(const Accumulator& accumulator)
{
    std::cout << accumulator.m_value; // 这里也需要修改
}

int main()
{
    Accumulator acc{};
    acc.add(5); // 将 5 加到 accumulator

    print(acc); // 调用 print() 非成员函数

    return 0;
}
```

更好的方式如下：

```C++
#include <iostream>

class Accumulator
{
private:
    int m_value { 0 };

public:
    void add(int value) { m_value += value; }
    int value() const { return m_value; } // 添加合理的访问函数
};

void print(const Accumulator& accumulator) // 不再是 Accumulator 的友元
{
    std::cout << accumulator.value(); // 使用访问函数而不是直接访问
}

int main()
{
    Accumulator acc{};
    acc.add(5); // 将 5 加到 accumulator

    print(acc); // 调用 print() 非成员函数

    return 0;
}
```

在本例中，print() 使用访问函数 value() 获取m_value的值，而不是直接访问m_value。现在，如果Accumulator的实现发生了更改，则不需要更新print() 。

在向现有类的公共接口添加新成员时要小心，因为每个函数（即使是微不足道的函数）都会增加一定程度的混乱和复杂性。在上述Accumulator的情况下，具有访问函数来获取当前累积值是完全合理的。在更复杂的情况下，最好使用友元，而不是向类的接口添加许多新的访问函数。

{{< alert success >}}
**最佳实践**

在可能和合理的情况下，更喜欢非友元函数。

{{< /alert >}}

***

{{< prevnext prev="/basic/chapter15/static-member-func/" next="/basic/chapter15/friend-class/" >}}
15.6 静态成员函数
<--->
15.8 友元类和友元成员函数
{{< /prevnext >}}
