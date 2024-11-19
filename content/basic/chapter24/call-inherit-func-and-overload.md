---
title: "调用继承的函数与重写行为"
date: 2024-10-08T17:45:57+08:00
---

默认情况下，派生类继承基类中定义的所有行为。在本课中，我们将更详细地检查如何选择成员函数，以及如何来更改派生类中的行为。

在派生类对象上调用成员函数时，编译器首先查看派生类中是否存在具有该名称的函数。如果是，则考虑具有该名称的所有重载函数，并使用函数重载解析过程来确定是否存在最佳匹配。如果不是，编译器将遍历继承链，以相同的方式依次检查每个层级中的父类。

换句话说，编译器将选择最匹配的继承链最下层的函数。

***
## 调用基类函数

首先，让我们研究当派生类没有匹配函数，但基类有匹配函数时会发生什么:

```C++
#include <iostream>

class Base
{
public:
    Base() { }

    void identify() const { std::cout << "Base::identify()\n"; }
};

class Derived: public Base
{
public:
    Derived() { }
};

int main()
{
    Base base {};
    base.identify();

    Derived derived {};
    derived.identify();

    return 0;
}
```

这将打印:

```C++
Base::identify()
Base::identify()
```

当调用base.identify()时，编译器会查看名为identify()的函数是否已在类base中定义。有，因此编译器会查看它是否匹配。是的，所以它被调用。

当调用derived.identify()时，编译器会查看是否在derived类中定义了名为identify()的函数。没有。因此移动到父类（在本例中为Base），并在那里重新查找。Base定义了identify()函数，因此它使用该函数。换句话说，使用Base::identity()是因为Derived::identify()不存在。

这意味着，如果基类提供的行为足够，可以简单地直接使用基类行为。

***
## 重新定义行为

然而，如果我们在Derived类中定义了Derived::identify（），则会改用它。

这意味着，通过在派生类中重新定义函数，我们可以使函数以不同的方式与派生类一起工作！

例如，假设我们希望derived.identify()打印derived::identify（可以简单地在Derived类中添加函数identify()，以便在使用Derived对象调用函数identity()时返回正确的响应。

要修改基类中定义的函数在派生类中的工作方式，只需在派生类内重新定义该函数。

```C++
#include <iostream>

class Base
{
public:
    Base() { }

    void identify() const { std::cout << "Base::identify()\n"; }
};

class Derived: public Base
{
public:
    Derived() { }

    void identify() const { std::cout << "Derived::identify()\n"; }
};

int main()
{
    Base base {};
    base.identify();

    Derived derived {};
    derived.identify();

    return 0;
}
```

这将打印:

```C++
Base::identify()
Derived::identify()
```

请注意，在派生类中重新定义函数时，派生函数不会继承基类中同名函数的访问说明符。它使用在派生类中定义的新的访问说明符。因此，在基类中定义为私有的函数可以在派生类中重新定义为public的，反之亦然！

```C++
#include <iostream>

class Base
{
private:
	void print() const 
	{
		std::cout << "Base";
	}
};
 
class Derived : public Base
{
public:
	void print() const 
	{
		std::cout << "Derived ";
	}
};
 
 
int main()
{
	Derived derived {};
	derived.print(); // 调用 derived::print(), 它是 public
	return 0;
}
```

***
## 使用部分现有功能

有时，我们不想完全替换基类函数，而是希望在用派生对象调用时向其添加额外的功能。在上面的示例中，请注意Derived::identity()完全覆盖了Base::identify()！这可能不是我们想要的。可以让派生函数调用基类函数的版本（为了重用代码），然后添加其他功能。

要让派生函数调用同名的基类函数，只需执行普通函数调用，但在函数前面加上基类的作用域限定符。例如:

```C++
#include <iostream>

class Base
{
public:
    Base() { }

    void identify() const { std::cout << "Base::identify()\n"; }
};

class Derived: public Base
{
public:
    Derived() { }

    void identify() const
    {
        std::cout << "Derived::identify()\n";
        Base::identify(); // 注 这里调用 Base::identify()
    }
};

int main()
{
    Base base {};
    base.identify();

    Derived derived {};
    derived.identify();

    return 0;
}
```

这将打印:

```C++
Base::identify()
Derived::identify()
Base::identify()
```

当执行derived.identity()时，它解析为Derived::identify()。在打印“Derived::identify()”之后，调用Base::identity（），后者打印“Base::identify()”。

这应该是相当简单的。为什么需要使用作用域限定符（::）？如果我们这样定义了Derived::identify():

```C++
#include <iostream>

class Base
{
public:
    Base() { }

    void identify() const { std::cout << "Base::identify()\n"; }
};

class Derived: public Base
{
public:
    Derived() { }

    void identify() const
    {
        std::cout << "Derived::identify()\n";
        identify(); // 不使用作用域限定符，会调用Derived的identify()，会无限循环调用自身
    }
};

int main()
{
    Base base {};
    base.identify();

    Derived derived {};
    derived.identify();

    return 0;
}
```

