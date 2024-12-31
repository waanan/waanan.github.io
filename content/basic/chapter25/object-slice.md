---
title: "对象切片（Object slicing）"
date: 2024-11-04T13:14:53+08:00
---

让我们回到前面看到的示例：

```C++
#include <iostream>
#include <string_view>

class Base
{
protected:
    int m_value{};

public:
    Base(int value)
        : m_value{ value }
    {
    }

    virtual ~Base() = default;

    virtual std::string_view getName() const { return "Base"; }
    int getValue() const { return m_value; }
};

class Derived: public Base
{
public:
    Derived(int value)
        : Base{ value }
    {
    }

   std::string_view getName() const override { return "Derived"; }
};

int main()
{
    Derived derived{ 5 };
    std::cout << "derived is a " << derived.getName() << " and has value " << derived.getValue() << '\n';

    Base& ref{ derived };
    std::cout << "ref is a " << ref.getName() << " and has value " << ref.getValue() << '\n';

    Base* ptr{ &derived };
    std::cout << "ptr is a " << ptr->getName() << " and has value " << ptr->getValue() << '\n';

    return 0;
}
```

在上面的示例中，ref引用和ptr指向derived，derived具有Base和Derived分别的部分。因为ref和ptr的类型是Base，所以ref和ptr只能看到派生的Base部分——派生的Derived部分仍然存在，但不能通过ref或ptr看到。然而，通过使用虚函数，我们可以访问函数的最底层派生版本。因此，上面的程序打印：

```C++
derived is a Derived and has value 5
ref is a Derived and has value 5
ptr is a Derived and has value 5
```

但是，如果我们不是设置Base引用或指针，而是简单地将Derived对象分配给Base对象，会发生什么情况？


```C++
int main()
{
    Derived derived{ 5 };
    Base base{ derived }; // 这里会发生什么?
    std::cout << "base is a " << base.getName() << " and has value " << base.getValue() << '\n';

    return 0;
}
```

请记住，derived有Base和Derived分别的部分。将Derived对象指定给Base对象时，仅复制衍生对象的Base部分，Derived部分不复制。在上面的示例中，base接收derived的Base部分的副本，但不接收Derived部分的副本。该对象已被有效地“切割”。

因此，将派生类对象分配给基类对象被称为对象切片（或简称切片）。因为base是一个Base对象，所以base的虚函数指针仍然指向Base。因此，base.getName()解析为Base::getName()。

上面的示例打印：

```C++
base is a Base and has value 5
```

小心使用，切片功能是有用的。然而，如果使用不当，切片可能会以许多不同的方式导致意外的结果。让我们来看看其中的一些情况。

***
## 切片和函数

现在，您可能会认为上面的示例有点傻。毕竟，为什么要这样将派生类赋值给基类？然而，切片更可能在函数中意外发生。

考虑以下函数：

```C++
void printName(const Base base) // 注: 按值传递，而不是按引用传递
{
    std::cout << "I am a " << base.getName() << '\n';
}
```

上面的函数很简单，但是如果我们使用如下的方式进行调用呢？

```C++
int main()
{
    Derived d{ 5 };
    printName(d); // 哦，可能会有疏漏，没有意识到这里是按值传递的对象

    return 0;
}
```

编写此程序时，您可能没有注意到base是一个按值传递参数，而不是按引用传递的参数。因此，当被调用为printName(d)时，虽然我们可能期望base.getName()调用虚函数getName()并打印“I am a Derived”，但事实并非如此。相反，将对Derived对象d进行切片，并且仅将Base部分复制到base参数中。当base.getName()执行时，即使getName()函数是虚函数，也没有类的Derived部分可供其解析。

因此，该程序打印：

```C++
I am a Base
```

在这种情况下，发生了什么是很明显的，但如果您的函数实际上没有打印这样的任何标识信息，则跟踪错误可能是一项挑战。

当然，通过将函数参数设置为引用而不是传递值，可以很容易地避免这里的切片。

```C++
void printName(const Base& base) // 注: 现在是按引用传递
{
    std::cout << "I am a " << base.getName() << '\n';
}

int main()
{
    Derived d{ 5 };
    printName(d);

    return 0;
}
```

这打印出：

```C++
I am a Derived
```

***
## 切片和数组

新程序员在切片方面遇到麻烦的另一个领域是尝试用std::vector实现多态性。考虑以下程序：

