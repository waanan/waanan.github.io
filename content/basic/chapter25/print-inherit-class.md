---
title: "使用运算符<<打印继承的类"
date: 2024-11-04T13:14:53+08:00
---

考虑使用虚函数的以下程序：

```C++
#include <iostream>

class Base
{
public:
	virtual void print() const { std::cout << "Base";  }
};

class Derived : public Base
{
public:
	void print() const override { std::cout << "Derived"; }
};

int main()
{
	Derived d{};
	Base& b{ d };
	b.print(); // 会调用 Derived::print()

	return 0;
}
```

到目前，您应该已经了解b.print()将调用Derived::print()这一事实（因为b引用的是Derived类对象，Base::print()是一个虚函数，Derived::print()是子类重写的实现）。

虽然这样调用成员函数来进行输出是可以的，但这种类型的函数与std::cout不能很好地混合使用。

```C++
#include <iostream>

int main()
{
	Derived d{};
	Base& b{ d };

	std::cout << "b is a ";
	b.print(); // 这里使用我们自己的打印函数，中断了cout
	std::cout << '\n';

	return 0;
}
```

在本课中，我们将研究如何为使用继承的类重写运算符<<，如下所示：

```C++
std::cout << "b is a " << b << '\n'; // 更好的版本
```

***
## 使用「操作符<<」的挑战

让我们从重载操作符<<<开始，以典型的方式：

#include<iostream>class-Base{public:virtual-Voidprint（）const{std:：cout<<“Base”；}friend-std:：ostream&operator<<（std::ostream＆out，const-Base&b）{out<<“Base”；return-out；}}；派生的类：public Base{public:void print（）const override{std:：cout<<“Derived”；}friend std::ostream&operator<<（std::ostream&out，const Derived&d）{out<<“Delived”；return out；}}；int main（）{基数b{}；标准：：cout<<b<<'\n'；派生d{}；标准：：cout<<d<<'\n'；返回0；}

因为这里不需要虚拟函数解析，所以该程序按预期工作，并打印：

Base Derived Now，

考虑下面的main（）函数：

intmain（”{Derivedd{}；基&bref{d}；标准：：cout<<bref<<'\n'；返回0；}

这个程序打印：

Base

这可能不是我们期望的。发生这种情况是因为处理基本对象的运算符<<的版本不是虚拟的，因此std:：cout<<bref调用处理基本对象而不是派生对象的运算符<的版本。

这就是挑战所在。

我们可以使运算符<<虚拟吗？

如果这个问题是操作符<<不是虚拟的，我们不能简单地将其虚拟化吗？

简而言之，答案是否定的。

这有许多原因。

首先，只有成员函数可以虚拟化——这是有意义的，因为只有类可以从其他类继承，并且没有办法覆盖位于类之外的函数（您可以重载非成员函数，但不能覆盖它们）。由于我们通常将操作符<<实现为友元，并且友元不被视为成员函数，因此操作符<<<的友元版本不符合虚拟化的条件。（有关我们为什么以这种方式实现运算符<<的回顾，请重新访问第21.5课——使用成员函数重载运算符）。

其次，即使我们可以虚拟化运算符<<，也存在这样的问题：Base:：operator<<和Derived:：operator<<的函数参数不同（基本版本将采用Base参数，而派生版本将采用Derived参数）。因此，派生版本不会被视为基本版本的覆盖，因此不符合虚拟函数解析的条件。

那么，程序员应该做什么呢？

一个解决方案

答案，正如它所证明的，出奇地简单。

首先，我们像往常一样在基类中设置操作符<<作为朋友。但不是让操作符<<确定要打印的内容，而是让它调用可以虚拟化的普通成员函数！这个虚拟函数将完成确定每个类要打印的内容的工作。

在第一个解决方案中，我们的虚拟成员函数（我们称为identify（））返回一个std:：string，它由Base:：operator打印<<：