在没有范围解析限定符的情况下调用函数identity（）将默认为当前类中的identify（），它将是Derived::identify（）。这将导致Derived::identify（）调用自身，这将导致无限递归！

在试图调用基类的友元函数（如 操作符<<）时，可能会需要一点小技巧。由于基类的友元函数实际上不是基类的一部分，因此使用域解析限定符将不起作用。相反，需要一种方法，使Derived类暂时看起来像基类，以便可以调用函数的正确版本。

幸运的是，使用static_cast很容易做到这一点。下面是一个示例:

```C++
#include <iostream>

class Base
{
public:
    Base() { }

	friend std::ostream& operator<< (std::ostream& out, const Base&)
	{
		out << "In Base\n";
		return out;
	}
};

class Derived: public Base
{
public:
    Derived() { }

 	friend std::ostream& operator<< (std::ostream& out, const Derived& d)
	{
		out << "In Derived\n";
		// static_cast 将 Derived 转换为 Base 对象, 所以可以调用正确的 operator<< 版本
		out << static_cast<const Base&>(d); 
		return out;
    }
};

int main()
{
    Derived derived {};

    std::cout << derived << '\n';

    return 0;
}
```

因为Derived是一个Base，所以我们可以将Derived对象static_cast为Base的引用，以便调用使用Base的适当版本的 operator<<。

这将打印:

```C++
In Derived
In Base
```

***
## 派生类中的重载解析

如课程顶部所述，编译器将选择最匹配的继承链最下层的函数。

首先，让我们看一个简单的例子，其中有重载的成员函数:

```C++
#include <iostream>

class Base
{
public:
    void print(int)    { std::cout << "Base::print(int)\n"; }
    void print(double) { std::cout << "Base::print(double)\n"; }
};

class Derived: public Base
{
public:
};


int main()
{
    Derived d{};
    d.print(5); // 调用 Base::print(int)

    return 0;
}
```

对于调用d.print(5)，编译器在Derived中找不到名为print()的函数，因此它检查Base，其中找到两个同名函数。它使用函数重载解析过程来确定Base::print(int)比Base::print(double)更好的匹配。因此，Base::print(int)被调用，就像我们预期的那样。

现在，让我们来看一个行为不像我们预期的情况:

```C++
#include <iostream>

class Base
{
public:
    void print(int)    { std::cout << "Base::print(int)\n"; }
    void print(double) { std::cout << "Base::print(double)\n"; }
};

class Derived: public Base
{
public:
    void print(double) { std::cout << "Derived::print(double)"; } // 新增的函数
};


int main()
{
    Derived d{};
    d.print(5); // 调用 Derived::print(double), 而不是 Base::print(int)

    return 0;
}
```

对于调用d.print(5)，编译器在Derived中找到一个名为print()的函数，因此在尝试确定要解析到的函数时，它将先仅考虑Deriveed中的函数。对于此函数调用，也是Derived中的最佳匹配函数。因此，这将调用Derived::print(double)。

由于Base::print(int)的一个参数与int参数5的匹配程度高于Derived::print(double) ，因此您可能期望此函数调用解析为Base::print。但由于d是Derived，Deriveed中至少有一个print()函数，并且Derived在Base的继承链的更下层，因此甚至不考虑Base中的函数。

那么，如果我们确实希望d.print(5)解析为Base::print(int)，该怎么办？一种不太好的方法是定义Derived::print(int):

```C++
#include <iostream>

class Base
{
public:
    void print(int)    { std::cout << "Base::print(int)\n"; }
    void print(double) { std::cout << "Base::print(double)\n"; }
};

class Derived: public Base
{
public:
    void print(int n) { Base::print(n); } // 可以，但不是最优方式
    void print(double) { std::cout << "Derived::print(double)"; }
};

int main()
{
    Derived d{};
    d.print(5); // 调用 Derived::print(int), 其中调用 Base::print(int)

    return 0;
}
```

虽然这是可行的，但并不太好，因为我们必须为希望落入Base的每个函数重载添加一个函数到Derived。这可能是许多额外的函数，本质上只是将调用路由到Base。

更好的选择是在Derived声明需要使用的Base函数:

```C++
#include <iostream>

class Base
{
public:
    void print(int)    { std::cout << "Base::print(int)\n"; }
    void print(double) { std::cout << "Base::print(double)\n"; }
};

class Derived: public Base
{
public:
    using Base::print; // 让 Base::print() 函数可以在Derived被重载解析
    void print(double) { std::cout << "Derived::print(double)"; }
};


int main()
{
    Derived d{};
    d.print(5); // 调用 Base::print(int), 这是 Derived 中可以看到的最优匹配

    return 0;
}
```

通过放置using声明Base::print；在Derived中，我们告诉编译器，所有名为print的基类函数都应该在Derived中可见，这将导致它们符合重载解析的条件。因此，Base::print(int) 被选中，而不是 Derived::print(double)。

***

{{< prevnext prev="/basic/chapter24/add-new-func-to-derived-class/" next="/basic/chapter24/hide-inherit-func/" >}}
24.5 向派生类添加新功能
<--->
24.7 隐藏继承的功能
{{< /prevnext >}}