```C++
#include <vector>

int main()
{
	std::vector<Base> v{};
	v.push_back(Base{ 5 });    // 将Base对象添加到vector
	v.push_back(Derived{ 6 }); // 将Derived对象添加到vector

    // 打印vector中的所有元素
	for (const auto& element : v)
		std::cout << "I am a " << element.getName() << " with value " << element.getValue() << '\n';

	return 0;
}
```

这个程序编译得很好。但在运行时，它会打印：

```C++
I am a Base with value 5
I am a Base with value 6
```

类似于前面的示例，因为std::vector被声明为Base类型的数组，当Derived(6)被添加到数组时，它被切片。

解决这个问题有点困难。许多新程序员尝试创建包含引用的std::vector，如下所示：

```C++
std::vector<Base&> v{};
```

不幸的是，这无法编译。std::vector的元素必须是可赋值的，引用只能被初始化一次，不能重新赋值。

解决此问题的一种方法是创建指针数组：

```C++
#include <iostream>
#include <vector>

int main()
{
	std::vector<Base*> v{};

	Base b{ 5 }; // b 和 d 不能是匿名对象
	Derived d{ 6 };

	v.push_back(&b); // 将Base对象添加到vector
	v.push_back(&d); // 将Derived对象添加到vector

	// 打印vector中的所有元素
	for (const auto* element : v)
		std::cout << "I am a " << element->getName() << " with value " << element->getValue() << '\n';

	return 0;
}
```

这打印：

```C++
I am a Base with value 5
I am a Derived with value 6
```

这很有效！但是，首先，nullptr现在是一个有效的选项，这可能是可取的，也可能是不可取的。其次，您现在必须处理指针语义，这可能会很尴尬。但好处是，使用指针允许我们将动态分配的对象放在向量中（只是不要忘记显式删除它们）。

另一个选项是使用std::reference_wrapper，这是一个模拟可重新赋值的引用的类：

```C++
#include <functional> // for std::reference_wrapper
#include <iostream>
#include <string_view>
#include <vector>

class Base
{
protected:
    int m_value{};

public:
    Base(int value)
        : m_value{ value }
    {
    }
    virtual ~Base() = default;

    virtual std::string_view getName() const { return "Base"; }
    int getValue() const { return m_value; }
};

class Derived : public Base
{
public:
    Derived(int value)
        : Base{ value }
    {
    }

    std::string_view getName() const override { return "Derived"; }
};

int main()
{
	std::vector<std::reference_wrapper<Base>> v{}; // Base 中包含可 reference_wrapper

	Base b{ 5 }; // b 和 d 不能是匿名对象
	Derived d{ 6 };

	v.push_back(b); // 将Base对象添加到vector
	v.push_back(d); // 将Derived对象添加到vector

	// 打印vector中的所有元素
	// 使用 .get() 获取 std::reference_wrapper 中的元素
	for (const auto& element : v) // element 的类型为 std::reference_wrapper<Base>&
		std::cout << "I am a " << element.get().getName() << " with value " << element.get().getValue() << '\n';

	return 0;
}
```

***
## 破碎的对象

在上面的例子中，我们看到了切片导致错误结果的情况。现在，让我们来看另一个存在的危险情况！

考虑以下代码：

```C++
int main()
{
    Derived d1{ 5 };
    Derived d2{ 6 };
    Base& b{ d2 };

    b = d1; // 这一行有问题

    return 0;
}
```

函数中的前三行非常简单。创建两个Derived对象，并将“Base”引用设置为第二个对象。

第四行是事情误入歧途的地方。由于b指向d2，我们将d1赋给b，你可能会认为结果是d1会被复制到d2中。但b是一个Base，C++为类提供的操作符=在默认情况下不是虚函数。因此，将调用Base的赋值运算符，并且仅将d1的Base部分复制到d2中。

因此，您将发现d2现在具有d1的Base部分和d2的Derived部分。在这个特定的示例中，这不是问题（因为Derived类没有自己的数据），但在大多数情况下，您就会创建出一个破碎的对象——由多个对象的部分组成。

更糟糕的是，没有简单的方法来防止这种情况发生（除了尽可能避免编写这样的代码）。

如果基类不是设计为需要实例化的（例如，它只是一个接口类），则可以通过使基类不可复制来避免切片（通过删除基类拷贝构造函数和赋值运算符）。

***
## 结论

尽管C++支持通过对象切片将派生对象分配给基类对象，但一般来说，这可能只会导致头痛的问题，通常应该尽量避免切片。确保函数参数是引用（或指针），并在涉及派生类时尝试避免任何类型的值传递。

***