#include<iostream>class-Base{public://这是我们的重载操作符<<friend std::ostream&operator<<（std::ostream&out，const Base&b：：string identity（）const{return“Base”；}}；类Derived:public Base{public://这是我们的override identity（）函数，用于处理Derived case std:：string identify（）const override{return“Deriveed”；}}；int main（）{基数b{}；标准：：cout<<b<<'\n'；派生d{}；标准：：cout<<d<<'\n'；//请注意，即使没有显式处理派生对象Base&bref{d}的运算符<<，也可以使用该方法；标准：：cout<<bref<<'\n'；返回0；}

这将打印预期的结果：

Base Derived Derived.

让我们更详细地检查一下它是如何工作的。在Base b的情况下，使用引用Base对象的参数b调用运算符<<。虚函数调用b.identify（）因此解析为Base:：identify（），它返回要打印的“Base”。这里没什么特别的。

在Derived的情况下，编译器首先查看是否存在接受Derived对象的运算符<<。没有一个，因为我们没有定义一个。接下来，编译器查看是否存在接受Base对象的运算符<<。是的，因此编译器将Derived对象隐式上转换为Base&并调用函数（我们可以自己进行上转换，但编译器在这方面很有帮助）。因为参数b引用的是Derived对象，所以虚函数调用b.identify（）解析为Derived:：identify（.），它返回要打印的“Derived.”。

请注意，我们不需要为每个派生类定义运算符<<！处理Base对象的版本对于Base对象和从Base派生的任何类都很好！

第三种情况是前两种情况的混合。首先，编译器将变量bref与接受Base引用的运算符<<匹配。由于参数b引用的是Derived对象，因此b.identity（）解析为Derived:：identify（），它返回“Derived.”。

问题已解决。

更灵活的解决方案

上述解决方案工作良好，但有两个潜在的缺点：

它假设所需的输出可以表示为单个std:：string.

Our Identification（）成员函数不能访问流对象。

后者在需要流对象的情况下是有问题的，例如当我们想要打印具有重载运算符<<的成员变量的值时。

幸运的是，可以直接修改上面的示例来解决这两个问题。在以前的版本中，虚拟函数identify（）返回了一个字符串，由Base:：operator<<打印。在这个版本中，我们将改为定义虚拟成员函数print（），并将直接打印的责任委托给该函数。

下面是一个说明想法的示例：

#include<iostream>class-Base{public://这是我们的重载操作符<<friend std:：ostream&operator<<（std::ostream＆out，const Base&b）{//将打印责任委托给虚拟成员函数print（）return b.print（out）；}//我们将依赖成员函数prind（）来执行实际的打印//因为print（/年具有重载运算符<<struct Employee{std:：string name{}的某个类或结构；整数id{}；friend std:：ostream&operator<<（std::：ostream&out，const Employee&e）{out<<“员工（”<<e.name<<“，”<<e.id<<“）”；return out；}}；派生的类：公共基{private:Employee m_e{}；//Derived现在有一个Employee成员public:Deriveed（const Employer&e）：m_e{e}{}//这是我们的override print（）函数，用于处理Derived-case std:：ostream&print（std:∶ostream&out）const override{out<<“Derived:”；//使用流对象out<<m_e；return out；}}打印员工成员；int main（）{基数b{}；标准：：cout<<b<<'\n'；派生d{Employee{“Jim”，4}}；标准：：cout<<d<<'\n'；//请注意，即使没有显式处理派生对象Base&bref{d}的运算符<<，也可以使用该方法；标准：：cout<<bref<<'\n'；返回0；}

此输出：

Base Derived:Employee（Jim，4）Derived:Employme（Jim，4）

在此版本中，Base:：operator<<本身不进行任何打印。相反，它只是调用虚拟成员函数print（）并将其传递给流对象。然后，print（）函数使用该流对象进行自己的打印。Base:：print（）使用流对象打印“Base”。更有趣的是，Derived:：print（）使用流对象来打印“Derived:”，并调用Employee:：operator<<来打印成员m_e的值。在前面的示例中，后者可能更具挑战性！

***