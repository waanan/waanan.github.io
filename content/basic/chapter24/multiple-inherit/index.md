---
title: "多重继承"
date: 2024-10-08T17:45:57+08:00
---

到目前为止，我们提供的所有继承示例都是单继承的——也就是说，每个继承的类都有一个且只有一个父类。然而，C++提供了进行多重继承的能力。

多重继承使派生类能够从多个父级类继承成员。假设我们想编写一个程序来跟踪一群老师。教师是一个人。然而，教师也是雇员。多重继承可用于创建从Person和Employee继承属性的Teacher类。要使用多重继承，只需指定每个基类（就像在单个继承中一样），用逗号分隔：

{{< img src="./PersonTeacher.gif" title="Teacher类多重继承">}}

```C++
#include <string>
#include <string_view>

class Person
{
private:
    std::string m_name{};
    int m_age{};

public:
    Person(std::string_view name, int age)
        : m_name{ name }, m_age{ age }
    {
    }

    const std::string& getName() const { return m_name; }
    int getAge() const { return m_age; }
};

class Employee
{
private:
    std::string m_employer{};
    double m_wage{};

public:
    Employee(std::string_view employer, double wage)
        : m_employer{ employer }, m_wage{ wage }
    {
    }

    const std::string& getEmployer() const { return m_employer; }
    double getWage() const { return m_wage; }
};

// Teacher public 继承 Person 和 Employee
class Teacher : public Person, public Employee
{
private:
    int m_teachesGrade{};

public:
    Teacher(std::string_view name, int age, std::string_view employer, double wage, int teachesGrade)
        : Person{ name, age }, Employee{ employer, wage }, m_teachesGrade{ teachesGrade }
    {
    }
};

int main()
{
    Teacher t{ "Mary", 45, "Boo", 14.3, 8 };

    return 0;
}
```

***
## 继承链

mixin 

mixin（也称为“mix-in”）是一个小类，可以从中继承，以便将属性添加到类中。名称mixin表示该类打算混合到其他类中，而不是单独实例化。

在下面的示例中，Box、Label和Tooltip类是我们从中继承的mixin，以便创建新的Button类。

```C++
// h/t to reader Waldo for this example
#include <string>

struct Point2D
{
	int x{};
	int y{};
};

class Box // mixin Box class
{
public:
	void setTopLeft(Point2D point) { m_topLeft = point; }
	void setBottomRight(Point2D point) { m_bottomRight = point; }
private:
	Point2D m_topLeft{};
	Point2D m_bottomRight{};
};

class Label // mixin Label class
{
public:
	void setText(const std::string_view str) { m_text = str; }
	void setFontSize(int fontSize) { m_fontSize = fontSize; }
private:
	std::string m_text{};
	int m_fontSize{};
};

class Tooltip // mixin Tooltip class
{
public:
	void setText(const std::string_view str) { m_text = str; }
private:
	std::string m_text{};
};

class Button : public Box, public Label, public Tooltip {}; // Button using three mixins

int main()
{
	Button button{};
	button.Box::setTopLeft({ 1, 1 });
	button.Box::setBottomRight({ 10, 10 });
	button.Label::setText("Submit");
	button.Label::setFontSize(6);
	button.Tooltip::setText("Submit the form to the server");
}
```

您可能想知道，当在大多数情况下不需要使用显式Box:：、Label:：和Tooltip:：范围分辨率前缀时，为什么要使用显式的Box:：。

标签：：setText（）和工具提示：：setText（）具有相同的原型。如果调用button.setText（），编译器将产生不明确的函数调用编译错误。在这种情况下，我们必须使用前缀来消除所需版本的歧义。在不模棱两可的情况下，使用mixin名称提供了关于函数调用应用于哪个mixin的文档，这有助于使我们的代码更容易理解。如果我们添加额外的mixin，不模糊的情况在将来可能会变得模糊。使用显式前缀有助于防止发生这种情况。

对于高级读取器

因为mixin旨在向派生类添加功能，而不是提供接口，所以mixin通常不使用虚拟函数（在下一章中介绍）。相反，如果mixin类需要定制为以特定的方式工作，则通常使用模板。

由于这个原因，mixin类通常是模板化的。也许令人惊讶的是，派生类可以使用派生类作为模板类型参数从mixin基类继承。这种继承称为奇循环模板模式（简称CRTP），如下所示

：//奇循环模板图案（CRTP）模板<class T>class Mixin{//Mixin<T>可以使用模板类型参数T来访问Derived//via（static_cast<T*>（this））}的成员；派生类：公共Mixin<Derived>{}；


多重继承的问题

虽然多重继承似乎是单个继承的简单扩展，但多重继承引入了许多问题，这些问题会显著增加程序的复杂性，并使它们成为维护的噩梦。让我们来看看其中的一些情况。

首先，当多个基类包含同名的函数时，可能会导致歧义。例如：

#include<iostream>class USBDevice{private:long m_id{}；公共：USBDevice（长id）：m_id{id}{}长getID（）const{return m_id；}}；类网络设备{private:long m_id{}；public:NetworkDevice（长id）：m_id{id}{}long getID（）const{return m_id；}}；类WirelessAdapter:public USB设备，public NetworkDevice{public:WirelessA适配器（长usbId，长networkId）：USB设备{usbId}，网络设备{networkId}{}}；int main（）{WirelessAdapter c54G{5442，181742}；标准：：cout<<c54G.getID（）；//我们调用哪个getID（）？返回0；}

在编译c54G.getID（）时，编译器会查看WirelessAdapter是否包含名为getID（.）的函数。编译器然后查看是否有任何父类具有名为getID（）的函数。看到这里的问题了吗？问题是c54G实际上包含两个getID（）函数：一个从USBDevice继承，另一个从NetworkDevice继承。因此，此函数调用是不明确的，如果尝试编译它，将收到编译器错误。

然而，有一种方法可以解决此问题：可以显式指定要调用的版本：

intmain（）{WirelessAdapter c54G{5442181742}；标准：：cout<<c54G。USB设备：：getID（）；返回0；}

虽然这个变通方法相当简单，但您可以看到当您的类继承自四个或六个基类（这些基类本身继承自其他类）时，事情是如何变得复杂的。当您继承更多的类时，命名冲突的可能性呈指数级增加，并且每个命名冲突都需要显式地解决。

第二，也是更严重的是钻石问题，你的作者喜欢称之为“末日钻石”。当一个类从两个类进行乘法继承时，会发生这种情况，每个类都从单个基类继承。这导致了菱形继承模式。

例如，考虑以下一组类：

类PoweredDevice{}；类扫描仪：公共PoweredDevice{}；类打印机：公共PoweredDevice{}；类复印机：公共扫描仪，公共打印机{}；

扫描仪和打印机都是供电设备，因此它们源自PoweredDevice。然而，复印机结合了扫描仪和打印机的功能。

在这种情况下会出现许多问题，包括Copier是否应该具有PoweredDevice的一个或两个副本，以及如何解决某些类型的不明确引用。虽然大多数这些问题都可以通过显式作用域来解决，但为了处理增加的复杂性而添加到类中的维护开销可能会导致开发时间激增。在下一章（第25.8课——虚拟基类）中，我们将更多地讨论解决菱形问题的方法。

多重继承是否比它的价值更麻烦？

事实证明，使用多重继承可以解决的大多数问题也可以使用单一继承来解决。许多面向对象的语言（例如Smalltalk、PHP）甚至不支持多重继承。许多相对现代的语言（如Java和C#）将类限制为普通类的单个继承，但允许接口类的多个继承（我们将在后面讨论）。在这些语言中不允许多重继承背后的驱动思想是，它只会使语言过于复杂，并最终导致比修复更多的问题。

许多作者和经验丰富的程序员认为，C++中的多重继承应该不惜一切代价避免，因为它会带来许多潜在的问题。您的作者不同意这种方法，因为在某些情况下，多重继承是继续进行的最佳方法。然而，应该非常明智地使用多重继承。

有趣的是，您已经在使用使用多重继承编写的类，而不知道它：iostream库对象std:：cin和std:∶cout都是使用多重继承实现的！

***

